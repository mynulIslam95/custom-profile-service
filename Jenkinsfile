pipeline {
  agent any
  options {
    timestamps()
  }
  stages {
    stage('Test') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
          mkdir -p reports
          pytest -q --junitxml=reports/junit.xml
        '''
      }
    }
    stage('Package') {
      steps {
        sh 'docker build -t custom-profile-service:${BUILD_NUMBER:-local} .'
      }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/junit.xml'
    }
  }
}
