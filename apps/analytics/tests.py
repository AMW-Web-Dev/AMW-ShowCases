"""Regression tests for the analytics middleware path-exclusion logic.

The unit tests call the exclusion check directly via RequestFactory because
CommonMiddleware's APPEND_SLASH redirect would otherwise swallow bare-path
requests before the middleware runs, producing false-green results.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory, override_settings

from .middleware import AnalyticsMiddleware
from .models import PageView


@pytest.fixture
def middleware():
    return AnalyticsMiddleware(lambda request: None)


@pytest.fixture
def rf():
    return RequestFactory()


def test_bare_nexus_not_tracked(middleware, rf):
    request = rf.get("/nexus")
    assert middleware.should_track(request) is False


def test_nexus_slash_not_tracked(middleware, rf):
    request = rf.get("/nexus/")
    assert middleware.should_track(request) is False


def test_nexus_analytics_changelist_not_tracked(middleware, rf):
    request = rf.get("/nexus/analytics/pageview/")
    assert middleware.should_track(request) is False


def test_bare_hub_not_tracked(middleware, rf):
    request = rf.get("/hub")
    assert middleware.should_track(request) is False


def test_hub_slash_not_tracked(middleware, rf):
    request = rf.get("/hub/")
    assert middleware.should_track(request) is False


def test_static_not_tracked(middleware, rf):
    request = rf.get("/static/css/app.css")
    assert middleware.should_track(request) is False


def test_public_path_tracked(middleware, rf):
    request = rf.get("/")
    assert middleware.should_track(request) is True


def test_false_positive_guard_nexusfoo_tracked(middleware, rf):
    """A path that merely starts with the excluded prefix must stay tracked."""
    request = rf.get("/nexusfoo")
    assert middleware.should_track(request) is True


def test_staff_exempt(middleware, rf, db):
    user = get_user_model().objects.create_user(
        username="staffer",
        password=None,
        is_staff=True,
    )
    request = rf.get("/")
    request.user = user
    assert middleware.should_track(request) is False


def test_hx_request_exempt(middleware, rf):
    request = rf.get("/", HTTP_HX_REQUEST="true")
    assert middleware.should_track(request) is False


@override_settings(APPEND_SLASH=False)
def test_integration_no_pageview_for_bare_nexus(client, db):
    client.get("/nexus")
    assert PageView.objects.filter(path="/nexus").count() == 0


def test_integration_public_path_still_tracked(client, db):
    client.get("/")
    assert PageView.objects.filter(path="/").count() == 1
