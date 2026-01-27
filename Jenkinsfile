pipeline {
    agent any

    environment {
        SECRET_KEY = 'jenkins-temp-secret'
        DJANGO_DEBUG = 'True'

        DB_NAME = 'django_db'
        DB_USER = 'django_user'
        DB_PASSWORD = 'django_password'
        DB_HOST = 'mysql'
        DB_PORT = '3306'

        MYSQL_ROOT_PASSWORD = 'rootpassword'
        MYSQL_DATABASE = 'django_db'
        MYSQL_USER = 'django_user'
        MYSQL_PASSWORD = 'django_password'
    }

    stages {

        stage('Build services') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start MySQL') {
            steps {
                sh 'docker compose up -d mysql'
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
