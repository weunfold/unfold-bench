# Voice expression

How Unfold delivers a reply: as text, as speech, or as a spoken one-line summary with the full answer on screen; the mood
of the voice, chosen from the moods that voice has; and nonverbal sounds. 160 dev cases, 83 in English and 77 in
Portuguese. The instruction block is English; only the conversation is in Portuguese.

| Path | Contents |
|---|---|
| `tasks/voice-expression/cases.jsonl` | The 160 dev cases with their gold labels (schema below) |
| `tasks/voice-expression/system_prompt.md` | The instruction block the model under test gets. The runner fills `{{TURN_FACTS}}` and `{{AVAILABLE_MOODS}}` per case. It carries no gold labels |
| `runners/voice_expression_run.py` | Runs the cases against any OpenAI-compatible endpoint, or a naive built-in stub with `--dry-run` |
| `runners/voice_expression_parse.py` | Raw reply to the fields the scorer judges. It never raises on model output |
| `runners/voice_expression_score.py` | The metrics below, as Markdown, plus JSON with the per-case evaluations |
| `evidence/voice-expression/` | Every published run: its replies, its score and a summary of all rows |

```sh
python3 runners/voice_expression_run.py --base-url http://127.0.0.1:8080/v1 --model <name> --api-key-file <key file> --max-tokens 400 --out out/<name>.jsonl
python3 runners/voice_expression_score.py tasks/voice-expression/cases.jsonl out/<name>.jsonl --json out/<name>.json
```

- The flags fall back to `EXPR_BENCH_BASE_URL`, `EXPR_BENCH_MODEL` and `EXPR_BENCH_API_KEY_FILE` (or `EXPR_BENCH_API_KEY`).
- The key is sent as a Bearer header only. It is never printed or written.
- Temperature 0 by default. Re-running with the same `--out` skips the cases already done.
- A leading `<think>…</think>` is stripped by the parser, and `reasoning_content` is kept apart.

## Reply grammar

```
⟨say:speech mood=M⟩          first line: speak everything below (bare ⟨say:speech⟩ = neutral)
⟨say:summary mood=M⟩         first line: spoken one-line summary, full answer shown only
⟨summary⟩one line⟨/summary⟩   right after the summary marker; spoken, not shown; ≤ 30 words, one line
(no marker) or ⟨say:text⟩     text only
⟨mood=M⟩                     inline, spoken parts only: switches mood from the next sentence on
<um> <laugh> <giggle> <sigh> <gasp> <pause> (((words)))     events, spoken parts only
```

- Moods: the vocabulary is `neutral calm joy serious surprised tired tender`. Each case lists only the moods its voice
  has, and `neutral` is always among them.
- Everything in the grammar is stripped before display. Code (``` fences and inline backticks) is opaque: `<T>` inside
  code is not markup and does not count as a leak.
- `⟨say:summary⟩` plus the `⟨summary⟩` block is this bench's own marker for a spoken summary.

**Format errors** (each is reported, never raised):
- marker lookalike (`[say:speech]`, `<say:speech>`), or a marker that is not first;
- an unknown say kind, an unknown marker attribute, or a mood on a text reply;
- an unknown mood;
- an unknown `<tag>` or `⟨control⟩`;
- unbalanced `(((`, `)))`, `⟨` or `⟩`;
- a stage direction (`*laughs*`, `(sighs)`, `[risos]`);
- an event or mood tag outside spoken text;
- a missing, multi-line or over-long summary;
- an empty reply, an API error, a missing reply.

Two buckets are kept apart. An unknown mood is a format error. A known mood that is not in the case's
`available_moods` is an availability violation.

A **display leak** is any of these left in `displayed_text` outside code: `⟨ ⟩ ((( )))`, a `<tag>`, a marker lookalike,
or a stage direction. Known markup is stripped. Unknown markup stays in the text, as a runtime that does not know it
would leave it, and counts as a leak.

## The say gate (gold rule)

The gold `say` of every case follows these rules in order; the first rule that matches decides.

1. Asked for text: "stop talking", "type it", "I can't hear you". → **text**
2. Muted. Mute applies on every channel. → **text**
3. **WhatsApp or Telegram.** Speech means a voice note. It is spoken iff the inbound turn was a voice note (`dictated`),
   or the person explicitly asked for audio; otherwise **text**. On these channels the Mac's `voice_mode`,
   `person_present` and `output_device_busy` are irrelevant: a voice note is a file, not the Mac speaker.
4. Desktop, with the output device busy or the person not at the Mac. → **text**
5. Desktop, with an explicit request to say it out loud. → speak. This beats typed modality and voice mode being off.
   It never beats mute, absence or a busy device: those are earlier rules.
6. Desktop, with voice mode off. → **text**
7. Desktop: typed → **text**, dictated → speak.

When a rule says speak, the content gate checks the reply. Code, a URL or path, or a table → **speech_summary**.
A list of more than 3 items, dense numbers, or more than about 60 words → **speech_summary** too.

**Lift rule:** an explicit request to read a list or a long answer aloud lifts the list and length limits. It never lifts
code, URL, path, table or dense numbers. Lifted: `en-hard-08` and `pt-hard-08`. Not lifted: `pt-hard-09` (numbers) and `en-hard-13` (code).

On messaging, `speech_summary` means a text message plus a one-line voice note.

## Case schema

- `id`, `lang`, `group` (gate | content | emo | hard), `gate_branch` (the rule that decided the gold `say`), `emotion`, `content`, `flags`
  (`ask_aloud`, `ask_text`, `lift_list`).
- `context`: `{input_modality, voice_mode, muted, output_device_busy, channel, person_present}`.
- `messages`: OpenAI messages, without the system prompt. History assistant turns are the displayed
  text, with no markup. Dictated turns read like ASR output (lowercase, little punctuation). The noisy-dictation cases
  carry `[noise]` and `[inaudible]` in the transcript.
- `available_moods`: one of 8 voice sets, from `[neutral]` to all 7.
- Gold:
  - `say`;
  - `acceptable_moods` and `best_mood`: the emotion profile's ideal moods ∩ `available_moods`, or else the profile's
    fallback order. Empty or null for text;
  - `forbidden_moods`, checked on the marker mood and every per-sentence mood;
  - `allowed_events`, `forbidden_events`, `max_events`;
  - `mood_fallback`: true when the ideal mood is not in this voice.
- `note`: why the gold is what it is.

**Counts.**

| breakdown | counts |
|---|---|
| say | speech 93, text 43, speech_summary 24 |
| group | gate 31, content 32, emo 75, hard 22 |
| gate branch | desktop:dictated 93, desktop:typed 17, messaging:voice_note_in 18, desktop:asked_for_text 6, desktop:voice_mode_off 4, desktop:muted 4, desktop:device_busy 4, desktop:typed_asked_aloud 4, messaging:typed 4, desktop:absent 2, messaging:muted 2, messaging:typed_asked_for_voice 2 |
| emotion | info 71, small_talk 15, greeting 10, good_news 10, joke 9, condolence 8, bad_news 7, frustration 6, tired_night 6, goodbye 6, safety_refusal 6, apology 4, crisis 2 |
| content | none 121, code 7, short_numbers 6, long 6, numbers 5, url 4, list 4, list3 3, path 2, table 2 |
| mood fallback | 19 cases |

## Metrics (`runners/voice_expression_score.py`)

Each is reported overall, and by language, gate branch, emotion, content and case group.

| metric | definition |
|---|---|
| say accuracy | Plus a 3×3 confusion matrix. |
| mood ∈ acceptable / mood = best | Over cases where gold and reply both speak. Also over every case that should speak (`mood_acc_all` in the JSON). A mood the voice lacks, an unknown mood, or a forbidden mood anywhere in the reply counts as wrong. |
| availability violation | Over replies that spoke: any mood used that is not in `available_moods`. |
| forbidden event, overuse | Over replies that spoke: any `forbidden_events`; more events than `max_events`. |
| format error, display leak | Over all cases. |
| self-gate | Diagnostic, unweighted: a reply marked `speech` whose own spoken text has code, a URL or path, a table, a list > 3, ≥ 6 numbers or > 60 words. |

**Expression score**, per case, then averaged ×100. Weights are renormalised over the parts that apply.

| part | weight | scoring |
|---|---:|---|
| say | 0.40 | Exact match. |
| mood | 0.25 | Gold speaks only. 1.0 best, 0.7 acceptable, 0 otherwise. |
| events | 0.20 | Gold speaks only. 0 if not spoken, forbidden or overused; 0.5 if outside `allowed_events`; 1 otherwise. |
| format | 0.15 | No format error and no leak. |

A text-gold case is judged on say and format only. Why these weights: say is the decision that changes what the person
experiences, mood is the next most audible, events are rarer and optional, and format is a hygiene floor.

## Limits

- Gold `say` assumes the intended content of a good answer: `content` is hand-assigned. A model that answers "how do I
  reverse a list in Python" in one spoken sentence without code is marked wrong (gold `speech_summary`). The self-gate
  diagnostic catches the opposite case, speaking code.
- No case judges answer quality, wording or language choice. Only expression is scored.
- Event placement is recorded (character offset and sentence index) but not scored.
