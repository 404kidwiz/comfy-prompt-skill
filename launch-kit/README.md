# Launch Kit — comfy-prompt v3.0.0

Promotional assets for LinkedIn + X + Twitter. Designed for:
1. **Show people how to use it** — runnable demos, copy-paste commands
2. **Show people how to iterate** — fork, customize, extend

## Files

| File | What it is |
|------|-----------|
| `linkedin-post.md` | Long-form LinkedIn launch post (~280 words) |
| `x-thread.md` | 8-tweet X thread with code snippets |
| `one-liner.md` | Elevator pitch + 5 alternate hooks |
| `quickstart.md` | 60-second onboarding for new users |
| `fork-and-customize.md` | How to make the skill yours |
| `demo-video.sh` | **Runnable** — generates a promo video using the skill itself |
| `hero-promo.sh` | **Runnable** — generates the hero image for posts |
| `press-kit/feature-grid.md` | Screenshot/recording checklist for visuals |
| `press-kit/before-after.md` | Prompt comparison samples |

## The meta-move

The skill promotes itself. `demo-video.sh` and `hero-promo.sh` are real
shell scripts that use `cf` + `comfy generate` to produce the very assets
you'd post on LinkedIn/X. People reading the post can run the script and
generate their own variant.

That's the loop: see post → run script → produce own variant → post own variant.

## Run order to launch

```bash
# 1. Generate hero image (~$0.10, takes 10s)
export COMFY_API_KEY=comfyui-...
~/.claude/skills/comfy-prompt/launch-kit/hero-promo.sh

# 2. Generate demo video (~$0.60, takes 2min async)
~/.claude/skills/comfy-prompt/launch-kit/demo-video.sh

# 3. Pull copy
cat ~/.claude/skills/comfy-prompt/launch-kit/linkedin-post.md
cat ~/.claude/skills/comfy-prompt/launch-kit/x-thread.md

# 4. Post to LinkedIn + X with the generated hero image
```

Total: ~3 minutes of generation, $0.70 of credits, fully launched.
