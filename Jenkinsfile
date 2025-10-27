// Jenkinsfile — Linux-friendly, creates ephemeral venv in /tmp to avoid workspace permission locks
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
        // best-effort workspace wipe at start
        deleteDir()
      }
    }

    stage('Checkout') {
      steps {
        checkout scm
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
          # install dvc (change extras if you use s3, gdrive etc.)
          "$PIP" install "dvc[gdrive]" >/dev/null
          "$DVC" version
        '''
      }
    }

    stage('Sanitize DVC config') {
      steps {
        // Re-write .dvc/config as UTF-8 (portable way)
        sh '''
          if [ -f .dvc/config ]; then
            python3 - <<'PY'
import io,sys
with io.open('.dvc/config','r',encoding='utf-8',errors='surrogateescape') as f:
    s=f.read()
with io.open('.dvc/config','w',encoding='utf-8') as f:
    f.write(s)
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
          "$DVC" repro
        '''
      }
    }
  }

  post {
    always {
      // run cleanup inside node (so workspace FilePath is available)
      node {
        sh '''
          set +e
          echo "Removing ephemeral venv: $VENV"
          rm -rf "$VENV" || true

          # best-effort workspace cleanup (careful: removes workspace contents)
          echo "Cleaning workspace contents"
          rm -rf "${WORKSPACE:?}/"* || true
          set -e
        '''
      }
    }
  }
}
