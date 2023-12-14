/** @type {import('tailwindcss').Config} */
module.exports = {
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
  content: ["./**/templates/**/*.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        gruv: {
          red: {
            50: "#fb4934",
            100: "#cc241d",
            200: "#9d0006",
          },
          orange: {
            50: "#fe8019",
            100: "#d65d0e",
            200: "#af3a03",
          },
          yellow: {
            50: "#fabd2f",
            100: "#d79921",
            200: "#b57614",
          },
          green: {
            50: "#b8bb26",
            100: "#98971a",
            200: "#79740e",
          },
          aqua: {
            50: "#8ec07c",
            100: "#689d6a",
            200: "#427b58",
          },
          blue: {
            50: "#83a598",
            100: "#458588",
            200: "#076678",
          },
          purple: {
            50: "#d3869b",
            100: "#b16286",
            200: "#8f3f71",
          },
          50: "#fbf1c7",
          100: "#ebdbb2",
          200: "#d5c4a1",
          300: "#bdae93",
          400: "#a89984",
          500: "#7c6f64",
          600: "#665c54",
          700: "#504945",
          800: "#3c3836",
          850: "#32302f",
          900: "#282828",
          950: "#1d2021",

          bg: "#282828",
          fg: "#ebdbb2",
        },
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            a: {
              textDecoration: "none",
              "&:hover": {
                textDecoration: "underline",
              },
              "&:visited": {},
            },
          },
        },
      }),
    },
    fontFamily: {
      sans: [
        "sans-serif",
        "Apple Color Emoji",
        "Segoe UI Emoji",
        "Segoe UI Symbol",
        "Noto Color Emoji",
      ],
      serif: [
        "serif",
        "Apple Color Emoji",
        "Segoe UI Emoji",
        "Segoe UI Symbol",
        "Noto Color Emoji",
      ],
    },
  },
};
