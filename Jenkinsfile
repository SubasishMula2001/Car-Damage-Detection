pipeline {
  agent any
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
      agent {
        docker {
          image 'python:3.10-slim'
          args '--user 0:0'
          reuseNode true
        }
      }
      steps {
        sh '''
          set -e
          apt-get update -y
          apt-get install -y git build-essential
          rm -rf ${VENV}
          python3 -m venv ${VENV}
          . ${VENV}/bin/activate
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install -r backend/requirements.txt dvc
          dvc pull || true
          dvc repro -f
        '''
      }
    }
  }

  post { always { archiveArtifacts artifacts: 'data/processed/**', allowEmptyArchive: true } }
}
