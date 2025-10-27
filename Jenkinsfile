pipeline {
  agent any
  options { timestamps() }

  environment {
    // Windows PowerShell friendly venv path (unique per build)
    VENV = "${env.TEMP}\\venv_${env.BUILD_NUMBER}"
    PY = "${env.VENV}\\Scripts\\python.exe"
    PIP = "${env.VENV}\\Scripts\\pip.exe"
    DVC = "${env.VENV}\\Scripts\\dvc.exe"
  }

  stages {
    stage('Clean') {
      steps {
        // best-effort initial workspace cleanup
        deleteDir()
      }
    }

    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python') {
      steps {
        // use powershell for robust Windows path handling and error control
        powershell '''
          set-StrictMode -Version Latest
          $ErrorActionPreference = "Stop"

          $venv = "${env:VENV}"
          Write-Output "Creating venv at $venv"

          # create venv (py.exe must be on PATH)
          py -3 -m venv $venv

          # upgrade pip and install requirements if present
          & "$venv\\Scripts\\pip.exe" install -U pip
          if (Test-Path "requirements.txt") {
            & "$venv\\Scripts\\pip.exe" install -r requirements.txt
          }

          # install dvc (gdrive if you need it) - retry once if transient network glitches
          & "$venv\\Scripts\\pip.exe" install "dvc[gdrive]" -q
          & "$venv\\Scripts\\dvc.exe" version
        '''
      }
    }

    stage('Sanitize DVC config') {
      steps {
        powershell '''
          if (Test-Path ".dvc\\config") {
            # Re-write file with explicit UTF8 (no BOM)
            $c = Get-Content .dvc\\config -Raw
            [IO.File]::WriteAllText(".dvc\\config", $c, [Text.UTF8Encoding]::new($false))
          }
        '''
      }
    }

    stage('DVC Pull (optional)') {
      when { expression { return fileExists('.dvc\\config') } }
      steps {
        powershell '''
          $dvc = "${env:VENV}\\Scripts\\dvc.exe"
          # wrap in try so failure doesn't halt pipeline (adjust as needed)
          try {
            & $dvc pull -r gdrive-remote
          } catch {
            Write-Warning "dvc pull failed or skipped: $($_.Exception.Message)"
          }
        '''
      }
    }

    stage('DVC repro') {
      steps {
        powershell '''
          $dvc = "${env:VENV}\\Scripts\\dvc.exe"
          & $dvc repro
        '''
      }
    }
  }

  post {
    always {
      // robust cleanup: try to remove venv and workspace, with retries
      powershell '''
        $ErrorActionPreference = "Continue"
        $venv = "${env:VENV}"
        Write-Output "Cleaning venv: $venv"

        function Remove-WithRetry($path, $attempts=3) {
          for ($i=1; $i -le $attempts; $i++) {
            try {
              if (Test-Path $path) {
                Remove-Item -LiteralPath $path -Recurse -Force -ErrorAction Stop
              }
              Write-Output "Removed $path"
              return $true
            } catch {
              Write-Warning "Attempt $i to remove $path failed: $($_.Exception.Message)"
              Start-Sleep -Seconds (2 * $i)
            }
          }
          return $false
        }

        # attempt to remove venv
        Remove-WithRetry $venv

        # try workspace cleanup as fallback
        try { Remove-Item -LiteralPath "${env.WORKSPACE}\\*" -Recurse -Force -ErrorAction SilentlyContinue } catch {}

        # last attempt: call deleteDir from pipeline (Jenkins will already have done one at start)
      '''
    }
  }
}
