# Deployment Guide — Render

## Deployed service

- Repository: https://github.com/logicsingh/student-performance-analysis
- Branch: main; automatic deploys enabled
- Runtime: Docker; Dockerfile ./Dockerfile; context .
- Region: Singapore
- Plan: Free, verified 13 November 2026
- Public URL: https://student-performance-analysis-vsvn.onrender.com
- Dashboard: https://dashboard.render.com/web/srv-dbre76d6e07s73bdqpng

Plan availability and terms can change. Check the dashboard before relying on current status.

## Deployment flow

1. A commit is pushed to main.
2. Render detects the commit through the connected GitHub repository.
3. Render builds an image using the repository Dockerfile.
4. Gunicorn starts and binds to 0.0.0.0 on the platform-provided PORT.
5. Render serves the application at the public URL.

GitHub Actions validates code and the container. It does not publish an image to a registry or deploy to Render in this setup. Render independently builds and deploys from GitHub.

## Configuration

This version requires no secrets or database credentials. The app uses PORT with 5000 as the local fallback. Do not commit secrets if future changes introduce them; configure them in the hosting platform.

The Dockerfile contains a Docker-level health check for /healthz. This is distinct from a separately configured Render health-check path; verify the latter in the service dashboard if one is configured.

## Post-deployment verification

- Open the public URL.
- Check dashboard, charts, search and class filter.
- Open student records, report and validation pages.
- Download the CSV export.
- Request /healthz; expected response: {"status":"ok"}.
- Inspect Render deploy and application logs if a page fails.

The project owner manually confirmed the main user-facing features loaded successfully on 13 November 2026.

## Troubleshooting

| Symptom | Inspect |
|---|---|
| Image build fails | Dockerfile, dependency installation and build logs |
| App does not start | Gunicorn command, wsgi:app, application logs |
| Port/routing issue | Bind address 0.0.0.0 and environment variable PORT |
| Dashboard fails | CSV path, required columns, templates and traceback |
| Charts missing | Matplotlib dependency, writable chart directory and logs |
| Health endpoint fails | Request /healthz and inspect startup logs |

## Cost and operational limits

The service was configured on Render Free at the time of writing; no paid add-ons or database were created for this deployment. Free services may sleep and have resource, cold-start or usage limits. This is not an always-on production service.

The container filesystem is not durable storage. There is no database, backup strategy, high availability, authentication, authorisation or production monitoring configured.
