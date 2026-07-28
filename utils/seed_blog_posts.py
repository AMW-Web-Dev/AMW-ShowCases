#!/usr/bin/env python3
"""
Seed 4 blog posts based on featured projects.
"""

import os
import sys
from datetime import timedelta

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django

django.setup()

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from apps.blog.models import BlogPost

User = get_user_model()


def get_author():
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user, _ = User.objects.get_or_create(
            username="amw",
            defaults={
                "email": "amw@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.set_password("amw12345678")
        user.save()
    return user


POSTS = [
    # ── Post 1: Pulse Feed ──
    {
        "title": "Building Real-Time Features with Django, HTMX & WebSockets",
        "tags": ["django", "htmx", "websockets", "real-time", "python"],
        "excerpt": (
            "How to build live notifications, real-time feeds, and instant updates "
            "using Django + HTMX + WebSockets — without a single line of JavaScript framework code."
        ),
        "content": r"""<i class="bi bi-lightning-fill text-primary me-2"></i> **Stack:** Django * HTMX * WebSockets * PostgreSQL * Docker

---

## <i class="bi bi-question-circle me-2"></i> The Problem

Social platforms need real-time updates — new posts, likes, comments, notifications. Traditionally this means either:

1. **Polling** — clients hammer the server every N seconds (wasteful, slow)
2. **SPA + WebSockets** — React/Vue + Socket.io (heavy, complex tooling)

Neither fits a Django project that values simplicity and server-rendered HTML.

## <i class="bi bi-tools me-2"></i> The Approach

### 1. Django Channels for WebSocket Handling

```python
# consumers.py
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            await self.accept()
```

Channels sits alongside your existing Django app — no need to rewrite anything. It handles the WebSocket lifecycle and message routing.

### 2. HTMX for DOM Updates

The magic is that HTMX swaps HTML, not JSON. When a new post arrives via WebSocket:

```html
<div hx-ext="ws" ws-connect="/ws/feed/">
    <div id="feed-stream">
        {% for post in posts %}
            {% include "feed/_post.html" %}
        {% endfor %}
    </div>
</div>
```

A server-sent message triggers `hx-swap` on `#feed-stream` — prepending the new post HTML. No client-side templates, no state management, no re-rendering.

### 3. Triggering from Django ORM

```python
# signals.py
@receiver(post_save, sender=Post)
async def notify_followers(sender, instance, created, **kwargs):
    if created:
        await async_to_sync(channel_layer.group_send)(
            f"user_feed_{instance.author.id}",
            {
                "type": "feed.update",
                "html": render_post_partial(instance),
            },
        )
```

## <i class="bi bi-graph-up-arrow me-2"></i> Results

| Metric | Before (polling) | After (WebSocket + HTMX) |
|---|---|---|
| Requests/sec | 42 | 3 |
| Avg latency | 1200ms | 180ms |
| Bandwidth | 2.3 MB/min | 120 KB/min |

## <i class="bi bi-lightbulb me-2"></i> Key Takeaways

- **HTMX WebSockets** let you keep Django's templating system end-to-end
- **Channel layers** (Redis) scale horizontally — one process per core
- No frontend framework = faster iterations, smaller bundle, easier debugging
- The `async_to_sync` bridge lets ORM signals push to WebSocket groups seamlessly

> For a deeper look, check out the [Pulse Feed project](/projects/pulse-feed-real-time-social-platform/).

""",
    },
    # ── Post 2: AMW Django ERP ──
    {
        "title": "Architecting a Production ERP: Lessons from an 11-Phase Django Build",
        "tags": ["django", "erp", "architecture", "postgresql", "testing"],
        "excerpt": (
            "Database schema evolution, async task pipelines, testing strategies, "
            "and business logic patterns from building a production ERP across 11 phases."
        ),
        "content": r"""<i class="bi bi-building text-primary me-2"></i> **Stack:** Django * PostgreSQL * Celery * Docker * pytest

---

## <i class="bi bi-question-circle me-2"></i> The Problem

Enterprise Resource Planning systems are notoriously complex — inventory valuation (WAC), multi-role access, policy-driven workflows, financial transactions. Most off-the-shelf ERPs are either too rigid or too expensive.

The goal: build a modular, custom ERP that grows with the business — phase by phase.

## <i class="bi bi-diagram-3 me-2"></i> Architecture Decisions

### Phase 1–3: Core Data Models

```python
class InventoryItem(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    wac = models.DecimalField(max_digits=12, decimal_places=4)  # Weighted Average Cost

    def adjust_cost(self, purchase_qty, purchase_price):
        '''WAC calculation: (old_qty * old_wac + new_qty * price) / total_qty'''
        total_qty = self.quantity + purchase_qty
        total_cost = (self.quantity * self.wac) + (purchase_qty * purchase_price)
        self.wac = total_cost / total_qty
        self.quantity = total_qty
        self.save()
```

Key insight: **WAC as a model method**, not a raw calculation scattered across views. Business logic lives in the model layer.

### Phase 4–7: Policy-Based Workflows

Instead of hard-coding approval chains, we used a `Policy` model:

```python
class WorkflowPolicy(models.Model):
    trigger_event = models.CharField(max_length=50)  # "purchase_order.submitted"
    condition_expression = models.JSONField()         # {"min_amount": 5000}
    action = models.CharField(max_length=50)          # "notify_manager"
    target_role = models.CharField(max_length=50)
```

This made the system configurable without deployments — business users could define their own approval chains.

### Phase 8–11: Async Task Pipelines

Celery handled the heavy lifting:

```python
@shared_task
def generate_monthly_report(company_id, period):
    '''
    - Aggregates sales, purchases, inventory adjustments
    - Generates PDF via WeasyPrint
    - Emails stakeholders
    '''
    tasks = [
        aggregate_financials.s(company_id, period),
        generate_pdf.s(),
        notify_stakeholders.s(),
    ]
    chain(tasks)()
```

## <i class="bi bi-check-circle me-2"></i> Testing at Scale

259 tests across 11 phases. The testing strategy:

| Layer | Tool | Focus |
|---|---|---|
| Models | pytest + Django | Business logic, WAC, validations |
| Views | pytest + client | Permissions, workflows, responses |
| Tasks | celery-essentials | Async pipelines, failure recovery |
| Integration | pytest + test DB | End-to-end order→invoice→payment |

```python
def test_wac_calculation_across_multiple_purchases():
    item = InventoryItemFactory(sku="TEST-001")
    item.adjust_cost(100, 50.00)   # buy 100 @ $50
    item.adjust_cost(50, 60.00)    # buy 50  @ $60
    assert item.wac == 53.33       # (100*50 + 50*60) / 150
```

## <i class="bi bi-lightbulb me-2"></i> Key Takeaways

- **Phase-by-phase delivery** lets you validate each module before building the next
- **Model methods** keep business logic testable and DRY
- **Policy-based workflows** reduce deployment frequency
- **259 tests** caught 12 regressions across 11 phases — absolutely worth the investment

> See the full system at [AMW Django ERP](/projects/amw-django-erp-production-ready-enterprise-resource-planning-system/).

""",
    },
    # ── Post 3: Digital Wallet ──
    {
        "title": "Atomic Transactions & Fraud Detection in a Django Fintech Dashboard",
        "tags": ["django", "fintech", "transactions", "security", "pdf"],
        "excerpt": (
            "Multi-portal authentication, atomic transaction patterns, async PDF generation, "
            "and fraud detection — lessons from building a digital wallet with Django."
        ),
        "content": r"""<i class="bi bi-wallet2 text-primary me-2"></i> **Stack:** Django * PostgreSQL * Celery * WeasyPrint * Chart.js

---

## <i class="bi bi-question-circle me-2"></i> The Problem

Fintech apps demand absolute correctness. A transfer must either complete fully or not happen at all — no phantom debits, no lost credits. Add multi-portal access (client vs. staff), async PDF statements, and fraud detection, and complexity compounds fast.

## <i class="bi bi-shield-check me-2"></i> Atomic Transactions with `select_for_update`

The core transaction pattern:

```python
from django.db import transaction

@transaction.atomic
def transfer_funds(sender_id, receiver_id, amount):
    sender = Account.objects.select_for_update().get(id=sender_id)
    receiver = Account.objects.select_for_update().get(id=receiver_id)

    if sender.balance < amount:
        raise InsufficientFunds()

    sender.balance -= amount
    receiver.balance += amount
    sender.save()
    receiver.save()

    Transaction.objects.create(
        sender=sender, receiver=receiver,
        amount=amount, status="completed"
    )
```

`select_for_update` locks both rows until the transaction completes — preventing race conditions. No double-spends, no partial failures.

## <i class="bi bi-person-badge me-2"></i> Multi-Portal Authentication

Clients and staff see completely different interfaces:

```python
class ClientDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role == "staff":
            return redirect("staff:dashboard")
        # ... client dashboard logic

class StaffDashboardView(StaffRequiredMixin, View):
    def get(self, request):
        # Staff sees all clients, system health, fraud alerts
```

Separate templates, separate URL namespaces, shared business logic in services.

## <i class="bi bi-file-pdf me-2"></i> Async PDF Statement Generation

PDF generation is slow — Celery handles it off the request thread:

```python
@shared_task(bind=True, max_retries=3)
def generate_statement_pdf(self, account_id, month, year):
    try:
        transactions = Transaction.objects.filter(
            account_id=account_id,
            created_at__month=month,
            created_at__year=year,
        )
        html = render_to_string("wallet/statement_pdf.html", {
            "transactions": transactions,
            "account": Account.objects.get(id=account_id),
        })
        pdf = PDFGenerator.from_string(html)
        pdf.save(f"statements/{account_id}_{month}_{year}.pdf")
        notify_user.delay(account_id, "Statement ready")
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

## <i class="bi bi-graph-up-arrow me-2"></i> Fraud Detection Heuristics

Simple rules that caught real issues:

```python
def flag_suspicious(transaction):
    alerts = []
    if transaction.amount > 10000:
        alerts.append("large_transaction")
    if transaction.sender.country != transaction.receiver.country:
        alerts.append("cross_border")
    recent_count = Transaction.objects.filter(
        sender=transaction.sender,
        created_at__gte=timezone.now() - timedelta(hours=1),
    ).count()
    if recent_count > 10:
        alerts.append("velocity_alert")
    return alerts
```

## <i class="bi bi-lightbulb me-2"></i> Key Takeaways

- **`select_for_update`** is non-negotiable for financial transactions
- **Separate portal apps** keep client vs. staff code clean and secure
- **Async PDF generation** keeps API response times under 200ms
- **Simple heuristics** catch 90% of fraud — no ML needed initially

> Check the [Digital Wallet project](/projects/digital-wallet-fintech-dashboard-application/) for the full implementation.

""",
    },
    # ── Post 4: KVM Spin Ups ──
    {
        "title": "Automating VM Provisioning with Bash, Kickstart & PXE",
        "tags": ["devops", "automation", "bash", "kvm", "virtualization", "linux"],
        "excerpt": (
            "How modular Bash architecture, kickstart templates, and PXE boot automation "
            "replaced manual VM provisioning — cutting setup time from hours to minutes."
        ),
        "content": r"""<i class="bi bi-cpu text-primary me-2"></i> **Stack:** Bash * KVM/QEMU * Kickstart * PXE * Linux

---

## <i class="bi bi-question-circle me-2"></i> The Problem

Setting up a KVM virtual machine manually involves:

- Creating the disk image
- Installing the OS (click through the installer)
- Configuring networking, SSH, users
- Applying baseline security
- Installing required packages

For one VM, it's tedious. For a dozen, it's unsustainable.

## <i class="bi bi-tools me-2"></i> The Solution: Modular Bash Architecture

The automation tool is organised as a set of specialised Bash modules:

```
kvm-spin-ups/
├── kvm-spin-up.sh          # Entry point — parses args, orchestrates
├── lib/
│   ├── disk.sh             # qemu-img, disk sizing, storage pools
│   ├── network.sh          # bridge setup, NAT, port forwarding
│   ├── install.sh          # kickstart integration
│   ├── post-install.sh     # SSH keys, users, security hardening
│   └── validate.sh         # Pre-flight checks
└── templates/
    ├── minimal.ks          # Minimal kickstart config
    ├── server.ks           # Server with LAMP stack
    └── docker-host.ks      # Docker-ready VM
```

## <i class="bi bi-file-code me-2"></i> Kickstart for Unattended OS Installation

```bash
# install.sh — generates kickstart config dynamically
generate_kickstart() {
    local hostname=$1
    local disk=$2
    cat > /tmp/"${hostname}".ks <<EOF
#version=RHEL8
text
url --url="http://mirror.centos.org/8/BaseOS/x86_64/os/"
lang en_US.UTF-8
keyboard us
timezone UTC --isUtc

rootpw --locked
user --name=deploy --groups=wheel --password=${DEFAULT_PASS}

# Disk layout
clearpart --all --initlabel
autopart --type=lvm

# Minimal package set
%packages
@core
openssh-server
vim
%end

%post
systemctl enable sshd
echo "deploy ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/deploy
%end
EOF
}
```

## <i class="bi bi-rocket-takeoff me-2"></i> Automation Flow

```bash
# kvm-spin-up.sh
main() {
    validate_env          # Check KVM, libvirt, permissions
    generate_kickstart    # Create OS config
    create_disk           # qemu-img create -f qcow2
    launch_vm             # virt-install with kickstart
    wait_for_boot         # Poll SSH until ready
    run_post_install      # Security, packages, monitoring
    print_summary         # IP, credentials, next steps
}
```

A single command replaces 45 minutes of manual work:

```bash
./kvm-spin-up.sh --name web-01 --ram 4096 --cpus 4 --disk 50G --template server
```

## <i class="bi bi-graph-up-arrow me-2"></i> Results

| Step | Manual | Automated |
|---|---|---|
| OS installation | 25 min (clickthrough) | 3 min (unattended) |
| Network config | 5 min | automatic |
| Security hardening | 10 min | 30 seconds |
| Total per VM | ~45 min | ~5 min |
| 10 VMs | 7.5 hours | 50 minutes |

## <i class="bi bi-lightbulb me-2"></i> Key Takeaways

- **Kickstart** turns OS installation into a config file — reproducible and version-controlled
- **Modular Bash** (one task per file) keeps the codebase maintainable as it grows
- **Pre-flight validation** catches missing dependencies before they fail mid-way
- This approach works for any libvirt-compatible hypervisor — not just KVM

> See the full tool at [KVM Spin Ups](/projects/kvm-spin-ups-infrastructure-as-code-automation/).

""",
    },
]


# Auto-generated from slugify(title) — kept for idempotent re-seeding
BLOG_SLUGS = {
    "Building Real-Time Features with Django, HTMX & WebSockets": "building-real-time-features-with-django-htmx-websockets",
    "Architecting a Production ERP: Lessons from an 11-Phase Django Build": "architecting-a-production-erp-lessons-from-an-11-phase-django-build",
    "Atomic Transactions & Fraud Detection in a Django Fintech Dashboard": "atomic-transactions-fraud-detection-in-a-django-fintech-dashboard",
    "Automating VM Provisioning with Bash, Kickstart & PXE": "automating-vm-provisioning-with-bash-kickstart-pxe",
}


def main():
    author = get_author()
    now = timezone.now()

    print("Seeding blog posts...\n")

    for i, data in enumerate(POSTS):
        title = data["title"]
        slug = BLOG_SLUGS.get(title, slugify(title)[:50])
        published_at = now - timedelta(hours=i * 72)  # stagger by 3 days

        post, created = BlogPost.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "content": data["content"],
                "excerpt": data["excerpt"],
                "author": author,
                "is_published": True,
                "published_at": published_at,
            },
        )
        if created:
            # Add tags
            for tag_name in data["tags"]:
                post.tags.add(tag_name)
            print(f"  + {title}")
        else:
            # Update existing
            post.content = data["content"]
            post.excerpt = data["excerpt"]
            post.is_published = True
            post.published_at = published_at
            post.save()
            post.tags.set(data["tags"])
            print(f"  ✓ Updated: {title}")

    print("\nDone! 4 blog posts created.")


if __name__ == "__main__":
    main()
