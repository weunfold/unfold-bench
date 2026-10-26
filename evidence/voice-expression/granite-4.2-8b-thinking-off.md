## evidence/voice-expression/replies/granite-4.2-8b-thinking-off.jsonl  (granite-4.2-8b x160)

**Expression score 64.4** over 160 cases (missing replies: 0). say 56.2, mood in acceptable 80.2 of 101 rightly spoken (69.2 of all 117 that should speak), best 63.4.

### say confusion (rows gold, columns predicted)

| gold \ pred | text | speech | speech_summary |
|---|---:|---:|---:|
| text | 11 | 32 | 0 |
| speech | 14 | 79 | 0 |
| speech_summary | 2 | 22 | 0 |

### Overall

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 160 | 56.2 | 80.2 | 63.4 | 0.0 | 0.0 | 0.0 | 18.1 | 17.5 | 35.3 | 64.4 |

### By language

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| en | 83 | 55.4 | 85.4 | 66.7 | 0.0 | 0.0 | 0.0 | 10.8 | 10.8 | 33.8 | 65.1 |
| pt | 77 | 57.1 | 75.5 | 60.4 | 0.0 | 0.0 | 0.0 | 26.0 | 24.7 | 36.8 | 63.6 |

### By gate branch

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| desktop:absent | 2 | 0.0 | – | – | 0.0 | 0.0 | 0.0 | 50.0 | 50.0 | 50.0 | 13.6 |
| desktop:asked_for_text | 6 | 33.3 | – | – | 0.0 | 0.0 | 0.0 | 16.7 | 16.7 | 25.0 | 47.0 |
| desktop:device_busy | 4 | 0.0 | – | – | 0.0 | 0.0 | 0.0 | 50.0 | 50.0 | 25.0 | 13.6 |
| desktop:dictated | 93 | 64.5 | 82.7 | 66.7 | 0.0 | 0.0 | 0.0 | 19.4 | 19.4 | 42.0 | 72.2 |
| desktop:muted | 4 | 0.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 25.0 | 27.3 |
| desktop:typed | 17 | 29.4 | – | – | 0.0 | 0.0 | 0.0 | 5.9 | 5.9 | 41.7 | 47.1 |
| desktop:typed_asked_aloud | 4 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 25.0 | 25.0 | 25.0 | 96.2 |
| desktop:voice_mode_off | 4 | 50.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 63.6 |
| messaging:muted | 2 | 50.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 63.6 |
| messaging:typed | 4 | 25.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 45.5 |
| messaging:typed_asked_for_voice | 2 | 100.0 | 50.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 50.0 | 87.5 |
| messaging:voice_note_in | 18 | 72.2 | 64.3 | 35.7 | 0.0 | 0.0 | 0.0 | 27.8 | 22.2 | 7.1 | 66.1 |

### By emotion

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| apology | 4 | 75.0 | 66.7 | 66.7 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 33.3 | 72.5 |
| bad_news | 7 | 85.7 | 60.0 | 40.0 | 0.0 | 0.0 | 0.0 | 14.3 | 14.3 | 40.0 | 77.5 |
| condolence | 8 | 62.5 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 25.0 | 12.5 | 0.0 | 64.4 |
| crisis | 2 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |
| frustration | 6 | 66.7 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 16.7 | 16.7 | 60.0 | 54.5 |
| good_news | 10 | 90.0 | 66.7 | 44.4 | 0.0 | 0.0 | 0.0 | 10.0 | 10.0 | 10.0 | 82.2 |
| goodbye | 6 | 83.3 | 100.0 | 25.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 82.1 |
| greeting | 10 | 60.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 64.2 |
| info | 71 | 33.8 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 19.7 | 19.7 | 56.9 | 57.8 |
| joke | 9 | 88.9 | 25.0 | 25.0 | 0.0 | 0.0 | 0.0 | 22.2 | 22.2 | 0.0 | 71.9 |
| safety_refusal | 6 | 66.7 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 33.3 | 33.3 | 66.7 | 54.2 |
| small_talk | 15 | 73.3 | 100.0 | 30.0 | 0.0 | 0.0 | 0.0 | 26.7 | 26.7 | 7.1 | 72.4 |
| tired_night | 6 | 83.3 | 80.0 | 80.0 | 0.0 | 0.0 | 0.0 | 33.3 | 33.3 | 0.0 | 78.7 |

### By content

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| code | 7 | 0.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 14.3 | 14.3 | 100.0 | 42.1 |
| list | 4 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 25.0 | 25.0 | 50.0 | 76.2 |
| list3 | 3 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 33.3 | 33.3 | 33.3 | 95.0 |
| long | 6 | 0.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 49.1 |
| none | 121 | 66.1 | 73.9 | 49.3 | 0.0 | 0.0 | 0.0 | 19.0 | 18.2 | 18.8 | 65.7 |
| numbers | 5 | 0.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 40.0 | 40.0 | 80.0 | 54.0 |
| path | 2 | 0.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 50.0 | 50.0 | 100.0 | 52.5 |
| short_numbers | 6 | 83.3 | 60.0 | 60.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 66.7 | 79.5 |
| table | 2 | 0.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 60.0 |
| url | 4 | 0.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 66.7 | 48.8 |

### By case group

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| content | 32 | 18.8 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 12.5 | 12.5 | 90.3 | 60.1 |
| emo | 75 | 76.0 | 63.5 | 38.5 | 0.0 | 0.0 | 0.0 | 16.0 | 14.7 | 15.8 | 70.3 |
| gate | 31 | 45.2 | 100.0 | 60.0 | 0.0 | 0.0 | 0.0 | 29.0 | 29.0 | 23.1 | 52.8 |
| hard | 22 | 59.1 | 91.7 | 91.7 | 0.0 | 0.0 | 0.0 | 18.2 | 18.2 | 21.1 | 66.8 |

Format error types: unknown_control 26, unknown_say 1, unknown_tag 1, unbalanced_markup 1

Rates are % of: say/fmt err/leak/EXPR all cases; mood columns the cases where gold and reply both speak; avail viol/forbid ev/overuse replies that spoke; self-gate replies marked speech. – means no case qualified.
