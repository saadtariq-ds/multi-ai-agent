# AWS Deployment Guide

## Step 1. AWS Setup, Build and Push to AWS
Follow these steps to set up AWS integration with Jenkins for building and pushing Docker images to Amazon ECR.

### 1. Install Required Jenkins Plugins
1. Go to Manage Jenkins -> Manage Plugins.
2. Search for and install the following plugins:
- AWS SDK (All)
- AWS Credentials
3. Restart jenkins-dind after the plugins installation:
```bash
docker restart jenkins-dind
```

### 2. Create an IAM User for AWS Access
1. Go to the AWS Console → IAM → Users → Add User.
2. Add the necessary policies:
- Attach the policy: AmazonEC2ContainerRegistryFullAccess
3. Once the user is created, select the user and click on Create Access Key.
4. Copy the Access Key ID and Secret Access Key.

### Add AWS Credentials to Jenkins
1. Go to Jenkins Dashboard → Manage Jenkins → Manage Credentials → Global.
2. Add a new AWS Credentials:
- ID: aws-credentials
- Access Key ID: Paste the Access Key ID from AWS.
- Secret Access Key: Paste the Secret Access Key from AWS.
3. Save the credentials.

### 4. Install AWS CLI on Jenkins Container
1. Open a new terminal and run the following commands inside your jenkins-dind container:
```bash
docker exec -u root -it jenkins-dind bash
```

2. Update the package list and install required tools:
```bash
apt update
apt install -y unzip curl
```

3. Download and install AWS CLI:
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
```

4. Verify the installation:
```bash
aws --version
```

5. Exit the container:
```bash
exit
```

### 5. Create an ECR Repository in AWS
1. Go to AWS Console → ECR (Elastic Container Registry) → Create Repository.
2. Name the repository (e.g., my-repository).
3. Set up the repository as required and save the repository URL for later use.

### 6. Add Build and Push Docker Image to ECR Stage in Jenkinsfile
Already done if clone just change according to your repo name..

### 7. Push the Changes to GitHub
Push the updated Jenkinsfile to your GitHub repository to trigger the pipeline.

### 8. Run the Jenkins Pipeline
1. Go to the Jenkins Dashboard.
2. Click on Build Now for your pipeline.
3. The pipeline will execute, building the Docker image and pushing it to Amazon ECR.

## Step 2 : Final Deployment Stage with AWS ECS and Jenkins
Follow these steps to deploy your app to AWS ECS Fargate using Jenkins and automate the deployment process.

### 1. Create ECS Cluster and Task Definition
1. Create ECS Cluster:
- Go to ECS → Clusters → Create Cluster.
- Give your cluster a name and select Fargate.
- Click Create to create the cluster.

2. Create ECS Task Definition:
- Go to ECS → Task Definitions → Create new Task Definition.
- Select Fargate as the launch type.
- Give the task definition a name (e.g., `llmops-task`).

3. Container Configuration:
- Under Container details, give the container a name and use the ECR URI (the Docker image URL from your ECR repository).
- In Port Mapping, use the following configuration:
    - Port: 8501
    - Protocol: TCP
    - None: leave it as default.

4. Create Task Definition:
    - Click Create to create the task definition.

### 2. Create ECS Service
1. Go to ECS → Clusters → Your cluster.
2. Click Create Service.
3. Select your Task Definition (`llmops-task`).
4. Select Fargate for launch type (this should be the default option).
5. Give the service a name (e.g., llmops-service).
6. Under Networking, select:
    - Public IP: Allow a public IP.
7. Click Create and wait for a few minutes for the service to be deployed.

### 3. Configure Security Group for Public Access
1. Search for Security Groups in the AWS console.
2. Select the Default security group.
3. Go to the Inbound Rules and click Edit inbound rules.
4. Add a new Custom TCP rule with the following details:
    - Port range: 8501
    - Source: 0.0.0.0/0 (allow access from all IPs).
5. Save the rules.

### 4. Check the Deployment
1. After the ECS service has been deployed (this may take a few minutes), go to your ECS cluster.
2. Open the Tasks tab and copy the Public IP of your task.
3. Open a browser and visit: `http://<PublicIP>:8501.`
    - You should see your app running.

### 5. Automate Deployment with Jenkins
1. Add ECS Full Access Policy to the IAM user:
    - Go to IAM → Users → Your IAM User → Attach Policies.
    - Attach the AmazonECS_FullAccess policy to the IAM user.
2. Update Jenkinsfile for ECS Deployment:
    - Add the deployment stage to your Jenkinsfile. This will automate the deployment of your Docker container to AWS ECS.
3. Push the updated code to GitHub.

### 6. Build Jenkins Pipeline
1. Go to Jenkins Dashboard.
2. Click on Build Now to trigger the Jenkins pipeline.
3. The pipeline will run, and you will see the task in the ECS Service go to In Progress.
4. Once the pipeline is complete, your service will be Running again.

### 7. Verify the Deployment
1. Open the ECS cluster and check the Task status.
2. After the task is successfully deployed, visit your app at `http://<PublicIP>:8501` to ensure it is working.