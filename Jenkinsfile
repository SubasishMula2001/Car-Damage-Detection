pipeline {
    agent any
    environment {
        VENV = '.venv'
        PYTHON = 'python3.13'
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
                  python3 --version
                  which python3
                  rm -rf ${VENV}
                  python3 -m venv ${VENV}
                  . ${VENV}/bin/activate
                  python -m ensurepip --upgrade
                  python -m pip install --upgrade pip setuptools wheel
                  python -m pip install -r backend/requirements.txt dvc
                  dvc pull || true
                  dvc repro -f
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'data/processed/**', allowEmptyArchive: true
        }
    }
}
