import struct, math
# Builds the two posting plans (plain WordprocessingML, no external libraries):
#   Brain Teasers\Posting Plan - Brain Teasers.docx   and   Wild Facts\Posting Plan - Wild Facts.docx
# Each video gets one self-contained section in YouTube Studio upload order, ready to copy and paste.
# When a video is uploaded, delete its entry from BT or WF below and re-run.
import zipfile, os, datetime
from xml.sax.saxutils import escape

ROOT = r'C:\Users\nhojjat.d3security\Downloads\brain-teasers-club-repo'
BTC, WFL, FB = 'https://brainteasersclub.app/btc', 'https://brainteasersclub.app/wildfacts', 'https://brainteasersclub.app/fb'

def day(d): return datetime.date(2026, 10, d).strftime('%a %b %-d') if os.name != 'nt' else datetime.date(2026, 10, d).strftime('%a %b %#d')

# ---------------- Brain Teasers ----------------
BT_PIN = ['How many did you get? Comment your score 👇', '🧠 Play 1,200+ more free puzzles: brainteasersclub.app/btc']
BT_FOOT = ['', '🧠 Play 1,200+ free brain teasers (daily challenge, play with friends, no download needed):', BTC]
# Links are not clickable in Shorts descriptions or comments, so Shorts show the plain, easy-to-type address.
SITE = 'brainteasersclub.app'
BT_FOOT_SHORT = ['', '🧠 Play 1,200+ free brain teasers at ' + SITE + ' (daily challenge, play with friends, no download needed)']
BT_PIN_SHORT = ['How many did you get? Comment your score 👇', '🧠 Play 1,200+ more free puzzles: ' + SITE]
def bt_short(d, file, title, hook, tags, hashtags, ig, playlist, related=None):
    related = related or ('Guess 20 Movies by Emoji (long video)' if d < 9 else 'Guess 20 Animals by Emoji (long video)')
    return dict(d=d, time='6:00 pm', kind='Short', file=file, title=title + ' #shorts', desc=[hook] + BT_FOOT_SHORT + ['', '#shorts ' + hashtags],
                tags=tags, playlist=playlist, category='Entertainment', related=related, pin=BT_PIN_SHORT,
                ig=ig + ['', '🧠 1,200+ free brain teasers: link in bio', '', hashtags], ig_time='12:00 pm')
def bt_long(d, file, thumb, title, hook, chapters, tags, hashtags, pin, credits=()):
    chapters = [chapters] if isinstance(chapters, str) else chapters
    return dict(d=d, time='12:00 pm', kind='Long video (16:9)', file=file, thumb=thumb, title=title,
                desc=[hook, ''] + chapters + BT_FOOT + ([''] + list(credits) if credits else []) + ['', hashtags], tags=tags, playlist='Puzzle Videos', category='Entertainment',
                endscreen='Element 1: Subscribe. Element 2: Video → "Best for viewer". Start at ' + chapters[-1].split()[0] + ', run to the end.', pin=pin)

# Animal photos in the Oct 9 long video (Wikimedia Commons; sources in .new/vid/animals_img/sources.json)
ANIMAL_CREDITS = ['📷 Animal photos from Wikimedia Commons:',
  'Starfish: Katie Ahlfeld (CC BY-SA 4.0) · Seahorse: Hans Hillewaert (CC BY-SA 4.0) · Catfish: HalbsHännile, Thomsonmg2000, Guillermo Enrique Terán (CC BY-SA 4.0) · '
  'Swordfish: Naturalis Biodiversity Center (CC0) · Bullfrog: Carl D. Howe (CC BY-SA 2.5) · Honey bee: Andreas Trepte (CC BY-SA 2.5) · '
  'Lionfish: Jens Petersen (CC BY 2.5) · Reindeer: Are G Nilsen (CC BY-SA 3.0) · Sea lion: Jonathan Eisen (CC BY 4.0) · '
  'Tiger shark, hammerhead shark: Albert kok (CC BY-SA 3.0 / 4.0) · King crab: Roger Mann, VIMS (public domain) · '
  'Blue whale: NOAA (public domain) · Dogfish: Doug Costa, NOAA (public domain) · Kangaroo rat: public domain · '
  'Manatee: Galen Rathbun (public domain) · Zebrafish: Azul (free use) · Ghost crab: Rushenb (CC BY-SA 3.0) · '
  'Frogfish: Christian Gloor (CC BY 2.0) · Deer mouse: Seney Natural History Association (CC BY-SA 2.0)']

BT = [
 bt_long(9, 'Guess 20 Animals by Emoji - Easy to Hard (long, Oct 9).mp4', 'Guess 20 Animals by Emoji - thumbnail.png',
   'Guess 20 Animals by Emoji 🐾 Emoji + Emoji = Animal | Easy to Hard',
   'Two emoji make one animal 🐾 Can you guess all 20? It starts easy and gets harder every round. Keep score and comment how many you got!',
   ['0:00 Intro', '0:07 Round 1: Easy', '1:04 Round 2: Medium', '2:02 Round 3: Hard', '2:53 Your score'],
   'emoji quiz, guess the animal, animal quiz, emoji challenge, brain teasers, animal riddles, quiz, trivia', '#emojiquiz #animalquiz #guesstheanimal',
   ['How many animals did you get out of 20? 🐾👇', 'Curious Cub (0–7) · Animal Fan (8–14) · Wild Expert (15–19) · Zoo Genius (20)', '🧠 Play 1,200+ more free puzzles: brainteasersclub.app/btc'], ANIMAL_CREDITS),
 bt_short(9, 'Oct 9 - Guess the Saying by Emoji 💬 #shorts.mp4', 'Guess the Saying by Emoji 💬 3 Seconds Each',
   'Can you guess all 5 sayings from the emoji? 💬 Comment your score!',
   'guess the saying by emoji, emoji quiz, idioms quiz, english idioms, emoji challenge, brain teasers, quiz shorts', '#emojiquiz #idioms #guessthesaying #quiz',
   ['Can you guess all 5 sayings from the emoji? 💬 3 seconds each!', 'Comment your score 👇'], 'Puzzle Videos'),
 bt_short(10, 'Oct 10 - Find the Odd Letter 🔤 #shorts.mp4', 'Find the Odd Letter 🔤 Level 2 Fools Everyone',
   '3 levels, 6 seconds each 🔤 Did level 2 trick you? Comment below!',
   'find the odd one out, odd letter, eye test, optical illusion, visual puzzle, brain teasers, spot the difference', '#oddoneout #eyetest #findtheodd #braintest',
   ['Find the odd letter 🔤 Level 2 fools a lot of people 👀', 'Did it get you? 👇'], 'Puzzle Videos'),
 bt_short(11, 'Oct 11 - Find the Odd One Out 2 👀 #shorts.mp4', 'Find the Odd One Out 👀 Level 3 Is Almost Impossible',
   '3 levels, 6 seconds each 👀 How many did you find? Comment below!',
   'find the odd one out, odd one out, emoji puzzle, eye test, spot the difference, brain teasers, visual puzzle', '#oddoneout #findtheodd #eyetest #braintest',
   ['3 levels, 6 seconds each 👀 Level 3 is almost impossible!', 'How many did you find? 👇'], 'Puzzle Videos'),
 bt_short(12, 'Oct 12 - Find the Odd One Out 3 👀 #shorts.mp4', 'Find the Odd One Out 👀 Only Sharp Eyes Find Level 3',
   '3 levels, 6 seconds each 👀 Faces this time! How many did you find? Comment below!',
   'find the odd one out, odd one out, emoji puzzle, eye test, spot the difference, brain teasers, visual puzzle', '#oddoneout #findtheodd #eyetest #braintest',
   ['Find the odd emoji 👀 3 levels, 6 seconds each.', 'How many did you find? 👇'], 'Puzzle Videos'),
 bt_long(13, 'Oct 13 - Guess 20 Foods by Emoji - Easy to Hard (long).mp4', 'Oct 13 - Guess 20 Foods by Emoji - thumbnail.png',
   'Guess 20 Foods by Emoji 🍔 Easy to Hard | Emoji Food Quiz',
   'Can you guess all 20 foods from just emoji? 🍔 It starts easy and gets harder every round. Keep score and comment how many you got!',
   'CHAPTERS_FOODS', 'emoji quiz, guess the food, food quiz, emoji challenge, brain teasers, guess the food by emoji, quiz, trivia', '#emojiquiz #foodquiz #guessthefood',
   ['How many foods did you get out of 20? 🍔👇', 'Snack Rookie (0–7) · Food Fan (8–14) · Top Chef (15–19) · Food Genius (20)', '🧠 Play 1,200+ more free puzzles: brainteasersclub.app/btc']),
 bt_short(13, 'Oct 13 - Guess the Fairy Tale by Emoji 🏰 #shorts.mp4', 'Guess the Fairy Tale by Emoji 🏰 3 Seconds Each',
   'Can you guess all 5 fairy tales from the emoji? 🏰 Comment your score!',
   'guess the fairy tale by emoji, emoji quiz, fairy tale quiz, disney quiz, emoji challenge, brain teasers, quiz shorts', '#emojiquiz #fairytale #guessthestory #quiz',
   ['Guess all 5 fairy tales from the emoji 🏰 3 seconds each!', 'Comment your score 👇'], 'Puzzle Videos', 'Guess 20 Foods by Emoji (long video)'),
 bt_short(14, 'Oct 14 - 3 Riddles in 30 Seconds 2 🧩 #shorts.mp4', '3 Riddles in 30 Seconds 🧩 Can You Beat the Timer?',
   '3 riddles, 6 seconds each 🧩 How many did you get? Comment your score!',
   'riddles, riddles with answers, brain teasers, riddle challenge, tricky riddles, quiz shorts, logic puzzles', '#riddles #brainteasers #riddlechallenge #quiz',
   ['3 riddles, 6 seconds each 🧩 Can you beat the timer?', 'How many did you solve? 👇'], 'Puzzle Videos', 'Guess 20 Foods by Emoji (long video)'),
 bt_short(15, 'Oct 15 - Find the Odd One Out 4 👀 #shorts.mp4', 'Find the Odd One Out 👀 Level 3 Takes a Second Look',
   '3 levels, 6 seconds each 👀 How many did you find? Comment below!',
   'find the odd one out, odd one out, emoji puzzle, eye test, spot the difference, brain teasers, visual puzzle', '#oddoneout #findtheodd #eyetest #braintest',
   ['3 levels, 6 seconds each 👀 Level 3 takes a second look!', 'How many did you find? 👇'], 'Puzzle Videos', 'Guess 20 Foods by Emoji (long video)'),
 bt_short(16, 'Oct 16 - Guess the Cartoon Movie by Emoji 🎬 #shorts.mp4', 'Guess the Cartoon Movie by Emoji 🎬 3 Seconds Each',
   'Can you guess all 5 animated movies from the emoji? 🎬 Comment your score!',
   'guess the movie by emoji, emoji quiz, disney quiz, cartoon quiz, animated movie quiz, emoji challenge, brain teasers, quiz shorts', '#emojiquiz #guessthemovie #disneyquiz #quiz',
   ['Guess all 5 animated movies from the emoji 🎬 3 seconds each!', 'Comment your score 👇'], 'Puzzle Videos', 'Guess 20 Foods by Emoji (long video)'),
 bt_long(17, 'Oct 17 - Guess 20 Words by Emoji - Easy to Hard (long).mp4', 'Oct 17 - Guess 20 Words by Emoji - thumbnail.png',
   'Guess 20 Words by Emoji 🧩 Emoji + Emoji = Word | Easy to Hard',
   'Two emoji make one word 🧩 Can you guess all 20? It starts easy and gets harder every round. Keep score and comment how many you got!',
   'CHAPTERS_WORDS', 'emoji quiz, compound words, guess the word, word quiz, emoji challenge, brain teasers, emoji riddles, quiz', '#emojiquiz #wordquiz #guesstheword',
   ['How many words did you get out of 20? 🧩👇', 'Word Rookie (0–7) · Word Fan (8–14) · Word Wizard (15–19) · Word Genius (20)', '🧠 Play 1,200+ more free puzzles: brainteasersclub.app/btc']),
 bt_short(17, 'Oct 17 - Find the Odd One Out 5 🔤 #shorts.mp4', 'Find the Odd One Out 🔤 Letters and Numbers Edition',
   '3 levels, 6 seconds each 🔤 Did level 3 trick you? Comment below!',
   'find the odd one out, odd letter, eye test, optical illusion, visual puzzle, brain teasers, spot the difference', '#oddoneout #eyetest #findtheodd #braintest',
   ['Find the odd one 🔤 Letters and numbers edition!', 'Did level 3 get you? 👇'], 'Puzzle Videos', 'Guess 20 Words by Emoji (long video)'),
 bt_short(18, 'Oct 18 - Guess the Halloween Word by Emoji 🎃 #shorts.mp4', 'Guess the Halloween Word by Emoji 🎃 3 Seconds Each',
   'Halloween is coming 🎃 Can you guess all 5 spooky words from the emoji? Comment your score!',
   'halloween quiz, guess the word by emoji, emoji quiz, halloween emoji, emoji challenge, brain teasers, quiz shorts', '#halloween #emojiquiz #halloweenquiz #quiz',
   ['Halloween is coming 🎃 Guess all 5 spooky words from the emoji!', 'Comment your score 👇'], 'Puzzle Videos', 'Guess 20 Words by Emoji (long video)'),
 bt_short(19, 'Oct 19 - 3 Riddles in 30 Seconds 3 🧩 #shorts.mp4', '3 Riddles in 30 Seconds 🧩 The Last One Is the Hardest',
   '3 riddles, 6 seconds each 🧩 How many did you get? Comment your score!',
   'riddles, riddles with answers, brain teasers, riddle challenge, tricky riddles, quiz shorts, logic puzzles', '#riddles #brainteasers #riddlechallenge #quiz',
   ['3 riddles, 6 seconds each 🧩 The last one is the hardest!', 'How many did you solve? 👇'], 'Puzzle Videos', 'Guess 20 Words by Emoji (long video)'),
]
BT_DONE = [('Wed Oct 7, 6:00 pm Short (live): Find the Odd One Out', BT_PIN_SHORT),
           ('Thu Oct 8, 6:00 pm Short (scheduled): 3 Riddles in 30 Seconds', BT_PIN_SHORT)]
BT_DONE_OLD = [('Mon Oct 5, 6:00 pm Short (already scheduled): Guess the Movie by Emoji', ['How many movies did you get? 🎬👇', 'Want the long version? 20 movies, easy to hard, is on the channel now.', '🧠 Play 1,200+ more free puzzles: brainteasersclub.app/btc'])]

# ---------------- Wild Facts ----------------
WF_TAIL = ['', '🐙 Follow for a new wild fact or quiz every day!', '🧠 More free quizzes and brain teasers: ' + WFL]
WF_PIN_Q = ['How many did you get? Comment your score 👇', '🐙 New quiz every day. More free quizzes: brainteasersclub.app/wildfacts']
WF_PIN_F = ['Which fact surprised you most: 1, 2 or 3? 👇', '🐙 A wild fact every day. More free quizzes: brainteasersclub.app/wildfacts']
WF_TAIL_SHORT = ['', '🐙 Follow for a new wild fact or quiz every day!', '🧠 More free quizzes and brain teasers: ' + SITE]
WF_PIN_Q_SHORT = ['How many did you get? Comment your score 👇', '🐙 New quiz every day. More free quizzes: ' + SITE]
WF_PIN_F_SHORT = ['Which fact surprised you most: 1, 2 or 3? 👇', '🐙 A wild fact every day. More free quizzes: ' + SITE]
def wf_short(d, file, title, hook, tags, hashtags, ig, facts=False, related=None, extra=None):
    related = related or ('Animal Quiz: 12 Questions Most Adults Get Wrong (long video)' if d < 11 else 'Ocean Quiz: 12 Questions (long video)')
    return dict(d=d, time='6:00 pm', kind='Short', file=file, title=title + ' #shorts', desc=[hook] + WF_TAIL_SHORT + ['', '#shorts ' + hashtags],
                tags=tags, playlist='Quiz Videos', category='Education', related=related, pin=WF_PIN_F_SHORT if facts else WF_PIN_Q_SHORT,
                ig=ig + ['', '🐙 Follow @wildfactsquiz for a new one every day', '🧠 More free quizzes: link in bio', '', hashtags], ig_time='6:00 pm', extra=extra)
def wf_long(d, file, thumb, title, hook, chapters, tags, hashtags, pin):
    chapters = [chapters] if isinstance(chapters, str) else chapters
    return dict(d=d, time='12:00 pm', kind='Long video (16:9)', file=file, thumb=thumb, title=title, desc=[hook, ''] + chapters + WF_TAIL + ['', hashtags],
                tags=tags, playlist='Quiz Videos', category='Education', pin=pin,
                endscreen='Element 1: Subscribe. Element 2: Video → "Best for viewer". Start at ' + chapters[-1].split()[0] + ', run to the end.')
CH = lambda times: ['0:00 Intro'] + [f'{t} Question {i+1}' for i, t in enumerate(times[:-1])] + [times[-1] + ' Your score']
WF = [
 wf_short(9, 'Oct 9 - Bird Quiz 3 Seconds Each 🦜 #shorts.mp4', 'Bird Quiz: 3 Seconds Each 🦜',
   '5 bird questions, 3 seconds each 🦜 The last one is the hardest. Comment your score!',
   'bird quiz, animal quiz, bird facts, quiz shorts, trivia, general knowledge, hummingbird, owl, albatross', '#birdquiz #animalquiz #quiz #trivia',
   ['Bird quiz 🦜 5 questions, 3 seconds each!', 'The last one is the hardest. Comment your score 👇']),
 wf_short(10, 'Oct 10 - 3 Bug Facts That Sound Fake 🐜 #shorts.mp4', '3 Bug Facts That Sound Fake (But Are True) 🐜',
   'Ants have no lungs, a headless cockroach, and the best hunter in the insect world 🐜 Which one surprised you most?',
   'bug facts, insect facts, animal facts, facts you didn\'t know, did you know, weird facts, ants, cockroach, dragonfly', '#animalfacts #insects #didyouknow #facts',
   ['3 bug facts that sound fake, but are true 🐜', 'Which one surprised you most? 👇'], facts=True),
 wf_long(11, 'Oct 11 - Ocean Quiz 12 Questions (long).mp4', 'Oct 11 - Ocean Quiz 12 Questions - thumbnail.png',
   'Ocean Quiz: 12 Questions About the Sea 🌊 How Many Can You Get?',
   '12 ocean questions 🌊 Read along, answer before the timer ends, and keep score. Comment how many you got!',
   CH(['0:05', '0:20', '0:38', '0:51', '1:07', '1:23', '1:38', '1:52', '2:06', '2:21', '2:36', '2:53', '3:10']),
   'ocean quiz, sea animals quiz, animal quiz, ocean facts, trivia, general knowledge quiz, quiz for kids and adults, marine life', '#oceanquiz #animalquiz #trivia',
   ['How many did you get out of 12? 🌊👇', '🐙 New quiz every day. More free quizzes: brainteasersclub.app/wildfacts']),
 wf_short(12, 'Oct 12 - Food Quiz Question 3 Is Tricky 🍯 #shorts.mp4', 'Food Quiz: Question 3 Is Tricky 🍯',
   '3 food questions, 5 seconds each 🍯 Did question 3 trick you? Comment your score!',
   'food quiz, food facts, quiz shorts, trivia, general knowledge, banana berry, honey, potato', '#foodquiz #foodfacts #quiz #trivia',
   ['Food quiz 🍯 3 questions. Question 3 is tricky!', 'Comment your score 👇'], related='Ocean Quiz: 12 Questions (long video)'),
 wf_short(13, 'Oct 13 - 3 Eye Facts That Sound Fake 👀 #shorts.mp4', '3 Eye Facts That Sound Fake (But Are True) 👀',
   'Your eye breathes air, has a blind spot and sees the world upside down 👀 Which one surprised you most?',
   'eye facts, human body facts, did you know, facts you didn\'t know, weird facts, science facts, cornea, blind spot', '#eyefacts #humanbody #didyouknow #facts',
   ['3 facts about your eyes that sound fake, but are true 👀', 'Which one surprised you most? 👇'], facts=True, related='Ocean Quiz: 12 Questions (long video)'),
 wf_short(20, 'Oct 20 - World Quiz 3 Seconds Each 🌍 #shorts.mp4', 'World Quiz: 3 Seconds Each 🌍',
   '5 geography questions, 3 seconds each 🌍 The last one surprises a lot of people. Comment your score!',
   'geography quiz, world quiz, countries quiz, quiz shorts, trivia, general knowledge, oceans, deserts', '#geography #worldquiz #quiz #trivia',
   ['World quiz 🌍 5 questions, 3 seconds each!', 'The last one surprises a lot of people 👇'], related='Ocean Quiz: 12 Questions (long video)'),
 wf_short(14, 'Oct 14 - 3 More Animal Facts That Sound Fake 🦛 #shorts.mp4', '3 More Animal Facts That Sound Fake (But Are True) 🦛',
   'Koala fingerprints, elephants that can\'t jump and hippo sunscreen 🦛 Which one surprised you most?',
   'animal facts, facts you didn\'t know, did you know, weird animal facts, koala, elephant, hippo', '#animalfacts #didyouknow #facts #animals',
   ['3 more animal facts that sound fake, but are true 🦛', 'Which one surprised you most? 👇'], facts=True, related='Ocean Quiz: 12 Questions (long video)'),
 wf_long(15, 'Oct 15 - Space Quiz 12 Questions (long).mp4', 'Oct 15 - Space Quiz 12 Questions - thumbnail.png',
   'Space Quiz: 12 Questions About Planets and Stars 🪐 How Many Can You Get?',
   '12 space questions 🪐 Read along, answer before the timer ends, and keep score. Comment how many you got!',
   CH(['0:05', '0:20', '0:34', '0:48', '1:02', '1:16', '1:30', '1:45', '1:58', '2:13', '2:27', '2:42', '2:56']),
   'space quiz, planets quiz, solar system quiz, astronomy quiz, trivia, general knowledge quiz, science quiz', '#spacequiz #planets #trivia',
   ['How many did you get out of 12? 🪐👇', '🐙 New quiz every day. More free quizzes: brainteasersclub.app/wildfacts']),
 wf_short(15, 'Oct 15 - Kids vs Parents Round 2 🐼 #shorts.mp4', 'Kids vs Parents: Who Gets 3/3? Round 2 🐼',
   'Kids vs parents, round 2 🐼 3 animal questions. Who got 3/3 in your house? Comment below!',
   'kids vs parents, animal quiz, family quiz, quiz shorts, trivia, panda, cheetah, koala', '#kidsvsparents #animalquiz #familyquiz #quiz',
   ['Kids vs parents, round 2 🐼 Who gets 3/3?', 'Tell us who won 👇'], related='Space Quiz: 12 Questions (long video)'),
 wf_short(16, 'Oct 16 - 3 Cat Facts That Sound Fake 🐱 #shorts.mp4', '3 Cat Facts That Sound Fake (But Are True) 🐱',
   "Cats can't taste sweet, rarely meow at each other and have a hidden third eyelid 🐱 Which one surprised you most?",
   "cat facts, cats, animal facts, did you know, weird facts, facts you didn't know, pets", '#catfacts #cats #animalfacts #didyouknow',
   ['3 cat facts that sound fake, but are true 🐱', 'Which one surprised you most? 👇'], facts=True, related='Space Quiz: 12 Questions (long video)'),
 wf_short(21, 'Oct 21 - Dinosaur Quiz 3 Seconds Each 🦖 #shorts.mp4', 'Dinosaur Quiz: 3 Seconds Each 🦖',
   '5 dinosaur questions, 3 seconds each 🦖 The last one surprises everyone. Comment your score!',
   'dinosaur quiz, dinosaur facts, quiz shorts, trivia, triceratops, stegosaurus, t rex', '#dinosaurs #dinosaurquiz #quiz #trivia',
   ['Dinosaur quiz 🦖 5 questions, 3 seconds each!', 'Comment your score 👇'], related='Space Quiz: 12 Questions (long video)'),
 wf_short(17, 'Oct 17 - 3 Ocean Facts That Sound Fake 🦦 #shorts.mp4', '3 Ocean Facts That Sound Fake (But Are True) 🦦',
   'Glowing sharks, the densest fur on Earth and where your oxygen comes from 🦦 Which one surprised you most?',
   'ocean facts, sea animal facts, did you know, weird facts, sea otter, shark, plankton', '#oceanfacts #didyouknow #facts #animals',
   ['3 ocean facts that sound fake, but are true 🦦', 'Which one surprised you most? 👇'], facts=True, related='Space Quiz: 12 Questions (long video)'),
 wf_short(18, 'Oct 18 - Science Quiz Can You Get 3 of 3 🔬 #shorts.mp4', 'Science Quiz: Can You Get 3/3? 🔬',
   '3 science questions, 5 seconds each 🔬 The last one surprises everyone. Comment your score!',
   'science quiz, science facts, quiz shorts, trivia, general knowledge, mars, atom, light', '#sciencequiz #science #quiz #trivia',
   ['Science quiz 🔬 3 questions. The last one surprises everyone!', 'Comment your score 👇'], related='Space Quiz: 12 Questions (long video)'),
 wf_long(19, 'Oct 19 - Human Body Quiz 12 Questions (long).mp4', 'Oct 19 - Human Body Quiz 12 Questions - thumbnail.png',
   'Human Body Quiz: 12 Questions About You 🫀 How Many Can You Get?',
   '12 questions about the human body 🫀 Read along, answer before the timer ends, and keep score. Comment how many you got!',
   'CHAPTERS_BODY', 'human body quiz, body facts, science quiz, biology quiz, trivia, general knowledge quiz, health quiz', '#humanbody #sciencequiz #trivia',
   ['How many did you get out of 12? 🫀👇', '🐙 New quiz every day. More free quizzes: brainteasersclub.app/wildfacts']),
 wf_short(19, 'Oct 19 - Baby Animal Names Quiz 🐣 #shorts.mp4', 'Baby Animal Names Quiz: 3 Seconds Each 🐣',
   '5 baby animal names, 3 seconds each 🐣 Did you know the last one? Comment your score!',
   'baby animals, baby animal names, animal quiz, quiz shorts, trivia, joey, cygnet, hoglet', '#babyanimals #animalquiz #quiz #trivia',
   ['What do you call these baby animals? 🐣 3 seconds each!', 'Comment your score 👇'], related='Human Body Quiz: 12 Questions (long video)'),
]
# Already uploaded: only a comment (or a title fix) is left.
WF_DONE = [
 ('Wed Oct 7, 12:00 pm long (scheduled): General Knowledge Quiz: 12 Questions', ['How many did you get out of 12? 🧠👇', '🐙 New quiz every day. More free quizzes: brainteasersclub.app/wildfacts']),
 ('Wed Oct 7, 6:00 pm Short (scheduled): What Is a Group of Crows Called?', ['Did you know it? 🐦‍⬛ Comment below 👇', '🐙 A wild fact every day. More free quizzes: brainteasersclub.app/wildfacts']),
 ('Thu Oct 8, 6:00 pm Short (scheduled): 3 Animal Facts That Sound Fake', WF_PIN_F_SHORT),
 ('Sun Oct 11, 6:00 pm Short (scheduled): 3 Space Facts Your Teacher Never Told You', WF_PIN_F_SHORT),
 ('Sat Oct 3 long (posted): Animal Quiz: 12 Questions. Correction to post and pin (question 12: owls also have three eyelids)',
  ['Correction on question 12 🦉 Camels have three eyelids, but so do owls (and many other birds and reptiles). If you picked Owl, give yourself the point!', 'How many did you get out of 12? 👇']),
 ('Posted Shorts with made-up statistics in the title. Optional rename (Studio → Content → title):',
  ['"99% Fail Question 4 🦒 Animal Quiz"  →  "Animal Quiz: Question 4 Is Tricky 🦒 #shorts"', '"Only 1% Get 5/5 on This Animal Quiz 🐾"  →  "Animal Quiz: Can You Get 5/5? 🐾 #shorts"']),
]

BT_PLAYLISTS = [
 ('Playlist 1 (title, then description). Add the videos already up: Guess the Country by Emoji, Guess 20 Movies by Emoji (long), Guess the Movie by Emoji',
  ['Puzzle Videos', 'Guess the movie, food, animal or saying from just emoji. New quiz every day!']),
 ('Playlist 2 (title, then description). Add the videos already up: Can Your Eyes Beat the Clock?, Only 3% Find All 3 (Odd One Out)',
  ['Puzzle Videos', 'Find the odd one out before the timer ends, and quick riddles to test your brain.']),
]
WF_PLAYLISTS = [
 ('Playlist 1 (title, then description). Add: Only 1% Get 5/5, 99% Fail Question 4, Kids vs Parents, Animal Quiz: 12 Questions (long), Biggest Brain, Only Ocean Experts Get 5/5, and when they go live: General Knowledge Quiz (long), Group of Crows',
  ['Quiz Videos', 'Animal, ocean, space and general knowledge quizzes. How many can you get?']),
 ('Playlist 2 (title, then description). Add: 8 Animal Facts That Sound Fake (long), 3 Things Your Body Does, and when they go live: 3 Animal Facts That Sound Fake, 3 Space Facts',
  ['Did You Know? Wild Facts', 'Short, true facts about animals, space and the human body that sound fake.']),
]

# ---------------- document builder ----------------
def build(path, title, intro, glance, videos, done, done_title, ig_note, playlists=None):
    videos = sorted(videos, key=lambda v: (v['d'], 0 if v['time'].startswith('12') else 1))
    body = []
    def run(t, b=False, mono=False, color=None, size=None, i=False):
        rpr = ('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>' if mono else '') + ('<w:b/>' if b else '') + ('<w:i/>' if i else '') + \
              (f'<w:color w:val="{color}"/>' if color else '') + (f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>' if size else '')
        return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
    def p(*runs, style=None, shade=None, after=120, keep=False, indent=None):
        ppr = (f'<w:pStyle w:val="{style}"/>' if style else '') + ('<w:keepNext/>' if keep else '') + \
              (f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else '') + f'<w:spacing w:before="0" w:after="{after}"/>' + \
              (f'<w:ind w:left="{indent}"/>' if indent else '')
        body.append(f'<w:p><w:pPr>{ppr}</w:pPr>{"".join(runs)}</w:p>')
    def h(t, lvl=1): p(run(t), style=f'Heading{lvl}', keep=True)
    def field(name, val): p(run(name + ': ', b=True, color='5B3FB8'), run(val), after=50)
    def label(t): p(run(t, b=True, color='5B3FB8'), after=30, keep=True)
    def copy(lines):
        for k, line in enumerate(lines):
            p(run(line if line else ' ', mono=True, size=19), shade='F1F1F4', after=0 if k < len(lines) - 1 else 140, indent=120)
    def table(rows, widths):
        grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
        out = [f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:tblBorders>' + ''.join(f'<w:{s} w:val="single" w:sz="4" w:color="BFBFC8"/>' for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) + f'</w:tblBorders><w:tblCellMar><w:left w:w="90" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
        for ri, r in enumerate(rows):
            cells = ''.join(f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/>' + ('<w:shd w:val="clear" w:color="auto" w:fill="5B3FB8"/>' if ri == 0 else '') +
                            f'</w:tcPr><w:p><w:pPr><w:spacing w:before="30" w:after="30"/></w:pPr>{run(c, b=ri == 0, color="FFFFFF" if ri == 0 else None, size=18)}</w:p></w:tc>' for ci, c in enumerate(r))
            out.append(f'<w:tr>{cells}</w:tr>')
        out.append('</w:tbl>'); body.append(''.join(out)); p(run(''), after=100)
    pb = lambda: body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    p(run(title, b=True, size=44, color='1B1B3A'), after=60)
    for line in intro: p(run(line, color='555566'), after=60)
    h('Schedule (not uploaded yet)')
    table([['Date', 'Time', 'Type', 'Title']] + [[day(v['d']), v['time'], v['kind'].replace(' (16:9)', ''), v['title'].replace(' #shorts', '')] for v in videos], [1400, 1000, 1000, 6600])
    if playlists:
        h('Playlists (set up once)')
        for t, lines in playlists: label(t); copy(lines)
    if done:
        h(done_title)
        for t, lines in done: label(t); copy(lines)
    for v in videos:
        pb()
        h(f"{day(v['d'])} · {v['time']} · {v['kind']}")
        if v.get('extra'):
            for e in v['extra']: p(run(e, b=True, color='C0392B'), after=60)
        h('YouTube', 2)
        n = iter(range(1, 20)); N = lambda t: f'{next(n)}. {t}'
        field(N('File'), v['file'])
        label(N('Title')); copy([v['title']])
        label(N('Description')); copy(v['desc'])
        if v.get('thumb'): field(N('Thumbnail'), v['thumb'])
        field(N('Playlist'), v['playlist'])
        field(N('Audience'), 'No, it\'s not made for kids  ·  Age restriction: No')
        label(N('Show more → Tags')); copy([v['tags']])
        field(N('Show more → other'), 'Altered content: No  ·  Language: English  ·  Category: ' + v['category'] + '  ·  Comments: On')
        if v.get('related'): field(N('Related video (Shorts)'), v['related'])
        if v.get('endscreen'): field(N('End screen'), v['endscreen'])
        field(N('Visibility'), 'Schedule → ' + day(v['d']) + ', 2026 · ' + v['time'] + ' · Time zone: (GMT-07:00) Vancouver')
        label(N('After it goes live: post this comment and pin it')); copy(v['pin'])
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + ''.join(body) +
           '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1000" w:right="1000" w:bottom="1000" w:left="1000" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="1B1B3A"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="C2552D"/><w:sz w:val="25"/><w:szCs w:val="25"/></w:rPr></w:style></w:styles>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
    rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    drels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'
    try: open(path, 'ab').close()
    except PermissionError: print('LOCKED (close it in Word, then re-run):', path); return
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels); z.writestr('word/document.xml', doc); z.writestr('word/styles.xml', styles); z.writestr('word/_rels/document.xml.rels', drels)
    print('wrote', path, os.path.getsize(path), 'bytes,', len(videos), 'videos')

if __name__ == '__main__':
    import json, sys
    chapters = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chapters.json'), encoding='utf-8'))
    for v in BT + WF:
        if isinstance(v['desc'], list) and any(isinstance(x, str) and x.startswith('CHAPTERS_') for x in v['desc']): pass
    def fill(v):
        out = []
        for x in v['desc']:
            out += chapters[x] if x in chapters else [x]
        v['desc'] = out
        if v.get('endscreen') and 'CHAPTERS_' in v['endscreen']: pass
        return v
    def mp4_secs(path):  # length from the mp4 header (mvhd), or None
        try:
            b = open(path, 'rb').read(); i = b.find(b'mvhd')
            ts, d = struct.unpack('>II', b[i+16:i+24]) if b[i+4] == 0 else struct.unpack('>IQ', b[i+24:i+36])
            return d / ts
        except Exception: return None
    mmss = lambda x: f'{int(x)//60}:{int(x)%60:02d}'
    for lst, folder in ((BT, 'Brain Teasers'), (WF, 'Wild Facts')):
        for v in lst:
            fill(v)
            if v.get('endscreen'):
                sc = [c for c in v['desc'] if c.endswith('Your score')][0].split()[0]
                start = int(sc.split(':')[0]) * 60 + int(sc.split(':')[1])
                secs = mp4_secs(os.path.join(ROOT, folder, v['file']))
                if secs: start = max(start, math.ceil(secs - 20))  # YouTube end screens can only use the last 20 seconds
                v['endscreen'] = 'Element 1: Subscribe. Element 2: Video → "Best for viewer". Start at ' + mmss(start) + ', run to the end.'
    build(os.path.join(ROOT, 'Brain Teasers', 'Posting Plan - Brain Teasers.docx'), 'Brain Teasers — Posting Plan',
          ['Each section below is one upload, in the order YouTube Studio asks for things. Copy each grey box as it is.',
           'When a video is uploaded, it can be removed from this plan (ask Claude, or delete the section).'],
          None, BT, BT_DONE, 'Already scheduled: only the pinned comment is left', '')
    build(os.path.join(ROOT, 'Wild Facts', 'Posting Plan - Wild Facts.docx'), 'Wild Facts — Posting Plan',
          ['Each section below is one upload, in the order YouTube Studio asks for things. Copy each grey box as it is.',
           'When a video is uploaded, it can be removed from this plan (ask Claude, or delete the section).'],
          None, WF, WF_DONE, 'Already uploaded: comments to post and pin, and fixes', '')
