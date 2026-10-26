"""Parse a raw model reply into the expression fields the scorer judges. Never raises on model output: anything malformed
or unknown becomes an entry in `format_errors`.

Grammar (also in system_prompt.md):
  first line   ⟨say:speech⟩ | ⟨say:speech mood=M⟩ | ⟨say:summary mood=M⟩ | ⟨say:text⟩ | nothing (= text)
  summary      ⟨say:summary …⟩ is followed by ⟨summary⟩one spoken line⟨/summary⟩; the rest is displayed, not spoken
  inline       ⟨mood=M⟩ switches mood from the next sentence on (spoken parts only)
  events       <um> <laugh> <giggle> <sigh> <gasp> <pause> and (((emphasised words))) (spoken parts only)
Code (``` fences and `inline`) is opaque: nothing inside it is markup.

Usage: voice_expression_parse.py 'raw reply'   or   parse.py - < reply.txt   (prints the parsed JSON)"""
import json, re, sys

MOODS = ('neutral', 'calm', 'joy', 'serious', 'surprised', 'tired', 'tender')
EVENTS = ('um', 'laugh', 'giggle', 'sigh', 'gasp', 'pause')
EMPHASIS = 'emphasis'
SAY = {'speech': 'speech', 'summary': 'speech_summary', 'text': 'text'}
SUMMARY_MAX_WORDS = 30

THINK_RE = re.compile(r'\A\s*<think>.*?</think>\s*', re.S)
MARKER_RE = re.compile(r'\A\s*⟨say:([^\s⟩]*)([^⟩\n]*)⟩[ \t]*\n?')
LOOKALIKE_RE = re.compile(r'\A\s*(?:[<\[{(]\s*say\s*[:=]|⟨\s*say\b(?!:))', re.I)
SUMMARY_RE = re.compile(r'\A\s*⟨summary⟩(.*?)⟨/summary⟩[ \t]*\n?', re.S)
CODE_RE = re.compile(r'```.*?(?:```|\Z)|`[^`\n]+`', re.S)
STAGE = r'(?:laughs?|laughing|giggles?|chuckles?|sighs?|gasps?|pauses?|smiles?|grins?|coughs?|clears throat|risos?|risadas?|suspiros?|suspira)\b'
TOKEN_RE = re.compile(
    r'⟨mood=(?P<mood>[^⟩]*)⟩'
    r'|<(?P<close>/?)(?P<tag>[A-Za-z][\w-]*)\s*/?>'
    r'|\(\(\((?P<emph>[^()\n]+)\)\)\)'
    r'|(?P<control>⟨[^⟩\n]*⟩)'
    r'|(?P<stray>\(\(\(|\)\)\)|⟨|⟩)'
    r'|(?P<stage>\*' + STAGE + r'[^*\n]{0,20}\*|\[' + STAGE + r'[^\]\n]{0,20}\]|\(' + STAGE + r'[^)\n]{0,20}\))', re.I)
LEAK_RE = re.compile(
    r'⟨|⟩|\(\(\(|\)\)\)|<\/?[A-Za-z][\w-]*\s*\/?>|[<\[{]\s*say\s*[:=][^\]>}\n]*[\]>}]'
    r'|\*' + STAGE + r'[^*\n]{0,20}\*|\[' + STAGE + r'[^\]\n]{0,20}\]|\(' + STAGE + r'[^)\n]{0,20}\)', re.I)
SENT_END_RE = re.compile(r'[.!?…]+(?=\s|$)')


def _segments(text):
    """Yield (is_code, chunk) so markup handling never touches code."""
    pos = 0
    for m in CODE_RE.finditer(text):
        if m.start() > pos: yield False, text[pos:m.start()]
        yield True, m.group(0); pos = m.end()
    if pos < len(text): yield False, text[pos:]


def display_leaks(text):
    """Markup-like fragments left in displayed text, ignoring code."""
    return [m.group(0) for code, chunk in _segments(text) if not code for m in LEAK_RE.finditer(chunk)]


def _strip(text, spoken, errors):
    """Strip known markup. Returns (clean, markup, events, moods). `markup` keeps valid tags in canonical form (TTS input);
    positions in events/moods are offsets into `clean`. Unknown markup stays in both outputs and is reported."""
    out, mk, events, moods = [], [], [], []
    n = 0  # length of the clean text so far

    def emit(s, m=None):
        nonlocal n
        out.append(s); mk.append(s if m is None else m); n += len(s)

    def drop(tag_markup, following):
        # removing a tag between two spaces must not leave a double space
        skip = 1 if out and out[-1].endswith(' ') and following.startswith(' ') else 0
        mk.append(tag_markup + ' ' * skip)
        return skip

    for code, chunk in _segments(text):
        if code: emit(chunk); continue
        i = 0
        for m in TOKEN_RE.finditer(chunk):
            emit(chunk[i:m.start()]); i = m.end()
            rest = chunk[i:]
            if m.group('mood') is not None:
                v = m.group('mood').strip().lower()
                if v not in MOODS: errors.append(f'unknown_mood:{v}')
                elif not spoken: errors.append('mood_outside_speech')
                else: moods.append({'mood': v, 'pos': n})
                i += drop(f'⟨mood={v}⟩' if spoken and v in MOODS else '', rest)
            elif m.group('tag') is not None:
                t = m.group('tag').lower()
                if t in EVENTS and not m.group('close'):
                    if spoken: events.append({'event': f'<{t}>', 'pos': n})
                    else: errors.append('event_outside_speech')
                    i += drop(f'<{t}>' if spoken else '', rest)
                else:
                    errors.append(f'unknown_tag:{m.group(0)}'); emit(m.group(0))
            elif m.group('emph') is not None:
                if spoken: events.append({'event': EMPHASIS, 'pos': n})
                else: errors.append('event_outside_speech')
                emit(m.group('emph'), f"((({m.group('emph')})))" if spoken else None)
            elif m.group('control') is not None:
                c = m.group('control')
                errors.append('marker_not_first' if c.startswith('⟨say') else f'unknown_control:{c}'); emit(c)
            elif m.group('stray') is not None:
                errors.append('unbalanced_markup'); emit(m.group(0))
            else:
                errors.append(f'stage_direction:{m.group(0)}'); emit(m.group(0))
        emit(chunk[i:])
    return ''.join(out), ''.join(mk), events, moods


def _sentence_of(text, pos):
    return sum(1 for m in SENT_END_RE.finditer(text) if m.end() <= pos)


def parse(raw):
    r = {'marker_present': False, 'say': 'text', 'mood': None, 'mood_raw': None, 'per_sentence_moods': [], 'events': [],
         'displayed_text': '', 'spoken_text': '', 'spoken_markup': '', 'format_errors': [], 'display_leaks': [],
         'think_stripped': False}
    errors = r['format_errors']
    if not isinstance(raw, str):
        errors.append('empty_reply'); return r
    m = THINK_RE.match(raw)
    if m: raw = raw[m.end():]; r['think_stripped'] = True
    if not raw.strip():
        errors.append('empty_reply'); return r
    body = raw
    m = MARKER_RE.match(raw)
    if m:
        r['marker_present'] = True; body = raw[m.end():]
        kind, attrs = m.group(1), m.group(2).split()
        if kind not in SAY: errors.append(f'unknown_say:{kind}')
        r['say'] = SAY.get(kind, 'text')
        for a in attrs:
            k, _, v = a.partition('=')
            if k != 'mood' or not v: errors.append(f'unknown_marker_attr:{a}'); continue
            r['mood_raw'] = v
            if r['say'] == 'text': errors.append('mood_on_text')
            elif v.lower() not in MOODS: errors.append(f'unknown_mood:{v}')
            else: r['mood'] = v.lower()
        if r['say'] != 'text' and r['mood'] is None: r['mood'] = 'neutral'  # bare marker, or unknown mood: runtime falls back
    elif LOOKALIKE_RE.match(raw):
        errors.append('marker_lookalike')

    if r['say'] == 'speech_summary':
        s = SUMMARY_RE.match(body)
        if s:
            summary, body = s.group(1), body[s.end():]
            if '\n' in summary.strip(): errors.append('summary_multiline')
            if len(summary.split()) > SUMMARY_MAX_WORDS: errors.append('summary_too_long')
        else:
            summary = ''; errors.append('summary_missing')
        spoken, markup, events, moods = _strip(summary.strip(), True, errors)
        shown = _strip(body, False, errors)[0]
    elif r['say'] == 'speech':
        spoken, markup, events, moods = _strip(body.strip(), True, errors)
        shown = spoken
    else:
        shown = _strip(body, False, errors)[0]; spoken, markup, events, moods = '', '', [], []

    if r['say'] != 'text' and not spoken.strip(): errors.append('nothing_to_speak')
    for e in events: e['sentence'] = _sentence_of(spoken, e['pos'])
    for mo in moods: mo['sentence'] = _sentence_of(spoken, mo['pos'])
    r.update(events=events, per_sentence_moods=moods, spoken_text=spoken.strip(), spoken_markup=markup.strip(),
             displayed_text=shown.strip())
    r['display_leaks'] = display_leaks(r['displayed_text'])
    return r


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else '-'
    print(json.dumps(parse(sys.stdin.read() if arg == '-' else arg), ensure_ascii=False, indent=1))
