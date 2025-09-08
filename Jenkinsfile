pipeline {
    agent any
    options {
        checkoutToSubdirectory('argo-mon-library')
    }
    environment {
        PROJECT_DIR = 'argo-mon-library'
        GIT_COMMIT = sh(script: "cd ${WORKSPACE}/$PROJECT_DIR && git log -1 --format=\"%H\"", returnStdout: true).trim()
        GIT_COMMIT_HASH = sh(script: "cd ${WORKSPACE}/$PROJECT_DIR && git log -1 --format=\"%H\" | cut -c1-7", returnStdout: true).trim()
        GIT_COMMIT_DATE = sh(script: "date -d \"\$(cd ${WORKSPACE}/$PROJECT_DIR && git show -s --format = %ci ${GIT_COMMIT_HASH})\" \"+%Y%m%d%H%M%S\"", returnStdout: true).trim()
    }
    stages {
        stage('Run Linting') {
            agent {
                docker {
                    image 'argo.registry:5000/epel-9-acc'
                    args '-u jenkins:jenkins'
                }
            }
            steps {
                echo 'Executing lint checks'
                sh '''
                    cd ${WORKSPACE}/$PROJECT_DIR
                    rm -f .python-version &>/dev/null
                    rm -rf .coverage* .tox/ coverage.xml &> /dev/null

                    pip install flake8 isort bandit mypy

                    export PATH=$HOME/.local/bin:$PATH

                    echo "Running flake8..."
                    flake8 --max-line-length=120 .

                    echo "Running isort..."
                    isort --check-only .

                    echo "Running bandit..."
                    bandit -r .

                    echo "Running mypy..."
                    if find . -name "*.py" | grep -q .; then
                        mypy --disable-error-code=import-untyped --ignore-missing-imports .
                    else
                        echo "No Python files found. Skipping mypy."
                    fi
                '''
            }
        }
        stage('Run tests') {
            agent {
                docker {
                    image 'argo.registry:5000/epel-9-acc'
                    args '-u jenkins:jenkins'
                }
            }
            steps {
                echo 'Executing tox tests'
                sh '''
                    cd ${WORKSPACE}/$PROJECT_DIR
                    rm -f .python-version &>/dev/null
                    rm -rf .coverage* .tox/ coverage.xml &> /dev/null
                    source $HOME/pyenv.sh
                    ALLPYVERS=$(pyenv versions | grep '^[ ]*[0-9]' | tr '\n' ' ')
                    echo Found Python versions $ALLPYVERS
                    pyenv local $ALLPYVERS
                    export TOX_SKIP_ENV="py27.*|py36.*"
                    if [ -f tox.ini ] || [ -f pyproject.toml ] || [ -f setup.cfg ]; then
                        echo "Running tox..."
                        tox -p all
                        coverage xml --omit=*usr* --omit=*.tox*
                    else
                    echo "No tox config found. Skipping tox."
                    fi
                    '''
                    script {
                        if (fileExists('**/coverage.xml')) {
                            cobertura coberturaReportFile: '**/coverage.xml'
                        } else {
                            echo 'No coverage.xml found. Skipping cobertura report.'
                        }
                    }
            }
        }
        stage('Build Rocky 9') {
            agent {
                docker {
                    image 'argo.registry:5000/epel-9-acc'
                    args '-u jenkins:jenkins'
                }
            }
            steps {
                echo 'Building Rocky 9 RPM...'
                withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'jenkins-rpm-repo', usernameVariable: 'REPOUSER', \
                                                            keyFileVariable: 'REPOKEY')]) {
                    sh "/home/jenkins/build-rpm.sh -w ${WORKSPACE} -b ${BRANCH_NAME} -d rocky9 -p ${PROJECT_DIR} -s ${REPOKEY}"
                                                            }
                archiveArtifacts artifacts: '**/*.rpm', fingerprint: true
            }
        }
        stage ('Upload to PyPI'){
            when {
                branch 'master'
            }
            agent {
                docker {
                    image 'argo.registry:5000/python3'
                }
            }
            steps {
                echo 'Build python package and upload'
                withCredentials(bindings: [usernamePassword(credentialsId: 'pypi-token', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        cd ${WORKSPACE}/$PROJECT_DIR
                        pipenv install --dev
                        pipenv run python setup.py sdist bdist_wheel
                        pipenv run python -m twine upload -u $USERNAME -p $PASSWORD dist/*
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning workspace and exiting'
            cleanWs()
        }
    }
}
