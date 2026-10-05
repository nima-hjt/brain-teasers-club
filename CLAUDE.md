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
- Finished videos go in `Downloads\brain-teasers-club-repo\Brain Teasers\` (named by posting date).
- ALWAYS update `Brain Teasers\Posting Plan - Brain Teasers.docx` after making videos: add each video's file name, scheduled
  date/time, YouTube title, description (with chapters for long videos), tags, pinned comment, Instagram caption and
  Facebook text; text only, no images. Generator: `tools/video/make_plan.py` (edit VIDEOS, re-run).
- Making videos: `python tools/video/serve.py` (port 8768, PUT /out/<file>), narration with
  `tools/video/say_cfg.py <name> af_heart` (Kokoro, offline; model files in `.new/tts/`, not in git), then open
  `short.html?s=<name>` (configs in `shorts.json`, kinds emoji | riddle | odd) or `long.html` in the browser and run
  `exportMp4()`. Export is frame-exact (WebCodecs + mp4-muxer); never record in real time (it drifts out of sync).
- Before export: no invented statistics in titles or narration, puzzles not in the next two weeks' Dailies, no clue
  with two valid answers; check a frame sheet (`sheet()`) and the audio sync.
