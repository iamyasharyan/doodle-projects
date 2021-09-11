pipeline {
    agent any
    
    stages{
        stage('Git Download to WS'){
            steps{
                git branch: 'docker-dev', credentialsId: 'xongl_git_cred_token_pair', url: 'https://github.com/Samarjayee/xongl-panel'
            }
        }
        
        stage('Docket Build Image'){
            steps{
                sh"""docker build -t xongl/dev ."""
            }
        }
        
        stage('Docket Stop Exsiting Container'){
            steps{
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh"""docker stop xonglqa"""
                    sh"""docker rm xonglqa"""
                }
            }
        }
        
        stage('Docket Run Container'){
            steps{
                sh"""docker run -dp 80:8080 --name xonglqa xongl/dev"""
            }
        }
    }
    
    post {
        success{echo "Docket Run Sucess"}
        failure{echo "Docket Run Failure"}
    }
}
