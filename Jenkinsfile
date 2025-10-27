// Jenkinsfile — Linux-friendly declarative pipeline (fixed post section)
pipeline {
  agent any
  options { timestamps() }

  environment {
    VENV = "/tmp/venv_${env.BUILD_NUMBER}"
    PY   = "${env.VENV}/bin/python3"
    PIP  = "${env.VENV}/bin/pip"
    DVC  = "${env.VENV}/bin/dvc"
  }

  stages {
    stage('Clean') {
      steps {
        deleteDir()
      }
    }

    stage('Checkout') {
  steps {
    checkout([
      $class: 'GitSCM',
      branches: [[name: '*/main']],
      doGenerateSubmoduleConfigurations: false,
      extensions: [[$class: 'CloneOption', depth: 1, noTags: false, shallow: true]],
      userRemoteConfigs: [[url: 'https://github.com/SubasishMula2001/Car-Damage-Detection.git', credentialsId: 'git-creds']]
    ])
  }
}


    stage('Setup Python') {
      steps {
        sh '''
          set -euo pipefail
          echo "Creating venv at $VENV"
          python3 -m venv "$VENV"
          "$PIP" install --upgrade pip
          if [ -f requirements.txt ]; then
            "$PIP" install -r requirements.txt
          fi
          "$PIP" install "dvc[gdrive]" >/dev/null || true
          "$DVC" version || true
        '''
      }
    }

    stage('Sanitize DVC config') {
      steps {
        sh '''
          if [ -f .dvc/config ]; then
            python3 - <<'PY'
import io
with io.open('.dvc/config','r',encoding='utf-8',errors='surrogateescape') as f: s=f.read()
with io.open('.dvc/config','w',encoding='utf-8') as f: f.write(s)
print(".dvc/config normalized to UTF-8")
PY
          fi
        '''
      }
    }

    stage('DVC Pull (optional)') {
      when { expression { fileExists('.dvc/config') } }
      steps {
        sh '''
          set +e
          "$DVC" pull -r gdrive-remote
          RC=$?
          if [ $RC -ne 0 ]; then
            echo "dvc pull failed or skipped (exit $RC)"
          fi
          set -e
        '''
      }
    }

    stage('DVC Repro') {
      steps {
        sh '''
          "$DVC" repro || true
        '''
      }
    }
  }

  post {
    always {
      // Use script so we can conditionally run steps; avoid using node { } here.
      script {
        // remove ephemeral venv we created in /tmp
        if (env.VENV) {
          sh "rm -rf ${env.VENV} || true"
        }
        // best-effort workspace cleanup (runs in the current agent context)
        // deleteDir() works inside script in declarative pipelines
        try {
          deleteDir()
        } catch (err) {
          echo "deleteDir() failed: ${err}"
        }
      }
    }
  }
}
