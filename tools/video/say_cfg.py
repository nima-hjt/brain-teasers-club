# Render narration for one Short from vid/shorts.json. Usage: python say_cfg.py <name> <voice>
import sys, json, os, soundfile as sf
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, '..', '..', '.new', 'tts')  # kokoro-v1.0.onnx + voices-v1.0.bin, not in git
name, voice = sys.argv[1], sys.argv[2]
cfg = json.load(open(os.path.join(HERE, 'shorts.json'), encoding='utf-8'))[name]
out = os.path.join(HERE, 'voice_' + name)
k = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
os.makedirs(out, exist_ok=True); dur = {}
for key, text in cfg['lines'].items():
    samples, sr = k.create(text, voice=voice, speed=1.13, lang='en-us')
    sf.write(os.path.join(out, key + '.wav'), samples, sr); dur[key] = round(len(samples) / sr, 2)
json.dump(dur, open(os.path.join(out, 'durations.json'), 'w'))
print(name, len(dur), 'lines')
