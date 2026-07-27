# AMW Portfolio Showcase

Professional portfolio website showcasing skills, projects, and technical expertise.

## Tech Stack

- **Backend**: Django 6.0.7
- **Frontend**: HTMX 1.28.0 + Bootstrap 5.3.0
- **Database**: PostgreSQL (Neon)
- **Storage**: CloudFlare R2 (media, static files)
- **Hosting**: Render

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/dev.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver 8000
```

## Project Structure

```
AMWPortfolio/
├── apps/           # Django applications
│   ├── core/       # Homepage, shared utilities
│   ├── humans/     # Authentication
│   ├── skills/     # Skills management
│   ├── projects/   # Project showcase
│   ├── blog/       # Blog with Markdown/tags
│   └── analytics/  # Analytics dashboard
├── config/         # Project configuration
├── static/         # Static assets
├── templates/      # Global templates
└── requirements/   # Dependency files
```

## Deployment

See `render.yaml` for Render deployment configuration.
