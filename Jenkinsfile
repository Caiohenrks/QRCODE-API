import groovy.json.JsonSlurper

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }  
        
        stage('SonarQube analysis') {
            steps {
                withCredentials([string(credentialsId: 'SONARQUBE_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh "/opt/sonar-scanner/bin/sonar-scanner -Dsonar.projectKey=${JOB_NAME} -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.token=${SONAR_TOKEN} -Dsonar.python.version=3.8"
                }
            }
        }

        stage('Docker build') {
            steps {
                sh 'docker rm -f qrcodeapi || true'
                sh 'docker rmi -f qrcodeapi || true'
                sh 'docker build -t qrcodeapi .'
                sh 'docker run -d -p 5000:5000 --name qrcodeapi --restart always qrcodeapi'
            }
        }

        stage('Push Nexus') {
        steps {
            script {
                def nexusUrl = 'localhost:8082'
                def repoName = 'docker'
    
                withCredentials([usernamePassword(credentialsId: 'NEXUS_CREDENTIALS', usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
                    sh "docker login -u $NEXUS_USERNAME -p $NEXUS_PASSWORD ${nexusUrl}"
                    sh "docker tag qrcodeapi ${nexusUrl}/${repoName}:latest"
                    sh "docker push ${nexusUrl}/${repoName}:latest"
                }
            }
        }
    }


        stage('Test Endpoints') {
            steps {
                sleep(time: 10, unit: 'SECONDS')
                sh 'sudo chmod +x test_endpoints.sh'
                sh './test_endpoints.sh'
            }
        }
    }
}
