# The Hook Arsenal — 12 Universal Patterns

Adapted from Roman Knox / @roman.knox AI Video Generator skill set.
Apply these to ANY Comfy video gen (seedance, pika, runway-i2v, vidu, grok-video).

## Why 2 seconds

| Window | What happens |
|--------|--------------|
| 0-2s | Gate. 50%+ bounce here, video dies. 90% stay, algorithm promotes. |
| 2-5s | Hook confirmation. Brain decides: worth it or not. |
| 5-15s | Engagement peak. Reveals, emotional beats, payoffs. |
| 15s+ | Retention cliff. Most viral videos under 15s. |

Videos with 80%+ completion get 2-3x algorithmic reach.

---

## 1. Pattern Interrupt — Break Reality

### Physics Break
Open with object defying physics — floating up, sliding in reverse, freezing mid-air.
Camera steady, treating impossible action as mundane. First 0.8s shows normal expectation,
0.8-2s breaks it. No music, only ambient sound emphasizing wrongness.

### Scale Warp
EWS: familiar object (coin, key, pen) scaled to building size in landscape. Human figure
provides scale reference. Drone-style slow push forward. Overcast lighting, photoreal.
Viewer spends 2s processing scale.

### Color Bomb
Scene begins fully desaturated — gray, lifeless. At 1.2s, single element ignites with
saturated color (neon pink / electric blue / gold). Color bleeds outward across frame
over 0.8s. Hard bass hit synced to color moment.

---

## 2. Curiosity Gap — Incomplete Information

### Obscured Subject
Tight framing: only hands working on something. Close-up of concentrated facial
expression. Creation sounds — cutting, assembling, clicking. Camera never shows full
object. At 2s slight pull-back hints at shape but doesn't reveal. Forces continued watch.

### Reaction Before Action
Open on person's face — eyes widen, jaw drops, hand covers mouth. Pure shock reaction
for 2s. No context, no environment. Sound: gasp, then silence. "What are they looking
at?" forces continued viewing.

### Countdown Tension
Bold text "3" appears center-frame with bass hit. Cut to new angle, "2" with rising synth.
Cut again, "1" with tension peak. Frame holds on black for 0.5s. The reveal never comes
in the hook — it's downstream. Camera movements accelerate with countdown.

---

## 3. Dopamine Trigger — Instant Reward

### Satisfying Motion (ASMR-tier)
ECU: liquid pouring perfectly into glass / knife slicing through smooth surface /
sand cascading slow motion. Macro lens, shallow DOF. Crisp ASMR audio synced to motion.
Slow motion at 0.5x speed. Warm golden side lighting.

### Before-After Flash
Split screen or quick cut: left/top shows "before" state for 0.8s. Hard cut or wipe.
Right/bottom shows transformed "after" state. Contrast must be dramatic — ugly→beautiful,
chaos→order, empty→full. Transition sound: whoosh + impact.

### Kinetic Typography
Bold white text on black. Words slam into frame one at a time, synced to beat. Each word
creates micro screen-shake. Text: provocative statement — 3-5 words max. Camera pushes in
slightly with each word. Bass-heavy sound design.

---

## 4. Primal Attention — Evolutionary Triggers

### Eye Contact
ECU of eyes in shadow. At 0.6s, eyes snap open and lock into camera. Pupil dilates.
Subtle head tilt forward — predatory, intense. Single rim light catches iris detail.
No blinking for 2s. Sound: heartbeat, low frequency.

### Sudden Movement
Frame is static, calm, almost boring for 1s. Then — fast object enters frame from edge
at high speed. Or person lunges toward camera. Movement creates motion blur trails.
Camera flinches slightly in response. Sound: sharp whoosh or impact synced.

### Silence Then Sound
First 1.5s: complete silence. Black screen or static wide shot. No sound at all — the
absence is jarring on a platform of constant noise. At 1.5s: explosive audio — bass drop,
scream, impact, alarm. Synced with hard visual cut to action.

---

## How to use in a Comfy video prompt

Pick a hook pattern. Build the rest of the MCSLA (Model · Camera · Subject · Look ·
Action) around it. Always lock the first 2 seconds as your hook beat, then escalate.

Example hook integration:

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s

HOOK [0-2s]: Color Bomb — open on fully desaturated kitchen scene, lifeless gray.
At 1.2s, single coffee mug ignites with deep amber color, warmth bleeding outward
across the frame over 0.8s. Hard bass hit synced to color moment.

ESCALATE [2-5s]: Camera slow push-in toward the mug. Color spreads to envelope
the room — now fully saturated golden hour. Steam rises.

PAYOFF [5-8s]: Hand enters frame, lifts the mug. Logo subtly visible on mug face.
Final beat: hand holding mug center-frame, single point of focus.

Run:
comfy generate seedance --prompt "..." --duration 8 --aspect_ratio 9:16 --async
```
