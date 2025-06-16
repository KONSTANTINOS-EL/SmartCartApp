pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/KONSTANTINOS-EL/SmartCartApp'
            }
        }
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
