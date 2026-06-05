# Qualizenz Flask Deployment Guide

Qualizenz is a Flask webapp for pharmaceutical GMP articles, templates, downloads, newsletter capture, consulting inquiries and owner-only admin control.

Do not deploy the backend on GitHub Pages. GitHub Pages can only host static files. Use Render for Flask and Supabase for storage/database services.

## Files required for Render

- `requirements.txt` installs Flask, Gunicorn, document/PDF libraries and Supabase support.
- `Procfile` starts the app with `gunicorn app:app`.
- `runtime.txt` pins Python to `python-3.11.9`.
- `render.yaml` defines Render build/start commands and production environment placeholders.
- `app.py` serves `/`, `/admin/login`, `/admin/dashboard` and API routes.

## Render setup

1. Push this repository to GitHub.
2. Open Render and create a new **Web Service**.
3. Connect the GitHub repository.
4. Use these settings:
   - Runtime: Python
   - Build command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Add the environment variables below.
6. Deploy.

## Required environment variables

Set these in Render under **Environment**:

```text
FLASK_ENV=production
QUALIZENZ_SECRET_KEY=use-a-long-random-secret
QUALIZENZ_ADMIN_PASSWORD=use-a-strong-admin-password
QUALIZENZ_ADMIN_USERNAME=admin
```

Generate a strong secret locally with:

```powershell
py -c "import secrets; print(secrets.token_urlsafe(48))"
```

## Supabase setup

1. Create a Supabase project.
2. Create a Storage bucket named:

```text
qualizenz-uploads
```

3. Keep the bucket private.
4. Copy your Supabase project URL and service role key.
5. Add these Render environment variables:

```text
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_STORAGE_BUCKET=qualizenz-uploads
SUPABASE_ARTICLE_PREFIX=articles
```

`SUPABASE_SERVICE_ROLE_KEY` must stay secret. Do not expose it in frontend JavaScript.

## Admin URLs

After deployment:

```text
https://your-render-app.onrender.com/admin/login
https://your-render-app.onrender.com/admin/dashboard
```

Use the password from `QUALIZENZ_ADMIN_PASSWORD`.

## Public URLs

```text
https://your-render-app.onrender.com/
https://your-render-app.onrender.com/api/status
```

The `/api/status` endpoint shows whether Supabase Storage is configured.

## Upload and download behavior

When Supabase env vars are configured, article uploads are stored in Supabase Storage. When they are not configured, uploads fall back to local `uploads/articles` for development.

Article PDF/DOCX downloads are served as Qualizenz-branded PDFs with header, footer, watermark, date and time stamp.

Supported upload types:

```text
PDF, DOCX, XLSX, PNG, JPG, JPEG
```

Only PDF and DOCX files can be converted into branded article-download PDFs.

## Production notes

- Render provides the `PORT` variable automatically.
- Flask debug mode is disabled when `FLASK_ENV=production` or Render sets `RENDER=true`.
- Session cookies are HTTP-only and secure in production.
- Admin write APIs require an authenticated admin session.
- Local JSON files are acceptable for development, but a full production database should move content tables to Supabase Postgres.

## Suggested Supabase tables

- `admin_users` or environment-based admin auth
- `articles`
- `sop_templates`
- `validation_templates`
- `free_resources`
- `homepage_content`
- `site_settings`
- `contact_messages`
- `consulting_requests`
- `newsletter_subscribers`
- `downloads`

Each content table should include:

```text
id, title, category, description, content, file_path, image_path, price,
is_free, is_visible, status, created_at, updated_at
```
