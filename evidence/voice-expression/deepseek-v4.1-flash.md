## evidence/voice-expression/replies/deepseek-v4.1-flash.jsonl  (deepseek-ai/DeepSeek-V4.1-Flash-1017 x160)

**Expression score 87.6** over 160 cases (missing replies: 0). say 90.6, mood in acceptable 96.2 of 105 rightly spoken (86.3 of all 117 that should speak), best 80.0.

### say confusion (rows gold, columns predicted)

| gold \ pred | text | speech | speech_summary |
|---|---:|---:|---:|
| text | 43 | 0 | 0 |
| speech | 4 | 88 | 1 |
| speech_summary | 8 | 2 | 14 |

### Overall

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 160 | 90.6 | 96.2 | 80.0 | 0.0 | 1.0 | 3.8 | 18.1 | 9.4 | 5.6 | 87.6 |

### By language

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| en | 83 | 89.2 | 96.2 | 80.8 | 0.0 | 1.9 | 1.9 | 18.1 | 9.6 | 4.4 | 87.5 |
| pt | 77 | 92.2 | 96.2 | 79.2 | 0.0 | 0.0 | 5.7 | 18.2 | 9.1 | 6.7 | 87.7 |

### By gate branch

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| desktop:absent | 2 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:asked_for_text | 6 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:device_busy | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:dictated | 93 | 86.0 | 95.1 | 80.5 | 0.0 | 1.2 | 4.9 | 24.7 | 15.1 | 5.9 | 82.0 |
| desktop:muted | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:typed | 17 | 100.0 | – | – | – | – | – | 17.6 | 0.0 | – | 95.2 |
| desktop:typed_asked_aloud | 4 | 75.0 | 100.0 | 66.7 | 0.0 | 0.0 | 0.0 | 25.0 | 0.0 | 33.3 | 73.1 |
| desktop:voice_mode_off | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:muted | 2 | 100.0 | – | – | – | – | – | 50.0 | 0.0 | – | 86.4 |
| messaging:typed | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed_asked_for_voice | 2 | 100.0 | 100.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.2 |
| messaging:voice_note_in | 18 | 94.4 | 100.0 | 83.3 | 0.0 | 0.0 | 0.0 | 5.6 | 5.6 | 0.0 | 95.1 |

### By emotion

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| apology | 4 | 100.0 | 50.0 | 25.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 83.1 |
| bad_news | 7 | 100.0 | 83.3 | 83.3 | 0.0 | 0.0 | 33.3 | 0.0 | 0.0 | 16.7 | 90.7 |
| condolence | 8 | 100.0 | 100.0 | 85.7 | 0.0 | 14.3 | 14.3 | 0.0 | 0.0 | 0.0 | 96.6 |
| crisis | 2 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 50.0 | 0.0 | 0.0 | 50.0 |
| frustration | 6 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 20.0 | 0.0 | 0.0 | 0.0 | 96.7 |
| good_news | 10 | 90.0 | 100.0 | 87.5 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 0.0 | 88.2 |
| goodbye | 6 | 100.0 | 100.0 | 40.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.2 |
| greeting | 10 | 100.0 | 100.0 | 71.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 97.5 |
| info | 71 | 84.5 | 100.0 | 88.6 | 0.0 | 0.0 | 0.0 | 32.4 | 15.5 | 9.5 | 82.1 |
| joke | 9 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| safety_refusal | 6 | 83.3 | 75.0 | 25.0 | 0.0 | 0.0 | 0.0 | 33.3 | 33.3 | 50.0 | 74.2 |
| small_talk | 15 | 93.3 | 100.0 | 70.0 | 0.0 | 0.0 | 0.0 | 13.3 | 13.3 | 0.0 | 92.5 |
| tired_night | 6 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |

### By content

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| code | 7 | 85.7 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 57.1 | 42.9 | 0.0 | 84.0 |
| list | 4 | 100.0 | 100.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.2 |
| list3 | 3 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 33.3 | 33.3 | 0.0 | 95.0 |
| long | 6 | 33.3 | – | – | – | – | – | 100.0 | 0.0 | – | 24.2 |
| none | 121 | 96.7 | 97.5 | 78.8 | 0.0 | 1.2 | 5.0 | 6.6 | 4.1 | 3.8 | 94.1 |
| numbers | 5 | 40.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 60.0 | 0.0 | – | 40.0 |
| path | 2 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 100.0 | 100.0 | – | 85.0 |
| short_numbers | 6 | 83.3 | 50.0 | 50.0 | 0.0 | 0.0 | 0.0 | 16.7 | 16.7 | 50.0 | 75.0 |
| table | 2 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 100.0 | 50.0 | – | 42.5 |
| url | 4 | 75.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 50.0 | 50.0 | 0.0 | 82.5 |

### By case group

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| content | 32 | 71.9 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 62.5 | 31.2 | 16.7 | 67.0 |
| emo | 75 | 97.3 | 93.7 | 76.2 | 0.0 | 1.6 | 6.3 | 5.3 | 4.0 | 4.8 | 92.9 |
| gate | 31 | 96.8 | 100.0 | 81.8 | 0.0 | 0.0 | 0.0 | 6.5 | 3.2 | 0.0 | 96.5 |
| hard | 22 | 86.4 | 100.0 | 63.6 | 0.0 | 0.0 | 0.0 | 13.6 | 4.5 | 9.1 | 87.0 |

Format error types: empty_reply 14, summary_missing 9, unknown_control 9, nothing_to_speak 9, unknown_tag 4, unbalanced_markup 2, marker_lookalike 1

Rates are % of: say/fmt err/leak/EXPR all cases; mood columns the cases where gold and reply both speak; avail viol/forbid ev/overuse replies that spoke; self-gate replies marked speech. – means no case qualified.
