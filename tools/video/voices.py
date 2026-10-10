# Narration helpers shared by say_wf.py / say_cfg.py.
# PICKED: the Kokoro voices Nima chose (Oct 10, 2026). Each video gets one of them; pick_voice rotates so neighbours differ.
import json, os, zlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PICKED = ['af_alloy', 'af_aoede', 'af_bella', 'af_heart', 'af_jessica', 'af_kore', 'af_nova', 'af_river', 'af_sarah', 'af_sky',
          'am_adam', 'am_echo', 'am_eric', 'am_fenrir', 'am_liam', 'am_michael', 'am_puck',
          'bf_alice', 'bf_emma', 'bf_isabella', 'bf_lily', 'bm_daniel', 'bm_fable', 'bm_george', 'bm_lewis']
LOG = os.path.join(HERE, 'voices_used.json')  # {video name: voice}, so a re-render keeps its voice

def pick_voice(name):
    used = json.load(open(LOG)) if os.path.exists(LOG) else {}
    if name in used: return used[name]
    recent = list(used.values())[-8:]  # avoid the last few voices
    pool = [v for v in PICKED if v not in recent] or PICKED
    v = pool[zlib.crc32(name.encode()) % len(pool)]
    used[name] = v; json.dump(used, open(LOG, 'w'), indent=1)
    return v

def lang_of(voice): return 'en-gb' if voice.startswith('b') else 'en-us'

def clean_letter(k, letter, voice, speed=1.08, carrier='Two'):
    """A lone "B." comes out as "Bee-ay" in some voices, so say "B. Two." (letter pronounced as in a sentence) and keep only
    the letter: cut at the quietest point before the carrier's "t" (a stop consonant, so there is a short silence)."""
    lang = lang_of(voice)
    full, sr = k.create(f'{letter}. {carrier}.', voice=voice, speed=speed, lang=lang)
    car, _ = k.create(f'{carrier}.', voice=voice, speed=speed, lang=lang)
    guess = max(len(full) - len(car), int(0.12 * sr))
    f = int(sr * 0.01); lo = max(int(0.2 * sr), guess - int(0.15 * sr)); hi = min(len(full) - f, max(lo + f, guess + int(0.10 * sr)))
    starts = list(range(lo, hi, f // 2)); e = [np.sqrt(np.mean(full[i:i + f] ** 2)) for i in starts]
    cut = starts[int(np.argmin(e))] + f // 2
    s = full[:cut].copy(); fade = int(0.015 * sr); s[-fade:] *= np.linspace(1, 0, fade)
    return s, sr
