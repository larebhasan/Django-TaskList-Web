pipeline {
    agent any

    stages {
        stage('Build services') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run Django container') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            sh 'docker compose down'
        }
    }
}
