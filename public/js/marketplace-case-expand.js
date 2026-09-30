(function initMarketplaceCaseExpand() {
  const buttons = document.querySelectorAll("[data-expand-target]");
  if (!buttons.length) return;

  buttons.forEach((btn) => {
    const id = btn.getAttribute("data-expand-target");
    const grid = id ? document.getElementById(id) : null;
    if (!grid) return;

    btn.addEventListener("click", () => {
      const expanded = grid.classList.toggle("is-expanded");
      btn.setAttribute("aria-expanded", expanded ? "true" : "false");
      btn.textContent = expanded ? "Свернуть слайды" : "Показать все 6 слайдов";
    });
  });
})();
