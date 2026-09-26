# Безопасность витрины и демо на VPS

Аудит от 2026-09-26 (статический обзор + заголовки HTTP).

## GitHub Pages (`spiritwalker84.github.io/freelance-portfolio`)

| Проверка | Статус | Комментарий |
|----------|--------|-------------|
| HTTPS / HSTS | OK | `strict-transport-security` от GitHub |
| Секреты в репозитории | OK | Токены ботов не в `public/` |
| CSP / X-Frame-Options | Нет | Для статики приемлемо; при желании — meta CSP в `index.html` |
| Форма на главной | Частично | Сейчас deep-link в Telegram или опциональный `leadApiUrl`; honeypot в форме |
| Showcase для Kwork | OK | `noindex`, без `t.me`/форм; скрипт `scripts/verify-showcase-safe.sh` |

**Важно:** в откликах на Kwork давать только URL **showcase**, не главную (там Telegram/Kwork-кнопки).

## VPS демо (`5.35.94.25`, лендинги)

| Проверка | Статус | Рекомендация |
|----------|--------|--------------|
| TLS | Нет (HTTP) | Подключить Let's Encrypt, редирект 80→443 |
| Заголовки безопасности | Нет | `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options` в nginx |
| form-api CORS | `allow_origins=["*"]` | Ограничить `CORS_ORIGINS` доменами лендинга и GitHub Pages |
| Токен Telegram | На сервере в `.env` | Не коммитить; ротация при утечке |
| Rate limit | Нет | nginx `limit_req` на `/api/lead` или slowapi |
| `/health` | Публичный | Не раскрывать лишнее; без токенов в ответе |

## portfolio-lead-api (опционально)

См. `deploy/portfolio-lead-api/` — отдельный endpoint для формы главной витрины с whitelist origin и honeypot.

## Перед продакшеном

1. Заполнить `telegramUsername` в `public/js/site-config.js`.
2. `./scripts/verify-showcase-safe.sh`
3. После деплоя: `curl -sI` на главную и на `/landingN/api/lead` (только POST с валидным телом).
