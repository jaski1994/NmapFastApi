from fastapi.testclient import TestClient
from main import app
from app.models.scan import ScanType

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Nmap API"}

def test_create_and_get_scan():
    # 1. Create a scan
    create_response = client.post(
        "/api/v1/scan/",
        json={"target": "127.0.0.1", "scan_type": ScanType.quick.value}
    )
    assert create_response.status_code == 202
    data = create_response.json()
    assert "scan_id" in data
    assert data["target"] == "127.0.0.1"
    assert data["scan_type"] == ScanType.quick.value
    assert data["status"] == "pending"

    scan_id = data["scan_id"]

    # 2. Get the scan status
    get_response = client.get(f"/api/v1/scan/{scan_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["scan_id"] == scan_id
    assert get_data["status"] in ["pending", "running", "completed", "failed"]

def test_list_scans():
    response = client.get("/api/v1/scan/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_nonexistent_scan():
    response = client.get("/api/v1/scan/this-id-does-not-exist")
    assert response.status_code == 404
