pipeline {
  agent {
    docker {
      image 'python:3.10-slim'     // TensorFlow 2.14 supports py3.10
      args  '-u root:root'
    }
  }
  environment { VENV = ".venv" }
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
          apt-get update -y && apt-get install -y git build-essential python3-venv python3-distutils
          ln -sf /usr/bin/python3 /usr/bin/python || true
          python3 -m venv ${VENV}
          . ${VENV}/bin/activate
          python -m pip install --upgrade pip
          python -m pip install -r backend/requirements.txt dvc
          dvc pull || true
          dvc repro -f
        '''
      }
    }
  }
  post { always { archiveArtifacts artifacts: 'data/processed/**', allowEmptyArchive: true } }
}