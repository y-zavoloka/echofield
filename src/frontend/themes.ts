export interface ThemeColors {
  // Catppuccin palette
  rosewater: string;
  flamingo: string;
  pink: string;
  mauve: string;
  red: string;
  maroon: string;
  peach: string;
  yellow: string;
  green: string;
  teal: string;
  sky: string;
  sapphire: string;
  blue: string;
  lavender: string;
  // Text and surface
  text: string;
  subtext1: string;
  subtext0: string;
  overlay2: string;
  overlay1: string;
  overlay0: string;
  surface2: string;
  surface1: string;
  surface0: string;
  base: string;
  mantle: string;
  crust: string;
}

export interface Theme {
  id: string;
  name: string;
  colors: ThemeColors;
}

export const themes: Theme[] = [
  // Catppuccin Latte
  {
    id: "latte",
    name: "Catppuccin Latte",
    colors: {
      rosewater: "#dc8a78",
      flamingo: "#dd7878",
      pink: "#ea76cb",
      mauve: "#8839ef",
      red: "#d20f39",
      maroon: "#e64553",
      peach: "#fe640b",
      yellow: "#df8e1d",
      green: "#40a02b",
      teal: "#179299",
      sky: "#04a5e5",
      sapphire: "#209fb5",
      blue: "#1e66f5",
      lavender: "#7287fd",
      text: "#4c4f69",
      subtext1: "#5c5f77",
      subtext0: "#6c6f85",
      overlay2: "#7c7f93",
      overlay1: "#8c8fa1",
      overlay0: "#9ca0b0",
      surface2: "#acb0be",
      surface1: "#bcc0cc",
      surface0: "#ccd0da",
      base: "#eff1f5",
      mantle: "#e6e9ef",
      crust: "#dce0e8",
    },
  },
  // Catppuccin Frappe
  {
    id: "frappe",
    name: "Catppuccin Frappe",
    colors: {
      rosewater: "#f2d5cf",
      flamingo: "#eebebe",
      pink: "#f4b8e4",
      mauve: "#ca9ee6",
      red: "#e78284",
      maroon: "#ea999c",
      peach: "#ef9f76",
      yellow: "#e5c890",
      green: "#a6d189",
      teal: "#81c8be",
      sky: "#99d1db",
      sapphire: "#85c1dc",
      blue: "#8caaee",
      lavender: "#babbf1",
      text: "#c6d0f5",
      subtext1: "#b5bfe2",
      subtext0: "#a5adce",
      overlay2: "#949cbb",
      overlay1: "#838ba7",
      overlay0: "#737994",
      surface2: "#626880",
      surface1: "#51576d",
      surface0: "#414559",
      base: "#303446",
      mantle: "#292c3c",
      crust: "#232634",
    },
  },
  // Catppuccin Macchiato
  {
    id: "macchiato",
    name: "Catppuccin Macchiato",
    colors: {
      rosewater: "#f4dbd6",
      flamingo: "#f0c6c6",
      pink: "#f5bde6",
      mauve: "#c6a0f6",
      red: "#ed8796",
      maroon: "#ee99a0",
      peach: "#f5a97f",
      yellow: "#eed49f",
      green: "#a6da95",
      teal: "#8bd5ca",
      sky: "#91d7e3",
      sapphire: "#7dc4e4",
      blue: "#8aadf4",
      lavender: "#b7bdf8",
      text: "#cad3f5",
      subtext1: "#b8c0e0",
      subtext0: "#a5adcb",
      overlay2: "#939ab7",
      overlay1: "#8087a2",
      overlay0: "#6e738d",
      surface2: "#5b6078",
      surface1: "#494d64",
      surface0: "#363a4f",
      base: "#24273a",
      mantle: "#1e2030",
      crust: "#181926",
    },
  },
  // Catppuccin Mocha
  {
    id: "mocha",
    name: "Catppuccin Mocha",
    colors: {
      rosewater: "#f5e0dc",
      flamingo: "#f2cdcd",
      pink: "#f5c2e7",
      mauve: "#cba6f7",
      red: "#f38ba8",
      maroon: "#eba0ac",
      peach: "#fab387",
      yellow: "#f9e2af",
      green: "#a6e3a1",
      teal: "#94e2d5",
      sky: "#89dceb",
      sapphire: "#74c7ec",
      blue: "#89b4fa",
      lavender: "#b4befe",
      text: "#cdd6f4",
      subtext1: "#bac2de",
      subtext0: "#a6adc8",
      overlay2: "#9399b2",
      overlay1: "#7f849c",
      overlay0: "#6c7086",
      surface2: "#585b70",
      surface1: "#45475a",
      surface0: "#313244",
      base: "#1e1e2e",
      mantle: "#181825",
      crust: "#11111b",
    },
  },
  // Nord
  {
    id: "nord",
    name: "Nord",
    colors: {
      rosewater: "#bf616a",
      flamingo: "#bf616a",
      pink: "#b48ead",
      mauve: "#b48ead",
      red: "#bf616a",
      maroon: "#bf616a",
      peach: "#d08770",
      yellow: "#ebcb8b",
      green: "#a3be8c",
      teal: "#8fbcbb",
      sky: "#88c0d0",
      sapphire: "#5e81ac",
      blue: "#5e81ac",
      lavender: "#81a1c1",
      text: "#2e3440",
      subtext1: "#3b4252",
      subtext0: "#434c5e",
      overlay2: "#4c566a",
      overlay1: "#5e81ac",
      overlay0: "#81a1c1",
      surface2: "#88c0d0",
      surface1: "#8fbcbb",
      surface0: "#d8dee9",
      base: "#eceff4",
      mantle: "#e5e9f0",
      crust: "#d8dee9",
    },
  },
  // Tokyo Night Day
  {
    id: "tokyo-day",
    name: "Tokyo Night Day",
    colors: {
      rosewater: "#c0caf5",
      flamingo: "#bb9af7",
      pink: "#bb9af7",
      mauve: "#9d7cd8",
      red: "#f7768e",
      maroon: "#f7768e",
      peach: "#ff9e64",
      yellow: "#e0af68",
      green: "#9ece6a",
      teal: "#2ac3de",
      sky: "#7dcfff",
      sapphire: "#7aa2f7",
      blue: "#7aa2f7",
      lavender: "#bb9af7",
      text: "#1a1b26",
      subtext1: "#2f3549",
      subtext0: "#414868",
      overlay2: "#565f89",
      overlay1: "#737aa2",
      overlay0: "#9aa5ce",
      surface2: "#c0caf5",
      surface1: "#c9d1f9",
      surface0: "#d5d9f0",
      base: "#e1e2e7",
      mantle: "#d5d6db",
      crust: "#c9c9d1",
    },
  },
  // Tokyo Night Night
  {
    id: "tokyo-night",
    name: "Tokyo Night",
    colors: {
      rosewater: "#c0caf5",
      flamingo: "#bb9af7",
      pink: "#bb9af7",
      mauve: "#9d7cd8",
      red: "#f7768e",
      maroon: "#f7768e",
      peach: "#ff9e64",
      yellow: "#e0af68",
      green: "#9ece6a",
      teal: "#2ac3de",
      sky: "#7dcfff",
      sapphire: "#7aa2f7",
      blue: "#7aa2f7",
      lavender: "#bb9af7",
      text: "#c0caf5",
      subtext1: "#a9b1d6",
      subtext0: "#9aa5ce",
      overlay2: "#737aa2",
      overlay1: "#565f89",
      overlay0: "#414868",
      surface2: "#2f3549",
      surface1: "#24283b",
      surface0: "#1a1b26",
      base: "#1a1b26",
      mantle: "#16161e",
      crust: "#13141a",
    },
  },
  // Gruvbox Light
  {
    id: "gruvbox-light",
    name: "Gruvbox Light",
    colors: {
      rosewater: "#cc241d",
      flamingo: "#cc241d",
      pink: "#b16286",
      mauve: "#b16286",
      red: "#cc241d",
      maroon: "#cc241d",
      peach: "#d65d0e",
      yellow: "#d79921",
      green: "#98971a",
      teal: "#689d6a",
      sky: "#458588",
      sapphire: "#458588",
      blue: "#458588",
      lavender: "#b16286",
      text: "#3c3836",
      subtext1: "#504945",
      subtext0: "#665c54",
      overlay2: "#7c6f64",
      overlay1: "#928374",
      overlay0: "#a89984",
      surface2: "#bdae93",
      surface1: "#d5c4a1",
      surface0: "#ebdbb2",
      base: "#fbf1c7",
      mantle: "#f2e5bc",
      crust: "#ebdbb2",
    },
  },
  // Gruvbox Dark
  {
    id: "gruvbox-dark",
    name: "Gruvbox Dark",
    colors: {
      rosewater: "#fb4934",
      flamingo: "#fb4934",
      pink: "#b16286",
      mauve: "#b16286",
      red: "#fb4934",
      maroon: "#fb4934",
      peach: "#fe8019",
      yellow: "#fabd2f",
      green: "#b8bb26",
      teal: "#8ec07c",
      sky: "#83a598",
      sapphire: "#83a598",
      blue: "#83a598",
      lavender: "#b16286",
      text: "#ebdbb2",
      subtext1: "#d5c4a1",
      subtext0: "#bdae93",
      overlay2: "#a89984",
      overlay1: "#928374",
      overlay0: "#7c6f64",
      surface2: "#665c54",
      surface1: "#504945",
      surface0: "#3c3836",
      base: "#282828",
      mantle: "#1d2021",
      crust: "#1d2021",
    },
  },
];

export const DEFAULT_THEME = "macchiato";

export function getThemeById(id: string): Theme | undefined {
  return themes.find((theme) => theme.id === id);
}

export function generateThemeCSS(theme: Theme): string {
  const colors = theme.colors;
  return `
:root[data-theme="${theme.id}"] {
  /* Catppuccin palette */
  --ctp-rosewater: ${colors.rosewater};
  --ctp-flamingo: ${colors.flamingo};
  --ctp-pink: ${colors.pink};
  --ctp-mauve: ${colors.mauve};
  --ctp-red: ${colors.red};
  --ctp-maroon: ${colors.maroon};
  --ctp-peach: ${colors.peach};
  --ctp-yellow: ${colors.yellow};
  --ctp-green: ${colors.green};
  --ctp-teal: ${colors.teal};
  --ctp-sky: ${colors.sky};
  --ctp-sapphire: ${colors.sapphire};
  --ctp-blue: ${colors.blue};
  --ctp-lavender: ${colors.lavender};

  --ctp-text: ${colors.text};
  --ctp-subtext1: ${colors.subtext1};
  --ctp-subtext0: ${colors.subtext0};
  --ctp-overlay2: ${colors.overlay2};
  --ctp-overlay1: ${colors.overlay1};
  --ctp-overlay0: ${colors.overlay0};
  --ctp-surface2: ${colors.surface2};
  --ctp-surface1: ${colors.surface1};
  --ctp-surface0: ${colors.surface0};
  --ctp-base: ${colors.base};
  --ctp-mantle: ${colors.mantle};
  --ctp-crust: ${colors.crust};

  /* Semantic tokens */
  --bg: var(--ctp-base);
  --bg-elevated: var(--ctp-mantle);
  --bg-header: ${colors.base}E6;
  --text: var(--ctp-text);
  --text-muted: var(--ctp-subtext0);
  --accent: var(--ctp-blue);
  --accent-soft: ${hexToRgba(colors.blue, 0.12)};
  --accent-strong: var(--ctp-sapphire);
  --accent-contrast: ${getContrastColor(colors.base)};
  --border-subtle: var(--ctp-surface0);
  --border-strong: var(--ctp-surface1);
  --shadow-soft: ${getShadowColor(colors.base)};
}
`;
}

function hexToRgba(hex: string, alpha: number): string {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function getContrastColor(bgColor: string): string {
  // Simple check: if base is light, use dark text, else light text
  const r = parseInt(bgColor.slice(1, 3), 16);
  const g = parseInt(bgColor.slice(3, 5), 16);
  const b = parseInt(bgColor.slice(5, 7), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 128 ? "#000000" : "#ffffff";
}

function getShadowColor(bgColor: string): string {
  const r = parseInt(bgColor.slice(1, 3), 16);
  const g = parseInt(bgColor.slice(3, 5), 16);
  const b = parseInt(bgColor.slice(5, 7), 16);
  // Dark shadow for light themes, light shadow for dark themes
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  if (brightness > 128) {
    return `0 8px 16px rgba(15, 23, 42, 0.06)`;
  } else {
    return `0 8px 16px rgba(0, 0, 0, 0.3)`;
  }
}
