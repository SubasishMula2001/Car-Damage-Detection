📄 README.md
# 🚗 Car Damage Detection — Live (MLOps Ready)

An AI-powered web application that detects **car damages in real-time** using a deep learning model, **FastAPI backend**, and a **webcam-enabled frontend**.  
This project is **MLOps-ready** with **Docker**, **DVC**, and **Jenkins CI/CD** support.

---

## 📂 Folder Structure


car_damage_detection/
│── backend/ # FastAPI backend + model
│ ├── app.py
│ ├── model_helper.py
│ ├── requirements.txt
│ ├── saved_model.pth # tracked with DVC
│ ├── classes.txt
│ └── server_captures/ # saved damage frames
│
│── frontend/ # Static frontend UI
│ ├── index.html
│ ├── script.js
│ └── styles.css
│
│── tests/ # Unit tests
│── data/ # Dataset (optional, DVC tracked)
│── Dockerfile # Backend Dockerfile
│── docker-compose.yml # Backend + frontend orchestration
│── Jenkinsfile # CI/CD pipeline
│── .gitignore # Ignore unnecessary files
│── README.md # Documentation


---

## ⚙️ Installation (Local)

### 1. Clone repository
```bash
git clone https://github.com/your-username/car-damage-detection-live.git
cd car-damage-detection-live

2. Create virtual environment
python -m venv venv
# Activate
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

3. Install dependencies
pip install -r backend/requirements.txt

4. Run FastAPI server
cd backend
uvicorn app:app --reload --port 8000

5. Open frontend

Go to:

http://127.0.0.1:8000/static/index.html

🐳 Run with Docker
Build image
docker build -t car-damage-detection .

Run container
docker run -p 8000:8000 car-damage-detection


Then open:

http://127.0.0.1:8000/static/index.html

🐙 Run with Docker Compose
docker-compose up --build


Backend → http://localhost:8000

Frontend → http://localhost:8080

📦 MLOps Integration
🔹 DVC (Data & Model Versioning)
dvc init
dvc add backend/saved_model.pth
git add backend/saved_model.pth.dvc .gitignore
git commit -m "Track model with DVC"
dvc remote add -d myremote gdrive://<folder-id>
dvc push

🔹 Jenkins (CI/CD)

The Jenkinsfile automates:

Clone repo

Setup Python environment

Run tests

Build Docker image

Deploy container

🎯 Features

Real-time car damage detection using webcam feed.

History panel with thumbnails, labels, confidence scores.

Auto-saves damaged frames to backend/server_captures/.

Private mode: each user only sees their own predictions.

MLOps-ready: Docker, Jenkins, DVC integrated.

🛠 Tech Stack

Backend: FastAPI (Python)

Frontend: HTML, CSS, JavaScript

Deep Learning: PyTorch

Image Processing: OpenCV, Pillow

MLOps: Docker, Jenkins, DVC

🚀 Future Work

Extend classification to multiple damage types (scratch, dent, broken glass).

Cloud deployment (Azure/AWS).

Mobile app integration for roadside damage assessment.

Multi-user dashboards with WebSockets.

👨‍💻 Author

Developed with ❤️ in India 🇮🇳
M.Tech CSE (AI & DS) Project


---
