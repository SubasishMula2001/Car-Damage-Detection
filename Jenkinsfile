pipeline {
  agent any
  environment {
    PYTHON = "python3"
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
    stage('Setup Python') {
      steps {
        sh '''
          ${PYTHON} -m venv ${VENV}
          . ${VENV}/bin/activate
          pip install --upgrade pip
          pip install -r backend/requirements.txt dvc
        '''
      }
    }
    stage('Get Data') {
      steps {
        sh '''
          . ${VENV}/bin/activate
          dvc pull || true
        '''
      }
    }
    stage('Reproduce') {
      steps {
        sh '''
          . ${VENV}/bin/activate
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