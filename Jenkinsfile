pipeline{
    agent any

    environment {
            VENV_DIR = 'venv'
    }

    stages{
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
    }
}