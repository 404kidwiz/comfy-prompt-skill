# Vertical: Course Promo — Trailers That Sell Out Programs

Adapted from Roman Knox `seedance-course-promo` skill for Comfy.

## When to use
Course, coaching, masterclass, webinar, tutorial, training, academy, educational
product video, online program promo.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Course trailer (10-15s, audio, multi-shot) | `seedance` | Cloud, async |
| Coach face hero (5s) | `pika-i2v`, `runway-i2v` | Cloud, async |
| Curriculum reveal still (modules visualized) | `flux-pro`, `nano-banana` | Cloud, sync |
| Module text overlay | `ideogram` | Cloud, sync |

---

## The Promise → Proof → Path Structure

Course promos that convert follow a 3-beat arc:

1. **Promise** (0-3s) — name the transformation in visual terms
2. **Proof** (3-8s) — show the work / method / result
3. **Path** (8-12s) — the curriculum / next step

Skip any beat and you have content, not conversion.

---

## Hook Patterns for Course Promo

### Outcome Reveal
```
Open on the END STATE the course delivers — confident speaker on stage, finished
product launched, fit body in mirror, six-figure dashboard. Hold 2s. NO context.
Viewer immediately sees: "this is what I want."
```

### Method Tease
```
Tight ECU of the COACH'S HANDS doing the thing — writing the framework, drawing
the diagram, demonstrating the technique. Don't show face. The method is the hook.
Camera 0.5x slow motion. Sound: pen on paper / hand on whiteboard ASMR.
```

### Pattern Interrupt — Cost Question
```
Bold typography text-overlay: "Why is no one teaching this?" Beat. Replace with
"Here's the framework." Hard cut to coach in environment. Music drops in on cut.
```

---

## Visual Style Templates

### Educational Authority
```
Coach in clean workspace. Whiteboard or large display visible. Soft key from window.
Subject in 3/4 angle to camera. Cinematic but documentary — feels like a glimpse
of real teaching. Cool blue ambient with warm coach lighting separation.
```

### Result Showcase
```
Quick cuts of student transformations — before/after pairs, screenshots of wins,
testimonial faces with caption overlays. Each shot 1s. Synced to beat. Reads as
proof, not promise.
```

### Curriculum Visualization
```
Animated module structure — text or numbered modules floating in 3D space. Each
module reveals with text-overlay animation. Camera orbits or pushes through.
Reads as roadmap, not table of contents.
```

---

## Lighting for Course Content

| Setup | Use |
|-------|-----|
| **Window Studio** | Single large window key, no fill. Natural authority register. Coach reads as approachable expert. |
| **Premium Stage** | Backlit speaker silhouette with audience implied in background bokeh. Reads as paid speaking gigs / authority. |
| **Workspace Real** | Three-point on coach at desk. Environment props (books, certificates, equipment) lit with practicals. |

---

## Sound Design for Course

Critical: avoid the "course ad" sound. Banish:
- Stock acoustic ukulele
- Generic corporate uplift
- Inspirational orchestral swells

Use instead:
- Minimal electronic, 90-110 BPM, modern
- Single sustained pad with subtle progression
- Voiceover-driven with sparse music underneath
- Drum + bass for energetic / hustle-coded promos

---

## Worked Example — Course Trailer (12s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 12s | Style: Premium Coaching Trailer

[0-2s] PROMISE:
Hard cut to the END STATE: confident person on a Zoom call leading a team, screen
visible with their product/dashboard. Camera slow push-in. Warm window light. Sound:
ambient room tone + faint typing + subtle motivational pad enters at 1s.

[2-4s] CONTEXT:
Cut to text-overlay: "How [outcome] in [timeframe]" bold sans-serif, white on
slightly desaturated freeze-frame background. Text slides up from bottom over 0.5s.
Hold 1.5s.

[4-7s] METHOD TEASE:
Cut to coach in workspace, MCU 3/4 angle. They write a framework on a notebook,
camera ECU on hand. Cut back to MCU coach looking at camera with slight smile.
Cut to whiteboard with key concept written in marker. 3 cuts in 3s, music begins
building.

[7-10s] PROOF:
Quick montage of 3 student wins — caption overlay names + result. Each 1s. Faces
visible, real. Cinematic but documentary. Music reaches plateau.

[10-12s] CTA:
Final frame: coach centered, MS angle, slight smile, in workspace. Text-overlay
below: "Join the [program name]" + small "Link in bio" detail. Music resolves on
final chord.

Sound: 0-2s ambient + soft pad. 2-4s pad continues. 4-7s pad layers in subtle
percussion. 7-10s full mix, drums + bass. 10-12s music plateaus then resolves.

Material references: --image $COACH (coach face/identity), --image $WORKSPACE
(coach environment).

Run:
COACH=/path/to/coach.jpg
comfy generate seedance --prompt "<...>" --image "$COACH" --aspect_ratio 9:16 --duration 12 --async
```

---

## Worked Example — Coaching Pattern-Interrupt Hook (6s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 6s | Style: Pattern-Interrupt Coaching

[0-2s] HOOK:
Black screen. Bold white text: "Why is no one teaching this?" Hold 1s, fade to
text 2: "Here's the framework." Hard cut to coach in workspace, MCU 3/4 angle.
Music drops in: minimal electronic with bass.

[2-4s] DEMONSTRATE:
Cut to ECU of coach's hand drawing 3 simple boxes on a notebook with arrows
between them. Caption appears next to each box: [Module 1] → [Module 2] → [Module 3].
Cut to MCU coach looking at camera with raised eyebrow + slight nod.

[4-6s] CTA:
Cut to text-overlay: "[Program name] enrollment open until [date]" with timer
visual. Final beat: coach centered MS, slight smile, holds for 1s. Music resolves.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 6 --async
```

---

## Identity locks for course promo
- Coach face → eye contact at moments of conviction, not constant smiling.
- Outcome shown before method. Promise → Proof → Path.
- Whiteboard / notebook / framework visible. Course = method visualized.
- Real student wins, not fake testimonials. Caption with name + result.
- Never use stock acoustic ukulele or generic corporate uplift music.
- CTA at end, clear next step. Link-in-bio / enroll-now / DM-keyword.
