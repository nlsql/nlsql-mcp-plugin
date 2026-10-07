# NLSQL plugin

Connect your database to [NLSQL](https://nlsql.com) from your AI assistant.

A guided wizard sets up an NLSQL data source with you:

- It reads the schema you paste (schema only, no table data).
- You pick the tables, columns and joins to include.
- You describe your KPIs, top-N rankings, filters and calculated metrics in plain language.
- It publishes the result to your NLSQL account, so your team can query the data in plain English.

You can also add the known values of category columns to make answers more accurate.
Supported databases: MySQL, PostgreSQL, MSSQL, BigQuery, Snowflake, Amazon Redshift, SQLite and CQL.

This repository is a thin client: plugin manifests, usage rules and a pointer to the hosted NLSQL MCP
server at `https://mcp.nlsql.com/mcp`. No server code runs on your machine. You sign in with your
NLSQL account the first time a tool is used.

## Install

### Cursor

Install **NLSQL** from the Cursor Marketplace, or click the install link:

[Add NLSQL to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=nlsql&config=eyJ1cmwiOiJodHRwczovL21jcC5ubHNxbC5jb20vbWNwIn0=)

Or add it by hand to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "nlsql": { "url": "https://mcp.nlsql.com/mcp" }
  }
}
```

### Claude Code

```
/plugin marketplace add nlsql/nlsql-mcp-plugin
/plugin install nlsql@nlsql
```

Or connect only the server, without the skill:

```
claude mcp add --transport http nlsql https://mcp.nlsql.com/mcp
```

### ChatGPT and Codex

Search for **NLSQL** in the ChatGPT / Codex plugin directory and connect it.

To install from this repository in the Codex CLI:

```
codex plugin marketplace add nlsql/nlsql-mcp-plugin
```

Then open `/plugins` in Codex and install **NLSQL**.

### Claude.ai and Claude Desktop

Go to **Settings → Connectors → Add custom connector** and enter `https://mcp.nlsql.com/mcp`.

## Usage

Ask your assistant something like *"Set up my PostgreSQL database in NLSQL"*. It starts the wizard, and
you can stop at any point. Ask it to *"continue my NLSQL data source setup"* later to pick up where you
left off.

## What's included

| Path | Purpose |
| --- | --- |
| `.cursor-plugin/plugin.json` | Cursor plugin manifest |
| `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` | ChatGPT / Codex plugin manifest (server address inline) and marketplace entry |
| `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` | Claude Code plugin manifest and marketplace entry |
| `mcp.json` / `.mcp.json` | Hosted server address (Cursor / Claude Code formats) |
| `dist/nlsql-openai-plugin.zip` | Upload package for platform.openai.com/plugins (portable Agent Plugins layout). Rebuild with `python3 scripts/build-openai-package.py` after changing `.codex-plugin/plugin.json`, `skills/` or `assets/` |
| `review/sample-schema.sql` | Sample PostgreSQL schema used by the directory review test cases |
| `rules/nlsql.mdc` | Cursor rule for driving the wizard |
| `skills/nlsql/SKILL.md` | How to drive the wizard well (Cursor, Codex and Claude Code) |

## Notes

- One data source is set up at a time per account. Finish or publish it before starting the next.
- The wizard never asks for database credentials or table data. It works from the schema text you provide.

## License

MIT. The license covers this repository's files only. The NLSQL service and MCP server are proprietary.
