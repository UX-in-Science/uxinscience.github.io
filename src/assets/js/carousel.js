document.querySelectorAll('[data-carousel]').forEach((carousel) => {
  const slides = [...carousel.querySelectorAll('[data-slide]')];
  if (slides.length < 2) return;

  const controls = carousel.querySelector('[data-carousel-controls]');
  const status = carousel.querySelector('[data-carousel-status]');
  const toggle = carousel.querySelector('[data-rotation]');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let paused = motion.matches;
  let hovering = false;
  let timer;

  function syncRotation() {
    window.clearInterval(timer);
    const running = !paused && !hovering && !document.hidden;
    status.setAttribute('aria-live', running ? 'off' : 'polite');
    toggle.textContent = paused ? 'Play' : 'Pause';
    toggle.setAttribute('aria-label', paused ? 'Start automatic highlights' : 'Pause automatic highlights');
    if (running) timer = window.setInterval(() => showSlide(current + 1), 6000);
  }

  function showSlide(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, slideIndex) => {
      slide.hidden = slideIndex !== current;
    });
    status.textContent = `${current + 1} / ${slides.length}`;
  }

  function manualStep(direction) {
    paused = true;
    syncRotation();
    showSlide(current + direction);
  }

  carousel.setAttribute('aria-roledescription', 'carousel');
  slides.forEach((slide, index) => {
    slide.setAttribute('aria-roledescription', 'slide');
    slide.setAttribute('aria-label', `${index + 1} of ${slides.length}`);
  });
  carousel.querySelector('[data-previous]').addEventListener('click', () => manualStep(-1));
  carousel.querySelector('[data-next]').addEventListener('click', () => manualStep(1));
  toggle.addEventListener('click', () => {
    paused = !paused;
    syncRotation();
  });
  carousel.addEventListener('mouseenter', () => {
    hovering = true;
    syncRotation();
  });
  carousel.addEventListener('mouseleave', () => {
    hovering = false;
    syncRotation();
  });
  // Stop when keyboard users enter; resume only through the Play button.
  carousel.addEventListener('focusin', () => {
    paused = true;
    syncRotation();
  });
  document.addEventListener('visibilitychange', syncRotation);
  motion.addEventListener('change', () => {
    if (motion.matches) paused = true;
    syncRotation();
  });
  showSlide(0);
  controls.hidden = false;
  syncRotation();
});
