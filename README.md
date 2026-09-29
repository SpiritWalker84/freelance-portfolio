# Портфолио-витрина (GitHub Pages + VPS для демо)

Статический сайт для Kwork, hh, Telegram и прямых клиентов.

## Публичные URL (актуально)

| Страница | Ссылка |
|----------|--------|
| **Главная** (боты, автоматизация) | https://spiritwalker84.github.io/freelance-portfolio/ |
| **Карточки WB/Ozon** | https://spiritwalker84.github.io/freelance-portfolio/marketplace/ |
| **Kwork: боты** (без контактов) | https://spiritwalker84.github.io/freelance-portfolio/showcase/ |
| **Kwork: карточки МП** (без контактов) | https://spiritwalker84.github.io/freelance-portfolio/showcase/mp/ |

**Хостинг сайта:** [GitHub Pages](https://github.com/SpiritWalker84/freelance-portfolio) (ветка `master`, workflow `.github/workflows/deploy-pages.yml`).

**VPS** (`5.35.94.25`): live-демо лендингов (`/landing1/` …), API формы заявки с главной (`leadApiUrl` в `site-config.js`). Сам портфолио-сайт на VPS не обязателен — основная витрина на GitHub.

## Быстрый старт локально

```bash
cd /home/dns/projects/freelance-portfolio/public
python -m http.server 8080
```

Открой: http://127.0.0.1:8080

## Перед пушем

1. `public/js/site-config.js` — `telegramUsername`, `kworkUsername`, `leadApiUrl`
2. Для откликов **Kwork** не давайте главную (там контакты):
   - разработка → `…/showcase/`
   - карточки МП → `…/showcase/mp/`
3. `./scripts/verify-showcase-safe.sh`

## Деплой (GitHub Pages)

```bash
cd /home/dns/projects/freelance-portfolio
git add public/ scripts/ docs/ README.md
git commit -m "Описание изменений"
git push origin master
```

Через 1–3 минуты обновится https://spiritwalker84.github.io/freelance-portfolio/ (Actions → Deploy GitHub Pages).

## Структура

```
freelance-portfolio/
├── .github/workflows/deploy-pages.yml
├── public/
│   ├── index.html              # автоматизация
│   ├── marketplace/            # карточки WB/Ozon
│   ├── showcase/               # Kwork: боты
│   ├── showcase/mp/            # Kwork: маркетплейсы
│   ├── images/marketplace/     # слайды FGg03
│   └── js/site-config.js
├── deploy/portfolio-lead-api/  # форма заявки на VPS
└── docs/HH-PORTFOLIO.md        # что давать работодателям hh
```

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| Старый контент на сайте | Проверь push в `master` и зелёный workflow в Actions |
| Форма на главной не шлёт | `leadApiUrl` и CORS/HTTPS на VPS; с GitHub Pages API должен отвечать по сети |
| Kwork отклоняет ссылку | Только `showcase/` или `showcase/mp/`, без Telegram в HTML |

## Опционально

- Свой домен: GitHub repo → Settings → Pages → Custom domain
- `.gitlab-ci.yml` — запасной деплой GitLab; основной канал сейчас GitHub
