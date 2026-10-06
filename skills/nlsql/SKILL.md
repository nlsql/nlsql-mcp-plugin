---
name: nlsql
description: Use when the user wants to connect a database to NLSQL, set up or continue an NLSQL data source, or add column values to NLSQL, through the NLSQL MCP tools.
---

# Setting up an NLSQL data source

The `nlsql` MCP server signs the user in with their NLSQL account and runs a guided
wizard. The wizard turns their database schema and business metrics into an NLSQL
data source, then publishes it to their account so they can query the data in plain English.

The server sends its own detailed instructions when you connect. Follow them; this
skill only adds the points that are easy to get wrong.

## The loop

1. Call `nlsql_config_wizard` with no data. It resumes wherever this user left off,
   so it is also the way to continue an earlier session.
2. Every response has a `next_action`. Do it straight away, then call the wizard
   again with exactly the keys named in the response's `after` field:
   - `ask_user_text`: show `message` and collect the user's answer.
   - `ask_user_question`: ask the `questions` as multiple choice.
   - `interpret`: do the extraction `message` describes yourself and send back the
     JSON it asks for.
   - `show_then_ask`: show `message`, then ask the `questions`.
3. When the wizard returns `final_response`, call `publish_datasource` without
   waiting to be asked.

**No `AskUserQuestion` tool?** Show each question with its options as a numbered
list, say whether one or several may be picked (`multiselect`), and wait for the
reply. Map the reply back to the exact option text before calling the wizard.

## Getting the schema

The wizard gives the user a command for their database type that prints the schema
only (for example `pg_dump --schema-only`). It needs no table data.

- If you can run shell commands, you may offer to run that command for the user.
  Ask first, because it needs their database credentials, and never echo a password
  back into the chat.
- Otherwise ask the user to run it and paste the output.

When interpreting the schema, include joins that are obvious from naming (for
example `orders.customer_id` to `customers.id`) even if no foreign key declares them.

## Things to keep in mind

- **Data source names** may contain only letters, numbers, hyphens and underscores.
- **Steps 10 to 14 are optional.** These are KPIs, top-N rankings, filters,
  calculated metrics and column-value arguments. The user can answer `none` to skip any of them.
- **One setup at a time.** Each account has one data source in progress. Finish or
  publish it before starting another.
- **Column values come after publishing.** To improve accuracy, call
  `get_column_values`. It asks you to write `SELECT DISTINCT` queries for the user to
  run. Send their results back, confirm them, then call `publish_column_values`.
- **Errors**: if `publish_datasource` returns an `error`, show it and offer to retry.
