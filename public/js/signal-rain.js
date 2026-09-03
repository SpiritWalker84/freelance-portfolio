/**
 * Signal rain — subtle data stream for hero (not full Matrix cosplay).
 * Accent-colored, low opacity, pauses on reduced-motion / hidden tab.
 */
(function initSignalRain() {
  const canvas = document.getElementById("signalRain");
  if (!canvas) return;

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) return;

  const ctx = canvas.getContext("2d");
  const chars = "01{}botAPI/TG#_py→✓".split("");
  const fontSize = 13;
  let columns = 0;
  let drops = [];
  let animationId = null;
  let isVisible = true;

  const resize = () => {
    const hero = canvas.closest(".hero");
    if (!hero) return;
    const rect = hero.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = `${rect.width}px`;
    canvas.style.height = `${rect.height}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    columns = Math.floor(rect.width / fontSize);
    drops = Array.from({ length: columns }, () => Math.random() * -40);
  };

  const draw = () => {
    if (!isVisible) {
      animationId = requestAnimationFrame(draw);
      return;
    }

    const w = canvas.width / (window.devicePixelRatio || 1);
    const h = canvas.height / (window.devicePixelRatio || 1);

    ctx.fillStyle = "rgba(10, 9, 8, 0.08)";
    ctx.fillRect(0, 0, w, h);

    ctx.font = `${fontSize}px "IBM Plex Mono", monospace`;

    for (let i = 0; i < drops.length; i += 1) {
      const char = chars[Math.floor(Math.random() * chars.length)];
      const x = i * fontSize;
      const y = drops[i] * fontSize;
      const alpha = 0.08 + Math.random() * 0.22;
      ctx.fillStyle = `rgba(224, 120, 64, ${alpha})`;
      ctx.fillText(char, x, y);

      if (y > h && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i] += 0.45 + Math.random() * 0.35;
    }

    animationId = requestAnimationFrame(draw);
  };

  resize();
  draw();

  window.addEventListener("resize", resize, { passive: true });

  document.addEventListener("visibilitychange", () => {
    isVisible = !document.hidden;
  });

  window.addEventListener("beforeunload", () => {
    if (animationId) cancelAnimationFrame(animationId);
  });
})();
