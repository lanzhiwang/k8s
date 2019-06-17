## sonarqube

```bash

wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-7.7.zip
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-7.7.zip

docker pull sonarqube

docker run -d --name sonarqube -p 9000:9000 sonarqube


docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=root \
    -e sonar.jdbc.password=rootpassword \
    -e "sonar.jdbc.url=jdbc:mysql://10.0.2.15/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true" \
    sonarqube
    

mkdir conf data logs extensions
chmod -R 777 logs

docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=root \
    -e sonar.jdbc.password=rootpassword \
    -e "sonar.jdbc.url=jdbc:mysql://10.0.2.15/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true" \
    -v /root/work/SonarQube/conf:/opt/sonarqube/conf \
    -v /root/work/SonarQube/data:/opt/sonarqube/data \
    -v /root/work/SonarQube/logs:/opt/sonarqube/logs \
    -v /root/work/SonarQube/extensions:/opt/sonarqube/extensions \
    sonarqube









```

