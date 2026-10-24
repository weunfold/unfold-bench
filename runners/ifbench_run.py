"""Absorbed benchmark: IFBench (Ai2, Apache-2.0, commit 1c40f0c1). Generate one reply per prompt with a local model,
then score with IFBench's own verifiers (its code, unmodified, run from its lockfile venv).

One llama-server at a time, started and stopped here by recorded PID (reflection_bench.server/stop).
Usage: python3 -I ifbench_run.py OUT KEY=GGUF[,KEY=GGUF...]   then IFBench's run_eval per model (printed at the end).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reflection_bench as rb  # noqa: E402

out, models = sys.argv[1], dict(a.split('=', 1) for a in sys.argv[2].split(','))
os.makedirs(out, exist_ok=True)
prompts = [json.loads(l) for l in open(f'{HERE}/IFBench/data/IFBench_test.jsonl')]
for key, path in models.items():
    dst = f'{out}/{key}.responses.jsonl'
    done = {json.loads(l)['prompt'] for l in open(dst)} if os.path.exists(dst) else set()
    p = rb.server(key, path, out)
    try:
        with open(dst, 'a') as f:
            for x in prompts:
                if x['prompt'] in done: continue
                try: r = rb.call([{'role': 'user', 'content': x['prompt']}], max_tokens=1024, temperature=0)
                except Exception as e: r = {'text': '', 'finish': f'error: {str(e)[:80]}', 'ttft_ms': None, 'total_ms': None, 'tok_s': None}
                f.write(json.dumps({'prompt': x['prompt'], 'response': r['text'], 'finish': r['finish'], 'ttft_ms': r['ttft_ms'], 'total_ms': r['total_ms'], 'tok_s': r['tok_s']}, ensure_ascii=False) + '\n'); f.flush()
    finally:
        rb.stop(p)
    print(key, 'done', flush=True)
for key in models:
    print(f'cd {HERE}/IFBench && NLTK_DATA=$PWD/.nltk uv run --frozen python -m run_eval --input_data=data/IFBench_test.jsonl '
          f'--input_response_data={os.path.abspath(out)}/{key}.responses.jsonl --output_dir={os.path.abspath(out)}/eval-{key}')
