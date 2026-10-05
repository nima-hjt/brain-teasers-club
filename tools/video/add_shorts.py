# Add the Oct 12-19 Brain Teasers Shorts to shorts.json and render their narration (Kokoro af_heart).
import json, os, sys, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'shorts.json'); d = json.load(open(P, encoding='utf-8'))
END = "How many did you get? Comment your score, and follow for more!"
ENDF = "How many did you find? Comment your score, and follow for more!"
PLUG = "Over twelve hundred free brain teasers, at brain teasers club dot app."
def odd(emoji, items, a3, intro="Find the odd one out! Three levels. Six seconds each.", text=False):
    c = {"kind": "odd", "count": 6, "label": "FIND THE ODD ONE OUT", "title": ["FIND THE", "ODD ONE"], "titleEmoji": emoji,
         "pill": "3 LEVELS · 6 SECONDS EACH", "introEmoji": [i[0] for i in items] if not text else ["🔍", "👀", "⏱️"],
         "items": [{"common": cm, "odd": od, "cols": cols, "rows": rows, "pos": pos, "cap": cap, "a": "FOUND IT!"}
                   for (cm, od, cols, rows, pos), cap in zip(items, ["Level one", "Level two: harder", "Level three: almost impossible"])],
         "lines": {"intro": intro, "l1": "Level one.", "a1": "There it is!", "l2": "Level two. Harder.", "a2": "Got it?",
                   "l3": "Level three. Almost impossible.", "a3": a3, "end": ENDF, "plug": PLUG}}
    if text: c["text"] = True
    return c
def emoji(label, title, temoji, items, intro, says):
    caps = ["Number one", "Number two", "Number three", "This one's tricky!", "Last one: the hardest"]
    lines = {"intro": intro}
    pre = ["Number one.", "Number two.", "Number three.", "Number four. This one's tricky!", "Last one! This is the hardest."]
    for i, (q, a) in enumerate(items):
        lines[f"l{i+1}"] = pre[i]; lines[f"a{i+1}"] = says[i]
    lines["end"] = END; lines["plug"] = PLUG
    return {"kind": "emoji", "count": 3, "label": label, "title": title, "titleEmoji": temoji, "pill": f"5 {title[1]}S · 3 SECONDS EACH".replace("TALES", "TALE").replace("MOVIES", "MOVIE"),
            "introEmoji": [q[:2] if len(q) > 1 else q for q, a in items][:5] and [list(q)[0] for q, a in items],
            "items": [{"q": q, "a": a, "cap": caps[i]} for i, (q, a) in enumerate(items)], "lines": lines}
def riddles(items, says, intro="Three riddles. Six seconds each. Can you solve them all?"):
    pre = ["Riddle one.", "Riddle two.", "Last one. This is the hardest."]
    lines = {"intro": intro}
    for i in range(3): lines[f"l{i+1}"] = pre[i]; lines[f"a{i+1}"] = says[i]
    lines["end"] = END; lines["plug"] = PLUG
    return {"kind": "riddle", "count": 6, "label": "QUICK RIDDLE", "title": ["3 RIDDLES", "30 SECONDS"], "titleEmoji": "🧩",
            "pill": "6 SECONDS EACH · NO PEEKING", "introEmoji": ["🎹", "🤧", "🪙"] if says[0].startswith("A piano") else ["🪡", "🎂", "🪮"],
            "items": [{"q": q, "a": a, "opts": o, "cap": c} for (q, a, o), c in zip(items, ["Riddle one", "Riddle two", "Last one: the hardest"])], "lines": lines}
NEW = {
 "odd3": odd("👀", [("😐", "😑", 5, 6, 22), ("😮", "😯", 6, 7, 15), ("⌛", "⏳", 7, 8, 38)], "Sand at the top, not the bottom!"),
 "fairy": emoji("GUESS THE FAIRY TALE", ["GUESS THE", "FAIRY TALE"], "🏰",
     [("🍎👸🪞", "SNOW WHITE"), ("👠🎃🕛", "CINDERELLA"), ("🐺👵🧺", "LITTLE RED RIDING HOOD"), ("🐷🐷🐷🐺", "THE THREE LITTLE PIGS"), ("🫘🌱🏰", "JACK AND THE BEANSTALK")],
     "Can you guess all five fairy tales from just emoji?",
     ["Snow White!", "Cinderella!", "Little Red Riding Hood!", "The Three Little Pigs!", "Jack and the Beanstalk!"]),
 "riddles2": riddles([("What has keys but can't open locks?", "A piano", ["A map", "A piano", "A car", "A door"]),
                      ("What can you catch but not throw?", "A cold", ["A ball", "A cold", "A frisbee", "A stick"]),
                      ("What has a head and a tail, but no body?", "A coin", ["A snake", "A coin", "A cat", "A fish"])],
                     ["A piano!", "A cold!", "A coin! Heads or tails."]),
 "odd4": odd("👀", [("🌲", "🌳", 5, 6, 8), ("😗", "😙", 6, 7, 30), ("🕗", "🕣", 7, 8, 49)], "Eight thirty, not eight o'clock!"),
 "movies2": emoji("GUESS THE MOVIE", ["GUESS THE", "CARTOON"], "🎬",
     [("🦁👑", "THE LION KING"), ("🧸🤠🚀", "TOY STORY"), ("🧜‍♀️🐠🦀", "THE LITTLE MERMAID"), ("🌹👹", "BEAUTY AND THE BEAST"), ("🧞‍♂️🪔🐒", "ALADDIN")],
     "Can you guess all five animated movies from just emoji?",
     ["The Lion King!", "Toy Story!", "The Little Mermaid!", "Beauty and the Beast!", "Aladdin!"]),
 "oddletters2": odd("🔤", [("E", "F", 5, 6, 17), ("69", "96", 5, 7, 23), ("8", "B", 6, 8, 40)], "B, not eight!",
     intro="Can your eyes find the odd one? Three levels. Six seconds each.", text=True),
 "halloween": emoji("GUESS THE WORD", ["GUESS THE", "HALLOWEEN WORD"], "🎃",
     [("🍬🌽", "CANDY CORN"), ("🏚️👻", "HAUNTED HOUSE"), ("🃏🍬", "TRICK OR TREAT"), ("🌕🐺", "WEREWOLF"), ("🎃🏮", "JACK-O'-LANTERN")],
     "Halloween is coming! Can you guess all five spooky words from just emoji?",
     ["Candy corn!", "Haunted house!", "Trick or treat!", "Werewolf!", "Jack-o'-lantern!"]),
 "riddles3": riddles([("What has an eye but cannot see?", "A needle", ["A needle", "A cat", "A fish", "A bird"]),
                      ("What goes up but never comes down?", "Your age", ["A balloon", "Your age", "A ball", "A kite"]),
                      ("What has many teeth but can't bite?", "A comb", ["A shark", "A comb", "A dog", "A crocodile"])],
                     ["A needle!", "Your age!", "A comb!"]),
}
NEW["halloween"]["pill"] = "5 WORDS · 3 SECONDS EACH"; NEW["fairy"]["pill"] = "5 TALES · 3 SECONDS EACH"; NEW["movies2"]["pill"] = "5 MOVIES · 3 SECONDS EACH"
for k, v in NEW.items():
    if v["kind"] == "emoji": v["introEmoji"] = [list(i["q"])[0] for i in v["items"]]
d.update(NEW); json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from kokoro_onnx import Kokoro
M = os.path.join(HERE, '..', '..', '.new', 'tts'); kk = Kokoro(os.path.join(M, 'kokoro-v1.0.onnx'), os.path.join(M, 'voices-v1.0.bin'))
for name, cfg in NEW.items():
    out = os.path.join(HERE, 'voice_' + name); os.makedirs(out, exist_ok=True); dur = {}
    for key, text in cfg['lines'].items():
        s, sr = kk.create(text, voice='af_heart', speed=1.13, lang='en-us'); sf.write(os.path.join(out, key + '.wav'), s, sr); dur[key] = round(len(s) / sr, 2)
    json.dump(dur, open(os.path.join(out, 'durations.json'), 'w')); print(name, len(dur))
