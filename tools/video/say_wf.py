# Narration for Wild Facts videos from wf.json / wf_long.json. Usage: python say_wf.py <file.json> <name> [voice]
import sys, json, os, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, '..', '..', '.new', 'tts')
src, name = sys.argv[1], sys.argv[2]; voice = sys.argv[3] if len(sys.argv) > 3 else 'af_bella'
c = json.load(open(os.path.join(HERE, src), encoding='utf-8'))[name]
L = {'intro': c['intro']}
if c.get('kind') == 'facts':
    for i, it in enumerate(c['items']): L[f'f{i+1}'] = it['say']
    L['end'] = 'Which one surprised you most? Follow for a wild fact every day!'
else:
    for i, it in enumerate(c['items']):
        L[f'q{i+1}'] = it['q']
        if c.get('read', True):
            for j, o in enumerate(it['o']): L[f'o{i+1}_{j}'] = ('ABC'[j] + '.', o + '.')  # letter, pause, option
        L[f'a{i+1}'] = it['say']
    n = len(c['items'])
    if n == 5: L['last'] = 'Last one. The hardest!'
    L['end'] = f'How many did you get out of {n}? Comment your score, and follow for more!'
L['plug'] = 'Want more? Play over twelve hundred free brain teasers, at brain teasers club dot app.'
k = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
out = os.path.join(HERE, 'voice_wf_' + name); os.makedirs(out, exist_ok=True); dur = {}
GAP = 0.5  # seconds between the option letter and its text (Nima: "A" ... "Hummingbird")
lang = 'en-gb' if voice.startswith('b') else 'en-us'
for key, text in L.items():
    if isinstance(text, tuple):
        a, sr = k.create(text[0], voice=voice, speed=1.08, lang=lang); b, sr = k.create(text[1], voice=voice, speed=1.08, lang=lang)
        s = np.concatenate([a, np.zeros(int(sr * GAP), dtype=a.dtype), b])
    else:
        s, sr = k.create(text, voice=voice, speed=1.08, lang=lang)
    sf.write(os.path.join(out, key + '.wav'), s, sr); dur[key] = round(len(s) / sr, 2)
json.dump(dur, open(os.path.join(out, 'durations.json'), 'w'))
print(name, len(dur), 'lines', round(sum(dur.values()), 1), 's')
