// // Jenkinsfile — Linux-friendly declarative pipeline (fixed post section)
// pipeline {
//   agent any
//   options { timestamps() }

//   environment {
//     VENV = "/tmp/venv_${env.BUILD_NUMBER}"
//     PY   = "${env.VENV}/bin/python3"
//     PIP  = "${env.VENV}/bin/pip"
//     DVC  = "${env.VENV}/bin/dvc"
//   }

//   stages {
//     stage('Clean') {
//       steps {
//         deleteDir()
//       }
//     }

//     stage('Checkout') {
//   steps {
//     checkout([
//       $class: 'GitSCM',
//       branches: [[name: '*/main']],
//       doGenerateSubmoduleConfigurations: false,
//       extensions: [[$class: 'CloneOption', depth: 1, noTags: false, shallow: true]],
//       userRemoteConfigs: [[url: 'https://github.com/SubasishMula2001/Car-Damage-Detection.git', credentialsId: 'git-creds']]
//     ])
//   }
// }


//     stage('Setup Python') {
//       steps {
//         sh '''
//           set -euo pipefail
//           echo "Creating venv at $VENV"
//           python3 -m venv "$VENV"
//           "$PIP" install --upgrade pip
//           if [ -f requirements.txt ]; then
//             "$PIP" install -r requirements.txt
//           fi
//           "$PIP" install "dvc[gdrive]" >/dev/null || true
//           "$DVC" version || true
//         '''
//       }
//     }

//     stage('Sanitize DVC config') {
//       steps {
//         sh '''
//           if [ -f .dvc/config ]; then
//             python3 - <<'PY'
// import io
// with io.open('.dvc/config','r',encoding='utf-8',errors='surrogateescape') as f: s=f.read()
// with io.open('.dvc/config','w',encoding='utf-8') as f: f.write(s)
// print(".dvc/config normalized to UTF-8")
// PY
//           fi
//         '''
//       }
//     }

//     stage('DVC Pull (optional)') {
//       when { expression { fileExists('.dvc/config') } }
//       steps {
//         sh '''
//           set +e
//           "$DVC" pull -r gdrive-remote
//           RC=$?
//           if [ $RC -ne 0 ]; then
//             echo "dvc pull failed or skipped (exit $RC)"
//           fi
//           set -e
//         '''
//       }
//     }

//     stage('DVC Repro') {
//       steps {
//         sh '''
//           "$DVC" repro || true
//         '''
//       }
//     }
//   }

//   post {
//     always {
//       // Use script so we can conditionally run steps; avoid using node { } here.
//       script {
//         // remove ephemeral venv we created in /tmp
//         if (env.VENV) {
//           sh "rm -rf ${env.VENV} || true"
//         }
//         // best-effort workspace cleanup (runs in the current agent context)
//         // deleteDir() works inside script in declarative pipelines
//         try {
//           deleteDir()
//         } catch (err) {
//           echo "deleteDir() failed: ${err}"
//         }
//       }
//     }
//   }
// }
// Jenkinsfile (Docker-based declarative pipeline, Linux)
pipeline {
  agent {
    // Uses a Docker image so the agent itself doesn't need Python/DVC preinstalled.
    docker {
      image 'python:3.11-slim'
      args  '--user 1000:1000 --env DEBIAN_FRONTEND=noninteractive'
    }
  }

  options {
    timestamps()
    // keep a reasonable timeout for long dvc pulls or installs
    timeout(time: 60, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '30'))
  }

  environment {
    // Replace these with proper Jenkins credentials IDs if you bind secrets below
    GIT_CREDENTIALS = 'git-creds'   // configure in Jenkins -> Credentials and set here
    DVC_REMOTE_NAME = 'gdrive-remote' // optional: the remote name you expect in .dvc/config
    ARTIFACTS = '**/models/**,**/saved_model.*' // adjust artifact globs as needed
  }

  stages {
    stage('Prep / Diagnostics') {
      steps {
        sh '''
          set -euxo pipefail
          echo "=== container info ==="
          uname -a || true
          id || true
          echo "=== python/git/dvc check ==="
          python --version || true
          pip --version || true
          git --version || true
        '''
      }
    }

    stage('Checkout (robust clone)') {
  steps {
    sh '''
      set -euxo pipefail
      echo "Workspace: ${WORKSPACE}"
      # Tune git for large transfers / flaky networks
      git --version || true
      git config --global http.postBuffer 524288000 || true
      git config --global http.lowSpeedLimit 0 || true
      git config --global http.lowSpeedTime 999999 || true

      REPO="https://github.com/SubasishMula2001/Car-Damage-Detection.git"
      DEST="${WORKSPACE}/_tmp_clone"
      RETRIES=3

      # Ensure clean start
      rm -rf "$DEST"
      for i in $(seq 1 $RETRIES); do
        echo "Clone attempt $i ..."
        # Try a shallow clone first (fast). If it fails, fall back to full clone.
        GIT_TRACE=1 GIT_CURL_VERBOSE=1 git clone --depth 1 "$REPO" "$DEST" && break || true
        echo "Shallow clone failed; removing partial clone and retrying with full clone..."
        rm -rf "$DEST"
        sleep 2
        GIT_TRACE=1 GIT_CURL_VERBOSE=1 git clone "$REPO" "$DEST" && break || true
        # remove partial and retry
        rm -rf "$DEST"
        sleep 3
      done

      if [ ! -d "$DEST/.git" ]; then
        echo "ERROR: git clone failed after $RETRIES attempts"
        # show disk and network diagnostics
        df -h || true
        ip route || true
        exit 1
      fi

      # Move contents into the pipeline workspace root (preserve workspace expected layout)
      shopt -s dotglob || true
      cp -a "$DEST/." "${WORKSPACE}/"
      rm -rf "$DEST"
      echo "Repo cloned into workspace"
    '''
  }
}

    stage('Install dependencies & DVC') {
      steps {
        sh '''
          set -euxo pipefail
          # minimal apt-get to enable dvc extras (if needed)
          apt-get update -y
          apt-get install -y --no-install-recommends git gnupg2 curl ca-certificates
          # Use python -m pip to avoid ambiguous pip binaries
          python -m pip install --upgrade pip wheel setuptools
          if [ -f requirements.txt ]; then
            python -m pip install -r requirements.txt
          fi
          # Install DVC with gdrive support (only if you use gdrive remote)
          python -m pip install "dvc[gdrive]"
          dvc version || true
        '''
      }
    }

    stage('Sanity: show DVC remotes') {
      when { expression { fileExists('.dvc/config') } }
      steps {
        sh '''
          set -euxo pipefail
          echo "=== .dvc/config contents ==="
          sed -n '1,200p' .dvc/config || true
          echo "=== dvc remote list ==="
          dvc remote list || true
        '''
      }
    }

    stage('DVC Pull (best-effort)') {
      when { expression { fileExists('.dvc/config') } }
      steps {
        sh '''
          set -euxo pipefail
          # Keep this tolerant — failing pull should not necessarily stop CI if remote not reachable
          set +e
          dvc pull -v
          RC=$?
          set -e
          if [ "$RC" -ne 0 ]; then
            echo "WARNING: dvc pull failed (exit $RC). Continue to allow debugging artifacts in logs."
            dvc status || true
          fi
        '''
      }
    }

    stage('Run pipeline / Repro') {
      steps {
        sh '''
          set -euxo pipefail
          # Run dvc repro if pipeline exists
          if [ -f dvc.yaml ] || [ -f dvc.yaml.lock ]; then
            dvc repro || echo "dvc repro failed or nothing to run"
          else
            echo "No dvc.yaml detected — skipping dvc repro"
          fi

          # Example training command — replace with your project's train entrypoint
          if [ -f train.py ]; then
            python train.py || echo "train.py exited non-zero"
          else
            echo "No train.py found — add your training command to the Jenkinsfile"
          fi
        '''
      }
    }

    stage('Tests (optional)') {
      steps {
        sh '''
          set -euxo pipefail
          if command -v pytest >/dev/null 2>&1 && [ -d tests ]; then
            pytest -q || echo "Some tests failed; inspect junit or logs"
          else
            echo "pytest not configured or tests/ missing — skipping"
          fi
        '''
      }
    }

    stage('Archive artifacts') {
      steps {
        archiveArtifacts artifacts: env.ARTIFACTS, allowEmptyArchive: true
      }
    }
  }

  post {
    always {
      sh 'echo "Build finished at: $(date -u +\"%Y-%m-%dT%H:%M:%SZ\")"'
      junit allowEmptyResults: true, testResults: 'tests/**/junit-*.xml'
    }

    failure {
      sh 'echo "Build failed. See console output above for errors." || true'
    }
  }
}
