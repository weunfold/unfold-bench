"""Score replies against cases. Deterministic; no model involved.
Usage: voice_expression_score.py CASES.jsonl REPLIES.jsonl [--json OUT.json]   (prints Markdown tables)

Expression score, per case, then averaged and shown x100. Weights are renormalised over the parts that apply:
  say     0.40  say matches gold (text | speech | speech_summary)
  mood    0.25  only when gold speaks: 1.0 best mood, 0.7 another acceptable mood, 0 otherwise (incl. not speaking, a mood the
                voice lacks, an unknown mood, or a forbidden mood anywhere in the reply, per-sentence tags included)
  events  0.20  only when gold speaks: 0 if not spoken, a forbidden event, or more than max_events; 0.5 if an event is
                outside allowed_events; 1 otherwise (no events is fine)
  format  0.15  no format errors and nothing leaked into the displayed text
A text-gold case is judged on say and format only, so speaking where it should not costs the say part."""
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from voice_expression_parse import parse

W = {'say': 0.40, 'mood': 0.25, 'events': 0.20, 'format': 0.15}
SAYS = ('text', 'speech', 'speech_summary')
URL_RE = re.compile(r'https?://|www\.|\b[\w-]+\.(?:com|org|net|io|gov|br|dev)(?:\.br)?(?:/|\b)', re.I)
PATH_RE = re.compile(r'(?:^|\s)(?:~/|/)[\w.-]+/[\w./-]*|\b[A-Z]:\\', re.M)
LIST_RE = re.compile(r'^\s*(?:[-*•]|\d+[.)])\s+', re.M)
NUM_RE = re.compile(r'\d+(?:[.,]\d+)?')


def content_flags(text):
    """What in a spoken text should have forced a summary (tts-options §4 content gate)."""
    f = []
    if '```' in text or re.search(r'`[^`\n]+`', text): f.append('code')
    if URL_RE.search(text): f.append('url')
    if PATH_RE.search(text): f.append('path')
    if sum(1 for l in text.splitlines() if l.count('|') >= 2) >= 2: f.append('table')
    if len(LIST_RE.findall(text)) > 3: f.append('list')
    if len(NUM_RE.findall(text)) >= 6: f.append('numbers')
    if len(text.split()) > 60: f.append('long')
    return f


def evaluate(case, reply):
    raw = reply.get('raw') if reply else None
    p = parse(raw)
    if reply is None: p['format_errors'].append('missing_reply')
    elif reply.get('error'): p['format_errors'].append('api_error')
    gold, pred = case['say'], p['say']
    gs, spoke = gold != 'text', pred != 'text'
    used = ([p['mood']] if p['mood'] else []) + [m['mood'] for m in p['per_sentence_moods']]
    unknown_mood = any(e.startswith('unknown_mood') for e in p['format_errors'])
    avail_v = spoke and any(m not in case['available_moods'] for m in used)
    forb_mood = spoke and any(m in case['forbidden_moods'] for m in used)
    ev = [e['event'] for e in p['events']]
    forb_ev = spoke and any(e in case['forbidden_events'] for e in ev)
    over = spoke and len(ev) > case['max_events']
    offlist = spoke and any(e not in case['allowed_events'] for e in ev)
    mood_ok = gs and spoke and p['mood'] in case['acceptable_moods'] and not (avail_v or forb_mood or unknown_mood)
    mood_best = mood_ok and p['mood'] == case['best_mood']
    fmt_ok = not p['format_errors'] and not p['display_leaks']
    comp = {'say': float(pred == gold), 'format': float(fmt_ok)}
    if gs:
        comp['mood'] = 1.0 if mood_best else 0.7 if mood_ok else 0.0
        comp['events'] = 0.0 if (not spoke or forb_ev or over) else 0.5 if offlist else 1.0
    score = sum(W[k] * v for k, v in comp.items()) / sum(W[k] for k in comp)
    self_gate = content_flags(p['spoken_text']) if pred == 'speech' and 'lift_list' not in case['flags'] else []
    return {'id': case['id'], 'lang': case['lang'], 'group': case['group'], 'gate_branch': case['gate_branch'], 'emotion': case['emotion'],
            'content': case['content'], 'gold_say': gold, 'pred_say': pred, 'gold_speaks': gs, 'spoke': spoke,
            'mood': p['mood'], 'moods_used': used, 'mood_ok': mood_ok, 'mood_best': mood_best, 'availability_violation': avail_v,
            'forbidden_mood': forb_mood, 'events': ev, 'forbidden_event': forb_ev, 'overuse': over, 'offlist_event': offlist,
            'format_errors': p['format_errors'], 'display_leaks': p['display_leaks'], 'self_gate': self_gate,
            'components': comp, 'expression': round(score, 4), 'latency_ms': (reply or {}).get('latency_ms')}


def rate(rows, key, cond=None):
    d = [r for r in rows if cond is None or cond(r)]
    return (sum(bool(r[key]) for r in d) / len(d), len(d)) if d else (None, 0)


def summary(rows):
    s = {'n': len(rows)}
    s['say_acc'] = rate(rows, 'say_ok')
    s['mood_acc'] = rate(rows, 'mood_ok', lambda r: r['gold_speaks'] and r['spoke'])  # among replies that rightly spoke
    s['mood_best'] = rate(rows, 'mood_best', lambda r: r['gold_speaks'] and r['spoke'])
    s['mood_acc_all'] = rate(rows, 'mood_ok', lambda r: r['gold_speaks'])              # over every case that should speak
    s['availability_violation'] = rate(rows, 'availability_violation', lambda r: r['spoke'])
    s['forbidden_event'] = rate(rows, 'forbidden_event', lambda r: r['spoke'])
    s['overuse'] = rate(rows, 'overuse', lambda r: r['spoke'])
    s['format_error'] = rate(rows, 'format_errors')
    s['display_leak'] = rate(rows, 'display_leaks')
    s['self_gate'] = rate(rows, 'self_gate', lambda r: r['pred_say'] == 'speech')
    s['expression'] = (sum(r['expression'] for r in rows) / len(rows), len(rows)) if rows else (None, 0)
    return s


COLS = [('say_acc', 'say'), ('mood_acc', 'mood∈acc'), ('mood_best', 'mood=best'), ('availability_violation', 'avail viol'),
        ('forbidden_event', 'forbid ev'), ('overuse', 'overuse'), ('format_error', 'fmt err'), ('display_leak', 'leak'),
        ('self_gate', 'self-gate'), ('expression', 'EXPR')]


def pct(v):
    return '–' if v[0] is None else f'{100 * v[0]:.1f}'


def table(title, groups):
    out = [f'### {title}', '', '| group | n | ' + ' | '.join(c[1] for c in COLS) + ' |', '|---|---:|' + '---:|' * len(COLS)]
    for g, s in groups:
        out.append(f"| {g} | {s['n']} | " + ' | '.join(pct(s[k]) for k, _ in COLS) + ' |')
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cases'); ap.add_argument('replies'); ap.add_argument('--json')
    a = ap.parse_args()
    cases = [json.loads(l) for l in open(a.cases)]
    replies = {}
    for l in open(a.replies):
        if l.strip(): r = json.loads(l); replies[r['id']] = r  # a later line for the same id wins
    rows = [evaluate(c, replies.get(c['id'])) for c in cases]
    for r in rows: r['say_ok'] = r['gold_say'] == r['pred_say']
    models = Counter(r.get('model') for r in replies.values())
    res = {'replies': a.replies, 'models': dict(models), 'cases': len(cases), 'missing': sum(c['id'] not in replies for c in cases),
           'weights': W, 'overall': summary(rows)}
    conf = {g: {p: sum(1 for r in rows if r['gold_say'] == g and r['pred_say'] == p) for p in SAYS} for g in SAYS}
    res['confusion'] = conf
    for key in ('lang', 'group', 'gate_branch', 'emotion', 'content'):
        by = defaultdict(list)
        for r in rows: by[r[key]].append(r)
        res[f'by_{key}'] = {g: summary(v) for g, v in sorted(by.items())}
    errs = Counter(e.split(':')[0] for r in rows for e in r['format_errors'])
    res['format_error_types'] = dict(errs.most_common())
    lat = sorted(r['latency_ms'] for r in rows if isinstance(r['latency_ms'], (int, float)))
    res['latency_ms_p50'] = lat[len(lat) // 2] if lat else None

    o = res['overall']
    print(f"## {a.replies}  ({', '.join(f'{m} x{n}' for m, n in models.items())})\n")
    print(f"**Expression score {pct(o['expression'])}** over {len(cases)} cases (missing replies: {res['missing']}). "
          f"say {pct(o['say_acc'])}, mood in acceptable {pct(o['mood_acc'])} of {o['mood_acc'][1]} rightly spoken "
          f"({pct(o['mood_acc_all'])} of all {o['mood_acc_all'][1]} that should speak), best {pct(o['mood_best'])}.\n")
    print('### say confusion (rows gold, columns predicted)\n\n| gold \\ pred | ' + ' | '.join(SAYS) + ' |\n|---|' + '---:|' * 3)
    for g in SAYS: print(f'| {g} | ' + ' | '.join(str(conf[g][p]) for p in SAYS) + ' |')
    print()
    print(table('Overall', [('all', o)]))
    for key, title in (('lang', 'By language'), ('gate_branch', 'By gate branch'), ('emotion', 'By emotion'), ('content', 'By content'), ('group', 'By case group')):
        print(table(title, list(res[f'by_{key}'].items())))
    print('Format error types: ' + (', '.join(f'{k} {v}' for k, v in errs.most_common()) or 'none') + '\n')
    print('Rates are % of: say/fmt err/leak/EXPR all cases; mood columns the cases where gold and reply both speak; '
          'avail viol/forbid ev/overuse replies that spoke; self-gate replies marked speech. – means no case qualified.')
    if a.json:
        res['per_case'] = rows
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
