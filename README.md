# HI Comfort demo

Demo concept website for HI Comfort (renovations, Varna). Not the official company site.

- `site/` is what Netlify publishes (set in `netlify.toml`). It is generated, so do not edit it by hand.
- `src/build.py` holds all texts in Bulgarian and English and builds the pages: `python3 src/build.py`.
- `src/site.css` and `src/site.js` are the shared styles and behaviour.

Bulgarian pages sit at the root, English pages under `/en/`.

Preview links: Netlify builds a preview for each pull request.
