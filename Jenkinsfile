pipeline {
    agent any

    stages {
        stage('Clonar Repositório') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/laboratorio-de-pogramacao/lab09.git'
            }
        }
        stage('Configurar Ambiente') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }
        stage('Migrações da Base de Dados') {
            steps {
                sh './venv/bin/python manage.py migrate --noinput'
            }
        }
        stage('Executar Testes') {
            steps {
                sh './venv/bin/coverage run --source="." manage.py test'
            }
        }
        stage('Gerar Relatórios de Cobertura') {
            steps {
                sh '''
                    ./venv/bin/coverage xml
                    ./venv/bin/coverage html -d htmlcov
                '''
            }
        }
    }

    post {
        always {
            junit '*/**/TEST-*.xml'
            publishCoverage adapters: [coberturaAdapter(path: '**/coverage.xml')], sourceFileResolver: sourceFiles('NEVER_STORE')
            archiveArtifacts artifacts: 'htmlcov/**', fingerprint: true
        }
    }
}