pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Clean') { steps { deleteDir() } }
    stage('Checkout') { steps { checkout scm } }

    stage('Setup Python') {
      steps {
        bat '''
          py -3 -m venv venv
          venv\\Scripts\\pip install -U pip
          if exist requirements.txt venv\\Scripts\\pip install -r requirements.txt
          venv\\Scripts\\pip install "dvc[gdrive]"
          venv\\Scripts\\dvc version
        '''
      }
    }

    stage('Sanitize DVC config') {
      steps {
        powershell '''
          if (Test-Path ".dvc\\config") {
            $c = Get-Content .dvc\\config -Raw
            [IO.File]::WriteAllText(".dvc\\config", $c, [Text.UTF8Encoding]::new($false))
          }
        '''
      }
    }

    stage('DVC Pull (optional)') {
      when { expression { return fileExists('.dvc/config') } }
      steps {
        // If you use a GDrive service account, wrap these in withCredentials as shown earlier.
        bat 'venv\\Scripts\\dvc pull -r gdrive-remote || echo "dvc pull skipped or failed"'
      }
    }

    stage('DVC') {
      steps { bat 'venv\\Scripts\\dvc repro' }
    }
  }
}