# Docker and GitHub Actions — Learning Notes

## 1. Dockerfile explained

| Instruction | Meaning |
|---|---|
| FROM python:3.12-slim | Starts from a smaller official Python 3.12 base image. |
| PYTHONDONTWRITEBYTECODE=1 | Avoids writing Python bytecode files. |
| PYTHONUNBUFFERED=1 | Makes application output appear promptly in logs. |
| FLASK_DEBUG=0 | Keeps Flask debug mode off in the container. |
| WORKDIR /app | Sets the working directory for later instructions. |
| COPY requirements.txt . | Copies dependency declarations separately so Docker can reuse this layer when only app code changes. |
| RUN python -m pip ... | Upgrades pip and installs dependencies without retaining pip's download cache in the image layer. |
| RUN useradd ... appuser | Creates a non-root Linux user with a fixed UID. |
| COPY --chown=appuser:appuser . . | Copies project files and assigns ownership to that user. |
| USER appuser | Runs the application as non-root. |
| EXPOSE 5000 | Documents the conventional container port; it does not publish a host port or override PORT. |
| HEALTHCHECK ... | Docker periodically requests /healthz and records whether the container is healthy. |
| CMD ... | Starts Gunicorn, binds to all interfaces, reads PORT and falls back to 5000. exec replaces the shell so signals reach Gunicorn more directly. |

Build and run:

~~~bash
docker build -t student-performance-analysis .
docker run --rm -p 5000:5000 student-performance-analysis
~~~

-t names the image; -p host:container maps a host port to a container port; --rm removes the stopped container. An image is the packaged template; a container is a running (or stopped) instance of that image.

## 2. GitHub Actions workflows

All workflows run on GitHub-hosted Ubuntu runners for pushes and pull requests targeting main. They declare contents: read so the workflow can check out source without broader repository permissions.

### .github/workflows/python-tests.yml

Checks out the repository, sets up Python 3.12 with pip caching, installs requirements and runs python -m pytest -q. It tests Python logic and Flask routes; it does not build or deploy a container.

### .github/workflows/docker-build.yml

Checks out the code, builds an image tagged with the commit SHA, starts a container on port 5000, polls /healthz for up to 20 attempts, prints logs if the smoke test fails, and removes the container using an if: always() cleanup step. It does not push the image to a registry.

### .github/workflows/ci.yml

Checks out code, sets up Python 3.12, installs dependencies, runs pytest, builds an image, then starts a container with PORT=10000 and tests /healthz. A shell trap prints logs and removes the container when the script exits.

This combined workflow overlaps with the two focused workflows, so some checks are repeated. That is redundant but not inherently wrong for a learning repository. A future tidy-up could retain one combined workflow or the two focused workflows.

## 3. CI versus CD in this repository

- CI: GitHub Actions tests the code, builds the image and smoke-tests the container.
- CD: Render watches the connected main branch and builds/deploys new commits.
- GitHub Actions does not deploy to Render here.
- There is no image registry push, deployment token or GitHub secret in this pipeline.

## 4. What the checks prove — and do not prove

The owner confirmed the main live application features loaded successfully on 13 November 2026. Previously recorded GitHub Actions runs passed the Python tests and Docker build/smoke test. These checks do not prove security, load capacity, production readiness, or correctness for every possible input dataset.

## 5. Check your understanding

Try to explain these without looking at the source:

1. What is the difference between a Docker image and a container?
2. Why copy requirements.txt before copying the application source?
3. Why bind to 0.0.0.0 inside a container rather than only 127.0.0.1?
4. What does EXPOSE do, and what does it not do?
5. Why use Gunicorn on Render instead of Flask's development server?
6. What does the /healthz smoke test actually prove?
7. Which service performs the deployment after a push to main?
8. Why should important uploaded data not be stored in the container filesystem?

You understand the core workflow when you can explain these answers and trace a commit from GitHub Actions checks to Render deployment.
