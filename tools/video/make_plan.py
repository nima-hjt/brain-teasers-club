# Builds "Posting Plan - Brain Teasers.docx" in the Brain Teasers folder (plain WordprocessingML, no external libraries).
# Add every new video to VIDEOS (date, time, files, YouTube title/description/tags/pin, Instagram caption) and re-run.
import zipfile, os
from xml.sax.saxutils import escape

OUT = r'C:\Users\nhojjat.d3security\Downloads\brain-teasers-club-repo\Brain Teasers\Posting Plan - Brain Teasers.docx'
LINK_YT, LINK_IG, LINK_FB = 'https://brainteasersclub.app/btc', 'brainteasersclub.app/ig', 'https://brainteasersclub.app/fb'

body = []
def run(t, b=False, mono=False, color=None, size=None, i=False):
    rpr = ''
    if mono: rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
    if b: rpr += '<w:b/>'
    if i: rpr += '<w:i/>'
    if color: rpr += f'<w:color w:val="{color}"/>'
    if size: rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
def p(*runs, style=None, shade=None, after=120, keep=False, indent=None):
    ppr = ''
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if keep: ppr += '<w:keepNext/>'
    if shade: ppr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    ppr += f'<w:spacing w:before="0" w:after="{after}"/>'
    if indent: ppr += f'<w:ind w:left="{indent}"/>'
    body.append(f'<w:p><w:pPr>{ppr}</w:pPr>{"".join(runs)}</w:p>')
def h(t, lvl=1): p(run(t), style=f'Heading{lvl}', keep=True)
def label(t): p(run(t, b=True, color='5B3FB8'), after=40, keep=True)
def copy(lines):  # a grey "copy and paste" box
    for k, line in enumerate(lines):
        p(run(line if line else ' ', mono=True, size=19), shade='F1F1F4', after=0 if k < len(lines) - 1 else 160, indent=120)
def bullet(t, b=None):
    runs = [run('•  ')] + ([run(b, b=True), run(t)] if b else [run(t)])
    p(*runs, indent=360, after=60)
def pagebreak(): body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
def table(rows, widths):
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:tblBorders>' + ''.join(f'<w:{s} w:val="single" w:sz="4" w:color="BFBFC8"/>' for s in ('top','left','bottom','right','insideH','insideV')) + f'</w:tblBorders><w:tblCellMar><w:left w:w="90" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
    for ri, r in enumerate(rows):
        cells = ''
        for ci, c in enumerate(r):
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="5B3FB8"/>' if ri == 0 else ('<w:shd w:val="clear" w:color="auto" w:fill="F6F4FB"/>' if ri % 2 == 0 else '')
            cells += f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/>{shade}</w:tcPr><w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>{run(c, b=ri == 0, color="FFFFFF" if ri == 0 else None, size=19)}</w:p></w:tc>'
        out.append(f'<w:tr>{cells}</w:tr>')
    out.append('</w:tbl>')
    body.append(''.join(out)); p(run(''), after=120)

PIN = 'How many did you get? 👇 Play 1,200+ more free: brainteasersclub.app/btc'
VIDEOS = [
 dict(date='Sun Oct 5', time='12:00 pm', kind='Long video (16:9)', status='Posted',
      file='Guess 20 Movies by Emoji - Easy to Hard (long).mp4', thumb='Guess 20 Movies by Emoji - thumbnail.png',
      title='Guess 20 Movies by Emoji 🎬 Easy to Hard | Emoji Movie Quiz',
      desc=['Can you guess all 20 movies from just emoji? 🎬 It starts easy and gets harder every round. Keep score and comment how many you got!','','0:00 Intro','0:06 Round 1: Easy','1:03 Round 2: Medium','2:01 Round 3: Hard','2:52 Your score','','🧠 Play 1,200+ free brain teasers – daily challenge, play with friends, no app needed:',LINK_YT,'','#emojiquiz #guessthemovie #moviequiz'],
      tags='emoji quiz, guess the movie, movie quiz, emoji challenge, brain teasers, guess the movie by emoji, quiz, trivia',
      pin=['How many movies did you get out of 20? 🎬👇','Movie Newbie (0–7) · Film Fan (8–14) · Movie Buff (15–19) · Cinema Genius (20)','🧠 Play 1,200+ more free puzzles: brainteasersclub.app/btc'],
      ig=None, endscreen='Subscribe + 1 video, from 2:52 to the end'),
 dict(date='Sun Oct 5', time='6:00 pm', kind='Short', status='Scheduled',
      file='Guess the Movie by Emoji 🎬 3 Seconds Each #shorts.mp4',
      title='Guess the Movie by Emoji 🎬 3 Seconds Each #shorts',
      desc=['Can you guess all 5 movies from the emoji? 🎬 Comment your score!','1,200+ free brain teasers: '+LINK_YT,'#shorts #emojiquiz #guessthemovie #braintest #quiz'],
      tags='guess the movie by emoji, emoji quiz, movie quiz, guess the movie, emoji movie quiz, emoji challenge, movie emoji quiz, brain teasers, quiz shorts, trivia',
      ig=['Can you guess all 5 movies from just emoji? 🎬 3 seconds each!','Comment your score 👇','','🧠 1,200+ free brain teasers — link in bio','','#emojiquiz #guessthemovie #moviequiz #braintest #quiz']),
 dict(date='Mon Oct 6', time='6:00 pm', kind='Short', status='To schedule',
      file='Oct 6 - Guess the Food by Emoji 🍔 #shorts.mp4',
      title='Guess the Food by Emoji 🍔 3 Seconds Each #shorts',
      desc=['Can you guess all 5 foods from the emoji? 🍔 Comment your score!','1,200+ free brain teasers: '+LINK_YT,'#shorts #emojiquiz #foodquiz #guessthefood #quiz'],
      tags='guess the food by emoji, emoji quiz, food quiz, guess the food, emoji challenge, brain teasers, quiz shorts',
      ig=['Guess all 5 foods from the emoji 🍔 3 seconds each — the last one is tricky!','Comment your score 👇','','🧠 1,200+ free brain teasers — link in bio','','#emojiquiz #foodquiz #guessthefood #braintest #quiz']),
 dict(date='Tue Oct 7', time='6:00 pm', kind='Short', status='To schedule',
      file='Oct 7 - Find the Odd One Out 👀 #shorts.mp4',
      title='Find the Odd One Out 👀 Can Your Eyes Beat the Clock? #shorts',
      desc=['3 levels, 6 seconds each 👀 How many did you find? Comment below!','1,200+ free brain teasers: '+LINK_YT,'#shorts #oddoneout #findtheodd #eyetest #braintest'],
      tags='find the odd one out, odd one out, emoji puzzle, eye test, spot the difference, brain teasers, visual puzzle',
      ig=['Can your eyes beat the clock? 👀 3 levels, 6 seconds each.','How many did you find? 👇','','🧠 1,200+ free brain teasers — link in bio','','#oddoneout #eyetest #findtheodd #braintest #puzzle']),
 dict(date='Wed Oct 8', time='6:00 pm', kind='Short', status='To schedule',
      file='Oct 8 - 3 Riddles in 30 Seconds 🧩 #shorts.mp4',
      title='3 Riddles in 30 Seconds 🧩 Can You Solve Them All? #shorts',
      desc=['3 riddles, 6 seconds each 🧩 How many did you get? Comment your score!','1,200+ free brain teasers: '+LINK_YT,'#shorts #riddles #brainteasers #riddlechallenge #quiz'],
      tags='riddles, riddles with answers, brain teasers, riddle challenge, tricky riddles, quiz shorts, logic puzzles',
      ig=['3 riddles, 6 seconds each 🧩 No peeking at the answers!','How many did you solve? 👇','','🧠 1,200+ free brain teasers — link in bio','','#riddles #brainteasers #riddlechallenge #quiz #logic']),
 dict(date='Thu Oct 9', time='12:00 pm', kind='Long video (16:9)', status='To schedule',
      file='Guess 20 Animals by Emoji - Easy to Hard (long, Oct 9).mp4', thumb='Guess 20 Animals by Emoji - thumbnail.png',
      title='Guess 20 Animals by Emoji 🐾 Emoji + Emoji = Animal | Easy to Hard',
      desc=['Two emoji make one animal 🐾 Can you guess all 20? It starts easy and gets harder every round. Keep score and comment how many you got!','','0:00 Intro','0:07 Round 1: Easy','1:04 Round 2: Medium','2:02 Round 3: Hard','2:53 Your score','','🧠 Play 1,200+ free brain teasers – daily challenge, play with friends, no app needed:',LINK_YT,'','#emojiquiz #animalquiz #guesstheanimal'],
      tags='emoji quiz, guess the animal, animal quiz, emoji challenge, brain teasers, animal riddles, quiz, trivia',
      pin=['How many animals did you get out of 20? 🐾👇','Curious Cub (0–7) · Animal Fan (8–14) · Wild Expert (15–19) · Zoo Genius (20)','🧠 Play 1,200+ more free puzzles: brainteasersclub.app/btc'],
      ig=None, endscreen='Subscribe + 1 video, from 2:53 to the end'),
 dict(date='Thu Oct 9', time='6:00 pm', kind='Short', status='To schedule',
      file='Oct 9 - Guess the Saying by Emoji 💬 #shorts.mp4',
      title='Guess the Saying by Emoji 💬 3 Seconds Each #shorts',
      desc=['Can you guess all 5 sayings from the emoji? 💬 Comment your score!','1,200+ free brain teasers: '+LINK_YT,'#shorts #emojiquiz #idioms #guessthesaying #quiz'],
      tags='guess the saying by emoji, emoji quiz, idioms quiz, english idioms, emoji challenge, brain teasers, quiz shorts',
      ig=['Can you guess all 5 sayings from the emoji? 💬 3 seconds each!','Comment your score 👇','','🧠 1,200+ free brain teasers — link in bio','','#emojiquiz #idioms #guessthesaying #braintest #quiz']),
 dict(date='Fri Oct 10', time='6:00 pm', kind='Short', status='To schedule',
      file='Oct 10 - Find the Odd Letter 🔤 #shorts.mp4',
      title='Find the Odd Letter 🔤 Level 2 Fools Everyone #shorts',
      desc=['3 levels, 6 seconds each 🔤 Did level 2 trick you? Comment below!','1,200+ free brain teasers: '+LINK_YT,'#shorts #oddoneout #eyetest #findtheodd #braintest'],
      tags='find the odd one out, odd letter, eye test, optical illusion, visual puzzle, brain teasers, spot the difference',
      ig=['Find the odd letter 🔤 Level 2 fools a lot of people 👀','Did it get you? 👇','','🧠 1,200+ free brain teasers — link in bio','','#oddoneout #eyetest #findtheodd #opticalillusion #braintest']),
 dict(date='Sat Oct 11', time='6:00 pm', kind='Short', status='To schedule',
      file='Oct 11 - Find the Odd One Out 2 👀 #shorts.mp4',
      title='Find the Odd One Out 👀 Level 3 Is Almost Impossible #shorts',
      desc=['3 levels, 6 seconds each 👀 How many did you find? Comment below!','1,200+ free brain teasers: '+LINK_YT,'#shorts #oddoneout #findtheodd #eyetest #braintest'],
      tags='find the odd one out, odd one out, emoji puzzle, eye test, spot the difference, brain teasers, visual puzzle',
      ig=['3 levels, 6 seconds each 👀 Level 3 is almost impossible!','How many did you find? 👇','','🧠 1,200+ free brain teasers — link in bio','','#oddoneout #eyetest #findtheodd #braintest #puzzle']),
]

# ---------- document ----------
p(run('Brain Teasers — Posting Plan', b=True, size=44, color='1B1B3A'), after=60)
p(run('Everything to copy and paste for each upload: YouTube title, description, tags and pinned comment, plus the Instagram and Facebook captions. All video files are in this same folder.', color='555566'), after=200)

h('Same for every video')
bullet(' Not made for kids · No age restriction · Category: Entertainment · Language: English', 'YouTube settings:')
bullet(' Shorts at 6:00 pm daily · long videos at 12:00 pm every 4 days', 'Times:')
bullet(' YouTube Brain Teasers /btc · YouTube Wild Facts /wildfacts · Facebook /fb · Instagram /ig (bio only)', 'Tracking links (brainteasersclub.app + ...):')
bullet(' share the Reel to your Story with a Link sticker (brainteasersclub.app/ig) and a Poll sticker.', 'Instagram after posting:')
bullet(' use the Instagram caption, but replace "link in bio" with ' + LINK_FB + ' (clickable on Facebook).', 'Facebook:')
bullet(' "99% fail", "Only 1% get it", "Most adults fail" — they are made-up statistics.', 'Avoid in titles:')

h('Schedule at a glance')
table([['Date', 'Time', 'Type', 'Video', 'Status']] + [[v['date'], v['time'], v['kind'], v['title'].replace(' #shorts', ''), v['status']] for v in VIDEOS], [1300, 1000, 1500, 4300, 1260])

h('How to pin or change the first comment')
label('YouTube (phone app or computer)')
for t in ['Open the video and post the comment from the channel account (your channel name must show as the author).',
          'Tap ⋮ (three dots) next to your comment → Pin. It moves to the top with a pin icon.',
          'To change it later: ⋮ on the pinned comment → Edit, or post a new comment and pin it (only one comment can be pinned, so the new one replaces the old).',
          'On a computer you can also use YouTube Studio → Comments, find your comment, ⋮ → Pin.']:
    bullet(' ' + t)
label('Instagram')
for t in ['Post the comment from your account, then press and hold it (or swipe left on iPhone) → tap the pin icon. Up to 3 comments can be pinned.',
          'Captions can be edited: ⋯ on the post → Edit. Links in captions are not clickable, so use "link in bio".']:
    bullet(' ' + t)
label('Facebook')
for t in ['Comment on the post, then ⋯ next to your comment → Pin comment (Pages). Edit the post text with ⋯ → Edit post; links in posts are clickable.']:
    bullet(' ' + t)

for v in VIDEOS:
    pagebreak()
    h(f"{v['date']} · {v['time']} · {v['kind']}  —  {v['status']}")
    p(run('File: ', b=True), run(v['file']), after=40)
    if v.get('thumb'): p(run('Thumbnail: ', b=True), run(v['thumb']), after=40)
    if v.get('endscreen'): p(run('End screen: ', b=True), run(v['endscreen']), after=40)
    p(run(''), after=60)
    h('YouTube', 2)
    label('Title'); copy([v['title']])
    label('Description'); copy(v['desc'])
    label('Tags'); copy([v['tags']])
    label('Pinned comment'); copy(v.get('pin') or [PIN])
    if v['ig']:
        h('Instagram (Reel)', 2); label('Caption'); copy(v['ig'])
        h('Facebook', 2); label('Post text'); copy([l.replace('link in bio', LINK_FB) for l in v['ig']])
    else:
        h('Instagram / Facebook', 2)
        p(run('Long widescreen video — not suited to Reels. Post the matching Short instead, or ask for a 30-second vertical cut-down.', i=True, color='555566'))

doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
       '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + ''.join(body) +
       '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
 '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
 '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
 '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="100"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="1B1B3A"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>'
 '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="C2552D"/><w:sz w:val="25"/><w:szCs w:val="25"/></w:rPr></w:style>'
 '</w:styles>')
ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
    z.writestr('word/document.xml', doc); z.writestr('word/styles.xml', styles); z.writestr('word/_rels/document.xml.rels', drels)
print('wrote', OUT, os.path.getsize(OUT), 'bytes,', len(VIDEOS), 'videos')
