# 🚗 AutoInspect AI — Car Damage Detection System

A full-stack deep learning application that automatically detects **car damage type** from images (Front/Rear — Normal, Broken, Crushed).

Built using **ResNet50 + FastAPI + HTML/CSS/JS**, and fully deployed on **Microsoft Azure App Service using Docker** with a custom domain.

> Upgraded version with:  
> - Full frontend camera-based UI  
> - FastAPI backend  
> - Azure cloud deployment  
> - Custom domain support  
> - Real-time prediction (every 3 seconds)

---

## 🚀 Live Demo

| Component | URL |
|-----------|-----|
| 🌐 Full Application | **http://autoinspectai.online/** |

---

## 📌 Key Features

- 🧠 Deep Learning model (**ResNet50**) trained for 6 damage classes  
- 🚘 Predicts: **Front Normal, Front Broken, Front Crushed, Rear Normal, Rear Broken, Rear Crushed**  
- 📷 Real-time **camera-based automatic detection**  
- ⚡ Fast prediction via FastAPI backend  
- 🐳 Dockerized backend for deployment  
- ☁️ Hosted with Azure App Service + custom domain  
- 📱 Clean HTML/CSS/JS UI with auto-refresh

---

## 🛠️ Tech Stack

| Layer | Tools Used |
|-------|------------|
| **Model** | PyTorch, ResNet50 |
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | HTML, CSS, JavaScript |
| **Training / Experiments** | Jupyter, DVC |
| **Deployment** | Azure App Service, Docker |
| **Development** | VS Code, GitHub |

---

## 📬 API Usage

### **POST** `/predict`

- **Headers:** `Content-Type: multipart/form-data`  
- **Body:** Image (`file`)  
- **Hosted API URL:**  
  `http://autoinspectai.online/predict`

### ✔️ cURL Example

```bash
curl -X POST -F "file=@test.jpg" http://autoinspectai.online/predict
```

### ✔️ Sample API Response

```json
{
  "prediction": "Rear Broken",
  "confidence": 0.93
}
```

---

## 🧠 Model Details

- **Architecture:** ResNet50 (ImageNet pre-trained)  
- **Custom head:** 6 output classes  
- **Classes:**  
  - Front Normal  
  - Front Broken  
  - Front Crushed  
  - Rear Normal  
  - Rear Broken  
  - Rear Crushed  

### 📊 Metrics

- **Training Accuracy:** 94%  
- **Validation Accuracy:** 91%  
- **Test Accuracy:** 92%  
- **Inference Speed:** ~1 second per image

---

## 🖥️ Frontend

- Built with **HTML/CSS/JS**  
- Auto-captures image every **3 seconds**  
- Sends to backend using Fetch API  
- Displays prediction dynamically  
- Responsive layout  

---

## 📸 Screenshots

(Add your screenshots inside `/screenshots` folder)

| Live Camera | Prediction |
|-------------|-------------|
| ![camera](screenshots/camera.png) | ![output](screenshots/output.png) |

---

## ⚙️ Local Setup

### 🔧 Step-by-step Setup

```bash
# 1. Clone repository
git clone https://github.com/SubasishMula2001/Car-Damage-Detection.git
cd Car-Damage-Detection

# 2. Create virtual env
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run FastAPI backend (correct command)
python -m uvicorn backend.app:app --reload --port 8000
```

### 🔗 Local URLs

- Frontend: open `frontend/index.html`  
- Backend: `http://127.0.0.1:8000/predict`

---

## 🌍 Deployment

| Platform | Purpose | URL |
|----------|---------|-----|
| **Azure App Service** | Deployed App | http://autoinspectai.online/ |
| **Docker** | Backend container | used for Azure deployment |
| **DVC** | Dataset & pipeline tracking | `dvc.yaml` |

---

## 📦 Requirements

```
fastapi
uvicorn
torch
torchvision
pillow
python-multipart
opencv-python
numpy
dvc
```

---

## 📁 Project Structure (Your Repo)

```
CAR_DAMAGE_DETECTION/
├── backend/
│   ├── app.py
│   ├── model_helper.py
│   ├── evaluation.py
│   ├── data_preprocessing.py
│   ├── monitoring.py
│   ├── cascades/
│   └── server_captures/
│
├── data/
├── dvc_store/
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── notebooks/
│   ├── Car_Damage_Detection.ipynb
│   └── damage_prediction.ipynb
│
├── logs/
├── saved_model.pth
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── test.jpg
```

---

## 🙋‍♂️ Author

**Subasish Mula**  
📧 subasishmula@gmail.com  
🔗 GitHub: https://github.com/SubasishMula2001  

---

## 📄 License

This project is licensed under the **MIT License**.

---

### ⭐ If you found this helpful, please star the repo!
