const menuToggle = document.getElementById("menuToggle");
const nav = document.getElementById("nav");
const header = document.getElementById("header");

if (menuToggle && nav) {
  menuToggle.addEventListener("click", () => {
    nav.classList.toggle("is-open");
  });

  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => nav.classList.remove("is-open"));
  });
}

if (header) {
  const onScroll = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 24);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

const revealItems = document.querySelectorAll(".reveal");
const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!prefersReduced && revealItems.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
  );

  revealItems.forEach((item, index) => {
    item.style.transitionDelay = `${Math.min(index * 0.06, 0.36)}s`;
    observer.observe(item);
  });
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

const leadForm = document.getElementById("leadForm");
if (leadForm) {
  leadForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const telegramUser = leadForm.dataset.telegram || "TELEGRAM_USERNAME";
    if (telegramUser === "TELEGRAM_USERNAME") {
      alert("Укажи Telegram username в data-telegram формы и в ссылках на сайте.");
      return;
    }

    const name = leadForm.name.value.trim();
    const contact = leadForm.contact.value.trim();
    const task = leadForm.task.value.trim();

    const message = [
      "Заявка с портфолио",
      "",
      `Имя: ${name}`,
      `Контакт: ${contact}`,
      "",
      "Задача:",
      task,
    ].join("\n");

    const url = `https://t.me/${telegramUser}?text=${encodeURIComponent(message)}`;
    window.open(url, "_blank", "noopener,noreferrer");
  });
}

const THEME_KEY = "signal-theme";

function initThemeToggle() {
  const themeToggle = document.getElementById("themeToggle");
  const themeToggleLabel = document.getElementById("themeToggleLabel");

  function applyTheme(neon) {
    if (neon) {
      document.documentElement.setAttribute("data-theme", "neon");
      if (themeToggleLabel) themeToggleLabel.textContent = "Неон: вкл";
    } else {
      document.documentElement.removeAttribute("data-theme");
      if (themeToggleLabel) themeToggleLabel.textContent = "v1";
    }
  }

  const savedTheme = localStorage.getItem(THEME_KEY);
  if (savedTheme === "v1") {
    applyTheme(false);
  } else if (savedTheme === "neon") {
    applyTheme(true);
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const isNeon = document.documentElement.getAttribute("data-theme") === "neon";
      applyTheme(!isNeon);
      localStorage.setItem(THEME_KEY, !isNeon ? "neon" : "v1");
    });
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initThemeToggle);
} else {
  initThemeToggle();
}
