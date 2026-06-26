# Rockfile — портфолио / showcase

> **A personal contact and card-making system inspired by the Rockefeller card index, powered by AI.**

![Python](https://img.shields.io/static/v1?label=Python&message=3.12&logo=python&logoColor=white&labelColor=3776AB&color=6A737D&style=for-the-badge)
![FastAPI](https://img.shields.io/static/v1?label=FastAPI&message=0.128&logo=fastapi&logoColor=white&labelColor=009688&color=6A737D&style=for-the-badge)
![Pydantic](https://img.shields.io/static/v1?label=Pydantic&message=v2&logo=pydantic&logoColor=white&labelColor=E92063&color=6A737D&style=for-the-badge)
![SQLAlchemy](https://img.shields.io/static/v1?label=SQLAlchemy&message=2.0&logo=sqlalchemy&logoColor=white&labelColor=D71F00&color=6A737D&style=for-the-badge)
![PostgreSQL](https://img.shields.io/static/v1?label=PostgreSQL&message=16&logo=postgresql&logoColor=white&labelColor=4169E1&color=6A737D&style=for-the-badge)  
![Docker](https://img.shields.io/static/v1?label=Docker&message=Compose&logo=docker&logoColor=white&labelColor=2496ED&color=6A737D&style=for-the-badge)
![Keycloak](https://img.shields.io/static/v1?label=Keycloak&message=OIDC&logo=keycloak&logoColor=white&labelColor=5B68A3&color=6A737D&style=for-the-badge)
![LangGraph](https://img.shields.io/static/v1?label=LangGraph&message=agents&labelColor=8e4c34&logoColor=white&color=6A737D&style=for-the-badge)
![AWS](https://img.shields.io/static/v1?label=AWS&message=EC2%20%2B%20RDS&logo=amazonaws&logoColor=white&labelColor=232F3E&color=6A737D&style=for-the-badge)
![Caddy](https://img.shields.io/static/v1?label=Caddy&message=auto-HTTPS&logo=caddy&logoColor=white&labelColor=1F88C0&color=6A737D&style=for-the-badge)
![GitHub Actions](https://img.shields.io/static/v1?label=CI%2FCD&message=GitHub%20Actions&logo=githubactions&logoColor=white&labelColor=2088FF&color=6A737D&style=for-the-badge)  
![Status](https://img.shields.io/static/v1?label=status&message=private%20beta&labelColor=c96c4b&logoColor=white&color=6A737D&style=for-the-badge)

**Live:** [getrockfile.com](https://getrockfile.com) · private beta — access by invite.

**Source code:** репозиторий приватный. По запросу могу выдать доступ для код-ревью.
Связь: `dmitry.v.sychev@gmail.com` · [Telegram](https://t.me/old_healer).

---

**Rockfile** (Rockefeller-style contact file) — личный «картотечный» CRM: подробные **карточки контактов**, граф **кто-с-кем-знаком**, история **взаимодействий** (встречи, звонки, заметки, обещания). Цель — иметь богатый контекст для тёплых и осмысленных follow-up'ов.

Этот репозиторий — публичная витрина проекта. Содержит документацию архитектуры, план разработки и скриншоты. Сам код проекта живёт в приватном репозитории.

## Features

- **Contact cards** — identity (name, phone, email, address), relationship type, personal block (family, birthday, notes, interests), goals & ambitions, aggregated **promises**
- **Relationships graph** — `ContactLink` between people in your file (friend, colleague, family, etc.)
- **Interaction history** — `ContactInteraction` with channel, notes, promises; list views show **last interaction** where relevant
- **Import** — vCard (`.vcf`) and CSV (Google Contacts / Outlook / RU mapping) via `POST /api/v1/contacts/import`
- **AI agents** — LangGraph flows: meeting-prep + Concierge. Cloud LLM (Groq primary + Gemini fallback via `with_fallbacks()`) or local Ollama
- **Auth** — Keycloak (JWT + OIDC), self-registration, auto-refresh, GDPR account deletion, email verification (JWT 24h, soft-block contact creation until verified)
- **Email** — SMTP (Yandex/Gmail) or Resend (HTTPS API, used in prod since ISP blocks SMTP ports), Jinja2 templates
- **Web UI** — static HTML/CSS/JS, две темы (Purple/Amber), glassmorphism, mobile-adaptive
- **Admin panel** — `/admin` со счётчиками, списком юзеров (поиск + ban/verify/delete) и логом AI-вызовов с tokens/latency/provider
- **API docs** — Swagger at `/api/docs`

## Tech stack

| Layer | Choice |
|--------|--------|
| Backend | FastAPI, Pydantic v2, pydantic-settings |
| DB | PostgreSQL 16, SQLAlchemy 2.0 async, asyncpg, Alembic |
| Auth | Keycloak (JWT / OIDC), multi-tenant `tenant_id` on data |
| Email | Resend (HTTPS API, prod) or generic SMTP, Jinja2 templates |
| Agents | LangGraph + FastMCP, cloud LLMs (Groq → Gemini fallback) or local Ollama |
| Frontend | Static HTML/CSS/JS, served by FastAPI |
| Infra (prod) | AWS EC2 + RDS (Free Tier, eu-central-1), Caddy reverse-proxy + Let's Encrypt, domain via Porkbun |
| CI/CD | GitHub Actions — pytest + docker build + smoke on PR; auto-deploy via SSH on push to `master`; post-deploy smoke + auto-rollback |

## Screenshots

<!--
Подкинуть PNG'шки в docs/screenshots/ и заменить ссылки ниже.
Рекомендуемые: landing.png, contacts-list.png, contact-detail.png,
ai-agent.png, admin-panel.png, mobile-burger.png.
-->

| Главная (landing) | Список контактов |
|---|---|
| *(скрин будет добавлен)* | *(скрин будет добавлен)* |

| Карточка контакта | AI-агент (Concierge) |
|---|---|
| *(скрин будет добавлен)* | *(скрин будет добавлен)* |

| Admin-панель | Mobile |
|---|---|
| *(скрин будет добавлен)* | *(скрин будет добавлен)* |

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — domain model, layers, product directions
- [`docs/DEVELOPMENT_PLAN.md`](docs/DEVELOPMENT_PLAN.md) — phased checklist with progress column (от 0 до Phase 7.9 Admin panel)
- [`docs/AGENTS.md`](docs/AGENTS.md) — AI agents, MCP vs local mode, meeting prep
- [`docs/PRE_BETA_ROADMAP.md`](docs/PRE_BETA_ROADMAP.md) — приоритеты до beta-релиза

Developer-facing docs are partly in Russian; этот README по большей части на английском для нейтральной поверхности.

## Что сделано (highlights)

- ✅ Domain: contacts / links / interactions / promises (with completion tracking)
- ✅ Full-text search + filters (last contact, relationship type, birthday soon)
- ✅ AI: meeting-prep agent + Concierge (LangGraph), cloud LLM with provider fallback
- ✅ Auth: Keycloak, self-registration, auto-refresh, logout, account deletion, email verification, password reset
- ✅ Email: SMTP + Resend (HTTPS API) with provider switch
- ✅ Import: vCard + CSV with synonym-based column mapping
- ✅ UI: Purple/Soft Violet + Amber темы, glassmorphism, demo-data seeding on registration
- ✅ Mobile-adaptive UI (≤768px): burger drawer, unified compact forms, 44px tap targets
- ✅ Production deploy on AWS: EC2 + RDS + Elastic IP, Caddy reverse-proxy with auto-HTTPS (Let's Encrypt), domain via Porkbun, Keycloak under `/auth/*`
- ✅ CI/CD: GitHub Actions — PR validation (pytest + compose-validate + build & smoke image), auto-deploy via SSH on push to `master`, post-deploy smoke с auto-rollback на failure, Step Summary alerts + email notifications
- ✅ Admin panel: статистика, список юзеров с поиском/пагинацией, ban/verify-email/delete actions, лог AI-вызовов (provider, tokens, latency)
- ✅ Security: TruffleHog secrets scan, Dependabot, Branch protection

## What's next

- Telegram bot (Phase 9)
- PostHog Cloud — funnel events (signup, first_contact_added, first_ai_call)
- In-UI feedback widget
- Export user data (`GET /api/v1/export`)

## License / usage

Proprietary — All Rights Reserved. The source is visible for viewing and reference only; no rights are granted to use, copy, modify, or run this software. See [`LICENSE`](LICENSE) for the full text.

Licensing inquiries: dmitry.v.sychev@gmail.com.  
Ideas or questions: [Telegram](https://t.me/old_healer).
