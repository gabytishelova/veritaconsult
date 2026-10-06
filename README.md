# Verita site (`/demo/agency2`)

Static build. Two brand elements are maintained here by hand.

## Animated header mark

Lives inline in the logo component inside `assets/index-DJU1rbE0.js` (search for
`verita-hdr-vGold`). It is a pure SVG + CSS shine — no JS, transform only.
Gradient/clip ids are prefixed `verita-hdr-` to avoid collisions with other inline SVGs.

The keyframes live at the bottom of `assets/index-Bie2yWpX.css`:

```css
@keyframes verita-shine{
  0%,62%   {transform:translateX(-1.35px) rotate(18deg)}
  82%,100% {transform:translateX(1.35px)  rotate(18deg)}
}
.verita-shine{animation:verita-shine 5s ease-in-out infinite}
```

- Shine interval: change the `5s` duration.
- Sweep speed: move the `62%` / `82%` stops (closer together = faster rake).
- Reduced motion disables the band.
- Never render the mark below 28px tall; scale via `width`/`height` only. Do not edit the
  path data, stroke width, `stroke-dasharray`, or the arc gap.
- Light-background header: swap the gradient stops to `#a8843c` → `#6f5220`.

## Intro sting

Markup, styles and the vanilla controller are in `index.html`. Sources:

- `assets/verita-sting.mp4` (H.264, listed first for Safari/iOS)
- `assets/verita-sting.webm` (VP9)
- `assets/verita-sting-poster.png` (final frame; poster + held end state)

To swap the clip, replace those three files in place (same names) — nothing is bundled
or optimised. The current master is `verita-sting-1920x1080-3.webm`.

Behaviour (current):
- The site root opens on a full-screen intro (`#verita-sting` in `index.html`).
- The clip autoplays muted/inline on every refresh.
- The clip is 4 seconds (the original 7s master, first 6s sped up 1.5x). When playback ends the intro fades out
  by itself over 700 ms. There is no ENTER button. **Skip** (top right) and `Esc` still close it at any time.
  If the video errors, autoplay is blocked or it is not ready within 2.5s, the intro closes instead of waiting.
  A 7s safety timer closes it regardless.
- `Esc` and the bottom-right **Skip** button both dismiss the intro immediately.
- Fallbacks: if autoplay is blocked, the video errors, or `canplay`/`canplaythrough`
  has not fired within 2.5 s, the CTAs appear anyway so the visitor is never trapped.
- Skipped entirely under `prefers-reduced-motion: reduce`.

## Encoding notes

Current assets were produced from the uploaded master `verita-sting-1920x1080-3.webm`
(VP9, 1920×1080, ~59.94 fps) with these commands:

```bash
# MP4 fallback (H.264, High L4.2, yuv420p, CFR 59.94)
ffmpeg -i master.webm -c:v libx264 -pix_fmt yuv420p -profile:v high -level 4.2 \
  -crf 18 -preset slow -r 60000/1001 -movflags +faststart -an verita-sting.mp4

# WebM (VP9, CFR 59.94)
ffmpeg -i master.webm -c:v libvpx-vp9 -pix_fmt yuv420p -crf 24 \
  -b:v 8M -minrate 4M -maxrate 12M -r 60000/1001 -an verita-sting.webm

# Poster (final frame)
ffmpeg -sseof -0.5 -i verita-sting.mp4 -q:v 2 -frames:v 1 verita-sting-poster.png
```

Result: MP4 ~1.3 MB, WebM ~960 KB, poster ~280 KB. The mostly-black content compresses
very efficiently while retaining the 60 fps motion.

## Recent changes (this round)

**Card hover treatment.** All three card sections — What We Do, Why Verita, Who We
Work With — now share the same hover language: lift (`translateY(-4px)`), a gold
border glow (`box-shadow: 0 0 0 1px rgba(200,164,74,0.4), 0 12px 24px rgba(0,0,0,0.35)`),
and a subtle background tint (`var(--muted)`). Why Verita didn't have a bordered
container before this — one was added so it could carry the same treatment.
Guarded behind `window.matchMedia('(hover: hover)')` so touch devices never get a
"stuck" glow after tapping (mobile fires `mouseenter` without a matching
`mouseleave`) — desktop-only effect by design, not an oversight.

**Forms.** Both the contact form and the newsletter signup now post to Formspree
(`formspree.io/f/mvkoozrz` and `formspree.io/f/mnpqqjvz`) with proper loading/error
states. Previously the contact form didn't send anywhere at all, and the newsletter
form pointed at a backend route (`/api/public/verita-subscribe`) that only existed
on the old Lovable-hosted version.

**Copy/consistency fixes.** All em-dashes replaced with standard hyphens site-wide.
"CYPRUS" is now uppercase everywhere it appears (hero geo tabs, the geographic-focus
card, and the footer) — previously only the hero copy forced uppercase via CSS,
so the other two spots showed mixed-case "Cyprus". Numbered badges (01/02/03...)
removed from What We Do and Who We Work With cards; step circles in How We Work
are now unlabeled.

**New elements.** A "Book a Call" banner linking to Calendly sits above the contact
form. A visible gold `:focus-visible` outline (using the existing but previously
unused `--ring` token) now shows on keyboard focus for all links, buttons, and
form fields — there was no custom focus state before, only inconsistent browser
defaults.

**Mobile fixes.**
- Hero no longer leaves a dead-space gap under the nav on short viewports — was
  caused by `min-height: 100vh` + `justify-content: flex-end` + 140px top padding,
  a combination that assumes a tall desktop viewport. Fixed via a `max-width: 640px`
  override (`.hero-section` / `.hero-content` classes).
- The 6-step "How We Work" timeline now stacks vertically below 640px instead of
  relying on unlabeled horizontal scroll — steps 4-6 were previously invisible
  unless a visitor happened to swipe.
- Mobile nav dropdown background changed from `rgba(12,14,20,0.97)` to solid
  `var(--background)` — the 97% opacity was letting hero text visibly bleed
  through the open menu.

## Blog

Posts live as markdown in `_src/posts/` (front matter: title, slug, date, desc). Covers are generated by `_src/gen_covers.py`.
Run `python3 _src/build.py` to regenerate post pages (`/blog/<slug>/`), covers' PNG share images, `sitemap.xml`, and to re-apply the
homepage blog section, nav and footer links to the built bundle. `_src/` is excluded from deploys by `.vercelignore`.
Voice check: `python3 _src/lint.py`. Deploys happen on push to `main`; other branches get preview URLs.
