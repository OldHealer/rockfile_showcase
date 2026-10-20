# Engineering notes

Short write-ups of decisions in Rockfile that were not obvious, with the reasoning behind them. Each note is *problem → decision → result*.

- [Strict CSP without `unsafe-inline`](#strict-csp-without-unsafe-inline)
- [Server-side i18n for a vanilla-JS app](#server-side-i18n-for-a-vanilla-js-app)
- [Cache busting without a build step](#cache-busting-without-a-build-step)
- [LLM fallback chain with a per-attempt audit](#llm-fallback-chain-with-a-per-attempt-audit)
- [Grounded answers: sources come from the graph](#grounded-answers-sources-come-from-the-graph)
- [Deploy with automatic rollback](#deploy-with-automatic-rollback)
- [AWS → Hetzner migration](#aws--hetzner-migration)
- [Race-safe invite codes](#race-safe-invite-codes)
- [Notes ↔ promises: one fact, two views](#notes--promises-one-fact-two-views)
- [Frontend audit: bugs worth remembering](#frontend-audit-bugs-worth-remembering)

---

## Strict CSP without `unsafe-inline`

**Problem.** The frontend has no bundler, and a few inline scripts are essential: the theme has to be applied before first paint (otherwise the page flashes in the wrong theme), and some small pages have inline modules. The usual shortcut is `script-src 'unsafe-inline'`, which removes most of the XSS protection CSP gives.

**Decision.** At startup the app scans every HTML page, computes a `sha256` for each inline `<script>` and puts the hashes into `script-src`. The policy therefore always matches the files on disk and needs no manual upkeep, while any injected script has no hash and is blocked. The rest of the policy is `default-src 'self'`, `connect-src 'self'` (Keycloak is proxied on the same origin), `frame-ancestors 'none'`, `object-src 'none'`, `base-uri` and `form-action` locked to self; fonts are self-hosted. The middleware also sets `nosniff`, `X-Frame-Options: DENY` and a strict referrer policy.

**Rollout.** First `Content-Security-Policy-Report-Only`, then a Playwright smoke test that opens all 16 pages, switches theme and language and fails on any CSP message in the console. Only after a clean run (18 checks, 0 violations), including the Keycloak login flow, the header was switched to enforcing mode.

**Result.** Enforced CSP with hashes only. The e2e check stays in place, so a new inline script without a matching hash fails the suite rather than breaking production.

## Server-side i18n for a vanilla-JS app

**Problem.** The UI was translated in the browser after load. On the English version Russian text was visible for a moment and labels in the header jumped as they were replaced.

**Decision.** One set of JSON dictionaries (common + one per screen) is shared by both sides:

- the browser imports them as JSON modules (`import … with { type: "json" }`) and applies `data-i18n`, `data-i18n-html` and `data-i18n-attr` attributes;
- the server applies the same rules to the HTML before sending it, choosing the language from a cookie and answering with `Vary: Cookie`.

Rendered pages are cached per page and language and invalidated by file modification time, so editing a dictionary needs no restart. The server deliberately never touches `<script>` contents - otherwise the CSP hashes above would stop matching. API error messages and agent answers are localized too.

**Result.** Pages arrive already in the right language with no flash of untranslated text, and there is still exactly one place where each string lives.

## Cache busting without a build step

**Problem.** Without a bundler there are no content-hashed filenames. Cache busting was done by hand with `?v=N` query strings - 81 of them across the HTML - and a forgotten bump meant users ran stale JavaScript against a new API.

**Decision.** All app assets are served with `Cache-Control: no-cache`, which in HTTP means "store, but revalidate before use". The static file server already sends `ETag`s, so revalidation is a cheap `304 Not Modified`. Fonts are the exception: their filenames change with the version, so they get `max-age=31536000, immutable` and never cost a round trip before text renders.

**Result.** Every deploy is picked up on the next page load, with no manual versioning and only conditional requests as the overhead.

## LLM fallback chain with a per-attempt audit

**Problem.** Free LLM tiers are fast but rate-limited and occasionally down. Paid providers are reliable but cost money, and for a beta the bill must stay predictable.

**Decision.** A single factory builds the model as `primary.with_fallbacks([...])` from configuration: **Groq → Gemini → DeepSeek → OpenAI → Anthropic → Ollama**. Free tiers come first, then cheap paid models, then a local model. A provider without an API key is skipped, so the chain is configured once and filled in as keys appear. Paid providers run on small prepaid balances, so a runaway loop cannot produce a surprise bill.

Each model in the chain carries callback handlers and its provider name in metadata. Every attempt, including failed ones that triggered a fallback, is stored in `agent_calls` with provider, model, tokens, latency and status, and shown in the admin panel. The whole chain was verified end-to-end by forcing failures down to each provider.

**Result.** The assistants keep working when a provider is rate-limited, and the admin log shows exactly which provider answered, how often fallbacks happen and what each call costs in tokens.

## Grounded answers: sources come from the graph

**Problem.** An assistant that says "you promised Anna to send the deck" is only useful if the user can click through to Anna's card - and if Anna actually exists. Asking the model to list its sources invites invented names and IDs.

**Decision.** In the Concierge graph the nodes that load data (`collect_birthdays`, `collect_promises`, `enrich_context`) also record the sources: contact ID, name and a reason such as "birthday on 12 Nov" or "3 open promises". The LLM only writes the prose. Low-confidence intent classification (< 0.5) goes to a clarifying question rather than a guess.

**Result.** Every reference in an answer points to a real card the user owns; the model has no channel to fabricate one.

## Deploy with automatic rollback

**Problem.** A single production server, no orchestrator, and a solo developer who may not be watching when a deploy finishes.

**Decision.**

- **Before merge**: every PR builds the production image, starts it (database migrations run on startup) and checks the app and its OpenAPI schema, besides the test suite and `docker compose config` for both environments.
- **On deploy**: the workflow remembers the current commit, deploys the new one and polls the public URL up to 15 times. If it never answers `200`, the job prints the app logs, resets to the previous commit, rebuilds, checks that production is alive again and writes a "PROD ROLLBACK" summary.

**Result.** A broken release costs a minute of degraded service instead of an outage until someone notices.

## AWS → Hetzner migration

**Problem.** Production ran on AWS EC2 + RDS on the free plan. When it ended, the same setup would cost about $30/month on 1 GB of RAM.

**Decision.** Move to a Hetzner Cloud ARM VPS in Finland with 4 GB of RAM for a fraction of the price, as a single Compose stack with PostgreSQL in a container. Things that mattered:

- **Version pinning for a clean restore.** The app database runs PostgreSQL 18 to match the RDS version the dump came from. Keycloak is pinned to the exact version of its schema; a `latest` image would have silently migrated the restored database on first start.
- **Reproducible builds.** `poetry.lock` is committed and used in the image, so the server builds exactly what CI tested. All images and dependency wheels were checked for `arm64`.
- **Server hardening as code.** One idempotent bootstrap script: Docker with log rotation, unprivileged deploy user with a read-only deploy key, swap, firewall, `fail2ban`, unattended security upgrades, key-only SSH without root.
- **Backups replacing RDS snapshots.** A dedicated container takes nightly `pg_dump`s of both databases, writes them through a temporary file so an interrupted dump never looks complete, catches up immediately after a reboot, and keeps seven days.

**Result.** Four times the memory at a fraction of the cost, a server that can be rebuilt from scratch with one script, and the same deploy pipeline as before.

## Race-safe invite codes

**Problem.** Registration is invite-only. Checking that a code is unused and then marking it used are two steps; two people registering with the same code at the same moment could both pass the check.

**Decision.** The code is consumed with a single conditional `UPDATE … WHERE used_at IS NULL AND NOT revoked AND (not expired)` and the affected row count decides the winner. Because the user has already been created in Keycloak and the local database by that point, the loser's account is rolled back through the regular account-deletion path, so nothing is left half-created in either system.

The same "fail cleanly across two systems" thinking applies to the rest of sign-up: demo-data seeding and the verification email are best-effort and never undo an already created account.

## Notes ↔ promises: one fact, two views

**Problem.** Users write follow-ups as checklist items in notes ("send Anna the deck by Friday"), but the Today view and the assistants work with promises. Keeping two lists in sync by hand defeats the purpose.

**Decision.** Promises have a polymorphic source - an interaction or a note row. When a row on a note linked to a contact gets a due date, it becomes a checkbox and a promise is created; removing the date removes the promise; checking the row completes the promise; completing the promise from Today checks the row. If the source is deleted, the promise stays for history with its source cleared. Lists that show where a promise came from resolve all sources with two batch queries instead of one per item.

**Result.** One fact, visible in the note, on the contact card, in Today and to the assistants, with a single source of truth.

## Frontend audit: bugs worth remembering

Two audits of the frontend found issues that are easy to miss in a framework-free code base:

- **Stored XSS through attribute quotes.** The HTML-escaping helpers escaped `& < >` but not quotes, while their output was also used inside attributes (`value="…"`, `aria-label="…"`). A contact name containing `"` could break out of the attribute and add an event handler. Fixed by escaping quotes and replacing a dozen per-module copies with one shared helper.
- **Logout on parallel requests.** Keycloak rotates refresh tokens. When several requests got `401` at once, each one refreshed with the same old token; the second refresh was rejected and the user was logged out. Fixed with a single-flight refresh that all waiting requests share. A related case: pages prerendered by the browser must not refresh tokens in the background, so the timer starts only once the page is actually shown.
- **Lost deletions with undo.** Two deletions in a row cancelled the first one's timer, and leaving the page during the undo window dropped the request. Now a new deletion commits the previous one, and leaving the page sends the pending delete with `keepalive`.

The audit also confirmed the overall choice: a vanilla multi-page app fits the product, and the effort goes into shared helpers, linting and e2e checks rather than a rewrite.
