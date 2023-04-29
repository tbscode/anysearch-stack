/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial':
          'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      colors: {
        'background': '#202328',
        'darkground': '#181A1E',
        'grayout': '#959595',
        'softwhite': '#F8F8F8',
      },
      animation: {
        'wiggle': 'wiggle 1.2s ease-in-out infinite',
      },
      keyframes: {
        wiggle: {
          '0%, 100%': { transform: 'translateY(-7px)' },
          '50%': { transform: 'translateY(7px)' },
        }
      }
    },
  },
  plugins: [require('daisyui')],
};
