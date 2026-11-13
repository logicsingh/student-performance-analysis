# Student Performance Analysis

A Flask educational dashboard for analysing a fictional student dataset. It demonstrates Python data processing, descriptive statistics, validation, visualisation, automated testing, Docker, and a basic cloud deployment workflow.

> Educational use only: included records are fictional. Do not upload real or personally identifiable student data.

## Features
- CSV processing and validation with Pandas
- Missing/non-numeric, duplicate and out-of-range data checks
- Median imputation and range clipping for analysis, with source-quality issues reported
- Totals, averages, example grades and pass/support indicators
- Dashboard metrics and Matplotlib charts
- Search by student name or ID; filter by class/section
- Student records, text analysis report and CSV export
- JSON health endpoint at /healthz
- pytest tests, Docker image and GitHub Actions workflows

## Technology
Python 3.12, Flask, Pandas, Matplotlib, pytest, Gunicorn, Docker, GitHub Actions and Render.

## Application routes

| Route | Purpose |
|---|---|
| / | Dashboard, metrics, charts, search and class filter |
| /students | Student records, search and class filter |
| /report | Text analysis report |
| /validate | Data-quality results |
| /download/csv | CSV export |
| /healthz | JSON health response |

## Run locally on Windows

1. Install Python 3.10 or newer.
2. Open PowerShell in the project directory.
3. Create and activate a virtual environment:

~~~powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
~~~

4. Install dependencies and start Flask:

~~~powershell
python -m pip install -r requirements.txt
python app.py
~~~

5. Open http://127.0.0.1:5000. Stop the server with Ctrl+C.

If PowerShell blocks activation, use Command Prompt and .venv\Scripts\activate.bat, or invoke the environment's Python directly.

## Run tests

~~~powershell
python -m pytest -q
~~~

## Run with Docker

~~~bash
docker build -t student-performance-analysis .
docker run --rm -p 5000:5000 student-performance-analysis
~~~

Open http://127.0.0.1:5000. Test the health endpoint with curl http://127.0.0.1:5000/healthz.

## Architecture and deployment
- [Architecture overview](docs/ARCHITECTURE.md)
- [Deployment guide and Render configuration](docs/DEPLOYMENT.md)
- [Docker and GitHub Actions explanation](docs/DOCKER-CI-CD.md)

## Example grading rules

The fictional sample uses A (80+), B (65–below 80), C (50–below 65), D (35–below 50), and F (below 35). A record is marked Pass only if every subject score is at least 33. These are demonstration rules, not Chandigarh University's or any other institution's official grading policy.

## Limitations and responsible use
- No authentication, authorisation, database, or user-managed CSV upload.
- The CSV is the source of truth; this is not a multi-user student information system.
- Median imputation and clipping are demonstration choices and can affect interpretation.
- Do not use real student data or treat scores as definitive judgments about individuals.
- Runtime chart files are generated in the container filesystem; container filesystems may be ephemeral.
- This is a small educational demo, not a production-hardened, high-availability service.
- Free hosting may sleep or have resource and availability limits; platform terms can change.

## License
MIT. See LICENSE.
