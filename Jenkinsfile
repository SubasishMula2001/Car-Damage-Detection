pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/<your-repo>/car-damage-detection.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'pip install -r backend/requirements.txt'
            }
        }

        stage('Pull Model from DVC') {
            steps {
                sh 'dvc pull'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest tests/'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
