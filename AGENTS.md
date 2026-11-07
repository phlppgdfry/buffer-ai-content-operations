# AGENTS.md — Guidelines for AI Coding Agents

This repository is maintained and operated with multi-agent assistance. Follow these guidelines when making modifications:

## 1. Safety & Posting Policy
- **Never modify `saveToDraft: True` default**: Any automated posting integration must preserve human sign-off before publishing to social media.
- **Dry-run First**: Always ensure `--dry-run` validation works before running live mutations.

## 2. Testing & Quality Verification
- Run tests before committing:
  ```bash
  source .venv/bin/activate
  pytest -v
  ruff check .
  ```
- All new extractors or agent steps must include corresponding unit tests in `tests/`.

## 3. Buffer API Conventions
- Reference official schemas via `buffer schema describe posts create`.
- Adhere to Buffer's GraphQL conventions:
  - Endpoint: `https://api.buffer.com`
  - Mutation: `createPost(input: $input)`
  - Key fields: `channelId`, `mode`, `schedulingType`, `saveToDraft`, `text`.
