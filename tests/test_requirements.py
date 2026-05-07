from pathlib import Path


def test_web_dashboard_dependencies_present():
    requirements_path = Path(__file__).resolve().parents[1] / "requirements.txt"
    requirements_text = requirements_path.read_text(encoding="utf-8")

    for dependency in [
        "flask",
        "flask-socketio",
        "python-socketio",
        "websockets",
    ]:
        assert dependency in requirements_text
