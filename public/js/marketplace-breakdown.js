(function initMarketplaceBreakdown() {
  const toggles = document.querySelectorAll("[data-breakdown-toggle]");
  if (!toggles.length) return;

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  toggles.forEach((btn) => {
    const panelId = btn.getAttribute("aria-controls");
    const panel = panelId ? document.getElementById(panelId) : null;
    const label = btn.querySelector(".mp-breakdown-toggle__text");
    if (!panel || !label) return;

    const clip = panel.querySelector(".mp-breakdown__clip") || panel;

    // Closed by default — works even if CSS is cached/old
    panel.hidden = true;
    panel.classList.remove("is-open");
    panel.style.height = "";
    btn.classList.remove("is-open");
    btn.setAttribute("aria-expanded", "false");
    const closedLabel = btn.dataset.closedLabel || "Показать разбор";
    label.textContent = closedLabel;

    let animating = false;

    const onTransitionEnd = (event) => {
      if (event.target !== panel || event.propertyName !== "height") return;
      animating = false;
      if (panel.classList.contains("is-open")) {
        panel.style.height = "auto";
      } else {
        panel.hidden = true;
        panel.style.height = "";
      }
    };

    panel.addEventListener("transitionend", onTransitionEnd);

    btn.addEventListener("click", () => {
      if (animating) return;
      const open = panel.hidden || !panel.classList.contains("is-open");

      btn.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      const openLabel = btn.dataset.openLabel || "Скрыть разбор";
      const closedLabel = btn.dataset.closedLabel || "Показать разбор";
      label.textContent = open ? openLabel : closedLabel;

      if (reduceMotion) {
        panel.hidden = !open;
        panel.classList.toggle("is-open", open);
        panel.style.height = "";
        return;
      }

      animating = true;

      if (open) {
        panel.hidden = false;
        panel.classList.add("is-open");
        panel.style.height = "0px";
        // force layout, then expand to content height
        void panel.offsetHeight;
        panel.style.height = `${clip.scrollHeight}px`;
      } else {
        panel.style.height = `${panel.scrollHeight}px`;
        void panel.offsetHeight;
        panel.classList.remove("is-open");
        panel.style.height = "0px";
      }
    });
  });
})();
