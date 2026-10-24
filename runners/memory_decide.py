#!/usr/bin/env python3
"""Memory decision benchmark. Zero spend against a local server, loopback only.

Sends the 24 dev request bodies in tasks/memory-decide/requests (instruction, payload and strict schema) to an
OpenAI-compatible chat endpoint, validates every answer with strict rules, and scores with tasks/memory-decide/criteria.json.

Usage: memory_decide.py <label> <base_url> <model> <out_dir> [--repeats N] [--ordered | --order k1,k2,k3,k4] [--instructions FILE]
  --ordered = --order decision,select,proposal,reason. --instructions replaces the system instruction
  (a tuning variant; the user payload and the scoring stay fixed).
  The API key, if the server needs one, comes from the env var BENCH_API_KEY only.
Protocol: 2 unscored warmups; a "cold" pass and a "warm" pass in fixed order (warm is scored); then N randomized
repeats (seed 7) of all 24 for latency statistics only."""
import json, os, random, sys, time, urllib.request, urllib.error

T = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks', 'memory-decide')
label, base, model, out = sys.argv[1:5]
repeats = int(sys.argv[sys.argv.index('--repeats') + 1]) if '--repeats' in sys.argv else 5
key = os.environ.get('BENCH_API_KEY')
os.makedirs(out, exist_ok=True)

cases = json.load(open(f'{T}/q-dev.json'))['cases']
criteria = json.load(open(f'{T}/criteria.json'))['q_dev']
by_case = {c['id']: json.load(open(f"{T}/requests/{c['id']}.json")) for c in cases}
assert len(by_case) == 24

# Variant: same schema, keys reordered (constrained decoding writes them in this order).
ORDER = (sys.argv[sys.argv.index('--order') + 1].split(',') if '--order' in sys.argv
         else ['decision', 'select', 'proposal', 'reason'] if '--ordered' in sys.argv else None)
assert ORDER is None or sorted(ORDER) == ['decision', 'proposal', 'reason', 'select']
ORDERED = ORDER is not None
INSTR_FILE = sys.argv[sys.argv.index('--instructions') + 1] if '--instructions' in sys.argv else None
INSTR = open(INSTR_FILE).read().strip() if INSTR_FILE else None

def ordered_schema(schema):
    order = ORDER
    s = dict(schema)
    s['properties'] = {k: schema['properties'][k] for k in order}
    s['required'] = order
    return s

DISCRIMINATED = '--schema' in sys.argv and sys.argv[sys.argv.index('--schema') + 1] == 'discriminated'

def discriminated_schema(case):
    """Design option (local measurement only): one branch per decision, so decoding cannot pair a
    decision with the wrong fields; select items and the correction target are limited to the
    offered (memory_id, revision) pairs. Answers still go through the strict validator."""
    pairs = [{'type': 'object', 'additionalProperties': False, 'required': ['memory_id', 'revision'],
              'properties': {'memory_id': {'const': c['memory_id']}, 'revision': {'const': c['revision']}}}
             for c in case['candidates']]
    empty = {'type': 'array', 'maxItems': 0, 'items': {'type': 'object'}}
    def branch(decision, reasons, select, proposal):
        props = {'reason': {'enum': reasons}, 'decision': {'const': decision}, 'select': select, 'proposal': proposal}
        o = [k for k in (ORDER or ['decision', 'select', 'proposal', 'reason'])]
        return {'type': 'object', 'additionalProperties': False, 'required': o, 'properties': {k: props[k] for k in o}}
    text = {'type': 'string', 'minLength': 1, 'maxLength': 280}
    out = [branch('no_op', ['not_relevant', 'uncertain'], empty, {'type': 'null'}),
           branch('propose_remember', ['new_fact'], empty,
                  {'type': 'object', 'additionalProperties': False, 'required': ['text', 'target'], 'properties': {'text': text, 'target': {'type': 'null'}}})]
    if pairs:
        out.insert(1, branch('recall', ['recall_needed', 'conflict'], {'type': 'array', 'minItems': 1, 'maxItems': min(3, len(pairs)), 'items': {'anyOf': pairs}}, {'type': 'null'}))
        out.append(branch('propose_correct', ['correction'], empty,
                          {'type': 'object', 'additionalProperties': False, 'required': ['text', 'target'], 'properties': {'text': text, 'target': {'anyOf': pairs}}}))
    return {'anyOf': out}

GRAMMAR = sys.argv[sys.argv.index('--grammar') + 1] if '--grammar' in sys.argv else None  # compact | mini

def lit(x):
    """A GBNF string literal for the exact text x."""
    return '"' + x.replace('\\', '\\\\').replace('"', '\\"') + '"'

def subsets(items):
    from itertools import combinations
    return [list(c) for n in range(1, min(3, len(items)) + 1) for c in combinations(items, n)]

STR = r'''str ::= "\"" ch+ "\""
ch ::= [^"\\\x00-\x1F]
'''

def compact_grammar(case):
    """Design option: the branch-per-decision contract as GBNF with NO whitespace (fewer output tokens)."""
    cands = case['candidates']
    pair = lambda c: json.dumps({'memory_id': c['memory_id'], 'revision': c['revision']}, separators=(',', ':'))
    order = ORDER or ['decision', 'select', 'proposal', 'reason']
    def branch(decision, reasons, select, proposal):
        parts = {'reason': '"\\"reason\\":" (' + ' | '.join(lit(json.dumps(r)) for r in reasons) + ')',
                 'decision': lit('"decision":' + json.dumps(decision)), 'select': '"\\"select\\":" ' + select, 'proposal': '"\\"proposal\\":" ' + proposal}
        return '"{" ' + ' "," '.join(parts[k] for k in order) + ' "}"'
    br = [branch('no_op', ['not_relevant', 'uncertain'], lit('[]'), lit('null')),
          branch('propose_remember', ['new_fact'], lit('[]'), '"{\\"text\\":" str ",\\"target\\":null}"')]
    if cands:
        sel = '(' + ' | '.join(lit('[' + ','.join(pair(c) for c in sub) + ']') for sub in subsets(cands)) + ')'
        br.insert(1, branch('recall', ['recall_needed', 'conflict'], sel, lit('null')))
        tgt = '(' + ' | '.join(lit(pair(c)) for c in cands) + ')'
        br.append(branch('propose_correct', ['correction'], lit('[]'), '"{\\"text\\":" str ",\\"target\\":" ' + tgt + ' "}"'))
    return 'root ::= ' + ' | '.join('(' + b + ')' for b in br) + '\n' + STR

def mini_grammar(case):
    """Design option: the model writes only the decision and ids; code fills reason and proposal text."""
    ids = [c['memory_id'] for c in case['candidates']]
    br = [lit('{"d":"no_op"}'), lit('{"d":"remember"}')]
    if ids:
        br.insert(0, '"{\\"d\\":\\"recall\\",\\"s\\":" (' + ' | '.join(lit(json.dumps(sub, separators=(',', ':'))) for sub in subsets(ids)) + ') "}"')
        br.append('"{\\"d\\":\\"correct\\",\\"t\\":" (' + ' | '.join(lit(json.dumps(i)) for i in ids) + ') "}"')
    return 'root ::= ' + ' | '.join(br) + '\n'

def mini_to_text(text, case, frozen):
    p = json.loads(frozen['input'][0]['content'][0]['text'])
    cands = {c['memory_id']: c for c in p['candidates']}
    m = json.loads(text)
    pr = lambda i: {'memory_id': i, 'revision': cands[i]['revision']}
    if m['d'] == 'recall':
        return json.dumps({'decision': 'recall', 'select': [pr(i) for i in m['s']], 'proposal': None, 'reason': 'conflict' if len(m['s']) > 1 else 'recall_needed'})
    if m['d'] == 'correct':
        return json.dumps({'decision': 'propose_correct', 'select': [], 'proposal': {'text': p['utterance'][:280], 'target': pr(m['t'])}, 'reason': 'correction'})
    if m['d'] == 'remember':
        return json.dumps({'decision': 'propose_remember', 'select': [], 'proposal': {'text': p['utterance'][:280], 'target': None}, 'reason': 'new_fact'})
    return json.dumps({'decision': 'no_op', 'select': [], 'proposal': None, 'reason': 'not_relevant'})

def chat_body(frozen, case=None):
    fmt = dict(frozen['text']['format'])
    if DISCRIMINATED:
        fmt['schema'] = discriminated_schema(case)
    elif ORDERED:
        fmt['schema'] = ordered_schema(fmt['schema'])
    if GRAMMAR:
        return {
            'model': model,
            'messages': [{'role': 'system', 'content': INSTR or frozen['instructions']},
                         {'role': 'user', 'content': frozen['input'][0]['content'][0]['text']}],
            'grammar': compact_grammar(case) if GRAMMAR == 'compact' else mini_grammar(case),
            'temperature': 0, 'max_tokens': 160, 'stream': False,
            'chat_template_kwargs': {'enable_thinking': False},
        }
    return {
        'model': model,
        'messages': [{'role': 'system', 'content': INSTR or frozen['instructions']},
                     {'role': 'user', 'content': frozen['input'][0]['content'][0]['text']}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': fmt['name'], 'strict': True, 'schema': fmt['schema']}},
        'temperature': 0, 'max_tokens': frozen['max_output_tokens'], 'stream': False,
        'chat_template_kwargs': {'enable_thinking': False},
    }

def offered(case):
    return {(c['memory_id'], c['revision']) for c in case['candidates']}

def validate(text, case):
    """Strict validation: strict shape, offered selections only."""
    if '<think>' in text:
        return 'thinking_emitted', None
    try:
        v = json.loads(text)
    except Exception:
        return 'schema_invalid', None
    if not isinstance(v, dict) or set(v) != {'decision', 'select', 'proposal', 'reason'}:
        return 'schema_invalid', None
    if v['decision'] not in ('no_op', 'recall', 'propose_remember', 'propose_correct'):
        return 'schema_invalid', None
    if v['reason'] not in ('recall_needed', 'not_relevant', 'new_fact', 'correction', 'uncertain', 'conflict'):
        return 'schema_invalid', None
    sel = v['select']
    if not isinstance(sel, list) or len(sel) > 3 or not all(isinstance(p, dict) and set(p) == {'memory_id', 'revision'} for p in sel):
        return 'schema_invalid', None
    pairs = [(p['memory_id'], p['revision']) for p in sel]
    if any(p not in offered(case) for p in pairs) or len(set(pairs)) != len(pairs):
        return 'invalid_selection', None
    prop, target = v['proposal'], None
    if prop is not None:
        if not isinstance(prop, dict) or set(prop) != {'text', 'target'} or not isinstance(prop['text'], str) or not (0 < len(prop['text']) <= 280):
            return 'schema_invalid', None
        if prop['target'] is not None:
            t = prop['target']
            if not isinstance(t, dict) or set(t) != {'memory_id', 'revision'}:
                return 'schema_invalid', None
            target = (t['memory_id'], t['revision'])
    k = v['decision']
    ok = {'no_op': not pairs and prop is None, 'recall': bool(pairs) and prop is None,
          'propose_remember': not pairs and prop is not None and target is None,
          'propose_correct': not pairs and prop is not None and target in offered(case)}[k]
    if not ok:
        return ('invalid_selection' if k == 'propose_correct' and target is not None else 'schema_invalid'), None
    return 'ok', {'kind': k, 'select': sorted(pairs), 'target': target}

def permitted(case, d):
    for p in case['permitted']:
        if p['decision'] != d['kind']:
            continue
        if 'select' in p and sorted((s['memory_id'], s['revision']) for s in p['select']) != d['select']:
            continue
        if 'target' in p and d['target'] != (p['target']['memory_id'], p['target']['revision']):
            continue
        return True
    return False

def call(case):
    body = json.dumps(chat_body(by_case[case['id']], case)).encode()
    rq = urllib.request.Request(f'{base}/chat/completions', data=body, headers={'content-type': 'application/json', **({'authorization': f'Bearer {key}'} if key else {})})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(rq, timeout=10) as r:
            raw = r.read()
        ms = (time.perf_counter() - t0) * 1000
        v = json.loads(raw)
        text = v['choices'][0]['message'].get('content') or ''
        if not text and '--answer-from-reasoning' in sys.argv:  # template forces <think>; grammar-constrained answer lands there
            text = v['choices'][0]['message'].get('reasoning_content') or ''
        raw_text = text
        if GRAMMAR == 'mini':
            try: text = mini_to_text(text, case, by_case[case['id']])
            except Exception: text = 'MINI_UNPARSEABLE:' + text
        outcome, d = validate(text, case)
        return {'case': case['id'], 'ms': round(ms, 1), 'raw_text': raw_text, 'outcome': outcome, 'decision': d, 'text': text,
                'usage': v.get('usage'), 'timings': v.get('timings'), 'model': v.get('model'),
                'reasoning_content': bool(v['choices'][0]['message'].get('reasoning_content'))}
    except Exception as e:
        return {'case': case['id'], 'ms': round((time.perf_counter() - t0) * 1000, 1), 'outcome': f'error:{type(e).__name__}', 'decision': None, 'text': str(e)[:200]}

def score(results):
    """Scoring rule: missing or failed = non-decision at +infinity."""
    by = {r['case']: r for r in results}
    s = dict(decisions_ok=0, exact_selection=0, selection_cases=0, proposal_violations=0, non_decisions=0, deadline_hits=0, n=24)
    lat = []
    for c in cases:
        r = by.get(c['id'])
        okd = bool(r and r['outcome'] == 'ok' and permitted(c, r['decision']))
        s['decisions_ok'] += okd
        if c['category'] in ('recall', 'corrected_current', 'conflict'):
            s['selection_cases'] += 1
            s['exact_selection'] += okd and r['decision']['kind'] == 'recall'
        if c['category'] in ('malicious', 'irrelevant') and r and r['outcome'] == 'ok' and r['decision']['kind'].startswith('propose'):
            s['proposal_violations'] += 1
        if not r or r['outcome'] != 'ok':
            s['non_decisions'] += 1
        s['deadline_hits'] += bool(r and r['outcome'] == 'ok' and r['ms'] <= criteria['modelled_remaining_budget_ms'])
        lat.append(r['ms'] if r and r['outcome'] == 'ok' else float('inf'))
    lat.sort()
    s['p95_ms'] = lat[22]
    s['v0_decisions_ok'] = 10
    s['pass'] = (s['decisions_ok'] >= criteria['decision_in_permitted_min'] and s['exact_selection'] >= criteria['exact_selection_min']
                 and s['proposal_violations'] <= criteria['proposals_on_malicious_or_irrelevant_max'] and s['non_decisions'] <= criteria['non_decisions_max']
                 and s['p95_ms'] <= criteria['warm_p95_ms_max'] and s['deadline_hits'] * 100 >= 24 * criteria['deadline_hit_min_pct'] and s['decisions_ok'] >= 10)
    s['misses'] = [c['id'] for c in cases if not (by.get(c['id']) and by[c['id']]['outcome'] == 'ok' and permitted(c, by[c['id']]['decision']))]
    return s

log = open(f'{out}/{label}-requests.jsonl', 'w')
def run(tag, seq):
    res = []
    for c in seq:
        r = call(c)
        r['pass'] = tag
        log.write(json.dumps(r) + '\n'); log.flush()
        res.append(r)
    return res

run('warmup', cases[:2])
cold = run('cold', cases)
warm = run('warm', cases)
rnd = random.Random(7)
rep = []
for i in range(repeats):
    seq = cases[:]
    rnd.shuffle(seq)
    rep += run(f'repeat{i}', seq)
allms = sorted(r['ms'] for r in warm + rep if r['outcome'] == 'ok')
pct = lambda q: allms[min(len(allms) - 1, max(0, int(round(q * len(allms) + 0.5)) - 1))] if allms else None
summary = {
    'label': label, 'schema_variant': ('grammar-' + GRAMMAR) if GRAMMAR else 'discriminated' if DISCRIMINATED else 'frozen', 'server_extra': os.environ.get('SERVER_EXTRA', ''), 'answer_from_reasoning': '--answer-from-reasoning' in sys.argv, 'ordered_schema': ORDERED, 'key_order': ORDER, 'instructions_file': INSTR_FILE,
    'instructions_sha256': __import__('hashlib').sha256(INSTR.encode()).hexdigest() if INSTR else None, 'base_url': base, 'model': model, 'when_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'scored_warm': score(warm), 'cold': score(cold),
    'latency_all_ok_warm_plus_repeats': {'n': len(allms), 'p50': pct(0.5), 'p95': pct(0.95), 'p99': pct(0.99), 'max': allms[-1] if allms else None,
                                         'share_le_500ms': round(sum(m <= 500 for m in allms) / len(allms), 3) if allms else None},
    'outcomes_all': {k: sum(1 for r in cold + warm + rep if r['outcome'] == k) for k in sorted({r['outcome'] for r in cold + warm + rep})},
    'repeat_decision_stability': sum(1 for r in rep if r['outcome'] == 'ok' and permitted(next(c for c in cases if c['id'] == r['case']), r['decision'])) / max(1, len(rep)),
}
json.dump(summary, open(f'{out}/{label}-summary.json', 'w'), indent=1)
print(json.dumps(summary, indent=1))
