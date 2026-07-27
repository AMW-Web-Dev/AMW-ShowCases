# Portfolio Website - Module Guidelines

## TL;DR

> **Quick Summary**: Build a modern, elegant portfolio website using Django + HTMX + PostgreSQL with categorized skills, project showcase, and blog functionality.
>
> **Tech Stack**: Django 6.0.7 + HTMX 1.28.0 + PostgreSQL (Neon) + CloudFlare R2
>
> **Modules**:
> - Module 1: Development Phase (Project Setup)
> - Module 2: Landing Page
> - Module 3: About Section
> - Module 4: Skills Section (Accordion-style)
> - Module 5: Projects Section
> - Module 6: Blog Section (with Tags)
> - Module 7: Contact Section
> - Module 8: Admin Dashboard & Analytics
> - Module 9: Production Phase (Deployment & Launch)
>
> **Approach**: Complete thorough planning first, then build once without rebuilding
> **Discussion**: Each module will be discussed individually before implementation

---

## Project Structure

```
AMWShowCase/
├── .agents/                          # Agent configurations
├── Architecture/                     # Phase plans (dynamic - changes as project evolves)
│   ├── Phase_1_Development.md
│   ├── Phase_2_Landing_Page.md
│   └── ...
├── Brand/                            # Visual identity (thumbnails, color palettes)
│   ├── Portfolio_Thumbnail.png
│   └── Color_Palette.css
├── Constitution/                     # Rules & laws (static - rarely changes)
│   ├── Architecture_Law.md
│   ├── Frontend_Law.md
│   ├── Content_Law.md
│   ├── Deployment_Law.md
│   ├── Design_Law.md
│   └── Testing_Law.md
├── config/                           # Django configuration
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                             # Django applications
│   ├── landing/                      # Landing page
│   ├── about/                        # About section
│   ├── skills/                       # Skills with categories
│   ├── projects/                     # Project showcase
│   ├── blog/                         # Blog with tags
│   ├── contact/                      # Contact form
│   ├── analytics/                    # Analytics dashboard
│   └── core/                         # Shared utilities
├── templates/                        # Django templates
│   ├── layouts/                      # Base layouts
│   ├── components/                   # Reusable components
│   └── pages/                        # Page-specific templates
├── static/                           # Static files
│   ├── styles/                       # CSS files
│   ├── scripts/                      # JavaScript files
│   └── images/                       # Static images
├── media/                            # User uploads (CV, project images)
├── utils/                            # Utility scripts
│   ├── git_task_commit.sh
│   ├── deploy.sh
│   └── ...
├── requirements/                     # Python dependencies
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env.example                      # Environment variables template
├── manage.py                         # Django management
├── Dockerfile                        # Docker configuration
├── docker-compose.yml                # Docker Compose
├── pyproject.toml                    # Python project config
└── README.md                         # Documentation
```

---

## Module Guidelines

### Module 1: Development Phase (Project Setup & Configuration)

**Goal**: Set up Django project with all dependencies for development

**Components**:
- Django project structure (using ProjectBootstrapAgent)
- HTMX integration
- PostgreSQL connection (Neon - local development)
- Static files setup
- Environment variables configuration
- Constitution files creation
- Utility scripts (copied from ERP, modified)
- Docker configuration for development
- Package dependencies

**Guidelines**:
- Use ProjectBootstrapAgent for initial setup
- Follow Django best practices
- Use django-environ for configuration
- Create Constitution files for governance
- Copy and modify utility scripts from ERP
- Include Docker for consistent development environment
- NO docs/ directory (use README.md only)
- NO deployment configuration yet (that's Module 9)

**Development Tools**:
- PostgreSQL local or Neon for development
- WhiteNoise for static files
- django-environ for environment variables
- pytest for testing

**Packages (requirements/base.txt)**:
```
# Core Framework
Django==6.0.7
django-environ==0.14.0
django-htmx==1.28.0

# Database
psycopg2-binary==2.9.12

# Static Files & Media
whitenoise==6.12.0
django-storages==1.14.6
pillow==12.3.0

# Content Management
django-taggit==6.1.0
django-mdeditor==0.1.20

# Production Server
gunicorn==26.0.0

# Testing
pytest==9.1.1
pytest-django==4.12.0
```

**Packages (requirements/dev.txt)**:
```
-r base.txt

# Development Tools
django-debug-toolbar==6.3.0
django-extensions==4.1.0
```

**Packages (requirements/prod.txt)**:
```
-r base.txt

# Production only (add as needed)
```

**Constitution Files Detail**:

**Architecture_Law.md**:
- Project structure rules
- App organization pattern (apps/ directory)
- Database design principles
- How to add new apps
- File naming conventions

**Frontend_Law.md**:
- HTMX usage rules
- CSS organization (variables, components)
- Animation guidelines
- Mobile-first approach
- Template structure rules

**Content_Law.md**:
- How content is managed (admin only)
- Markdown rules for blog
- Image handling rules
- SEO metadata requirements

**Deployment_Law.md**:
- Render deployment rules (future)
- Neon database connection
- CloudFlare R2 usage
- Environment variable management

**Design_Law.md**:
- Color palette
- Typography rules
- Spacing system
- Component design patterns

**Testing_Law.md**:
- What to test
- Testing approach
- Test file organization
- Coverage requirements

**Agent Usage** (using your existing aliases):
```bash
# Create project with all agents
AMWBootstrapAgentFullBootstrap webdev portfolio

# Or scaffold only
AMWStructureAgentScaffold webdev portfolio

# Validate structure
AMWStructureAgentValidate .

# Fix missing elements
AMWStructureAgentAddMissing .
```

---

### Module 2: Landing Page

**Goal**: Create the main landing page with summary of all sections

**Components**:
- Hero section (name, title, professional headline)
- Quick About preview
- Top skills preview (categorized, not limited)
- Featured projects (2-3 best projects)
- Blog preview (latest 2-3 posts)
- Contact CTA

**Guidelines**:
- Clean, modern design with animations
- Smooth scrolling between sections
- Mobile responsive
- Fast loading (optimize images)
- HTMX for dynamic content loading

---

### Module 3: About Section

**Goal**: Professional journey and personal summary

**Components**:
- Professional summary
- Personal summary
- Work experience timeline (admin → freelance → automation)
- Education (if applicable)
- CV/Resume download (PDF from CloudFlare R2)

**Guidelines**:
- Storytelling approach
- Visual timeline if possible
- Easy to update via admin
- Downloadable CV

---

### Module 4: Skills Section

**Goal**: Categorized skills with accordion UI

**Components**:
- Skill categories (determined during building)
- Accordion-style expand/collapse
- Skill icons/logos
- Proficiency indicators (optional)
- Easy to add/modify via admin

**Guidelines**:
- Categories will be determined during building
- Extract skills from projects
- Visual representation (icons)
- Mobile-friendly accordion
- NOT limited to 7-8 categories

---

### Module 5: Projects Section

**Goal**: Showcase projects with filtering and details

**Components**:
- Project list with thumbnails
- Filtering by skills/tags
- Project detail pages
- Expandable case study sections
- Links to GitHub/Notion

**Fields per Project**:
- Title
- Thumbnail image (AI-generated)
- Description
- Skills/tags used
- GitHub URL
- Notion URL (optional)
- Live demo URL (optional)
- Problem statement
- Solution approach
- Results/metrics

**Guidelines**:
- AI-generated thumbnails
- Easy to add via admin
- SEO-friendly URLs
- Mobile responsive cards

---

### Module 6: Blog Section

**Goal**: Technical blog with Markdown and tagging

**Components**:
- Blog post list
- Individual post pages (Markdown rendering)
- Tagging system (django-taggit)
- Filter by tags
- Related posts
- SEO metadata

**Fields per Post**:
- Title
- Content (Markdown via django-mdeditor)
- Tags (multiple)
- Published date
- Featured image (optional)
- Excerpt/summary

**Guidelines**:
- Markdown editor in admin
- Code syntax highlighting
- Mobile responsive reading
- Easy to publish from admin

---

### Module 7: Contact Section

**Goal**: Contact form and professional social links

**Components**:
- Contact form (name, email, subject, message)
- Social links (GitHub, LinkedIn, Notion)
- Email display
- Mobile display
- Form validation
- Email notification (optional)

**Guidelines**:
- Simple, clean form
- Spam protection
- Mobile-friendly
- Response confirmation

---

### Module 8: Admin Dashboard & Analytics

**Goal**: Django admin with analytics dashboard

**Components**:
- Customized Django admin
- Analytics dashboard (page views, visitor info)
- Content management (add projects, blog posts, skills)
- Media upload to CloudFlare R2

**Analytics Features**:
- Total page views
- Most viewed projects
- Visitor locations
- Device types
- Referral sources

**Guidelines**:
- User-friendly admin interface
- Easy content updates
- Real-time analytics
- Secure access

---

### Module 9: Production Phase (Deployment & Launch)

**Goal**: Deploy to production and go live

**Components**:
- Render deployment
- Neon database setup (production)
- CloudFlare R2 configuration
- Domain setup (if available)
- SSL certificate
- Environment variables (production)
- Post-deployment testing

**Guidelines**:
- Follow deployment checklist
- Test all functionality
- Monitor for errors
- SEO setup