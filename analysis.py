
from pathlib import Path
import pandas as pd

SUBJECTS = {"Mathematics":"maths_marks","Science":"science_marks","English":"english_marks","Computer Science":"computer_marks"}
REQUIRED = ["student_id","student_name","class_section","attendance_percentage",*SUBJECTS.values()]

def assign_grade(avg):
    if pd.isna(avg): return "F"
    if avg >= 80: return "A"
    if avg >= 65: return "B"
    if avg >= 50: return "C"
    if avg >= 35: return "D"
    return "F"

def load_dataset(path):
    df=pd.read_csv(path)
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError("Dataset is missing required columns: "+", ".join(missing))
    df=df.copy()
    for c in ["student_id","student_name","class_section"]:
        df[c]=df[c].astype("string").str.strip()
    numeric=["attendance_percentage",*SUBJECTS.values()]
    for c in numeric: df[c]=pd.to_numeric(df[c],errors="coerce")
    df[numeric]=df[numeric].fillna(df[numeric].median())
    df["attendance_percentage"]=df["attendance_percentage"].clip(0,100)
    for c in SUBJECTS.values(): df[c]=df[c].clip(0,100)
    df["average_marks"]=df[list(SUBJECTS.values())].mean(axis=1).round(2)
    df["total_marks"]=df[list(SUBJECTS.values())].sum(axis=1).round(2)
    df["grade"]=df["average_marks"].apply(assign_grade)
    df["result"]=df.apply(lambda r:"Pass" if all(r[c]>=33 for c in SUBJECTS.values()) else "Needs Improvement",axis=1)
    return df

def summarize_dataset(df):
    if df.empty: return {"total_students":0,"average_marks":0,"pass_percentage":0,"average_attendance":0,"needs_improvement":0}
    return {"total_students":int(len(df)),"average_marks":round(float(df.average_marks.mean()),2),
            "pass_percentage":round(float((df.result=="Pass").mean()*100),2),
            "average_attendance":round(float(df.attendance_percentage.mean()),2),
            "needs_improvement":int((df.result=="Needs Improvement").sum())}

def subject_summary(df):
    return pd.DataFrame([{"subject":name,"average_marks":round(float(df[col].mean()),2)} for name,col in SUBJECTS.items()])

def grade_distribution(df):
    counts=df.grade.value_counts().to_dict()
    return pd.DataFrame([{"grade":g,"students":int(counts.get(g,0))} for g in ["A","B","C","D","F"]])

def validate_dataset(df):
    errors=[]
    if df.empty: errors.append("Dataset has no student records.")
    if df.student_id.isna().any() or (df.student_id.astype(str).str.strip()=="").any(): errors.append("Some records have a missing student ID.")
    if df.student_id.duplicated().any(): errors.append("Duplicate student IDs were found.")
    if df.student_name.isna().any() or (df.student_name.astype(str).str.strip()=="").any(): errors.append("Some records have a missing student name.")
    for c in ["attendance_percentage",*SUBJECTS.values()]:
        if df[c].isna().any(): errors.append(f"Column {c} contains missing numeric values.")
        if ((df[c]<0)|(df[c]>100)).any(): errors.append(f"Column {c} contains values outside 0–100.")
    return errors or ["No data quality issues found in the processed dataset."]

def generate_report(df):
    m=summarize_dataset(df); subs=subject_summary(df).sort_values("average_marks",ascending=False)
    top=df.sort_values("average_marks",ascending=False).head(5); low=df.sort_values("average_marks").head(5)
    lines=["STUDENT PERFORMANCE ANALYSIS REPORT","="*38,"",f"Total students: {m['total_students']}",
      f"Overall average marks: {m['average_marks']}/100",f"Pass percentage: {m['pass_percentage']}%",
      f"Average attendance: {m['average_attendance']}%",f"Students needing improvement: {m['needs_improvement']}","",
      "SUBJECT AVERAGES","-"*16]
    lines += [f"{r.subject}: {r.average_marks}/100" for r in subs.itertuples()]
    lines += ["","TOP 5 STUDENTS","-"*14]+[f"{r.student_name} ({r.student_id}) — {r.average_marks}/100, Grade {r.grade}" for r in top.itertuples()]
    lines += ["","5 STUDENTS TO SUPPORT","-"*21]+[f"{r.student_name} ({r.student_id}) — {r.average_marks}/100, Grade {r.grade}" for r in low.itertuples()]
    lines += ["","Interpretation","-"*14,"Use summaries to identify patterns and plan support. Marks and attendance alone do not explain every student's performance."]
    return "\n".join(lines)
