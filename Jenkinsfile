pipeline{
    agent any

    environment {
            VENV_DIR = 'venv'
            GCP_PROJECT = 'hotel-reservation-project-01'
            GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages{
        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .

                    
                    '''

                }
            }
        }
        
        stage('Build & Push Docker Image to GCR') {
      steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          script {
            echo 'Preparing GCP credentials…'
            sh '''
              mkdir -p keys
              cp "$GOOGLE_APPLICATION_CREDENTIALS" keys/gcp-credentials.json
              # authenticate gcloud so docker push to GCR works
              gcloud auth activate-service-account --key-file=keys/gcp-credentials.json
              gcloud auth configure-docker --quiet
            '''
            echo "Building Docker image…"
            sh """
              docker build -t gcr.io/${env.GCP_PROJECT}/${env.IMAGE_NAME}:${env.BUILD_NUMBER} .
            """
            echo "Pushing to GCR…"
            sh """
              docker push gcr.io/${env.GCP_PROJECT}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}
            """
          }
        }
      }
    }
    }
}




