"""Refresh data/checkpoints.json: for every local model on the bench, the official release date (base repo createdAt),
the GGUF repo's last update and head commit, and the commit we benchmarked. build.py reads the cached file, so the page
works offline. If the head moved past the benchmarked commit, the page flags "new checkpoint: re-bench".
LLMs released before 2026 are marked out of scope. Non-LLMs (STT, TTS, vision) may be older when no 2026 model works.
Public metadata reads only (no download). Usage: python3 -I checkpoints.py
"""
import json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
# model key -> (base repo for the release date, GGUF repo we download from, commit we benchmarked or None if not pinned)
CKPT = {
    'granite41-3b-q4km': ('ibm-granite/granite-4.1-3b', 'ibm-granite/granite-4.1-3b-GGUF', 'ab4701481089b58a082ef63cc1cee738887293ff'),
    'granite41-3b-q3km': ('ibm-granite/granite-4.1-3b', 'ibm-granite/granite-4.1-3b-GGUF', 'ab4701481089b58a082ef63cc1cee738887293ff'),
    'Qwen3.5-2B-Q8_0': ('Qwen/Qwen3.5-2B', 'unsloth/Qwen3.5-2B-GGUF', 'f6d5376be1edb4d416d56da11e5397a961aca8ae'),
    'Qwen3.5-2B-Q4_K_M': ('Qwen/Qwen3.5-2B', 'unsloth/Qwen3.5-2B-GGUF', 'f6d5376be1edb4d416d56da11e5397a961aca8ae'),
    'Qwen3.5-0.8B-Q8_0': ('Qwen/Qwen3.5-0.8B', 'unsloth/Qwen3.5-0.8B-GGUF', None),
    'lfm25-26b-q4km': ('LiquidAI/LFM2.5-2.6B', 'LiquidAI/LFM2.5-2.6B-GGUF', 'e7caca5d835a3901a8e0d63e94009429bafafdfc'),
    'lfm25-12b-q8': ('LiquidAI/LFM2.5-1.2B-Instruct', 'LiquidAI/LFM2.5-1.2B-Instruct-GGUF', '8ed288026e23'),
    'LFM2.5-350M-Q8_0': ('LiquidAI/LFM2.5-350M', 'LiquidAI/LFM2.5-350M-GGUF', None),
    'LFM2.5-350M-QAD-Q4_0': ('LiquidAI/LFM2.5-350M', 'LiquidAI/LFM2.5-350M-GGUF', None),
    'memop-17b-q8': ('MemTensor/MemOperator-1.7B', 'mradermacher/MemOperator-1.7B-GGUF', '220f6da733f7f22345d28cabdf28b3406347d06d'),
    'memop-06b-q8': ('MemTensor/MemOperator-0.6B', 'mradermacher/MemOperator-0.6B-GGUF', None),
    'granite40-h1b-q8': ('ibm-granite/granite-4.0-h-1b', 'ibm-granite/granite-4.0-h-1b-GGUF', 'c2cb1972f511add21f3bae244990b8ff3a3ffb23'),
    'granite40-h1b-q4km': ('ibm-granite/granite-4.0-h-1b', 'ibm-granite/granite-4.0-h-1b-GGUF', 'c2cb1972f511add21f3bae244990b8ff3a3ffb23'),
    'granite40-1b-q8': ('ibm-granite/granite-4.0-1b', 'ibm-granite/granite-4.0-1b-GGUF', None),
    'granite40-350m-q8': ('ibm-granite/granite-4.0-350m', 'ibm-granite/granite-4.0-350m-GGUF', None),
    'granite40-h350m-q8': ('ibm-granite/granite-4.0-h-350m', 'ibm-granite/granite-4.0-h-350m-GGUF', None),
}


def meta(repo):
    try:
        with urllib.request.urlopen(f'https://huggingface.co/api/models/{repo}', timeout=15) as r:
            d = json.load(r)
        return {'created': (d.get('createdAt') or '')[:10] or None, 'updated': (d.get('lastModified') or '')[:10] or None, 'sha': d.get('sha')}
    except Exception as e:
        return {'error': str(e)[:80]}


out, cache = {}, {}
for key, (base, gguf, pin) in CKPT.items():
    b = cache.setdefault(base, meta(base)); g = cache.setdefault(gguf, meta(gguf))
    released = b.get('created') or g.get('created')  # gated base repos don't answer anonymously; fall back to the GGUF repo
    head = g.get('sha')
    status = ('released before 2026' if released and released < '2026' else
              'unknown' if not head else
              'pin unknown: re-bench to pin' if not pin else
              'current' if head.startswith(pin) else 'new checkpoint: re-bench')
    out[key] = {'base_repo': base, 'gguf_repo': gguf, 'released': released, 'released_source': 'base repo' if b.get('created') else 'GGUF repo (base gated)',
                'upstream_updated': g.get('updated'), 'upstream_head': head, 'benched_commit': pin, 'status': status}
    print(f"{key:24} released {released}  updated {g.get('updated')}  {status}")
json.dump({'checked': time.strftime('%Y-%m-%d', time.gmtime()), 'models': out}, open(f'{HERE}/../data/checkpoints.json', 'w'), indent=1)
