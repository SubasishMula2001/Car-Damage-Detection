

---

````markdown
# 🚗 AutoInspect AI — Car Damage Detection System

A full-stack deep learning application that automatically detects **car damage type** from images (Front/Rear — Normal, Broken, Crushed).

Built using **ResNet50 + FastAPI + HTML/CSS/JS**, and fully deployed on **Microsoft Azure App Service using Docker**.

> Upgraded version with:  
> - Full frontend camera-based UI  
> - FastAPI backend  
> - Azure cloud deployment  
> - Real-time prediction (every 3 seconds)

---

## 🚀 Live Demo

| Component | URL |
|-----------|-----|
| 🌐 Full Application (Azure) | **https://car-damage-app-eastus.azurewebsites.net/static/index.html** |

---

## 📌 Key Features

- 🧠 Deep Learning model (**ResNet50**) trained for 6 damage classes  
- 🚘 Predicts: **Front Normal, Front Broken, Front Crushed, Rear Normal, Rear Broken, Rear Crushed**  
- 📷 **Live camera detection** (auto-capture every 3 seconds)  
- ⚡ Fast and accurate predictions via FastAPI backend  
- 🐳 Backend fully containerized with Docker  
- ☁️ Deployed on **Microsoft Azure App Service**  
- 📱 Clean and responsive HTML/CSS/JS interface

---

## 🛠️ Tech Stack

| Layer | Tools Used |
|-------|------------|
| **Model** | PyTorch, ResNet50, CNN |
| **Backend** | FastAPI, Uvicorn, Python |
| **Frontend** | HTML, CSS, JavaScript |
| **Deployment** | Azure App Service, Docker |
| **Development** | Jupyter Notebook, VS Code, GitHub |

---

## 📬 API Usage

### **POST** `/predict`

- **Headers:** `Content-Type: multipart/form-data`  
- **Body:** Image file (`file`)  
- **URL:**  
  `https://car-damage-app-eastus.azurewebsites.net/predict`

### ✔️ Sample Request (cURL)

```bash
curl -X POST -F "file=@test.jpg" https://car-damage-app-eastus.azurewebsites.net/predict
```

### ✔️ Sample Response

```json
{
  "prediction": "Rear Broken",
  "confidence": 0.93
}
```

---

## 🧠 Model Details

- **Base model:** ResNet50 (pre-trained on ImageNet)  
- **Fine-tuned** for 6 car damage classes (Front/Rear × Normal/Broken/Crushed)  
- Dataset contains front & rear car images with augmentation and normalization  
- Techniques used:
  - Data augmentation (rotation, flip, zoom)  
  - Transfer learning (fine-tuning)  
  - Batch normalization & dropout to reduce overfitting

### 📊 Final Metrics

- **Training Accuracy:** 94%  
- **Validation Accuracy:** 91%  
- **Test Accuracy:** 92%  
- **Inference Speed:** ~1 sec / image

---

## 🖥️ Frontend

- Built with **HTML / CSS / JavaScript**  
- Auto-captures images from live camera feed (every 3 seconds)  
- Sends images to FastAPI backend and displays predictions in real time  
- Mobile-friendly and simple UI for quick inspections

---

## 📸 Screenshots

> Add images to a `/screenshots` folder in your repository and reference them below.

| Live Camera | Prediction Output |
|-------------|-------------------|
| ![camera](screenshots/camera.png) | ![output](screenshots/output.png) |

---

## ⚙️ Local Setup

### 🔧 Step-by-step

```bash
# 1. Clone the repository
git clone https://github.com/SubasishMula2001/Car-Damage-Detection.git
cd Car-Damage-Detection

# 2. (Optional) Create virtual environment
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# 3. Install requirements
pip install -r requirements.txt

# 4. Run FastAPI backend (from project root)
uvicorn app:app --reload
```

### 🔗 Local URLs

- Frontend: open `static/index.html` in your browser  
- Backend: `http://127.0.0.1:8000/predict`

---

## 🌍 Deployment

| Platform | Purpose | Link |
|----------|---------|------|
| **Azure App Service** | Full App Deployment (Frontend + Backend) | https://car-damage-app-eastus.azurewebsites.net/static/index.html |
| **Docker** | Containerized FastAPI backend (used for Azure deployment) | — |

> Ensure CORS is allowed on the API and that the frontend points to the correct API URL when deployed.

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
```

---

## 🔧 Project Structure (suggested)

```
Car-Damage-Detection/
├── app.py                  # FastAPI app
├── saved_model.pth         # Trained PyTorch model (git-lfs or omit large files)
├── requirements.txt
├── static/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── screenshots/
│   ├── camera.png
│   └── output.png
├── notebooks/
│   └── training_notebook.ipynb
└── README.md
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
````

---

✅ **THIS is the original unrendered Markdown.**  
When you paste this into GitHub, it will display perfectly with:

- Proper `#` headings  
- Proper `##` subheadings  
- Proper `---` separators  
- Tables & code blocks  
- Emojis  
- Line breaks  

If you want, I can also provide:

✅ RAW LinkedIn post  
✅ RAW GitHub short description  
✅ RAW project summary for resume
