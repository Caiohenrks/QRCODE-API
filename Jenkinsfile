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
                sh '/opt/sonar-scanner/bin/sonar-scanner -Dsonar.projectKey=QRCODE-API -Dsonar.sources=. -Dsonar.host.url=http://dockerlab:9000 -Dsonar.token=squ_924168670f71ab32440fda9ced08771703722cfd'
            }
        }

        stage('Docker build') {
            steps {
                sh 'docker rm -f qrcodeapi || true'
                sh 'docker rmi -f qrcodeapi || true'
                sh 'docker build -t qrcodeapi .'
                sh 'docker run -d -p 5000:5000 --name qrcodeapi qrcodeapi'
            }
        }

        stage('Push Nexus') {
        steps {
            script {
                def nexusUrl = '192.168.15.80:8082'
                def repoName = 'docker'
    
                withCredentials([usernamePassword(credentialsId: 'NexusLogin', usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD')]) {
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
