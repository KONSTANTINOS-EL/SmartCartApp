pipeline {
    agent any
    stages {
        stage('Build Containers') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Run Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }
        // Προαιρετικά:
        stage('Run Tests') {
            steps {
                sh 'docker exec smartcart-backend pytest tests/'
            }
        }
    }
}
