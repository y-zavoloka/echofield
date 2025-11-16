import { themes, DEFAULT_THEME, getThemeById } from "./themes";

const THEME_STORAGE_KEY = "echofield-theme";
const THEME_COOKIE_NAME = "theme";

export function initThemeSwitcher(): void {
  const themeSwitcher = document.getElementById("theme-switcher");
  const modal = document.getElementById("theme-switcher-modal") as HTMLDialogElement | null;
  const trigger = document.getElementById("theme-switcher-trigger");
  const closeButton = modal?.querySelector<HTMLButtonElement>(".theme-switcher-close");

  if (!themeSwitcher || !modal) return;

  const buttons = themeSwitcher.querySelectorAll<HTMLButtonElement>(
    "[data-theme-id]"
  );
  if (buttons.length === 0) return;

  // Get current theme from storage or cookie
  const currentTheme = getCurrentTheme();

  // Set initial theme
  setTheme(currentTheme, false);

  // Mark active theme button on page load
  updateThemeButtons(currentTheme);

  // Open modal when trigger is clicked
  trigger?.addEventListener("click", () => {
    modal.showModal();
  });

  // Close modal when close button is clicked
  closeButton?.addEventListener("click", () => {
    modal.close();
  });

  // Close modal when clicking outside (on backdrop)
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.close();
    }
  });

  // Close modal on Escape key
  modal.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      modal.close();
    }
  });

  // Add click handlers for theme selection
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const themeId = button.dataset.themeId;
      if (themeId) {
        setTheme(themeId, true);
        // Close modal after selection
        modal.close();
      }
    });
  });
}

function getCurrentTheme(): string {
  // Try localStorage first
  const stored = localStorage.getItem(THEME_STORAGE_KEY);
  if (stored && getThemeById(stored)) {
    return stored;
  }

  // Try cookie
  const cookie = getCookie(THEME_COOKIE_NAME);
  if (cookie && getThemeById(cookie)) {
    return cookie;
  }

  // Default theme
  return DEFAULT_THEME;
}

function setTheme(themeId: string, updateUI: boolean): void {
  const theme = getThemeById(themeId);
  if (!theme) {
    console.warn(`Theme ${themeId} not found`);
    return;
  }

  // Update DOM
  document.documentElement.setAttribute("data-theme", themeId);

  // Update storage
  localStorage.setItem(THEME_STORAGE_KEY, themeId);

  // Update cookie (expires in 1 year)
  const expires = new Date();
  expires.setFullYear(expires.getFullYear() + 1);
  document.cookie = `${THEME_COOKIE_NAME}=${themeId}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;

  // Update UI if needed
  if (updateUI) {
    updateThemeButtons(themeId);
  }
}

function updateThemeButtons(activeThemeId: string): void {
  const themeSwitcher = document.getElementById("theme-switcher");
  if (!themeSwitcher) return;

  const buttons = themeSwitcher.querySelectorAll<HTMLButtonElement>(
    "[data-theme-id]"
  );

  buttons.forEach((button) => {
    const isActive = button.dataset.themeId === activeThemeId;
    if (isActive) {
      button.classList.add("is-active");
      button.setAttribute("aria-checked", "true");
    } else {
      button.classList.remove("is-active");
      button.setAttribute("aria-checked", "false");
    }
  });
}

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(";").shift() || null;
  }
  return null;
}

// Export themes for use in templates
export { themes, DEFAULT_THEME };
