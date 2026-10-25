"""Reflection bench v1 runner: scores local open models on R1, R2, R4-decide and R7 automatically, and
saves R3/R4/R5 talk replies for blind judging. R6 (speed) is measured on every call.

Local only (llama-server on loopback), $0, no mic or speaker. It runs one server at a time and stops only PIDs it spawned.
Usage: python3 -I reflection_bench.py OUT_DIR --split dev|gate --decide KEY=GGUF,... --talk KEY=GGUF,...
The gate split is held out and not published.
"""
import argparse, json, os, re, signal, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SYSTEM_PROMPT = open(f'{HERE}/../tasks/reflection/talk-system-prompt.txt').read()

PORT = 8096
INTENTS = ['question', 'statement', 'remember', 'correct', 'small_talk', 'act', 'not_addressed']
DECIDE_SYS = """You are the reflection step of Unfold, a personal AI agent. For the person's latest utterance, output only JSON.
intent: question (asks for information) | statement (comment, feeling, passing info, nothing to store) | remember (a durable fact about the person, or an explicit ask to remember) | correct (fixes something said or stored before) | small_talk (greeting, thanks, banter) | act (asks the agent to do something with a tool or the outside world) | not_addressed (not meant for the agent: someone else in the room, TV, self-talk, a fragment).
recall: true if answering well needs stored memories about the person or past conversations.
timing: now (reply right away) | wait (stay silent: unfinished, or not addressed) | escalate (needs a bigger model, a tool, or long work)."""
R1_SCHEMA = {'type': 'object', 'properties': {'intent': {'enum': INTENTS}, 'recall': {'type': 'boolean'}, 'timing': {'enum': ['now', 'wait', 'escalate']}}, 'required': ['intent', 'recall', 'timing']}
R4_SYS = """You are the reflection step of Unfold. Given the stored memories offered for this turn and the person's question, decide whether the memories alone answer it. Output only JSON: {"gold": "answer" or "abstain"}. If two memories conflict and one is clearly newer or a correction, the newer one counts. Never answer from guesses."""
R4_SCHEMA = {'type': 'object', 'properties': {'gold': {'enum': ['answer', 'abstain']}}, 'required': ['gold']}
R7_SYS = """You are the reflection step of Unfold. For the person's latest message in this conversation, choose the agent's move. Output only JSON: {"move": "talk" | "act" | "ask"}.
talk = just reply; act = call a tool (reminder, message, search, calendar, timer, music) because everything needed is known; ask = one clarifying question, because something needed is missing or ambiguous."""
R7_SCHEMA = {'type': 'object', 'properties': {'move': {'enum': ['talk', 'act', 'ask']}}, 'required': ['move']}


def call(messages, schema=None, max_tokens=220, temperature=0.3):
    body = {'messages': messages, 'stream': True, 'temperature': temperature, 'seed': 7, 'max_tokens': max_tokens,
            'chat_template_kwargs': {'enable_thinking': False}}
    if schema:
        body['response_format'] = {'type': 'json_schema', 'json_schema': {'name': 'out', 'schema': schema}}
        body['temperature'] = 0
    req = urllib.request.Request(f'http://127.0.0.1:{PORT}/v1/chat/completions', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    t0 = time.monotonic(); first = None; text = ''; timings = None; finish = None
    with urllib.request.urlopen(req, timeout=120) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith('data:') or line == 'data: [DONE]':
                continue
            ev = json.loads(line[5:]); timings = ev.get('timings') or timings
            for ch in ev.get('choices', []):
                d = (ch.get('delta') or {}).get('content') or ''
                if d and first is None:
                    first = time.monotonic()
                text += d; finish = ch.get('finish_reason') or finish
    t1 = time.monotonic()
    return {'text': text, 'finish': finish, 'ttft_ms': round(((first or t1) - t0) * 1000, 1), 'total_ms': round((t1 - t0) * 1000, 1),
            'tok_s': timings and round(timings.get('predicted_per_second', 0), 1)}


def parsed(r):
    try:
        return json.loads(r['text']) if r['finish'] == 'stop' else None
    except Exception:
        return None


# ---- R2: machine-checkable output rules
def check(c, reply):
    t, v, s = c['type'], c.get('value'), reply.strip()
    words = re.findall(r"\w[\w'’-]*", s)
    if t == 'max_words': return len(words) <= int(v)
    if t == 'one_sentence': return len([x for x in re.split(r'(?<=[.!?])\s+', s) if x.strip()]) == 1
    if t == 'yes_no_only': return re.fullmatch(r'(sim|não|nao|yes|no)[.!]?', s.lower()) is not None
    if t == 'starts_with': return s.lower().startswith(str(v).lower())
    if t == 'ends_with': return s.lower().rstrip().endswith(str(v).lower())
    if t == 'include_word': return re.search(r'(?<!\w)' + re.escape(str(v).lower()) + r'(?!\w)', s.lower()) is not None
    if t == 'exclude_word': return re.search(r'(?<!\w)' + re.escape(str(v).lower()) + r'(?!\w)', s.lower()) is None
    if t == 'no_question': return '?' not in s
    if t == 'bullets_exact': return len([l for l in s.splitlines() if re.match(r'\s*([-*•]|\d+[.)])\s+', l)]) == int(v)
    if t == 'all_lowercase': return s == s.lower()
    if t == 'no_emoji': return re.search('[\U0001F300-\U0001FAFF☀-➿]', s) is None
    if t == 'json_keys':
        try:
            o = json.loads(re.sub(r'^```(json)?|```$', '', s).strip())
            return isinstance(o, dict) and sorted(o) == sorted(v)
        except Exception:
            return False
    raise ValueError(t)


def server(key, path, out):
    log = open(f'{out}/{key}.server.log', 'w')
    # LFM 2.5 2.6B's template always opens a thinking block; the memory bench fixed it with a zero reasoning budget.
    extra = ['--reasoning-budget', '0'] if key.startswith('lfm25-26b') else []
    p = subprocess.Popen(['llama-server', '-m', os.path.expanduser(path), '--host', '127.0.0.1', '--port', str(PORT), '-c', '8192', '-ngl', '99', '-fa', 'on', '--jinja'] + extra, stdout=log, stderr=subprocess.STDOUT)
    open(f'{out}/spawned-pids.txt', 'a').write(f'{p.pid} {key}\n')
    for _ in range(360):
        if p.poll() is not None: break
        try:
            if urllib.request.urlopen(f'http://127.0.0.1:{PORT}/health', timeout=2).status == 200: return p
        except Exception: pass
        time.sleep(0.5)  # bounded readiness wait; real work follows
    stop(p); raise RuntimeError(f'{key}: server not healthy')


def stop(p):
    p.send_signal(signal.SIGTERM)
    try: p.wait(timeout=20)
    except subprocess.TimeoutExpired: p.kill()


DONE = set()   # (model, task, id) already in results.jsonl: a rerun into the same OUT skips them
LANG = None    # --lang en: score only items in that input language


def load(sets, name, split):
    return [x for x in json.load(open(f'{sets}/{name}.json'))['items'] if x['split'] == split and not x.get('excluded') and not x.get('contested')
            and (LANG is None or x.get('lang') == LANG)]


def todo(key, task, x):
    return (key, task, x['id']) not in DONE


def run_decide(key, sets, split, w):
    call([{'role': 'system', 'content': DECIDE_SYS}, {'role': 'user', 'content': 'oi'}], R1_SCHEMA)  # warmup
    for x in load(sets, 'r1-route', split):
        if (key, 'R1', x['id']) in DONE: continue
        # One user message (some chat templates require strict user/assistant alternation).
        u = (f"Previous turn (agent): {x['prior']}\nLatest utterance: {x['utterance']}" if x.get('prior') else f"Latest utterance: {x['utterance']}")
        msgs = [{'role': 'system', 'content': DECIDE_SYS}, {'role': 'user', 'content': u}]
        r = call(msgs, R1_SCHEMA, max_tokens=40); o = parsed(r) or {}
        w({'task': 'R1', 'model': key, 'id': x['id'], 'lang': x['lang'], 'gold': {k: x[k] for k in ('intent', 'recall', 'timing')}, 'pred': o,
           'ok_intent': o.get('intent') == x['intent'], 'ok_recall': o.get('recall') == x['recall'], 'ok_timing': o.get('timing') == x['timing'], 'valid': bool(o)} | {k: r[k] for k in ('ttft_ms', 'total_ms')})
    for x in load(sets, 'r4-honest', split):
        if (key, 'R4-decide', x['id']) in DONE: continue
        mem = '\n'.join(f"[{m['id']}] {m['text']}" for m in x['memories']) or '(no memories offered)'
        r = call([{'role': 'system', 'content': R4_SYS}, {'role': 'user', 'content': f'Memories:\n{mem}\n\nQuestion: {x["utterance"]}'}], R4_SCHEMA, max_tokens=20); o = parsed(r) or {}
        w({'task': 'R4-decide', 'model': key, 'id': x['id'], 'lang': x['lang'], 'gold': x['gold'], 'pred': o.get('gold'), 'ok': o.get('gold') == x['gold'], 'valid': bool(o)} | {k: r[k] for k in ('ttft_ms', 'total_ms')})
    for x in load(sets, 'r7-converse', split):
        if (key, 'R7', f"{x['id']}#1") in DONE: continue
        hist = []
        for i, t in enumerate(x['turns']):
            hist.append({'role': 'user', 'content': t['user']})
            r = call([{'role': 'system', 'content': R7_SYS}] + hist, R7_SCHEMA, max_tokens=20); o = parsed(r) or {}
            if not t.get('excluded'): w({'task': 'R7', 'model': key, 'id': f"{x['id']}#{i + 1}", 'lang': x['lang'], 'gold': t['expected'], 'pred': o.get('move'), 'ok': o.get('move') == t['expected'], 'valid': bool(o)} | {k: r[k] for k in ('ttft_ms', 'total_ms')})
            hist.append({'role': 'assistant', 'content': f"[{t['expected']}]"})  # the gold move so far, so each turn is judged on its own


def run_talk(key, sets, split, w):
    sp = SYSTEM_PROMPT
    call([{'role': 'system', 'content': sp}, {'role': 'user', 'content': 'oi'}])  # warmup
    for x in load(sets, 'r2-obey', split):
        if (key, 'R2', x['id']) in DONE: continue
        r = call([{'role': 'system', 'content': sp}, {'role': 'user', 'content': x['prompt']}])
        w({'task': 'R2', 'model': key, 'id': x['id'], 'lang': x['lang'], 'constraint': x['constraint'], 'reply': r['text'], 'ok': r['finish'] == 'stop' and check(x['constraint'], r['text'])} | {k: r[k] for k in ('ttft_ms', 'total_ms', 'tok_s', 'finish')})
    for x in load(sets, 'r3-talk', split):
        if (key, 'R3', x['id']) in DONE: continue
        r = call([{'role': 'system', 'content': sp}] + [{'role': t['role'], 'content': t['text']} for t in x['turns']])
        w({'task': 'R3', 'model': key, 'id': x['id'], 'lang': x['lang'], 'reply': r['text']} | {k: r[k] for k in ('ttft_ms', 'total_ms', 'tok_s', 'finish')})
    for x in load(sets, 'r4-honest', split):
        if (key, 'R4-reply', x['id']) in DONE: continue
        mem = '\n'.join(f"- {m['text']}" for m in x['memories']) or '(none)'
        r = call([{'role': 'system', 'content': sp + f'\n\nMEMORIES OFFERED FOR THIS TURN (stored facts about the person; nothing else is known):\n{mem}'}, {'role': 'user', 'content': x['utterance']}])
        w({'task': 'R4-reply', 'model': key, 'id': x['id'], 'lang': x['lang'], 'reply': r['text']} | {k: r[k] for k in ('ttft_ms', 'total_ms', 'tok_s', 'finish')})
    for x in load(sets, 'r5-self', split):
        if (key, 'R5', x['id']) in DONE: continue
        r = call([{'role': 'system', 'content': sp}] + [{'role': t['role'], 'content': t['text']} for t in x['turns']])
        w({'task': 'R5', 'model': key, 'id': x['id'], 'lang': x['lang'], 'reply': r['text']} | {k: r[k] for k in ('ttft_ms', 'total_ms', 'tok_s', 'finish')})


def main():
    a = argparse.ArgumentParser()
    a.add_argument('out'); a.add_argument('--split', default='dev'); a.add_argument('--sets', default=f'{HERE}/../tasks/reflection')
    a.add_argument('--decide', default=''); a.add_argument('--talk', default=''); a.add_argument('--lang', default=None)
    o = a.parse_args()
    if o.split == 'gate' and os.environ.get('GATE_OK') != '1':
        sys.exit('gate split is held out and not published')
    os.makedirs(o.out, exist_ok=True)
    global LANG
    LANG = o.lang
    if os.path.exists(f'{o.out}/results.jsonl'):
        for l in open(f'{o.out}/results.jsonl'):
            r = json.loads(l)
            if r.get('task') != 'error': DONE.add((r['model'], r['task'], r['id']))
    f = open(f'{o.out}/results.jsonl', 'a')
    w = lambda r: (f.write(json.dumps(r, ensure_ascii=False) + '\n'), f.flush())
    for kind, spec, fn in (('decide', o.decide, run_decide), ('talk', o.talk, run_talk)):
        for item in filter(None, spec.split(',')):
            key, path = item.split('=', 1)
            try:
                p = server(key, path, o.out)
            except Exception as e:
                w({'task': 'error', 'model': key, 'kind': kind, 'error': str(e)[:300]}); print(kind, key, 'SERVER FAILED', flush=True); continue
            try: fn(key, o.sets, o.split, w)
            except Exception as e:
                w({'task': 'error', 'model': key, 'kind': kind, 'error': str(e)[:300]}); print(kind, key, 'FAILED', str(e)[:120], flush=True)
            finally: stop(p)
            print(kind, key, 'done', flush=True)


if __name__ == '__main__':
    main()
