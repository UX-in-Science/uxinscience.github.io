document.querySelectorAll("[data-copy-link]").forEach((button) => {
  const status = button.parentElement.querySelector("[data-copy-link-status]");

  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      status.textContent = "Link copied!";
    } catch {
      status.textContent = "Could not copy the link. Copy the URL from your browser.";
    }
  });
});
