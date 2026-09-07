pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '417521971848'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse --short=7 HEAD',
                        returnStdout: true
                    ).trim()

                    echo "Image tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Test') {
            steps {
                sh '''
                    set -e

                    for service in frontend product-service order-service; do
                        echo "Testing $service"

                        cd services/$service
                        python3 -m py_compile app.py
                        cd ../..
                    done
                '''
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                    set -e

                    docker build \
                      -t frontend:$IMAGE_TAG \
                      services/frontend

                    docker build \
                      -t product-service:$IMAGE_TAG \
                      services/product-service

                    docker build \
                      -t order-service:$IMAGE_TAG \
                      services/order-service
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region "$AWS_REGION" | \
                    docker login \
                      --username AWS \
                      --password-stdin "$ECR_REGISTRY"
                '''
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                    docker tag frontend:$IMAGE_TAG \
                      "$ECR_REGISTRY/frontend:$IMAGE_TAG"

                    docker tag product-service:$IMAGE_TAG \
                      "$ECR_REGISTRY/product-service:$IMAGE_TAG"

                    docker tag order-service:$IMAGE_TAG \
                      "$ECR_REGISTRY/order-service:$IMAGE_TAG"
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                    set -e

                    docker push "$ECR_REGISTRY/frontend:$IMAGE_TAG"
                    docker push "$ECR_REGISTRY/product-service:$IMAGE_TAG"
                    docker push "$ECR_REGISTRY/order-service:$IMAGE_TAG"
                '''
            }
        }
    }

    post {
        success {
            echo "Images successfully pushed to ECR with tag: ${env.IMAGE_TAG}"
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
