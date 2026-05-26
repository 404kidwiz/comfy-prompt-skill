# Template: Comedy / Social Media / Skit

## Genre / Use case
TikTok/Reels skits, social media clips, comedic reactions, meme video, talking-head
comedy, awkward-pause humor, slapstick, character comedy.

## When to use
User asks for funny, comedy, TikTok, meme, skit, social media clip, reaction shot,
sitcom moment, awkward moment.

## Recommended models
- **Talking-head reactions**: `seedance` (audio-capable, 9:16 ready) — best for face-driven comedy.
- **Static reaction meme**: `nano-banana` (versatile, fast, text-friendly).
- **Multi-character chat**: `seedance` for dialogue lip-sync.
- **Image meme + caption**: `ideogram` for clean text-in-image.

## Example prompt — `seedance` (TikTok skit)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Authentic UGC

A young man sits at his kitchen table, scrolling on his phone, looking bored.
[0-2s] MCU eye level. Static phone-camera angle. He glances up at someone off-screen.
[2-5s] Eyes widen comically. He slowly lowers the phone, mouth opening. Camera holds.
[5-8s] He looks back down at phone, then back up, then back down, double-take rhythm.
Audio: ambient kitchen sounds, no dialogue. End with quiet "no way" muttered.
Style: Authentic UGC TikTok. iPhone front-camera aesthetic, slight phone-grip shake,
natural daylight from off-screen window, no professional lighting.

Run:
comfy generate seedance --prompt "young man at kitchen table scrolling phone looking bored, MCU eye level static phone-camera, glances up at someone off-screen, eyes widen comically slowly lowers phone mouth opening, double-take rhythm looking back down at phone then back up then back down, ambient kitchen sounds quietly mutters 'no way' at end, authentic UGC TikTok iPhone front-camera aesthetic slight grip shake, natural daylight from off-screen window no professional lighting" --duration 8 --aspect_ratio 9:16 --async
```

## Annotation

| Element | Why it works |
|---------|--------------|
| "young man at kitchen table scrolling phone looking bored" | Mundane setup primes the contrast |
| "[0-2s] / [2-5s] / [5-8s] beat structure" | Comedy = timing. Per-second beats force rhythm. |
| "Eyes widen comically. He slowly lowers the phone" | Specific micro-expressions + slow gesture |
| "double-take rhythm: phone → up → phone → up" | Named comedic mechanic |
| "Authentic UGC TikTok. iPhone front-camera aesthetic" | Specific platform register |
| "slight phone-grip shake, natural daylight" | Anti-polish: comedy works when it looks unstaged |

## Negative constraints
```
no over-acting (eyebrows-to-hairline territory), no cartoonish exaggeration unless
explicitly cartoon register, no over-lit professional video look,
no clean cinematic composition (this is supposed to look unstaged)
```

## Common mistakes
1. **Over-acting** — Subtle beats > big mugging. "Slight smirk" > "huge laugh".
2. **Professional lighting** — Kills the UGC authenticity. Use "phone front-camera, natural light".
3. **Long prompts** — Comedy timing requires per-second beat structure. Keep it punchy.
4. **No payoff** — Setup → escalation → payoff. Name all three.
5. **Generic "funny"** — Be specific about the mechanic: double-take, awkward pause, slow burn, reaction shot.

## Variations

### Static reaction meme — `nano-banana`
```
Model: nano-banana (cloud)
Aspect: 1:1 | Style: Reaction Meme

ECU Eye Level of a young woman's face at the exact moment she sees something offensive
on her phone screen — eyebrows raised mid-flinch, mouth in a sideways pucker.
Phone partially visible at bottom-frame edge.
Lighting: harsh phone-screen glow on her face (cold cyan-blue).
Style: Reaction meme. iPhone selfie aesthetic. Slightly compressed.
No filter, no beauty smoothing, raw expression.
```

### Awkward pause — `seedance`
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 6s

Two people sitting across a small table. Both freeze mid-sentence.
[0-1s] Person A's mouth still open from last word.
[1-5s] Five seconds of silent eye contact. Neither breaks. Person B blinks once.
[5-6s] Person A slowly reaches for their drink, eyes still locked.
Camera: static MS two-shot, locked off.
Audio: room tone only, single distant car passing.
Style: Awkward sitcom register. Documentary lighting — soft overhead, no key.
The Office / Curb Your Enthusiasm flavor.
```

### Talking-head rant — `seedance`
```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s

A man speaking directly into front-facing phone camera while walking.
He's mid-rant about something mundane (parking, weather, customer service).
[0-3s] MCU walking head-on. Gesturing emphatically with free hand.
[3-7s] Slight build of intensity. He gestures wider, laughs at himself mid-sentence.
[7-10s] Final pause. He stops walking, looks directly at camera, says "...anyway."
Style: TikTok rant aesthetic. Phone-camera vertical. Natural light.
Background blurred urban sidewalk. Audio: clear voice, ambient street noise.
```

### Sitcom multi-cam reaction — `seedance`
```
Model: seedance (cloud, async)
Aspect: 16:9 | Duration: 8s

Three roommates in a living room. The first delivers an absurd statement, the other
two react in sequence.
[0-2s] WS three-shot. Roommate A says something absurd off-screen, looks up.
[2-4s] Cut to MS of Roommate B — slow blink, head tilt.
[4-6s] Cut to MS of Roommate C — already-eating chip frozen halfway to mouth.
[6-8s] Cut back to WS three-shot. Everyone holds the awkward beat.
Style: 90s sitcom multi-cam. Bright even sitcom lighting. Pastel set design.
Laugh track NOT included — let the silence carry it.
```

## Multi-shot social media campaign
```bash
# 1. Hook frame (still — would screenshot well for thumbnail)
comfy generate flux-pro --prompt "MCU young man at kitchen table holding phone, eyes wide in comic shock, natural daylight, TikTok aesthetic" --aspect_ratio 9:16 --download /tmp/hook.png

# 2. Animate hook into 5s clip
comfy generate pika-i2v --image /tmp/hook.png --prompt "subtle micro-expressions, hand slowly lowers phone, comedic timing" --duration 5 --async

# 3. Generate text-overlay variant (caption meme)
comfy generate ideogram --image /tmp/hook.png --prompt "add caption at top: 'when she sees the receipt', bold white sans-serif with subtle drop shadow, TikTok meme style" --download /tmp/captioned.png
```
