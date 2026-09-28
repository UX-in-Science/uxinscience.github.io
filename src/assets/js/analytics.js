(() => {
  const script = document.currentScript;
  const measurementId = script?.dataset.measurementId;
  // Keep local development and alternate preview hosts out of production reports.
  if (!/^G-[A-Z0-9]+$/.test(measurementId || '') ||
      window.location.hostname !== script.dataset.hostname) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', measurementId);

  const tag = document.createElement('script');
  tag.async = true;
  tag.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(tag);
})();
