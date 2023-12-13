/** @type {import('tailwindcss').Config} */
module.exports = {
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
  content: ["./**/templates/**/*.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        red: "#fb4934",
        orange: "#fe8019",
        yellow: "#fabd2f",
        green: "#b8bb26",
        aqua: "#8ec07c",
        blue: "#83a598",
        purple: "#d3869b",

        red_d: "#cc241d",
        orange_d: "#d65d0e",
        yellow_d: "#d79921",
        green_d: "#98971a",
        aqua_d: "#689d6a",
        blue_d: "#458588",
        purple_d: "#b16286",

        gruv: {
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
        },

        bg: "#282828",
        fg: "#ebdbb2",
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            a: {
              color: theme("colors.blue"),
              textDecoration: "none",
              "&:hover": {
                textDecoration: "underline",
              },
              "&:visited": {
                color: theme("colors.blue"),
              },
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
