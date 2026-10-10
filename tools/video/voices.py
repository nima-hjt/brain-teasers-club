# Narration helpers shared by say_wf.py / say_cfg.py.
# PICKED: the Kokoro voices Nima chose (Oct 10, 2026). Each video gets one of them at random (not one of the last few used).
import json, os, zlib
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
