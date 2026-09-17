# Missouri DeMolay — Public Website Prototype

This is a **prototype of the public Missouri DeMolay website** (the recruitment/marketing
site) — not the member portal/wiki. It's a small set of static HTML pages, no build
step, no backend, no dependencies beyond two Google Fonts loaded over the network.
`index.html` is the homepage; the interior pages share `assets/site.css` and
`assets/site.js`. Every link on the site now resolves to a real page — anything still
undecided is called out in `BLOCKED-ITEMS.md` and marked `data-gap` in the HTML.

The look and feel (palette, type, spacing) is now **locked in** per the Executive
Officer, and the site carries complete SEO metadata (`sitemap.xml`, `site.webmanifest`,
Open Graph/Twitter Card tags with a real share image on every page). It is **still kept
out of search engines and still staging-only** — see step 5 under "Deploy to GitHub
Pages" below.

Before this goes anywhere near the public internet, read **`BLOCKED-ITEMS.md`** (the
decisions the Executive Officer needs to make) and **`LAUNCH-CHECKLIST.md`** (the
engineering punch-list — what's done, what's gated on those decisions, and what's gated
on DNS/launch timing). Both are untracked, local-only files — see `.gitignore`.

## What's in this folder

| File | Purpose |
|---|---|
| `index.html` | Homepage. |
| `what-is-demolay.html`, `our-beginnings.html`, `our-namesake.html`, `the-program.html`, `notable-demolays.html`, `how-to-join.html` | "The Order" content pages. |
| `news.html`, `story-*.html` | The MoBull News hub and its (placeholder) posts — see `BLOCKED-ITEMS.md` #11. |
| `events.html`, `honors.html`, `volunteer.html`, `alumni.html`, `members.html` | Program, honors, and getting-involved pages. `events.html` is titled "The DeMolay Year" — the filename is kept so existing links still resolve. |
| `donate.html`, `youth-protection.html` | Pages that resolve every link but are gated on a decision (see `BLOCKED-ITEMS.md`). |
| `assets/site.css`, `assets/site.js` | Shared shell (header, footer, buttons, prose layout) and behaviour (mobile menu, sticky-nav shadow) for the interior pages. The homepage keeps its own inline CSS/JS. |
| `assets/photos/` | Small, optimized action photos actually used on the site (referenced from `index.html`). |
| `assets/DI_images/` | **Full-resolution source photography, not referenced by any page.** ~390MB of raw camera exports the optimized photos above were drawn from. Flagged in `LAUNCH-CHECKLIST.md` as a repo-size question worth a decision — it doesn't need to ship inside this repo to appear on the live site. |
| `assets/brand/` | Missouri DeMolay's official trademark source files (PDF/EPS/PNG) and the script used to derive the SVG logos at the root of `assets/`. Not linked from any page directly. |
| `assets/og-image.jpg` | Social-share preview image (1200×630) used by every page's Open Graph/Twitter Card tags. |
| `sitemap.xml` | Lists all public pages for search engines. Only takes effect once `robots.txt`/`noindex` come off — see below. |
| `site.webmanifest` | Basic web app manifest (name, theme color, icons) linked from every page. |
| `robots.txt` | Blocks search engines from indexing the *staging* copy. **Remove or replace before public launch.** |
| `.nojekyll` | Tells GitHub Pages to serve files as-is, no Jekyll processing. |
| `BLOCKED-ITEMS.md` | Numbered decisions needed from the EO before this can go from prototype to real site. Untracked — see `.gitignore`. |
| `LAUNCH-CHECKLIST.md` | Engineering punch-list: what's done, what's still gated on an EO decision, what's gated on DNS/launch timing. Untracked — see `.gitignore`. |
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

## Two review tools that used to be built into the prototype

Earlier drafts shipped two staging-only reviewer tools — a "Show content gaps" bar on
every page (highlighted every `data-gap` spot) and a bottom-right "🎨 Adjust Look" panel
for trying palette/type/spacing options live. Both are now **removed**: the EO confirmed
the look and feel is locked in, so there was nothing left for them to review (see
`BLOCKED-ITEMS.md` #17). If you're reading old commit history and see `PROTOTYPE REVIEW
TOOL` comments or a `modemolay-theme-prefs` localStorage key, that's what they were.

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
   URL can open it — GitHub Pages on a public repo has no access control by default. Per
   `BLOCKED-ITEMS.md` #16, the EO has already decided this is acceptable during review
   and no access gate is needed — noted here only so it isn't mistaken for an oversight.

## Updating the prototype

Since it's one static file, edits are direct: change `index.html`, commit, push to
`main` — GitHub Pages redeploys automatically within a minute or two. No build tooling
to run.

## Content gaps at a glance

Every spot marked `data-gap="..."` in the HTML is real placeholder content. There's no
visual toggle for these anymore (removed along with the other review tools — see above);
search the source for `data-gap="` to find them, or just read `BLOCKED-ITEMS.md`, which
turns that same list into a decision doc for the EO, plus a handful of judgment calls
that aren't marked in the page itself (legal, privacy, domain, security).
