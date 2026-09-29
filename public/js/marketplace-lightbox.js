(function initMarketplaceLightbox() {
  const slides = document.querySelectorAll(".mp-slide img");
  if (!slides.length) return;

  let dialog = document.getElementById("mpLightbox");
  if (!dialog) {
    dialog = document.createElement("dialog");
    dialog.id = "mpLightbox";
    dialog.className = "mp-lightbox";
    dialog.innerHTML =
      '<div class="mp-lightbox__inner">' +
      '<button type="button" class="mp-lightbox__close" aria-label="Закрыть">×</button>' +
      '<img class="mp-lightbox__img" id="mpLightboxImg" alt="">' +
      "</div>";
    document.body.appendChild(dialog);
    dialog.querySelector(".mp-lightbox__close").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (e) => {
      if (e.target === dialog) dialog.close();
    });
  }

  const lbImg = dialog.querySelector("#mpLightboxImg");

  document.querySelectorAll(".mp-slide").forEach((fig) => {
    const img = fig.querySelector("img");
    if (!img) return;
    let link = fig.querySelector(".mp-slide__link");
    if (!link) {
      link = document.createElement("a");
      link.className = "mp-slide__link";
      link.href = img.currentSrc || img.src;
      link.setAttribute("aria-label", "Увеличить слайд");
      img.parentNode.insertBefore(link, img);
      link.appendChild(img);
    }
    const open = () => {
      lbImg.src = img.currentSrc || img.src;
      lbImg.alt = img.alt || "";
      if (typeof dialog.showModal === "function") dialog.showModal();
    };
    link.addEventListener("click", (e) => {
      e.preventDefault();
      open();
    });
  });
})();
