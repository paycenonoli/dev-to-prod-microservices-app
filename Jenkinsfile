pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '417521971848'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        GITOPS_REPO = 'https://github.com/paycenonoli/dev-to-prod-microservices-gitops.git'
        GITOPS_BRANCH = "jenkins/promote-${env.BUILD_NUMBER}"
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

                    docker build -t frontend:$IMAGE_TAG services/frontend
                    docker build -t product-service:$IMAGE_TAG services/product-service
                    docker build -t order-service:$IMAGE_TAG services/order-service
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

        stage('Push Images') {
            steps {
                sh '''
                    set -e

                    docker tag frontend:$IMAGE_TAG \
                      "$ECR_REGISTRY/frontend:$IMAGE_TAG"

                    docker tag product-service:$IMAGE_TAG \
                      "$ECR_REGISTRY/product-service:$IMAGE_TAG"

                    docker tag order-service:$IMAGE_TAG \
                      "$ECR_REGISTRY/order-service:$IMAGE_TAG"

                    docker push "$ECR_REGISTRY/frontend:$IMAGE_TAG"
                    docker push "$ECR_REGISTRY/product-service:$IMAGE_TAG"
                    docker push "$ECR_REGISTRY/order-service:$IMAGE_TAG"
                '''
            }
        }

        stage('Update GitOps') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-gitops',
                        usernameVariable: 'GITHUB_USER',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e

                        rm -rf gitops

                        git clone \
                          "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/paycenonoli/dev-to-prod-microservices-gitops.git" \
                          gitops

                        cd gitops

                        git checkout -b "$GITOPS_BRANCH"

                        sed -i "s/tag: \".*\"/tag: \\"$IMAGE_TAG\\"/" \
                          environments/dev/frontend-values.yaml

                        sed -i "s/tag: \".*\"/tag: \\"$IMAGE_TAG\\"/" \
                          environments/dev/product-values.yaml

                        sed -i "s/tag: \".*\"/tag: \\"$IMAGE_TAG\\"/" \
                          environments/dev/order-values.yaml

                        git config user.name "jenkins"
                        git config user.email "jenkins@localhost"

                        git add environments/dev/

                        git commit \
                          -m "ci: promote ${IMAGE_TAG} to dev"

                        git push origin "$GITOPS_BRANCH"
                    '''
                }
            }
        }

        stage('Create GitHub PR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-gitops',
                        usernameVariable: 'GITHUB_USER',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e

                        curl -sS \
                          -X POST \
                          -H "Authorization: Bearer $GITHUB_TOKEN" \
                          -H "Accept: application/vnd.github+json" \
                          https://api.github.com/repos/paycenonoli/dev-to-prod-microservices-gitops/pulls \
                          -d "{
                            \\"title\\": \\"ci: promote ${IMAGE_TAG} to dev\\",
                            \\"head\\": \\"${GITOPS_BRANCH}\\",
                            \\"base\\": \\"main\\",
                            \\"body\\": \\"Automated promotion created by Jenkins.\\\\n\\\\nImage tag: ${IMAGE_TAG}\\"
                          }"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Build and GitOps promotion completed for ${IMAGE_TAG}"
        }

        failure {
            echo "Pipeline failed. Check the stage logs."
        }
    }
}
