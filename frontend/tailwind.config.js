/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#07111f",
        panel: "#0b1929",
        line: "#173047",
        cyan: "#79d9df",
        teal: "#40b4a8",
        mint: "#9ee5d1"
      },
      boxShadow: {
        panel: "0 18px 60px rgba(0, 0, 0, 0.32)",
        cyan: "0 12px 32px rgba(121, 217, 223, 0.12)"
      }
    }
  },
  plugins: []
}
