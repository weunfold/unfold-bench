"""Run the expression bench against an OpenAI-compatible chat endpoint, or a built-in stub with --dry-run.

  voice_expression_run.py --base-url URL --model NAME --api-key-file PATH [--cases FILE] [--out out/NAME.jsonl]
  voice_expression_run.py --dry-run --out out/dry-run.jsonl

Flags fall back to env: EXPR_BENCH_BASE_URL, EXPR_BENCH_MODEL, EXPR_BENCH_API_KEY_FILE (or EXPR_BENCH_API_KEY).
The key is read but never printed or written. Existing ids in --out are skipped, so an interrupted run resumes.
Each output line: {id, model, latency_ms, raw, error, finish_reason, usage, reasoning?}."""
import argparse, json, os, sys, time, urllib.error, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
T = HERE.parent / 'tasks' / 'voice-expression'
MOOD_DESC = {'neutral': 'plain and friendly', 'calm': 'soft, slow, reassuring', 'joy': 'bright and happy',
             'serious': 'firm and grave', 'surprised': 'amazed, lively', 'tired': 'low energy, sleepy', 'tender': 'warm, gentle, caring'}
CHANNEL = {'desktop': 'the Unfold desktop app on the Mac', 'whatsapp': 'WhatsApp', 'telegram': 'Telegram'}


def turn_facts(c):
    msg = c['channel'] != 'desktop'
    how = ('a voice note (you see its transcript)' if msg else 'dictated: the person spoke and you see the transcript') \
        if c['input_modality'] == 'dictated' else ('a text message' if msg else 'typed')
    yn = lambda b: 'yes' if b else 'no'
    return '\n'.join([f"- Channel: {CHANNEL[c['channel']]}", f'- This turn arrived as: {how}',
                      f"- Voice mode on the Mac: {c['voice_mode']}", f"- Speech muted: {yn(c['muted'])}",
                      f"- Mac output device busy: {yn(c['output_device_busy'])}", f"- Person at the Mac: {yn(c['person_present'])}"])


def system_prompt(case, template=None):
    t = template or (T / 'system_prompt.md').read_text()
    moods = '\n'.join(f'- `{m}`: {MOOD_DESC[m]}' for m in case['available_moods'])
    return t.replace('{{TURN_FACTS}}', turn_facts(case['context'])).replace('{{AVAILABLE_MOODS}}', moods)


def request_messages(case, template=None):
    return [{'role': 'system', 'content': system_prompt(case, template)}] + [
        {'role': m['role'], 'content': m['content'], **({'reasoning_content': ''} if REPLAY_REASONING and m['role'] == 'assistant' else {})}
        for m in case['messages']]


CUES = {'joy': ('got the job', 'passed', 'passei', 'promovid', 'baby', 'consegui', 'joke', 'piada', 'funny', 'kkkk', 'haha'),
        'serious': ('died', 'passed away', 'faleceu', 'morreu', 'enterro', 'cancelled', 'demitido', 'roubaram', 'malignant')}


def stub_reply(case, messages):
    """A deliberately naive replier for --dry-run: it reads only what a model sees (the facts and the chat), speaks iff the
    turn was dictated and not muted, ignores the device, voice mode, explicit requests and the content gate, picks a mood
    from keywords without checking the voice, and laughs whenever the person seems to joke or celebrate."""
    sysmsg, user = messages[0]['content'], messages[-1]['content'].lower()
    dictated = 'arrived as: dictated' in sysmsg or 'arrived as: a voice note' in sysmsg
    if not dictated or 'Speech muted: yes' in sysmsg:
        return 'Sure, here is my answer.' if case['lang'] == 'en' else 'Claro, aqui vai a resposta.'
    mood = next((m for m, cues in CUES.items() if any(k in user for k in cues)), 'neutral')
    laugh = '<laugh> ' if mood == 'joy' else ''
    body = 'Okay, here is my answer.' if case['lang'] == 'en' else 'Beleza, aqui vai a resposta.'
    if sum(map(ord, case['id'])) % 13 == 0:
        return f'[say:speech] {body}'  # a malformed marker now and then, like small models produce
    return f'⟨say:speech mood={mood}⟩\n{laugh}{body}'


REPLAY_REASONING = '--replay-reasoning' in sys.argv  # IFM: every assistant turn carries reasoning_content ('' is valid)

def call(base_url, model, key, messages, args):
    # Two budgets: the reply budget (--max-tokens) and a separate thinking budget. Some servers take max_tokens as the
    # reply budget alone; a bare llama-server counts thinking inside max_tokens, so --raw-endpoint sends their sum.
    body = {'model': model, 'messages': messages, 'temperature': args.temperature,
            'max_tokens': args.max_tokens + (args.think_budget if args.raw_endpoint else 0),
            **({'reasoning_effort': args.reasoning_effort} if args.reasoning_effort else {}),
            **({'thinking_budget_tokens': args.think_budget} if args.think_budget and not args.no_budget_field else {}),
            **({'chat_template_kwargs': json.loads(args.template_kwargs)} if args.template_kwargs else {})}
    req = urllib.request.Request(base_url.rstrip('/') + '/chat/completions', data=json.dumps(body).encode(), method='POST',
                                 headers={'Content-Type': 'application/json', **({'Authorization': f'Bearer {key}'} if key else {})})
    if not args.stream:
        with urllib.request.urlopen(req, timeout=args.timeout) as r:
            return json.load(r)
    # Streaming: time to the first token (reasoning or reply), to the first reply token, and decode time after the first
    # token, as on Artificial Analysis's speed charts (decode time excludes TTFT). Reassembled into the non-stream shape.
    req.data = json.dumps({**body, 'stream': True, 'stream_options': {'include_usage': True}}).encode()
    t0 = time.perf_counter(); first = first_reply = None; content, reasoning, finish, usage, model_id = [], [], None, None, None
    with urllib.request.urlopen(req, timeout=args.timeout) as r:
        for line in r:
            line = line.decode(errors='replace').strip()
            if not line.startswith('data:') or line == 'data: [DONE]': continue
            ev = json.loads(line[5:]); usage = ev.get('usage') or usage; model_id = ev.get('model') or model_id
            for ch in ev.get('choices') or []:
                d = ch.get('delta') or {}; now = time.perf_counter()
                if d.get('reasoning_content'): reasoning.append(d['reasoning_content']); first = first or now
                if d.get('content'): content.append(d['content']); first = first or now; first_reply = first_reply or now
                finish = ch.get('finish_reason') or finish
    end = time.perf_counter(); ms = lambda a: round((a - t0) * 1000, 1) if a else None
    return {'model': model_id, 'usage': usage,
            'choices': [{'finish_reason': finish, 'message': {'content': ''.join(content), 'reasoning_content': ''.join(reasoning)}}],
            '_timing': {'ttft_ms': ms(first), 'first_reply_ms': ms(first_reply), 'total_ms': ms(end),
                        'decode_ms': round((end - first) * 1000, 1) if first else None}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--cases', default=str(T / 'cases.jsonl'))
    ap.add_argument('--out')
    ap.add_argument('--base-url', default=os.environ.get('EXPR_BENCH_BASE_URL'))
    ap.add_argument('--model', default=os.environ.get('EXPR_BENCH_MODEL'))
    ap.add_argument('--api-key-file', default=os.environ.get('EXPR_BENCH_API_KEY_FILE'))
    ap.add_argument('--temperature', type=float, default=0.0)
    ap.add_argument('--template-kwargs', default=None, help='JSON for chat_template_kwargs, e.g. {"enable_thinking": false}')
    ap.add_argument('--stream', action='store_true', help='stream and record ttft_ms, first_reply_ms, decode_ms per reply')
    ap.add_argument('--replay-reasoning', action='store_true', help="send reasoning_content '' on history assistant turns")
    ap.add_argument('--no-budget-field', action='store_true', help='provider rejects thinking_budget_tokens (IFM): only widen max_tokens')
    ap.add_argument('--raw-endpoint', action='store_true', help='bare llama-server: max_tokens covers thinking too')
    ap.add_argument('--think-budget', type=int, default=0, help='thinking tokens allowed on top of the reply budget')
    ap.add_argument('--reasoning-effort', default=None, help='off | low | full (sent as reasoning_effort; omitted when unset)')
    ap.add_argument('--max-tokens', type=int, default=600)
    ap.add_argument('--timeout', type=float, default=120)
    ap.add_argument('--limit', type=int, help='only the first N cases')
    ap.add_argument('--dry-run', action='store_true', help='use the built-in stub; no network')
    args = ap.parse_args()

    if args.dry_run: model, key = 'stub-naive-v1', None
    else:
        if not args.base_url or not args.model: ap.error('--base-url and --model (or EXPR_BENCH_BASE_URL / EXPR_BENCH_MODEL) are required without --dry-run')
        model = args.model
        key = Path(args.api_key_file).expanduser().read_text().strip() if args.api_key_file else os.environ.get('EXPR_BENCH_API_KEY')
    out = Path(args.out or Path('out') / f"{model.replace('/', '_')}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)['id'] for l in open(out)} if out.exists() else set()
    cases = [json.loads(l) for l in open(args.cases)][:args.limit]
    template = (T / 'system_prompt.md').read_text()
    n_err = 0
    with open(out, 'a') as f:
        for case in cases:
            if case['id'] in done: continue
            messages = request_messages(case, template)
            row = {'id': case['id'], 'model': model, 'latency_ms': None, 'raw': None, 'error': None, 'finish_reason': None, 'usage': None}
            t0 = time.perf_counter()
            if args.dry_run:
                row.update(raw=stub_reply(case, messages), finish_reason='stop')
            else:
                try:
                    resp = call(args.base_url, model, key, messages, args)
                    ch = resp['choices'][0]; msg = ch.get('message') or {}
                    row.update(raw=msg.get('content'), finish_reason=ch.get('finish_reason'), usage=resp.get('usage'), model=resp.get('model') or model)
                    if msg.get('reasoning_content'): row['reasoning'] = msg['reasoning_content']
                    if resp.get('_timing'): row['timing'] = resp['_timing']
                except (urllib.error.URLError, TimeoutError, KeyError, IndexError, ValueError) as e:
                    detail = e.read().decode(errors='replace')[:300] if isinstance(e, urllib.error.HTTPError) else ''
                    row['error'] = f'{type(e).__name__}: {e} {detail}'.strip(); n_err += 1
            row['latency_ms'] = round((time.perf_counter() - t0) * 1000, 1)
            f.write(json.dumps(row, ensure_ascii=False) + '\n'); f.flush()
    print(json.dumps({'out': str(out), 'model': model, 'cases': len(cases), 'skipped_done': len(done), 'errors': n_err}))


if __name__ == '__main__':
    main()
