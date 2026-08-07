/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html"],
  // O site usa apenas a config padrão do Tailwind v3 (mesma do cdn.tailwindcss.com).
  // A classe `font-heading` usada no HTML é no-op: o styles.css já aplica
  // font-family: var(--font-heading) em todos os h1-h6.
  theme: {
    extend: {},
  },
  plugins: [],
};
