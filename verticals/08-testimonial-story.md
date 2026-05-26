# Vertical: Testimonial Story — Social Proof That Converts

Adapted from Roman Knox `seedance-testimonial-story` skill for Comfy.

## When to use
Customer testimonial, case study, social proof, review showcase, success story,
client wins, results-focused content.

## Recommended Comfy models
| Use | Model | Path |
|-----|-------|------|
| Multi-customer reel (10-12s) | `seedance` | Cloud, async |
| Single customer face hero (5-8s) | `seedance`, `pika-i2v` | Cloud, async |
| Image-to-video customer portrait | `pika-i2v`, `runway-i2v` | Cloud, async |
| Text-overlay quote cards | `ideogram` | Cloud, sync |
| Static customer portrait | `flux-pro`, `nano-banana` | Cloud, sync |

---

## Why Traditional Testimonials Fail

Bad testimonials look like:
1. **Talking head reading a script** — robotic, doesn't feel real
2. **Stock-photo "happy customer"** — clearly fake
3. **Text-on-screen review** — boring, no humans, no story
4. **Long-form interview clip** — buries the hook 30 seconds in

Testimonials that convert do three things:
1. **Show the customer's CONTEXT** — environment communicates credibility
2. **Show specific RESULTS** — numbers, before-after, real outcomes
3. **Capture micro-emotion** — small genuine reactions (smile breaking, eyes
   widening, gentle laugh) beat performative gratitude

---

## Hook Patterns for Testimonials

### Result First, Person Second
```
Bold text overlay: "$50K in 30 days." Hold 1.5s. Sound: bass hit. Cut to customer
in their context (office, home, business). They look at camera, slight smile.
Voiceover: "And I didn't expect this." Hook lands by showing the WIN first, then
the person.
```

### Voiceover Over Context
```
ECU of customer's hands on their work — coding, designing, writing, building.
Voiceover begins immediately: confident statement. Camera pulls back to MS of
customer in workspace. Then cuts to face at the emotional beat of the statement.
```

### Multi-Customer Montage
```
Quick cuts (1s each) of 3-5 different customers in their contexts. Caption
overlay names each with key result. Last shot holds 2-3s on most relatable
customer. Music builds to peak on landing customer.
```

### Before-After Story Arc
```
0-2s: Customer in "before" state (frustrated, generic office, dim light).
2-4s: Wipe transition with bass hit.
4-8s: Customer in "after" state (confident, premium environment, warm light).
Voiceover spans both: the transformation IS the testimonial.
```

---

## Visual Formats for Testimonials

### Workspace Interview
```
Customer in their actual workspace (or generated equivalent). MS 3/4 angle.
Three-point lighting with warm key. Subject talks to interviewer just off-camera.
Reads as documentary captured moment, not staged shoot.
```

### Result Reveal
```
ECU on the result itself — bank dashboard with revenue, fitness photo,
before-after design, screenshot of feedback. Hold 1.5s. Cut to customer's
reaction face. Their genuine response IS the testimonial.
```

### Multi-Cut Story
```
5-6 quick cuts: customer working, customer celebrating, the result, customer
explaining (voiceover layered), customer at end resolving. Music builds and
resolves.
```

### Quote Card Composite
```
Customer in subtle bokeh background, large pull-quote in clean typography
overlaid. Customer slightly out of focus, quote sharp and primary. Reads as
editorial / magazine register.
```

---

## Typography for Testimonial Cards

For text-overlay testimonial cards, use `ideogram` or `dalle` for cleanest text:

```bash
comfy generate ideogram \
  --prompt "magazine-style testimonial quote card, large pull-quote text 'I made $50K in 30 days' in bold serif typography, small attribution below 'Sarah K., Founder, [Company]', warm ivory background with soft drop shadow, editorial design aesthetic" \
  --aspect_ratio 9:16 \
  --download /tmp/quote.png
```

---

## Lighting for Testimonials

| Setup | Use |
|-------|-----|
| **Window Documentary** | Single large window key, no fill. Natural authenticity. Subject in 3/4 to camera. |
| **Warm Workspace** | Three-point with warm key. Reveals customer's real environment. Reads as captured moment. |
| **Office Editorial** | Cleaner studio-style with two-tone lighting. Premium / executive register. |
| **Outdoor Natural** | Golden-hour outdoor for lifestyle customer (fitness, travel, etc.). Soft side-light + ambient. |

---

## Sound Design for Testimonials

| Layer | What it does |
|-------|--------------|
| Customer voice | Primary track. Clear recording. Sentences naturally cadenced. |
| Music | Warm pad enters at 2s, builds subtly, resolves on landing customer line. |
| Sound effects | Whoosh on cuts to result reveals. Bass hit on key emotional beats. |
| Environmental | Light room tone keeps authenticity. Don't strip all ambient sound. |

NEVER use: fake applause, over-the-top music swells, stock "uplifting acoustic"
tracks. These signal fake testimonial immediately.

---

## Worked Example — Multi-Customer Reel (10s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 10s | Style: Documentary Cinematic

[0-2s] HOOK — Result First:
Black screen. Bold text overlay: "$127K in 60 days" — large, white, serif type
center frame. Hold 1.5s. Sound: ambient room tone + soft music pad enters.
Hard cut at 1.5s to first customer.

[2-4s] CUSTOMER 1:
Sarah, MS 3/4 angle at her workspace (cafe / home office). Warm window light.
She looks at camera, half-smile, says short phrase. Lower-third caption: "Sarah K.
— $127K in 60 days." Sound: voiceover with her actual statement.

[4-6s] CUSTOMER 2:
Hard cut to Marcus, MS 3/4 angle in his gym / office. Different environment but
same warm window-light register. He gestures emphatically. Caption: "Marcus T. —
Lost 40lbs in 90 days." Music continues building.

[6-8s] CUSTOMER 3:
Cut to Priya, ECU rack focus on her hands working then to her face. Same warm
ambient. Caption: "Priya N. — Launched in 30 days." Music reaches peak.

[8-10s] LANDING:
Final frame: composite or split-screen of all 3 customers, each in their context.
Text overlay: "Real results. Real people." Music resolves on sustained chord.

Sound: 0-2s room tone + pad entering. 2-8s each customer's voice + pad layer
building. 8-10s music resolution.

Material references: --image $C1, --image $C2, --image $C3 (customer portraits
if available).

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 10 --async
```

---

## Worked Example — Single Customer Hero (8s)

```
Model: seedance (cloud, async)
Aspect: 9:16 | Duration: 8s | Style: Documentary Authority

[0-2s] HOOK — Voiceover Over Context:
ECU of customer's hands on their work — typing on laptop, business activity
specific to their industry. Macro lens, shallow DOF. Warm window light. Sound:
voiceover begins immediately: "I used to think this was impossible." No music yet.

[2-5s] REVEAL:
Camera pulls back to MS revealing customer in workspace. Three-point lighting:
warm key, soft fill, brand-color rim. Customer continues voiceover, eyes lift to
look just past camera. Music ambient pad enters at 3s.

[5-7s] EMOTION:
Cut to slightly closer angle. Customer's voiceover lands key line — the
transformation moment. Their face shows genuine micro-emotion — smile breaking,
eyes slightly wider, gentle laugh. NO performance, captured moment.

[7-8s] LANDING:
Final frame: customer in 3/4 frame, slight smile, environment in shallow bokeh.
Music resolves. Voiceover delivers final 3-word sentence.

Run:
comfy generate seedance --prompt "<...>" --aspect_ratio 9:16 --duration 8 --async
```

---

## Identity locks for testimonials
- Show RESULT before person (when possible) — hook by win, confirm by face.
- Customer in their REAL context. Generic office b-roll kills credibility.
- Capture MICRO-emotion. Performative gratitude reads fake.
- Lower-third captions with name + specific result. Numbers > adjectives.
- Music sparse, voice primary. Avoid stock uplifting acoustic.
- Multiple customers > one customer for proof-density.
- Last beat: name + result + brand logo. Clear who's saying this and what they did.
