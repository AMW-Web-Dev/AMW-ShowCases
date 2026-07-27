# Frontend Constitution

## Frontend Philosophy
- **HTMX-first**: All dynamic interactions via HTMX
- **Progressive enhancement**: Works without JavaScript
- **Professional aesthetic**: Clean, modern, impressive
- **Mobile-responsive**: Looks great on all devices

## HTMX Law

### Usage Patterns
```html
<!-- GET request for content -->
<button hx-get="/blog/list/" hx-target="#content">Load Blog</button>

<!-- POST request for forms -->
<form hx-post="/blog/create/" hx-target="#result">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create</button>
</html>

<!-- Swapping strategies -->
<div hx-get="/data/" hx-swap="innerHTML" hx-trigger="every 30s"></div>
```

### HTMX Attributes
- `hx-get`, `hx-post`, `hx-put`, `hx-delete`: HTTP methods
- `hx-target`: Where to put response
- `hx-swap`: How to swap (innerHTML, outerHTML, beforeend, etc.)
- `hx-trigger`: When to trigger (click, submit, every 30s, etc.)
- `hx-indicator`: Loading indicator CSS class

### HTMX Response Format
```python
# Django view returning HTML fragment
def blog_list_view(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/components/post_list.html', {'posts': posts})
```

## Bootstrap Law

### CDN Links (in base.html)
```html
<!-- CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

### Component Usage
```html
<!-- Cards -->
<div class="card">
    <img src="..." class="card-img-top" alt="...">
    <div class="card-body">
        <h5 class="card-title">Project Title</h5>
        <p class="card-text">Description</p>
        <a href="#" class="btn btn-primary">View Details</a>
    </div>
</div>

<!-- Navigation -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="/">AMW Portfolio</a>
        <div class="navbar-nav">
            <a class="nav-link" href="/skills/">Skills</a>
            <a class="nav-link" href="/projects/">Projects</a>
            <a class="nav-link" href="/blog/">Blog</a>
        </div>
    </div>
</nav>

<!-- Grid System -->
<div class="row">
    <div class="col-md-6">Left content</div>
    <div class="col-md-6">Right content</div>
</div>
```

### Custom Styling
```css
/* Add to static/css/custom.css */
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --accent-color: #3b82f6;
    --text-color: #1f2937;
    --bg-color: #ffffff;
}

/* Professional card styling */
.card {
    border: none;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-5px);
}
```

## Template Law

### Base Template Structure
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AMW Portfolio{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'css/custom.css' %}" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'components/navbar.html' %}
    
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    
    {% include 'components/footer.html' %}
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Template Inheritance
```html
<!-- Child template -->
{% extends 'base.html' %}

{% block title %}Blog - AMW Portfolio{% endblock %}

{% block content %}
<h1>Blog Posts</h1>
<div id="blog-list">
    {% include 'blog/components/post_list.html' %}
</div>
{% endblock %}
```

### Template Components
```html
<!-- Component structure -->
templates/
├── base.html
├── components/
│   ├── navbar.html
│   ├── footer.html
│   ├── card.html
│   └── pagination.html
├── core/
│   ├── homepage.html
│   └── components/
├── blog/
│   ├── blog_list.html
│   ├── blog_detail.html
│   └── components/
└── ...
```

## CSS Law

### File Structure
```
static/
├── css/
│   ├── custom.css          # Global custom styles
│   ├── variables.css       # CSS variables (colors, spacing)
│   └── components/
│       ├── cards.css       # Card component styles
│       ├── navigation.css  # Navbar styles
│       └── forms.css       # Form styles
├── js/
│   ├── custom.js           # Global JavaScript
│   └── components/
│       ├── animations.js   # Scroll animations
│       └── forms.js        # Form validation
└── images/
    ├── logo.png
    ├── favicon.ico
    └── og-image.png        # Social sharing image
```

### CSS Variables
```css
/* static/css/variables.css */
:root {
    /* Colors */
    --color-primary: #2563eb;
    --color-primary-dark: #1e40af;
    --color-secondary: #64748b;
    --color-accent: #3b82f6;
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
    
    /* Text */
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --text-muted: #9ca3af;
    
    /* Backgrounds */
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --bg-dark: #111827;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Border radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.375rem;
    --radius-lg: 0.5rem;
    --radius-xl: 0.75rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

## Responsive Design Law

### Breakpoints (Bootstrap standard)
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
```html
<!-- Mobile: stack, Desktop: side by side -->
<div class="row">
    <div class="col-12 col-md-6">Left</div>
    <div class="col-12 col-md-6">Right</div>
</div>

<!-- Hide on mobile, show on desktop -->
<div class="d-none d-md-block">Desktop only</div>

<!-- Show on mobile, hide on desktop -->
<div class="d-md-none">Mobile only</div>
```

## Animation Law

### HTMX Animations
```html
<!-- Fade in -->
<div hx-get="/data/" hx-swap="innerHTML" class="fade-in">
    Content
</div>

<!-- Loading indicator -->
<button hx-get="/load/" hx-indicator="#spinner">
    <span id="spinner" class="spinner-border spinner-border-sm d-none"></span>
    Load Data
</button>
```

### CSS Animations
```css
/* Scroll reveal */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal.active {
    opacity: 1;
    transform: translateY(0);
}

/* Card hover */
.card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}
```

## Accessibility Law

### Semantic HTML
```html
<!-- Use semantic elements -->
<header>
<nav>
<main>
<article>
<section>
<aside>
<footer>

<!-- ARIA labels -->
<button aria-label="Close menu">×</button>
<nav aria-label="Main navigation">...</nav>
```

### Keyboard Navigation
```html
<!-- Focusable elements -->
<a href="/link/" tabindex="0">Link</a>
<button tabindex="0">Button</button>

<!-- Skip navigation -->
<a href="#main-content" class="visually-hidden">Skip to main content</a>
<main id="main-content">...</main>
```

## Performance Law

### Image Optimization
```html
<!-- Lazy loading -->
<img src="image.webp" alt="Description" loading="lazy" width="800" height="600">

<!-- Responsive images -->
<img srcset="image-320w.webp 320w,
             image-640w.webp 640w,
             image-1280w.webp 1280w"
     sizes="(max-width: 320px) 280px,
            (max-width: 640px) 640px,
            1280px"
     src="image-1280w.webp"
     alt="Description">
```

### Code Splitting
```html
<!-- Load HTMX only where needed -->
{% if use_htmx %}
<script src="https://unpkg.com/htmx.org@1.9.12"></script>
{% endif %}
```

## Security Law

### XSS Prevention
```html
<!-- Django auto-escapes -->
{{ user_input }}  <!-- Safe -->

<!-- Mark safe only when you control the content -->
{{ trusted_content|safe }}

<!-- Never trust user input -->
{% autoescape on %}
    {{ user_content }}
{% endautoescape %}
```

### CSRF Protection
```html
<!-- Always include CSRF token -->
<form method="post">
    {% csrf_token %}
    ...
</form>
```

## Testing Law

### Visual Testing
- Manual testing on multiple devices
- Browser compatibility (Chrome, Firefox, Safari)
- Mobile responsiveness verification
- Accessibility testing with screen readers

### No Automated Frontend Tests
- Keep it simple for portfolio
- Focus on backend testing
- Manual QA for frontend
