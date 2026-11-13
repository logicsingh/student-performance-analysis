from app import app


def test_dashboard_search_treats_query_as_literal_text():
    client = app.test_client()
    response = client.get("/?q=%5B")
    assert response.status_code == 200


def test_student_search_treats_query_as_literal_text():
    client = app.test_client()
    response = client.get("/students?q=%5B")
    assert response.status_code == 200


def test_flask_debug_is_disabled_by_default():
    assert app.debug is False
