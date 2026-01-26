pipeline {
    agent any

    stages {
        stage('Build services') {
            steps {
                sh 'docker compose build'
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
            sh 'docker compose down'
        }
    }
}
