# Student Performance Analysis

A Python data-analysis and web-dashboard project that explores student marks, attendance, grade distribution, and subject-wise performance using a fictional CSV dataset. Built as a beginner-to-intermediate BSc Computer Science portfolio project.

## Features

- Load and clean CSV data with Pandas
- Handle missing or invalid numeric values using median filling and range checks
- Calculate total marks, average marks, grade, and pass/support status
- Dashboard with KPI cards and Matplotlib charts
- Search by student name or ID and filter by class/section
- Student records table with subject-wise marks
- Export processed records to CSV
- Generated text analysis report
- Data-quality checks for missing fields, duplicate IDs, and invalid ranges
- Responsive HTML/CSS interface
- Reusable analysis functions and automated tests

## Screenshots

After running the application, capture screenshots of the dashboard, student records, report, and data-quality page, then add them here.

## Tech Stack

Python 3.10+, Flask, Pandas, Matplotlib, HTML, CSS, pytest.

## Run on Windows

1. Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/). Enable **Add Python to PATH** during installation.
2. Extract the project folder.
3. Double-click `run_windows.bat` and wait for dependency installation.
4. Double-click `start_windows.bat`.
5. Open [http://127.0.0.1:5000](http://127.0.0.1:5000).
6. Stop the local server with `Ctrl+C` in the terminal.

### Manual setup

```bash
py -m venv .venv
.venv\\Scripts\\activate
py -m pip install -r requirements.txt
py app.py
```

## Run Tests

With dependencies installed:

```bash
py -m pytest -q
```

## Dataset and Grading Rules

The included CSV contains fictional sample records. Grade rules are configurable examples: A >= 80, B >= 65, C >= 50, D >= 35, and F below 35. A student is marked Pass only if each subject score is at least 33. These are not any institution's official grading rules.

## Limitations

This is a local educational project, not a production student-information system. It has no login, authorization, database persistence, or deployment hardening. Use fictional data only. Simple indicators should not be treated as definitive judgments about students.

## Future Improvements

- Upload a CSV with schema validation
- Add SQLite persistence and authentication
- Add configurable grading rules and PDF report export
- Add Docker and GitHub Actions CI
- Deploy with environment-based configuration

## License

MIT. See [LICENSE](LICENSE).
