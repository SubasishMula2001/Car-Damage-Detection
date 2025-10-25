pipeline {
  agent {
    docker {
      image 'python:3.12-slim'   // changed from python:3.9-slim
      args  '-u root:root'
    }
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
    stage('Setup & Run') {
      steps {
        sh '''
          apt-get update -y && apt-get install -y git build-essential
          python -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r backend/requirements.txt dvc
          dvc pull || true
          dvc repro -f
        '''
      }
    }
  }
  post { always { archiveArtifacts artifacts: 'data/processed/**', allowEmptyArchive: true } }
}