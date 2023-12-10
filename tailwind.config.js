/** @type {import('tailwindcss').Config} */
module.exports = {
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
  content: ["./**/templates/**/*.html"],
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

        bg0_h: "#1d2021",
        bg0: "#282828",
        bg: "#282828",
        bg0_s: "#32302f",
        bg1: "#3c3836",
        bg2: "#504945",
        bg3: "#665c54",
        bg4: "#7c6f64",

        grey: "#928374",
        fg4: "#a89984",
        fg3: "#bdae93",
        fg2: "#d5c4a1",
        fg1: "#ebdbb2",
        fg0: "#fbf1c7",
        fg: "#ebdbb2",

        muted: "#a89984",
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            "--tw-prose-headings": theme("colors.fg"),
            "--tw-prose-captions": theme("colors.muted"),
            color: theme("colors.fg"),
            strong: theme("colors.fg"),
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
