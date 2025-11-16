import { writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { themes, generateThemeCSS } from "./themes.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Generate CSS file with all themes
const outputPath = resolve(__dirname, "../blog/static/blog/themes.css");
let css = "/* Auto-generated theme CSS - do not edit manually */\n\n";

themes.forEach((theme) => {
  css += generateThemeCSS(theme);
});

writeFileSync(outputPath, css, "utf-8");
console.log(`Generated themes.css with ${themes.length} themes`);
