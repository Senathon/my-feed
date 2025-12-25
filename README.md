# RSS feed starter (free)

This folder contains:
- `feed.xml` — a ready-to-host static RSS feed (edit by hand)
- `items.json` + `make_rss.py` — an optional simple generator that outputs `feed.xml`

## Fastest path to a public RSS link (GitHub Pages, free)

1) Create a GitHub account (free) if you don't have one.
2) Create a new PUBLIC repo (example: `my-feed`).
3) Upload `feed.xml` to the repo root (or run the generator first).
4) In the repo: **Settings → Pages**
   - Source: *Deploy from a branch*
   - Branch: `main` (or `master`) and folder `/ (root)`
   - Save

GitHub will give you a URL like:
  `https://USERNAME.github.io/REPO/feed.xml`

Paste that URL into any RSS reader.

## If you want a feed generated from websites / keywords

You need a rule for where items come from (sites, pages, search terms).
Share:
- the exact sites/pages you want tracked
- how often you want updates
- what counts as an "item" (new post, press release, tweet, etc.)

Then you can host a generator (still free) via GitHub Actions, Cloudflare Workers, etc.
