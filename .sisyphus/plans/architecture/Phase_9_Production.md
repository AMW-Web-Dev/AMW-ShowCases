# Phase 9: Production

## Objective
Configure production settings and deploy to Render.

## Duration
2-3 hours

## Dependencies
- Phase 8: Frontend Polish

## Tasks

### Task 9.1: Production Settings (Already in Phase 1)
Production settings already defined in Phase 1. This phase deploys.

### Task 9.2: Render Configuration (Already in Phase 1)
render.yaml already created in Phase 1.

### Task 9.3: Requirements Production (Already in Phase 1)
requirements/prod.txt already created in Phase 1.

### Task 9.4: Environment Variables (Already in Phase 1)
.env.example already created in Phase 1.

### Task 9.5: Deployment Steps
```bash
# 1. Ensure all changes committed
git add .
git commit -m "Production ready"
git push origin main

# 2. Create Render account
# Visit https://render.com

# 3. Create new web service
# Connect GitHub repository

# 4. Configure environment variables in Render dashboard:
# - DJANGO_SETTINGS_MODULE=config.settings.production
# - SECRET_KEY (auto-generated)
# - DATABASE_URL (from Neon)
# - R2_ACCESS_KEY_ID
# - R2_SECRET_ACCESS_KEY
# - R2_BUCKET_NAME
# - R2_ENDPOINT_URL
# - ALLOWED_HOSTS=your-app.onrender.com

# 5. Deploy
# Render will auto-deploy on push to main

# 6. Post-deploy (via Render shell):
python manage.py migrate --noinput
python manage.py createsuperuser --noinput
```

### Task 9.6: Post-Deployment Verification
```bash
# Test production site
curl -I https://your-app.onrender.com

# Check health endpoint
curl https://your-app.onrender.com/health/

# Verify admin access
# Visit https://your-app.onrender.com/admin/

# Test all pages:
# - Homepage
# - Skills
# - Projects
# - Blog
# - Dashboard (staff only)
# - About
# - Contact
```

### Task 9.7: Custom Domain (Optional)
```yaml
# In render.yaml, add:
services:
  - type: web
    name: amw-portfolio
    domains:
      - amw.com
      - www.amw.com
```

## Verification
- [ ] Production settings configured
- [ ] Render service created
- [ ] Environment variables set
- [ ] Site accessible via HTTPS
- [ ] Admin interface working
- [ ] Static files loading
- [ ] Media files uploading

## Commands
```bash
# Deploy to production
git push origin main

# Monitor deployment
# Visit Render dashboard
```

## Completion
- [ ] All phases complete
- [ ] Portfolio website live
- [ ] Admin interface functional
- [ ] Blog system working
- [ ] Skills and projects displayed
- [ ] Analytics tracking visitors

## Next Steps
1. Add content via admin interface
2. Customize styling further
3. Add more features as needed
4. Monitor analytics
5. Share portfolio with others