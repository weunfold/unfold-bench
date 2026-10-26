## evidence/voice-expression/replies/celeris-1.jsonl  (celeris-1 x160)

**Expression score 79.3** over 160 cases (missing replies: 0). say 76.2, mood in acceptable 94.5 of 109 rightly spoken (88.0 of all 117 that should speak), best 74.3.

### say confusion (rows gold, columns predicted)

| gold \ pred | text | speech | speech_summary |
|---|---:|---:|---:|
| text | 18 | 21 | 4 |
| speech | 7 | 84 | 2 |
| speech_summary | 1 | 3 | 20 |

### Overall

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 160 | 76.2 | 94.5 | 74.3 | 0.0 | 3.0 | 0.0 | 6.2 | 6.2 | 2.8 | 79.3 |

### By language

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| en | 83 | 74.7 | 92.6 | 72.2 | 0.0 | 2.9 | 0.0 | 2.4 | 2.4 | 0.0 | 78.5 |
| pt | 77 | 77.9 | 96.4 | 76.4 | 0.0 | 3.1 | 0.0 | 10.4 | 10.4 | 5.6 | 80.1 |

### By gate branch

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| desktop:absent | 2 | 0.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 27.3 |
| desktop:asked_for_text | 6 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| desktop:device_busy | 4 | 50.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 63.6 |
| desktop:dictated | 93 | 91.4 | 93.3 | 73.0 | 0.0 | 2.2 | 0.0 | 8.6 | 8.6 | 4.3 | 89.2 |
| desktop:muted | 4 | 0.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 27.3 |
| desktop:typed | 17 | 11.8 | – | – | 0.0 | 6.7 | 0.0 | 11.8 | 11.8 | 0.0 | 32.6 |
| desktop:typed_asked_aloud | 4 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| desktop:voice_mode_off | 4 | 50.0 | – | – | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 63.6 |
| messaging:muted | 2 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed | 4 | 100.0 | – | – | – | – | – | 0.0 | 0.0 | – | 100.0 |
| messaging:typed_asked_for_voice | 2 | 0.0 | – | – | – | – | – | 0.0 | 0.0 | – | 15.0 |
| messaging:voice_note_in | 18 | 83.3 | 100.0 | 75.0 | 0.0 | 6.2 | 0.0 | 0.0 | 0.0 | 0.0 | 85.0 |

### By emotion

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| apology | 4 | 100.0 | 50.0 | 25.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 83.1 |
| bad_news | 7 | 85.7 | 100.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 83.5 |
| condolence | 8 | 87.5 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 90.9 |
| crisis | 2 | 100.0 | 100.0 | 50.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 96.2 |
| frustration | 6 | 83.3 | 80.0 | 60.0 | 0.0 | 66.7 | 0.0 | 0.0 | 0.0 | 0.0 | 72.5 |
| good_news | 10 | 90.0 | 88.9 | 77.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 87.5 |
| goodbye | 6 | 83.3 | 100.0 | 40.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 84.1 |
| greeting | 10 | 80.0 | 100.0 | 57.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 83.2 |
| info | 71 | 70.4 | 97.6 | 92.9 | 0.0 | 0.0 | 0.0 | 14.1 | 14.1 | 6.7 | 77.4 |
| joke | 9 | 77.8 | 85.7 | 71.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 78.9 |
| safety_refusal | 6 | 16.7 | – | – | – | – | – | 0.0 | 0.0 | – | 29.2 |
| small_talk | 15 | 80.0 | 100.0 | 40.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 7.7 | 81.1 |
| tired_night | 6 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |

### By content

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| code | 7 | 57.1 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 14.3 | 14.3 | 100.0 | 69.6 |
| list | 4 | 100.0 | 100.0 | 75.0 | 0.0 | 0.0 | 0.0 | 25.0 | 25.0 | 0.0 | 94.4 |
| list3 | 3 | 66.7 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 86.7 |
| long | 6 | 66.7 | 75.0 | 75.0 | 0.0 | 0.0 | 0.0 | 66.7 | 66.7 | – | 59.5 |
| none | 121 | 76.0 | 94.7 | 69.7 | 0.0 | 4.1 | 0.0 | 0.0 | 0.0 | 1.0 | 79.1 |
| numbers | 5 | 80.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 40.0 | 40.0 | 0.0 | 86.0 |
| path | 2 | 50.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 80.0 |
| short_numbers | 6 | 100.0 | 80.0 | 40.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 93.3 |
| table | 2 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 50.0 | 50.0 | – | 92.5 |
| url | 4 | 75.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 | 25.0 | 25.0 | – | 75.0 |

### By case group

| group | n | say | mood∈acc | mood=best | avail viol | forbid ev | overuse | fmt err | leak | self-gate | EXPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| content | 32 | 71.9 | 96.3 | 92.6 | 0.0 | 0.0 | 0.0 | 28.1 | 28.1 | 25.0 | 77.3 |
| emo | 75 | 84.0 | 91.7 | 61.7 | 0.0 | 6.0 | 0.0 | 0.0 | 0.0 | 0.0 | 82.5 |
| gate | 31 | 61.3 | 100.0 | 81.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 4.8 | 72.1 |
| hard | 22 | 77.3 | 100.0 | 90.9 | 0.0 | 0.0 | 0.0 | 4.5 | 4.5 | 0.0 | 81.3 |

Format error types: summary_missing 10, unknown_control 10, nothing_to_speak 10, unbalanced_markup 2

Rates are % of: say/fmt err/leak/EXPR all cases; mood columns the cases where gold and reply both speak; avail viol/forbid ev/overuse replies that spoke; self-gate replies marked speech. – means no case qualified.
