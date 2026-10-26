# Unfold Bench

Open benchmarks for the parts of Unfold, the open personal agent from we unfold. Each part (deciding what to remember, choosing how to reply, talking) is measured on its own: real tasks, the exact settings used, and the evidence for every score. Local models that run for free on your own computer are listed first. Cloud models show what each run cost.

The data in `data/` is what the bench page on [weunfold.github.io](https://weunfold.github.io/) renders.

## What is here

| Path | Contents |
|---|---|
| `data/results.json` | Every scored run: model, runtime, quality, latency, cost, energy, and the checks it passed |
| `data/checkpoints.json` | Release date, last upstream update and benched commit for each local model, so a new checkpoint shows up as "re-bench" |
| `tasks/memory-decide/` | 24 dev tasks: one spoken sentence plus saved memories, decided as recall, no-op, remember or correct. Includes the exact request bodies, scoring criteria and prompt variants |
| `tasks/voice-expression/` | 160 dev cases (83 English, 77 Portuguese): reply as text, speech or a spoken summary, with which voice mood and which nonverbal sounds. Includes the instruction block and the scoring rules |
| `tasks/reflection/` | Dev tasks for the first step after you speak: routing (R1), following strict rules (R2), small talk (R3), honest memory answers (R4), honest self-description (R5), and act, talk or ask (R7) |
| `evidence/memory-decide/` | One summary per run: settings, per-task outcomes, latency percentiles |
| `evidence/voice-expression/` | Every published run's replies and score, and `summary.json` with all rows, cloud and local labelled |
| `evidence/hear-emotion/` | Summary scores of LAION Humaneness Ears Base and Medium on emoUERJ (pt-BR emotional speech); no audio, no per-clip rows |
| `runners/` | The scripts that produced the results |

## Progress and versions

`data/results.json` → `progress` scores the current skill map. Each skill earns a level:

| Level | Name | Means |
|---|---|---|
| 0 | Named | On the map, no tasks yet |
| 1 | Drafted | Tasks written, nothing scored |
| 2 | Measured | Scored runs with evidence, on dev tasks |
| 3 | Passes dev | A model meets every product floor on dev tasks |
| 4 | Passes held-out | A model meets every product floor on the private held-out tasks |

The progress index is the share of all levels reached: the sum of levels divided by 4 × the number of skills. It is not a measure of general intelligence. The map is versioned (v0.1 has 14 skills in 6 domains). A new version that adds skills or tasks lowers the index, and indexes are compared only within one version, like any versioned benchmark.

## Changes

- **2026-10-26, v0.1.3** (19 skills): Measured skills 0 → 2. Added `conversation.voice-expression` (160 dev cases; best local Granite 4.2 8B 64.4, best cloud Celeris 1 Magnus 93.9; oracle 100, always-text 37.8) and `perception.hear-emotion` (emoUERJ; Humaneness Ears Medium, speaker-held-out probe UAR 0.811 on CPU). The v0.1.3 index is 23.7%. It is not comparable with v0.1.2's 20.6%, which counted 17 skills.

## Held-out tasks

Each task set has a dev split, published here, and a held-out split kept private. A held-out score is the score that counts; dev scores can be tuned against and say so. The memory dev tasks were also sent to cloud providers during reference runs, so treat them as seen.

The reflection tasks were written by Claude Haiku 5.5 and checked by hand. The people and facts in them are fictional.

## Run it

Local runs need [llama.cpp](https://github.com/ggml-org/llama.cpp)'s `llama-server` and a GGUF file. Python 3.10 or newer, standard library only.

```sh
# Memory decision against any OpenAI-compatible server
# (the settings behind Granite 4.1 3B's 24/24: mini contract, prompt variant mini-v4)
llama-server -m granite-4.1-3b-Q4_K_M.gguf --port 8080 -ngl 99 -fa on --ctx-size 1536 --jinja &
python3 runners/memory_decide.py granite-3b http://127.0.0.1:8080/v1 granite out/granite-3b \
  --grammar mini --instructions tasks/memory-decide/instructions/instructions-mini-v4.txt

# Reflection tasks: the runner starts and stops llama-server itself, one model at a time
python3 runners/reflection_bench.py out/reflection --decide granite=granite-4.1-3b-Q4_K_M.gguf --talk granite=granite-4.1-3b-Q4_K_M.gguf
python3 runners/reflection_score.py out/reflection

# Voice expression against any OpenAI-compatible endpoint; the key, if any, is read from a file
python3 runners/voice_expression_run.py --base-url http://127.0.0.1:8080/v1 --model granite --api-key-file <key file> --max-tokens 400 --out out/granite.jsonl
python3 runners/voice_expression_score.py tasks/voice-expression/cases.jsonl out/granite.jsonl

# Check every local model for a newer upstream checkpoint (reads public metadata only)
python3 runners/checkpoints.py
```

`runners/hear_emotion_emouerj.py` scores Humaneness Ears on the emoUERJ clips. Unlike the other runners it needs numpy, scikit-learn and a local copy of the Ears model repository.

`runners/ifbench_run.py` runs [IFBench](https://github.com/allenai/IFBench) (Apache-2.0) with local models. Clone IFBench into `runners/IFBench` first; scoring uses IFBench's own code.

## Benchmarks we build on

| Benchmark | Licence | Used for |
|---|---|---|
| [IFBench](https://github.com/allenai/IFBench) | Apache-2.0 | Following strict output rules |
| [LongMemEval](https://github.com/xiaowu0162/LongMemEval) | MIT | Long-term conversational memory (planned) |
| [BFCL](https://github.com/ShishirPatil/gorilla) | Apache-2.0 | Function calling (planned) |
| [τ-bench](https://github.com/sierra-research/tau-bench), [τ²-bench](https://github.com/sierra-research/tau2-bench) | MIT | Acting in a conversation (planned) |
| [LoCoMo](https://github.com/snap-research/locomo), [Full-Duplex-Bench](https://github.com/DanielLin94144/Full-Duplex-Bench) | CC-BY-NC-4.0 | Long conversations, spoken turn-taking (planned; non-commercial) |

| [emoUERJ](https://zenodo.org/records/5427549) (R. G. Bastos Germano, M. Pompeu Tcheou, F. da Rocha Henriques, S. Pinto Gomes Junior, 2021) | CC BY 4.0 | Hearing emotion in pt-BR speech: 377 clips, 8 actors, 4 emotions |
| [LAION Humaneness Ears](https://huggingface.co/laion/humaneness-ears-base-medium) (model) | CC BY 4.0 | The emotion model measured on emoUERJ |

Their data stays in their own repositories under their own licences.

## Licence

MIT for the code and the data in this repository. See `LICENSE`.
