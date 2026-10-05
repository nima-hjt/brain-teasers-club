# Narration for the long video "Guess 20 Movies by Emoji". Usage: python say_long.py <voice> <outdir>
import sys, json, os, soundfile as sf
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, '..', '..', '.new', 'tts')  # kokoro-v1.0.onnx + voices-v1.0.bin, not in git
voice, out = sys.argv[1], sys.argv[2]
ANSWERS = ['Harry Potter', 'Jurassic Park', 'Ghostbusters', 'Finding Nemo', 'Frozen', 'Shrek', 'Star Wars',
           'Kung Fu Panda', 'Back to the Future', 'Pirates of the Caribbean', 'Inside Out', 'Monsters, Inc.', 'Jumanji', 'The Wizard of Oz',
           'The Dark Knight', 'The Truman Show', 'Psycho', 'The Godfather', 'The Silence of the Lambs', 'Cast Away']
LINES = {
  'intro': "Can you guess twenty movies from just emoji? It starts easy, and gets harder every round. Keep score!",
  'r1': "Round one. Easy.",
  'r2': "Round two. Medium. These take a little more thought.",
  'r3': "Final round. Hard. Only real movie fans get these.",
  'end': "How many did you get out of twenty? Tell me in the comments, and subscribe for a new quiz every few days!",
  'plug': "Want more? Play over twelve hundred free brain teasers, at brain teasers club dot app.",
}
for i, a in enumerate(ANSWERS): LINES[f'a{i+1}'] = a + '!'
k = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
os.makedirs(out, exist_ok=True); dur = {}
for name, text in LINES.items():
    samples, sr = k.create(text, voice=voice, speed=1.1, lang='en-us')
    sf.write(os.path.join(out, name + '.wav'), samples, sr); dur[name] = round(len(samples) / sr, 2)
json.dump(dur, open(os.path.join(out, 'durations.json'), 'w'))
print(len(dur), 'lines', round(sum(dur.values()), 1), 's of speech')
