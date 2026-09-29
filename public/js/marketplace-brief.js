(function initMarketplaceBrief() {
  const form = document.getElementById("mpBrief");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const cfg = window.SITE_CONFIG || {};
    const username = String(cfg.telegramUsername || "").replace(/^@/, "").trim();
    const product = String(form.elements.product.value || "").trim();
    if (!username || !product) {
      form.elements.product.focus();
      return;
    }

    const message = [
      "Здравствуйте! Хочу обсудить карточку товара.",
      "",
      `Товар: ${product}`,
      `Площадка: ${form.elements.platform.value}`,
      `Объём: ${form.elements.slides.value}`,
      `Фото: ${form.elements.photos.value}`,
      "",
      "Ссылку на товар / фотографии прикреплю следующим сообщением.",
    ].join("\n");

    window.open(`https://t.me/${encodeURIComponent(username)}?text=${encodeURIComponent(message)}`, "_blank", "noopener");
  });
})();
