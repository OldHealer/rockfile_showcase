# План разработки: Rockfile

## Обзор

План разбит на фазы от MVP до полномасштабного продукта. Каждая фаза завершается рабочим инкрементом.

**Условные обозначения:** ✅ выполнено · 🚧 частично · ❌ не начато

---

## Фаза 0: Подготовка инфраструктуры ✅

| #   | Задача                                              | Результат                                                | Статус |
| --- | --------------------------------------------------- | -------------------------------------------------------- | ------ |
| 0.1 | Настроить Alembic для async SQLAlchemy              | `alembic init`, конфиг под asyncpg                       | ✅     |
| 0.2 | Создать первую миграцию по текущим моделям          | `contact_cards`, `contact_links`, `contact_interactions` | ✅     |
| 0.3 | Добавить в pyproject: pytest, pytest-asyncio, httpx | Готовность к тестам                                      | ✅     |
| 0.4 | docker-compose с PostgreSQL и Keycloak              | Локальный запуск одной командой                          | ✅     |

---

## Фаза 1: Аутентификация и авторизация (Keycloak + OIDC) ✅

| #   | Задача                                          | Результат                          | Статус |
| --- | ----------------------------------------------- | ---------------------------------- | ------ |
| 1.1 | Развернуть Keycloak локально                    | Доступен admin UI (порт 8282)      | ✅     |
| 1.2 | Создать Realm, Client, Role                     | Базовая конфигурация OIDC          | ✅     |
| 1.3 | Включить self‑registration                      | Пользователь может создать аккаунт | ✅     |
| 1.4 | Настроить маппинг claims (`tenant_id`, `roles`) | JWT содержит нужные поля           | ✅     |
| 1.5 | Добавить проверку JWT в FastAPI                 | Защита эндпоинтов                  | ✅     |
| 1.6 | Реализовать создание tenant при первом входе    | Self‑service, мультитенантность    | ✅     |
| 1.7 | Изоляция данных по `tenant_id`                  | Фильтрация во всех сервисах        | ✅     |

---

## Фаза 2: MVP API (Карточки и базовый CRUD) ✅

| #     | Задача                                          | Результат                                  | Статус |
| ----- | ----------------------------------------------- | ------------------------------------------ | ------ |
| 2.1.1 | `ContactCardCreate/Update/Response`             | Pydantic-схемы                             | ✅     |
| 2.1.2 | `ContactCardListResponse` с пагинацией          | `items`, `total`, `page`, `per_page`       | ✅     |
| 2.2.1 | `GET /api/v1/contacts` с пагинацией и сортировкой | `page`, `per_page`, `sort`               | ✅     |
| 2.2.2 | `POST /api/v1/contacts`                         | Валидация, возврат созданной карточки      | ✅     |
| 2.2.3 | `GET /api/v1/contacts/{id}`                     | Карточка по ID, 404 при отсутствии         | ✅     |
| 2.2.4 | `PATCH /api/v1/contacts/{id}`                   | Частичное обновление                       | ✅     |
| 2.2.5 | `DELETE /api/v1/contacts/{id}`                  | Удаление контакта                          | ✅     |
| 2.3.1 | Сервисный слой `ContactService`                 | Централизация логики                       | ✅     |
| 2.4.1 | Подключить роутеры, DI для сессии БД            | Маршруты доступны, `get_db()` через `yield`| ✅     |
| 2.4.2 | Глобальный обработчик ошибок                    | 404, 422, 500 в едином формате             | ✅     |

---

## Фаза 3: Связи и взаимодействия ✅

| #     | Задача                                                        | Результат                                            | Статус |
| ----- | ------------------------------------------------------------- | ---------------------------------------------------- | ------ |
| 3.1.1 | Схемы `ContactLinkCreate/Update/Response`                     | Связи между контактами                               | ✅     |
| 3.1.2 | Схемы `ContactInteractionCreate/Update/Response`              | Взаимодействия                                       | ✅     |
| 3.2.1 | `GET/POST /api/v1/contacts/{id}/links`                        | Список и добавление связей                           | ✅     |
| 3.2.2 | `PATCH/DELETE /api/v1/contacts/{id}/links/{link_id}`          | Редактирование и удаление связи                      | ✅     |
| 3.2.4 | `GET/POST /api/v1/contacts/{id}/interactions`                 | История и добавление взаимодействий                  | ✅     |
| 3.2.5 | `PATCH/DELETE /api/v1/contacts/{id}/interactions/{id}`        | Редактирование и удаление                            | ✅     |
| 3.3.1 | Обновление `last_contact_at` при добавлении Interaction       | Автоматическая актуализация карточки                 | ✅     |
| 3.3.2 | Агрегация `promises` из Interaction → ContactCard             | Обещания с direction (mine/theirs), interaction_id   | ✅     |
| 3.3.3 | `POST /contacts/{id}/promises/{promise_id}/complete`          | Отметка выполнения обещания                          | ✅     |
| 3.3.4 | `GET /contacts/{id}` подгружает links и interactions          | Полная карточка                                      | ✅     |

---

## Фаза 4: Веб-фронтенд ✅

| #   | Задача                                        | Результат                                                 | Статус |
| --- | --------------------------------------------- | --------------------------------------------------------- | ------ |
| 4.1 | HTML-страницы, CSS-стили                      | Главная, вход, список контактов, карточка контакта        | ✅     |
| 4.2 | JavaScript для работы с API (fetch, ES modules)| CRUD без перезагрузки страницы                           | ✅     |
| 4.3 | Авторизация через Keycloak в UI               | JWT в localStorage, редирект при 401                     | ✅     |
| 4.4 | Форма взаимодействий с обещаниями (mine/theirs)| Отслеживание направления обещаний                        | ✅     |
| 4.5 | Форма связей с редактированием и удалением    | CRUD для ContactLink прямо со страницы                   | ✅     |
| 4.6 | Тёмная/светлая тема на всех страницах         | Anti-FOUC, localStorage, toggle во всех nav              | ✅     |
| 4.7 | Тост-уведомления вместо сырого JSON ошибок    | Парсинг 422, читаемые сообщения                          | ✅     |
| 4.8 | Страница входа: вкладки Вход/Регистрация      | Переключение без перезагрузки                            | ✅     |
| 4.9 | Поиск контактов в UI                          | Серверный поиск с дебаунсом, не ограничен 50 записями    | ✅     |

---

---

## Фаза 4.5: Security & Hardening ✅

Проведено полное ревью безопасности и качества кода.

| #     | Задача                                                   | Результат                                                              | Статус |
| ----- | -------------------------------------------------------- | ---------------------------------------------------------------------- | ------ |
| 4.5.1 | Tenant isolation: `GET/PATCH/DELETE /contacts/{id}`      | `get_contact` фильтрует по `tenant_id`, 404 при чужом UUID             | ✅     |
| 4.5.2 | Tenant isolation: `GET /contacts/{id}/links`             | `list_links_for_contact` проверяет tenant через `_ensure_...`          | ✅     |
| 4.5.3 | `UniqueConstraint` на `ContactLink` + Alembic            | Нет дублей пар (с нормализацией undirected), 409 на конфликт           | ✅     |
| 4.5.4 | Убрать дефолтные пароли из `docker-compose.yml`          | `${VAR:?message}` вместо `:-default`, создан `.env.example`           | ✅     |
| 4.5.5 | `lazy="raise"` на всех ORM-коллекциях                    | Убраны лишние SELECT на каждый запрос (4–6 штук)                       | ✅     |
| 4.5.6 | `max_length` на Pydantic-схемах                          | Соответствие `String(N)` в моделях; validation на входе                | ✅     |
| 4.5.7 | `LOCAL_DEV` из переменной окружения                      | Убран захардкоженный `False` в `settings.py`                           | ✅     |
| 4.5.8 | Таймауты в агенте (per-call + total)                     | `ChatOllama(timeout=300)`, `asyncio.wait_for(timeout=720)`             | ✅     |
| 4.5.9 | Дедупликация auth-утилит в JS                            | `getToken/applyTokenFromHash/handleUnauthorized` вынесены в `ui.js`   | ✅     |
| 4.5.10| Alembic startup: thread executor + URL object            | Работает из async lifespan, не ломается на `%` в паролях               | ✅     |

---

## Фаза 4.7: UI Polish — lite-редизайн (premium SaaS look) ✅

Lite-редизайн в стиле premium SaaS (вдохновение — brain.fm): тёмная градиентная база, неон-акцент, glassmorphism, современная типографика. Без переписывания DOM/JS/логики — только CSS + загрузка одного шрифта.

| #     | Задача                                                | Результат                                                                                                  | Статус |
| ----- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------ |
| 4.7.1 | Палитра + тёмная база                                 | CSS-переменные: тёмный фон `#0e0a1f / #1a1330`, неон-акцент (определить — синий/фиолетовый/циан), пересмотр светлой темы. Все цвета через `var(--*)` | ❌     |
| 4.7.2 | Типографика                                           | Inter / Plus Jakarta Sans через Google Fonts (`<link rel=preconnect>` + 1 шрифт). Шкала h1-h6, line-height. Применить ко всем страницам | ❌     |
| 4.7.3 | Hero на index.html                                    | Gradient-фон (radial/conic), крупный заголовок, новый CTA с glow. Без иллюстраций — только CSS                                  | ❌     |
| 4.7.4 | Glassmorphism для card                                | Применить `backdrop-filter: blur(20px)` + тонкие border'ы + лёгкий box-shadow glow на: sidebar widgets, AI-карточки, modal, login-карточка | ❌     |
| 4.7.5 | Header: sticky + тонкая граница                       | Убрать плотный фон, добавить `border-bottom`, sticky-позиционирование. Воздух наверху страницы | ❌     |
| 4.7.6 | Кнопки/инпуты polish                                  | Увеличенный border-radius, цельные тени, focus-state в неоне (без outline default), accent-color на чекбоксах | ❌     |
| 4.7.7 | Skeletons + fade-in карточек                          | CSS-анимация скелетонов для контактов/sidebar widgets. `@keyframes fade-up` для появления карточек | ❌     |
| 4.7.8 | Mobile + cross-browser проверка                       | Тёмная/светлая на всех страницах, breakpoints, тест на iPhone/Android при наличии              | ❌     |

**~6 рабочих дней (12-18 вечеров).** Перед Phase 7.3a (vCard import) — потому что новые UI-элементы (импорт-форма с превью) лучше делать сразу в новом стиле.

**Принятые ограничения:**
- Без сборщика. Чистый CSS, можно использовать кастомные свойства/CSS nesting (поддержка во всех современных браузерах с 2023).
- Без иллюстраций — только градиенты/blur. Иллюстратор/иконки в Phase 4.7b если захочется позже.
- Без сложных анимаций (parallax, particles, Lottie). Только CSS transitions/keyframes.
- Структура HTML не меняется — только классы/стили. Layout остаётся.

---

## Фаза 4.6: Auth UX — auto-refresh и logout ✅

Доработки auth, без которых активные юзеры быстро выкидываются на логин (access token живёт 5 мин по умолчанию, refresh во фронте нет).

| #     | Задача                                                | Результат                                                                                                                                | Статус |
| ----- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 4.6.1 | Backend endpoint `POST /api/v1/auth/refresh`          | Принимает `refresh_token`, дергает Keycloak token endpoint с `grant_type=refresh_token`, возвращает новые `access_token` + `refresh_token` | ✅     |
| 4.6.2 | Frontend: автообновление токена                       | `scheduleAutoRefresh()` в ui.js: декодирует JWT exp, ставит setTimeout на (exp - 60s), обновляет оба токена. Запуск на DOMContentLoaded всех страниц | ✅     |
| 4.6.3 | Backend endpoint `POST /api/v1/auth/logout`           | Дергает Keycloak `/logout` с refresh_token чтобы инвалидировать SSO-сессию (нельзя просто удалить токен на клиенте — refresh останется валидным). 204, идемпотентно. Кнопка «Выйти» в header | ✅     |
| 4.6.4 | Подкрутить TTL в realm (быстрый фикс)                  | Опционально: `accessTokenLifespan=3600`, `ssoSessionIdle=86400`. При работающем auto-refresh не критично                                  | ⏸     |

---

## Фаза 5: AI-агенты ✅

| #   | Задача                                              | Результат                                            | Статус |
| --- | --------------------------------------------------- | ---------------------------------------------------- | ------ |
| 5.1 | LangGraph агент `prepare_meeting_agent`             | Граф: get_history → summarize → generate → format    | ✅     |
| 5.2 | FastMCP сервер + инструмент `contacts_get`          | MCP-режим получения данных                           | ✅     |
| 5.3 | Локальный режим (без MCP) через сервисный слой      | Переключение через `AGENT__MODE`                     | ✅     |
| 5.4 | `POST /api/v1/agents/prepare-meeting`               | Эндпоинт вызова агента, результат в UI               | ✅     |
| 5.5 | Автодополнение контакта в форме агента (UI)         | Поиск по имени, выбор из списка                      | ✅     |
| 5.6 | `GET /api/v1/promises` — агрегированный список обещаний | Параметры: `open`, `direction`; 7 тестов         | ✅     |
| 5.7 | MCP tools `contacts_list_tool` + `promises_list_tool`| В `mcp_app.py`; Python-функции в `contacts_tools.py` | ✅     |
| 5.8 | Агент «Concierge» (`concierge_agent.py`)            | LangGraph граф: birthdays / promises / matchmaker / unknown; `POST /api/v1/agents/concierge` | ✅     |
| 5.9 | UI-карточка Concierge на странице контактов         | Форма с textarea, вывод markdown-ответа              | ✅     |

---

## Фаза 5.5a: Cloud LLM (focus-group блокер) ✅

Уход от локального Ollama к cloud-провайдерам, in-process fallback между бесплатными tier'ами. Без queue — синхронный flow остаётся, но Groq отвечает за 5-10 сек вместо 30-60 сек на Ollama.

| #      | Задача                                                | Результат                                                                                                                                                 | Статус |
| ------ | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 5.5a.1 | Зависимости                                            | `pyproject.toml`: `langchain-groq ^0.3`, `langchain-anthropic ^0.3`, `langchain-openai ^0.3`, `langchain-google-genai ^2.0`                                | ✅     |
| 5.5a.2 | LLM factory                                            | `sources/agents/llm_factory.py` — единая `build_llm()`, ленивые билдеры по провайдерам, кеш instance на уровне модуля                                      | ✅     |
| 5.5a.3 | Refactor `AgentSettings`                                | Общие `llm_temperature/llm_num_predict/llm_timeout`. Провайдер-специфичные `*_api_key: SecretStr`, `*_model`. `llm_provider` + `llm_fallbacks` (CSV)        | ✅     |
| 5.5a.4 | Refactor агентов                                       | `prepare_meeting_agent.py` и `concierge_agent.py` — заменён `build_default_ollama_llm`/`_get_llm` на `build_llm()`. Удалено ~25 строк дубликата кеша       | ✅     |
| 5.5a.5 | Multi-provider fallback in-process                     | LangChain `with_fallbacks()`: `primary.with_fallbacks(fallback_llms)`. Провайдеры без креденшелов пропускаются                                              | ✅     |
| 5.5a.6 | Token usage в audit log                                | Отложено: будет в Phase 5.5b вместе с job queue                                                                                                             | ⏸     |
| 5.5a.7 | `.env.example`                                         | Новые ключи: `AGENT__LLM_PROVIDER`, `AGENT__LLM_FALLBACKS`, `AGENT__{GROQ,GEMINI,DEEPSEEK,OPENAI,ANTHROPIC}_API_KEY`                                       | ✅     |
| 5.5a.8 | Тесты                                                  | Существующие тесты узлов инжектят LLM как MagicMock через DI — рефактор прозрачен. Сообщения об ошибках обновлены                                          | ✅     |
| 5.5a.9 | CHANGELOG                                              | Запись добавлена в `## [Unreleased]`                                                                                                                        | ✅     |

---

## Фаза 5.5b: Job Queue + persistence (после focus-group) ❌

Уход от блокирующих HTTP-запросов, сохранение истории запусков агентов, готовность к масштабу.

| #       | Задача                                                | Результат                                                                                                                          | Статус |
| ------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 5.5b.1  | Redis + arq                                            | Контейнер `redis` в docker-compose с AOF persistence; зависимость `arq ^0.26`                                                       | ❌     |
| 5.5b.2  | Таблица `agent_jobs` + Alembic                         | UUID PK, `tenant_id`, `created_by_user_id`, `agent_type`, `status`, `payload jsonb`, `result jsonb`, `error_message`, `provider_used`, `input_tokens`, `output_tokens`, timestamps. Индексы по `tenant_id+status`, `created_at` | ❌     |
| 5.5b.3  | Worker процесс                                          | `sources/worker.py` с `WorkerSettings.functions=[run_prepare_meeting, run_concierge]`, `job_timeout=900`. Отдельный сервис `worker:` в docker-compose | ❌     |
| 5.5b.4  | `jobs_service.py`                                       | CRUD над `agent_jobs`: `create_job`, `get_job`, `list_jobs`, `update_job_status`. Все с tenant filter                                | ❌     |
| 5.5b.5  | Async endpoints `/agents/*`                             | `POST /agents/prepare-meeting` и `/concierge` → создают job, enqueue в arq, возвращают `202 {job_id}`. Опц. `?sync=true` для тестов | ❌     |
| 5.5b.6  | Job status endpoints                                    | `GET /api/v1/jobs/{job_id}`, `GET /api/v1/jobs?status=...`. Tenant isolation                                                         | ❌     |
| 5.5b.7  | Migrate fallback in-process → worker                    | Перенос `invoke_with_fallback` из request handler в worker. Логика та же, переезжает                                                | ❌     |
| 5.5b.8  | Token tracking → БД                                     | Из audit log → в `agent_jobs.input_tokens/output_tokens`. Для аналитики usage                                                        | ❌     |
| 5.5b.9  | Frontend: polling                                       | UI создаёт job, спиннер, опрос `/api/v1/jobs/{id}` раз в 2 сек, отрисовка результата. Применяется к обоим агентам                    | ❌     |
| 5.5b.10 | Тесты                                                   | Integration тесты async flow (mock arq), worker fallback, jobs CRUD                                                                  | ❌     |
| 5.5b.11 | CHANGELOG                                               | Migration от sync к async; sync через `?sync=true` для backward compat                                                               | ❌     |

---

## Фаза 6: Поиск и фильтрация ✅

| #   | Задача                                     | Результат                                              | Статус |
| --- | ------------------------------------------ | ------------------------------------------------------ | ------ |
| 6.1 | Параметр `?q=` в `GET /contacts`           | Серверный поиск по `full_name`, `email` (ILIKE)        | ✅     |
| 6.2 | Фильтр `relationship_type`                 | `?relationship_type=colleague` + UI-дропдаун           | ✅     |
| 6.3 | Сортировка `sort=last_contact_at`          | NULLS LAST + UI-опция                                   | ✅     |
| 6.4 | Фильтр `last_contact_before=N`             | С кем давно не общались (N дней) + UI-дропдаун          | ✅     |
| 6.5 | Фильтр `has_birthday_soon=N`               | ДР в ближайшие N дней (ring day-of-year) + UI-дропдаун  | ✅     |
| 6.6 | Полнотекстовый поиск (tsvector + GIN)      | `GET /api/v1/search?q=` по заметкам, интересам, целям   | ✅     |
| 6.7 | Обновить UI: фильтры и серверный поиск     | Поиск не ограничен загруженными 50 записями            | ✅     |

---

## Фаза 7: Расширенные возможности ❌

| #     | Задача                                          | Результат                                                                                                  | Статус |
| ----- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------ |
| 7.1   | Теги (`ContactTag`, many-to-many с ContactCard) | Группировка по сферам, проектам                                                                            | ❌     |
| 7.2   | Напоминания (`ContactReminder`)                 | Follow-up, дни рождения                                                                                    | ❌     |
| 7.3a  | Импорт vCard + CSV (MVP, 1-2 дня)               | `POST /api/v1/contacts/import` multipart, диспатч по расширению. vCard через `vobject`, CSV — stdlib с автоопределением кодировки/разделителя и синонимами заголовков (Google Contacts, Outlook, ru/en). Skip-dup по full_name+email. Лимиты 200/2MB. UI в sidebar + отдельная страница `/import-help.html` | ✅     |
| 7.3b  | Preview + dedup перед импортом (после фидбека)  | Two-step API (`/import/preview` + `/import/commit`). UI с чекбоксами. Dedup по phone (нормализованный). Merge с существующим | ❌     |
| 7.3c  | Импорт полностью (3-4 дня)                      | vCard 4.0, CSV mapping UI (как Mailchimp), dedup по phone (нормализованный), merge existing, iPhone Share Sheet | ❌     |
| 7.3.e | Экспорт                                          | `GET /api/v1/export` — JSON dump всех данных юзера (контакты, взаимодействия, links). UI: "Скачать мои данные" | ❌     |
| 7.4   | `known_through_contact_id` на карточке          | Через кого познакомился (UI)                                                                                | ❌     |
| 7.6   | Demo-data при регистрации (0.5 дня)              | При создании tenant'а — seed 10 фейковых контактов с разными `relationship_type`, заполненными `hobbies`, `interests`, `goals`, ДР, парой взаимодействий и обещаний. Опция "загрузить демо" в UI (можно потом удалить) | ✅     |
| 7.7   | Удаление аккаунта (GDPR right to be forgotten, 1-1.5 дня) | `DELETE /api/v1/auth/account` — каскадное удаление AppUser + Tenant + все ContactCard/Interactions/Links/Promises + удаление пользователя в Keycloak (admin API). UI: кнопка в settings, confirm-форма с вводом email для подтверждения, выход из сессии после успеха. Без soft-delete — данные удаляются физически | ✅     |
| 7.8   | Архивы взаимодействий и обещаний + UX-полировка карточки контакта (1 день) | На `/contact.html` показываем 5 последних взаимодействий и 10 активных обещаний с лимитом + «недавно выполненные» (3 за 7 дней). Полные списки на `/contact-interactions.html` (фильтр по каналу) и `/contact-promises.html` (tabs все/активные/выполненные, удаление). Карточки взаимодействий с иконкой канала и счётчиком обещаний. Chip-input для обещаний в форме взаимодействия (Enter / клик «Пообещать»). Inline-действия без сброса скролла. Rename полей: «Жизненные цели», «Над чем сейчас работает» | ✅     |

---

## Фаза 7.5: Email-уведомления и восстановление доступа ✅

| #     | Задача                                                  | Результат                                                                                                                                              | Статус |
| ----- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| 7.5.1 | Интеграция отправки писем (SMTP + Resend)               | `email_service.send_email()` с диспатчем `EMAIL__PROVIDER=smtp\|resend`. SMTP через aiosmtplib (SSL 465 / STARTTLS 587 авто), Resend через HTTPS API. Jinja2-шаблоны. Smoke-эндпоинт `POST /auth/test-email`. 15 тестов | ✅ (6b5b67f) |
| 7.5.2 | Подтверждение email при регистрации                     | Свой JWT-flow HS256 TTL 24h (KC не поддерживает HTTP-провайдеры). `email_verification_service.py`. `GET /auth/verify-email?token=...` (200/400/410/404/409), `POST /auth/resend-verify-email` (rate-limit 60s). `email_verified` в `TokenPayload` и `/me`. `require_verified_email` блокирует POST /contacts и /contacts/import → 403. UI: страница `verify-email.html` (tryRefreshTokens после ✓ — баннер исчезает сразу), жёлтый баннер в `/contacts.html`, кнопка resend. KC user создаётся с `emailVerified=False`, верификация ставит true через admin API. 23 теста | ✅ (08a9013) |
| 7.5.3 | Восстановление пароля через email                       | `password_reset_service.py`: JWT HS256 TTL 1h (typ=reset, cross-typ блок с verify). `POST /auth/forgot-password` — anti-enumeration (всегда 204, rate-limit 3/час по email, swallow SMTP errors). `POST /auth/reset-password` — 200/400/410/404/409, Pydantic min_length=6. KC admin `set_password()` через PUT /users/{id}/reset-password. UI: `forgot-password.html` + `reset-password.html`, ссылка «Забыли пароль?» на login. Единый CSS-паттерн `.auth-status` для status-блоков. 15 тестов | ✅     |

---

## Фаза 8: Тесты 🚧

| #   | Задача                                              | Результат                                                                    | Статус |
| --- | --------------------------------------------------- | ---------------------------------------------------------------------------- | ------ |
| 8.1 | Интеграционные тесты contacts                       | CRUD + поиск + фильтры + tenant isolation (28 тестов)                        | ✅     |
| 8.2 | Тесты сервисного слоя (агрегация обещаний и т.п.)   | Покрыты через integration-тесты promises aggregation                         | 🚧     |
| 8.3 | Тест агента prepare-meeting (мок MCP)               | 21 тест: узлы, граф, HTTP-эндпоинт (`tests/test_prepare_meeting_agent.py`)   | ✅     |
| 8.4 | Интеграционные тесты links / interactions           | CRUD, complete promise, rebuild promises on delete, tenant isolation (20 тестов) | ✅     |
| 8.5 | Интеграционные тесты search                         | 7 тестов: поля, JSON-массивы, заметки, tenant, ранжирование, лимит           | ✅     |
| 8.6 | Интеграционные тесты auth                           | GET /me (auth/unauth), register (success/dup/validation), login (8 тестов)   | ✅     |
| 8.7 | Интеграционные тесты promises                       | 7 тестов: список, фильтры open/direction, tenant isolation                   | ✅     |
| 8.8 | Тест агента Concierge (мок tools/LLM)               | 19 тестов: узлы, граф, HTTP-эндпоинт (`tests/test_concierge_agent.py`)        | ✅     |

---

## Фаза 9: Telegram-бот ❌ (перспектива)

| #   | Задача                                         | Результат                             | Статус |
| --- | ---------------------------------------------- | ------------------------------------- | ------ |
| 9.1 | Авторизация через Telegram + привязка аккаунта | Пользователь связан с tenant          | ❌     |
| 9.2 | Поиск контактов и создание взаимодействий      | Быстрое внесение заметок после встреч | ❌     |
| 9.3 | Сценарии диалога и быстрые кнопки              | Удобный UX в чате                     | ❌     |
| 9.4 | Синхронизация через тот же API                 | Единый источник правды                | ❌     |

---

## Фаза 10: Мобильное приложение ❌ (перспектива)

| #    | Задача                                            | Результат                                        | Статус |
| ---- | ------------------------------------------------- | ------------------------------------------------ | ------ |
| 10.1 | Тот же REST API — основа для мобильного клиента   | Единый источник правды                           | ❌     |
| 10.2 | Стратегия синхронизации (онлайн-first или гибрид) | Версионирование сущностей, разрешение конфликтов | ❌     |
| 10.3 | Flutter / React Native / нативный клиент          | iOS и Android                                    | ❌     |
| 10.4 | Push-уведомления (для напоминаний от ИИ-агента)   | Интеграция с Firebase/APNs                       | ❌     |

---

## Текущие приоритеты (следующие шаги)

| Приоритет | Фаза  | Задача                                                                         |
| --------- | ----- | ------------------------------------------------------------------------------ |
| ✅        | 5.5a  | Cloud LLM (блокер focus-group) — реализовано                                    |
| 🟡 —      | —     | API-ключи: ✅ Groq + Gemini получены и проверены (fallback Groq→Gemini работает); ⏸ DeepSeek/OpenAI/Anthropic — потом, перед focus-group |
| ✅        | 7.6   | Demo-data при регистрации — реализовано                                         |
| ✅        | 4.6   | Auth: auto-refresh access token + logout — реализовано                          |
| ✅        | 4.7   | UI Polish — Purple + Amber темы, Inter, glassmorphism, hero — реализовано       |
| ✅        | 7.3a  | Импорт vCard MVP — реализовано                                                  |
| ✅        | 7.7   | Удаление аккаунта (GDPR) — реализовано                                          |
| ✅        | 7.5.1 | SMTP + Resend, smoke /auth/test-email — реализовано                             |
| ✅        | 7.5.2 | Email verification (JWT 24h) + блок POST контактов без подтверждения — реализовано |
| ✅        | 7.5.3 | Password reset (JWT 1h, anti-enumeration, rate-limit) — реализовано             |
| ✅        | 7.8   | Архивы + UX-редизайн карточки контакта (Phase 7.8) — реализовано                |
| ✅        | 9.5   | CI + Dependabot + TruffleHog + Branch protection — реализовано                  |
| 🟢 9      | —     | Полный редизайн (после focus-group) — на основе реального фидбека юзеров        |
| 🟢 10     | 5.5b  | Job Queue + persistence (после focus-group, ~2-3 дня)                           |
| 🟢 11     | 7.3b  | Preview + dedup перед импортом (после фидбека)                                  |
| 🟢 12     | 7.3.e | Экспорт данных (`GET /export`)                                                  |
| 🟢 13     | 7.1   | Теги для группировки контактов                                                  |
| 🟢 14     | 7.2   | Напоминания (`ContactReminder`)                                                 |

---

## Чек-лист перед коммитом

- Обновить `CHANGELOG.md` (секция `## [Unreleased]`)
- Убедиться, что `.env` не попал в staging
- Прошли все существующие тесты (`pytest`)

---

## Детали реализации

### 7.5.1: Интеграция отправки писем — план

**Принятые архитектурные решения:**
- Generic SMTP через `aiosmtplib` (не SES SDK, не fastapi-mail) — гибкость, провайдер меняется через .env
- Шаблоны на Jinja2, лежат рядом с сервисом
- Dev/prod через один и тот же код. Локально — реальный SMTP (Gmail/Yandex с App Password). MailPit как опция при необходимости
- Опечатка `smpt` → `smtp` исправляется одной миграцией, breaking change, в CHANGELOG отметить

**Что НЕ делается в этой фазе:**
- Шаблоны конкретных писем (verify, reset) — это 7.5.2 / 7.5.3
- Изменение registration flow (`emailVerified: True` остаётся) — это 7.5.2
- Токены для verify/reset ссылок — это 7.5.2
- Frontend (формы reset/verify) — это 7.5.2 / 7.5.3
- Keycloak SMTP config не трогаем (у нас своя регистрация)

**Этапы:**

| # | Что                              | Файл                                                | Описание                                                                                                                                              |
|---|----------------------------------|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Зависимости                       | `pyproject.toml`                                    | `aiosmtplib ^4.0`, `jinja2 ^3.1`                                                                                                                       |
| 2 | Переименование поля               | `sources/settings.py`                               | `smpt` → `smtp` в `Settings`. Поле `send_to` удалить (это про другое — нотификации админу)                                                              |
| 3 | Расширить `SMTPSettings`          | `sources/settings.py`                               | Добавить `use_tls: bool=True`, `use_starttls: bool=False`, `from_address: EmailStr \| None`, `from_name: str="Rockfile"`                                |
| 4 | Сервис отправки                   | `sources/api/services/email_service.py`             | `send_email(to, subject, html, text=None)`, `send_template_email(to, subject, template_name, context)`, `class EmailSendError(Exception)`             |
| 5 | Папка шаблонов                    | `sources/api/services/email_templates/`             | Пустая (.gitkeep). Шаблоны появятся в 7.5.2 / 7.5.3                                                                                                    |
| 6 | Обновить `.env.example`           | `.env.example`                                      | `SMTP__HOST`, `SMTP__PORT`, `SMTP__USERNAME`, `SMTP__PASSWORD`, `SMTP__USE_TLS`, `SMTP__USE_STARTTLS`, `SMTP__FROM_ADDRESS`, `SMTP__FROM_NAME`         |
| 7 | Тесты                             | `tests/test_email_service.py`                       | Мокаем `aiosmtplib.send`. Проверяем: вызов с правильными args, рендер шаблона, retry на transient, `EmailSendError` на permanent                       |
| 8 | CHANGELOG                         | `CHANGELOG.md`                                      | `### Added` для email_service, `### Changed` для `smpt`→`smtp` (breaking)                                                                              |

**API сервиса:**

```python
async def send_email(
    to: str, subject: str, html: str, text: str | None = None
) -> None:
    """Низкоуровневая отправка. Поднимает EmailSendError после исчерпания retries."""

async def send_template_email(
    to: str, subject: str, template_name: str, context: dict
) -> None:
    """Рендерит {template_name}.html.j2 + .txt.j2 из email_templates/ и шлёт."""

class EmailSendError(Exception): ...
```

**Поведение:**
- Async через `aiosmtplib` — не блокирует FastAPI loop
- Timeout 15 сек на одну отправку
- 1 retry на transient (timeout, connection refused), 0 retry на permanent (auth failure, 5xx от сервера)
- Логирование: `to`, `subject`, `template_name` (НЕ логируем тело письма и пароли)

**Риски при подключении реального SMTP сразу:**
- Gmail/Yandex требуют App Password (отдельный)
- Лимиты: Gmail ~500/день, Yandex ~150/час
- Без DKIM/SPF на собственном домене письма могут лететь в spam
- При ошибке в шаблоне можно случайно разослать пачку писем и попасть в бан почтового сервиса

---

### 5.5a: Cloud LLM (focus-group блокер) — план

Зачем: убрать локальный Ollama, дать тестерам Cloud LLM с быстрым ответом (Groq 5-10 сек vs Ollama 30-60 сек на CPU). Без queue — синхронный flow остаётся.

**Принятые архитектурные решения:**
- **Multi-provider fallback:** подход A — Try-fallback in-process. Простота важнее оптимальности
- **Приоритет провайдеров:** Groq → Cerebras → Gemini → Anthropic (paid в конце)
- **LLM abstraction:** factory с lazy import (`langchain-groq` подтягивается только если включён `groq`)
- **Frontend:** не трогаем, всё синхронно как сейчас. UX-компромисс на 2-4 недели focus-group
- **Timeouts:** per-provider 15 сек, total 45 сек (тогда 503 юзеру с toast)

**Важная корректировка по провайдерам:**
- OpenAI API: $5 при регистрации, **разовый**. Ежедневного free tier **нет** (путаница с ChatGPT web)
- Anthropic API: $5 разово
- **Daily-renewing бесплатные:** Groq (14400 RPD / 500k TPD), Cerebras (~1M tokens/day), Gemini Flash (1500 RPD), Mistral (~1k req/day), OpenRouter (free models)

**Стоимость если откажемся от fallback:**
- Groq paid Llama 3.3 70B: $0.59/1M input, $0.79/1M output
- Focus group ~80 запусков/день × 14 дней × ~6k tokens ≈ **$5-8** за всё мероприятие

**Что НЕ делается в 5.5a:**
- Queue, Redis, worker, agent_jobs — это 5.5b
- Persistence истории запусков — пока только audit log
- State-aware routing — оверкилл
- UI выбора провайдера юзером — infra-level

**Этапы реализации:**

| # | Что | Файл / артефакт |
|---|---|---|
| 1 | Зависимости | `pyproject.toml`: `langchain-groq ^0.4`, `langchain-anthropic ^0.5`, `langchain-openai ^0.5` |
| 2 | LLM factory | `sources/agents/llm_factory.py`: `def build_llm(provider: str \| None = None) -> BaseChatModel`. Lazy import. Кеш instance по провайдеру (dict) |
| 3 | Расширить `AgentSettings` | `sources/settings.py`: общие `llm_*` поля, deprecate `ollama_*` (оставить как алиасы на одну версию) |
| 4 | Refactor агентов | `prepare_meeting_agent.py`/`concierge_agent.py` — заменить кастомные factory на `build_llm()`. Убрать дубликат `_llm_instance` |
| 5 | Fallback функция | `sources/agents/llm_factory.py`: `async def invoke_with_fallback(graph_fn, payload, providers) -> tuple[result, provider_used, in_tokens, out_tokens]` |
| 6 | Использование в endpoints | `routers/v1/agents.py` — обёртка вокруг graph.ainvoke через `invoke_with_fallback` |
| 7 | Token usage logging | Через `usage_metadata` LangChain. В audit log с `provider_used`, `input_tokens`, `output_tokens` |
| 8 | `.env.example` | `AGENT__LLM_PROVIDER`, `AGENT__LLM_MODEL`, `AGENT__GROQ_API_KEY`, `AGENT__ANTHROPIC_API_KEY`, etc. |
| 9 | Тесты | `tests/test_llm_factory.py` (моки 4 провайдеров), `tests/test_agent_fallback.py` (первый 429 → второй ok, все упали → 503) |
| 10 | CHANGELOG | Breaking change в .env (`AGENT__OLLAMA_*` → `AGENT__LLM_*`), переход с Ollama default → Groq default |

**API factory + fallback:**

```python
# sources/agents/llm_factory.py
from langchain_core.language_models import BaseChatModel

_llm_cache: dict[str, BaseChatModel] = {}

def build_llm(provider: str | None = None) -> BaseChatModel:
    """Создаёт LLM по конфигу. provider=None → берёт из settings."""
    p = provider or config.agent.llm_provider
    if p in _llm_cache:
        return _llm_cache[p]
    # lazy import + создание
    ...

async def invoke_with_fallback(
    graph_runner: Callable,
    payload: dict,
    providers: list[str] | None = None,
    per_provider_timeout: int = 15,
    total_timeout: int = 45,
) -> tuple[dict, str, int, int]:
    """Try-fallback in-process. RateLimitError/ConnectionError/Timeout → next."""
```

**Подводные камни 5.5a:**
- `num_predict` (Ollama) vs `max_tokens` (всё остальное) — маппинг в factory
- Разные модели по-разному с structured output → snapshot-тесты на каждого провайдера (минимум один JSON-output тест)
- HTTP request может висеть до 45 сек — фронт должен показывать realistic ожидание
- Browser default timeout 30+ сек терпит, но nginx/proxy в будущем могут резать раньше

---

### 5.5b: Job Queue + persistence — план

Зачем: после focus-group переводим агентов в async-режим с persistence истории. Готовимся к scale.

**Принятые архитектурные решения:**
- **Queue:** arq + Redis (стандарт, узнаваемо на собесе, ~30MB RAM)
- **Persistence:** таблица `agent_jobs` в Postgres — даже при падении Redis/worker job не теряется
- **Frontend ← backend:** polling раз в 2 сек (а не SSE/WebSocket — проще)

**Что НЕ делается в 5.5b:**
- State-aware routing (трекинг лимитов по провайдерам в Redis) — оверкилл
- Стриминг ответа агента в UI — LangGraph не умеет out-of-box
- SSE/WebSocket вместо polling — отложено

**Этапы реализации:**

| # | Что | Файл / артефакт |
|---|---|---|
| 1 | Зависимости | `pyproject.toml`: `arq ^0.26` |
| 2 | Redis контейнер | `docker-compose.yml`: `redis:` сервис, том для AOF persistence |
| 3 | Worker контейнер | `docker-compose.yml`: `worker:` (тот же image что app), команда `arq sources.worker.WorkerSettings` |
| 4 | Модель `AgentJob` | `sources/api/data_base/models.py`: SQLAlchemy модель |
| 5 | Alembic migration | `alembic/versions/<rev>_add_agent_jobs.py` |
| 6 | Сервис jobs | `sources/api/services/jobs_service.py`: `create_job`, `get_job`, `list_jobs`, `update_job_status` |
| 7 | Worker config | `sources/worker.py`: `WorkerSettings.functions = [run_prepare_meeting, run_concierge]`, `job_timeout=900`, `max_jobs=4` |
| 8 | Migrate fallback в worker | Перенос `invoke_with_fallback` из request handler в worker. Логика та же |
| 9 | Async endpoints | `routers/v1/agents.py`: рефакторинг — создание job + enqueue, опц. `?sync=true` для тестов |
| 10 | Endpoints jobs | `routers/v1/jobs.py`: `GET /jobs/{id}`, `GET /jobs?status=...` |
| 11 | Frontend polling | `web/assets/js/contacts.js`: рефактор `runPrepareMeeting`/`runConcierge` на enqueue + poll |
| 12 | Тесты | `test_jobs.py`, `test_async_agents.py`, перенос `test_agent_fallback.py` |
| 13 | CHANGELOG | Async flow, sync mode через `?sync=true` |

**Схема таблицы `agent_jobs`:**

```python
class AgentJob(Base):
    __tablename__ = "agent_jobs"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    created_by_user_id: Mapped[UUID] = mapped_column(ForeignKey("app_users.id"), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "prepare_meeting" | "concierge"
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # pending | running | done | error
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    result: Mapped[dict | None] = mapped_column(JSONB)
    error_message: Mapped[str | None] = mapped_column(Text)
    provider_used: Mapped[str | None] = mapped_column(String(30))
    input_tokens: Mapped[int | None] = mapped_column(Integer)
    output_tokens: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    started_at: Mapped[datetime | None]
    finished_at: Mapped[datetime | None]
```

**Подводные камни 5.5b:**
- Worker умер посередине job → `status=running` навечно. Решение: heartbeat + watchdog (раз в N сек обновлять `last_seen_at`, recovery job перевешивает зависшие в `pending`)
- Юзер дважды кликает кнопку → два job. Решение: idempotency key (hash payload) ИЛИ disable кнопки на фронте
- Worker и FastAPI делят codebase → один Dockerfile, разные команды (`python sources/main.py` vs `arq sources.worker.WorkerSettings`)
- Tenant isolation в jobs — НЕ забыть фильтровать по `tenant_id` во всех job endpoints
- Polling нагрузка: 30 юзеров × 0.5 RPS = 15 RPS на `/jobs/{id}` — терпимо. Кешировать response при `status=done`
- Refactor с 5.5a минимальный — основная часть кода (factory + fallback) не меняется, только переезжает

---

### 7.6: Demo-data при регистрации — план (0.5 дня)

Зачем: бороться с "пустой dashboard" эффектом. Юзер сразу видит UI с заполненными карточками, разными `relationship_type`, парой взаимодействий, обещаниями. Может удалить демо одной кнопкой когда добавит своих.

**Принятые решения:**
- Опция при регистрации (checkbox "Загрузить демо для знакомства"). По умолчанию ON
- Создаются с тегом/префиксом "Демо: ..." в `full_name` или флаг `is_demo: bool` на ContactCard
- Кнопка "Удалить все демо-данные" в settings

**Этапы:**

| # | Что | Файл |
|---|---|---|
| 1 | Поле `is_demo: bool = False` на `ContactCard` | `sources/api/data_base/models.py` + Alembic |
| 2 | Seed-файл | `sources/api/services/demo_data.py` — 10 контактов с реалистичными именами, фотками-заглушками, разными `relationship_type`, по 1-2 взаимодействия с обещаниями и упоминаниями ДР в ближайшие 30 дней |
| 3 | Интеграция в registration | `user_registration_service.py:register_user` — если payload содержит `load_demo: bool = True`, после создания tenant'а вызывает `seed_demo_data(tenant_id)` |
| 4 | UI checkbox | `web/login.html` — на вкладке "Регистрация" добавить чекбокс "Загрузить демо" |
| 5 | Endpoint удаления | `POST /api/v1/contacts/clear-demo` — удаляет все `is_demo=True` в текущем tenant. UI кнопка в settings |
| 6 | Тесты | Создание tenant с демо → проверка что N контактов с `is_demo=True` есть. Удаление демо → 0 контактов |

**Содержимое демо (примерный набор):**
- 3× business (коллега, инвестор, партнёр)
- 3× personal (друг детства, тренер, бариста)
- 2× family
- 2× other (сосед, врач)
- Распределить ДР по `+5/+12/+25 дней` от сегодня (чтобы попасть в фильтр "ДР скоро")
- 1-2 контакта с открытым обещанием mine, 1-2 с обещанием theirs (чтобы Concierge agent имел что показать)

**Подводные камни:**
- Локализация имён — все Иваны Ивановы будут странно. Подобрать разнообразные: Анна Соколова, Дмитрий Петров, Артём Ким, etc.
- Photos: vCard PHOTO embedded — не используем. UI рендерит первую букву имени как сейчас
- При импорте `is_demo` не выставляется (только при регистрации)
- Удаление демо: cascade на interactions/links через `cascade="all, delete-orphan"` уже работает в модели

---

### 7.7: Удаление аккаунта (GDPR) — план (1-1.5 дня)

Зачем: GDPR/152-ФЗ требуют right to be forgotten. Без этого фокус-группа с реальными PII контактов — юридический риск. Также повышает доверие тестеров («мои данные не заложники»).

**Принятые решения:**
- **Hard delete** (физическое удаление), без soft-delete/анонимизации. Проще, чище, удовлетворяет GDPR без споров.
- **Подтверждение через ввод email** в UI (типичный pattern Stripe/GitHub). Без капчи/повторного пароля — overkill для нашего масштаба.
- **Удалять и из Keycloak** — иначе пользователь останется в IdP, не сможет повторно зарегаться с тем же email.
- **Без grace-периода** — focus-group, нет смысла. Можно вернуть позже как «выгрузить данные и удалить через 30 дней».
- **Audit log записи** удаляются вместе с пользователем (так как они в той же БД и относятся к нему). При желании можно вынести в отдельную anonymized таблицу позже.

**Этапы:**

| # | Что | Файл |
|---|---|---|
| 1 | Сервис каскадного удаления | `sources/api/services/account_service.py` — `delete_account(session, user, kc_admin_client)`: 1) удалить контакты/взаимодействия/связи через `cascade` (через delete Tenant — все его контакты исчезнут), 2) удалить AppUser, 3) удалить Tenant, 4) вызвать `delete_keycloak_user(keycloak_sub)` |
| 2 | Keycloak admin: delete user | `sources/api/auth/keycloak_admin.py` — `delete_keycloak_user(keycloak_id)`. DELETE `/admin/realms/{realm}/users/{id}` |
| 3 | Endpoint | `DELETE /api/v1/auth/account` в `routers/v1/auth.py`. Тело: `{"confirm_email": "..."}`. Проверка `confirm_email == current_user.email` (case-insensitive trim). На несовпадение → 400. На успех → 204 |
| 4 | UI — кнопка в settings | Пока settings-страницы нет → временно добавить «Опасная зона» в footer/footer-card страницы `/contacts.html` или создать `/settings.html`. Решить при реализации |
| 5 | UI — confirm-форма | Модалка: текст «Все ваши контакты, взаимодействия, обещания будут удалены безвозвратно. Введите ваш email для подтверждения: ___» + кнопка «Удалить навсегда» (`button-danger`) |
| 6 | Logout после удаления | На success — localStorage.removeItem('token'), редирект на `/web/login.html?deleted=1` с toast «Аккаунт удалён» |
| 7 | Тесты | `tests/test_account_deletion.py`: успешное удаление с правильным email; 400 при неверном email; контакты/обещания/links реально исчезают из БД; KC-admin вызван с правильным keycloak_sub (mock); 401 без авторизации |

**Подводные камни:**
- **KC недоступен** во время удаления → пользователь остаётся в IdP, в БД его нет. Юзер не сможет зайти, при ретрае регистрации увидит «email already exists» в KC. Решение: делать KC delete **первым**, потом БД. Если KC упал — 503, ничего не удалено в БД, повтор будет идемпотентным. (Альтернативно — сделать delete отдельной background job через arq, ретраить до победы. Но это Phase 5.5b.)
- **Foreign keys:** `Tenant → AppUser`, `Tenant → ContactCard`, `ContactCard → Interactions/Links/FamilyMembers`. Существующие `cascade="all, delete-orphan"` работают только при удалении через ORM. Для надёжности добавить SQL-уровневый `ON DELETE CASCADE` где ещё не выставлен.
- **Multi-user в одном tenant:** пока 1 user = 1 tenant. Если в будущем добавим команды — нужно либо запрещать удаление последнему пользователю tenant'а, либо назначать transfer ownership. Пока не критично.
- **AGENT cache instance:** `_llm_instance` в `llm_factory.py` живёт за пределами запроса. На удаление аккаунта не влияет (LLM-инстанс глобальный, не привязан к юзеру).
- **GDPR audit trail:** некоторые регуляторы требуют сохранять сам факт удаления (без PII) на 6+ месяцев. Простой компромисс: дёшево залогировать `account deleted: tenant_id=<uuid> at=<ts>` в loguru `audit.log`. Этого хватит, реальные PII не сохраняются.

**Что НЕ делаем сейчас:**
- Экспорт перед удалением (юзер должен сам выгрузить через будущий `GET /export` — Phase 7.3.e)
- Email-уведомление об удалении (требует Phase 7.5.1)
- Восстановление в течение N дней (no grace period)

---

### 7.3a: Импорт vCard MVP — план (1-2 дня)

Зачем: дать тестерам быстро залить 20-50 своих важных контактов из iPhone/Google/Android экспорта.

**Принятые решения:**
- Парсер `vobject` (стабильный, проверенный)
- vCard 3.0 (стандарт iPhone/Google exports). 4.0 — позже
- Blind import без preview — упростить MVP. Preview в 7.3b
- Без dedup — юзер сам разберётся. Dedup в 7.3b
- Лимит 200 контактов / 2MB / 1 файл

**Этапы:**

| # | Что | Файл |
|---|---|---|
| 1 | Зависимость | `pyproject.toml`: `vobject ^0.9` |
| 2 | Парсер | `sources/api/services/import_service.py` — `parse_vcard(content: bytes) -> list[ContactCardCreate]` |
| 3 | Mapping | FN → full_name (required), TEL[0] → phone, EMAIL[0] → email, ADR → склейка строкой, BDAY → birthday (с обработкой формата `--MM-DD` без года), NOTE → ambitions. `relationship_type` ставим `other` по дефолту |
| 4 | Endpoint | `POST /api/v1/contacts/import` multipart/form-data, file (.vcf). Возвращает `{created: N, errors: [{line, message}], total: N}` |
| 5 | Сервис записи | Использует существующий `ContactService.create_contact`. Tenant_id из `current_user.tenant_id`. Транзакция: либо все, либо ни одного (на errors — rollback?) |
| 6 | UI | Кнопка "Импортировать vCard" на странице контактов → `<input type="file" accept=".vcf">` → upload → toast "Импортировано N, ошибок M". Список контактов рефрешится |
| 7 | Тесты | Файлы фикстур: iPhone export (8 контактов), Google export, edge cases (кириллица UTF-8, multiple TEL/EMAIL, BDAY без года, NOTE с переносами строк, файл без FN — error) |
| 8 | Validation | Magic bytes / расширение `.vcf`, размер ≤2MB, лимит 200 контактов (на 201-м обрывать с error), валидация EmailStr на email |

**API спец-кейсы:**

```python
async def parse_vcard(content: bytes) -> list[tuple[ContactCardCreate, str | None]]:
    """Возвращает [(contact_create, error_message_or_None), ...]"""
    # vobject.readComponents(content.decode('utf-8'))
    # для каждого vcard → выдёргиваем поля, формируем ContactCardCreate
    # ошибки парсинга — пропускаем с сообщением, не падаем

@router.post("/contacts/import", status_code=200)
async def import_contacts(file: UploadFile, current_user: AuthUser, session: AsyncSession):
    if file.size > 2 * 1024 * 1024:
        raise HTTPException(413, "Файл слишком большой (макс 2 MB)")
    content = await file.read()
    parsed = await parse_vcard(content)
    if len(parsed) > 200:
        raise HTTPException(400, f"Слишком много контактов в файле (макс 200, найдено {len(parsed)})")
    
    created = 0
    errors = []
    for idx, (contact, error) in enumerate(parsed):
        if error:
            errors.append({"line": idx, "message": error})
            continue
        try:
            await ContactService.create_contact(session, contact, current_user.tenant_id)
            created += 1
        except Exception as e:
            errors.append({"line": idx, "message": str(e)})
    
    return {"created": created, "errors": errors, "total": len(parsed)}
```

**Подводные камни:**
- vCard PHOTO в base64 — игнорируем (увеличивает payload и не нужно)
- Кириллица: vCard 3.0 часто с `quoted-printable`, vobject сам декодирует. Тест-фикстура нужна
- Multiple TEL/EMAIL: для MVP берём первый. В ambitions можно добавить "Доп.телефоны: ...; Доп.email: ..."
- BDAY без года: формат `--01-15` (январь 15, год неизвестен). Сохранять как `1900-01-15` или nullable year? **Поставим 1900** (отображение в UI можно прятать год если 1900)
- Файл с разными кодировками: пробуем UTF-8, на UnicodeDecodeError → CP1251 (русский Windows). Если оба fail → 400
- Транзакция: атомарность? Сейчас в плане **per-contact** — если 5-й контакт упал, первые 4 сохранены. Это OK для MVP. Можно потом сделать `?atomic=true` опцию
- Tenant isolation: `current_user.tenant_id` обязательно, на всех контактах
- iPhone export часто содержит **группы контактов** (X-ABLabel) — игнорируем (нет места)
- Quick-add форма (имя+phone+email) у нас уже есть — её НЕ ломаем
