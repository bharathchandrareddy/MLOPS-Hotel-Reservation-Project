// pipeline{
//     agent any

//     environment {
//             VENV_DIR = 'venv'
//             GCP_PROJECT = 'hotel-reservation-project-01'
//             GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
//     }

//     stages{
//         stage('Setting up our Virtual Environment and Installing dependancies'){
//             steps{
//                 script{
//                     echo 'Setting up our Virtual Environment and Installing dependancies............'
//                     sh '''
//                     python3 -m venv ${VENV_DIR}
//                     . ${VENV_DIR}/bin/activate
//                     pip install --upgrade pip
//                     pip install -e .

                    
//                     '''

//                 }
//             }
//         }
        
//         stage('Build & Push Docker Image to GCR') {

//             steps {
//                 withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_CREDENTIALS_FILE')]) {
//                     script {
//                         echo 'Building and pushing Docker image to GCR...'
//                         sh 'cp $GOOGLE_APPLICATION_CREDENTIALS /app/keys/gcp-credentials.json' 
//                         sh '''
//                         export PATH=$PATH:${GCLOUD_PATH}

//                         gcloud auth activate-service-account --key-file=${GOOGLE_CREDENTIALS_FILE}
//                         gcloud config set project ${GCP_PROJECT}
//                         gcloud auth configure-docker --quiet

//                         # Copy credentials file temporarily into Docker context
//                         cp ${GOOGLE_CREDENTIALS_FILE} /app/keys/gcp-credentials.json

//                         docker build -t gcr.io/${GCP_PROJECT}/ml-project:hotel_reservation .

//                         docker push gcr.io/${GCP_PROJECT}/ml-project:hotel_reservation

//                         rm gcp-credentials.json
//                         '''

//                 }
//             }
//     }
// }

//     }
// }



pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "mlops-new-447207"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/MLOPS-COURSE-PROJECT-1.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:hotel_reservation .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:hotel_reservation 

                        '''
                    }
                }
            }
        }
    }
}


