🚗 AutoInspect AI — Car Damage Detection System

A full-stack deep learning application that automatically detects car damage type from images (Front/Rear — Normal, Broken, Crushed).

Built using ResNet50 + FastAPI + HTML/CSS/JS, and fully deployed on Microsoft Azure App Service using Docker.

Upgraded version with:

Full frontend camera-based UI

FastAPI backend

Azure cloud deployment

Real-time prediction (every 3 seconds)

🚀 Live Demo
Component	URL
🌐 Full Application (Azure)	https://car-damage-app-eastus.azurewebsites.net/static/index.html
📌 Key Features

🧠 Deep Learning model (ResNet50) trained for 6 damage classes

🚘 Predicts: Front Normal, Front Broken, Front Crushed, Rear Normal, Rear Broken, Rear Crushed

📷 Live camera prediction (auto-captures every 3 seconds)

⚡ Instant results with FastAPI backend

🐳 Containerized using Docker

☁️ Deployed on Azure App Service

📱 Simple and user-friendly UI (HTML/CSS/JS)

🛠️ Tech Stack
Layer	Tools Used
Model	PyTorch, ResNet50, CNN
Backend	FastAPI, Uvicorn, Python
Frontend	HTML, CSS, JavaScript
Deployment	Azure App Service, Docker
Development	Jupyter Notebook, VS Code, GitHub
📬 API Usage
POST /predict

Headers: Content-Type: multipart/form-data

Body: Image file (file)

URL:
https://car-damage-app-eastus.azurewebsites.net/predict

✅ Example (using cURL)
curl -X POST -F "file=@test.jpg" https://car-damage-app-eastus.azurewebsites.net/predict

✅ Sample Response
{
  "prediction": "Rear Broken",
  "confidence": 0.93
}

🧠 Model Details

Base model: ResNet50 pre-trained on ImageNet

Fine-tuned to classify 6 categories

Dataset includes images of front & rear car surfaces

Techniques used:

Data augmentation (rotate, flip, zoom)

Transfer learning

Normalization

Dropout to reduce overfitting

Final Accuracy:

Training: 94%

Validation: 91%

Test: 92%

🖥️ Frontend

Built with HTML, CSS, and JavaScript

Features:

Live camera feed capture

Automatic image capture every 3 seconds

Displays predicted label instantly

Works on mobile and desktop

📷 Screenshots
Live Camera	Prediction Output

	

(Add screenshots in your repo folder screenshots/)

⚙️ Local Setup
🔧 Step-by-step
# 1. Clone repository
git clone https://github.com/<your-username>/Car-Damage-Detection.git
cd Car-Damage-Detection

# 2. Create virtual environment (optional)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run FastAPI backend
uvicorn app:app --reload

🔗 Local URLs

Frontend: Open static/index.html

Backend: http://127.0.0.1:8000/predict

🌍 Deployment
Platform	Purpose	Link
Azure App Service	Full Application (Frontend + Backend)	https://car-damage-app-eastus.azurewebsites.net/static/index.html

Docker	Containerized FastAPI backend	Deployed on Azure
📦 Requirements
fastapi
uvicorn
pytorch
torchvision
pillow
python-multipart

🙋‍♂️ Author

Subasish Mula
📧 subasishmula@gmail.com

🔗 GitHub: https://github.com/SubasishMula2001

📄 License

This project is licensed under the MIT License.

⭐ Found this project useful? Don’t forget to star the repo!
