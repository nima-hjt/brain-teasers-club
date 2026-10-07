# Brain Teasers Club — notes for Claude sessions

Owner: Nima. Live at https://brainteasersclub.app (Cloudflare Pages project `brainteasersclub-git`,
auto-deploys every push to `main`: build command `python3 build.py`, output `dist`).
Companion to the YouTube channels Brain Teasers Club (@BrainTeasersClub) and Wild Facts (@wildfactsdaily-q3z).

## Layout
- `src/index.html` — the entire game (HTML/CSS/JS, no framework). Puzzle banks are injected at `/*__BANK__*/`.
- `content/*.json` — puzzle banks. odd: {common, odd}; emoji/logic: {q, a, wrong[3], why, cat}; animals: same + cat.
- `build.py` — validates content (4 distinct options, no duplicate questions, strings only), writes `dist/`
  (game, about, facts, privacy, 404, manifest, sw.js, sitemap, icons from `assets/`). Bump the cache name in sw.js
  (`btc-vN`) when shipping changes players must pick up immediately.
- Tracking links: `build.py` also writes `dist/btc.html`, `wildfacts.html` (YouTube), `fb.html` and `ig.html` (copies of
  the game) so each source shows as its own path in Web Analytics. Shares use `shareBase()`,
  which strips those paths, the query and the hash.
- Levels: every puzzle has `lvl` 1-3 (quick / needs a moment / tricky). `LEVEL_MIX` in src/index.html sets puzzles
  per level for a 10-puzzle round (easy 7/3/0, normal 3/5/2, hard 1/5/4, impossible 0/3/7) and rounds run easy → hard.
  The Daily ignores levels.
- New puzzles: append them (never delete or reorder; fix in place instead) and give each `"added": "YYYY-MM-DD"` at
  least two days ahead. The Daily skips puzzles added after its date, so shipping never changes a Daily in progress.
- No-repeat order: unseeded rounds (Play Solo) deal from shuffled decks per type and level in localStorage
  (`btc-deck2-<type><lvl>`, `deckPick`); new puzzles are shuffled into the remaining deck. Adding puzzles changes the
  Live Match bank version (both players need the same build) and the puzzles behind old Challenge codes.
- Languages (English, Persian, Spanish): UI text is in `src/i18n.js` (`STR`, `t("key",{vars})`, injected at
  `/*__I18N__*/`); static HTML uses `data-t` / `data-tp`. Puzzle translations are `content/i18n/<lang>.json`
  ({logic|facts: {bank index: [q, a, [3 wrong in English order], why]}}), served as `dist/i18n/<lang>.json` and fetched
  on demand. Options keep their English text as identity (`loc(q).opt`), so answers, Live Match and Challenge codes work
  across languages; untranslated puzzles fall back to English. Emoji Riddles are English-only; other languages get
  their own Daily (4 odd, 3 logic, 3 facts). Persian is RTL with Vazirmatn and Persian digits (`num()`).
  When adding logic/facts puzzles, translate them too (or they stay English-only for those players).
- World Quiz (home → World Quiz → Flags / Capitals): `content/world.json`, 193 UN members + Vatican City
  ({c: ISO code, cont, lvl, n:{en,fa,es}, cap:{en,fa,es} or absent}). No capital question where the capital is disputed,
  split, or shares the country's name. Injected as `WORLD`; types `flags` / `capitals` use the normal round engine
  (levels, no-repeat keys `F<i>` / `C<i>`), options are country codes from the same continent, never two look-alike flags
  (`LOOKALIKE`). Flags are SVGs from the flag-icons CDN on jsDelivr. Not in the Daily or Challenge links.
  Currencies: `content/currency.json` (190 countries, short names like "Franc", `also` = other names legal there so they
  are never wrong options; sources in content/currency_sources.md; Zimbabwe, Sierra Leone, Afghanistan, Bolivia left
  out). Options never repeat a text in any language. Hangman (`startHangman`): 5 country/capital names per round in the
  player's language, 6 misses, untimed; accents ignored, ñ and Persian letters have keys.
  Country Clues (`startClues`): 5 countries, clues opened weakest first (currency, capital's first letter, capital,
  flag; never anything about the name, since the 6 options are on screen), options from the same continent; a wrong
  pick opens the next clue. In Play with Friends → World Quiz, Hangman and Country Clues are chips that exclude the
  quiz types (`worldTypes`); they run in Pass & Play (`hpass`/`cpass`) and Live Match (`makeRound`, word lists packed
  as {t,i}); Duel is disabled for them. Live word games show each player's own language. The home logo is the app icon.
  Play with Friends has a Classic puzzles / World Quiz switch (`fset`, `friendTypes()`); Live Match packs World Quiz
  options as they are (`w`). Data audited Oct 2026 (Egypt: Cairo kept, constitutional capital; Equatorial Guinea and
  Indonesia excluded while their capitals move).
- Design system: tokens at the top of the stylesheet. Light = "Paper & Ink" (paper #f7f3ea, ink #16120d outlines, tile
  colours yellow/pink/blue/green, Fraunces + Inter); dark mode = "Calm Night" (#0f1720, mint #3ee0b5, Space Grotesk).
  Components use only the tokens; icons are inline line SVGs, no emoji as icons. Theme follows the phone; the button switches to the other
  theme (saved as `btc-theme`, cleared when it matches the phone again), applied by a script in <head> before paint.
- `tools/video/` — YouTube/Instagram video maker (see "Videos" below).
- `soundboard.html` — sound audition page; the chosen set is in `SFX` in src/index.html.
- `tools/mockdb.js` — offline emulator of Firebase RTDB REST + SSE for testing Live Match with two headless browsers.

## Rules the owner cares about
- Accuracy: never invent statistics or facts. Animal facts must be verifiable (Guinness, Nat Geo, Smithsonian, NOAA…).
  Puzzles must not be solvable in the first second; no trivial items.
- Daily Challenge: same puzzles for everyone, always Normal difficulty, one attempt per day (quit/reload counts).
- Keep the home screen simple: Daily hero card, Play Solo, Play with Friends.
- Sounds (owner's picks): tap=blip, countdown=heartbeat, correct=coin (pitch rises with streak), streak=harp gliss,
  wrong=down blips, timeout=slide down, win=8-bit victory, lose=sad trombone, start jingle=none, difficulty=step note.
- Spend nothing beyond the domain unless asked.

## Live Match
Firebase Realtime Database `https://brainteasersclub-f12c1-default-rtdb.firebaseio.com` (Spark/free plan), used over
plain REST + EventSource (no SDK). Rooms live at `rooms/CODE` (4 chars). The host writes the exact packed puzzle list
(`settings.round`) and a bank version (`settings.ver`); guests play that list, never re-derive it. Patch events from
Firebase use multi-path keys like `"host/rematch": null` — apply them per key, null deletes.
Database rules (set in the Firebase console) only allow writes under rooms/{4-char code}.
Each player writes `seen` (their seen-puzzle keys, oldest first) on Ready and on Rematch; when both are ready the
host picks the round with `buildRound(..., mergedSeen(them.seen))`, so it avoids both players' histories.
To test with two separate histories, load the host from 127.0.0.1 and the guest from localhost (separate storage).

## Play statistics
Each visit to the live site writes one anonymous record to Firebase `stats/days/<YYYY-MM-DD>/<pushId>`
({u: random device id, n: new device, s: source, l: language, d: m|d, t, a: active seconds, r: rounds, f: finished, m: modes});
see `statStart` in src/index.html. Off on localhost/test pages and on devices opened once with `?notrack`.
`/stats` (src/stats.html, noindex, unlinked) reads and totals them. Firebase rule: `stats` readable, `$day/$id` writable.

## Not done yet
- AdSense: set `ADSENSE_CLIENT` / `ADSENSE_SLOT` in src/index.html after approval; add the verification snippet.
- Cloudflare Web Analytics: enable in the Pages project (Metrics → Web Analytics); Cloudflare injects the beacon
  automatically, so there is no token in the code. The privacy page already describes it.
- Tablet/laptop layout is a centred phone column (acceptable for now).

## Testing before pushing
Build, then load `dist/index.html` in Playwright at 390px wide: play a round in each mode, check no console errors and
no horizontal scroll. For Live Match, run tools/mockdb.js and drive two browser contexts through create → join →
ready → play → results → rematch → disconnect.

## Videos (YouTube channels Brain Teasers + Wild Facts, Instagram, Facebook)
- Owner's schedule: one Short daily at 6 pm, one long 16:9 video (~3 min) every 4 days at 12 pm. Not made for kids, no age
  restriction. Tracking links: /btc (Brain Teasers YouTube), /wildfacts, /fb, /ig (Instagram bio only).
- Finished videos go in `Downloads\brain-teasers-club-repo\Brain Teasers\` or `...\Wild Facts\` (named "Oct N - ..."). Never mix
  the two channels.
- ALWAYS update the posting plans after making videos: `Brain Teasers\Posting Plan - Brain Teasers.docx` and
  `Wild Facts\Posting Plan - Wild Facts.docx`, both from `tools/video/make_plans.py` (BT / WF lists; long-video chapter
  times in chapters.json). One self-contained section per upload in YouTube Studio order (file, title, description,
  thumbnail, playlist, audience, tags, category, related video or end screen, schedule, pinned comment, Instagram and
  Facebook text). Text only. Remove a video's entry once it is uploaded.
- Wild Facts videos: `wf.html?f=wf.json&s=<name>` (Shorts: kind quiz | facts, octopus mascot) and
  `wf.html?f=wf_long.json&s=<name>` (12-question 16:9 quiz); narration `say_wf.py <file.json> <name>` (voice af_bella).
  Every fact is checked against reliable sources before export (a sailfish myth once had to be pulled).
- Brain Teasers "Guess 20 X by Emoji" long videos: `gen_long.py <key>` writes `<key>.html` + narration from animals.html.
- Making videos: `python tools/video/serve.py` (port 8768, PUT /out/<file>), narration with
  `tools/video/say_cfg.py <name> af_heart` (Kokoro, offline; model files in `.new/tts/`, not in git), then open
  `short.html?s=<name>` (configs in `shorts.json`, kinds emoji | riddle | odd) or `long.html` in the browser and run
  `exportMp4()`. Export is frame-exact (WebCodecs + mp4-muxer); never record in real time (it drifts out of sync).
- Instagram/Facebook: Reels go in `Downloads\brain-teasers-club-repo\Instagram-Facebook\` with the plan from
  `tools/video/make_social.py` (caption for Instagram, which auto-shares to Facebook, plus a Facebook comment with the /fb
  link). Reel versions skip the intro: add `&reel=1` to the short.html / wf.html URL before `exportMp4()`.
- Hook: YouTube Shorts and Reels start on the first puzzle (no title card). Analytics showed ~70% swiping away during
  the old 2–3 s intros. Brain Teasers: short.html `&reel=1&yt=1` for YouTube, `&reel=1` for Instagram ("link in bio");
  Wild Facts: wf.html `&reel=1` for both.
- No repeats: check every new video against `tools/video/posted.md` (posted + planned content for both channels, which
  also covers Instagram/Facebook Reels) and add the new video there.
- Before export: no invented statistics in titles or narration, puzzles not in the next two weeks' Dailies, no clue
  with two valid answers; check a frame sheet (`sheet()`) and the audio sync.
