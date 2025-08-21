 tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'primary': {
                            50: '#f0f9ff',
                            100: '#e0f2fe',
                            500: '#0ea5e9',
                            600: '#0284c7',
                            700: '#0369a1',
                        },
                        'accent': {
                            500: '#10b981',
                            600: '#059669',
                        }
                    },
                    animation: {
                        'fade-in': 'fadeIn 0.6s ease-out',
                        'slide-up': 'slideUp 0.8s ease-out',
                        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
                    }
                }
            }
        }