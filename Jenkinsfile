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
                      -t frontend:1.1.0 \
                      services/frontend

                    docker build \
                      -t product-service:1.0.0 \
                      services/product-service

                    docker build \
                      -t order-service:1.0.0 \
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
                    docker tag frontend:1.1.0 \
                      "$ECR_REGISTRY/frontend:1.1.0"

                    docker tag product-service:1.0.0 \
                      "$ECR_REGISTRY/product-service:1.0.0"

                    docker tag order-service:1.0.0 \
                      "$ECR_REGISTRY/order-service:1.0.0"
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                    set -e

                    docker push "$ECR_REGISTRY/frontend:1.1.0"
                    docker push "$ECR_REGISTRY/product-service:1.0.0"
                    docker push "$ECR_REGISTRY/order-service:1.0.0"
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD image build and ECR push completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
