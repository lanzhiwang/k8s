## sonarqube

```bash

wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-7.7.zip
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-7.7.zip

docker pull sonarqube

docker run -d --name sonarqube -p 9000:9000 sonarqube

docker run -d --name sonarqube -p 9000:9000 -e sonar.jdbc.username=sonar -e sonar.jdbc.password=sonar -e sonar.jdbc.url=jdbc:postgresql://localhost/sonar sonarqube 


docker run -d --name sonarqube -p 9000:9000 -e sonar.jdbc.username=root -e sonar.jdbc.password=rootpassword -e sonar.jdbc.url=jdbc:mysql://localhost/sonar sonarqube 


```