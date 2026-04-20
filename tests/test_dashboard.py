from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_page_serves_html() -> None:
    client = TestClient(app)
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Quan sát hệ thống AI Career Assistant HUST" in response.text


def test_metrics_snapshot_shape() -> None:
    client = TestClient(app)
    response = client.get("/metrics")

    payload = response.json()
    assert response.status_code == 200
    assert "latency_p95" in payload
    assert "traffic" in payload
    assert "error_breakdown" in payload
    assert "quality_avg" in payload


def test_chat_ui_serves_html() -> None:
    client = TestClient(app)
    response = client.get("/chat-ui")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Trò chuyện với trợ lý nghề nghiệp" in response.text
