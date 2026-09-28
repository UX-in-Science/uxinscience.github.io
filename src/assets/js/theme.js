(() => {
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
  let preference;
  try {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") preference = saved;
  } catch {}

  function applyTheme() {
    const theme = preference || (systemTheme.matches ? "dark" : "light");
    const dark = theme === "dark";
    document.documentElement.dataset.theme = theme;
    document.querySelectorAll("[data-theme-logo]").forEach((source) => {
      source.media = dark ? "all" : "not all";
    });
    document.querySelectorAll('meta[name="theme-color"]').forEach((meta) => {
      meta.removeAttribute("media");
      meta.content = dark ? "#010A00" : "#F7FFF6";
    });
    const button = document.querySelector(".theme-toggle");
    if (button) {
      button.hidden = false;
      button.setAttribute("aria-pressed", String(dark));
      button.title = `Switch to ${dark ? "light" : "dark"} mode`;
    }
  }

  applyTheme();
  document.addEventListener("DOMContentLoaded", () => {
    applyTheme();
    document.querySelector(".theme-toggle")?.addEventListener("click", () => {
      preference = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      try {
        localStorage.setItem("theme", preference);
      } catch {}
      applyTheme();
    });
  });
  systemTheme.addEventListener("change", applyTheme);
})();
