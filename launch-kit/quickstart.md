# 60-Second Quickstart — comfy-prompt v3.0.0

For developers who want to be productive in under a minute.

## Install (15s)

```bash
# Skill already at ~/.claude/skills/comfy-prompt/
# cf wrapper already at ~/.local/bin/cf

# Ensure ~/.local/bin in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Set Comfy Cloud API key (https://platform.comfy.org → API Keys)
export COMFY_API_KEY=comfyui-xxxxx
```

## First generation (10s)

```bash
cf gen nano-banana "minimalist matte black coffee mug on sunlit wooden desk" --tag first
```

Output lands in `~/Comfy-Output/2026-05/first/`. Auto-opens with `COMFY_AUTO_OPEN=1`.

## First video (1s submit, 2min async)

```bash
cf vid seedance "slow dolly over neon-drenched Tokyo street, rain reflections on pavement, 10 seconds" --platform tiktok
```

Returns a job_id, auto-logs it. Check with `cf jobs pending`.

## First workflow recipe (~45s)

```bash
cf character "weathered space pilot, late 30s, scarred jaw, worn leather jacket"
```

Generates 4-angle character sheet with identity locked. Outputs to `~/Comfy-Output/2026-05/character-sheet/`.

## See your spend

```bash
cf jobs budget
```

```
Total jobs  : 5
Completed   : $0.7600
Pending est : $0.0000
Grand total : $0.7600

By model:
    seedance      1 jobs  $0.6000
    nano-banana   4 jobs  $0.0400
```

## See everything available

```bash
cf help
```

## That's it.

You now have a brand-aware, cost-tracked, lint-validated, async-watched, gallery-ready Comfy workflow.

---

## Next-day moves

| When you want to... | Run |
|---------------------|-----|
| Set up a client project | `cf init ~/projects/client-x --name "Client X"` |
| Save a brand reference | `cf refs add brand-x ./hero.png --tags client,brand` |
| Generate 4 lighting variants | `cf variants "portrait" --axis lighting --exec` |
| Compare 3 models on same prompt | `cf compare "prompt" --models flux-pro flux-ultra nano-banana` |
| Compose template + vertical + style | `cf compose "subject" --template product --vertical viral-hook --style cyberpunk-blade-runner` |
| Open TUI dashboard | `cf dash --watch` |
| Generate HTML gallery | `cf gallery ~/Comfy-Output/2026-05/client-x/ --open` |
| Auto-poll async jobs | `cf watch --loop` |
