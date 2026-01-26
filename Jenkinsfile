pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image for Django app'
                sh 'docker build -t django-tasklist-ci .'
            }   
        }
    }
}