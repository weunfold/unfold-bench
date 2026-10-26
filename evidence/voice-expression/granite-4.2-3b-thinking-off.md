## evidence/voice-expression/replies/granite-4.2-3b-thinking-off.jsonl  (granite-4.2-3b-Q4_K_M x160)

**Expression score 42.2** over 160 cases (missing replies: 0). say 31.2, mood in acceptable 81.2 of 16 rightly spoken (11.1 of all 117 that should speak), best 68.8.

### say confusion (rows gold, columns predicted)

| gold \ pred | text | speech | speech_summary |
|---|---:|---:|---:|
| text | 38 | 5 | 0 |
| speech | 80 | 12 | 1 |
| speech_summary | 21 | 3 | 0 |

### Overall

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 160 | 31.2 | 81.2 | 68.8 | 0.0 | 19.0 | 0.0 | 1.2 | 1.2 | 35.0 | 42.2 |

### By language

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| en | 83 | 36.1 | 83.3 | 75.0 | 0.0 | 23.5 | 0.0 | 1.2 | 1.2 | 41.2 | 46.4 |
| pt | 77 | 26.0 | 75.0 | 50.0 | 0.0 | 0.0 | 0.0 | 1.3 | 1.3 | 0.0 | 37.6 |

### By gate branch

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| desktop:absent | 2 | 50.0 | – | – | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 63.6 |
| desktop:asked_for_text | 6 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:device_busy | 4 | 50.0 | – | – | 0.0 | 50.0 | 0.0 | 0.0 | 0.0 | 100.0 | 63.6 |
| desktop:dictated | 93 | 10.8 | 78.6 | 64.3 | 0.0 | 7.1 | 0.0 | 1.1 | 1.1 | 30.8 | 24.7 |
| desktop:muted | 4 | 50.0 | – | – | 0.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 63.6 |
| desktop:typed | 17 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:typed_asked_aloud | 4 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 25.0 | 25.0 | 50.0 | 53.8 |
| desktop:voice_mode_off | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:muted | 2 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed_asked_for_voice | 2 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |
| messaging:voice_note_in | 18 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |

### By emotion

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| apology | 4 | 25.0 | 0.0 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 100.0 | 25.0 |
| bad_news | 7 | 14.3 | – | – | – | – | – | 0.0 | 0.0 | – | 27.1 |
| condolence | 8 | 12.5 | – | – | – | – | – | 0.0 | 0.0 | – | 25.6 |
| crisis | 2 | 50.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 53.8 |
| frustration | 6 | 16.7 | – | – | – | – | – | 0.0 | 0.0 | – | 29.2 |
| good_news | 10 | 40.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 33.3 | 49.0 |
| goodbye | 6 | 16.7 | – | – | – | – | – | 0.0 | 0.0 | – | 29.2 |
| greeting | 10 | 30.0 | – | – | – | – | – | 0.0 | 0.0 | – | 40.5 |
| info | 71 | 38.0 | 100.0 | 85.7 | 0.0 | 27.3 | 0.0 | 1.4 | 1.4 | 36.4 | 49.6 |
| joke | 9 | 22.2 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 31.1 |
| safety_refusal | 6 | 16.7 | – | – | – | – | – | 0.0 | 0.0 | – | 29.2 |
| small_talk | 15 | 26.7 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 38.5 |
| tired_night | 6 | 50.0 | 66.7 | 66.7 | 0.0 | 0.0 | 0.0 | 16.7 | 16.7 | 50.0 | 58.3 |

### By content

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| code | 7 | 28.6 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 45.7 |
| list | 4 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 57.5 |
| list3 | 3 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |
| long | 6 | 33.3 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 50.8 |
| none | 121 | 33.9 | 77.8 | 66.7 | 0.0 | 21.4 | 0.0 | 1.7 | 1.7 | 30.8 | 44.0 |
| numbers | 5 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 22.5 |
| path | 2 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |
| short_numbers | 6 | 50.0 | 50.0 | 50.0 | 0.0 | 50.0 | 0.0 | 0.0 | 0.0 | 50.0 | 50.0 |
| table | 2 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |
| url | 4 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |

### By case group

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| content | 32 | 15.6 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 66.7 | 31.1 |
| emo | 75 | 21.3 | 57.1 | 42.9 | 0.0 | 14.3 | 0.0 | 1.3 | 1.3 | 33.3 | 32.2 |
| gate | 31 | 54.8 | – | – | 0.0 | 33.3 | 0.0 | 0.0 | 0.0 | 33.3 | 62.8 |
| hard | 22 | 54.5 | 100.0 | 83.3 | 0.0 | 25.0 | 0.0 | 4.5 | 4.5 | 25.0 | 63.5 |

Format error types: marker_not_first 2, unknown_control 2, unknown_tag 1, event_outside_speech 1

Rates are % of: say/fmt err/leak/EXPR all cases; mood columns the cases where gold and reply both speak; avail viol/forbid ev/overuse replies that spoke; self-gate replies marked speech. – means no case qualified.
