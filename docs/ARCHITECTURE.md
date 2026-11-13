# Architecture — Student Performance Analysis

## System overview

A single Flask application serves HTML pages and CSV/JSON responses. A CSV file is the data source. Pandas performs cleaning and calculations, Jinja templates render pages, and Matplotlib generates chart images.

~~~mermaid
flowchart TD
    U[Browser] --> F[Flask application]
    F --> R[Dashboard, students, report, validate, CSV, health routes]
    R --> A[analysis.py]
    A --> C[CSV dataset]
    A --> P[Pandas cleaning and summaries]
    R --> T[Jinja templates]
    R --> M[Matplotlib charts]
    M --> S[static/charts]
    T --> U
    S --> U
~~~

## Components

| Component | Responsibility |
|---|---|
| app.py | Flask app, routes, chart generation, templates and CSV export |
| analysis.py | Required columns, cleaning, derived fields, summaries, validation and report text |
| data/student_performance.csv | Fictional source data |
| templates/ | Jinja pages for dashboard, records, report, validation and errors |
| static/ | CSS and generated chart images |
| tests/ | Unit and Flask test-client checks |
| wsgi.py | Exposes the Flask app object to Gunicorn |
| Dockerfile | Container image and startup command |
| .github/workflows/ | Automated tests, image builds and health smoke tests |

## Request and data flow

1. Browser requests a Flask route.
2. The route loads the CSV using the project data-loading function.
3. analysis.load_dataset() checks required columns and converts values to appropriate types.
4. Missing numeric values are median-imputed; values outside 0–100 are clipped for analysis. Source data-quality issues are retained in DataFrame metadata for the validation page.
5. The module derives averages, totals, grades and pass/support status.
6. The route prepares summaries and passes them to a Jinja template, or returns a CSV/JSON response.

## Design decisions

- CSV, not a database: keeps the first version focused on programming and data analysis, but does not provide persistent multi-user storage.
- Separate analysis module: reusable logic can be tested independently of HTTP routes.
- Flask test client: exercises routes without starting an external server.
- Gunicorn: serves the WSGI app in the hosted container instead of Flask's development server.
- Dynamic port: the process reads the platform-provided PORT, falling back to 5000 for local use.
- One Gunicorn worker: keeps resource use small for this demo; it is not a scaling strategy.

## Runtime and persistence

Dashboard chart images are generated under static/charts. The packaged CSV remains the data source. A hosted container's writable filesystem may be replaced during restarts or deployments, so generated files and runtime changes must not be treated as durable storage.

## Security and scope

This public demo has no authentication or authorisation and must only use fictional data. Real use would require access control, privacy review, secure persistent storage, upload validation, auditability, backups, monitoring and security testing.
