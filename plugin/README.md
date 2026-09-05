# System Design Architect Plugin

This package turns the open-source System Design Architect skill into an interactive ChatGPT/Codex plugin.

## Architecture

```text
ChatGPT / Codex
      │
      ├── bundled System Design Architect skill
      │       └── reasoning, evidence discipline, system design, BUILD READY decomposition
      │
      └── MCP app
              ├── validate_system
              ├── visualize_system ──► interactive React workspace
              └── load_example_system
```

The canonical system model remains the structural source of truth. The widget renders synchronized views and lets the user drill into granular process-step contracts.

## What the widget shows

- AS-IS / TARGET structural views
- granular BUILD READY process steps
- full process-step implementation contracts
- risks, controls, and recovery
- health signals and adaptive/self-healing boundaries
- model validation status

## Local development

Requirements: Node.js 20+ and npm.

```bash
cd plugin
npm install
npm run build
npm start
```

The MCP endpoint will be available at:

```text
http://localhost:8000/mcp
```

A basic server status endpoint is available at `http://localhost:8000/`.

## Try the app with MCP Inspector

After starting the server, connect an MCP Inspector/client to:

```text
http://localhost:8000/mcp
```

Useful first calls:

1. `load_example_system` — loads the worked onboarding system and opens the visual workspace.
2. `validate_system` — validates a canonical model and its BUILD READY process-step contracts.
3. `visualize_system` — renders a model supplied by ChatGPT or another client.

## Try inside ChatGPT

For local testing, ChatGPT needs a public HTTPS URL for the MCP server.

1. Run the server locally on port 8000.
2. Expose it through an HTTPS tunnel, for example:

   ```bash
   ngrok http 8000
   ```

3. In ChatGPT, enable Developer Mode under **Settings → Apps & Connectors → Advanced settings**.
4. Create/add a development app using the public tunnel URL with `/mcp`, for example:

   ```text
   https://<your-tunnel-domain>/mcp
   ```

5. Refresh the app after tool or widget metadata changes.
6. In a new chat, try:

   ```text
   Use System Design Architect to build a complete employee onboarding system.
   Make it visual and end to end. Do not stop at architecture: decompose the
   TARGET into granular BUILD READY process steps, validate the model, and show
   me the interactive system workspace.
   ```

Or simply ask to load the example system first.

## Important packaging note

The folder already contains the plugin manifest (`.codex-plugin/plugin.json`), bundled skill (`skills/`), and local MCP configuration (`.mcp.json`). For ChatGPT directory/public distribution, the hosted MCP server must first be registered as an app; add the resulting app registration mapping according to the current OpenAI plugin packaging workflow before public distribution.

## Security model

The current MCP tools are read-only. They validate and render a model supplied by the host; they do not mutate external systems or make open-web calls. The server is stateless by design.

## Current status

This is the first interactive plugin prototype. The next major product milestones remain:

- executable behavioral evals across models/agents;
- live evidence adapters for System Health;
- richer graph layout and direct node/flow drill-down;
- persisted system workspaces when a storage/auth layer is intentionally introduced.
