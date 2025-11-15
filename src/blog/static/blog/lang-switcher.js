document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("lang-form");
  const input = document.getElementById("lang-input");
  const pills = document.querySelectorAll(".lang-pill");

  if (!form || !input || pills.length === 0) return;

  pills.forEach((pill) => {
    pill.addEventListener("click", () => {
      const lang = pill.dataset.lang;
      if (!lang) return;

      input.value = lang;

      pills.forEach((p) => {
        const isActive = p === pill;
        p.classList.toggle("is-active", isActive);
        p.setAttribute("aria-checked", isActive ? "true" : "false");
      });

      form.submit();
    });
  });
});
