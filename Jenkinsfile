pipeline {
    agent any

    stages {
        stage('Build services') {
            steps {
                echo 'Building services using docker compose'
                sh 'docker compose build'
            }
        }

        stage('Run Django container') {
            steps {
                echo 'Starting Django container'
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            echo 'Stopping and removing containers'
            sh 'docker compose down'
        }
    }
}
