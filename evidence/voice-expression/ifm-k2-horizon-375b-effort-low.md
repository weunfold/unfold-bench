## evidence/voice-expression/replies/ifm-k2-horizon-375b-effort-low.jsonl  (IFM/K2-Horizon-375B-A23B x160)

**Expression score 54.0** over 160 cases (missing replies: 0). say 50.0, mood in acceptable 94.2 of 52 rightly spoken (41.9 of all 117 that should speak), best 78.8.

### say confusion (rows gold, columns predicted)

| gold \ pred | text | speech | speech_summary |
|---|---:|---:|---:|
| text | 35 | 8 | 0 |
| speech | 54 | 39 | 0 |
| speech_summary | 11 | 7 | 6 |

### Overall

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 160 | 50.0 | 94.2 | 78.8 | 0.0 | 0.0 | 0.0 | 28.7 | 0.6 | 9.3 | 54.0 |

### By language

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| en | 83 | 45.8 | 100.0 | 83.3 | 0.0 | 0.0 | 0.0 | 37.3 | 1.2 | 10.0 | 47.7 |
| pt | 77 | 54.5 | 91.2 | 76.5 | 0.0 | 0.0 | 0.0 | 19.5 | 0.0 | 8.8 | 60.8 |

### By gate branch

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| desktop:absent | 2 | 0.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 27.3 |
| desktop:asked_for_text | 6 | 66.7 | – | – | 0.0 | 0.0 | 0.0 | 33.3 | 0.0 | 0.0 | 66.7 |
| desktop:device_busy | 4 | 100.0 | – | – | – | – | – | 25.0 | 0.0 | – | 93.2 |
| desktop:dictated | 93 | 43.0 | 93.6 | 80.9 | 0.0 | 0.0 | 0.0 | 24.7 | 1.1 | 12.2 | 49.9 |
| desktop:muted | 4 | 50.0 | – | – | 0.0 | 0.0 | 0.0 | 50.0 | 0.0 | 0.0 | 50.0 |
| desktop:typed | 17 | 88.2 | – | – | 0.0 | 0.0 | 0.0 | 29.4 | 0.0 | 0.0 | 83.4 |
| desktop:typed_asked_aloud | 4 | 25.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 75.0 | 0.0 | 0.0 | 23.1 |
| desktop:voice_mode_off | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:muted | 2 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed | 4 | 100.0 | – | – | – | – | – | 50.0 | 0.0 | – | 86.4 |
| messaging:typed_asked_for_voice | 2 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 50.0 | 0.0 | 0.0 | 50.0 |
| messaging:voice_note_in | 18 | 16.7 | 100.0 | 66.7 | 0.0 | 0.0 | 0.0 | 38.9 | 0.0 | 0.0 | 22.9 |

### By emotion

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| apology | 4 | 25.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 30.0 |
| bad_news | 7 | 57.1 | 100.0 | 66.7 | 0.0 | 0.0 | 0.0 | 57.1 | 0.0 | 33.3 | 52.2 |
| condolence | 8 | 62.5 | 100.0 | 25.0 | 0.0 | 0.0 | 0.0 | 25.0 | 12.5 | 0.0 | 61.6 |
| crisis | 2 | 0.0 | – | – | – | – | – | 50.0 | 0.0 | – | 7.5 |
| frustration | 6 | 16.7 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 33.3 | 0.0 | 0.0 | 26.2 |
| good_news | 10 | 20.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 90.0 | 0.0 | 0.0 | 17.3 |
| goodbye | 6 | 66.7 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 16.7 | 0.0 | 0.0 | 69.2 |
| greeting | 10 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 30.0 | 0.0 | 0.0 | 53.0 |
| info | 71 | 50.7 | 90.5 | 85.7 | 0.0 | 0.0 | 0.0 | 21.1 | 0.0 | 20.0 | 58.2 |
| joke | 9 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| safety_refusal | 6 | 16.7 | – | – | – | – | – | 0.0 | 0.0 | – | 29.2 |
| small_talk | 15 | 73.3 | 100.0 | 57.1 | 0.0 | 0.0 | 0.0 | 33.3 | 0.0 | 0.0 | 69.2 |
| tired_night | 6 | 16.7 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 66.7 | 0.0 | 0.0 | 21.2 |

### By content

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| code | 7 | 28.6 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 28.6 | 0.0 | 50.0 | 46.1 |
| list | 4 | 50.0 | 66.7 | 66.7 | 0.0 | 0.0 | 0.0 | 25.0 | 0.0 | 33.3 | 58.8 |
| list3 | 3 | 66.7 | 50.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 63.3 |
| long | 6 | 83.3 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 16.7 | 0.0 | – | 81.3 |
| none | 121 | 52.9 | 97.1 | 76.5 | 0.0 | 0.0 | 0.0 | 33.1 | 0.8 | 0.0 | 54.2 |
| numbers | 5 | 40.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 33.3 | 76.0 |
| path | 2 | 0.0 | – | – | – | – | – | 50.0 | 0.0 | – | 7.5 |
| short_numbers | 6 | 33.3 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 42.1 |
| table | 2 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 50.0 | 0.0 | – | 50.0 |
| url | 4 | 0.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 26.2 |

### By case group

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| content | 32 | 37.5 | 85.7 | 85.7 | 0.0 | 0.0 | 0.0 | 18.8 | 0.0 | 50.0 | 50.2 |
| emo | 75 | 46.7 | 96.3 | 77.8 | 0.0 | 0.0 | 0.0 | 33.3 | 1.3 | 3.4 | 48.7 |
| gate | 31 | 71.0 | 100.0 | 60.0 | 0.0 | 0.0 | 0.0 | 19.4 | 0.0 | 0.0 | 71.9 |
| hard | 22 | 50.0 | 100.0 | 83.3 | 0.0 | 0.0 | 0.0 | 40.9 | 0.0 | 0.0 | 52.5 |

Format error types: empty_reply 42, event_outside_speech 5, marker_not_first 1

Rates are % of: say/fmt err/leak/EXPR all cases; mood columns the cases where gold and reply both speak; avail viol/forbid ev/overuse replies that spoke; self-gate replies marked speech. – means no case qualified.
