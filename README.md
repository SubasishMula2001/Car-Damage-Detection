AutoInspect AI – Car Damage Detection System

AutoInspect AI is an end-to-end car damage detection system built using Deep Learning (ResNet50) and deployed on Microsoft Azure App Service using Docker. The system automatically detects and classifies car damage from images into six categories, helping workshops, insurance teams, and vehicle owners make quicker decisions.

Problem Statement

Manual car inspection takes time and may lead to mistakes, especially when many cars are lined up. This project uses AI to automatically detect car damage from images in just one second, reducing human effort and speeding up the inspection process.

Objectives

Build an automated damage detection system

Reduce manual inspection time

Provide a simple live camera interface

Support decision-making for insurance and service centers

Modules
1. Data Collection & Preprocessing

Collected front and rear car images

Resized, normalized, and augmented (flip, rotate, zoom)

2. Model Development

Used ResNet50 (Transfer Learning)

Classified 6 categories:

Front Normal

Front Broken

Front Crushed

Rear Normal

Rear Broken

Rear Crushed

Achieved ~92% test accuracy

3. Backend – FastAPI

Loads the trained PyTorch model

Accepts image uploads and returns predictions instantly

4. Frontend – HTML/CSS/JavaScript

User-friendly interface

Captures live camera frames

Displays results instantly

5. Deployment – Azure + Docker

Containerized using Docker

Hosted on Azure App Service

Accessible publicly from anywhere

Live Application

https://car-damage-app-eastus.azurewebsites.net/static/index.html

Tech Stack

Model: PyTorch, ResNet50

Backend: FastAPI

Frontend: HTML, CSS, JavaScript

Deployment: Docker, Azure App Service

Tools: Jupyter Notebook, VS Code, GitHub

Results

Training Accuracy: 94%

Validation Accuracy: 91%

Test Accuracy: 92%

Prediction Time: ~1 second per image

Features

Live camera detection

Fast and accurate predictions

Cloud deployment with Azure

Easy to use from browser

Challenges & Learnings
Challenges

Overfitting during training

Smooth camera integration with FastAPI backend

Docker build optimization for Azure

Learnings

Transfer Learning with ResNet50

Cloud deployment and MLOps basics

Full-stack machine learning integration

Future Enhancements

Damage severity and repair cost estimation

Better detection in night/low-light

Integration with insurance claim workflows

Mobile app version (Flutter/React Native)
