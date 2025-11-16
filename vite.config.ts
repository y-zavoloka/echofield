import { defineConfig, Plugin } from "vite";
import { resolve } from "path";
import { execSync } from "child_process";

// Plugin to generate themes CSS before build
function generateThemesPlugin(): Plugin {
  return {
    name: "generate-themes",
    buildStart() {
      try {
        execSync("npm run generate-themes", { stdio: "inherit" });
      } catch (error) {
        console.warn("Failed to generate themes, continuing anyway:", error);
      }
    },
  };
}

export default defineConfig({
  plugins: [generateThemesPlugin()],
  build: {
    outDir: "src/blog/static/blog",
    emptyOutDir: false,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "src/frontend/main.ts"),
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith(".css")) {
            // Output base.css as main.css to match template expectations
            if (assetInfo.name === "base.css") {
              return "main.css";
            }
            return "[name][extname]";
          }
          return "[name][extname]";
        },
      },
    },
    cssCodeSplit: false,
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "src/frontend"),
    },
  },
});
