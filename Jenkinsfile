pipeline {
    agent any

    stages {
        stage('Build services') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start services') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Run migrations') {
            steps {
                sh 'docker compose exec -T web python manage.py migrate'
            }
        }

        stage('Run Django tests') {
            steps {
                sh 'docker compose exec -T web python manage.py test'
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v'
        }
    }
}
