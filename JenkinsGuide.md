# 🚀 Deployment Guide

## ✅ Progress Checklist
The following essential setup steps have been completed:

### ✅ WSL Setup Full
- Ubuntu installed via Microsoft Store
- Docker Engine installed inside Ubuntu WSL
- Project runs successfully in WSL

### ✅ Dockerfile Created
- Dockerfile written for the project
- Environment variables setup will be handled later
- Do not include `.env` in the Dockerfile for now

### ✅ GitHub Setup Completed
- Project is pushed to GitHub
- `.gitignore` is properly configured and includes `.env`

## 🚀 Deployment to AWS FARGATE
Follow the steps below to deploy the application.

Make sure you run commands inside a WSL terminal in VS Code

### 🛠️ Step 1 : Jenkins Setup for CI/CD (via Docker)

Follow the steps below to set up Jenkins inside a Docker container and configure it for the project:

#### 1. Create custom_jenkins Folder (already done if cloned)

#### 2. Create Dockerfile Inside custom_jenkins (already done if cloned)

#### 3. Build Docker Image
Build the Docker image for Jenkins:
```bash
docker build -t jenkins-dind .
```

#### 4. Run Jenkins Container
Run the Jenkins container with the following command:
```bash
docker run -d --name jenkins-dind \
  --privileged \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind
```
After successful execution, you'll receive a long alphanumeric string.

#### 5. Verify the Running Container
To verify if the Jenkins container is running:
```bash
docker ps
```

#### 6. Get Jenkins Logs and Password
To retrieve Jenkins logs and get the initial admin password:
```bash
docker logs jenkins-dind
```
You should see a password in the output. Copy that password.

#### 7. Find WSL IP Address
Run the following command to get the IP address of your WSL environment:
```bash
ip addr show eth0 | grep inet
```

#### 8. Access Jenkins
Now, access Jenkins on your browser using the following URL (replace `172.23.129.123` with the actual WSL IP address you retrieved):
```bash
http://172.23.129.123:8080
```

#### 9. Install Python and Set Up Jenkins
Return to the terminal and run the following commands to install Python inside the Jenkins container:
```bash
docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3
python3 --version
ln -s /usr/bin/python3 /usr/bin/python
python --version
apt install -y python3-pip
exit
```

#### 10. Restart Jenkins Container
Restart the Jenkins container to apply changes:
```bash
docker restart jenkins-dind
```

#### 11. Sign in to Jenkins
Go to the Jenkins dashboard and sign in using the initial password you retrieved earlier.

### 🔗 Step 2 : GitHub Integration with Jenkins
Follow the steps below to integrate GitHub with Jenkins for automated pipeline execution:

#### 1. Generate a GitHub Personal Access Token
- Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Click Generate new token (classic)
- Provide:
  - A name (e.g., `Jenkins Integration`)
  - Select scopes:
    - `repo` (for full control of private repositories)
    - `admin:repo_hook` (for webhook integration)
- Generate the token and save it securely (you won’t see it again!).

#### 2. Add GitHub Token to Jenkins Credentials
1. Go to Jenkins Dashboard → Manage Jenkins → Credentials → (Global) → Add Credentials
2. Fill in the following:
  - Username: Your GitHub username
  - Password: Paste the GitHub token you just generated
  - ID: `github-token`
  - Description: `GitHub Token for Jenkins`
3. Click Save.

#### 3. Create a New Pipeline Job in Jenkins
1. Go back to Jenkins Dashboard
2. Click New Item → Select Pipeline
3. Enter a name (e.g., multi-ai-agent)
4. Click OK → Scroll down, configure minimal settings → Click Save
⚠️ You will have to configure pipeline details again in the next step

#### 4. Generate Checkout Script from Jenkins UI
1. In the left sidebar of your pipeline project, click Pipeline Syntax
2. From the dropdown, select `checkout: General SCM`
3. Fill in:
  - SCM: Git
  - Repository URL: Your GitHub repo URL
  - Credentials: Select the `github-token` you just created
4. Click Generate Pipeline Script
5. Copy the generated Groovy script (e.g., `checkout([$class: 'GitSCM', ...])`)

#### 5. Create a Jenkinsfile in Your Repo
1. Open your project in VS Code
2. Create a file named Jenkinsfile in the root directory

#### 6. Push the Jenkinsfile to GitHub
```bash
git add Jenkinsfile
git commit -m "your commit name"
git push origin main
```

#### 7. Trigger the Pipeline
1. Go to Jenkins Dashboard → Select your pipeline → Click Build Now

🎉 You’ll see a SUCCESS message if everything works!
✅ Your GitHub repository has been cloned inside Jenkins’ workspace!

### 📊 Step 3 : SonarQube Integration with Jenkins
Follow these steps to integrate SonarQube with Jenkins for code quality analysis.

#### 1. Download and Run SonarQube Docker Container
1. Go to DockerHub and search for SonarQube. Scroll down to find the commands.
2. Run the following commands in a new WSL terminal to configure the system:
```bash
sysctl -w vm.max_map_count=524288
sysctl -w fs.file-max=131072
ulimit -n 131072
ulimit -u 8192
```
3. Run the SonarQube container with the appropriate settings. Make sure to change the container name to sonarqube-dind and remove the dollar sign ($) from the command. You will find the command in the Demo section of DockerHub.
```bash
docker run -d --name sonarqube-dind \
  -p 9000:9000 \
  -e SONARQUBE_JDBC_URL=jdbc:postgresql://localhost/sonar \
  sonarqube
```
4. Check if the container is running:
```bash
docker ps
```
5. Access SonarQube on http://<WSL_IP>:9000 (replace <WSL_IP> with your WSL IP address). Log in using the default credentials:
- Username: `admin`
- Password: `admin`

#### 2. Install Jenkins Plugins for SonarQube
1. Go to Jenkins Dashboard -> Manage Jenkins -> Manage Plugins.
2. Install the following plugins:
- SonarScanner
- SonarQualityGates
3. Restart the Jenkins container:
```bash
docker restart jenkins-dind
```

#### 3. Set Up SonarQube in Jenkins
1. Go to SonarQube -> Create a Local Project.
- Enter a name for the project (e.g., `LLMOPS`).
- Set the Main Branch.
- Save the project.

2. Go to SonarQube -> My Account (top-right) -> Security -> Generate New Token.
- Provide a name (e.g., `global-analysis-token`) and generate the token.
- Copy the generated token.

3. Go to Jenkins Dashboard -> Manage Jenkins -> Credentials -> Global.

4. Add a new Secret Text credential:
- ID: `sonarqube-token`
- Secret: Paste the token from SonarQube.
- Click OK to save.

#### 4. Configure SonarQube in Jenkins
1. Go to Manage Jenkins -> System Configuration.

2. Scroll down to SonarQube Servers and click Add SonarQube.
- Name: SonarQube (or any name you prefer)
- URL: http://<WSL_IP>:9000 (replace <WSL_IP> with your actual IP address)
- Select SonarQube Token from the credentials dropdown.
- Apply and save.

3. Go to Manage Jenkins -> Tools and look for SonarQube Scanner.
- Select SonarQube Scanner and configure it.
- Tick the option Install Automatically.

#### 5. Create a Stage in Jenkinsfile for SonarQube
1. Open the Jenkinsfile in VS Code and add the Sonarqube stage ( already provided in the code )
2. Push the changes to your GitHub repository.

#### 6. Create a Docker Network for Jenkins and SonarQube
1. Run the following command to create a new Docker network:
```bash
docker network create dind-network
```

2. Connect both containers to the new network:
```bash
docker network connect dind-network jenkins-dind
docker network connect dind-network sonarqube-dind
```

3. Update the Jenkinsfile to use the container name instead of the IP address: (already done in code )
```bash
-Dsonar.host.url=http://sonarqube-dind:9000
```

#### 8. Final Pipeline Run
1. Trigger the Jenkins Pipeline .
2. The build should now be successful, and the code will be analyzed by SonarQube.

#### 9. View Results in SonarQube
Go to SonarQube and see the code quality report generated for your project.
