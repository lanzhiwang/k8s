## sonarqube

https://www.sonarqube.org/

https://docs.sonarqube.org/latest/

https://hub.docker.com/_/sonarqube

https://github.com/SonarSource/docker-sonarqube>


```bash
# sonarqube 安装文件下载
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-7.7.zip

# 基础使用
docker pull sonarqube
docker run -d --name sonarqube -p 9000:9000 sonarqube

# 使用环境变量配置数据库
docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=root \
    -e sonar.jdbc.password=rootpass \
    -e "sonar.jdbc.url=jdbc:mysql://172.17.0.6/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true" \
    sonarqube
    

# 挂载相关目录 
mkdir conf data logs extensions
chmod -R 777 conf data logs extensions

docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=root \
    -e sonar.jdbc.password=rootpass \
    -e "sonar.jdbc.url=jdbc:mysql://172.17.0.6/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true" \
    -v /root/work/SonarQube/conf:/opt/sonarqube/conf \
    -v /root/work/SonarQube/data:/opt/sonarqube/data \
    -v /root/work/SonarQube/logs:/opt/sonarqube/logs \
    -v /root/work/SonarQube/extensions:/opt/sonarqube/extensions \
    sonarqube

09:16:07.195 [main] WARN org.sonar.application.config.AppSettingsLoaderImpl - Configuration file not found: /opt/sonarqube/conf/sonar.properties

09:16:07.487 [main] WARN org.sonar.application.config.JdbcSettings - JDBC URL is recommended to have the property 'useConfigs=maxPerformance'

java.nio.file.AccessDeniedException: /opt/sonarqube/data/es6

com.mysql.jdbc.exceptions.jdbc4.MySQLSyntaxErrorException: Unknown database 'sonar'

错误分析：
1、config 目录中没有 sonar.properties 文件，可以在运行的容器中拷贝
2、在 sonar.jdbc.url 环境变量中增加 useConfigs=maxPerformance 参数
3、所有目录都要最大权限
4、要提前创建 sonar 数据库 create database sonar;

docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=root \
    -e sonar.jdbc.password=rootpass \
    -e "sonar.jdbc.url=jdbc:mysql://172.17.0.6/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance" \
    -v /root/work/SonarQube/conf:/opt/sonarqube/conf \
    -v /root/work/SonarQube/data:/opt/sonarqube/data \
    -v /root/work/SonarQube/logs:/opt/sonarqube/logs \
    -v /root/work/SonarQube/extensions:/opt/sonarqube/extensions \
    sonarqube


# 使用下面的配置文件启动容器，不使用环境变量指定数据库
[root@localhost SonarQube]# cat sonar.properties 
# Property values can:
# - reference an environment variable, for example sonar.jdbc.url= ${env:SONAR_JDBC_URL}
# - be encrypted. See https://redirect.sonarsource.com/doc/settings-encryption.html

#--------------------------------------------------------------------------------------------------
# DATABASE
#
# IMPORTANT:
# - The embedded H2 database is used by default. It is recommended for tests but not for
#   production use. Supported databases are MySQL, Oracle, PostgreSQL and Microsoft SQLServer.
# - Changes to database connection URL (sonar.jdbc.url) can affect SonarSource licensed products.

# User credentials.
# Permissions to create tables, indices and triggers must be granted to JDBC user.
# The schema must be created first.
sonar.jdbc.username=root
sonar.jdbc.password=rootpass

#----- Embedded Database (default)
# H2 embedded database server listening port, defaults to 9092
#sonar.embeddedDatabase.port=9092

#----- DEPRECATED 
#----- MySQL >=5.6 && <8.0
# Support of MySQL is dropped in Data Center Editions and deprecated in all other editions
# Only InnoDB storage engine is supported (not myISAM).
# Only the bundled driver is supported. It can not be changed.
sonar.jdbc.url=jdbc:mysql://172.17.0.6:3306/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance&useSSL=false

#----- Oracle 11g/12c
# The Oracle JDBC driver must be copied into the directory extensions/jdbc-driver/oracle/.
# Only the thin client is supported, and only the versions 11.2.x or 12.2.x must be used. See
# https://jira.sonarsource.com/browse/SONAR-9758 for more details.
# If you need to set the schema, please refer to http://jira.sonarsource.com/browse/SONAR-5000
#sonar.jdbc.url=jdbc:oracle:thin:@localhost:1521/XE


#----- PostgreSQL 9.3 or greater
# By default the schema named "public" is used. It can be overridden with the parameter "currentSchema".
#sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube?currentSchema=my_schema


#----- Microsoft SQLServer 2014/2016/2017 and SQL Azure
# A database named sonar must exist and its collation must be case-sensitive (CS) and accent-sensitive (AS)
# Use the following connection string if you want to use integrated security with Microsoft Sql Server
# Do not set sonar.jdbc.username or sonar.jdbc.password property if you are using Integrated Security
# For Integrated Security to work, you have to download the Microsoft SQL JDBC driver package from
# https://www.microsoft.com/en-us/download/details.aspx?id=55539
# and copy sqljdbc_auth.dll to your path. You have to copy the 32 bit or 64 bit version of the dll
# depending upon the architecture of your server machine.
#sonar.jdbc.url=jdbc:sqlserver://localhost;databaseName=sonar;integratedSecurity=true

# Use the following connection string if you want to use SQL Auth while connecting to MS Sql Server.
# Set the sonar.jdbc.username and sonar.jdbc.password appropriately.
#sonar.jdbc.url=jdbc:sqlserver://localhost;databaseName=sonar


#----- Connection pool settings
# The maximum number of active connections that can be allocated
# at the same time, or negative for no limit.
# The recommended value is 1.2 * max sizes of HTTP pools. For example if HTTP ports are
# enabled with default sizes (50, see property sonar.web.http.maxThreads)
# then sonar.jdbc.maxActive should be 1.2 * 50 = 60.
#sonar.jdbc.maxActive=60

# The maximum number of connections that can remain idle in the
# pool, without extra ones being released, or negative for no limit.
#sonar.jdbc.maxIdle=5

# The minimum number of connections that can remain idle in the pool,
# without extra ones being created, or zero to create none.
#sonar.jdbc.minIdle=2

# The maximum number of milliseconds that the pool will wait (when there
# are no available connections) for a connection to be returned before
# throwing an exception, or <= 0 to wait indefinitely.
#sonar.jdbc.maxWait=5000

#sonar.jdbc.minEvictableIdleTimeMillis=600000
#sonar.jdbc.timeBetweenEvictionRunsMillis=30000



#--------------------------------------------------------------------------------------------------
# WEB SERVER
# Web server is executed in a dedicated Java process. By default heap size is 512Mb.
# Use the following property to customize JVM options.
#    Recommendations:
#
#    The HotSpot Server VM is recommended. The property -server should be added if server mode
#    is not enabled by default on your environment:
#    http://docs.oracle.com/javase/8/docs/technotes/guides/vm/server-class.html
#
#    Startup can be long if entropy source is short of entropy. Adding
#    -Djava.security.egd=file:/dev/./urandom is an option to resolve the problem.
#    See https://wiki.apache.org/tomcat/HowTo/FasterStartUp#Entropy_Source
#
#sonar.web.javaOpts=-Xmx512m -Xms128m -XX:+HeapDumpOnOutOfMemoryError

# Same as previous property, but allows to not repeat all other settings like -Xmx
#sonar.web.javaAdditionalOpts=

# Binding IP address. For servers with more than one IP address, this property specifies which
# address will be used for listening on the specified ports.
# By default, ports will be used on all IP addresses associated with the server.
#sonar.web.host=0.0.0.0

# Web context. When set, it must start with forward slash (for example /sonarqube).
# The default value is root context (empty value).
#sonar.web.context=
# TCP port for incoming HTTP connections. Default value is 9000.
sonar.web.port=9008


# The maximum number of connections that the server will accept and process at any given time.
# When this number has been reached, the server will not accept any more connections until
# the number of connections falls below this value. The operating system may still accept connections
# based on the sonar.web.connections.acceptCount property. The default value is 50.
#sonar.web.http.maxThreads=50

# The minimum number of threads always kept running. The default value is 5.
#sonar.web.http.minThreads=5

# The maximum queue length for incoming connection requests when all possible request processing
# threads are in use. Any requests received when the queue is full will be refused.
# The default value is 25.
#sonar.web.http.acceptCount=25

# By default users are logged out and sessions closed when server is restarted.
# If you prefer keeping user sessions open, a secret should be defined. Value is
# HS256 key encoded with base64. It must be unique for each installation of SonarQube.
# Example of command-line:
# echo -n "type_what_you_want" | openssl dgst -sha256 -hmac "key" -binary | base64
#sonar.auth.jwtBase64Hs256Secret=

# The inactivity timeout duration of user sessions, in minutes. After the configured
# period of time, the user is logged out.
# The default value is set to 3 days (4320 minutes)
# and cannot be greater than 3 months. Value must be strictly positive.
#sonar.web.sessionTimeoutInMinutes=4320

# A passcode can be defined to access some web services from monitoring
# tools without having to use the credentials of a system administrator.
# Check the Web API documentation to know which web services are supporting this authentication mode.
# The passcode should be provided in HTTP requests with the header "X-Sonar-Passcode".
# By default feature is disabled.
#sonar.web.systemPasscode=


#--------------------------------------------------------------------------------------------------
# SSO AUTHENTICATION

# Enable authentication using HTTP headers
#sonar.web.sso.enable=false

# Name of the header to get the user login.
# Only alphanumeric, '.' and '@' characters are allowed
#sonar.web.sso.loginHeader=X-Forwarded-Login

# Name of the header to get the user name
#sonar.web.sso.nameHeader=X-Forwarded-Name

# Name of the header to get the user email (optional)
#sonar.web.sso.emailHeader=X-Forwarded-Email

# Name of the header to get the list of user groups, separated by comma (optional).
# If the sonar.sso.groupsHeader is set, the user will belong to those groups if groups exist in SonarQube.
# If none of the provided groups exists in SonarQube, the user will only belong to the default group.
# Note that the default group will always be set.
#sonar.web.sso.groupsHeader=X-Forwarded-Groups

# Interval used to know when to refresh name, email and groups.
# During this interval, if for instance the name of the user is changed in the header, it will only be updated after X minutes.
#sonar.web.sso.refreshIntervalInMinutes=5

#--------------------------------------------------------------------------------------------------
# LDAP CONFIGURATION

# Enable the LDAP feature
# sonar.security.realm=LDAP

# Set to true when connecting to a LDAP server using a case-insensitive setup.
# sonar.authenticator.downcase=true

# URL of the LDAP server. Note that if you are using ldaps, then you should install the server certificate into the Java truststore.
# ldap.url=ldap://localhost:10389

# Bind DN is the username of an LDAP user to connect (or bind) with. Leave this blank for anonymous access to the LDAP directory (optional)
# ldap.bindDn=cn=sonar,ou=users,o=mycompany

# Bind Password is the password of the user to connect with. Leave this blank for anonymous access to the LDAP directory (optional)
# ldap.bindPassword=secret

# Possible values: simple | CRAM-MD5 | DIGEST-MD5 | GSSAPI See http://java.sun.com/products/jndi/tutorial/ldap/security/auth.html (default: simple)
# ldap.authentication=simple

# See :
#   * http://java.sun.com/products/jndi/tutorial/ldap/security/digest.html
#   * http://java.sun.com/products/jndi/tutorial/ldap/security/crammd5.html
# (optional)
# ldap.realm=example.org

# Context factory class (optional)
# ldap.contextFactoryClass=com.sun.jndi.ldap.LdapCtxFactory

# Enable usage of StartTLS (default : false)
# ldap.StartTLS=true

# Follow or not referrals. See http://docs.oracle.com/javase/jndi/tutorial/ldap/referral/jndi.html (default: true)
# ldap.followReferrals=false

# USER MAPPING

# Distinguished Name (DN) of the root node in LDAP from which to search for users (mandatory)
# ldap.user.baseDn=cn=users,dc=example,dc=org

# LDAP user request. (default: (&(objectClass=inetOrgPerson)(uid={login})) )
# ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))

# Attribute in LDAP defining the user’s real name. (default: cn)
# ldap.user.realNameAttribute=name

# Attribute in LDAP defining the user’s email. (default: mail)
# ldap.user.emailAttribute=email

# GROUP MAPPING

# Distinguished Name (DN) of the root node in LDAP from which to search for groups. (optional, default: empty)
# ldap.group.baseDn=cn=groups,dc=example,dc=org

# LDAP group request (default: (&(objectClass=groupOfUniqueNames)(uniqueMember={dn})) )
# ldap.group.request=(&(objectClass=group)(member={dn}))

# Property used to specifiy the attribute to be used for returning the list of user groups in the compatibility mode. (default: cn)
# ldap.group.idAttribute=sAMAccountName

#--------------------------------------------------------------------------------------------------
# COMPUTE ENGINE
# The Compute Engine is responsible for processing background tasks.
# Compute Engine is executed in a dedicated Java process. Default heap size is 512Mb.
# Use the following property to customize JVM options.
#    Recommendations:
#
#    The HotSpot Server VM is recommended. The property -server should be added if server mode
#    is not enabled by default on your environment:
#    http://docs.oracle.com/javase/8/docs/technotes/guides/vm/server-class.html
#
#sonar.ce.javaOpts=-Xmx512m -Xms128m -XX:+HeapDumpOnOutOfMemoryError

# Same as previous property, but allows to not repeat all other settings like -Xmx
#sonar.ce.javaAdditionalOpts=


#--------------------------------------------------------------------------------------------------
# ELASTICSEARCH
# Elasticsearch is used to facilitate fast and accurate information retrieval.
# It is executed in a dedicated Java process. Default heap size is 512Mb.
#
# --------------------------------------------------
# Word of caution for Linux users on 64bits systems
# --------------------------------------------------
# Please ensure Virtual Memory on your system is correctly configured for Elasticsearch to run properly
# (see https://www.elastic.co/guide/en/elasticsearch/reference/5.5/vm-max-map-count.html for details).
#
# When SonarQube runs standalone, a warning such as the following may appear in logs/es.log:
#      "max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]"
# When SonarQube runs as a cluster, however, Elasticsearch will refuse to start.
#

# JVM options of Elasticsearch process
#sonar.search.javaOpts=-Xms512m -Xmx512m -XX:+HeapDumpOnOutOfMemoryError

# Same as previous property, but allows to not repeat all other settings like -Xmx
#sonar.search.javaAdditionalOpts=

# Elasticsearch port. Default is 9001. Use 0 to get a free port.
# As a security precaution, should be blocked by a firewall and not exposed to the Internet.
#sonar.search.port=9001

# Elasticsearch host. The search server will bind this address and the search client will connect to it.
# Default is loopback address.
# As a security precaution, should NOT be set to a publicly available address.
#sonar.search.host=


#--------------------------------------------------------------------------------------------------
# UPDATE CENTER

# Update Center requires an internet connection to request https://update.sonarsource.org
# It is enabled by default.
#sonar.updatecenter.activate=true

# HTTP proxy (default none)
#http.proxyHost=
#http.proxyPort=
# HTTPS proxy (defaults are values of http.proxyHost and http.proxyPort)
#https.proxyHost=
#https.proxyPort=

# NT domain name if NTLM proxy is used
#http.auth.ntlm.domain=

# SOCKS proxy (default none)
#socksProxyHost=
#socksProxyPort=

# Proxy authentication (used for HTTP, HTTPS and SOCKS proxies)
#http.proxyUser=
#http.proxyPassword=


#--------------------------------------------------------------------------------------------------
# LOGGING

# SonarQube produces logs in 4 logs files located in the same directory (see property sonar.path.logs below),
# one per process:
#   Main process (aka. App) logs in sonar.log
#   Web Server (aka. Web) logs in web.log
#   Compute Engine (aka. CE) logs in ce.log
#   Elasticsearch (aka. ES) logs in es.log
#
# All 4 files follow the same rolling policy (see sonar.log.rollingPolicy and sonar.log.maxFiles) but it applies
# individually (eg. if sonar.log.maxFiles=4, there can be at most 4 of each files, ie. 16 files in total).
#
# All 4 files have logs in the same format:
#           1           2    3           4                       5                                                   6
# |-----------------| |---| |-|--------------------||------------------------------| |------------------------------------------------------------------------------------------------------------------------------|
# 2016.11.16 16:47:00 INFO  ce[AVht0dNXFcyiYejytc3m][o.s.s.c.t.CeWorkerCallableImpl] Executed task | project=org.sonarqube:example-java-maven | type=REPORT | id=AVht0dNXFcyiYejytc3m | submitter=admin | time=1699ms
#
# 1: timestamp. Format is YYYY.MM.DD HH:MM:SS
#    YYYY: year on 4 digits
#    MM: month on 2 digits
#    DD: day on 2 digits
#    HH: hour of day on 2 digits in 24 hours format
#    MM: minutes on 2 digits
#    SS: seconds on 2 digits
# 2: log level.
#    Possible values (in order of descending criticality): ERROR, WARN, INFO, DEBUG and TRACE
# 3: process identifier. Possible values: app (main), web (Web Server), ce (Compute Engine) and es (Elasticsearch)
# 4: SQ thread identifier. Can be empty.
#    In the Web Server, if present, it will be the HTTP request ID.
#    In the Compute Engine, if present, it will be the task ID.
# 5: logger name. Usually a class canonical name.
#    Package names are truncated to keep the whole field to 20 characters max
# 6: log payload. Content of this field does not follow any specific format, can vary in length and include line returns.
#    Some logs, however, will follow the convention to provide data in payload in the format " | key=value"
#    Especially, log of profiled pieces of code will end with " | time=XXXXms".

# Global level of logs (applies to all 4 processes).
# Supported values are INFO (default), DEBUG and TRACE
#sonar.log.level=INFO

# Level of logs of each process can be controlled individually with their respective properties.
# When specified, they overwrite the level defined at global level.
# Supported values are INFO, DEBUG and TRACE
#sonar.log.level.app=INFO
#sonar.log.level.web=INFO
#sonar.log.level.ce=INFO
#sonar.log.level.es=INFO

# Path to log files. Can be absolute or relative to installation directory.
# Default is <installation home>/logs
#sonar.path.logs=logs

# Rolling policy of log files
#    - based on time if value starts with "time:", for example by day ("time:yyyy-MM-dd")
#      or by month ("time:yyyy-MM")
#    - based on size if value starts with "size:", for example "size:10MB"
#    - disabled if value is "none".  That needs logs to be managed by an external system like logrotate.
#sonar.log.rollingPolicy=time:yyyy-MM-dd

# Maximum number of files to keep if a rolling policy is enabled.
#    - maximum value is 20 on size rolling policy
#    - unlimited on time rolling policy. Set to zero to disable old file purging.
#sonar.log.maxFiles=7

# Access log is the list of all the HTTP requests received by server. If enabled, it is stored
# in the file {sonar.path.logs}/access.log. This file follows the same rolling policy as other log file
# (see sonar.log.rollingPolicy and sonar.log.maxFiles).
#sonar.web.accessLogs.enable=true

# Format of access log. It is ignored if sonar.web.accessLogs.enable=false. Possible values are:
#    - "common" is the Common Log Format, shortcut to: %h %l %u %user %date "%r" %s %b
#    - "combined" is another format widely recognized, shortcut to: %h %l %u [%t] "%r" %s %b "%i{Referer}" "%i{User-Agent}"
#    - else a custom pattern. See http://logback.qos.ch/manual/layouts.html#AccessPatternLayout.
# The login of authenticated user is not implemented with "%u" but with "%reqAttribute{LOGIN}" (since version 6.1).
# The value displayed for anonymous users is "-".
# The SonarQube's HTTP request ID can be added to the pattern with "%reqAttribute{ID}" (since version 6.2).
# If SonarQube is behind a reverse proxy, then the following value allows to display the correct remote IP address:
#sonar.web.accessLogs.pattern=%i{X-Forwarded-For} %l %u [%t] "%r" %s %b "%i{Referer}" "%i{User-Agent}" "%reqAttribute{ID}"
# Default value (which was "combined" before version 6.2) is equivalent to "combined + SQ HTTP request ID":
#sonar.web.accessLogs.pattern=%h %l %u [%t] "%r" %s %b "%i{Referer}" "%i{User-Agent}" "%reqAttribute{ID}"


#--------------------------------------------------------------------------------------------------
# OTHERS

# Delay in seconds between processing of notification queue. Default is 60 seconds.
#sonar.notifications.delay=60

# Paths to persistent data files (embedded database and search index) and temporary files.
# Can be absolute or relative to installation directory.
# Defaults are respectively <installation home>/data and <installation home>/temp
#sonar.path.data=data
#sonar.path.temp=temp

# Telemetry - Share anonymous SonarQube statistics
# By sharing anonymous SonarQube statistics, you help us understand how SonarQube is used so we can improve the product to work even better for you.
# We don't collect source code or IP addresses. And we don't share the data with anyone else.
# To see an example of the data shared: login as a global administrator, call the WS api/system/info and check the Statistics field.
#sonar.telemetry.enable=true


#--------------------------------------------------------------------------------------------------
# DEVELOPMENT - only for developers
# The following properties MUST NOT be used in production environments.

# Elasticsearch HTTP connector
#sonar.search.httpPort=-1
[root@localhost SonarQube]# 

docker run -d --name sonarqube \
    -p 9000:9000 \
    -v /root/work/SonarQube/conf:/opt/sonarqube/conf \
    -v /root/work/SonarQube/data:/opt/sonarqube/data \
    -v /root/work/SonarQube/logs:/opt/sonarqube/logs \
    -v /root/work/SonarQube/extensions:/opt/sonarqube/extensions \
    sonarqube


错误分析：
配置文件没有起作用

unzip sonarqube-7.7.zip

mv sonarqube-7.7 sonarqube

groupadd -r sonarqube
useradd -r -g sonarqube sonarqube
chown -R sonarqube:sonarqube sonarqube

rm -rf sonarqube/bin/*

chmod -R 777 sonarqube

[root@localhost SonarQube]# vim sonarqube/bin/run.sh
[root@localhost SonarQube]# cat sonarqube/bin/run.sh
#!/usr/bin/env bash

set -e

if [ "${1:0:1}" != '-' ]; then
  exec "$@"
fi

# Parse Docker env vars to customize SonarQube
#
# e.g. Setting the env var sonar.jdbc.username=foo
#
# will cause SonarQube to be invoked with -Dsonar.jdbc.username=foo

declare -a sq_opts

while IFS='=' read -r envvar_key envvar_value
do
    if [[ "$envvar_key" =~ sonar.* ]] || [[ "$envvar_key" =~ ldap.* ]]; then
        sq_opts+=("-D${envvar_key}=${envvar_value}")
    fi
done < <(env)

exec java -jar lib/sonar-application-$SONAR_VERSION.jar \
  -Dsonar.log.console=true \
  -Dsonar.jdbc.username="$SONARQUBE_JDBC_USERNAME" \
  -Dsonar.jdbc.password="$SONARQUBE_JDBC_PASSWORD" \
  -Dsonar.jdbc.url="$SONARQUBE_JDBC_URL" \
  -Dsonar.web.javaAdditionalOpts="$SONARQUBE_WEB_JVM_OPTS -Djava.security.egd=file:/dev/./urandom" \
  "${sq_opts[@]}" \
  "$@"
You have new mail in /var/spool/mail/root
[root@localhost SonarQube]# chmod +x sonarqube/bin/run.sh
[root@localhost SonarQube]# ll sonarqube/bin/run.sh
-rwxr-xr-x 1 root root 832 Jun 18 08:07 sonarqube/bin/run.sh
[root@localhost SonarQube]# 

# 原始配置文件，修改数据看和默认端口
[root@localhost conf]# cat sonar.properties 
# Property values can:
# - reference an environment variable, for example sonar.jdbc.url= ${env:SONAR_JDBC_URL}
# - be encrypted. See https://redirect.sonarsource.com/doc/settings-encryption.html

#--------------------------------------------------------------------------------------------------
# DATABASE
#
# IMPORTANT:
# - The embedded H2 database is used by default. It is recommended for tests but not for
#   production use. Supported databases are MySQL, Oracle, PostgreSQL and Microsoft SQLServer.
# - Changes to database connection URL (sonar.jdbc.url) can affect SonarSource licensed products.

# User credentials.
# Permissions to create tables, indices and triggers must be granted to JDBC user.
# The schema must be created first.
#sonar.jdbc.username=
#sonar.jdbc.password=

#----- Embedded Database (default)
# H2 embedded database server listening port, defaults to 9092
#sonar.embeddedDatabase.port=9092

#----- DEPRECATED 
#----- MySQL >=5.6 && <8.0
# Support of MySQL is dropped in Data Center Editions and deprecated in all other editions
# Only InnoDB storage engine is supported (not myISAM).
# Only the bundled driver is supported. It can not be changed.
#sonar.jdbc.url=jdbc:mysql://localhost:3306/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance&useSSL=false


#----- Oracle 11g/12c
# The Oracle JDBC driver must be copied into the directory extensions/jdbc-driver/oracle/.
# Only the thin client is supported, and only the versions 11.2.x or 12.2.x must be used. See
# https://jira.sonarsource.com/browse/SONAR-9758 for more details.
# If you need to set the schema, please refer to http://jira.sonarsource.com/browse/SONAR-5000
#sonar.jdbc.url=jdbc:oracle:thin:@localhost:1521/XE


#----- PostgreSQL 9.3 or greater
# By default the schema named "public" is used. It can be overridden with the parameter "currentSchema".
#sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube?currentSchema=my_schema


#----- Microsoft SQLServer 2014/2016/2017 and SQL Azure
# A database named sonar must exist and its collation must be case-sensitive (CS) and accent-sensitive (AS)
# Use the following connection string if you want to use integrated security with Microsoft Sql Server
# Do not set sonar.jdbc.username or sonar.jdbc.password property if you are using Integrated Security
# For Integrated Security to work, you have to download the Microsoft SQL JDBC driver package from
# https://www.microsoft.com/en-us/download/details.aspx?id=55539
# and copy sqljdbc_auth.dll to your path. You have to copy the 32 bit or 64 bit version of the dll
# depending upon the architecture of your server machine.
#sonar.jdbc.url=jdbc:sqlserver://localhost;databaseName=sonar;integratedSecurity=true

# Use the following connection string if you want to use SQL Auth while connecting to MS Sql Server.
# Set the sonar.jdbc.username and sonar.jdbc.password appropriately.
#sonar.jdbc.url=jdbc:sqlserver://localhost;databaseName=sonar


#----- Connection pool settings
# The maximum number of active connections that can be allocated
# at the same time, or negative for no limit.
# The recommended value is 1.2 * max sizes of HTTP pools. For example if HTTP ports are
# enabled with default sizes (50, see property sonar.web.http.maxThreads)
# then sonar.jdbc.maxActive should be 1.2 * 50 = 60.
#sonar.jdbc.maxActive=60

# The maximum number of connections that can remain idle in the
# pool, without extra ones being released, or negative for no limit.
#sonar.jdbc.maxIdle=5

# The minimum number of connections that can remain idle in the pool,
# without extra ones being created, or zero to create none.
#sonar.jdbc.minIdle=2

# The maximum number of milliseconds that the pool will wait (when there
# are no available connections) for a connection to be returned before
# throwing an exception, or <= 0 to wait indefinitely.
#sonar.jdbc.maxWait=5000

#sonar.jdbc.minEvictableIdleTimeMillis=600000
#sonar.jdbc.timeBetweenEvictionRunsMillis=30000



#--------------------------------------------------------------------------------------------------
# WEB SERVER
# Web server is executed in a dedicated Java process. By default heap size is 512Mb.
# Use the following property to customize JVM options.
#    Recommendations:
#
#    The HotSpot Server VM is recommended. The property -server should be added if server mode
#    is not enabled by default on your environment:
#    http://docs.oracle.com/javase/8/docs/technotes/guides/vm/server-class.html
#
#    Startup can be long if entropy source is short of entropy. Adding
#    -Djava.security.egd=file:/dev/./urandom is an option to resolve the problem.
#    See https://wiki.apache.org/tomcat/HowTo/FasterStartUp#Entropy_Source
#
#sonar.web.javaOpts=-Xmx512m -Xms128m -XX:+HeapDumpOnOutOfMemoryError

# Same as previous property, but allows to not repeat all other settings like -Xmx
#sonar.web.javaAdditionalOpts=

# Binding IP address. For servers with more than one IP address, this property specifies which
# address will be used for listening on the specified ports.
# By default, ports will be used on all IP addresses associated with the server.
#sonar.web.host=0.0.0.0

# Web context. When set, it must start with forward slash (for example /sonarqube).
# The default value is root context (empty value).
#sonar.web.context=
# TCP port for incoming HTTP connections. Default value is 9000.
#sonar.web.port=9000


# The maximum number of connections that the server will accept and process at any given time.
# When this number has been reached, the server will not accept any more connections until
# the number of connections falls below this value. The operating system may still accept connections
# based on the sonar.web.connections.acceptCount property. The default value is 50.
#sonar.web.http.maxThreads=50

# The minimum number of threads always kept running. The default value is 5.
#sonar.web.http.minThreads=5

# The maximum queue length for incoming connection requests when all possible request processing
# threads are in use. Any requests received when the queue is full will be refused.
# The default value is 25.
#sonar.web.http.acceptCount=25

# By default users are logged out and sessions closed when server is restarted.
# If you prefer keeping user sessions open, a secret should be defined. Value is
# HS256 key encoded with base64. It must be unique for each installation of SonarQube.
# Example of command-line:
# echo -n "type_what_you_want" | openssl dgst -sha256 -hmac "key" -binary | base64
#sonar.auth.jwtBase64Hs256Secret=

# The inactivity timeout duration of user sessions, in minutes. After the configured
# period of time, the user is logged out.
# The default value is set to 3 days (4320 minutes)
# and cannot be greater than 3 months. Value must be strictly positive.
#sonar.web.sessionTimeoutInMinutes=4320

# A passcode can be defined to access some web services from monitoring
# tools without having to use the credentials of a system administrator.
# Check the Web API documentation to know which web services are supporting this authentication mode.
# The passcode should be provided in HTTP requests with the header "X-Sonar-Passcode".
# By default feature is disabled.
#sonar.web.systemPasscode=


#--------------------------------------------------------------------------------------------------
# SSO AUTHENTICATION

# Enable authentication using HTTP headers
#sonar.web.sso.enable=false

# Name of the header to get the user login.
# Only alphanumeric, '.' and '@' characters are allowed
#sonar.web.sso.loginHeader=X-Forwarded-Login

# Name of the header to get the user name
#sonar.web.sso.nameHeader=X-Forwarded-Name

# Name of the header to get the user email (optional)
#sonar.web.sso.emailHeader=X-Forwarded-Email

# Name of the header to get the list of user groups, separated by comma (optional).
# If the sonar.sso.groupsHeader is set, the user will belong to those groups if groups exist in SonarQube.
# If none of the provided groups exists in SonarQube, the user will only belong to the default group.
# Note that the default group will always be set.
#sonar.web.sso.groupsHeader=X-Forwarded-Groups

# Interval used to know when to refresh name, email and groups.
# During this interval, if for instance the name of the user is changed in the header, it will only be updated after X minutes.
#sonar.web.sso.refreshIntervalInMinutes=5

#--------------------------------------------------------------------------------------------------
# LDAP CONFIGURATION

# Enable the LDAP feature
# sonar.security.realm=LDAP

# Set to true when connecting to a LDAP server using a case-insensitive setup.
# sonar.authenticator.downcase=true

# URL of the LDAP server. Note that if you are using ldaps, then you should install the server certificate into the Java truststore.
# ldap.url=ldap://localhost:10389

# Bind DN is the username of an LDAP user to connect (or bind) with. Leave this blank for anonymous access to the LDAP directory (optional)
# ldap.bindDn=cn=sonar,ou=users,o=mycompany

# Bind Password is the password of the user to connect with. Leave this blank for anonymous access to the LDAP directory (optional)
# ldap.bindPassword=secret

# Possible values: simple | CRAM-MD5 | DIGEST-MD5 | GSSAPI See http://java.sun.com/products/jndi/tutorial/ldap/security/auth.html (default: simple)
# ldap.authentication=simple

# See :
#   * http://java.sun.com/products/jndi/tutorial/ldap/security/digest.html
#   * http://java.sun.com/products/jndi/tutorial/ldap/security/crammd5.html
# (optional)
# ldap.realm=example.org

# Context factory class (optional)
# ldap.contextFactoryClass=com.sun.jndi.ldap.LdapCtxFactory

# Enable usage of StartTLS (default : false)
# ldap.StartTLS=true

# Follow or not referrals. See http://docs.oracle.com/javase/jndi/tutorial/ldap/referral/jndi.html (default: true)
# ldap.followReferrals=false

# USER MAPPING

# Distinguished Name (DN) of the root node in LDAP from which to search for users (mandatory)
# ldap.user.baseDn=cn=users,dc=example,dc=org

# LDAP user request. (default: (&(objectClass=inetOrgPerson)(uid={login})) )
# ldap.user.request=(&(objectClass=user)(sAMAccountName={login}))

# Attribute in LDAP defining the user’s real name. (default: cn)
# ldap.user.realNameAttribute=name

# Attribute in LDAP defining the user’s email. (default: mail)
# ldap.user.emailAttribute=email

# GROUP MAPPING

# Distinguished Name (DN) of the root node in LDAP from which to search for groups. (optional, default: empty)
# ldap.group.baseDn=cn=groups,dc=example,dc=org

# LDAP group request (default: (&(objectClass=groupOfUniqueNames)(uniqueMember={dn})) )
# ldap.group.request=(&(objectClass=group)(member={dn}))

# Property used to specifiy the attribute to be used for returning the list of user groups in the compatibility mode. (default: cn)
# ldap.group.idAttribute=sAMAccountName

#--------------------------------------------------------------------------------------------------
# COMPUTE ENGINE
# The Compute Engine is responsible for processing background tasks.
# Compute Engine is executed in a dedicated Java process. Default heap size is 512Mb.
# Use the following property to customize JVM options.
#    Recommendations:
#
#    The HotSpot Server VM is recommended. The property -server should be added if server mode
#    is not enabled by default on your environment:
#    http://docs.oracle.com/javase/8/docs/technotes/guides/vm/server-class.html
#
#sonar.ce.javaOpts=-Xmx512m -Xms128m -XX:+HeapDumpOnOutOfMemoryError

# Same as previous property, but allows to not repeat all other settings like -Xmx
#sonar.ce.javaAdditionalOpts=


#--------------------------------------------------------------------------------------------------
# ELASTICSEARCH
# Elasticsearch is used to facilitate fast and accurate information retrieval.
# It is executed in a dedicated Java process. Default heap size is 512Mb.
#
# --------------------------------------------------
# Word of caution for Linux users on 64bits systems
# --------------------------------------------------
# Please ensure Virtual Memory on your system is correctly configured for Elasticsearch to run properly
# (see https://www.elastic.co/guide/en/elasticsearch/reference/5.5/vm-max-map-count.html for details).
#
# When SonarQube runs standalone, a warning such as the following may appear in logs/es.log:
#      "max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]"
# When SonarQube runs as a cluster, however, Elasticsearch will refuse to start.
#

# JVM options of Elasticsearch process
#sonar.search.javaOpts=-Xms512m -Xmx512m -XX:+HeapDumpOnOutOfMemoryError

# Same as previous property, but allows to not repeat all other settings like -Xmx
#sonar.search.javaAdditionalOpts=

# Elasticsearch port. Default is 9001. Use 0 to get a free port.
# As a security precaution, should be blocked by a firewall and not exposed to the Internet.
#sonar.search.port=9001

# Elasticsearch host. The search server will bind this address and the search client will connect to it.
# Default is loopback address.
# As a security precaution, should NOT be set to a publicly available address.
#sonar.search.host=


#--------------------------------------------------------------------------------------------------
# UPDATE CENTER

# Update Center requires an internet connection to request https://update.sonarsource.org
# It is enabled by default.
#sonar.updatecenter.activate=true

# HTTP proxy (default none)
#http.proxyHost=
#http.proxyPort=
# HTTPS proxy (defaults are values of http.proxyHost and http.proxyPort)
#https.proxyHost=
#https.proxyPort=

# NT domain name if NTLM proxy is used
#http.auth.ntlm.domain=

# SOCKS proxy (default none)
#socksProxyHost=
#socksProxyPort=

# Proxy authentication (used for HTTP, HTTPS and SOCKS proxies)
#http.proxyUser=
#http.proxyPassword=


#--------------------------------------------------------------------------------------------------
# LOGGING

# SonarQube produces logs in 4 logs files located in the same directory (see property sonar.path.logs below),
# one per process:
#   Main process (aka. App) logs in sonar.log
#   Web Server (aka. Web) logs in web.log
#   Compute Engine (aka. CE) logs in ce.log
#   Elasticsearch (aka. ES) logs in es.log
#
# All 4 files follow the same rolling policy (see sonar.log.rollingPolicy and sonar.log.maxFiles) but it applies
# individually (eg. if sonar.log.maxFiles=4, there can be at most 4 of each files, ie. 16 files in total).
#
# All 4 files have logs in the same format:
#           1           2    3           4                       5                                                   6
# |-----------------| |---| |-|--------------------||------------------------------| |------------------------------------------------------------------------------------------------------------------------------|
# 2016.11.16 16:47:00 INFO  ce[AVht0dNXFcyiYejytc3m][o.s.s.c.t.CeWorkerCallableImpl] Executed task | project=org.sonarqube:example-java-maven | type=REPORT | id=AVht0dNXFcyiYejytc3m | submitter=admin | time=1699ms
#
# 1: timestamp. Format is YYYY.MM.DD HH:MM:SS
#    YYYY: year on 4 digits
#    MM: month on 2 digits
#    DD: day on 2 digits
#    HH: hour of day on 2 digits in 24 hours format
#    MM: minutes on 2 digits
#    SS: seconds on 2 digits
# 2: log level.
#    Possible values (in order of descending criticality): ERROR, WARN, INFO, DEBUG and TRACE
# 3: process identifier. Possible values: app (main), web (Web Server), ce (Compute Engine) and es (Elasticsearch)
# 4: SQ thread identifier. Can be empty.
#    In the Web Server, if present, it will be the HTTP request ID.
#    In the Compute Engine, if present, it will be the task ID.
# 5: logger name. Usually a class canonical name.
#    Package names are truncated to keep the whole field to 20 characters max
# 6: log payload. Content of this field does not follow any specific format, can vary in length and include line returns.
#    Some logs, however, will follow the convention to provide data in payload in the format " | key=value"
#    Especially, log of profiled pieces of code will end with " | time=XXXXms".

# Global level of logs (applies to all 4 processes).
# Supported values are INFO (default), DEBUG and TRACE
#sonar.log.level=INFO

# Level of logs of each process can be controlled individually with their respective properties.
# When specified, they overwrite the level defined at global level.
# Supported values are INFO, DEBUG and TRACE
#sonar.log.level.app=INFO
#sonar.log.level.web=INFO
#sonar.log.level.ce=INFO
#sonar.log.level.es=INFO

# Path to log files. Can be absolute or relative to installation directory.
# Default is <installation home>/logs
#sonar.path.logs=logs

# Rolling policy of log files
#    - based on time if value starts with "time:", for example by day ("time:yyyy-MM-dd")
#      or by month ("time:yyyy-MM")
#    - based on size if value starts with "size:", for example "size:10MB"
#    - disabled if value is "none".  That needs logs to be managed by an external system like logrotate.
#sonar.log.rollingPolicy=time:yyyy-MM-dd

# Maximum number of files to keep if a rolling policy is enabled.
#    - maximum value is 20 on size rolling policy
#    - unlimited on time rolling policy. Set to zero to disable old file purging.
#sonar.log.maxFiles=7

# Access log is the list of all the HTTP requests received by server. If enabled, it is stored
# in the file {sonar.path.logs}/access.log. This file follows the same rolling policy as other log file
# (see sonar.log.rollingPolicy and sonar.log.maxFiles).
#sonar.web.accessLogs.enable=true

# Format of access log. It is ignored if sonar.web.accessLogs.enable=false. Possible values are:
#    - "common" is the Common Log Format, shortcut to: %h %l %u %user %date "%r" %s %b
#    - "combined" is another format widely recognized, shortcut to: %h %l %u [%t] "%r" %s %b "%i{Referer}" "%i{User-Agent}"
#    - else a custom pattern. See http://logback.qos.ch/manual/layouts.html#AccessPatternLayout.
# The login of authenticated user is not implemented with "%u" but with "%reqAttribute{LOGIN}" (since version 6.1).
# The value displayed for anonymous users is "-".
# The SonarQube's HTTP request ID can be added to the pattern with "%reqAttribute{ID}" (since version 6.2).
# If SonarQube is behind a reverse proxy, then the following value allows to display the correct remote IP address:
#sonar.web.accessLogs.pattern=%i{X-Forwarded-For} %l %u [%t] "%r" %s %b "%i{Referer}" "%i{User-Agent}" "%reqAttribute{ID}"
# Default value (which was "combined" before version 6.2) is equivalent to "combined + SQ HTTP request ID":
#sonar.web.accessLogs.pattern=%h %l %u [%t] "%r" %s %b "%i{Referer}" "%i{User-Agent}" "%reqAttribute{ID}"


#--------------------------------------------------------------------------------------------------
# OTHERS

# Delay in seconds between processing of notification queue. Default is 60 seconds.
#sonar.notifications.delay=60

# Paths to persistent data files (embedded database and search index) and temporary files.
# Can be absolute or relative to installation directory.
# Defaults are respectively <installation home>/data and <installation home>/temp
#sonar.path.data=data
#sonar.path.temp=temp

# Telemetry - Share anonymous SonarQube statistics
# By sharing anonymous SonarQube statistics, you help us understand how SonarQube is used so we can improve the product to work even better for you.
# We don't collect source code or IP addresses. And we don't share the data with anyone else.
# To see an example of the data shared: login as a global administrator, call the WS api/system/info and check the Statistics field.
#sonar.telemetry.enable=true


#--------------------------------------------------------------------------------------------------
# DEVELOPMENT - only for developers
# The following properties MUST NOT be used in production environments.

# Elasticsearch HTTP connector
#sonar.search.httpPort=-1
[root@localhost conf]# 


[root@localhost conf]# cat wrapper.conf 
# Path to JVM executable. By default it must be available in PATH.
# Can be an absolute path, for example:
#wrapper.java.command=/path/to/my/jdk/bin/java
wrapper.java.command=java


#
# DO NOT EDIT THE FOLLOWING SECTIONS
#


#********************************************************************
# Wrapper Java
#********************************************************************
wrapper.java.additional.1=-Dsonar.wrapped=true
wrapper.java.additional.2=-Djava.awt.headless=true
wrapper.java.mainclass=org.tanukisoftware.wrapper.WrapperSimpleApp
wrapper.java.classpath.1=../../lib/jsw/*.jar
wrapper.java.classpath.2=../../lib/common/*.jar
wrapper.java.classpath.3=../../lib/*.jar
wrapper.java.library.path.1=./lib
wrapper.app.parameter.1=org.sonar.application.App
wrapper.java.initmemory=8
wrapper.java.maxmemory=32

#********************************************************************
# Wrapper Logs
#********************************************************************

wrapper.console.format=PM
wrapper.console.loglevel=INFO
wrapper.logfile=../../logs/sonar.log
wrapper.logfile.format=M
wrapper.logfile.loglevel=INFO

# Maximum size that the log file will be allowed to grow to before
#  the log is rolled. Size is specified in bytes.  The default value
#  of 0, disables log rolling.  May abbreviate with the 'k' (kb) or
#  'm' (mb) suffix.  For example: 10m = 10 megabytes.
#wrapper.logfile.maxsize=0

# Maximum number of rolled log files which will be allowed before old
#  files are deleted.  The default value of 0 implies no limit.
#wrapper.logfile.maxfiles=0

# Log Level for sys/event log output.  (See docs for log levels)
wrapper.syslog.loglevel=NONE

#********************************************************************
# Wrapper Windows Properties
#********************************************************************
# Title to use when running as a console
wrapper.console.title=SonarQube

# Disallow start of multiple instances of an application at the same time on Windows
wrapper.single_invocation=true

#********************************************************************
# Wrapper Windows NT/2000/XP Service Properties
#********************************************************************
# WARNING - Do not modify any of these properties when an application
#  using this configuration file has been installed as a service.
#  Please uninstall the service before modifying this section.  The
#  service can then be reinstalled.

# Name of the service
wrapper.ntservice.name=SonarQube

# Display name of the service
wrapper.ntservice.displayname=SonarQube

# Description of the service
wrapper.ntservice.description=SonarQube

# Service dependencies.  Add dependencies as needed starting from 1
wrapper.ntservice.dependency.1=

# Mode in which the service is installed.  AUTO_START or DEMAND_START
wrapper.ntservice.starttype=AUTO_START

# Allow the service to interact with the desktop.
wrapper.ntservice.interactive=false

#********************************************************************
# Forking Properties
#********************************************************************
wrapper.disable_restarts=TRUE
wrapper.ping.timeout=0
wrapper.shutdown.timeout=300
wrapper.jvm_exit.timeout=300
[root@localhost conf]# 

docker run -d --name sonarqube \
    -p 9000:9008 \
    -v /root/work/SonarQube/sonarqube:/opt/sonarqube \
    sonarqube


```

## sonar kubernetes

```bash
[root@k8s-master1 temp]# cat ./my.cnf 
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
user=mysql
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
bind-address=0.0.0.0

# character-set-server=utf8
# collation-server=utf8_bin

default-storage-engine=INNODB

max_allowed_packet=256M

innodb_log_file_size=2GB

# sql_mode = sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

transaction-isolation=READ-COMMITTED

binlog_format=row


# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

# 
character_set_server=utf8mb4
collation_server=utf8mb4_bin
innodb_default_row_format=DYNAMIC
innodb_large_prefix=ON
innodb_file_format=Barracuda
# innodb_log_file_size=2G

# sql_mode = NO_AUTO_VALUE_ON_ZERO
[root@k8s-master1 temp]# 


kubectl create configmap sonar-mysql-config --from-file=./my.cnf

[root@k8s-master1 temp]# kubectl get configmap -o wide
NAME                      DATA   AGE
confluence-mysql-config   1      19d
docker-registry-auth      1      10d
docker-registry-config    1      10d
edusoho-mysql-config      1      19d
sonar-mysql-config        1      12m
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# vim sonar-mysql.yml 
[root@k8s-master1 temp]# cat sonar-mysql.yml 
---
apiVersion: v1
kind: Service
metadata:
  name: sonar-mysql
  labels:
    app: sonar
spec:
  ports:
    - port: 3306
  selector:
    app: sonar
    tier: mysql

---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: sonar-mysql
  labels:
    app: sonar
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: sonar
        tier: mysql
    spec:
      containers:
        - image: mysql/mysql-server:5.7
          name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: rootpassword
          ports:
            - containerPort: 3306
              name: mysql

          volumeMounts:
            - name: mysql-config
              subPath: my.cnf
              mountPath: /etc/my.cnf

            - name: mysql-log
              subPath: mysqld.log
              mountPath: /var/log/mysqld.log

            - name: mysql-data
              mountPath: /var/lib/mysql

      nodeSelector:
        nodename:
          k8s-linux-worker3

      volumes:
        - name: mysql-config
          configMap:
            name: sonar-mysql-config

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/sonar_mysql/mysql-log/

        - name: mysql-data
          hostPath:
            path: /opt/k8s/volume_data/sonar_mysql/mysql-data/

[root@k8s-master1 temp]# 

[root@k8s-linux-worker3 sonar_mysql]# pwd
/opt/k8s/volume_data/sonar_mysql
[root@k8s-linux-worker3 sonar_mysql]# mkdir mysql-log/
[root@k8s-linux-worker3 sonar_mysql]# mkdir mysql-data
[root@k8s-linux-worker3 sonar_mysql]# ll
total 8
drwxr-xr-x 2 root root 4096 Jun 25 10:08 mysql-data
drwxr-xr-x 2 root root 4096 Jun 25 10:08 mysql-log
[root@k8s-linux-worker3 sonar_mysql]# 
[root@k8s-linux-worker3 sonar_mysql]# touch mysql-log/mysqld.log
[root@k8s-linux-worker3 sonar_mysql]# chmod -R 777  mysql-log
[root@k8s-linux-worker3 sonar_mysql]# 
  
[root@k8s-master1 temp]# kubectl apply -f  ./sonar-mysql.yml
service/sonar-mysql created
deployment.extensions/sonar-mysql created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR
sonar-mysql        ClusterIP   10.68.239.53    <none>        3306/TCP         24s   app=sonar,tier=mysql
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS        IMAGES                                         SELECTOR
sonar-mysql             1/1     1            1           45s   mysql             mysql/mysql-server:5.7                         app=sonar,tier=mysql
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS      RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
sonar-mysql-69f946bd64-r28xc             1/1     Running     0          61s   172.20.2.20   10.1.36.48   <none>           <none>
[root@k8s-master1 temp]# 

bash-4.2# mysql -u root -p -h 10.68.239.53
Enter password: rootpassword

mysql> 
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpassword';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> 


docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=root \
    -e sonar.jdbc.password=rootpass \
    -e "sonar.jdbc.url=jdbc:mysql://172.17.0.6/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance" \
    -v /root/work/SonarQube/conf:/opt/sonarqube/conf \
    -v /root/work/SonarQube/data:/opt/sonarqube/data \
    -v /root/work/SonarQube/logs:/opt/sonarqube/logs \
    -v /root/work/SonarQube/extensions:/opt/sonarqube/extensions \
    sonarqube

[root@k8s-linux-worker3 conf]# pwd
/opt/k8s/volume_data/sonar_data/conf
[root@k8s-linux-worker3 conf]# vim sonar.properties


[root@k8s-master1 temp]# vim sonar.yml 
[root@k8s-master1 temp]# cat sonar.yml 
apiVersion: v1
kind: Service
metadata:
  name: sonar
  labels:
    app: sonar
spec:
  ports:
  - name: http
    port: 9000
    targetPort: 9000
    protocol: TCP
  selector:
    app: sonar
    service: sonar
  type: NodePort
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: sonar-deployment
  labels:
    service: sonar
    app: sonar

spec:
  replicas: 1
  selector:
    matchLabels:
      app: sonar
      service: sonar
  template:
    metadata:
      labels:
        app: sonar
        service: sonar
    spec:
      containers:
        - name: sonar
          image: sonarqube:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 9000
          env:
            - name: sonar.jdbc.username
              value: root
              
            - name: sonar.jdbc.password
              value: rootpassword
              
            - name: sonar.jdbc.url
              value: jdbc:mysql://10.68.239.53/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance
          volumeMounts:
            - name: sonar-conf
              mountPath: /opt/sonarqube/conf
              
            - name: sonar-data
              mountPath: /opt/sonarqube/data
              
            - name: sonar-extensions
              mountPath: /opt/sonarqube/extensions
              
            - name: sonar-logs
              mountPath: /opt/sonarqube/logs
             

      nodeSelector:
        nodename:
          k8s-linux-worker3

      volumes:
        - name: sonar-conf
          hostPath:
            path: /opt/k8s/volume_data/sonar_data/conf
            
        - name: sonar-data
          hostPath:
            path: /opt/k8s/volume_data/sonar_data/data
            
        - name: sonar-extensions
          hostPath:
            path: /opt/k8s/volume_data/sonar_data/extensions
            
        - name: sonar-logs
          hostPath:
            path: /opt/k8s/volume_data/sonar_data/logs

[root@k8s-master1 temp]# 


[root@k8s-master1 temp]# kubectl apply -f  ./sonar.yml 
service/sonar unchanged
deployment.apps/sonar-deployment created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get services -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   21d     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         25d     app=confluence,tier=mysql
docker-registry    NodePort    10.68.186.144   <none>        5000:36496/TCP   10d     app=docker-registry,service=docker-registry
edusoho            NodePort    10.68.148.20    <none>        80:29812/TCP     18d     app=edusoho,service=edusoho
edusoho-mysql      ClusterIP   10.68.42.16     <none>        3306/TCP         19d     app=edusoho,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   19d     app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          34d     <none>
sonar              NodePort    10.68.53.235    <none>        9000:28256/TCP   2m29s   app=sonar,service=sonar
sonar-mysql        ClusterIP   10.68.239.53    <none>        3306/TCP         41m     app=sonar,tier=mysql
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS        IMAGES                                         SELECTOR
confluence-deployment   1/1     1            1           15d   confluence        atlassian/confluence-server:latest             app=confluence,service=confluence
confluence-mysql        1/1     1            1           19d   mysql             mysql/mysql-server:5.7                         app=confluence,tier=mysql
docker-registry         1/1     1            1           10d   docker-registry   registry:latest                                app=docker-registry,service=docker-registry
edusoho-deployment      1/1     1            1           18d   edusoho           edusoho/edusoho                                app=edusoho,service=edusoho
edusoho-mysql           1/1     1            1           19d   mysql             mysql/mysql-server:5.7                         app=edusoho,tier=mysql
jira-deployment         1/1     1            1           19d   jira              cptactionhank/atlassian-jira-software:latest   app=jira,service=jira
my-nginx                8/8     8            8           27d   my-nginx          nginx                                          run=my-nginx
sonar-deployment        1/1     1            1           36s   sonar             sonarqube:latest                               app=sonar,service=sonar
sonar-mysql             1/1     1            1           41m   mysql             mysql/mysql-server:5.7                         app=sonar,tier=mysql
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS      RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-59c98447bf-tqndr   1/1     Running     0          15d     172.20.2.19   10.1.36.48   <none>           <none>
confluence-mysql-859d7f788b-24l27        1/1     Running     0          19d     172.20.0.19   10.1.36.46   <none>           <none>
docker-registry-6685d74448-t87zv         1/1     Running     0          10d     172.20.1.29   10.1.36.47   <none>           <none>
edusoho-deployment-64bc89766b-hqvcs      1/1     Running     0          18d     172.20.3.12   10.1.36.49   <none>           <none>
edusoho-mysql-fc4f549f5-hv9sw            1/1     Running     0          19d     172.20.1.26   10.1.36.47   <none>           <none>
jira-deployment-ccc84bffd-r9mzz          1/1     Running     0          19d     172.20.2.16   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running     0          27d     172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running     0          27d     172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running     0          27d     172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running     0          27d     172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running     0          27d     172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running     0          27d     172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running     0          27d     172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running     0          27d     172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     Completed   0          8m37s   172.20.1.30   10.1.36.47   <none>           <none>
sonar-deployment-7df689bd74-p4gss        1/1     Running     0          47s     172.20.2.21   10.1.36.48   <none>           <none>
sonar-mysql-69f946bd64-r28xc             1/1     Running     0          41m     172.20.2.20   10.1.36.48   <none>           <none>
[root@k8s-master1 temp]# 




```

## sonar 使用

[参考](https://blog.csdn.net/qq_42564846/article/details/81407117)

插件安装

chinese
c#
JavaScript

```

SonarScanner.MSBuild.exe begin /k:"platform" /n:"platform" /v:"platform-1.0" /d:sonar.cs.nunit.reportsPaths="NUnitResults.xml" /d:sonar.cs.dotcover.reportsPaths="dotCover.html"

msbuild src\平台整体解决方案.sln

SonarScanner.MSBuild.exe end

```

