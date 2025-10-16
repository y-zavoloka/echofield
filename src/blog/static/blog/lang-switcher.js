document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("lang-switcher");
  if (!select) return;

  select.addEventListener("change", () => {
    const form = document.getElementById("lang-form");
    form.submit();
  });
});
