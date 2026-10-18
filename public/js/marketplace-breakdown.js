(function initMarketplaceBreakdown() {
  const toggles = document.querySelectorAll("[data-breakdown-toggle]");
  if (!toggles.length) return;

  toggles.forEach((btn) => {
    const panelId = btn.getAttribute("aria-controls");
    const panel = panelId ? document.getElementById(panelId) : null;
    const label = btn.querySelector(".mp-breakdown-toggle__text");
    if (!panel || !label) return;

    btn.addEventListener("click", () => {
      const open = !panel.classList.contains("is-open");
      panel.classList.toggle("is-open", open);
      btn.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      label.textContent = open ? "Скрыть разбор" : "Показать разбор";
    });
  });
})();
