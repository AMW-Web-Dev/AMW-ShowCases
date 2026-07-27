# Design Constitution

## Design Philosophy
- **Professional aesthetic**: Clean, modern, impressive
- **Consistent branding**: Unified color scheme and typography
- **Mobile-first**: Responsive design for all devices
- **Accessibility**: WCAG 2.1 AA compliance

## Color System Law

### Primary Colors
```css
:root {
    /* Primary - Professional Blue */
    --color-primary: #2563eb;
    --color-primary-dark: #1e40af;
    --color-primary-light: #3b82f6;
    
    /* Secondary - Slate Gray */
    --color-secondary: #64748b;
    --color-secondary-dark: #475569;
    --color-secondary-light: #94a3b8;
    
    /* Accent - Vibrant Blue */
    --color-accent: #3b82f6;
    
    /* Success - Green */
    --color-success: #10b981;
    --color-success-dark: #059669;
    
    /* Warning - Amber */
    --color-warning: #f59e0b;
    --color-warning-dark: #d97706;
    
    /* Danger - Red */
    --color-danger: #ef4444;
    --color-danger-dark: #dc2626;
    
    /* Neutral - Gray Scale */
    --color-white: #ffffff;
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-200: #e5e7eb;
    --color-gray-300: #d1d5db;
    --color-gray-400: #9ca3af;
    --color-gray-500: #6b7280;
    --color-gray-600: #4b5563;
    --color-gray-700: #374151;
    --color-gray-800: #1f2937;
    --color-gray-900: #111827;
    --color-black: #000000;
}
```

### Dark Mode (Optional)
```css
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
    }
}
```

## Typography Law

### Font Stack
```css
:root {
    /* Primary - Inter */
    --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    
    /* Monospace - JetBrains Mono */
    --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    
    /* Heading - Inter (bold) */
    --font-heading: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

### Font Sizes
```css
:root {
    /* Type Scale */
    --text-xs: 0.75rem;      /* 12px */
    --text-sm: 0.875rem;     /* 14px */
    --text-base: 1rem;       /* 16px */
    --text-lg: 1.125rem;     /* 18px */
    --text-xl: 1.25rem;      /* 20px */
    --text-2xl: 1.5rem;      /* 24px */
    --text-3xl: 1.875rem;    /* 30px */
    --text-4xl: 2.25rem;     /* 36px */
    --text-5xl: 3rem;        /* 48px */
    --text-6xl: 3.75rem;     /* 60px */
    
    /* Line Heights */
    --leading-tight: 1.25;
    --leading-normal: 1.5;
    --leading-relaxed: 1.75;
}
```

### Font Weights
```css
:root {
    --font-light: 300;
    --font-normal: 400;
    --font-medium: 500;
    --font-semibold: 600;
    --font-bold: 700;
    --font-extrabold: 800;
}
```

## Spacing Law

### Spacing Scale
```css
:root {
    /* Spacing */
    --space-0: 0;
    --space-1: 0.25rem;    /* 4px */
    --space-2: 0.5rem;     /* 8px */
    --space-3: 0.75rem;    /* 12px */
    --space-4: 1rem;       /* 16px */
    --space-5: 1.25rem;    /* 20px */
    --space-6: 1.5rem;     /* 24px */
    --space-8: 2rem;       /* 32px */
    --space-10: 2.5rem;    /* 40px */
    --space-12: 3rem;      /* 48px */
    --space-16: 4rem;      /* 64px */
    --space-20: 5rem;      /* 80px */
    --space-24: 6rem;      /* 96px */
}
```

### Layout Spacing
```css
/* Container */
.container {
    max-width: 1280px;
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--space-4);
    padding-right: var(--space-4);
}

/* Section spacing */
.section {
    padding-top: var(--space-16);
    padding-bottom: var(--space-16);
}

/* Card spacing */
.card {
    padding: var(--space-6);
    margin-bottom: var(--space-6);
}
```

## Border Radius Law

### Radius Scale
```css
:root {
    --radius-none: 0;
    --radius-sm: 0.25rem;     /* 4px */
    --radius-md: 0.375rem;    /* 6px */
    --radius-lg: 0.5rem;      /* 8px */
    --radius-xl: 0.75rem;     /* 12px */
    --radius-2xl: 1rem;       /* 16px */
    --radius-full: 9999px;    /* Full rounded */
}
```

### Component Radius
```css
/* Buttons */
.btn {
    border-radius: var(--radius-lg);
}

/* Cards */
.card {
    border-radius: var(--radius-xl);
}

/* Input fields */
input, textarea, select {
    border-radius: var(--radius-md);
}

/* Avatars */
.avatar {
    border-radius: var(--radius-full);
}
```

## Shadow Law

### Shadow Scale
```css
:root {
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    
    /* Colored shadows */
    --shadow-primary: 0 4px 14px 0 rgba(37, 99, 235, 0.39);
    --shadow-success: 0 4px 14px 0 rgba(16, 185, 129, 0.39);
}
```

### Component Shadows
```css
/* Cards */
.card {
    box-shadow: var(--shadow-md);
}

.card:hover {
    box-shadow: var(--shadow-lg);
}

/* Buttons */
.btn {
    box-shadow: var(--shadow-sm);
}

.btn:hover {
    box-shadow: var(--shadow-md);
}

/* Dropdowns */
.dropdown-menu {
    box-shadow: var(--shadow-lg);
}
```

## Animation Law

### Transition Timing
```css
:root {
    --transition-fast: 150ms ease-in-out;
    --transition-normal: 200ms ease-in-out;
    --transition-slow: 300ms ease-in-out;
    --transition-slower: 500ms ease-in-out;
}
```

### Animation Examples
```css
/* Button hover */
.btn {
    transition: all var(--transition-fast);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

/* Card hover */
.card {
    transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

/* Fade in */
.fade-in {
    animation: fadeIn var(--transition-slow) ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Slide up */
.slide-up {
    animation: slideUp var(--transition-slow) ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## Component Design Law

### Buttons
```css
/* Primary button */
.btn-primary {
    background-color: var(--color-primary);
    color: var(--color-white);
    border: none;
    padding: var(--space-3) var(--space-6);
    font-weight: var(--font-semibold);
    border-radius: var(--radius-lg);
    transition: all var(--transition-fast);
}

.btn-primary:hover {
    background-color: var(--color-primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-primary);
}

/* Secondary button */
.btn-secondary {
    background-color: transparent;
    color: var(--color-primary);
    border: 2px solid var(--color-primary);
    padding: var(--space-3) var(--space-6);
    font-weight: var(--font-semibold);
    border-radius: var(--radius-lg);
    transition: all var(--transition-fast);
}

.btn-secondary:hover {
    background-color: var(--color-primary);
    color: var(--color-white);
}
```

### Cards
```css
.card {
    background-color: var(--color-white);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-md);
    overflow: hidden;
    transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.card-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.card-body {
    padding: var(--space-6);
}

.card-title {
    font-size: var(--text-xl);
    font-weight: var(--font-bold);
    color: var(--color-gray-900);
    margin-bottom: var(--space-2);
}

.card-text {
    font-size: var(--text-base);
    color: var(--color-gray-600);
    line-height: var(--leading-relaxed);
}
```

### Navigation
```css
.navbar {
    background-color: var(--color-white);
    box-shadow: var(--shadow-sm);
    padding: var(--space-4) 0;
}

.navbar-brand {
    font-size: var(--text-xl);
    font-weight: var(--font-bold);
    color: var(--color-primary);
}

.nav-link {
    color: var(--color-gray-600);
    font-weight: var(--font-medium);
    padding: var(--space-2) var(--space-4);
    transition: color var(--transition-fast);
}

.nav-link:hover,
.nav-link.active {
    color: var(--color-primary);
}
```

## Responsive Design Law

### Breakpoints
```css
/* Mobile first approach */
/* Default: mobile (< 576px) */
/* sm: 576px */
/* md: 768px */
/* lg: 992px */
/* xl: 1200px */
/* xxl: 1400px */
```

### Responsive Examples
```css
/* Mobile: stack, Desktop: side by side */
.row {
    display: flex;
    flex-wrap: wrap;
}

.col-12 {
    width: 100%;
}

@media (min-width: 768px) {
    .col-md-6 {
        width: 50%;
    }
}

/* Hide on mobile, show on desktop */
.d-none {
    display: none;
}

@media (min-width: 768px) {
    .d-md-block {
        display: block;
    }
}
```

## Layout Law

### Grid System
```css
.container {
    max-width: 1280px;
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--space-4);
    padding-right: var(--space-4);
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin-left: calc(var(--space-4) * -1);
    margin-right: calc(var(--space-4) * -1);
}

.col {
    flex: 1;
    padding-left: var(--space-4);
    padding-right: var(--space-4);
}
```

### Flexbox Utilities
```css
.d-flex {
    display: flex;
}

.flex-column {
    flex-direction: column;
}

.justify-content-center {
    justify-content: center;
}

.align-items-center {
    align-items: center;
}

.gap-2 {
    gap: var(--space-2);
}

.gap-4 {
    gap: var(--space-4);
}
```

## Accessibility Law

### Color Contrast
```css
/* Minimum contrast ratios */
/* Normal text: 4.5:1 */
/* Large text: 3:1 */
/* UI components: 3:1 */

/* Example */
.text-primary {
    color: var(--color-primary);  /* #2563eb on white = 4.5:1 */
}

.text-secondary {
    color: var(--color-secondary);  /* #64748b on white = 4.6:1 */
}
```

### Focus States
```css
/* Visible focus for keyboard navigation */
:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

/* Remove outline for mouse users */
:focus:not(:focus-visible) {
    outline: none;
}

/* Show outline only for keyboard users */
:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}
```

### Screen Reader Support
```css
/* Visually hidden but accessible */
.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
```

## Dark Mode Law

### Dark Mode Variables
```css
@media (prefers-color-scheme: dark) {
    :root {
        /* Backgrounds */
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --bg-tertiary: #374151;
        
        /* Text */
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --text-muted: #9ca3af;
        
        /* Borders */
        --border-color: #374151;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
}
```

## Testing Law

### Visual Testing
- Manual testing on multiple devices
- Browser compatibility (Chrome, Firefox, Safari)
- Mobile responsiveness verification
- Accessibility testing with screen readers

### Performance Testing
- Lighthouse score > 90
- First contentful paint < 1.5s
- Largest contentful paint < 2.5s
- Cumulative layout shift < 0.1
