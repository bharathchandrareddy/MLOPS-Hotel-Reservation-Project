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
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_CREDENTIALS_FILE')]) {
                    script {
                        echo 'Building and pushing Docker image to GCR...'
                        sh 'cp $GOOGLE_APPLICATION_CREDENTIALS gcp-credentials.json' 
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_CREDENTIALS_FILE}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        # Copy credentials file temporarily into Docker context
                        cp ${GOOGLE_CREDENTIALS_FILE} ./gcp-credentials.json

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:hotel_reservation .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:hotel_reservation

                        rm gcp-credentials.json
                        '''

                }
            }
    }
}

    }
}