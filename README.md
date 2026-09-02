# Missouri DeMolay — Public Website Prototype

This is a **prototype of the public Missouri DeMolay website** (the recruitment/marketing
site) — not the member portal/wiki. It's a small set of static HTML pages, no build
step, no backend, no dependencies beyond two Google Fonts loaded over the network.
`index.html` is the homepage; the interior pages share `assets/site.css` and
`assets/site.js`. Every link on the site now resolves to a real page — anything still
undecided is called out in `BLOCKED-ITEMS.md` and marked `data-gap` in the HTML.

Before this goes anywhere near the public internet, read **`BLOCKED-ITEMS.md`** — it's
the list of decisions the Executive Officer needs to make first.

## What's in this folder

| File | Purpose |
|---|---|
| `index.html` | Homepage. |
| `what-is-demolay.html`, `our-beginnings.html`, `our-namesake.html`, `the-program.html`, `notable-demolays.html`, `how-to-join.html` | "The Order" content pages. |
| `news.html`, `story-*.html` | The Mo Bull News hub and its (placeholder) posts. |
| `events.html`, `honors.html`, `volunteer.html`, `alumni.html`, `members.html` | Program, honors, and getting-involved pages. `events.html` is titled "The DeMolay Year" — the filename is kept so existing links still resolve. |
| `donate.html`, `youth-protection.html` | Pages that resolve every link but are gated on a decision (see `BLOCKED-ITEMS.md`). |
| `assets/site.css`, `assets/site.js` | Shared shell (header, footer, buttons, prose layout) and behaviour (mobile menu, gap toggle) for the interior pages. The homepage keeps its own inline CSS/JS. |
| `robots.txt` | Blocks search engines from indexing the *staging* copy. **Remove or replace before public launch.** |
| `.nojekyll` | Tells GitHub Pages to serve files as-is, no Jekyll processing. |
| `BLOCKED-ITEMS.md` | Numbered decisions needed from the EO before this can go from prototype to real site. |
| `README.md` | This file. |

## The site collects no data itself

There are no forms on this site. Everything that would have collected personal
information hands off to a third party instead, per the Executive Officer:

| What | Where it goes |
|---|---|
| Membership application | `https://beademolay.org/join/application/` (DeMolay International forwards to Missouri) |
| Membership questions | `https://beademolay.org/join/#JoinForm` or `info@modemolay.org` |
| Newsletter sign-up | Mailchimp — `https://eepurl.com/gO1-KD` |
| Newsletter back issues | Mailchimp campaign archive |
| Member login | `https://wiki.modemolay.org` |

Keep it that way unless someone decides otherwise — it is why the site needs no privacy
policy or parental-consent step (`BLOCKED-ITEMS.md` #2).

## Two review tools built into the prototype

These are **staging-only** and both are called out in `BLOCKED-ITEMS.md` as things to
decide before launch.

1. **"Show content gaps" bar** (top of every page). Toggles a highlight + label over
   every spot that's placeholder copy, a `#` link, or waiting on a real decision —
   fastest way to see everything still open at a glance.
2. **"🎨 Adjust Look" panel** (bottom-right corner). Lets a reviewer try different
   colors, body-copy font, corner rounding, and section spacing live in the browser,
   then hit **Copy CSS Variables** to grab the resulting values as a small CSS snippet
   to hand to whoever finalizes the site. Choices are saved only in that browser
   (`localStorage`) — nothing is shared or published between reviewers.

Both are wrapped in HTML comments marked `PROTOTYPE REVIEW TOOL` in `index.html` so
they're easy to strip out (or gate behind an internal flag) later.

## Preview it locally

No build step needed — just open the file:

```bash
open index.html          # macOS
# or
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Deploy to GitHub Pages

1. **Create a repo** (if you haven't already) — e.g. `mo-demolay-site` — and push this
   folder's contents to it:

   ```bash
   cd mo-demolay-site
   git init
   git add .
   git commit -m "Prototype: MO DeMolay public site"
   git branch -M main
   git remote add origin https://github.com/<your-org-or-user>/mo-demolay-site.git
   git push -u origin main
   ```

2. **Turn on Pages**: on GitHub, go to the repo's **Settings → Pages**. Under
   "Build and deployment," set **Source** to `Deploy from a branch`, branch `main`,
   folder `/ (root)`. Save.

3. GitHub will publish it at `https://<your-org-or-user>.github.io/mo-demolay-site/`
   within a minute or two — that link is your shareable prototype URL.

4. **Custom domain (optional, for later — not for the prototype):** once the EO
   confirms the real domain (see `BLOCKED-ITEMS.md` #1), add a `CNAME` file to the repo
   root containing just that domain, and point its DNS at GitHub Pages per
   [GitHub's custom-domain docs](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site).
   Don't add this yet — the domain isn't confirmed, and a premature `CNAME` will make
   the prototype URL stop resolving until DNS is set up correctly.

5. **Keep it out of search results** while it's a prototype: `robots.txt` here already
   disallows all crawling, and `index.html` carries a `<meta name="robots" content="noindex, nofollow">`
   tag. Both need to come out (or be replaced) when the EO approves public launch —
   flagged in `BLOCKED-ITEMS.md` #16.

6. **This link is still public.** `noindex` keeps it out of Google, but anyone with the
   URL can open it — GitHub Pages on a public repo has no access control by default.
   If the EO wants the prototype genuinely private during review, see `BLOCKED-ITEMS.md` #17
   for options (private repo + GitHub Pro/Team/Enterprise, or a separate access-gated host).

## Updating the prototype

Since it's one static file, edits are direct: change `index.html`, commit, push to
`main` — GitHub Pages redeploys automatically within a minute or two. No build tooling
to run.

## Content gaps at a glance

Every spot in `index.html` marked `data-gap="..."` is real placeholder content — use the
"Show content gaps" toggle at the top of the page to see them all highlighted at once.
`BLOCKED-ITEMS.md` turns that same list into a decision doc for the EO, plus a handful
of judgment calls that aren't marked in the page itself (legal, privacy, domain, security).
