# Render narration lines with Kokoro (offline). Usage: python say.py <voice> <outdir>
import sys, json, os, soundfile as sf
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, '..', '..', '.new', 'tts')  # kokoro-v1.0.onnx + voices-v1.0.bin, not in git
voice, out = sys.argv[1], sys.argv[2]
LINES = {
  'intro':  "Can you guess all five movies from just emoji?",
  'l1': "Number one.", 'a1': "The Lion King!",
  'l2': "Number two.", 'a2': "Titanic!",
  'l3': "Number three.", 'a3': "Jaws!",
  'l4': "Number four. This one's tricky!", 'a4': "Forrest Gump!",
  'l5': "Last one! Only real movie fans get this.", 'a5': "Groundhog Day!",
  'end':  "How many did you get? Comment your score, and follow for more!",
  'plug': "Over twelve hundred free brain teasers, at brain teasers club dot app.",
}
k = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
os.makedirs(out, exist_ok=True); dur = {}
for name, text in LINES.items():
    samples, sr = k.create(text, voice=voice, speed=1.13, lang='en-us')
    sf.write(os.path.join(out, name + '.wav'), samples, sr); dur[name] = round(len(samples) / sr, 2)
json.dump(dur, open(os.path.join(out, 'durations.json'), 'w'))
print(dur)
