export function initLangSwitcher(): void {
    console.log('initLangSwitcher');
    const form = <HTMLFormElement>document.getElementById("lang-form");
    const input = <HTMLInputElement>document.getElementById("lang-input");
    const pills = document.querySelectorAll<HTMLButtonElement>(".lang-pill");

    if (!form || !input || pills.length === 0) return;

    pills.forEach((pill) => {
      pill.addEventListener("click", () => {
        const lang = pill.dataset?.lang;
        if (!lang) return;

        input.value = lang;

        pills.forEach((p: HTMLButtonElement) => {
          const isActive = p === pill;
          p.classList.toggle("is-active", isActive);
          p.setAttribute("aria-checked", isActive ? "true" : "false");
        });

        form.submit();
      });
    });
}
