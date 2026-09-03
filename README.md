# Портфолио-витрина для фриланса (GitLab Pages)

Статический лендинг для ссылок из Kwork, откликов и Telegram.

## Быстрый старт локально

```bash
cd /home/dns/projects/freelance-portfolio/public
python -m http.server 8080
```

Открой: http://127.0.0.1:8080

## Перед публикацией

1. Открой `public/index.html`
2. Замени `TELEGRAM_USERNAME` на свой ник в Telegram (без `@`)
3. Замени ссылку Kwork на свою: `https://kwork.ru/user/ВАШ_ЛОГИН`
4. При необходимости поправь имя, описание, кейсы

---

## GitLab Pages — пошагово

### Шаг 1. Аккаунт GitLab

1. Зайди на https://gitlab.com
2. Зарегистрируйся или войди (можно через GitHub/Google)

### Шаг 2. Создай пустой проект

1. **New project** → **Create blank project**
2. Project name: `freelance-portfolio` (или любое)
3. Visibility: **Public** (Pages на free tier работает для public-проектов)
4. **Сними галочку** «Initialize repository with a README»
5. **Create project**

GitLab покажет команды для push — они понадобятся на шаге 4.

### Шаг 3. Инициализируй git локально (один раз)

```bash
cd /home/dns/projects/freelance-portfolio

git init
git add .
git commit -m "Initial portfolio landing for GitLab Pages"
```

Если git попросит имя/email:

```bash
git config user.name "Rinat"
git config user.email "your@email.com"
```

### Шаг 4. Привяжи remote и запушь

Подставь свой GitLab username вместо `YOUR_USERNAME`:

```bash
git branch -M main
git remote add origin git@gitlab.com:YOUR_USERNAME/freelance-portfolio.git
git push -u origin main
```

**SSH vs HTTPS:**

- SSH (рекомендуется): нужен ключ на GitLab → Settings → SSH Keys
- HTTPS: `git remote add origin https://gitlab.com/YOUR_USERNAME/freelance-portfolio.git` — при push спросит логин и Personal Access Token (не пароль)

### Шаг 5. Дождись CI pipeline

1. В проекте GitLab: **Build** → **Pipelines**
2. Должен пройти job `pages` (зелёная галочка, ~1 минута)
3. Если красный — открой job и посмотри лог

Файл `.gitlab-ci.yml` уже настроен: он отдаёт папку `public/` как сайт.

### Шаг 6. Получи URL сайта

1. **Deploy** → **Pages** (или **Settings** → **Pages**)
2. URL будет вида:

```
https://YOUR_USERNAME.gitlab.io/freelance-portfolio/
```

Именно эту ссылку вставляй в Kwork в поле «Портфолио» / в отклики.

### Шаг 7. Обновления

После правок в `public/`:

```bash
git add .
git commit -m "Update portfolio"
git push
```

Сайт обновится через 1–2 минуты после успешного pipeline.

---

## Структура проекта

```
freelance-portfolio/
├── .gitlab-ci.yml      # деплой на Pages
├── public/
│   ├── index.html      # лендинг
│   ├── css/styles.css
│   └── js/main.js
└── README.md           # эта инструкция
```

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| Pipeline не запускается | Проверь, что запушена ветка `main` и есть `.gitlab-ci.yml` |
| Pages 404 | Подожди 2–5 мин после первого успешного pipeline |
| Сайт без стилей | Пути в HTML относительные (`css/styles.css`) — не меняй на абсолютные без нужды |
| Проект private | На free tier Pages для private может быть недоступен — сделай public |

## Дальше (опционально)

- Свой домен: **Settings** → **Pages** → **New domain**
- Скриншоты кейсов: положи в `public/images/` и добавь в карточки
- Аналитика: Яндекс.Метрика / Plausible — скрипт в `index.html`
