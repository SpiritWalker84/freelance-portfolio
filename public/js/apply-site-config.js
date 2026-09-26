(function applySiteConfig() {
  const cfg = window.SITE_CONFIG;
  if (!cfg) return;

  const tg = (cfg.telegramUsername || "").replace(/^@/, "").trim();
  const kwork = (cfg.kworkUsername || "").trim();

  document.querySelectorAll('[data-site-link="telegram"]').forEach((el) => {
    if (!tg) {
      el.classList.add("is-disabled");
      el.setAttribute("aria-disabled", "true");
      el.addEventListener("click", (e) => {
        e.preventDefault();
        alert("Укажите telegramUsername в public/js/site-config.js");
      });
      return;
    }
    el.href = `https://t.me/${tg}`;
    el.target = "_blank";
    el.rel = "noopener noreferrer";
  });

  document.querySelectorAll('[data-site-link="kwork"]').forEach((el) => {
    if (!kwork) return;
    el.href = `https://kwork.ru/user/${kwork}`;
    el.target = "_blank";
    el.rel = "noopener noreferrer";
  });

  const gigs = cfg.kworkGigs || {};
  document.querySelectorAll("[data-kwork-gig]").forEach((el) => {
    const key = el.getAttribute("data-kwork-gig");
    const url = gigs[key];
    if (!url) return;
    el.href = url;
    el.target = "_blank";
    el.rel = "noopener noreferrer";
  });

  const form = document.getElementById("leadForm");
  if (form && tg) {
    form.dataset.telegram = tg;
  }
  if (form && cfg.leadApiUrl) {
    const onVps =
      window.location.hostname === "5.35.94.25" ||
      window.location.pathname.startsWith("/portfolio");
    form.dataset.leadApi = onVps ? "/api/portfolio-lead" : cfg.leadApiUrl;
  }
})();
