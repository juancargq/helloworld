pipeline {
    agent any
    stages {
        stage('Get Code') {
            steps {
                git 'https://github.com/juancargq/helloworld.git'
                bat 'dir'
            }
        }   
        
        stage('Unit') {
            steps {
                bat '''
                    SET PYTHONPATH=.
                    coverage run --branch --source=app --omit=app/__init__.py,app/api.py -m pytest --junitxml=junit-report.xml test/unit
                '''
                junit 'junit-report.xml'
            }
        }
        
        stage('Coverage') {
            steps {
                bat 'coverage xml'

                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    cobertura coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '100,80,90', lineCoverageTargets: '100,85,95'
                }
            }
        }
        
        stage('Static') {
            steps {
                bat '''
                    flake8 --exit-zero --format=pylint app > flake8.out
                '''
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], qualityGates: [[threshold: 8, type: 'TOTAL', unstable: true], [threshold: 10, type: 'TOTAL', unstable: false]]
                }
            }
        }
        
        stage('Security Test') {
            steps {
                bat '''
                    bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}"
                '''
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], qualityGates: [[threshold: 2, type: 'TOTAL', unstable: true], [threshold: 4, type: 'TOTAL', unstable: false]]
                }
            }
        }
        
        stage('Performance') {
            steps {
                bat '''
                    SET FLASK_APP=app/api.py
                    start flask run
                    C:/Users/jcgom/Documents/apache-jmeter/bin/jmeter.bat -n -t test/jmeter/caso-practico-1b.jmx -f -l caso-practico-1b.jtl
                '''
                perfReport sourceDataFiles: 'caso-practico-1b.jtl'
            }
        }
    }
}