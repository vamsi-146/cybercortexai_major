/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Base backgrounds
        background: {
          DEFAULT: '#050A0F',
          light: '#0A0F14',
          lighter: '#0F1419',
        },
        surface: {
          DEFAULT: '#0D1219',
          elevated: '#121820',
          higher: '#1A2230',
        },
        border: {
          DEFAULT: '#1E293B',
          light: '#334155',
          accent: '#0891B2',
        },

        // Primary intelligence accent
        primary: {
          DEFAULT: '#06B6D4',
          dark: '#0891B2',
          light: '#22D3EE',
        },

        // Secondary
        secondary: {
          DEFAULT: '#3B82F6',
          dark: '#2563EB',
          light: '#60A5FA',
        },

        // Tertiary
        tertiary: {
          DEFAULT: '#14B8A6',
          dark: '#0D9488',
          light: '#2DD4BF',
        },

        // Security states
        critical: '#EF4444',
        high: '#F97316',
        medium: '#EAB308',
        low: '#22C55E',
        info: '#06B6D4',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        'sm': '2px',
        'DEFAULT': '4px',
        'md': '6px',
        'lg': '8px',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(6, 182, 212, 0.15)',
        'glow-sm': '0 0 10px rgba(6, 182, 212, 0.1)',
        'card': '0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan': 'scan 2s linear infinite',
      },
      keyframes: {
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
      },
    },
  },
  plugins: [],
}
