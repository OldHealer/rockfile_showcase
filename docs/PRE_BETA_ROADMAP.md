# Pre-Beta Roadmap — путь к фокус-группе

> **Статус:** рабочий черновик, не для коммита в git.
> Цель — довести Rockfile до состояния, когда можно отдать продукт 20–50 тестерам и собрать вменяемый фидбек.

---

## ✅ Сделано

| Фаза | Что | Коммит |
|---|---|---|
| 5.5a | **Cloud LLM:** Groq primary + Gemini fallback. `with_fallbacks()`, CallbackHandler для трекинга модели в логах. Конфиг через `AGENT__LLM_PROVIDER` + CSV `AGENT__LLM_FALLBACKS` | (см. историю) |
| 4.6 | **Auth UX:** auto-refresh access token по `exp`, logout (KC SSO invalidate), user-info в header, reactive 401-handling | `77bdc1c` |
| 4.7 | **UI Polish:** Purple + Amber темы (toggle), Inter, glassmorphism, anti-FOUC inline-script, header sticky blur | `9547f5b` |
| 7.3a | **Импорт vCard + CSV:** Google/Outlook/RU mapping, авто-кодировка (utf-8 / cp1251), авто-разделитель, skip-dup, лимит 200, отдельная `/import-help.html` | `11d9ab3` |
| 7.6 | **Demo-data при регистрации:** флаг `load_demo` → 10 контактов, кнопка «удалить демо» одной нажимкой | (см. историю) |
| 7.7 | **Удаление аккаунта (GDPR):** KC delete + каскад БД, подтверждение email-ом, 204 | `40a038b` |
| 7.5.1 | **Email sending:** `email_service.send_email()` с диспатчем SMTP↔Resend (`EMAIL__PROVIDER`). Smoke-эндпоинт `/auth/test-email`. 15 тестов | `6b5b67f` |
| 7.5.2 | **Email verification:** свой JWT-flow HS256 TTL 24h, `GET /auth/verify-email`, `POST /auth/resend-verify-email` (rate-limit 60s), `email_verified` в `/me`. `require_verified_email` блокирует POST `/contacts` и `/contacts/import` → 403. UI: страница verify-email.html (с tryRefreshTokens), жёлтый баннер на /contacts. 23 теста | `08a9013` |
| 7.5.3 | **Password reset:** JWT TTL 1h. `POST /auth/forgot-password` (anti-enumeration: всегда 204, rate-limit 3/час). `POST /auth/reset-password` (200/400/410/404/409, cross-typ блок). KC admin `set_password()`. UI: `forgot-password.html` + `reset-password.html`, ссылка «Забыли пароль?» на login. Единый `.auth-status` CSS-паттерн. 15 тестов | следующий |
| infra | **Resend domain verified:** `getrockfile.com` куплен на Porkbun, DKIM/SPF/DMARC настроены, `RESEND__FROM_EMAIL=noreply@getrockfile.com` — письма летят на любые адреса (раньше Resend free tier пускал только на email Resend-аккаунта) | — |
| infra | **CI:** GitHub Actions pytest workflow + PR template + Dependabot. Push в dev запускает прогон. Branch protection включается через UI | `7e93fae` |

---

## 🟢 В работе / следующее

### Phase 7.5.2 — Email verification (~1 день)
Свой flow на JWT 24h (не Keycloak built-in — KC шлёт SMTP, не HTTP).

- `email_verification_service.py`: `generate_verify_token()` (HS256, `config.token.secret_key`), `decode_verify_token()`, `send_verification_email()`.
- `keycloak_admin_service.set_email_verified(sub, value)` через `PUT /admin/realms/.../users/{id}`.
- `GET /api/v1/auth/verify-email?token=...` — декодирует, ставит `emailVerified=true` в KC.
- `POST /api/v1/auth/resend-verify-email` (authed, rate limit 1/60s).
- При регистрации — best-effort вызов `send_verification_email` (warning на ошибку, регистрация не падает).
- UI: `sources/web/verify-email.html` (страница-обработчик), баннер в `contacts.html` с кнопкой «отправить заново».
- Edge cases: токен протух → 410, email сменился → 400, уже verified → idempotent 200.
- Доступ **не** блокируем (soft warning) — для фокус-группы достаточно.

### Phase 7.5.3 — Password reset (~1 день)
- `POST /api/v1/auth/forgot-password` (без авторизации): принимает email → если есть юзер, шлём JWT-токен с `typ=reset`, TTL 1h. Возвращаем 204 всегда (anti-enumeration).
- `POST /api/v1/auth/reset-password`: `{token, new_password}` → декодируем, через KC admin API ставим новый пароль (`PUT /users/{id}/reset-password`).
- UI: ссылка «Забыли пароль?» на login → форма ввода email → `reset-password.html` со страницей `?token=...`.
- Rate limit: на forgot-password — 3/час на email.

### Phase 7.8 — Архивы взаимодействий и обещаний на странице контакта (~1 день)
**Зачем:** сейчас все взаимодействия и обещания выводятся одним полотном — у активного контакта быстро превращается в простыню, форма ввода уезжает вниз.

- **Взаимодействия:** на `/contact.html` показываем **только 5 последних**, ниже — кнопка-ссылка «📋 Архив взаимодействий (N)». Клик → отдельная страница `/contact-interactions.html?contact_id=...` с полным списком + фильтрами (тип, период).
- **Обещания:** аналогично — в карточке «Планы и обещания» показываем **только активные** (≤5, отсортированы по дедлайну). Ниже — «📋 Архив обещаний (N выполнено)». Клик → `/contact-promises.html?contact_id=...` со всеми (активные + выполненные + просроченные) и фильтрами.
- **Учёт выполненных обещаний** — вариант **C (гибрид)**:
  - В модели уже есть `promises[].completed_at` (`null` = активно). API уже умеет `PATCH .../promises/{id}/complete`.
  - На карточке контакта порядок:
    1. **Активные** (включая просроченные, с warning-бэйджем) — каждое с кнопкой «✓ Выполнено» и «✗ Отменить».
    2. **Недавно выполнено** — секция с **3 последними за 7 дней** (зачёркнуты, дата).
    3. **Ссылка «📋 Архив (N выполнено) →»** на отдельную страницу со всеми (фильтры: активные / выполненные / просроченные / все).
  - На странице архива — возможность «вернуть в активные» (`completed_at = null`) если случайно отметил.
- **Метрика «keep-rate»** — добавляем, но **с порогом 30**:
  - В `/stats` показываем процент выполненных обещаний, **только** если у юзера ≥ 30 закрытых обещаний (`completed_at IS NOT NULL`).
  - До порога — placeholder «Метрика появится после 30 выполненных обещаний (сейчас N/30)». Иначе на маленькой выборке цифра врёт и демотивирует.
  - Формула простая: `completed / (completed + cancelled)` (без учёта активных). Cancelled — обещание было закрыто через кнопку «✗ Отменить».
- Backend: новые `GET /api/v1/contacts/{id}/interactions?limit=N&offset=...` и `GET /api/v1/contacts/{id}/promises?status=open|completed|overdue|all` (с пагинацией). UI: 2 новые страницы, минимальный CSS, переиспользуем существующие рендереры.

### Phase 8.0 — Mobile-responsive аудит (~2–3 дня)
- Sidebar `/contacts.html` → bottom-sheet или таб на <768px.
- Формы вертикально, поля 16px (чтобы iOS не зумил), кнопки 44×44.
- Header — burger меню вместо нав-линков.
- Тест на iPhone Safari + Android Chrome (не только DevTools).
- Touch-friendly modal close (свайп вниз).

### Phase 9.0 — Telegram bot (~5–7 дней)
**Минимум для focus group:** триггеры наружу, без них продукт = «открыл и забыл».

- Bot на `aiogram` или `python-telegram-bot`.
- Привязка через deep-link: `/start <one_time_token>` → matching с AppUser, сохраняем `tg_chat_id`.
- Утренний дайджест в 9:00 (cron / APScheduler): ДР через 1/7/30 дней, просроченные обещания.
- Quick capture: `/добавить Иван Петров +79991234567` → создание контакта.
- **Без Mini App** — пока просто bot.

### Phase 9.5 — Git/GitHub инфраструктура и PR-flow (~0.5 дня)
**Перед** Phase 10 — иметь нормальный flow `dev → master через PR` с CI и хотя бы базовым автоматическим ревью.
- Создать приватный репо на GitHub, push текущей ветки.
- Подключить **Branch protection** на master (require PR, require CI green).
- Завести `.github/workflows/test.yml` (pytest + postgres service).
- Шаблон PR (`.github/pull_request_template.md`) + Dependabot.
- **Sourcery** (бесплатно для приватных репо на персональном тарифе) для авто-ревью.
- Подробные инструкции и сравнение AI-ревьюеров — в `docs/PR_REVIEW_STACK.md`.

### Phase 10 — Деплой VPS + HTTPS + домен (~2–3 дня)
- VPS: Timeweb / Selectel (RU, для платежей) или Hetzner (EU, дешевле).
- Caddy для авто-HTTPS (Let's Encrypt) или nginx + certbot.
- Свой домен (куплен: **getrockfile.com** через Porkbun).
- Cron бэкапа Postgres → S3 (Selectel Object Storage / Backblaze).
- Sentry self-hosted или GlitchTip — для отлова прод-ошибок.
- Resend-домен уже подтверждён, FROM_EMAIL=noreply@getrockfile.com.

---

## 🟡 Сильно повышает шансы

### Phase 11 — Аналитика поведения (~1–2 дня)
- PostHog Cloud free (1M events/мес) или self-hosted.
- События: `signup`, `first_contact_added`, `first_interaction_added`, `first_ai_call`, `import_success`, `agent_error`, `page_view`.
- Понять где юзеры реально теряются — фидбек словами этого не даёт.

### Phase 12 — Feedback widget в UI (~1 день)
- Кнопка «💬 Фидбек» внизу справа → форма Tally / прямая ссылка в TG.
- Без этого юзеры ленятся писать в личку.

### Phase 13 — Экспорт данных (~1 день)
- `GET /api/v1/export` — JSON dump всех контактов/взаимодействий/связей юзера.
- Кнопка «Скачать мои данные» в /account.
- Важно для доверия: «мои данные не заложники».

---

## 🟢 НЕ нужно сейчас (после фокус-группы)

- Биллинг (фокус-группа бесплатная)
- Telegram Mini App (web + bot достаточно)
- Нативное мобильное приложение (responsive web)
- Команды/шеринг
- Теги/категории (можно добавить после фидбека)
- Реминдеры через планировщик (через TG-бот пока)
- BYOK для AI
- Другие LLM-провайдеры (DeepSeek/OpenAI/Anthropic — для фокус-группы хватит Groq+Gemini)

---

## Сводная таблица оставшегося

| Приоритет | Задача | Дней | Состояние |
|---|---|---|---|
| ✅ | Phase 7.5.2 — Email verification | 1 | сделано (08a9013) |
| ✅ | Phase 7.5.3 — Password reset | 1 | сделано (a616443) |
| ✅ | Phase 7.8 — Архивы взаимодействий и обещаний | 1 | сделано + UX-полировка карточек |
| ✅ | Phase 9.5 — Git/GitHub + CI + PR-review | 0.5 | сделано (CI + Dependabot + TruffleHog + Branch protection) |
| 🟢 | Phase 8 — Mobile-responsive аудит | 2–3 | |
| 🟢 | Phase 9 — Telegram bot + дайджест | 5–7 | |
| 🟢 | Phase 10 — Deploy VPS + HTTPS + домен | 2–3 | домен куплен |
| 🟡 | Phase 11 — PostHog + Sentry | 1–2 | |
| 🟡 | Phase 12 — Feedback widget | 1 | |
| 🟡 | Phase 13 — Export данных | 1 | |

**Итого осталось:** ~14–19 рабочих вечеров. При 2–3 вечера/неделю — **~5–9 календарных недель**.

---

## После Pre-Beta

### Focus group (4–6 недель)
- Рекрут 20–50 тестеров через личную сеть + 1–2 TG-канала.
- Структурированный фидбек каждые 2 недели (Tally form + интервью с 5).
- Метрики: D1/D7 retention, % сделавших импорт, % использовавших AI, NPS.

### Public launch
- Биллинг (ЮKassa / Lava).
- Лендинг с waitlist → платными планами.
- Telegram Mini App.
- Реминдеры через планировщик.
