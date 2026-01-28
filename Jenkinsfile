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

       stage('Wait for MySQL') {
    steps {
        sh '''
        echo "Waiting for MySQL to be ready..."
        for i in {1..20}; do
          docker compose exec -T mysql mysqladmin ping -h localhost && break
          sleep 3
        done
        '''
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
