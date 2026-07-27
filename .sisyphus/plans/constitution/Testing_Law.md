# Testing Constitution

## Testing Philosophy
- **Backend testing focus**: Django models, views, forms
- **No frontend tests**: Keep it simple for portfolio
- **Integration tests**: Test real workflows
- **Manual QA**: For frontend and visual testing

## Test Framework Law

### Setup
```python
# requirements/dev.txt
pytest==7.4.3
pytest-django==4.5.2
pytest-cov==4.1.0
factory-boy==3.3.0
faker==20.1.0
```

### Configuration
```python
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.development
python_files = tests.py test_*.py *_tests.py
addopts = --verbose --tb=short
```

### Test Structure
```
apps/
├── blog/
│   ├── models.py
│   ├── blog.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_forms.py
│   │   └── factories.py
│   └── ...
```

## Model Testing Law

### Basic Model Test
```python
# apps/blog/tests/test_models.py
import pytest
from apps.blog.models import BlogPost
from apps.blog.factories import BlogPostFactory

@pytest.mark.django_db
class TestBlogPost:
    def test_create_blog_post(self):
        """Test creating a blog post."""
        post = BlogPostFactory()
        assert post.pk is not None
        assert post.title is not None
    
    def test_blog_post_str(self):
        """Test string representation."""
        post = BlogPostFactory(title="Test Post")
        assert str(post) == "Test Post"
    
    def test_blog_post_slug(self):
        """Test slug generation."""
        post = BlogPostFactory(title="Test Post Title")
        assert post.slug == "test-post-title"
    
    def test_blog_post_ordering(self):
        """Test default ordering."""
        post1 = BlogPostFactory(created_at='2025-01-01')
        post2 = BlogPostFactory(created_at='2025-01-02')
        posts = BlogPost.objects.all()
        assert posts[0] == post2  # Newest first
```

### Relationship Test
```python
@pytest.mark.django_db
class TestBlogPostRelationships:
    def test_blog_post_tags(self):
        """Test many-to-many relationship with tags."""
        post = BlogPostFactory()
        post.tags.add('django', 'python')
        assert post.tags.count() == 2
    
    def test_blog_post_author(self):
        """Test foreign key relationship."""
        post = BlogPostFactory()
        assert post.author is not None
        assert post.author.pk is not None
```

## View Testing Law

### Basic View Test
```python
# apps/blog/tests/test_views.py
import pytest
from django.test import Client
from django.urls import reverse
from apps.blog.factories import BlogPostFactory

@pytest.mark.django_db
class TestBlogViews:
    def setup_method(self):
        self.client = Client()
    
    def test_blog_list_view(self):
        """Test blog list view."""
        response = self.client.get(reverse('blog:list'))
        assert response.status_code == 200
        assert 'blog_list.html' in [t.name for t in response.templates]
    
    def test_blog_detail_view(self):
        """Test blog detail view."""
        post = BlogPostFactory()
        response = self.client.get(reverse('blog:detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200
        assert response.context['post'] == post
    
    def test_blog_detail_view_404(self):
        """Test 404 for non-existent post."""
        response = self.client.get(reverse('blog:detail', kwargs={'slug': 'non-existent'}))
        assert response.status_code == 404
```

### HTMX View Test
```python
@pytest.mark.django_db
class TestBlogHTMXViews:
    def test_blog_list_htmx(self):
        """Test HTMX blog list response."""
        response = self.client.get(
            reverse('blog:list'),
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
        assert 'text/html' in response['Content-Type']
    
    def test_blog_create_htmx(self):
        """Test HTMX blog create response."""
        response = self.client.post(
            reverse('blog:create'),
            data={'title': 'Test', 'content': 'Content'},
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
```

## Form Testing Law

### Basic Form Test
```python
# apps/blog/tests/test_forms.py
import pytest
from apps.blog.forms import BlogPostForm

class TestBlogPostForm:
    def test_valid_form(self):
        """Test valid form data."""
        form = BlogPostForm(data={
            'title': 'Test Post',
            'content': 'Test content',
            'tags': 'django, python'
        })
        assert form.is_valid()
    
    def test_invalid_form(self):
        """Test invalid form data."""
        form = BlogPostForm(data={
            'title': '',  # Required
            'content': 'Content'
        })
        assert not form.is_valid()
        assert 'title' in form.errors
    
    def test_form_clean_title(self):
        """Test title cleaning."""
        form = BlogPostForm(data={
            'title': '  Test Post  ',
            'content': 'Content'
        })
        assert form.is_valid()
        assert form.cleaned_data['title'] == 'Test Post'
```

## Factory Law

### Basic Factory
```python
# apps/blog/factories.py
import factory
from django.utils.text import slugify
from apps.blog.models import BlogPost
from apps.humans.factories import UserFactory

class BlogPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogPost
    
    title = factory.Sequence(lambda n: f'Blog Post {n}')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    content = factory.Faker('paragraphs', nb=5, ext_word_list=None)
    author = factory.SubFactory(UserFactory)
    is_published = True
    
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
```

### Factory with Related Objects
```python
class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
    
    title = factory.Sequence(lambda n: f'Project {n}')
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    description = factory.Faker('paragraph')
    github_url = factory.Faker('url')
    live_url = factory.Faker('url')
    
    @factory.post_generation
    def technologies(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for tech in extracted:
                self.technologies.add(tech)
```

## Integration Testing Law

### Full Workflow Test
```python
@pytest.mark.django_db
class TestBlogWorkflow:
    def test_create_publish_workflow(self):
        """Test full blog post workflow."""
        # Create post
        post = BlogPostFactory(is_published=False)
        assert not post.is_published
        
        # Publish
        post.is_published = True
        post.save()
        
        # Verify published
        published_posts = BlogPost.objects.filter(is_published=True)
        assert post in published_posts
    
    def test_tag_filtering(self):
        """Test filtering by tags."""
        post1 = BlogPostFactory(tags=['django'])
        post2 = BlogPostFactory(tags=['python'])
        post3 = BlogPostFactory(tags=['django', 'python'])
        
        django_posts = BlogPost.objects.filter(tags__name='django')
        assert django_posts.count() == 2
        
        python_posts = BlogPost.objects.filter(tags__name='python')
        assert python_posts.count() == 2
```

## Performance Testing Law

### Query Count Test
```python
@pytest.mark.django_db
class TestPerformance:
    def test_blog_list_queries(self):
        """Test query count for blog list."""
        from django.test.utils import override_settings
        from django.db import connection
        
        # Create test data
        for _ in range(10):
            BlogPostFactory()
        
        # Reset queries
        connection.queries_log.clear()
        
        # Execute view
        response = self.client.get(reverse('blog:list'))
        
        # Check query count (should be < 10)
        assert len(connection.queries) < 10
```

## Coverage Law

### Coverage Configuration
```python
# .coveragerc
[run]
source = apps
omit = 
    */tests/*
    */migrations/*
    */factories.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if __name__ == "__main__":
    raise NotImplementedError
```

### Coverage Requirements
```bash
# Run coverage
pytest --cov=apps --cov-report=html

# Minimum coverage
# - Overall: 80%
# - Models: 90%
# - Views: 80%
# - Forms: 85%
```

## Manual Testing Law

### Frontend Testing Checklist
```markdown
## Visual Testing
- [ ] Homepage renders correctly
- [ ] Navigation works on all pages
- [ ] Blog list displays posts
- [ ] Blog detail shows full post
- [ ] Skills page shows categories
- [ ] Projects page shows gallery
- [ ] Analytics dashboard loads

## Responsive Testing
- [ ] Mobile (320px width)
- [ ] Tablet (768px width)
- [ ] Desktop (1200px width)
- [ ] Large desktop (1400px+ width)

## Interaction Testing
- [ ] HTMX content loads correctly
- [ ] Forms submit properly
- [ ] Buttons respond to clicks
- [ ] Navigation highlights active page

## Browser Testing
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
```

## Test Commands Law

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest apps/blog/tests/test_models.py

# Run specific test class
pytest apps/blog/tests/test_models.py::TestBlogPost

# Run specific test method
pytest apps/blog/tests/test_models.py::TestBlogPost::test_create_blog_post

# Run with coverage
pytest --cov=apps --cov-report=html

# Run with verbose output
pytest -v

# Run with parallel execution
pytest -n auto
```

### Test Fixtures
```python
# conftest.py
import pytest
from django.test import Client
from apps.humans.factories import UserFactory

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def authenticated_client(client, user):
    client.login(username=user.username, password='password')
    return client
```

## Continuous Testing Law

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        pass_filenames: false
```

### CI Integration
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements/dev.txt
      - run: pytest --cov=apps --cov-report=xml
      - uses: codecov/codecov-action@v3
```

## Test Documentation Law

### Test Naming Convention
```python
# Pattern: test_{action}_{condition}_{expected_result}
def test_blog_post_create_with_valid_data_succeeds():
def test_blog_post_create_with_missing_title_fails():
def test_blog_list_view_returns_200_status():
def test_blog_detail_view_returns_404_for_missing_post():
```

### Test Docstrings
```python
def test_blog_post_slug_generation():
    """
    Test that blog post slug is generated from title.
    
    Given: A blog post with title "Test Post Title"
    When: The post is saved
    Then: The slug should be "test-post-title"
    """
    post = BlogPostFactory(title="Test Post Title")
    assert post.slug == "test-post-title"
```

## Test Quality Law

### Test Characteristics
- **Independent**: Tests don't depend on each other
- **Repeatable**: Same result every time
- **Self-validating**: Clear pass/fail
- **Timely**: Written alongside code

### Test Anti-patterns
- ❌ Tests that depend on database state
- ❌ Tests that depend on external services
- ❌ Tests that are too broad (testing multiple things)
- ❌ Tests without clear assertions
- ❌ Tests that are too slow

### Test Best Practices
- ✅ Use factories for test data
- ✅ Test one thing per test
- ✅ Use descriptive test names
- ✅ Clean up test data
- ✅ Mock external services
- ✅ Test edge cases