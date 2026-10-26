## evidence/voice-expression/replies/celeris-1-magnus.jsonl  (celeris-1-magnus x160)

**Expression score 93.9** over 160 cases (missing replies: 0). say 95.6, mood in acceptable 93.0 of 115 rightly spoken (91.5 of all 117 that should speak), best 76.5.

### say confusion (rows gold, columns predicted)

| gold \ pred | text | speech | speech_summary |
|---|---:|---:|---:|
| text | 43 | 0 | 0 |
| speech | 1 | 90 | 2 |
| speech_summary | 1 | 3 | 20 |

### Overall

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 160 | 95.6 | 93.0 | 76.5 | 0.0 | 4.3 | 3.5 | 0.6 | 0.6 | 0.0 | 93.9 |

### By language

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| en | 83 | 96.4 | 93.1 | 75.9 | 0.0 | 1.7 | 0.0 | 0.0 | 0.0 | 0.0 | 95.8 |
| pt | 77 | 94.8 | 93.0 | 77.2 | 0.0 | 7.0 | 7.0 | 1.3 | 1.3 | 0.0 | 91.8 |

### By gate branch

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| desktop:absent | 2 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:asked_for_text | 6 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:device_busy | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:dictated | 93 | 94.6 | 93.5 | 78.3 | 0.0 | 4.3 | 4.3 | 0.0 | 0.0 | 0.0 | 92.3 |
| desktop:muted | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:typed | 17 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:typed_asked_aloud | 4 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| desktop:voice_mode_off | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:muted | 2 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed_asked_for_voice | 2 | 100.0 | 100.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.2 |
| messaging:voice_note_in | 18 | 88.9 | 88.2 | 64.7 | 0.0 | 5.9 | 0.0 | 5.6 | 5.6 | 0.0 | 86.1 |

### By emotion

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| apology | 4 | 100.0 | 50.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 82.5 |
| bad_news | 7 | 85.7 | 80.0 | 80.0 | 0.0 | 0.0 | 40.0 | 14.3 | 14.3 | 0.0 | 75.0 |
| condolence | 8 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.2 |
| crisis | 2 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 50.0 | 0.0 | 0.0 | 0.0 | 90.0 |
| frustration | 6 | 100.0 | 80.0 | 80.0 | 0.0 | 80.0 | 0.0 | 0.0 | 0.0 | 0.0 | 82.5 |
| good_news | 10 | 100.0 | 100.0 | 88.9 | 0.0 | 11.1 | 0.0 | 0.0 | 0.0 | 0.0 | 97.2 |
| goodbye | 6 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 93.8 |
| greeting | 10 | 100.0 | 85.7 | 28.6 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 94.5 |
| info | 71 | 94.4 | 97.7 | 93.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.5 |
| joke | 9 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| safety_refusal | 6 | 100.0 | 60.0 | 60.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 90.0 |
| small_talk | 15 | 86.7 | 100.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 92.2 |
| tired_night | 6 | 100.0 | 100.0 | 60.0 | 0.0 | 0.0 | 20.0 | 0.0 | 0.0 | 0.0 | 94.2 |

### By content

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| code | 7 | 85.7 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 94.3 |
| list | 4 | 100.0 | 75.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 91.9 |
| list3 | 3 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| long | 6 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | – | 100.0 |
| none | 121 | 97.5 | 93.9 | 72.0 | 0.0 | 6.1 | 4.9 | 0.8 | 0.8 | 0.0 | 94.3 |
| numbers | 5 | 60.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 75.0 |
| path | 2 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | – | 100.0 |
| short_numbers | 6 | 100.0 | 60.0 | 60.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 91.7 |
| table | 2 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | – | 100.0 |
| url | 4 | 75.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 90.0 |

### By case group

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| content | 32 | 90.6 | 96.3 | 96.3 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 94.1 |
| emo | 75 | 98.7 | 90.6 | 67.2 | 0.0 | 7.8 | 6.2 | 1.3 | 1.3 | 0.0 | 91.8 |
| gate | 31 | 93.5 | 90.9 | 72.7 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.1 |
| hard | 22 | 95.5 | 100.0 | 84.6 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 97.5 |

Format error types: marker_not_first 1

Rates are % of: say/fmt err/leak/EXPR all cases; mood columns the cases where gold and reply both speak; avail viol/forbid ev/overuse replies that spoke; self-gate replies marked speech. – means no case qualified.
