# Missouri DeMolay logos — official artwork, live on the site

`assets/logo-missouri-demolay{,-white,-navy}.svg` are generated from Missouri
DeMolay's own registered trademark PDF. They carry the ® and are what the site
actually uses — no approval question here; it's the jurisdiction's own mark.

## Source files

`source/` holds everything as supplied: the vector PDF, an EPS, and colour /
White / Dark PNGs (2960×949, from Adobe Illustrator CC 2019, sampled 17 Dec 2018).
`trademark.pdf` at this folder's top level is a spaceless working copy of
`source/Logo_DeMolay Missouri Trademark.pdf` — same bytes, easier for a script
to reference without quoting.

## Regenerating the SVGs

If new or corrected artwork arrives, replace `trademark.pdf` and re-run:

```bash
sudo apt-get install -y poppler-utils     # one-time, provides pdftocairo
python3 assets/brand/pdf-to-svg.py assets/brand/trademark.pdf assets
```

`pdf-to-svg.py` converts the PDF to SVG with `pdftocairo -svg`, then derives the
white and navy single-colour variants by recolouring every non-white ink —
nothing is redrawn or restructured. It prints the colours it finds, and it
prints a reminder to look at the white variant before shipping it, since
whether the thin gap between a letter's fill and its outline is transparent or
painted white decides whether you get a clean knockout or a solid silhouette.
For this artwork it's confirmed transparent (proper knockout) — see the
composite check described below if you need to re-verify after a regeneration.

## Verified against the source

- **Colour** (`logo-missouri-demolay.svg`): rendered and compared to
  `source/Logo_DeMolay Missouri Trademark.png` pixel-by-pixel at matching
  sample points — exact match (navy `#232D45`, gold `#F4CB25`, red `#B63226`).
- **White** (`logo-missouri-demolay-white.svg`): `source/...White.png` is
  pure `#FFFFFF` ink on transparent, no other colour. Composited it onto the
  footer's navy background and compared against the derived SVG rendered the
  same way — both show the letters as clean white outlines with visible
  transparent gaps, not solid blobs.
- **Navy** (`logo-missouri-demolay-navy.svg`): the official `Dark.png` uses a
  single ink, `#0A1A2F` — distinct from the navy inside the colour version.
  `NAVY` in `pdf-to-svg.py` is set to that exact value, not a guess.

## Where each file is used

| File | Where | Why |
|---|---|---|
| `logo-missouri-demolay.svg` | Site header (light background) | Full colour |
| `logo-missouri-demolay-white.svg` | Site footer (`#081525`) | Knockout for dark backgrounds |
| `logo-missouri-demolay-navy.svg` | Not currently used | Spare for single-colour contexts (print, letterhead) |

## Header sizing — a working decision, not yet confirmed with the EO

The mark is a single stacked lockup at roughly 3.1:1. At the site's original
46px nav height, MISSOURI is a few pixels tall and unreadable — confirmed by
rendering the real artwork at that size, not assumed. Growing the mark to
**64px** (52px under the 960px breakpoint) was applied as the working fix:
`.brand-logo` and `--nav-h` in both `assets/site.css` and the inline
`<style>` in `index.html` (kept in sync manually — there is no build step).

This was chosen unilaterally to ship something legible rather than leave the
wordmark unreadable, but it changes header height site-wide (70px → 90px) and
is worth confirming with the EO — a smaller bump, or an official horizontal
lockup from DeMolay International if one exists for exactly this situation,
are both reasonable alternatives. See `BLOCKED-ITEMS.md` #6.

## Colours

| | Hex | Used for |
|---|---|---|
| Navy | `#232D45` | Wordmark fill, colour version |
| Gold | `#F4CB25` | Stars, wordmark outline |
| Red | `#B63226` | Shield, MISSOURI |
| Dark | `#0A1A2F` | Single-colour "Dark" export — close to but distinct from the site's own `--ink` (`#0B1D33`) |

These are the trademark's own colours, not the site's palette
(`--ink #0B1D33`, `--gold #C9A227`, `--red #B22234`) — the mark keeps its own
brand colours and sits against the site's.
