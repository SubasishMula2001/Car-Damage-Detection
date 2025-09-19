import requests

def test_predict_endpoint():
    url = "http://localhost:8000/predict"
    files = {"file": open("sample.jpg", "rb")}
    response = requests.post(url, files=files)
    assert response.status_code == 200
