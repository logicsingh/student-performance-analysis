
from pathlib import Path
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request, send_file

from analysis import (
    load_dataset,
    summarize_dataset,
    subject_summary,
    grade_distribution,
    validate_dataset,
    generate_report,
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "student_performance.csv"
CHARTS = ROOT / "static" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)


def data():
    return load_dataset(DATA)


def charts(df):
    # Average marks by subject
    subjects = subject_summary(df)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(subjects.subject, subjects.average_marks)
    ax.set_title("Average Marks by Subject")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Average / 100")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHARTS / "subject_averages.png", dpi=120)
    plt.close(fig)

    # Grade distribution
    grades = grade_distribution(df)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(grades.grade, grades.students)
    ax.set_title("Grade Distribution")
    ax.set_ylabel("Student records")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHARTS / "grade_distribution.png", dpi=120)
    plt.close(fig)

    # Attendance versus average marks
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(
        df.attendance_percentage,
        df.average_marks,
        alpha=0.75,
    )
    ax.set_title("Attendance vs Average Marks")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Average marks")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHARTS / "attendance_vs_marks.png", dpi=120)
    plt.close(fig)


@app.route("/")
def dashboard():
    df = data()
    charts(df)
    metrics = summarize_dataset(df)

    query = request.args.get("q", "").strip()
    selected_class = request.args.get("class", "").strip()

    view = df.copy()

    if query:
        view = view[
            view.student_name.str.contains(
                query, case=False, na=False
            )
            | view.student_id.str.contains(
                query, case=False, na=False
            )
        ]

    if selected_class:
        view = view[view.class_section == selected_class]

    return render_template(
        "index.html",
        metrics=metrics,
        records=view.sort_values("student_name").to_dict("records"),
        subjects=subject_summary(df).to_dict("records"),
        classes=sorted(df.class_section.unique()),
        q=query,
        selected_class=selected_class,
        total_filtered=len(view),
    )


@app.route("/students")
def students():
    df = data()

    query = request.args.get("q", "").strip()
    selected_class = request.args.get("class", "").strip()

    if query:
        df = df[
            df.student_name.str.contains(
                query, case=False, na=False
            )
            | df.student_id.str.contains(
                query, case=False, na=False
            )
        ]

    if selected_class:
        df = df[df.class_section == selected_class]

    return render_template(
        "students.html",
        records=df.sort_values("student_name").to_dict("records"),
        q=query,
        selected_class=selected_class,
        classes=sorted(data().class_section.unique()),
    )


@app.route("/download/csv")
def download():
    output = io.BytesIO(
        data().to_csv(index=False).encode("utf-8")
    )
    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="student_performance_export.csv",
    )


@app.route("/report")
def report():
    return render_template(
        "report.html",
        report_text=generate_report(data()),
    )


@app.route("/validate")
def validate():
    df = data()
    errors = validate_dataset(df)

    clean_message = (
        "No data quality issues found in the processed dataset."
    )

    # Do not count the informational clean-data message as an issue.
    issue_count = (
        0 if errors == [clean_message] else len(errors)
    )

    return render_template(
        "validate.html",
        errors=errors,
        issue_count=issue_count,
        row_count=len(df),
        columns=list(df.columns),
    )


@app.errorhandler(404)
def not_found(_):
    return (
        render_template(
            "error.html",
            code=404,
            message="The requested page was not found.",
        ),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
