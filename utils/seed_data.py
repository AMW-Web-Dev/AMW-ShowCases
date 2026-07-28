#!/usr/bin/env python3
"""
Seed script — populates the database with curated sample data.

Usage:
    cd /path/to/project && python utils/seed_data.py

Uses the development settings by default. Override via DJANGO_SETTINGS_MODULE.
"""

import os
import sys
from datetime import timedelta

# Ensure project root is on sys.path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django

django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
from apps.skills.models import SkillCategory, Skill
from apps.projects.models import Project
from apps.blog.models import BlogPost

User = get_user_model()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _get_or_create_user():
    user, created = User.objects.get_or_create(
        username="amw",
        defaults={
            "email": "amw@example.com",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if created:
        user.set_password("amw12345678")
        user.save()
        print("  ✔ Created superuser amw / amw12345678")
    else:
        print("  ✓ Superuser already exists")
    return user


def _now():
    return timezone.now()


# =========================================================================
# SKILL CATEGORIES & SKILLS
# =========================================================================

SEED_SKILLS = [
    {
        "category": (
            "Languages",
            "programming-languages",
            "Programming & Scripting Languages",
            "code-slash",
        ),
        "skills": [
            (
                "Python",
                "python",
                95,
                8,
                "Expert-level Python with extensive experience in web development, automation, data processing, and API design.",
                "devicon-python-plain",
            ),
            (
                "TypeScript",
                "typescript",
                80,
                5,
                "Strong TypeScript skills for frontend and backend (Node.js) development.",
                "devicon-typescript-plain",
            ),
            (
                "JavaScript",
                "javascript",
                85,
                8,
                "Deep understanding of modern JavaScript (ES6+) including async patterns and DOM APIs.",
                "devicon-javascript-plain",
            ),
            (
                "Shell Scripting",
                "shell",
                90,
                8,
                "Advanced Bash/Zsh scripting for automation, CI/CD pipelines, and system administration.",
                "devicon-bash-plain",
            ),
            (
                "SQL",
                "sql",
                85,
                7,
                "Proficient in complex queries, query optimization, and database design across PostgreSQL and MySQL.",
                "bi bi-database",
            ),
            (
                "Go",
                "golang",
                60,
                3,
                "Working knowledge of Go for building CLI tools and performant microservices.",
                "devicon-go-plain",
            ),
        ],
    },
    {
        "category": (
            "Frameworks & Libraries",
            "frameworks",
            "Web Frameworks & Application Libraries",
            "layers",
        ),
        "skills": [
            (
                "Django",
                "django",
                95,
                7,
                "Expert-level Django: ORM, class-based views, REST framework, middleware, custom management commands.",
                "devicon-django-plain",
            ),
            (
                "FastAPI",
                "fastapi",
                75,
                3,
                "Building async APIs with FastAPI, Pydantic validation, and OpenAPI documentation.",
                "devicon-fastapi-plain",
            ),
            (
                "React",
                "react",
                70,
                4,
                "Building interactive UIs with React hooks, context API, and state management.",
                "devicon-react-plain",
            ),
            (
                "HTMX",
                "htmx",
                85,
                2,
                "Building dynamic UIs with HTMX — hypermedia-driven approach replacing heavy frontend frameworks.",
                "",
            ),
            (
                "Bootstrap",
                "bootstrap",
                90,
                7,
                "Extensive experience with Bootstrap 4/5 theming, custom components, and responsive design.",
                "devicon-bootstrap-plain",
            ),
            (
                "Tailwind CSS",
                "tailwind-css",
                75,
                3,
                "Utility-first CSS with Tailwind for rapid, consistent UI development.",
                "devicon-tailwindcss-plain",
            ),
        ],
    },
    {
        "category": (
            "DevOps & Cloud",
            "devops-cloud",
            "Infrastructure, Cloud & DevOps Tooling",
            "cloud",
        ),
        "skills": [
            (
                "Docker",
                "docker",
                90,
                6,
                "Containerization expert: multi-stage builds, Docker Compose, swarm, optimization.",
                "devicon-docker-plain",
            ),
            (
                "Kubernetes",
                "kubernetes",
                80,
                4,
                "Managing production clusters: deployments, Helm charts, service mesh, RBAC.",
                "devicon-kubernetes-plain",
            ),
            (
                "AWS",
                "aws",
                85,
                6,
                "AWS services: EC2, S3, RDS, Lambda, CloudFront, IAM, VPC design.",
                "devicon-amazonwebservices-plain-wordmark",
            ),
            (
                "CI/CD",
                "cicd",
                90,
                6,
                "Designing and maintaining CI/CD pipelines with GitHub Actions, GitLab CI, and Jenkins.",
                "bi bi-infinity",
            ),
            (
                "Terraform",
                "terraform",
                75,
                4,
                "Infrastructure-as-Code with Terraform for cloud resource provisioning.",
                "devicon-terraform-plain",
            ),
            (
                "Linux",
                "linux",
                95,
                10,
                "Expert Linux administration: systemd, networking, security hardening, performance tuning.",
                "devicon-linux-plain",
            ),
            (
                "Nginx",
                "nginx",
                85,
                6,
                "Reverse proxy, load balancing, SSL termination, caching strategies.",
                "devicon-nginx-plain",
            ),
            (
                "PostgreSQL",
                "postgresql",
                85,
                7,
                "Database administration: replication, partitioning, vacuum strategies, query planning.",
                "devicon-postgresql-plain",
            ),
        ],
    },
    {
        "category": (
            "Tools & Platforms",
            "tools",
            "Development Tools & Productivity Platforms",
            "gear",
        ),
        "skills": [
            (
                "Git",
                "git",
                90,
                8,
                "Advanced Git workflows: rebase strategies, bisect, hooks, submodules.",
                "devicon-git-plain",
            ),
            (
                "GitHub Actions",
                "github-actions",
                85,
                4,
                "Designing complex CI/CD workflows, matrix builds, custom actions.",
                "devicon-githubactions-plain",
            ),
            (
                "VS Code",
                "vscode",
                90,
                6,
                "Deeply customized VS Code environment with extensions, tasks, and debug configs.",
                "devicon-vscode-plain",
            ),
            (
                "Neovim",
                "neovim",
                80,
                5,
                "Terminal-based development with custom Neovim Lua configuration.",
                "devicon-neovim-plain",
            ),
            (
                "Prometheus & Grafana",
                "prometheus-grafana",
                75,
                4,
                "Monitoring stack: metric collection, alerting, dashboard creation.",
                "devicon-prometheus-plain",
            ),
        ],
    },
]


def seed_skills(user):
    print("\n── Skills ──")
    created_cats = 0
    created_skills = 0

    for group in SEED_SKILLS:
        cat_name, cat_slug, cat_desc, cat_icon = group["category"]
        cat, is_new = SkillCategory.objects.get_or_create(
            slug=cat_slug,
            defaults={
                "name": cat_name,
                "description": cat_desc,
                "icon": cat_icon,
            },
        )
        if is_new:
            created_cats += 1

        for order, skill_data in enumerate(group["skills"]):
            s_name, s_slug, s_prof, s_years, s_desc = skill_data[:5]
            s_icon = skill_data[5] if len(skill_data) > 5 else ""
            skill, is_new = Skill.objects.get_or_create(
                slug=s_slug,
                defaults={
                    "name": s_name,
                    "category": cat,
                    "proficiency": s_prof,
                    "years_experience": s_years,
                    "description": s_desc,
                    "icon": s_icon,
                    "featured": s_prof >= 80,
                    "order": order,
                },
            )
            if not is_new and skill.icon != s_icon:
                skill.icon = s_icon
                skill.save(update_fields=["icon"])
            if is_new:
                created_skills += 1

    print(f"  ✔ {created_cats} categories, {created_skills} skills created")


# =========================================================================
# PROJECTS
# =========================================================================

SEED_PROJECTS = [
    {
        "title": "Cloud Infrastructure Automation Platform",
        "slug": "cloud-infra-platform",
        "description": (
            "An automated infrastructure provisioning and management platform that "
            "reduced deployment time by 80% across 15 microservices."
        ),
        "long_description": """## Overview
A comprehensive infrastructure automation platform built with Terraform, AWS, and Python.

## Key Features
- **Infrastructure as Code**: Complete AWS environment defined in Terraform modules
- **Auto-scaling**: Dynamic resource allocation based on traffic patterns
- **Zero-downtime Deployments**: Blue-green deployment strategy with automated rollback
- **Monitoring**: Integrated Prometheus/Grafana stack with intelligent alerting

## Architecture
The platform uses a modular Terraform structure with remote state management,
GitHub Actions for CI/CD, and Python automation scripts for bootstrapping
and maintenance tasks.

## Impact
- 80% reduction in infrastructure provisioning time
- 99.95% uptime across all services
- Automated compliance checks for SOC2 and GDPR requirements
""",
        "technologies": ["python", "terraform", "aws", "docker", "kubernetes"],
        "github_url": "https://github.com/amw/cloud-infra",
        "live_url": "",
        "featured": True,
    },
    {
        "title": "Real-Time Analytics Dashboard",
        "slug": "analytics-dashboard",
        "description": (
            "A real-time analytics dashboard processing 10M+ events daily with "
            "sub-second query performance."
        ),
        "long_description": """## Overview
Real-time analytics platform built with Django, PostgreSQL, and Redis.

## Key Features
- **Live Dashboards**: WebSocket-powered real-time updates
- **Custom Metrics**: User-defined metric creation and aggregation
- **Data Export**: CSV, JSON, and API access to all analytics data
- **Role-based Access**: Multi-tenant architecture with granular permissions

## Tech Stack
- Backend: Django + Django REST Framework
- Database: PostgreSQL with TimescaleDB extension
- Cache/Queue: Redis for real-time processing
- Frontend: HTMX + Chart.js for interactive visualizations

## Impact
- Processed 10M+ events daily with <100ms latency
- Reduced reporting time from hours to seconds
- Served 200+ dashboard users across 5 teams
""",
        "technologies": ["python", "django", "postgresql", "typescript", "htmx"],
        "github_url": "https://github.com/amw/analytics-dashboard",
        "live_url": "",
        "featured": True,
    },
    {
        "title": "Developer Productivity CLI Suite",
        "slug": "dev-cli-suite",
        "description": (
            "A collection of CLI tools automating daily development workflows — "
            "from project scaffolding to deployment."
        ),
        "long_description": """## Overview
A Python-based CLI toolkit that automates common development tasks.

## Features
- **Project Scaffolding**: Interactive project generation with templates
- **Git Workflow Automation**: Branch management, commit conventions, PR creation
- **Environment Management**: Automated setup and dependency management
- **Deployment Tools**: One-command deploy to staging/production

## Technologies
Built with Click (Python CLI framework), rich for terminal UI,
and integrates with GitHub API, Docker, and cloud providers.
""",
        "technologies": ["python", "shell", "docker", "github-actions"],
        "github_url": "https://github.com/amw/dev-cli",
        "live_url": "",
        "featured": True,
    },
    {
        "title": "E-Commerce Microservices Platform",
        "slug": "ecommerce-microservices",
        "description": (
            "A scalable e-commerce platform built on a microservices architecture "
            "with event-driven communication."
        ),
        "long_description": """## Overview
Modern e-commerce platform decomposed into independently deployable services.

## Services
- **Product Service**: Catalog management with full-text search
- **Order Service**: Order processing with saga pattern
- **Payment Service**: Multi-provider payment integration
- **Notification Service**: Email, SMS, and push notifications

## Infrastructure
- Kubernetes orchestration with Helm
- gRPC for inter-service communication
- Kafka for event streaming
- Istio service mesh for observability
""",
        "technologies": [
            "python",
            "golang",
            "docker",
            "kubernetes",
            "postgresql",
            "cicd",
        ],
        "github_url": "https://github.com/amw/ecommerce-platform",
        "live_url": "",
        "featured": False,
    },
    {
        "title": "Open Source Contribution Bot",
        "slug": "oss-contribution-bot",
        "description": (
            "An automated bot that helps maintainers triage issues, review PRs, "
            "and onboard new contributors."
        ),
        "long_description": """## Overview
A GitHub App built with Python that automates open source maintenance tasks.

## Capabilities
- **Issue Triage**: Auto-labeling based on content analysis
- **PR Review**: Automated code style checks and test running
- **Onboarding**: Welcome messages and contribution guide pointers
- **Stale Management**: Automated stale issue/PR management

## Deployment
Deployed as a serverless GitHub App using AWS Lambda and API Gateway.
""",
        "technologies": ["python", "typescript", "github-actions", "aws", "cicd"],
        "github_url": "https://github.com/amw/oss-bot",
        "live_url": "",
        "featured": False,
    },
]


def seed_projects(user):
    print("\n── Projects ──")
    created = 0
    for data in SEED_PROJECTS:
        proj, is_new = Project.objects.get_or_create(
            slug=data["slug"],
            defaults={
                "title": data["title"],
                "description": data["description"],
                "long_description": data["long_description"],
                "github_url": data["github_url"],
                "live_url": data["live_url"],
                "featured": data["featured"],
            },
        )
        if is_new:
            for tech_slug in data["technologies"]:
                try:
                    skill = Skill.objects.get(slug=tech_slug)
                    proj.technologies.add(skill)
                except Skill.DoesNotExist:
                    print(f"  ⚠  Skill '{tech_slug}' not found — skipping")
            created += 1
    print(f"  ✔ {created} projects created")


# =========================================================================
# BLOG POSTS
# =========================================================================

SEED_POSTS = [
    {
        "title": "Building a Production-Ready Django Project Structure",
        "slug": "django-project-structure",
        "excerpt": (
            "How I structure Django projects for maintainability, scalability, "
            "and team productivity — with lessons learned from 5 years of Django development."
        ),
        "content": """## Why Project Structure Matters

After working on dozens of Django projects — from small MVPs to large-scale applications — I've learned that **project structure is one of the most impactful decisions** you make early on.

## My Preferred Structure

```
project_root/
├── apps/              # All Django apps
│   ├── core/          # Homepage, shared utilities
│   ├── accounts/      # Authentication
│   └── api/           # REST endpoints
├── config/            # Django settings (split by environment)
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   └── urls.py
├── templates/         # Project-level templates
├── static/            # Project-level static files
└── requirements/      # Split requirements
    ├── base.txt
    ├── dev.txt
    └── prod.txt
```

## Key Principles

1. **Flat is better than nested** — keep apps at the top level
2. **Split settings early** — base/prod/dev prevents production mishaps
3. **One app, one concern** — if an app does two things, split it
4. **Templates follow app structure** — `templates/app_name/template.html`

## What I'd Do Differently

Looking back, I'd add type annotations from day one and invest more in comprehensive testing early. The refactoring cost of adding types later is significant.

## TL;DR

Invest in project structure early. It pays compounding dividends as your project grows.
""",
        "tags": ["django", "python", "architecture", "best-practices"],
        "is_published": True,
        "published_days_ago": 3,
    },
    {
        "title": "Docker Multi-Stage Builds for Python Applications",
        "slug": "docker-multi-stage-python",
        "excerpt": (
            "Optimize your Docker images for Python applications using multi-stage builds — "
            "from 1.2GB to under 200MB."
        ),
        "content": """## The Problem

Standard Docker images for Python applications are **bloated**. They include build tools, compilers, and development dependencies that have no place in production.

## The Solution: Multi-Stage Builds

Multi-stage builds let you use **multiple FROM statements** in a single Dockerfile. Each stage starts fresh, and you selectively copy artifacts between stages.

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

COPY requirements/prod.txt /requirements.txt
RUN pip install --user --no-warn-script-location \\
    -r /requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app

CMD ["gunicorn", "config.wsgi:application"]
```

## Results

| Metric | Before | After |
|--------|--------|-------|
| Image size | 1.2 GB | 187 MB |
| Build time | 4m 30s | 1m 15s |
| Vulnerabilities | 24 (5 high) | 3 (0 high) |

## Additional Optimizations

- Use `--no-cache-dir` for pip
- Pin base image digests, not tags
- Use `.dockerignore` aggressively
- Combine RUN commands to reduce layers

The 80% reduction in image size means faster deployments, lower storage costs, and a smaller attack surface.
""",
        "tags": ["docker", "python", "devops", "containerization"],
        "is_published": True,
        "published_days_ago": 7,
    },
    {
        "title": "Understanding Python Async: From Basics to Production",
        "slug": "python-async-guide",
        "excerpt": (
            "A practical guide to async/await in Python — covering event loops, "
            "coroutines, and common pitfalls with real-world examples."
        ),
        "content": """## Why Async?

Python's `asyncio` library enables **concurrent code** using the `async`/`await` syntax. It's ideal for I/O-bound tasks like web requests, database queries, and file operations.

## The Basics

```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    result = await fetch_data("https://api.example.com/data")
    print(result)

asyncio.run(main())
```

## Common Pitfalls

### 1. Blocking the Event Loop

Never call blocking functions (like `time.sleep()` or `requests.get()`) inside async code:

```python
# WRONG — blocks the entire event loop
async def bad():
    time.sleep(1)  # ❌

# CORRECT — yields control
async def good():
    await asyncio.sleep(1)  # ✅
```

### 2. Forgeting to Await

```python
async def buggy():
    asyncio.sleep(1)  # ❌ Creates coroutine but never runs it
    await asyncio.sleep(1)  # ✅
```

## Production Patterns

- Use `asyncio.gather()` for parallel tasks
- Set timeouts with `asyncio.wait_for()`
- Use `asyncio.Queue` for producer-consumer patterns
- Always handle cancellation gracefully

Async Python is powerful but requires a mental model shift. Once it clicks, you'll wonder how you lived without it.
""",
        "tags": ["python", "async", "tutorial", "best-practices"],
        "is_published": True,
        "published_days_ago": 14,
    },
    {
        "title": "CI/CD Pipeline Design: A Practical Framework",
        "slug": "cicd-pipeline-design",
        "excerpt": (
            "Designing CI/CD pipelines that are fast, reliable, and actually useful — "
            "a framework based on real-world experience."
        ),
        "content": """## The Goal

A good CI/CD pipeline is **fast**, **reliable**, and **provides useful feedback**. Here's my framework for designing one.

## The Three Phases

### 1. Validation (< 2 minutes)
- Linting and formatting checks
- Type checking
- Unit tests
- Security scanning

### 2. Integration (< 10 minutes)
- Integration tests with real dependencies
- Build and containerize
- Deploy to ephemeral environment

### 3. Delivery (< 5 minutes)
- Deploy to staging
- Run smoke tests
- Manual approval gate (optional)
- Deploy to production

## Key Metrics

| Metric | Target | Why |
|--------|--------|-----|
| Pipeline duration | < 15 min | Fast feedback |
| Failure rate | < 5% | Reliable |
| Time to recover | < 30 min | Quick fixes |

## Tool-Specific Config

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v4
      - run: pytest --cov --cov-report=xml
```

The best pipeline is the one your team actually uses. Start simple, iterate, and automate everything that hurts.
""",
        "tags": ["devops", "cicd", "github-actions", "automation"],
        "is_published": True,
        "published_days_ago": 21,
    },
    {
        "title": "HTMX + Django: A Match Made in Heaven",
        "slug": "htmx-django-guide",
        "excerpt": (
            "Why HTMX pairs perfectly with Django for building dynamic web applications "
            "without writing a line of JavaScript."
        ),
        "content": """## The Old Way

For years, Django developers reached for a JavaScript frontend framework (React, Vue, Angular) whenever they needed interactivity. This meant **two codebases**, **two build pipelines**, and **twice the complexity**.

## Enter HTMX

HTMX lets you build dynamic UIs directly from HTML, using **hypermedia as the engine of application state** (HATEOAS).

## Real Examples

### Form Submission with Validation

```html
<form hx-post="{% url 'contact:submit' %}"
      hx-target="#form-response"
      hx-swap="outerHTML">
  {% csrf_token %}
  <input type="email" name="email" required>
  <button type="submit">Send</button>
</form>
<div id="form-response"></div>
```

### Infinite Scroll

```html
<div hx-get="{% url 'blog:page' 2 %}"
     hx-trigger="revealed"
     hx-target="this"
     hx-swap="afterend">
</div>
```

## Why It Works

1. **Server-side rendering** — no client-side state management
2. **Progressive enhancement** — works without JavaScript
3. **Minimal payloads** — just HTML fragments, no JSON parsing
4. **Django forms work** — same form handling as traditional views

## When Not to Use HTMX

HTMX isn't suitable for highly interactive UIs like real-time editors, complex drag-and-drop, or games. But for 90% of web applications, it's the sweet spot.

Django + HTMX is the most productive stack I've used.
""",
        "tags": ["django", "htmx", "python", "web-development"],
        "is_published": True,
        "published_days_ago": 30,
    },
    {
        "title": "Linux Performance Tuning: A Systematic Approach",
        "slug": "linux-performance-tuning",
        "excerpt": (
            "A systematic methodology for diagnosing and resolving Linux performance "
            "issues — from CPU to disk I/O."
        ),
        "content": """## The USE Method

The **USE Method** (Utilization, Saturation, Errors) is a systematic approach to performance analysis:

1. For every resource, check **Utilization**, **Saturation**, and **Errors**
2. Start with the highest-level resources and drill down

## CPU Analysis

```bash
# Check CPU utilization and saturation
top -bn1 | head -20
mpstat -P ALL 1 5
vmstat 1 5

# Per-process CPU usage
pidstat -p $(pgrep -u www-data) 1 5
```

## Memory Analysis

```bash
# Overall memory
free -h

# Detailed breakdown
cat /proc/meminfo

# Which processes use memory
ps aux --sort=-%mem | head -10
```

## Disk I/O Analysis

```bash
# I/O statistics
iostat -xz 1 5

# Per-process I/O
iotop -oP

# Find large files
du -sh /* 2>/dev/null | sort -rh | head -10
```

## Network Analysis

```bash
# Connection overview
ss -tuln
ss -s

# Network throughput
nload
iftop
```

## The 1-Second Rule

If a command takes less than 1 second to give you actionable insight, run it every time:
- `uptime` — load averages
- `dmesg | tail` — kernel errors
- `vmstat 1` — system summary
- `mpstat -P ALL 1` — per-CPU breakdown

Performance tuning is a skill that compounds. The more you do it, the faster you identify bottlenecks.
""",
        "tags": ["linux", "devops", "performance", "sysadmin"],
        "is_published": True,
        "published_days_ago": 45,
    },
]


def seed_blog(user):
    print("\n── Blog Posts ──")
    created = 0
    for data in SEED_POSTS:
        published_at = _now() - timedelta(days=data["published_days_ago"])
        post, is_new = BlogPost.objects.get_or_create(
            slug=data["slug"],
            defaults={
                "title": data["title"],
                "content": data["content"],
                "excerpt": data["excerpt"],
                "author": user,
                "is_published": data["is_published"],
                "published_at": published_at,
            },
        )
        if is_new:
            for tag_name in data["tags"]:
                post.tags.add(tag_name)
            created += 1
    print(f"  ✔ {created} blog posts created")


# =========================================================================
# MAIN
# =========================================================================


def main():
    print("=" * 48)
    print("  Portfolio Seed Script")
    print("=" * 48)

    print("\n── Users ──")
    user = _get_or_create_user()

    seed_skills(user)
    seed_projects(user)
    seed_blog(user)

    print("\n" + "=" * 48)
    print("  Seed complete! 🚀")
    print("=" * 48)


if __name__ == "__main__":
    main()
