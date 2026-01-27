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
                sh 'docker compose up -d mysql'
            }
        }

        stage('Wait for MySQL') {
            steps {
                sh '''
                until docker compose exec -T mysql mysqladmin ping -h localhost --silent; do
                  echo "Waiting for MySQL..."
                  sleep 2
                done
                '''
            }
        }

        stage('Run migrations') {
            steps {
                sh 'docker compose run --rm web python manage.py migrate'
            }
        }

        stage('Run Django tests') {
            steps {
                sh 'docker compose run --rm web python manage.py test'
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v'
        }
    }
}
