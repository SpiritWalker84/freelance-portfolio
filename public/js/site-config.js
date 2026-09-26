/**
 * Единая точка настроек витрины (главная страница).
 * Showcase (/showcase/) контакты не использует — только для откликов на Kwork.
 */
window.SITE_CONFIG = {
  /** Telegram @username без «@». Пусто — кнопки Telegram скрыты, форма покажет подсказку. */
  telegramUsername: "spiritwalker84",
  kworkUsername: "spiritwalker",
  /** POST JSON { name, contact, task, website? } — portfolio-lead-api на VPS */
  leadApiUrl: "http://5.35.94.25/api/portfolio-lead",
  kworkGigs: {
    zayavki: "https://kwork.ru/script-programming/54516506/telegram-bot-s-zayavkami-i-uvedomleniem-menedzheru",
    ai: "https://kwork.ru/script-programming/54516871/ai-konsultant-v-telegram-otvety-sbor-zayavki",
    menu: "https://kwork.ru/script-programming/54516815/telegram-bot-s-menyu-i-knopkami-pod-vash-biznes",
    parser: "https://kwork.ru/script-programming/54750732/parsing-sayta-na-python",
    landing: "https://kwork.ru/user/spiritwalker",
  },
  showcasePath: "/freelance-portfolio/showcase/",
};
