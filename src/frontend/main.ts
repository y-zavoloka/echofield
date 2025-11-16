import "./base.css";
import { initLangSwitcher } from "./lang-switcher";
import { initThemeSwitcher } from "./theme-switcher";


const init = () => {
  initThemeSwitcher();
  initLangSwitcher();
}

// Initialize theme switcher when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
