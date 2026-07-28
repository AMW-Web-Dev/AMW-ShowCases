#!/usr/bin/env python3
"""
Clear seed data — removes all sample data added by seed_data.py.

Deletes all entries from BlogPost, Project, Skill, and SkillCategory
so you can start fresh with your own data.

Usage:
    cd /path/to/project && python Utils/clear_seed_data.py
"""

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django

django.setup()

from apps.blog.models import BlogPost
from apps.projects.models import Project
from apps.skills.models import Skill, SkillCategory


def _delete_all(model, label):
    count = model.objects.count()
    if count:
        model.objects.all().delete()
        print(f"  ✕ Removed {count} {label}")
    else:
        print(f"  - No {label} to remove")


def main():
    print("Clearing seed data...\n")

    # Delete in FK-safe order (child models first)
    _delete_all(BlogPost, "blog posts")
    _delete_all(Project, "projects")
    _delete_all(Skill, "skills")
    _delete_all(SkillCategory, "skill categories")

    print("\nDone. Database is clean — ready for your own data.")


if __name__ == "__main__":
    main()
