"""Regression tests for the blog read counter.

read_count must increment for anonymous/regular readers on the detail view but
must NOT increment for the authenticated staff owner (who would otherwise
inflate their own numbers).
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings

from .models import BlogPost


@pytest.fixture
def post(db):
    author = get_user_model().objects.create_user(username="writer", password=None)
    return BlogPost.objects.create(
        title="A Test Post",
        slug="a-test-post",
        content="Body text",
        author=author,
        is_published=True,
    )


@override_settings(APPEND_SLASH=False)
def test_anonymous_reader_increments_count(client, post, db):
    client.get(f"/blog/{post.slug}/")
    post.refresh_from_db()
    assert post.read_count == 1


@override_settings(APPEND_SLASH=False)
def test_repeated_anonymous_reads_increment_each_time(client, post, db):
    client.get(f"/blog/{post.slug}/")
    client.get(f"/blog/{post.slug}/")
    post.refresh_from_db()
    assert post.read_count == 2


@override_settings(APPEND_SLASH=False)
def test_staff_owner_does_not_increment(client, post, db):
    staff = get_user_model().objects.create_user(
        username="owner", password=None, is_staff=True
    )
    client.force_login(staff)
    client.get(f"/blog/{post.slug}/")
    post.refresh_from_db()
    assert post.read_count == 0
