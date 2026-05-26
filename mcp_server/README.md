# MCP Server Stub for comfy-prompt

Exposes key `cf` commands as Model Context Protocol tools so any MCP-enabled
Claude session can invoke them without needing slash commands or shell access.

## Status

Stub / blueprint only. Implementation requires `mcp` Python package:
```bash
pip install mcp
```

## Planned tool surface

| MCP Tool             | Wraps                  | Purpose |
|----------------------|------------------------|---------|
| `comfy_generate`     | `cf gen`               | Single image generation |
| `comfy_video`        | `cf vid`               | Video generation |
| `comfy_compose`      | `cf compose`           | Template+vertical+style prompt builder |
| `comfy_variants`     | `cf variants`          | N-axis variations |
| `comfy_compare`      | `cf compare`           | Multi-model A/B |
| `comfy_lint`         | `cf lint`              | Pre-flight prompt validation |
| `comfy_budget`       | `cf jobs budget`       | Spend report |
| `comfy_refs_list`    | `cf refs list`         | Reference library listing |
| `comfy_refs_use`     | `cf refs use`          | Resolve ref slug → path |
| `comfy_jobs_pending` | `cf jobs pending`      | Async job status |

## Implementation outline

```python
# server.py
from mcp.server import Server
from mcp.types import Tool, TextContent
import subprocess
import json
from pathlib import Path

server = Server("comfy-prompt")
CF = "/Users/dawizkidmal/.local/bin/cf"

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="comfy_generate",
             description="Generate a still image via Comfy Cloud",
             inputSchema={
                 "type": "object",
                 "properties": {
                     "model": {"type": "string"},
                     "prompt": {"type": "string"},
                     "tag": {"type": "string"},
                     "platform": {"type": "string"},
                 },
                 "required": ["model", "prompt"],
             }),
        # ... etc
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "comfy_generate":
        args = [CF, "gen", arguments["model"], arguments["prompt"]]
        if tag := arguments.get("tag"):
            args += ["--tag", tag]
        if platform := arguments.get("platform"):
            args += ["--platform", platform]
        result = subprocess.run(args, capture_output=True, text=True)
        return [TextContent(type="text", text=result.stdout)]
    # ... etc
```

## Wire-up

Once implemented, register in Claude Code:

```bash
claude mcp add comfy-prompt-local \
  --transport stdio \
  python3 /Users/dawizkidmal/.claude/skills/comfy-prompt/mcp_server/server.py
```

## Notes

- Build only if you find yourself wanting Comfy ops from Claude sessions that
  can't run shell commands or invoke slash commands (rare).
- For 99% of use cases, the slash commands + `cf` wrapper are sufficient.
- An MCP server would mostly duplicate that surface with extra abstraction.
- Defer until clear demand emerges.
