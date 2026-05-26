# Platform Optimization

Adapted from Roman Knox / @roman.knox skill set.

---

## TikTok (9:16 vertical)

| Spec | Value |
|------|-------|
| Aspect | 9:16 |
| Hook landing | 1.5s (fastest scroll speed) |
| Safe text zone | center 80% of frame |
| Audio | Trending audio integration critical |
| Length sweet spot | 5-15s |
| Loop priority | High — last frame should visually connect to first |

**Loop template:**
```
Final frame composition mirrors opening frame — same camera angle, same lighting,
same subject position. Last 0.5s movement creates visual continuation into the
first frame when video replays. Seamless loop point.
```

**Comfy model picks:**
- `seedance` for 8-10s vertical with audio
- `pika` for 5s clean vertical motion
- `runway-i2v` for image-to-video hero

---

## Instagram Reels (9:16 vertical)

| Spec | Value |
|------|-------|
| Aspect | 9:16 |
| Hook landing | 2s (slightly more patient than TikTok) |
| Aesthetic | Higher quality bar than TikTok |
| Color grading | Polish matters — audience expects it |
| Cover frame | Must work as static image in grid |
| Length sweet spot | 6-15s |

**Cover-frame trick:**
Plan one frame in the video (usually 2-3s mark, hero moment) that works standalone
as a Reels grid thumbnail. Don't waste your strongest visual on a frame the algorithm
won't pick.

**Comfy model picks:**
- `seedance` for hero quality
- `flux-ultra` for the cover-frame still

---

## YouTube Shorts (9:16 vertical)

| Spec | Value |
|------|-------|
| Aspect | 9:16 |
| Hook landing | 2-3s (most patient audience) |
| Production value | Highest expectation of three platforms |
| Length sweet spot | 8-30s |
| Retention target | 80%+ at 15s = algorithmic push |

**Title/description leverage:**
YouTube context comes from title + description more than other platforms. Visual
can be more subtle / build-driven because the title sets up the payoff.

**Comfy model picks:**
- `seedance` for 10-12s with audio
- `pika` × 2-3 clips stitched
- Local `Text to Video (Wan 2.2)` for repeated iteration without cost

---

## Instagram Feed (1:1 or 4:5)

| Spec | Value |
|------|-------|
| Aspect | 1:1 or 4:5 (4:5 takes more screen real estate) |
| Hook landing | 3s (slowest scroll context) |
| Sound | Often muted on autoplay — caption + visual must work without audio |
| Length sweet spot | 6-12s |

**Caption-driven:**
First frame should have an on-screen hook (text overlay) since 60%+ of feed scrolls
happen muted. Use `ideogram` or `dalle` to generate text-overlay frames if compositing.

---

## LinkedIn Video

| Spec | Value |
|------|-------|
| Aspect | 1:1, 4:5, or 16:9 |
| Hook landing | 3-5s (B2B audience, slower scroll) |
| Sound | Default muted — captions mandatory |
| Length sweet spot | 30s-90s |
| Tone | Professional, founder-led, authority-driven |

**No music default:**
LinkedIn autoplay strips audio. Voiceover with strong captions is the only audio
strategy that works. Or pure visual storytelling with caption beats.

---

## Twitter / X Video

| Spec | Value |
|------|-------|
| Aspect | 16:9 (landscape preferred for embed) or 9:16 |
| Hook landing | 2s |
| Length sweet spot | 6-60s |
| Sound | Mid — some users have audio on, most don't |

---

## Multi-aspect rendering pattern

If shipping the same content to TikTok + Reels + YouTube Shorts + LinkedIn, render
the vertical first (9:16), then crop center 16:9 for LinkedIn instead of regenerating.

```bash
# Vertical hero
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 10 --async

# After getting vertical output, center-crop for landscape via ffmpeg
ffmpeg -i vertical.mp4 -filter:v "crop=ih*16/9:ih" -c:a copy landscape.mp4
```

---

## Aspect ratio enum — verify per model

Not all cloud models accept every aspect ratio. Use `comfy generate schema <model>`
to verify before requesting an unusual ratio (or use `scripts/schema_cache.py`).

Anamorphic / 2.35:1 / 2.39:1 are STYLE register (Look line), not output ratios.
Most cloud models output at fixed enums (1:1, 16:9, 9:16, 4:5, 3:4). Anamorphic
look = 16:9 output + "anamorphic widescreen, letterboxed black bars" in Look line.
