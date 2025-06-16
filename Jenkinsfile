pipeline {
    agent any
    stages {
        stage('Build Containers') {
            steps {
                bat 'docker-compose build'
            }
        }
        stage('Run Containers') {
            steps {
                bat 'docker-compose up -d'
            }
        }
        // Προαιρετικά:
        stage('Run Tests') {
            steps {
                bat 'docker exec smartcart-backend pytest tests/'
            }
        }
    }
}
