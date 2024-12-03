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
                    nix-shell --command "
                        python3 -m venv .venv &&
                        source .venv/bin/activate &&
                        pip install --upgrade pip &&
                        pip install -r requirements.txt
                    "
                '''
            }
        }
        stage('Migrações da Base de Dados') {
            steps {
                sh '''
                    nix-shell --command "
                        source .venv/bin/activate &&
                        python manage.py migrate --noinput
                    "
                '''
            }
        }
        stage('Executar Testes') {
            steps {
                sh '''
                    nix-shell --command "
                        source .venv/bin/activate &&
                        coverage run --source='.' manage.py test
                    "
                '''
            }
        }
        stage('Gerar Relatórios de Cobertura') {
            steps {
                sh '''
                    nix-shell --command "
                        source .venv/bin/activate &&
                        coverage xml &&
                        coverage html -d htmlcov
                    "
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