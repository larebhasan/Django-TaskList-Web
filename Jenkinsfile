pipeline {
    agent any

    environment {
        PATH = "/usr/libexec/docker/cli-plugins:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    }

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
