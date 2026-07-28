#!/usr/bin/env python3
"""
Seed your actual skills from MySkillsList.txt into the database.
Skill names are extracted cleanly — no parenthetical descriptions in names.

Usage:
    cd /path/to/project && python Utils/seed_my_skills.py
"""

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django

django.setup()

from django.utils.text import slugify
from apps.skills.models import SkillCategory, Skill


CATEGORY_ICONS = {
    "Development & Programming": "code-slash",
    "Additional Technical Skills": "cpu",
    "Data Processing & Manipulation": "graph-up",
    "DevOps & Automation": "cloud",
    "Infrastructure & System Administration": "layers",
    "Security & System Hardening": "shield",
    "Professional Skills Demonstrated": "stars",
    "Specialized Technical Areas": "gear",
}

SKILLS_DATA = [
    (
        "Development & Programming",
        [
            ("Shell Script Programming", "devicon-bash-plain colored", False),
            ("Python Development", "devicon-python-plain colored", True),
            ("Django Development", "devicon-django-plain colored", True),
            ("JavaScript / Node.js", "devicon-nodejs-plain colored", False),
            ("Git Version Control", "devicon-git-plain colored", True),
            ("LaTeX Document Preparation", "devicon-latex-plain colored", False),
        ],
    ),
    (
        "Additional Technical Skills",
        [
            ("Databases", "devicon-postgresql-plain colored", True),
            ("Real-Time Systems", "bi bi-lightning-fill", False),
            ("Infrastructure", "bi bi-server", False),
            ("Code Quality", "bi bi-check2-square", True),
            ("Enterprise Experience", "bi bi-building", False),
            ("Shopify API Integration", "bi bi-shop", False),
            ("AI CLI Tools", "bi bi-terminal", True),
        ],
    ),
    (
        "Data Processing & Manipulation",
        [
            ("Python Data Manipulation", "bi bi-file-spreadsheet", False),
            ("Data Analysis & Processing", "bi bi-graph-up-arrow", False),
            ("Data Integration", "bi bi-boxes", False),
            ("Data Validation & Quality", "bi bi-check-circle", False),
        ],
    ),
    (
        "DevOps & Automation",
        [
            ("CI/CD Pipeline Setup", "bi bi-arrow-repeat", True),
            ("Infrastructure as Code", "devicon-terraform-plain colored", False),
            ("Containerization", "devicon-docker-plain colored", True),
            ("Automation Scripting", "bi bi-robot", False),
            ("System Monitoring & Maintenance", "bi bi-activity", False),
        ],
    ),
    (
        "Infrastructure & System Administration",
        [
            ("Linux System Administration", "devicon-linux-plain colored", False),
            ("Package Management", "bi bi-box-seam", False),
            ("System Configuration & Customization", "bi bi-gear", False),
            ("Virtualization", "bi bi-cpu", False),
            ("Network Management", "bi bi-diagram-3", False),
        ],
    ),
    (
        "Security & System Hardening",
        [
            ("Firewall Configuration", "bi bi-shield-check", False),
            ("SSL Certificate Management", "bi bi-lock", False),
            ("System Security Hardening", "bi bi-shield-fill-check", False),
            ("Access Control Management", "bi bi-key", False),
        ],
    ),
    (
        "Professional Skills Demonstrated",
        [
            ("Technical Documentation Writing", "bi bi-pencil", False),
            ("Cross-Platform Tool Integration", "bi bi-boxes", False),
            ("Complex System Architecture", "bi bi-diagram-2", False),
            ("Systematic Troubleshooting", "bi bi-search", False),
        ],
    ),
    (
        "Specialized Technical Areas",
        [
            ("Test Automation & Quality Assurance", "bi bi-check2-square", True),
            ("Documentation Generation & Management", "bi bi-file-text", False),
            ("Performance Optimization", "bi bi-speedometer2", False),
            ("Backup & Recovery Systems", "bi bi-cloud-arrow-up", False),
        ],
    ),
]

DESCRIPTIONS = {
    "Shell Script Programming": "Writing automation scripts and CLI tools using Bash.",
    "Python Development": "Building applications, APIs, and tooling with Python.",
    "Django Development": "Building production web applications with the Django framework.",
    "JavaScript / Node.js": "Developing frontend and backend components with JavaScript and Node.js.",
    "Git Version Control": "Managing source code with Git across projects.",
    "LaTeX Document Preparation": "Authoring technical documents with LaTeX.",
    "Python Data Manipulation": "Processing CSV, Excel, and JSON data with Python ETL pipelines.",
    "Data Analysis & Processing": "Analyzing structured data with pandas and numpy.",
    "Data Integration": "Consolidating data from multiple sources and APIs.",
    "Data Validation & Quality": "Ensuring data integrity through cleaning and validation.",
    "Linux System Administration": "Administering Linux servers and services.",
    "Package Management": "Managing Debian-based packages with apt and dpkg.",
    "System Configuration & Customization": "Configuring Linux systems for specific needs.",
    "Virtualization": "Running and managing VMs with KVM, QEMU, and VirtualBox.",
    "Network Management": "Configuring VPNs, interfaces, and firewall rules.",
    "CI/CD Pipeline Setup": "Designing continuous integration and delivery pipelines.",
    "Infrastructure as Code": "Provisioning infrastructure declaratively with Terraform.",
    "Containerization": "Containerising applications with Docker and Docker Compose.",
    "Automation Scripting": "Automating repetitive tasks with custom scripts.",
    "System Monitoring & Maintenance": "Monitoring health, logs, and system performance.",
    "Firewall Configuration": "Managing firewall rules with UFW and fail2ban.",
    "SSL Certificate Management": "Obtaining and managing SSL/TLS certificates.",
    "System Security Hardening": "Hardening systems and reducing attack surface.",
    "Access Control Management": "Managing users, groups, and permissions.",
    "Test Automation & Quality Assurance": "Automating tests to ensure software quality.",
    "Documentation Generation & Management": "Creating and maintaining technical documentation.",
    "Performance Optimization": "Profiling and optimising system and application performance.",
    "Backup & Recovery Systems": "Designing backup strategies and recovery procedures.",
    "Technical Documentation Writing": "Writing clear technical documentation.",
    "Cross-Platform Tool Integration": "Integrating tools across different platforms.",
    "Complex System Architecture": "Designing complex system architectures.",
    "Systematic Troubleshooting": "Diagnosing issues methodically using logs and analysis.",
    "Databases": "Designing and optimising PostgreSQL and SQLite databases.",
    "Real-Time Systems": "Building real-time UIs with WebSockets and HTMX.",
    "Infrastructure": "Managing infrastructure with Docker, GitHub Actions, and Linux.",
    "Code Quality": "Maintaining quality through pytest, pre-commit, and CI.",
    "Enterprise Experience": "Developing production systems for business operations.",
    "Shopify API Integration": "Email-to-database automation, data parsing, and API integration for Shopify.",
}


def main():
    print("Seeding your skills...\n")

    order = 0
    for cat_name, skills in SKILLS_DATA:
        order += 10
        cat_slug = slugify(cat_name)
        icon_key = CATEGORY_ICONS.get(cat_name, "star")

        category, created = SkillCategory.objects.get_or_create(
            slug=cat_slug,
            defaults={
                "name": cat_name,
                "icon": icon_key,
                "order": order,
            },
        )
        if created:
            print(f"  + Category: {cat_name}")
        else:
            print(f"  ✓ Category: {cat_name}")
            if category.icon != icon_key:
                category.icon = icon_key
                category.save()

        skill_order = 0
        for skill_name, icon, featured in skills:
            skill_order += 10
            slug = slugify(skill_name)
            desc = DESCRIPTIONS.get(skill_name, "")

            skill, created = Skill.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": skill_name,
                    "category": category,
                    "icon": icon,
                    "featured": featured,
                    "description": desc,
                    "order": skill_order,
                },
            )
            if not created:
                skill.category = category
                skill.icon = icon
                skill.featured = featured
                skill.description = desc
                skill.order = skill_order
                skill.save()

            print(f"    {'★' if featured else ' '} {skill_name}")

    print("\nDone!")


if __name__ == "__main__":
    main()
