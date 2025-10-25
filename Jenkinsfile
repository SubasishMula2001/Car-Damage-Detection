pipeline {
  agent any
  environment {
    VENV = ".venv"
  }
  stages {
    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/SubasishMula2001/Car-Damage-Detection.git', credentialsId: 'git-creds']]
        ])
      }
    }
    stage('Run inside Python image') {
      steps {
        script {
          docker.image('python:3.9-slim').inside {
            sh '''
              apt-get update -y && apt-get install -y git build-essential
              python -m venv ${VENV}
              . ${VENV}/bin/activate
              pip install --upgrade pip
              pip install -r backend/requirements.txt dvc
              dvc pull || true
              dvc repro -f
            '''
          }
        }
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'data/processed/**', allowEmptyArchive: true
    }
  }
}