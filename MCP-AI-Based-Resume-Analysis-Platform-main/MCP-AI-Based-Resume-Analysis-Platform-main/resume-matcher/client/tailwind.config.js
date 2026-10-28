/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      backgroundOpacity: {
        3: "0.03",
        6: "0.06",
      },
    },
  },
  plugins: [],
};
