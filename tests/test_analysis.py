from pathlib import Path
from analysis import assign_grade, load_dataset, summarize_dataset, subject_summary, validate_dataset

DATA=Path(__file__).resolve().parents[1]/"data"/"student_performance.csv"

def test_grade_boundaries():
    assert assign_grade(80)=="A"
    assert assign_grade(65)=="B"
    assert assign_grade(50)=="C"
    assert assign_grade(35)=="D"
    assert assign_grade(34.99)=="F"

def test_dataset_and_derived_columns():
    df=load_dataset(DATA)
    assert len(df)>=20
    assert {"average_marks","total_marks","grade","result"}.issubset(df.columns)
    assert df.average_marks.between(0,100).all()

def test_summary_consistency():
    df=load_dataset(DATA); m=summarize_dataset(df)
    assert m["total_students"]==len(df)
    assert 0<=m["pass_percentage"]<=100
    assert len(subject_summary(df))==4

def test_demo_data_validation():
    assert validate_dataset(load_dataset(DATA))==["No data quality issues found in the processed dataset."]
