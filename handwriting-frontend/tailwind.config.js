/** @type {import('tailwindcss').Config} */
module.exports = {
  // Update the paths as per your project structure
  content: ['./src/**/*.{html,js,jsx,ts,tsx,vue}'],

  theme: {
    extend: {
      aspectRatio: {
        '4/3': '4 / 3',
        '100/141': '100 / 141', // Make sure to remove any spaces around slashes if you encounter issues.
      },
      colors: {
        orange: {
          50: '#FEF6E8',   // Lightest
          100: '#FEECD1',
          200: '#FDD8A3',
          300: '#FCC576',
          400: '#F7B345',   // Base color
          500: '#DC9C3C',
          600: '#BF8534',
          700: '#9F6D2B',
          800: '#7F5622',
          900: '#66431B'    // Darkest
        }
      }
    },
  },
  plugins: [],
}
