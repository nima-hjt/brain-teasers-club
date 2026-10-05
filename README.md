# Brain Teasers Club

Quick brain-teaser quiz game: odd one out, emoji riddles, logic, animal facts. Daily challenge,
duel on one phone, live two-phone matches, streaks and XP. Live at https://brainteasersclub.app

## How it is put together

- `src/index.html` – the whole game (HTML, CSS, JS) with a `/*__BANK__*/` marker where the puzzles go.
- `content/*.json` – the puzzle banks. Add puzzles here, never inside index.html.
- `build.py` – merges content into the page, writes `dist/` (the deployable site: game, about, privacy,
  facts page, manifest, service worker, icons, sitemap).
- `assets/` – pre-rendered icons and the social preview image.
- `soundboard.html` – the sound audition page used to choose the effects.

## Build

    python3 build.py

Output is in `dist/`. Cloudflare Pages runs this command on every push and publishes `dist/`.

## Live Match

Two-phone matches use a Firebase Realtime Database (free plan) over REST + server-sent events.
The database address is in `src/index.html` (`DB_URL`). Rules live in the Firebase console.

## Ads

The results-screen ad slot is off until `ADSENSE_CLIENT` and `ADSENSE_SLOT` in `src/index.html` are set.
