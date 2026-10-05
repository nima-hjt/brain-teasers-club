# Make a "Guess 20 X by Emoji" long page + narration from animals.html. Usage: python gen_long.py <key>
import sys, os, re, json, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = {
 'foods': dict(word='FOODS', one='FOOD', icon='🍔', voice='voice_foods/', intro_emoji=['🍔','🥞','🍰','🧀','🥚','🍟','🌭'],
   pill='EASY → MEDIUM → HARD', rsub3='Only real foodies get these',
   tiers=[['0–7','SNACK ROOKIE','🍪'],['8–14','FOOD FAN','🍕'],['15–19','TOP CHEF','🏆'],['20','FOOD GENIUS','🧠']],
   thumb='🏄🌱', intro="Can you guess twenty foods from just emoji? It starts easy, and gets harder every round. Keep score!",
   r3="Final round. Hard. Only real foodies get these.",
   rounds=[('EASY',[('🔥🐶','HOT DOG','HOT + DOG'),('🥜🧈','PEANUT BUTTER','PEANUT + BUTTER'),('🧀🍔','CHEESEBURGER','CHEESE + BURGER'),('🍎🥧','APPLE PIE','APPLE + PIE'),('🇫🇷🍞','FRENCH TOAST','FRENCH + TOAST'),('🥚🥓','BACON AND EGGS','EGGS + BACON'),('🍓🍦','STRAWBERRY ICE CREAM','STRAWBERRY + ICE CREAM')]),
     ('MEDIUM',[('🐟🍟','FISH AND CHIPS','FISH + CHIPS'),('🧀🍞🔥','GRILLED CHEESE','CHEESE + BREAD + HEAT'),('🍰🧀','CHEESECAKE','CAKE + CHEESE'),('🍌🍞','BANANA BREAD','BANANA + BREAD'),('🍗🧇','CHICKEN AND WAFFLES','CHICKEN + WAFFLES'),('🌽🐶','CORN DOG','CORN + DOG'),('🥒🥪','CUCUMBER SANDWICH','CUCUMBER + SANDWICH')]),
     ('HARD',[('🏄🌱','SURF AND TURF','SURF + TURF · seafood and steak'),('⬛🌲🍰','BLACK FOREST CAKE','BLACK + FOREST + CAKE'),('😈🍰',"DEVIL'S FOOD CAKE",'DEVIL + FOOD CAKE'),('🥚🧻','EGG ROLL','EGG + ROLL'),('🍞🍮','BREAD PUDDING','BREAD + PUDDING'),('🥔🔨','MASHED POTATOES','POTATOES + MASH')])]),
 'words': dict(word='WORDS', one='WORD', icon='🧩', voice='voice_words/', intro_emoji=['☀️','🌻','🦶','⚽','🌧️','🎀','🔥'],
   pill='EMOJI + EMOJI = WORD', rsub3='Only word wizards get these',
   tiers=[['0–7','WORD ROOKIE','🐣'],['8–14','WORD FAN','📚'],['15–19','WORD WIZARD','🏆'],['20','WORD GENIUS','🧠']],
   thumb='🌧️🎀', intro="Two emoji make one word. Can you guess all twenty? It starts easy, and gets harder every round. Keep score!",
   r3="Final round. Hard. Only word wizards get these.",
   rounds=[('EASY',[('☀️🌻','SUNFLOWER','SUN + FLOWER'),('🦶⚽','FOOTBALL','FOOT + BALL'),('🌧️🎀','RAINBOW','RAIN + BOW'),('🐎👞','HORSESHOE','HORSE + SHOE'),('⛄👨','SNOWMAN','SNOW + MAN'),('🌙💡','MOONLIGHT','MOON + LIGHT'),('🔥🪰','FIREFLY','FIRE + FLY')]),
     ('MEDIUM',[('🥚🪴','EGGPLANT','EGG + PLANT'),('🐶🏠','DOGHOUSE','DOG + HOUSE'),('🍯🌙','HONEYMOON','HONEY + MOON'),('✋👜','HANDBAG','HAND + BAG'),('🌊🐚','SEASHELL','SEA + SHELL'),('🔑🕳️','KEYHOLE','KEY + HOLE'),('🐦🏠','BIRDHOUSE','BIRD + HOUSE')]),
     ('HARD',[('🧠🌪️','BRAINSTORM','BRAIN + STORM'),('🐮👦','COWBOY','COW + BOY'),('🧈🥛','BUTTERMILK','BUTTER + MILK'),('👁️⚽','EYEBALL','EYE + BALL'),('🔥🏭','FIREWORKS','FIRE + WORKS'),('🥜🐚','NUTSHELL','NUT + SHELL')])]),
}
key = sys.argv[1]; c = CFG[key]
s = open(os.path.join(HERE, 'animals.html'), encoding='utf-8').read()
def js(v): return json.dumps(v, ensure_ascii=False)
def sub(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)
rounds = ',\n'.join("  {name:'%s',items:%s}" % (n, js([list(i) for i in items])) for n, items in c['rounds'])
s = re.sub(r"const ROUNDS=\[.*?\n\];", lambda m: "const ROUNDS=[\n" + rounds + "\n];", s, flags=re.S)
sub("const VOICE='voice_animals/'", "const VOICE='%s'" % c['voice'])
sub('Guess 20 Animals (long)', 'Guess 20 %s (long)' % c['word'].title())
sub("'Real animals, tricky names'", "'%s'" % c['rsub3'])
sub("stroked('GUESS 20 ANIMALS'", "stroked('GUESS 20 %s'" % c['word'])
sub("text('🐾',W/2+400", "text('%s',W/2+400" % c['icon'])
sub("['⭐','🌊','🐟','🦀','🦈','🐸','🦌']", js(c['intro_emoji']))
sub("pillAt('EMOJI + EMOJI = ANIMAL'", "pillAt('%s'" % c['pill'])
sub("stroked('GUESS THE ANIMAL'", "stroked('GUESS THE %s'" % c['one'])
cols = ['#ff6b4a', '#ffb020', '#22c55e', '#a855f7']
sub("[['0–7','CURIOUS CUB','🐣','#ff6b4a'],['8–14','ANIMAL FAN','🐾','#ffb020'],['15–19','WILD EXPERT','🏆','#22c55e'],['20','ZOO GENIUS','🧠','#a855f7']]",
    js([t + [cols[i]] for i, t in enumerate(c['tiers'])]))
sub("stroked('ANIMALS',520,450,190", "stroked('%s',520,450,190" % c['word'])
sub("text('🌊🐴',1440,430", "text('%s',1440,430" % c['thumb'])
sub("'🐾🧠👇🐣🏆❓⭐🌊🐟🦀🦈🐸🦌'", js(c['icon'] + '🧠👇🏆❓' + ''.join(c['intro_emoji']) + ''.join(t[2] for t in c['tiers'])))
open(os.path.join(HERE, key + '.html'), 'w', encoding='utf-8').write(s)
for chk in ['ANIMAL', 'nimal', '🐾']:
    if chk in s: print('WARN leftover', chk, [s[m.start()-40:m.start()+20] for m in re.finditer(chk, s)][:4])
from kokoro_onnx import Kokoro
M = os.path.join(HERE, '..', '..', '.new', 'tts'); k = Kokoro(os.path.join(M, 'kokoro-v1.0.onnx'), os.path.join(M, 'voices-v1.0.bin'))
L = {'intro': c['intro'], 'r1': 'Round one. Easy.', 'r2': 'Round two. Medium. These take a little more thought.', 'r3': c['r3'],
     'end': 'How many did you get out of twenty? Tell me in the comments, and subscribe for a new quiz every few days!',
     'plug': 'Want more? Play over twelve hundred free brain teasers, at brain teasers club dot app.'}
n = 0
for _, items in c['rounds']:
    for q, a, w in items:
        n += 1; L[f'a{n}'] = a.title().replace("'S", "'s") + '!'
out = os.path.join(HERE, c['voice'].strip('/')); os.makedirs(out, exist_ok=True); dur = {}
for nm, t in L.items():
    smp, sr = k.create(t, voice='af_heart', speed=1.1, lang='en-us'); sf.write(os.path.join(out, nm + '.wav'), smp, sr); dur[nm] = round(len(smp) / sr, 2)
json.dump(dur, open(os.path.join(out, 'durations.json'), 'w')); print(key, n, 'items', len(dur), 'lines')
