"""Build blind judging batches from talk replies (R3 pairwise, R4 replies, R5 probes). Model names are replaced
with opaque letters; A/B order alternates per pair to control position bias. Output: judge-input.json and judge-key.json.
Usage: python3 -I judge_prep.py RUN_DIR [RUN_DIR ...]
"""
import itertools, json, sys

rows = [json.loads(l) for d in sys.argv[1:] for l in open(f'{d}/results.jsonl')]
sets = {n: {x['id']: x for x in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks', 'reflection', f'{n}.json')))['items']} for n in ('r3-talk', 'r4-honest', 'r5-self')}
models = sorted({r['model'] for r in rows if r['task'] == 'R3'})
alias = {m: f'S{i + 1}' for i, m in enumerate(models)}
rep = {(r['task'], r['model'], r['id']): r['reply'] for r in rows if r['task'] in ('R3', 'R4-reply', 'R5')}

# R3: every pair of models on 16 of the dev items (a complete design per item).
r3_ids = sorted({r['id'] for r in rows if r['task'] == 'R3'})
r3_ids = r3_ids[::max(1, len(r3_ids) // 16)][:16]
pairs, key = [], {}
for i, (iid, (a, b)) in enumerate((iid, p) for iid in r3_ids for p in itertools.combinations(models, 2)):
    if i % 2: a, b = b, a
    pid = f'p{i:03d}'; key[pid] = {'item': iid, 'A': a, 'B': b}
    x = sets['r3-talk'][iid]
    pairs.append({'pair': pid, 'situation': x['situation'], 'conversation': x['turns'], 'A': rep[('R3', a, iid)], 'B': rep[('R3', b, iid)]})
r3_batches = [pairs[i:i + 30] for i in range(0, len(pairs), 30)]

# R4 replies and R5 probes: one batch per model, the model hidden behind its alias.
r4, r5 = {}, {}
for m in models:
    r4[alias[m]] = [{'id': i, 'memories': x['memories'], 'question': x['utterance'], 'gold': x['gold'], 'fact': x['answer_fact'], 'reply': rep[('R4-reply', m, i)]}
                    for i, x in sets['r4-honest'].items() if ('R4-reply', m, i) in rep]
    r5[alias[m]] = [{'id': i, 'conversation': x['turns'], 'pass_if': x['pass_if'], 'fail_if': x['fail_if'], 'reply': rep[('R5', m, i)]}
                    for i, x in sets['r5-self'].items() if ('R5', m, i) in rep]
json.dump({'r3_batches': r3_batches, 'r4': r4, 'r5': r5}, open('judge-input.json', 'w'), ensure_ascii=False)
json.dump({'alias': alias, 'pairs': key}, open('judge-key.json', 'w'), ensure_ascii=False, indent=1)
print(len(models), 'models', len(pairs), 'pairs in', len(r3_batches), 'batches;', {a: (len(r4[a]), len(r5[a])) for a in r4})
