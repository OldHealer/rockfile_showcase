# Roadmap

Rockfile is in private beta at [getrockfile.com](https://getrockfile.com). This page summarises what has been built and what comes next.

## Built

| Period | Milestone |
|---|---|
| Apr 2026 | Core: FastAPI + async SQLAlchemy + Keycloak, contacts CRUD, relationship links, interactions, promises with direction, web UI, full-text search, LangGraph agents (meeting prep, Concierge) on top of MCP tools |
| May 2026 | Cloud LLMs with fallback, LLM usage logging, PII-safe agent logs, email (verification, password reset), vCard / CSV import, demo data, account deletion |
| Jun 2026 | First production deploy with auto-HTTPS; CI: tests, image build + migrations + smoke on every PR, TruffleHog; auto-deploy with post-deploy smoke and automatic rollback; mobile layout; admin panel with AI call log; invite-only registration |
| Jun - Jul 2026 | UX pass (confirm dialogs, skeletons, empty states, shortcuts, feedback button); access periods; roadmap stored in the database; six-provider LLM chain verified end-to-end |
| Jul 2026 | Full redesign. Promises moved into a table of their own; checklist notes synced with promises; Today view; command palette; grounded sources in Concierge; new agents screen; mobile bottom navigation and PWA manifest; three themes with contrast fixes |
| Sep 2026 | Frontend tech debt: stored-XSS fix, shared API client and escaping, ESLint / Stylelint / Prettier, automatic cache busting, Playwright smoke suite, CSP moved from Report-Only to enforced, accessibility safety nets (`focus-visible`, `prefers-reduced-motion`) |
| Oct 2026 | Production moved from AWS to a Hetzner VPS with nightly backups and reproducible builds; frontend audit fixes (single-flight token refresh, reliable undo, double-submit guards); complete English UI with server-side translation; custom date picker; new landing page |

## Next

1. **Telegram bot.** A morning digest of due promises and birthdays, contact search and quick capture of interactions right after a meeting. The design is settled:
   - aiogram 3 over a webhook, a separate `bot` container calling the same domain services as the API;
   - accounts linked through a one-time token in a deep link; tenant isolation through a single `chat → user` resolver;
   - digest scheduled in each user's time zone, idempotent through a delivery log.
2. **Data export** - everything a user has stored, in an open format.
3. **Product analytics** - sign-up funnel and D1 / D7 / D30 retention by cohort, where "active" means creating data rather than just opening the app.
4. **Paid beta** - founder pricing for early users, with the decision threshold fixed before the experiment starts.

## Later

- Off-site copies of the nightly backups
- Access tokens in `httpOnly` cookies instead of browser storage
- Service worker, app icons, SEO / Open Graph tags
- Background job queue for long-running agent calls
- Dunbar layers for contacts, calendar integration, tags and reminders
- Clean-up of long-inactive accounts with advance notice
- Sending an assistant's answer to email or Telegram
