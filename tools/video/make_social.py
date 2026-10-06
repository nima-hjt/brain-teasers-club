# Builds "Instagram-Facebook\Posting Plan - Instagram & Facebook.docx" (plain WordprocessingML, no libraries).
# Instagram account @wildfactsquiz auto-shares every Reel to the Facebook page, so each Reel is posted once on
# Instagram; afterwards a comment with the clickable link is added on Facebook. Two Reels a day: Brain Teasers at
# 12 pm, Wild Facts at 6 pm, each one day after its YouTube premiere. Never repeat a puzzle already posted on
# Instagram (see posted.md). Remove a Reel's entry once it is posted and re-run.
import zipfile, os, datetime
from xml.sax.saxutils import escape

ROOT = r'C:\Users\nhojjat.d3security\Downloads\brain-teasers-club-repo'
OUT = os.path.join(ROOT, 'Instagram-Facebook', 'Posting Plan - Instagram & Facebook.docx')
TAIL = '🧠 1,200+ free brain teasers: link in bio'
FB_COMMENT = ['🧠 Play 1,200+ free puzzles here 👉 https://brainteasersclub.app/fb']
def day(d): return datetime.date(2026, 10, d).strftime('%a %b %#d' if os.name == 'nt' else '%a %b %-d')

# (day, time, file, caption lines, hashtags)
R = [
 (7, '12:00 pm', 'Oct 7 12pm - Guess the Food by Emoji 🍔.mp4', ['Guess all 5 foods from the emoji 🍔 3 seconds each! The last one is tricky 😈', 'Comment your score 👇'], '#emojiquiz #foodquiz #guessthefood #brainteaser'),
 (7, '6:00 pm', 'Oct 7 6pm - Ocean Quiz 3 Questions 🐬.mp4', ['Ocean quiz 🐬 3 questions, 5 seconds each. Can you get 3/3?', 'Comment your score 👇'], '#oceanquiz #animalquiz #quiz #trivia'),
 (8, '12:00 pm', 'Oct 8 12pm - Find the Odd One Out 👀.mp4', ['Can your eyes beat the clock? 👀 3 levels, 6 seconds each. Level 3 is the tricky one.', 'How many did you find? 👇'], '#oddoneout #eyetest #puzzle #brainteaser'),
 (8, '6:00 pm', 'Oct 8 6pm - Animal Group Names Quiz 🦉.mp4', ['Animal group names 🦉 3 questions. Can you get 3/3?', 'Comment your score 👇'], '#animalfacts #didyouknow #animals #quiz'),
 (9, '12:00 pm', 'Oct 9 12pm - 3 Riddles in 30 Seconds 🧩.mp4', ['3 riddles, 6 seconds each 🧩 No peeking!', 'How many did you solve? 👇'], '#riddles #brainteasers #riddlechallenge #quiz'),
 (9, '6:00 pm', 'Oct 9 6pm - Kids vs Parents Animal Quiz 🐯.mp4', ['Kids vs parents 🐯 3 animal questions. Who gets 3/3?', 'Tell us who won 👇'], '#kidsvsparents #animalquiz #familyquiz #quiz'),
 (10, '12:00 pm', 'Oct 10 12pm - Guess the Saying by Emoji 💬.mp4', ['Guess all 5 sayings from the emoji 💬 3 seconds each!', 'Comment your score 👇'], '#emojiquiz #idioms #guessthesaying #brainteaser'),
 (10, '6:00 pm', 'Oct 10 6pm - Bird Quiz 🦜.mp4', ['Bird quiz 🦜 5 questions, 3 seconds each! The last one is the hardest.', 'Comment your score 👇'], '#birdquiz #animalquiz #quiz #trivia'),
 (11, '12:00 pm', 'Oct 11 12pm - Find the Odd Letter 🔤.mp4', ['Find the odd letter 🔤 Level 2 fools a lot of people 👀', 'Did it get you? 👇'], '#oddoneout #eyetest #opticalillusion #brainteaser'),
 (11, '6:00 pm', 'Oct 11 6pm - 3 Bug Facts That Sound Fake 🐜.mp4', ['3 bug facts that sound fake, but are true 🐜', 'Which one surprised you most? 👇'], '#animalfacts #insects #didyouknow #facts'),
 (12, '12:00 pm', 'Oct 12 12pm - Find the Odd One Out 👀.mp4', ['Find the odd one out 👀 Fruit, faces and clocks. Level 3 takes a second look!', 'How many did you find? 👇'], '#oddoneout #eyetest #puzzle #brainteaser'),
 (12, '6:00 pm', 'Oct 12 6pm - 3 Space Facts 🌙.mp4', ['3 space facts that sound unreal 🌙', 'Which one surprised you most? 👇'], '#space #spacefacts #didyouknow #facts'),
 (13, '12:00 pm', 'Oct 13 12pm - Spot the Different Face 👀.mp4', ['Spot the different face 👀 3 levels, 6 seconds each.', 'How many did you find? 👇'], '#oddoneout #eyetest #puzzle #brainteaser'),
 (13, '6:00 pm', 'Oct 13 6pm - Food Quiz 🍯.mp4', ['Food quiz 🍯 3 questions. Question 3 is tricky!', 'Comment your score 👇'], '#foodquiz #foodfacts #quiz #trivia'),
 (14, '12:00 pm', 'Oct 14 12pm - Guess the Fairy Tale by Emoji 🏰.mp4', ['Guess all 5 fairy tales from the emoji 🏰 3 seconds each!', 'Comment your score 👇'], '#emojiquiz #fairytale #guessthestory #brainteaser'),
 (14, '6:00 pm', 'Oct 14 6pm - 3 Eye Facts That Sound Fake 👀.mp4', ['3 facts about your eyes that sound fake, but are true 👀', 'Which one surprised you most? 👇'], '#eyefacts #humanbody #didyouknow #facts'),
 (15, '12:00 pm', 'Oct 15 12pm - 3 Riddles in 30 Seconds 🧩.mp4', ['3 riddles, 6 seconds each 🧩 Can you beat the timer?', 'How many did you solve? 👇'], '#riddles #brainteasers #riddlechallenge #quiz'),
 (15, '6:00 pm', 'Oct 15 6pm - 3 Animal Facts That Sound Fake 🦛.mp4', ['3 animal facts that sound fake, but are true 🦛', 'Which one surprised you most? 👇'], '#animalfacts #didyouknow #facts #animals'),
 (16, '12:00 pm', 'Oct 16 12pm - Find the Odd One Out 👀.mp4', ['Find the odd one out 👀 Trees, smiles and clocks. 6 seconds each!', 'How many did you find? 👇'], '#oddoneout #eyetest #puzzle #brainteaser'),
 (16, '6:00 pm', 'Oct 16 6pm - Kids vs Parents Animal Quiz 🐼.mp4', ['Kids vs parents, round 2 🐼 3 new animal questions. Who gets 3/3?', 'Tell us who won 👇'], '#kidsvsparents #animalquiz #familyquiz #quiz'),
 (17, '12:00 pm', 'Oct 17 12pm - Guess the Cartoon Movie by Emoji 🎬.mp4', ['Guess the animated movie from the emoji 🎬 3 seconds each!', 'Comment your score 👇'], '#emojiquiz #guessthemovie #disneyquiz #brainteaser'),
 (17, '6:00 pm', 'Oct 17 6pm - Dinosaur Quiz 🦖.mp4', ['Dinosaur quiz 🦖 5 questions, 3 seconds each! The last one surprises everyone.', 'Comment your score 👇'], '#dinosaurs #dinosaurquiz #quiz #trivia'),
 (18, '12:00 pm', 'Oct 18 12pm - Find the Odd One Out 🔤.mp4', ['Find the odd one 🔤 Letters and numbers edition. Level 3 is sneaky!', 'Did it get you? 👇'], '#oddoneout #eyetest #opticalillusion #brainteaser'),
 (18, '6:00 pm', 'Oct 18 6pm - 3 Ocean Facts That Sound Fake 🦦.mp4', ['3 ocean facts that sound fake, but are true 🦦', 'Which one surprised you most? 👇'], '#oceanfacts #didyouknow #facts #animals'),
 (19, '12:00 pm', 'Oct 19 12pm - Guess the Halloween Word by Emoji 🎃.mp4', ['Halloween is coming 🎃 Guess all 5 spooky words from the emoji!', 'Comment your score 👇'], '#halloween #emojiquiz #halloweenquiz #brainteaser'),
 (19, '6:00 pm', 'Oct 19 6pm - Science Quiz 🔬.mp4', ['Science quiz 🔬 3 questions. The last one surprises everyone!', 'Comment your score 👇'], '#sciencequiz #science #quiz #trivia'),
 (20, '12:00 pm', 'Oct 20 12pm - 3 Riddles in 30 Seconds 🧩.mp4', ['3 riddles, 6 seconds each 🧩 The last one is the hardest!', 'How many did you solve? 👇'], '#riddles #brainteasers #riddlechallenge #quiz'),
 (20, '6:00 pm', 'Oct 20 6pm - Baby Animal Names Quiz 🐣.mp4', ['What do you call these baby animals? 🐣 3 seconds each!', 'Comment your score 👇'], '#babyanimals #animalquiz #quiz #trivia'),
 (21, '6:00 pm', 'Oct 21 6pm - World Quiz 🌍.mp4', ['World quiz 🌍 5 questions, 3 seconds each! The last one surprises a lot of people.', 'Comment your score 👇'], '#geography #worldquiz #quiz #trivia'),
]

body = []
def run(t, b=False, mono=False, color=None, size=None):
    rpr = ('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>' if mono else '') + ('<w:b/>' if b else '') + \
          (f'<w:color w:val="{color}"/>' if color else '') + (f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>' if size else '')
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
def p(*runs, style=None, shade=None, after=120, keep=False, indent=None):
    ppr = (f'<w:pStyle w:val="{style}"/>' if style else '') + ('<w:keepNext/>' if keep else '') + \
          (f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else '') + f'<w:spacing w:before="0" w:after="{after}"/>' + \
          (f'<w:ind w:left="{indent}"/>' if indent else '')
    body.append(f'<w:p><w:pPr>{ppr}</w:pPr>{"".join(runs)}</w:p>')
def h(t, lvl=1): p(run(t), style=f'Heading{lvl}', keep=True)
def label(t): p(run(t, b=True, color='5B3FB8'), after=30, keep=True)
def field(n, v): p(run(n + ': ', b=True, color='5B3FB8'), run(v), after=50)
def copy(lines):
    for k, line in enumerate(lines):
        p(run(line if line else ' ', mono=True, size=19), shade='F1F1F4', after=0 if k < len(lines) - 1 else 140, indent=120)

p(run('Instagram & Facebook — Posting Plan', b=True, size=44, color='1B1B3A'), after=60)
p(run('Post each Reel on Instagram (@wildfactsquiz); it shares to the Facebook page by itself. Then add the Facebook comment with the link. Remove a section once it is posted.', color='555566'), after=60)
h('Every time (same steps for each Reel)')
for s in ['1. Instagram app → + → Reel → choose the file → Next.',
          '2. Cover: pick a frame that shows the puzzle (not a blank or end screen).',
          '3. Paste the caption below. Make sure "Share to Facebook" is on (it stays on once set).',
          '4. Share now at the time shown, or Advanced settings → Schedule.',
          '5. When it appears on Facebook (a few minutes later): open the post on the Facebook page, paste the Facebook comment, then ⋯ → Pin comment.']:
    p(run(s), after=50, indent=200)
h('Schedule')
rows = [['Date', 'Time', 'Reel']] + [[day(d), tm, f.split(' - ', 1)[1].rsplit('.', 1)[0]] for d, tm, f, c, tags in R]
grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in (1500, 1100, 7400))
tbl = ['<w:tbl><w:tblPr><w:tblW w:w="10000" w:type="dxa"/><w:tblBorders>' + ''.join(f'<w:{s} w:val="single" w:sz="4" w:color="BFBFC8"/>' for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) + f'</w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
for ri, r in enumerate(rows):
    tbl.append('<w:tr>' + ''.join(f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>' + ('<w:shd w:val="clear" w:color="auto" w:fill="5B3FB8"/>' if ri == 0 else '') + f'</w:tcPr><w:p>{run(c, b=ri == 0, color="FFFFFF" if ri == 0 else None, size=18)}</w:p></w:tc>' for c, w in zip(r, (1500, 1100, 7400))) + '</w:tr>')
tbl.append('</w:tbl>'); body.append(''.join(tbl)); p(run(''), after=100)
for d, tm, f, cap, tags in R:
    body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    h(f'{day(d)} · {tm}')
    field('File', f)
    label('Caption (Instagram, shared to Facebook)'); copy(cap + ['', TAIL, '', tags])
    label('Facebook comment, then pin it'); copy(FB_COMMENT)

doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + ''.join(body) +
       '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1000" w:right="1000" w:bottom="1000" w:left="1000" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
          '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="1B1B3A"/><w:sz w:val="30"/></w:rPr></w:style></w:styles>')
ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
drels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'
try: open(OUT, 'ab').close()
except PermissionError: raise SystemExit('LOCKED (close it in Word, then re-run): ' + OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels); z.writestr('word/document.xml', doc); z.writestr('word/styles.xml', styles); z.writestr('word/_rels/document.xml.rels', drels)
missing = [f for d, tm, f, c, t in R if not os.path.exists(os.path.join(ROOT, 'Instagram-Facebook', f))]
print('wrote', OUT, len(R), 'reels; missing files:', missing or 'none')
