# System Design Architect — Optional Interactive App

This package is an optional MCP + React visual workspace for the System Design Architect skill.

The core plugin does not depend on this app. Use it when you want richer interactive system views and granular process-step drill-down inside ChatGPT.

## Local development

```bash
cd app
npm install
npm run build
npm start
```

MCP endpoint:

```text
http://localhost:8000/mcp
```

For ChatGPT Developer Mode, expose the local endpoint through HTTPS (for example with an HTTPS tunnel) and add the resulting `/mcp` URL as a development app.

## Tools

- `validate_system`
- `visualize_system`
- `load_example_system`

All current tools are read-only and the server is stateless.
