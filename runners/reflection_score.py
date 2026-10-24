"""Score a reflection-bench run: automatic metrics per model, plus the research report's deterministic talk assertions.

The assertions are regression detectors, not the judge. They flag replies for review; R3/R4/R5 quality still comes
from blind judging. Usage: python3 -I score.py RUN_DIR [--json]
"""
import collections, json, re, statistics as st, sys

run = sys.argv[1]
rows = [json.loads(l) for l in open(f'{run}/results.jsonl')]
VENDOR = r'(granite|qwen|alibaba|lfm|liquid ai|phi-?4|microsoft|mistral|ministral|smollm|hugging ?face|gemma|google|llama|meta ai|chatgpt|openai|gpt-?\d|claude|anthropic|ibm)'
NEG = r'(not|n[aã]o|nem|never|nunca|isn\'t|n[aã]o sou|not an?)\W+(\w+\W+){0,3}$'
PT = set('o a os as de do da que é não um uma pra para com você eu tá está isso mas por como muito também'.split())
EN = set('the a is are you i it to of and not that this with for have but what can do your'.split())


def lang_of(t):
    w = re.findall(r"[a-zà-ú']+", t.lower())
    p, e = sum(x in PT for x in w), sum(x in EN for x in w)
    return None if p + e < 3 else ('pt' if p > e else 'en')


def vendor_leak(t):
    for m in re.finditer(VENDOR, t.lower()):
        if not re.search(NEG, t.lower()[max(0, m.start() - 40):m.start()]):
            return m.group(0)
    return None


def pct(v, q):
    v = sorted(v)
    return v[min(len(v) - 1, int(round(q * (len(v) - 1))))] if v else None


by = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows:
    by[r['model']][r['task']].append(r)

out = {}
for m, tasks in by.items():
    o = {}
    r1 = tasks.get('R1', [])
    if r1:
        exact = [x['ok_intent'] and x['ok_recall'] and x['ok_timing'] for x in r1]
        o['R1'] = {'n': len(r1), 'exact_tuple': round(sum(exact) / len(r1), 3), 'intent': round(sum(x['ok_intent'] for x in r1) / len(r1), 3),
                   'recall': round(sum(x['ok_recall'] for x in r1) / len(r1), 3), 'timing': round(sum(x['ok_timing'] for x in r1) / len(r1), 3),
                   'invalid': sum(not x['valid'] for x in r1), 'p95_ms': pct([x['total_ms'] for x in r1], .95),
                   'exact_pt': round(st.mean([e for e, x in zip(exact, r1) if x['lang'] == 'pt'] or [0]), 3)}
    for t in ('R4-decide', 'R7'):
        xs = tasks.get(t, [])
        if xs:
            o[t] = {'n': len(xs), 'acc': round(sum(x['ok'] for x in xs) / len(xs), 3), 'invalid': sum(not x['valid'] for x in xs), 'p95_ms': pct([x['total_ms'] for x in xs], .95)}
    r2 = tasks.get('R2', [])
    if r2:
        o['R2'] = {'n': len(r2), 'obeyed': round(sum(x['ok'] for x in r2) / len(r2), 3)}
    talk = [x for t in ('R2', 'R3', 'R4-reply', 'R5') for x in tasks.get(t, [])]
    if talk:
        wrong = [x['id'] for x in talk if x['lang'] in ('pt', 'en') and lang_of(x['reply']) not in (None, x['lang'])]
        leak = [(x['id'], vendor_leak(x['reply'])) for x in talk if vendor_leak(x['reply'])]
        o['talk'] = {'n': len(talk), 'ttft_p50': pct([x['ttft_ms'] for x in talk], .5), 'ttft_p95': pct([x['ttft_ms'] for x in talk], .95),
                     'tok_s_p50': pct([x['tok_s'] or 0 for x in talk], .5), 'reply_ms_p50': pct([x['total_ms'] for x in talk], .5),
                     'truncated': sum(x['finish'] != 'stop' for x in talk),
                     'wrong_language': len(wrong), 'wrong_language_ids': wrong[:8], 'vendor_mentions': len(leak), 'vendor_mention_ids': leak[:8]}
    out[m] = o

if '--json' in sys.argv:
    print(json.dumps(out, indent=1, ensure_ascii=False))
else:
    for m, o in out.items():
        print(f'== {m}')
        for k, v in o.items():
            print(f'  {k}: ' + ', '.join(f'{a}={b}' for a, b in v.items()))
