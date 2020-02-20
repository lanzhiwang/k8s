# Confluence

[Confluence 镜像](https://hub.docker.com/r/atlassian/confluence-server)

## 分析 Dockerfile

```bash
FROM adoptopenjdk/openjdk8:alpine
MAINTAINER Atlassian Confluence

ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# https://confluence.atlassian.com/doc/confluence-home-and-other-important-directories-590259707.html
ENV CONFLUENCE_HOME          /var/atlassian/application-data/confluence
ENV CONFLUENCE_INSTALL_DIR   /opt/atlassian/confluence

VOLUME ["${CONFLUENCE_HOME}"]

# Expose HTTP and Synchrony ports
EXPOSE 8090
EXPOSE 8091

WORKDIR $CONFLUENCE_HOME

CMD ["/entrypoint.sh", "-fg"]
ENTRYPOINT ["/sbin/tini", "--"]

RUN apk add --no-cache ca-certificates wget curl openssh bash procps openssl perl ttf-dejavu tini

COPY entrypoint.sh              /entrypoint.sh

ARG CONFLUENCE_VERSION=6.9.3
ARG DOWNLOAD_URL=http://www.atlassian.com/software/confluence/downloads/binary/atlassian-confluence-${CONFLUENCE_VERSION}.tar.gz

COPY . /tmp

RUN mkdir -p                             ${CONFLUENCE_INSTALL_DIR} \
    && curl -L --silent                  ${DOWNLOAD_URL} | tar -xz --strip-components=1 -C "$CONFLUENCE_INSTALL_DIR" \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CONFLUENCE_INSTALL_DIR}/ \
    && sed -i -e 's/-Xms\([0-9]\+[kmg]\) -Xmx\([0-9]\+[kmg]\)/-Xms\${JVM_MINIMUM_MEMORY:=\1} -Xmx\${JVM_MAXIMUM_MEMORY:=\2} \${JVM_SUPPORT_RECOMMENDED_ARGS} -Dconfluence.home=\${CONFLUENCE_HOME}/g' ${CONFLUENCE_INSTALL_DIR}/bin/setenv.sh \
    && sed -i -e 's/port="8090"/port="8090" secure="${catalinaConnectorSecure}" scheme="${catalinaConnectorScheme}" proxyName="${catalinaConnectorProxyName}" proxyPort="${catalinaConnectorProxyPort}"/' ${CONFLUENCE_INSTALL_DIR}/conf/server.xml  \
    && sed -i -e 's/Context path=""/Context path="${catalinaContextPath}"/' ${CONFLUENCE_INSTALL_DIR}/conf/server.xml

# Workaround for AdoptOpenJDK fontconfig bug
RUN ln -s /usr/lib/libfontconfig.so.1 /usr/lib/libfontconfig.so \
    && ln -s /lib/libuuid.so.1 /usr/lib/libuuid.so.1 \
    && ln -s /lib/libc.musl-x86_64.so.1 /usr/lib/libc.musl-x86_64.so.1
ENV LD_LIBRARY_PATH /usr/lib

```

### 目录

/var/atlassian/application-data/confluence

/opt/atlassian/confluence



### 环境变量

${JVM_MINIMUM_MEMORY}

${JVM_MAXIMUM_MEMORY}

${JVM_SUPPORT_RECOMMENDED_ARGS}

${catalinaConnectorSecure}

${catalinaConnectorScheme}

${catalinaConnectorProxyName}

${catalinaConnectorProxyPort}

${catalinaContextPath}



测试点：

1、挂载 /opt/atlassian/confluence 目录



docker pull atlassian/confluence-server



### confluence 容器相关

```bash
# 使用最新的镜像启动 confluence 容器
[root@lanzhiwang-centos7 ~]# docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
atlassian/confluence-server   latest              d843736462f7        13 days ago         862MB
[root@lanzhiwang-centos7 ~]# 

# 挂载 confluence 数据目录启动容器，容器可以正常启动
[root@lanzhiwang-centos7 docker_data]# docker run -v /root/work/confluence/docker_data/confluence_home:/var/atlassian/application-data/confluence --name="confluence" -d -p 8090:8090 -p 8091:8091 atlassian/confluence-server
1fcb86fa81f94474fa03961a9b717ad86809cd98ba6146825f5c0da487b6b800
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
1fcb86fa81f9        atlassian/confluence-server   "/tini -- /entrypoin…"   4 seconds ago       Up 3 seconds        0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_home/
total 4
-rw-r----- 1 bin bin 3462 May 30 11:51 confluence.cfg.xml
drwxr-x--- 2 bin bin  102 May 30 11:51 logs
drwxr-x--- 2 bin bin   32 May 30 11:51 shared-home
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_install/
total 0
[root@lanzhiwang-centos7 docker_data]# 

# 挂载 confluence 数据目录和 安装目录 启动容器
[root@lanzhiwang-centos7 docker_data]# mkdir confluence_home
[root@lanzhiwang-centos7 docker_data]# mkdir confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x 2 root root 6 Jun  3 17:14 confluence_home
drwxr-xr-x 2 root root 6 Jun  3 17:15 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker run -v /root/work/confluence/docker_data/confluence_home:/var/atlassian/application-data/confluence -v /root/work/confluence/docker_data/confluence_install:/opt/atlassian/confluence --name="confluence" -d -p 8090:8090 -p 8091:8091 atlassian/confluence-server
08b8e7e14c3bf888310e60d4565f9c440ca7553bf99a69b3e8e975dafeebff0d
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS                       PORTS               NAMES
08b8e7e14c3b        atlassian/confluence-server   "/tini -- /entrypoin…"   8 seconds ago       Exited (127) 6 seconds ago                       confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker logs 08b8e7e14c3b
User is currently root. Will change directory ownership to daemon:daemon, then downgrade permission to daemon
bash: /opt/atlassian/confluence/bin/start-confluence.sh: No such file or directory
[root@lanzhiwang-centos7 docker_data]# 

错误分析：
1、要提前将 confluence tar 包内的目录和文件放入 /root/work/confluence/docker_data/confluence_install 目录中
2、将 /root/work/confluence/docker_data/confluence_install 用户和用户组修改成 daemon:daemon


[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root root   6 Jun  3 17:19 confluence_home
drwxr-xr-x 12 1000 1000 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chown -R daemon:daemon confluence_install/
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root   root     6 Jun  3 17:19 confluence_home
drwxr-xr-x 12 daemon daemon 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_home/
total 0
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_install/  # 从 atlassian-confluence-6.15.4.tar.gz 解压而来
total 204
drwxr-xr-x  3 daemon daemon  4096 Jun  3 17:21 bin
-rw-r--r--  1 daemon daemon 19743 Apr 12 23:24 BUILDING.txt
drwxr-xr-x  3 daemon daemon   256 Jun  3 17:21 conf
drwxr-xr-x 27 daemon daemon  4096 Jun  3 17:21 confluence
-rw-r--r--  1 daemon daemon  5543 Apr 12 23:24 CONTRIBUTING.md
drwxr-xr-x  2 daemon daemon  4096 Jun  3 17:21 lib
-rw-r--r--  1 daemon daemon 58153 Apr 12 23:24 LICENSE
drwxr-xr-x  2 daemon daemon 45056 Jun  3 17:21 licenses
drwxr-xr-x  2 daemon daemon     6 Apr 12 23:22 logs
-rw-r--r--  1 daemon daemon  2401 Apr 12 23:24 NOTICE
-rw-r--r--  1 daemon daemon  2294 May  8 11:09 README.html
-rw-r--r--  1 daemon daemon  3334 Apr 12 23:24 README.md
-rw-r--r--  1 daemon daemon  1204 May  8 11:09 README.txt
-rw-r--r--  1 daemon daemon  7025 Apr 12 23:24 RELEASE-NOTES
-rw-r--r--  1 daemon daemon 16738 Apr 12 23:24 RUNNING.txt
drwxr-xr-x  4 daemon daemon    37 Jun  3 17:21 synchrony-proxy
drwxr-xr-x  2 daemon daemon    30 Jun  3 17:21 temp
drwxr-xr-x  2 daemon daemon     6 May  8 11:10 webapps
drwxr-xr-x  2 daemon daemon     6 Apr 12 23:22 work
[root@lanzhiwang-centos7 docker_data]# 


[root@lanzhiwang-centos7 docker_data]# docker run -v /root/work/confluence/docker_data/confluence_home:/var/atlassian/application-data/confluence -v /root/work/confluence/docker_data/confluence_install:/opt/atlassian/confluence --name="confluence" -d -p 8090:8090 -p 8091:8091 atlassian/confluence-server
458de9470f8fb9ff2410a56dfa68a5d282c5627db8c0130b31b086effe3c8145
[root@lanzhiwang-centos7 docker_data]# 

# 容器启动成功，但是log里面有报错，访问页面也会报错
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
458de9470f8f        atlassian/confluence-server   "/tini -- /entrypoin…"   6 seconds ago       Up 5 seconds        0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker logs 458de9470f8f
User is currently root. Will change directory ownership to daemon:daemon, then downgrade permission to daemon
executing as current user
If you encounter issues starting up Confluence, please see the Installation guide at http://confluence.atlassian.com/display/DOC/Confluence+Installation+Guide

Server startup logs are located in /opt/atlassian/confluence/logs/catalina.out
---------------------------------------------------------------------------
Using Java: /opt/java/openjdk/bin/java
log4j:ERROR setFile(null,true) call failed.
java.io.FileNotFoundException: /opt/atlassian/confluence/logs/synchrony-proxy-watchdog.log (Permission denied)
	at java.io.FileOutputStream.open0(Native Method)
	at java.io.FileOutputStream.open(Unknown Source)
	at java.io.FileOutputStream.<init>(Unknown Source)
	at java.io.FileOutputStream.<init>(Unknown Source)
	at org.apache.log4j.FileAppender.setFile(FileAppender.java:294)
	at org.apache.log4j.RollingFileAppender.setFile(RollingFileAppender.java:207)
	at org.apache.log4j.FileAppender.activateOptions(FileAppender.java:165)
	at com.atlassian.confluence.bootstrap.SynchronyProxyWatchdog.addLogFileAppender(SynchronyProxyWatchdog.java:106)
	at com.atlassian.confluence.bootstrap.SynchronyProxyWatchdog.main(SynchronyProxyWatchdog.java:47)
2019-06-03 09:24:01,038 INFO [main] [atlassian.confluence.bootstrap.SynchronyProxyWatchdog] A Context element for ${confluence.context.path}/synchrony-proxy is found in /opt/atlassian/confluence/conf/server.xml. No further action is required
---------------------------------------------------------------------------
OpenJDK 64-Bit Server VM warning: Cannot open file /opt/atlassian/confluence/logs/gc-2019-06-03_09-24-01.log due to Permission denied

java.util.logging.ErrorManager: 4
java.io.FileNotFoundException: /opt/atlassian/confluence/logs/catalina.2019-06-03.log (Permission denied)
	at java.io.FileOutputStream.open0(Native Method)
	at java.io.FileOutputStream.open(Unknown Source)
	at java.io.FileOutputStream.<init>(Unknown Source)
	at org.apache.juli.FileHandler.openWriter(FileHandler.java:513)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:180)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:167)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:82)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:78)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:74)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(Unknown Source)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(Unknown Source)
	at java.lang.reflect.Constructor.newInstance(Unknown Source)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:602)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:538)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:336)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.readPrimordialConfiguration(Unknown Source)
	at java.util.logging.LogManager.access$800(Unknown Source)
	at java.util.logging.LogManager$2.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.ensureLogManagerInitialized(Unknown Source)
	at java.util.logging.LogManager.getLogManager(Unknown Source)
	at java.util.logging.Logger.demandLogger(Unknown Source)
	at java.util.logging.Logger.getLogger(Unknown Source)
	at org.apache.juli.logging.DirectJDKLog.<init>(DirectJDKLog.java:61)
	at org.apache.juli.logging.DirectJDKLog.getInstance(DirectJDKLog.java:181)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:130)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:153)
	at org.apache.juli.logging.LogFactory.getLog(LogFactory.java:208)
	at org.apache.catalina.startup.Bootstrap.<clinit>(Bootstrap.java:52)
java.util.logging.ErrorManager: 4
java.io.FileNotFoundException: /opt/atlassian/confluence/logs/localhost.2019-06-03.log (Permission denied)
	at java.io.FileOutputStream.open0(Native Method)
	at java.io.FileOutputStream.open(Unknown Source)
	at java.io.FileOutputStream.<init>(Unknown Source)
	at org.apache.juli.FileHandler.openWriter(FileHandler.java:513)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:180)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:167)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:82)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:78)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:74)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(Unknown Source)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(Unknown Source)
	at java.lang.reflect.Constructor.newInstance(Unknown Source)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:602)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:538)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:336)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.readPrimordialConfiguration(Unknown Source)
	at java.util.logging.LogManager.access$800(Unknown Source)
	at java.util.logging.LogManager$2.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.ensureLogManagerInitialized(Unknown Source)
	at java.util.logging.LogManager.getLogManager(Unknown Source)
	at java.util.logging.Logger.demandLogger(Unknown Source)
	at java.util.logging.Logger.getLogger(Unknown Source)
	at org.apache.juli.logging.DirectJDKLog.<init>(DirectJDKLog.java:61)
	at org.apache.juli.logging.DirectJDKLog.getInstance(DirectJDKLog.java:181)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:130)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:153)
	at org.apache.juli.logging.LogFactory.getLog(LogFactory.java:208)
	at org.apache.catalina.startup.Bootstrap.<clinit>(Bootstrap.java:52)
java.util.logging.ErrorManager: 4
java.io.FileNotFoundException: /opt/atlassian/confluence/logs/manager.2019-06-03.log (Permission denied)
	at java.io.FileOutputStream.open0(Native Method)
	at java.io.FileOutputStream.open(Unknown Source)
	at java.io.FileOutputStream.<init>(Unknown Source)
	at org.apache.juli.FileHandler.openWriter(FileHandler.java:513)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:180)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:167)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:82)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:78)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:74)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(Unknown Source)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(Unknown Source)
	at java.lang.reflect.Constructor.newInstance(Unknown Source)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:602)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:538)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:336)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.readPrimordialConfiguration(Unknown Source)
	at java.util.logging.LogManager.access$800(Unknown Source)
	at java.util.logging.LogManager$2.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.ensureLogManagerInitialized(Unknown Source)
	at java.util.logging.LogManager.getLogManager(Unknown Source)
	at java.util.logging.Logger.demandLogger(Unknown Source)
	at java.util.logging.Logger.getLogger(Unknown Source)
	at org.apache.juli.logging.DirectJDKLog.<init>(DirectJDKLog.java:61)
	at org.apache.juli.logging.DirectJDKLog.getInstance(DirectJDKLog.java:181)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:130)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:153)
	at org.apache.juli.logging.LogFactory.getLog(LogFactory.java:208)
	at org.apache.catalina.startup.Bootstrap.<clinit>(Bootstrap.java:52)
java.util.logging.ErrorManager: 4
java.io.FileNotFoundException: /opt/atlassian/confluence/logs/host-manager.2019-06-03.log (Permission denied)
	at java.io.FileOutputStream.open0(Native Method)
	at java.io.FileOutputStream.open(Unknown Source)
	at java.io.FileOutputStream.<init>(Unknown Source)
	at org.apache.juli.FileHandler.openWriter(FileHandler.java:513)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:180)
	at org.apache.juli.FileHandler.<init>(FileHandler.java:167)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:82)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:78)
	at org.apache.juli.AsyncFileHandler.<init>(AsyncFileHandler.java:74)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(Unknown Source)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(Unknown Source)
	at java.lang.reflect.Constructor.newInstance(Unknown Source)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:602)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:538)
	at org.apache.juli.ClassLoaderLogManager.readConfiguration(ClassLoaderLogManager.java:336)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.util.logging.LogManager$3.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.readPrimordialConfiguration(Unknown Source)
	at java.util.logging.LogManager.access$800(Unknown Source)
	at java.util.logging.LogManager$2.run(Unknown Source)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.util.logging.LogManager.ensureLogManagerInitialized(Unknown Source)
	at java.util.logging.LogManager.getLogManager(Unknown Source)
	at java.util.logging.Logger.demandLogger(Unknown Source)
	at java.util.logging.Logger.getLogger(Unknown Source)
	at org.apache.juli.logging.DirectJDKLog.<init>(DirectJDKLog.java:61)
	at org.apache.juli.logging.DirectJDKLog.getInstance(DirectJDKLog.java:181)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:130)
	at org.apache.juli.logging.LogFactory.getInstance(LogFactory.java:153)
	at org.apache.juli.logging.LogFactory.getLog(LogFactory.java:208)
	at org.apache.catalina.startup.Bootstrap.<clinit>(Bootstrap.java:52)
03-Jun-2019 09:24:01.428 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server] failed to set property [debug] to [0]
03-Jun-2019 09:24:01.540 WARNING [main] org.apache.catalina.startup.SetAllPropertiesRule.begin [SetAllPropertiesRule]{Server/Service/Connector} Setting property 'debug' to '0' did not find a matching property.
03-Jun-2019 09:24:01.561 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine] failed to set property [debug] to [0]
03-Jun-2019 09:24:01.565 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host] failed to set property [debug] to [0]
03-Jun-2019 09:24:01.591 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host/Context] failed to set property [debug] to [0]
03-Jun-2019 09:24:01.610 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host/Context] failed to set property [debug] to [0]
03-Jun-2019 09:24:01.877 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8090"]
03-Jun-2019 09:24:01.905 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [546] milliseconds
03-Jun-2019 09:24:01.912 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Tomcat-Standalone]
03-Jun-2019 09:24:01.912 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.19]
03-Jun-2019 09:24:01.930 WARNING [Catalina-utility-1] org.apache.catalina.core.StandardContext.postWorkDirectory Failed to create work directory [/opt/atlassian/confluence/work/Standalone/localhost/ROOT] for context []
03-Jun-2019 09:24:01.945 WARNING [Catalina-utility-2] org.apache.catalina.core.StandardContext.postWorkDirectory Failed to create work directory [/opt/atlassian/confluence/work/Standalone/localhost/synchrony-proxy] for context [/synchrony-proxy]
09:24:03,251 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Could NOT find resource [logback-test.xml]
09:24:03,251 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Could NOT find resource [logback.groovy]
09:24:03,251 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Found resource [logback.xml] at [file:/opt/atlassian/confluence/webapps/../synchrony-proxy/WEB-INF/classes/logback.xml]
09:24:03,314 |-INFO in ch.qos.logback.classic.joran.action.ConfigurationAction - debug attribute not set
09:24:03,320 |-INFO in ch.qos.logback.classic.joran.action.ConfigurationAction - Will scan for changes in [file:/opt/atlassian/confluence/webapps/../synchrony-proxy/WEB-INF/classes/logback.xml] 
09:24:03,320 |-INFO in ch.qos.logback.classic.joran.action.ConfigurationAction - Setting ReconfigureOnChangeTask scanning period to 10 seconds
09:24:03,326 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - About to instantiate appender of type [ch.qos.logback.core.ConsoleAppender]
09:24:03,332 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - Naming appender as [console]
09:24:03,341 |-INFO in ch.qos.logback.core.joran.action.NestedComplexPropertyIA - Assuming default type [ch.qos.logback.classic.encoder.PatternLayoutEncoder] for [encoder] property
09:24:03,368 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - About to instantiate appender of type [ch.qos.logback.core.rolling.RollingFileAppender]
09:24:03,372 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - Naming appender as [synchronyProxyLogAppender]
09:24:03,378 |-INFO in ch.qos.logback.core.rolling.FixedWindowRollingPolicy@6427203b - No compression will be used
09:24:03,382 |-INFO in ch.qos.logback.core.joran.action.NestedComplexPropertyIA - Assuming default type [ch.qos.logback.classic.encoder.PatternLayoutEncoder] for [encoder] property
09:24:03,383 |-INFO in ch.qos.logback.core.rolling.RollingFileAppender[synchronyProxyLogAppender] - Active log file name: /opt/atlassian/confluence/logs/atlassian-synchrony-proxy.log
09:24:03,383 |-INFO in ch.qos.logback.core.rolling.RollingFileAppender[synchronyProxyLogAppender] - File property is set to [/opt/atlassian/confluence/logs/atlassian-synchrony-proxy.log]
09:24:03,384 |-ERROR in ch.qos.logback.core.rolling.RollingFileAppender[synchronyProxyLogAppender] - openFile(/opt/atlassian/confluence/logs/atlassian-synchrony-proxy.log,true) call failed. java.io.FileNotFoundException: /opt/atlassian/confluence/logs/atlassian-synchrony-proxy.log (Permission denied)
	at java.io.FileNotFoundException: /opt/atlassian/confluence/logs/atlassian-synchrony-proxy.log (Permission denied)
	at 	at java.io.FileOutputStream.open0(Native Method)
	at 	at java.io.FileOutputStream.open(Unknown Source)
	at 	at java.io.FileOutputStream.<init>(Unknown Source)
	at 	at ch.qos.logback.core.recovery.ResilientFileOutputStream.<init>(ResilientFileOutputStream.java:26)
	at 	at ch.qos.logback.core.FileAppender.openFile(FileAppender.java:204)
	at 	at ch.qos.logback.core.FileAppender.start(FileAppender.java:127)
	at 	at ch.qos.logback.core.rolling.RollingFileAppender.start(RollingFileAppender.java:100)
	at 	at ch.qos.logback.core.joran.action.AppenderAction.end(AppenderAction.java:90)
	at 	at ch.qos.logback.core.joran.spi.Interpreter.callEndAction(Interpreter.java:309)
	at 	at ch.qos.logback.core.joran.spi.Interpreter.endElement(Interpreter.java:193)
	at 	at ch.qos.logback.core.joran.spi.Interpreter.endElement(Interpreter.java:179)
	at 	at ch.qos.logback.core.joran.spi.EventPlayer.play(EventPlayer.java:62)
	at 	at ch.qos.logback.core.joran.GenericConfigurator.doConfigure(GenericConfigurator.java:165)
	at 	at ch.qos.logback.core.joran.GenericConfigurator.doConfigure(GenericConfigurator.java:152)
	at 	at ch.qos.logback.core.joran.GenericConfigurator.doConfigure(GenericConfigurator.java:110)
	at 	at ch.qos.logback.core.joran.GenericConfigurator.doConfigure(GenericConfigurator.java:53)
	at 	at ch.qos.logback.classic.util.ContextInitializer.configureByResource(ContextInitializer.java:75)
	at 	at ch.qos.logback.classic.util.ContextInitializer.autoConfig(ContextInitializer.java:150)
	at 	at org.slf4j.impl.StaticLoggerBinder.init(StaticLoggerBinder.java:84)
	at 	at org.slf4j.impl.StaticLoggerBinder.<clinit>(StaticLoggerBinder.java:55)
	at 	at org.slf4j.LoggerFactory.bind(LoggerFactory.java:150)
	at 	at org.slf4j.LoggerFactory.performInitialization(LoggerFactory.java:124)
	at 	at org.slf4j.LoggerFactory.getILoggerFactory(LoggerFactory.java:412)
	at 	at ch.qos.logback.classic.util.StatusViaSLF4JLoggerFactory.addStatus(StatusViaSLF4JLoggerFactory.java:32)
	at 	at ch.qos.logback.classic.util.StatusViaSLF4JLoggerFactory.addInfo(StatusViaSLF4JLoggerFactory.java:20)
	at 	at ch.qos.logback.classic.servlet.LogbackServletContainerInitializer.onStartup(LogbackServletContainerInitializer.java:32)
	at 	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5139)
	at 	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:183)
	at 	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1377)
	at 	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1367)
	at 	at java.util.concurrent.FutureTask.run(Unknown Source)
	at 	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$201(Unknown Source)
	at 	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(Unknown Source)
	at 	at java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
	at 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
	at 	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
	at 	at java.lang.Thread.run(Unknown Source)
09:24:03,384 |-INFO in ch.qos.logback.classic.joran.action.LoggerAction - Setting level of logger [com.atlassian.synchrony] to WARN
09:24:03,384 |-INFO in ch.qos.logback.classic.joran.action.LoggerAction - Setting additivity of logger [com.atlassian.synchrony] to false
09:24:03,385 |-INFO in ch.qos.logback.core.joran.action.AppenderRefAction - Attaching appender named [synchronyProxyLogAppender] to Logger[com.atlassian.synchrony]
09:24:03,385 |-INFO in ch.qos.logback.classic.joran.action.LoggerAction - Setting level of logger [org.springframework.web] to WARN
09:24:03,385 |-INFO in ch.qos.logback.classic.joran.action.LoggerAction - Setting additivity of logger [org.springframework.web] to false
09:24:03,388 |-INFO in ch.qos.logback.core.joran.action.AppenderRefAction - Attaching appender named [synchronyProxyLogAppender] to Logger[org.springframework.web]
09:24:03,388 |-INFO in ch.qos.logback.classic.joran.action.LoggerAction - Setting level of logger [org.springframework.web.socket] to WARN
09:24:03,388 |-INFO in ch.qos.logback.classic.joran.action.LoggerAction - Setting additivity of logger [org.springframework.web.socket] to false
09:24:03,388 |-INFO in ch.qos.logback.core.joran.action.AppenderRefAction - Attaching appender named [synchronyProxyLogAppender] to Logger[org.springframework.web.socket]
09:24:03,388 |-INFO in ch.qos.logback.classic.joran.action.RootLoggerAction - Setting level of ROOT logger to WARN
09:24:03,388 |-INFO in ch.qos.logback.core.joran.action.AppenderRefAction - Attaching appender named [console] to Logger[ROOT]
09:24:03,388 |-INFO in ch.qos.logback.classic.joran.action.ConfigurationAction - End of configuration.
09:24:03,389 |-INFO in ch.qos.logback.classic.joran.JoranConfigurator@68f05bac - Registering current configuration as safe fallback point

03-Jun-2019 09:24:03.407 INFO [Catalina-utility-2] org.apache.catalina.core.ApplicationContext.log Spring WebApplicationInitializers detected on classpath: [com.atlassian.synchrony.proxy.SynchronyDispatcherServletInitializer@1e158ec6]
03-Jun-2019 09:24:03.473 INFO [Catalina-utility-2] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
03-Jun-2019 09:24:03.731 INFO [Catalina-utility-2] org.apache.catalina.core.ApplicationContext.log Initializing Spring FrameworkServlet 'dispatcher'
03-Jun-2019 09:24:03.731 INFO [Catalina-utility-2] org.springframework.web.servlet.DispatcherServlet.initServletBean FrameworkServlet 'dispatcher': initialization started
03-Jun-2019 09:24:03.734 INFO [Catalina-utility-2] org.springframework.web.context.support.AnnotationConfigWebApplicationContext.prepareRefresh Refreshing WebApplicationContext for namespace 'dispatcher-servlet': startup date [Mon Jun 03 09:24:03 GMT 2019]; root of context hierarchy
03-Jun-2019 09:24:03.839 INFO [Catalina-utility-2] org.springframework.web.context.support.AnnotationConfigWebApplicationContext.loadBeanDefinitions Registering annotated classes: [class com.atlassian.synchrony.proxy.websocket.WebSocketConfig,class com.atlassian.synchrony.proxy.web.SynchronyWebMvcConfig]
2019-06-03 09:24:04,207 INFO [Catalina-utility-1] [com.atlassian.confluence.lifecycle] contextInitialized Starting Confluence 6.15.4 [build 8100 based on commit hash b0984b7297905b7c7bd946458f753ce0130bfc8c] - synchrony version 2.1.0-master-9d112c9d
03-Jun-2019 09:24:04.411 INFO [Catalina-utility-2] org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler.initialize Initializing ExecutorService  'defaultSockJsTaskScheduler'
03-Jun-2019 09:24:04.471 INFO [Catalina-utility-2] org.springframework.web.socket.server.support.WebSocketHandlerMapping.registerHandler Mapped URL path [/v1/bayeux-sync1] onto handler of type [class org.springframework.web.socket.server.support.WebSocketHttpRequestHandler]
03-Jun-2019 09:24:05.364 INFO [Catalina-utility-2] org.springframework.web.servlet.handler.SimpleUrlHandlerMapping.registerHandler Mapped URL path [/**] onto handler of type [class org.springframework.web.servlet.resource.DefaultServletHttpRequestHandler]
03-Jun-2019 09:24:05.407 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.initControllerAdviceCache Looking for @ControllerAdvice: WebApplicationContext for namespace 'dispatcher-servlet': startup date [Mon Jun 03 09:24:03 GMT 2019]; root of context hierarchy
03-Jun-2019 09:24:05.496 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping.register Mapped "{[/healthcheck]}" onto public com.atlassian.synchrony.proxy.web.HealthCheckResult com.atlassian.synchrony.proxy.web.SynchronyProxyRestController.getSynchronyProxyInfo()
03-Jun-2019 09:24:05.500 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping.register Mapped "{[/reload],methods=[PUT]}" onto public org.springframework.http.ResponseEntity com.atlassian.synchrony.proxy.web.SynchronyProxyRestController.reloadConfiguration(com.atlassian.synchrony.proxy.web.SynchronyProxyConfigPayload)
03-Jun-2019 09:24:05.621 INFO [Catalina-utility-2] org.springframework.context.support.DefaultLifecycleProcessor.start Starting beans in phase 2147483647
03-Jun-2019 09:24:05.653 INFO [Catalina-utility-2] org.springframework.web.servlet.DispatcherServlet.initServletBean FrameworkServlet 'dispatcher': initialization completed in 1922 ms
03-Jun-2019 09:24:05.655 SEVERE [Catalina-utility-2] org.apache.jasper.EmbeddedServletOptions.<init> The scratchDir you specified: [/opt/atlassian/confluence/work/Standalone/localhost/synchrony-proxy] is unusable.
2019-06-03 09:24:07,620 ERROR [Catalina-utility-1] [confluence.impl.health.DefaultHealthCheckRunner] logEvent We can't locate your Confluence home directory.
2019-06-03 09:24:07,623 ERROR [Catalina-utility-1] [confluence.impl.health.DefaultHealthCheckRunner] logEvent You'll need to specify a home directory. Confluence can't start without this.
See our documentation for more information on setting your home directory.
2019-06-03 09:24:07,624 WARN [Catalina-utility-1] [atlassian.config.bootstrap.DefaultAtlassianBootstrapManager] init Unable to set up application config: no home set
03-Jun-2019 09:24:08.456 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8090"]
03-Jun-2019 09:24:08.478 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [6,572] milliseconds
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 

http://10.5.106.26:8090/

错误分析：
显示无法在 /opt/atlassian/confluence/logs 目录中写入日志，权限不够，而 /opt/atlassian/confluence/logs 是挂载在宿主机的 /root/work/confluence/docker_data/confluence_install/logs 上，因此将宿主机目录修改为最大权限 777

[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root root   6 Jun  3 17:35 confluence_home
drwxr-xr-x 12 1000 1000 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chown -R daemon:daemon confluence_install/
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chmod -R 777 confluence_install/logs/
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_home/
total 0
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_install/  # 从 atlassian-confluence-6.15.4.tar.gz 解压而来
total 204
drwxr-xr-x  3 daemon daemon  4096 Jun  3 17:34 bin
-rw-r--r--  1 daemon daemon 19743 Apr 12 23:24 BUILDING.txt
drwxr-xr-x  3 daemon daemon   256 Jun  3 17:34 conf
drwxr-xr-x 27 daemon daemon  4096 Jun  3 17:34 confluence
-rw-r--r--  1 daemon daemon  5543 Apr 12 23:24 CONTRIBUTING.md
drwxr-xr-x  2 daemon daemon  4096 Jun  3 17:34 lib
-rw-r--r--  1 daemon daemon 58153 Apr 12 23:24 LICENSE
drwxr-xr-x  2 daemon daemon 45056 Jun  3 17:34 licenses
drwxrwxrwx  2 daemon daemon     6 Apr 12 23:22 logs
-rw-r--r--  1 daemon daemon  2401 Apr 12 23:24 NOTICE
-rw-r--r--  1 daemon daemon  2294 May  8 11:09 README.html
-rw-r--r--  1 daemon daemon  3334 Apr 12 23:24 README.md
-rw-r--r--  1 daemon daemon  1204 May  8 11:09 README.txt
-rw-r--r--  1 daemon daemon  7025 Apr 12 23:24 RELEASE-NOTES
-rw-r--r--  1 daemon daemon 16738 Apr 12 23:24 RUNNING.txt
drwxr-xr-x  4 daemon daemon    37 Jun  3 17:34 synchrony-proxy
drwxr-xr-x  2 daemon daemon    30 Jun  3 17:34 temp
drwxr-xr-x  2 daemon daemon     6 May  8 11:10 webapps
drwxr-xr-x  2 daemon daemon     6 Apr 12 23:22 work
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_install/logs/
total 0
[root@lanzhiwang-centos7 docker_data]# 

[root@lanzhiwang-centos7 docker_data]# docker run -v /root/work/confluence/docker_data/confluence_home:/var/atlassian/application-data/confluence -v /root/work/confluence/docker_data/confluence_install:/opt/atlassian/confluence --name="confluence" -d -p 8090:8090 -p 8091:8091 atlassian/confluence-server
6493ffb38df891db48613f325be0d21e6e2ee96d44309d45c1eec1fe734c8005
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
6493ffb38df8        atlassian/confluence-server   "/tini -- /entrypoin…"   5 seconds ago       Up 5 seconds        0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
6493ffb38df8        atlassian/confluence-server   "/tini -- /entrypoin…"   11 seconds ago      Up 10 seconds       0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
6493ffb38df8        atlassian/confluence-server   "/tini -- /entrypoin…"   12 seconds ago      Up 11 seconds       0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker logs 6493ffb38df8
User is currently root. Will change directory ownership to daemon:daemon, then downgrade permission to daemon
executing as current user
If you encounter issues starting up Confluence, please see the Installation guide at http://confluence.atlassian.com/display/DOC/Confluence+Installation+Guide

Server startup logs are located in /opt/atlassian/confluence/logs/catalina.out
---------------------------------------------------------------------------
Using Java: /opt/java/openjdk/bin/java
2019-06-03 09:37:58,269 INFO [main] [atlassian.confluence.bootstrap.SynchronyProxyWatchdog] A Context element for ${confluence.context.path}/synchrony-proxy is found in /opt/atlassian/confluence/conf/server.xml. No further action is required
---------------------------------------------------------------------------
03-Jun-2019 09:37:58.694 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server] failed to set property [debug] to [0]
03-Jun-2019 09:37:58.743 WARNING [main] org.apache.catalina.startup.SetAllPropertiesRule.begin [SetAllPropertiesRule]{Server/Service/Connector} Setting property 'debug' to '0' did not find a matching property.
03-Jun-2019 09:37:58.759 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine] failed to set property [debug] to [0]
03-Jun-2019 09:37:58.763 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host] failed to set property [debug] to [0]
03-Jun-2019 09:37:58.790 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host/Context] failed to set property [debug] to [0]
03-Jun-2019 09:37:58.805 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host/Context] failed to set property [debug] to [0]
03-Jun-2019 09:37:59.083 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8090"]
03-Jun-2019 09:37:59.115 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [495] milliseconds
03-Jun-2019 09:37:59.122 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Tomcat-Standalone]
03-Jun-2019 09:37:59.122 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.19]
03-Jun-2019 09:37:59.149 WARNING [Catalina-utility-1] org.apache.catalina.core.StandardContext.postWorkDirectory Failed to create work directory [/opt/atlassian/confluence/work/Standalone/localhost/ROOT] for context []
03-Jun-2019 09:37:59.160 WARNING [Catalina-utility-2] org.apache.catalina.core.StandardContext.postWorkDirectory Failed to create work directory [/opt/atlassian/confluence/work/Standalone/localhost/synchrony-proxy] for context [/synchrony-proxy]
03-Jun-2019 09:38:00.820 INFO [Catalina-utility-2] org.apache.catalina.core.ApplicationContext.log Spring WebApplicationInitializers detected on classpath: [com.atlassian.synchrony.proxy.SynchronyDispatcherServletInitializer@79c40942]
03-Jun-2019 09:38:00.913 INFO [Catalina-utility-2] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
03-Jun-2019 09:38:01.285 INFO [Catalina-utility-2] org.apache.catalina.core.ApplicationContext.log Initializing Spring FrameworkServlet 'dispatcher'
03-Jun-2019 09:38:01.285 INFO [Catalina-utility-2] org.springframework.web.servlet.DispatcherServlet.initServletBean FrameworkServlet 'dispatcher': initialization started
03-Jun-2019 09:38:01.288 INFO [Catalina-utility-2] org.springframework.web.context.support.AnnotationConfigWebApplicationContext.prepareRefresh Refreshing WebApplicationContext for namespace 'dispatcher-servlet': startup date [Mon Jun 03 09:38:01 GMT 2019]; root of context hierarchy
03-Jun-2019 09:38:01.355 INFO [Catalina-utility-2] org.springframework.web.context.support.AnnotationConfigWebApplicationContext.loadBeanDefinitions Registering annotated classes: [class com.atlassian.synchrony.proxy.websocket.WebSocketConfig,class com.atlassian.synchrony.proxy.web.SynchronyWebMvcConfig]
2019-06-03 09:38:01,513 INFO [Catalina-utility-1] [com.atlassian.confluence.lifecycle] contextInitialized Starting Confluence 6.15.4 [build 8100 based on commit hash b0984b7297905b7c7bd946458f753ce0130bfc8c] - synchrony version 2.1.0-master-9d112c9d
03-Jun-2019 09:38:01.805 INFO [Catalina-utility-2] org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler.initialize Initializing ExecutorService  'defaultSockJsTaskScheduler'
03-Jun-2019 09:38:01.852 INFO [Catalina-utility-2] org.springframework.web.socket.server.support.WebSocketHandlerMapping.registerHandler Mapped URL path [/v1/bayeux-sync1] onto handler of type [class org.springframework.web.socket.server.support.WebSocketHttpRequestHandler]
03-Jun-2019 09:38:02.553 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.initControllerAdviceCache Looking for @ControllerAdvice: WebApplicationContext for namespace 'dispatcher-servlet': startup date [Mon Jun 03 09:38:01 GMT 2019]; root of context hierarchy
03-Jun-2019 09:38:02.670 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping.register Mapped "{[/healthcheck]}" onto public com.atlassian.synchrony.proxy.web.HealthCheckResult com.atlassian.synchrony.proxy.web.SynchronyProxyRestController.getSynchronyProxyInfo()
03-Jun-2019 09:38:02.671 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping.register Mapped "{[/reload],methods=[PUT]}" onto public org.springframework.http.ResponseEntity com.atlassian.synchrony.proxy.web.SynchronyProxyRestController.reloadConfiguration(com.atlassian.synchrony.proxy.web.SynchronyProxyConfigPayload)
03-Jun-2019 09:38:02.701 INFO [Catalina-utility-2] org.springframework.web.servlet.handler.SimpleUrlHandlerMapping.registerHandler Mapped URL path [/**] onto handler of type [class org.springframework.web.servlet.resource.DefaultServletHttpRequestHandler]
03-Jun-2019 09:38:02.859 INFO [Catalina-utility-2] org.springframework.context.support.DefaultLifecycleProcessor.start Starting beans in phase 2147483647
03-Jun-2019 09:38:02.943 INFO [Catalina-utility-2] org.springframework.web.servlet.DispatcherServlet.initServletBean FrameworkServlet 'dispatcher': initialization completed in 1633 ms
03-Jun-2019 09:38:02.945 SEVERE [Catalina-utility-2] org.apache.jasper.EmbeddedServletOptions.<init> The scratchDir you specified: [/opt/atlassian/confluence/work/Standalone/localhost/synchrony-proxy] is unusable.
2019-06-03 09:38:04,904 ERROR [Catalina-utility-1] [confluence.impl.health.DefaultHealthCheckRunner] logEvent We can't locate your Confluence home directory.
2019-06-03 09:38:04,907 ERROR [Catalina-utility-1] [confluence.impl.health.DefaultHealthCheckRunner] logEvent You'll need to specify a home directory. Confluence can't start without this.
See our documentation for more information on setting your home directory.
2019-06-03 09:38:04,908 WARN [Catalina-utility-1] [atlassian.config.bootstrap.DefaultAtlassianBootstrapManager] init Unable to set up application config: no home set
03-Jun-2019 09:38:05.943 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8090"]
03-Jun-2019 09:38:05.970 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [6,854] milliseconds
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
6493ffb38df8        atlassian/confluence-server   "/tini -- /entrypoin…"   3 minutes ago       Up 3 minutes        0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
6493ffb38df8        atlassian/confluence-server   "/tini -- /entrypoin…"   3 minutes ago       Up 3 minutes        0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 


错误分析：
修改 /root/work/confluence/docker_data/confluence_install/confluence/WEB-INF/classes/confluence-init.properties 配置文件 confluence.home=/var/atlassian/application-data/confluence/

[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root root   6 Jun  3 18:54 confluence_home
drwxr-xr-x 12 1000 1000 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chown -R daemon:daemon confluence_install/
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chmod -R 777 confluence_install/logs/
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root   root     6 Jun  3 18:54 confluence_home
drwxr-xr-x 12 daemon daemon 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# vim confluence_install/confluence/WEB-INF/classes/confluence-init.properties
[root@lanzhiwang-centos7 docker_data]# cat confluence_install/confluence/WEB-INF/classes/confluence-init.properties
# This file allows you to set the directory for Confluence to store its configuration files.
#
###########################
# Note for Windows Users  #
###########################
#
# Each backslash in your path must be written as a forward slash.
# - For example:
# c:\confluence\data
#
# should be written as:
#
# c:/confluence/data

###########################
# Note for Unix Users     #
###########################
# - For example:
# confluence.home=/var/confluence
#
# NOTE: If the path of your confluence.home directory contains symlinks,
# please set confluence.home to the absolute path, otherwise problems may occur.
# - For example:
# confluence.home=/data/confluence/ (where /data is a symlink to -> /var/data/)
# should be written as:
# confluence.home=/var/data/confluence/
confluence.home=/var/atlassian/application-data/confluence/

###########################
# Configuration Directory #
###########################

# specify your directory below (don't forget to remove the '#' in front)

# confluence.home=c:/confluence/data
[root@lanzhiwang-centos7 docker_data]# 

[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root root   6 Jun  3 18:54 confluence_home
drwxr-xr-x 12 1000 1000 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chown -R daemon:daemon confluence_install/
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chmod -R 777 confluence_install/logs/
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker run -v /root/work/confluence/docker_data/confluence_home:/var/atlassian/application-data/confluence -v /root/work/confluence/docker_data/confluence_install:/opt/atlassian/confluence --name="confluence" -d -p 8090:8090 -p 8091:8091 atlassian/confluence-server
0081a963bfc5776fbdafc69ce51327380e24995dd07b22a3b89dbff420481652
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
0081a963bfc5        atlassian/confluence-server   "/tini -- /entrypoin…"   7 seconds ago       Up 6 seconds        0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker logs 0081a963bfc5


http://10.5.106.26:8090


还是有错误。错误分析：
在启动容器后再修改配置文件 confluence_install/confluence/WEB-INF/classes/confluence-init.properties，不能提前修改

[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root root   6 Jun  3 19:06 confluence_home
drwxr-xr-x 12 1000 1000 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# chown -R daemon:daemon confluence_install/
[root@lanzhiwang-centos7 docker_data]# chmod -R 777 confluence_install/logs/
[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwxr-xr-x  2 root   root     6 Jun  3 19:06 confluence_home
drwxr-xr-x 12 daemon daemon 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# vim confluence_install/confluence/WEB-INF/classes/confluence-init.properties
[root@lanzhiwang-centos7 docker_data]# cat confluence_install/confluence/WEB-INF/classes/confluence-init.properties
# This file allows you to set the directory for Confluence to store its configuration files.
#
###########################
# Note for Windows Users  #
###########################
#
# Each backslash in your path must be written as a forward slash.
# - For example:
# c:\confluence\data
#
# should be written as:
#
# c:/confluence/data

###########################
# Note for Unix Users     #
###########################
# - For example:
# confluence.home=/var/confluence
#
# NOTE: If the path of your confluence.home directory contains symlinks,
# please set confluence.home to the absolute path, otherwise problems may occur.
# - For example:
# confluence.home=/data/confluence/ (where /data is a symlink to -> /var/data/)
# should be written as:
# confluence.home=/var/data/confluence/
confluence.home=/var/atlassian/application-data/confluence/

###########################
# Configuration Directory #
###########################

# specify your directory below (don't forget to remove the '#' in front)

# confluence.home=c:/confluence/data
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED              STATUS              PORTS                              NAMES
a76d26601b72        atlassian/confluence-server   "/tini -- /entrypoin…"   About a minute ago   Up About a minute   0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker restart a76d26601b72
a76d26601b72
[root@lanzhiwang-centos7 docker_data]# chmod -R 777 confluence_install/  # 要将整个 confluence_install 目录设置为最大权限
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker restart a76d26601b72
a76d26601b72
[root@lanzhiwang-centos7 docker_data]# 

总结：
1、将 atlassian-confluence-6.15.4.tar.gz 解压到 confluence_install 目录中
2、容器启动后修改配置文件 confluence_install/confluence/WEB-INF/classes/confluence-init.properties

/root/work/confluence/docker_data/confluence_install:/opt/atlassian/confluence

Confluence 需要一个驱动程序以连接到 MySQL 。 您将需要：

下载 MySQL驱动程序  # https://confluence.atlassian.com/doc/database-jdbc-drivers-171742.html  mysql-connector-java-5.1.47.tar.gz
将 .jar 文件放入 /opt/atlassian/confluence/confluence/WEB-INF/lib
重启 Confluence 并继续安装过程。
    
mysql 驱动安装目录
/opt/atlassian/confluence /confluence/WEB-INF/lib/
/root/work/confluence/docker_data/confluence_install /confluence/WEB-INF/lib/

添加驱动后要重启容器

也需要提前创建数据库 CREATE DATABASE confluence CHARACTER SET utf8 COLLATE utf8_bin;

rootpassword



```

### 在 k8s 上部署 confluence

```bash
[root@k8s-master1 temp]# vim ./confluence.yml
[root@k8s-master1 temp]# cat ./confluence.yml
---
apiVersion: v1
kind: Service
metadata:
  name: confluence
  labels:
    app: confluence
spec:
  ports:
  - name: http
    port: 8090
    targetPort: 8090
    protocol: TCP
  selector:
    app: confluence
    service: confluence
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: confluence-deployment
  labels:
    service: confluence
    app: confluence

spec:
  replicas: 1
  selector:
    matchLabels:
      app: confluence
      service: confluence
  template:
    metadata:
      labels:
        app: confluence
        service: confluence
    spec:
      containers:
        - name: confluence
          image: atlassian/confluence-server:latest
          imagePullPolicy: Always
          env:
            - name: JVM_MINIMUM_MEMORY
              value: 2048m
            - name: JVM_MAXIMUM_MEMORY
              value: 2048m
          ports:
            - containerPort: 8090

          volumeMounts:
          - name: confluence_home
            mountPath: /var/atlassian/application-data/confluence
          - name: confluence_install
            mountPath: /opt/atlassian/confluence

      volumes:
        - name: confluence_home
          hostPath:
            path: /opt/k8s/volume_data/confluence_home/
        - name: confluence_install
          hostPath:
            path: /opt/k8s/volume_data/confluence_install/

[root@k8s-master1 temp]# kubectl apply -f ./confluence.yml
service/confluence unchanged
The Deployment "confluence-deployment" is invalid: 
* spec.template.spec.volumes[0].name: Invalid value: "confluence_home": a DNS-1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')
* spec.template.spec.volumes[1].name: Invalid value: "confluence_install": a DNS-1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')
* spec.template.spec.containers[0].volumeMounts[0].name: Not found: "confluence_home"
* spec.template.spec.containers[0].volumeMounts[1].name: Not found: "confluence_install"
[root@k8s-master1 temp]# 

错误分析：
confluence_home 和 confluence_install 不能使用下划线，要使用中划线 confluence-home 和 confluence-install

[root@k8s-master1 temp]# vim  ./confluence.yml
[root@k8s-master1 temp]# cat  ./confluence.yml
---
apiVersion: v1
kind: Service
metadata:
  name: confluence
  labels:
    app: confluence
spec:
  ports:
  - name: http
    port: 8090
    targetPort: 8090
    protocol: TCP
  selector:
    app: confluence
    service: confluence
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: confluence-deployment
  labels:
    service: confluence
    app: confluence

spec:
  replicas: 1
  selector:
    matchLabels:
      app: confluence
      service: confluence
  template:
    metadata:
      labels:
        app: confluence
        service: confluence
    spec:
      containers:
        - name: confluence
          image: atlassian/confluence-server:latest
          imagePullPolicy: Always
          env:
            - name: JVM_MINIMUM_MEMORY
              value: 2048m
            - name: JVM_MAXIMUM_MEMORY
              value: 2048m
          ports:
            - containerPort: 8090

          volumeMounts:
          - name: confluence-home
            mountPath: /var/atlassian/application-data/confluence
          - name: confluence-install
            mountPath: /opt/atlassian/confluence

      volumes:
        - name: confluence-home
          hostPath:
            path: /opt/k8s/volume_data/confluence_home/
        - name: confluence-install
          hostPath:
            path: /opt/k8s/volume_data/confluence_install/

[root@k8s-master1 temp]# kubectl apply -f ./confluence.yml
service/confluence unchanged
deployment.apps/confluence-deployment created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                               SELECTOR
confluence-deployment   1/1     1            1           36s     confluence   atlassian/confluence-server:latest   app=confluence,service=confluence
confluence-mysql        1/1     1            1           4d18h   mysql        mysql/mysql-server:5.7               app=confluence,tier=mysql
my-nginx                8/8     8            8           5d23h   my-nginx     nginx                                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS             RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-7577774698-psgz2   1/1     Running            0          54s     172.20.0.17   10.1.36.46   <none>           <none>
confluence-mysql-d464855bd-9ckm9         1/1     Running            7          4d18h   172.20.0.15   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running            0          5d23h   172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running            0          5d23h   172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running            0          5d23h   172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running            0          5d23h   172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running            0          5d23h   172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running            0          5d23h   172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running            0          5d23h   172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running            0          5d23h   172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     CrashLoopBackOff   1024       3d23h   172.20.3.8    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl describe pod confluence-deployment-7577774698-psgz2
Name:           confluence-deployment-7577774698-psgz2
Namespace:      default
Node:           10.1.36.46/10.1.36.46
Start Time:     Tue, 04 Jun 2019 09:56:42 +0800
Labels:         app=confluence
                pod-template-hash=7577774698
                service=confluence
Annotations:    <none>
Status:         Running
IP:             172.20.0.17
Controlled By:  ReplicaSet/confluence-deployment-7577774698
Containers:
  confluence:
    Container ID:   docker://19120f7d60eeda1bdc3a037bc5bd7b1d87d31b3324a05ad974cc91b2cf04c821
    Image:          atlassian/confluence-server:latest
    Image ID:       docker-pullable://atlassian/confluence-server@sha256:2b8513e2fc80990c9ca8d0c69fef1ce8a2ff33658a01a42dc98a853b28ea39d7
    Port:           8090/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Tue, 04 Jun 2019 09:56:46 +0800
    Ready:          True
    Restart Count:  0
    Environment:
      JVM_MINIMUM_MEMORY:  2048m
      JVM_MAXIMUM_MEMORY:  2048m
    Mounts:
      /opt/atlassian/confluence from confluence-install (rw)
      /var/atlassian/application-data/confluence from confluence-home (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-lz2dc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  confluence-home:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/k8s/volume_data/confluence_home/
    HostPathType:  
  confluence-install:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/k8s/volume_data/confluence_install/
    HostPathType:  
  default-token-lz2dc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-lz2dc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     <none>
Events:
  Type    Reason     Age   From                 Message
  ----    ------     ----  ----                 -------
  Normal  Scheduled  2m8s  default-scheduler    Successfully assigned default/confluence-deployment-7577774698-psgz2 to 10.1.36.46
  Normal  Pulling    2m7s  kubelet, 10.1.36.46  Pulling image "atlassian/confluence-server:latest"
  Normal  Pulled     2m4s  kubelet, 10.1.36.46  Successfully pulled image "atlassian/confluence-server:latest"
  Normal  Created    2m4s  kubelet, 10.1.36.46  Created container confluence
  Normal  Started    2m4s  kubelet, 10.1.36.46  Started container confluence
[root@k8s-master1 temp]# 

[root@k8s-linux-worker1 volume_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS                  PORTS               NAMES
19120f7d60ee        atlassian/confluence-server   "/tini -- /entrypoin…"   4 minutes ago       Up 4 minutes                                k8s_confluence_confluence-deployment-7577774698-psgz2_default_ffd2c5df-866b-11e9-8f1f-0017fa00a076_0
b4a031e2564c        k8s.gcr.io/pause:3.1          "/pause"                 4 minutes ago       Up 4 minutes                                k8s_POD_confluence-deployment-7577774698-psgz2_default_ffd2c5df-866b-11e9-8f1f-0017fa00a076_0
cd4ad9dabcd9        ff281650a721                  "cp -f /etc/kube-fla…"   4 days ago          Exited (0) 4 days ago                       k8s_install-cni_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_0
516e95531598        857eadf53a54                  "/entrypoint.sh mysq…"   4 days ago          Up 4 days                                   k8s_mysql_confluence-mysql-d464855bd-9ckm9_default_fc148672-82ae-11e9-8f1f-0017fa00a076_7
e442817adadf        k8s.gcr.io/pause:3.1          "/pause"                 4 days ago          Up 4 days                                   k8s_POD_confluence-mysql-d464855bd-9ckm9_default_fc148672-82ae-11e9-8f1f-0017fa00a076_0
ff2443f44b3a        nginx                         "nginx -g 'daemon of…"   5 days ago          Up 5 days                                   k8s_my-nginx_my-nginx-86459cfc9f-qwclj_default_e5ff59c0-81ba-11e9-8f1f-0017fa00a076_0
01083b94ed24        nginx                         "nginx -g 'daemon of…"   5 days ago          Up 5 days                                   k8s_my-nginx_my-nginx-86459cfc9f-qhjww_default_e5ff0ba3-81ba-11e9-8f1f-0017fa00a076_0
3b01b7d98e57        k8s.gcr.io/pause:3.1          "/pause"                 5 days ago          Up 5 days                                   k8s_POD_my-nginx-86459cfc9f-qwclj_default_e5ff59c0-81ba-11e9-8f1f-0017fa00a076_0
c12093c6eb0e        k8s.gcr.io/pause:3.1          "/pause"                 5 days ago          Up 5 days                                   k8s_POD_my-nginx-86459cfc9f-qhjww_default_e5ff0ba3-81ba-11e9-8f1f-0017fa00a076_0
6d2174182b5d        f9aed6605b81                  "/dashboard --insecu…"   6 days ago          Up 6 days                                   k8s_kubernetes-dashboard_kubernetes-dashboard-5f7b999d65-sw96f_kube-system_62c2ea91-810f-11e9-8f1f-0017fa00a076_0
2938cb474079        ff281650a721                  "/opt/bin/flanneld -…"   6 days ago          Up 6 days                                   k8s_kube-flannel_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_4
975e00897c33        k8s.gcr.io/pause:3.1          "/pause"                 6 days ago          Up 6 days                                   k8s_POD_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_4
f2a933f2127f        k8s.gcr.io/pause:3.1          "/pause"                 6 days ago          Up 6 days                                   k8s_POD_kubernetes-dashboard-5f7b999d65-sw96f_kube-system_62c2ea91-810f-11e9-8f1f-0017fa00a076_3
[root@k8s-linux-worker1 volume_data]# 
[root@k8s-linux-worker1 volume_data]# docker logs 19120f7d60ee
User is currently root. Will change directory ownership to daemon:daemon, then downgrade permission to daemon
executing as current user
If you encounter issues starting up Confluence, please see the Installation guide at http://confluence.atlassian.com/display/DOC/Confluence+Installation+Guide

Server startup logs are located in /opt/atlassian/confluence/logs/catalina.out
---------------------------------------------------------------------------
Using Java: /opt/java/openjdk/bin/java
2019-06-04 01:56:47,498 INFO [main] [atlassian.confluence.bootstrap.SynchronyProxyWatchdog] A Context element for ${confluence.context.path}/synchrony-proxy is found in /opt/atlassian/confluence/conf/server.xml. No further action is required
---------------------------------------------------------------------------
04-Jun-2019 01:56:48.022 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server] failed to set property [debug] to [0]
04-Jun-2019 01:56:48.094 WARNING [main] org.apache.catalina.startup.SetAllPropertiesRule.begin [SetAllPropertiesRule]{Server/Service/Connector} Setting property 'debug' to '0' did not find a matching property.
04-Jun-2019 01:56:48.115 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine] failed to set property [debug] to [0]
04-Jun-2019 01:56:48.121 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host] failed to set property [debug] to [0]
04-Jun-2019 01:56:48.159 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host/Context] failed to set property [debug] to [0]
04-Jun-2019 01:56:48.182 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Engine/Host/Context] failed to set property [debug] to [0]
04-Jun-2019 01:56:48.514 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8090"]
04-Jun-2019 01:56:48.553 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [642] milliseconds
04-Jun-2019 01:56:48.562 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Tomcat-Standalone]
04-Jun-2019 01:56:48.562 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.19]
04-Jun-2019 01:56:50.477 INFO [Catalina-utility-2] org.apache.catalina.core.ApplicationContext.log Spring WebApplicationInitializers detected on classpath: [com.atlassian.synchrony.proxy.SynchronyDispatcherServletInitializer@61a170e6]
04-Jun-2019 01:56:50.619 INFO [Catalina-utility-2] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
2019-06-04 01:56:50,832 INFO [Catalina-utility-1] [com.atlassian.confluence.lifecycle] contextInitialized Starting Confluence 6.15.4 [build 8100 based on commit hash b0984b7297905b7c7bd946458f753ce0130bfc8c] - synchrony version 2.1.0-master-9d112c9d
04-Jun-2019 01:56:50.880 INFO [Catalina-utility-2] org.apache.catalina.core.ApplicationContext.log Initializing Spring FrameworkServlet 'dispatcher'
04-Jun-2019 01:56:50.880 INFO [Catalina-utility-2] org.springframework.web.servlet.DispatcherServlet.initServletBean FrameworkServlet 'dispatcher': initialization started
04-Jun-2019 01:56:50.887 INFO [Catalina-utility-2] org.springframework.web.context.support.AnnotationConfigWebApplicationContext.prepareRefresh Refreshing WebApplicationContext for namespace 'dispatcher-servlet': startup date [Tue Jun 04 01:56:50 GMT 2019]; root of context hierarchy
04-Jun-2019 01:56:50.969 INFO [Catalina-utility-2] org.springframework.web.context.support.AnnotationConfigWebApplicationContext.loadBeanDefinitions Registering annotated classes: [class com.atlassian.synchrony.proxy.websocket.WebSocketConfig,class com.atlassian.synchrony.proxy.web.SynchronyWebMvcConfig]
04-Jun-2019 01:56:51.523 INFO [Catalina-utility-2] org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler.initialize Initializing ExecutorService  'defaultSockJsTaskScheduler'
04-Jun-2019 01:56:51.579 INFO [Catalina-utility-2] org.springframework.web.socket.server.support.WebSocketHandlerMapping.registerHandler Mapped URL path [/v1/bayeux-sync1] onto handler of type [class org.springframework.web.socket.server.support.WebSocketHttpRequestHandler]
04-Jun-2019 01:56:52.209 INFO [Catalina-utility-2] org.springframework.web.servlet.handler.SimpleUrlHandlerMapping.registerHandler Mapped URL path [/**] onto handler of type [class org.springframework.web.servlet.resource.DefaultServletHttpRequestHandler]
04-Jun-2019 01:56:52.257 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.initControllerAdviceCache Looking for @ControllerAdvice: WebApplicationContext for namespace 'dispatcher-servlet': startup date [Tue Jun 04 01:56:50 GMT 2019]; root of context hierarchy
04-Jun-2019 01:56:52.361 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping.register Mapped "{[/healthcheck]}" onto public com.atlassian.synchrony.proxy.web.HealthCheckResult com.atlassian.synchrony.proxy.web.SynchronyProxyRestController.getSynchronyProxyInfo()
04-Jun-2019 01:56:52.362 INFO [Catalina-utility-2] org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping.register Mapped "{[/reload],methods=[PUT]}" onto public org.springframework.http.ResponseEntity com.atlassian.synchrony.proxy.web.SynchronyProxyRestController.reloadConfiguration(com.atlassian.synchrony.proxy.web.SynchronyProxyConfigPayload)
04-Jun-2019 01:56:52.443 INFO [Catalina-utility-2] org.springframework.context.support.DefaultLifecycleProcessor.start Starting beans in phase 2147483647
04-Jun-2019 01:56:52.475 INFO [Catalina-utility-2] org.springframework.web.servlet.DispatcherServlet.initServletBean FrameworkServlet 'dispatcher': initialization completed in 1595 ms
2019-06-04 01:56:55,009 ERROR [Catalina-utility-1] [confluence.impl.health.DefaultHealthCheckRunner] logEvent We can't locate your Confluence home directory.
2019-06-04 01:56:55,015 ERROR [Catalina-utility-1] [confluence.impl.health.DefaultHealthCheckRunner] logEvent You'll need to specify a home directory. Confluence can't start without this.
See our documentation for more information on setting your home directory.
2019-06-04 01:56:55,017 WARN [Catalina-utility-1] [atlassian.config.bootstrap.DefaultAtlassianBootstrapManager] init Unable to set up application config: no home set
04-Jun-2019 01:57:04.330 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8090"]
04-Jun-2019 01:57:04.344 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [15,789] milliseconds
[root@k8s-linux-worker1 volume_data]# 


错误分析：
检查 docker 容器本身还是有错误，没有配置 Confluence home directory，所以在配置文件中修改 Confluence home directory 选项，重启容器

[root@k8s-linux-worker1 volume_data]# vim confluence_install/confluence/WEB-INF/classes/confluence-init.properties
[root@k8s-linux-worker1 volume_data]# cat confluence_install/confluence/WEB-INF/classes/confluence-init.properties
# This file allows you to set the directory for Confluence to store its configuration files.
#
###########################
# Note for Windows Users  #
###########################
#
# Each backslash in your path must be written as a forward slash.
# - For example:
# c:\confluence\data
#
# should be written as:
#
# c:/confluence/data

###########################
# Note for Unix Users     #
###########################
# - For example:
# confluence.home=/var/confluence
#
# NOTE: If the path of your confluence.home directory contains symlinks,
# please set confluence.home to the absolute path, otherwise problems may occur.
# - For example:
# confluence.home=/data/confluence/ (where /data is a symlink to -> /var/data/)
# should be written as:
# confluence.home=/var/data/confluence/
confluence.home=/var/atlassian/application-data/confluence/

###########################
# Configuration Directory #
###########################

# specify your directory below (don't forget to remove the '#' in front)

# confluence.home=c:/confluence/data
[root@k8s-linux-worker1 volume_data]# 

[root@k8s-linux-worker1 volume_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS                  PORTS               NAMES
19120f7d60ee        atlassian/confluence-server   "/tini -- /entrypoin…"   11 minutes ago      Up 25 seconds                               k8s_confluence_confluence-deployment-7577774698-psgz2_default_ffd2c5df-866b-11e9-8f1f-0017fa00a076_0
b4a031e2564c        k8s.gcr.io/pause:3.1          "/pause"                 11 minutes ago      Up 11 minutes                               k8s_POD_confluence-deployment-7577774698-psgz2_default_ffd2c5df-866b-11e9-8f1f-0017fa00a076_0
cd4ad9dabcd9        ff281650a721                  "cp -f /etc/kube-fla…"   4 days ago          Exited (0) 4 days ago                       k8s_install-cni_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_0
516e95531598        857eadf53a54                  "/entrypoint.sh mysq…"   4 days ago          Up 4 days                                   k8s_mysql_confluence-mysql-d464855bd-9ckm9_default_fc148672-82ae-11e9-8f1f-0017fa00a076_7
e442817adadf        k8s.gcr.io/pause:3.1          "/pause"                 4 days ago          Up 4 days                                   k8s_POD_confluence-mysql-d464855bd-9ckm9_default_fc148672-82ae-11e9-8f1f-0017fa00a076_0
ff2443f44b3a        nginx                         "nginx -g 'daemon of…"   5 days ago          Up 5 days                                   k8s_my-nginx_my-nginx-86459cfc9f-qwclj_default_e5ff59c0-81ba-11e9-8f1f-0017fa00a076_0
01083b94ed24        nginx                         "nginx -g 'daemon of…"   5 days ago          Up 5 days                                   k8s_my-nginx_my-nginx-86459cfc9f-qhjww_default_e5ff0ba3-81ba-11e9-8f1f-0017fa00a076_0
3b01b7d98e57        k8s.gcr.io/pause:3.1          "/pause"                 5 days ago          Up 5 days                                   k8s_POD_my-nginx-86459cfc9f-qwclj_default_e5ff59c0-81ba-11e9-8f1f-0017fa00a076_0
c12093c6eb0e        k8s.gcr.io/pause:3.1          "/pause"                 5 days ago          Up 5 days                                   k8s_POD_my-nginx-86459cfc9f-qhjww_default_e5ff0ba3-81ba-11e9-8f1f-0017fa00a076_0
6d2174182b5d        f9aed6605b81                  "/dashboard --insecu…"   6 days ago          Up 6 days                                   k8s_kubernetes-dashboard_kubernetes-dashboard-5f7b999d65-sw96f_kube-system_62c2ea91-810f-11e9-8f1f-0017fa00a076_0
2938cb474079        ff281650a721                  "/opt/bin/flanneld -…"   6 days ago          Up 6 days                                   k8s_kube-flannel_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_4
975e00897c33        k8s.gcr.io/pause:3.1          "/pause"                 6 days ago          Up 6 days                                   k8s_POD_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_4
f2a933f2127f        k8s.gcr.io/pause:3.1          "/pause"                 6 days ago          Up 6 days                                   k8s_POD_kubernetes-dashboard-5f7b999d65-sw96f_kube-system_62c2ea91-810f-11e9-8f1f-0017fa00a076_3
[root@k8s-linux-worker1 volume_data]# 
[root@k8s-linux-worker1 volume_data]# docker restart 19120f7d60ee
19120f7d60ee
[root@k8s-linux-worker1 volume_data]# 


[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                               SELECTOR
confluence-deployment   1/1     1            1           12m     confluence   atlassian/confluence-server:latest   app=confluence,service=confluence
confluence-mysql        1/1     1            1           4d18h   mysql        mysql/mysql-server:5.7               app=confluence,tier=mysql
my-nginx                8/8     8            8           5d23h   my-nginx     nginx                                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS             RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-7577774698-psgz2   1/1     Running            0          12m     172.20.0.17   10.1.36.46   <none>           <none>
confluence-mysql-d464855bd-9ckm9         1/1     Running            7          4d18h   172.20.0.15   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running            0          5d23h   172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running            0          5d23h   172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running            0          5d23h   172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running            0          5d23h   172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running            0          5d23h   172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running            0          5d23h   172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running            0          5d23h   172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running            0          5d23h   172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     CrashLoopBackOff   1026       4d      172.20.3.8    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE     SELECTOR
confluence         ClusterIP   10.68.241.111   <none>        8090/TCP   22m     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP   4d16h   app=confluence,tier=mysql
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP    13d     <none>
[root@k8s-master1 temp]# 

修改服务的类型为：NodePort

[root@k8s-master1 temp]# vim ./confluence.yml 
[root@k8s-master1 temp]# cat ./confluence.yml 
---
apiVersion: v1
kind: Service
metadata:
  name: confluence
  labels:
    app: confluence
spec:
  ports:
  - name: http
    port: 8090
    targetPort: 8090
    protocol: TCP
  selector:
    app: confluence
    service: confluence
  type: NodePort
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: confluence-deployment
  labels:
    service: confluence
    app: confluence

spec:
  replicas: 1
  selector:
    matchLabels:
      app: confluence
      service: confluence
  template:
    metadata:
      labels:
        app: confluence
        service: confluence
    spec:
      containers:
        - name: confluence
          image: atlassian/confluence-server:latest
          imagePullPolicy: Always
          env:
            - name: JVM_MINIMUM_MEMORY
              value: 2048m
            - name: JVM_MAXIMUM_MEMORY
              value: 2048m
          ports:
            - containerPort: 8090

          volumeMounts:
          - name: confluence-home
            mountPath: /var/atlassian/application-data/confluence
          - name: confluence-install
            mountPath: /opt/atlassian/confluence

      volumes:
        - name: confluence-home
          hostPath:
            path: /opt/k8s/volume_data/confluence_home/
        - name: confluence-install
          hostPath:
            path: /opt/k8s/volume_data/confluence_install/

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f ./confluence.yml
service/confluence configured
deployment.apps/confluence-deployment unchanged
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                               SELECTOR
confluence-deployment   1/1     1            1           16m     confluence   atlassian/confluence-server:latest   app=confluence,service=confluence
confluence-mysql        1/1     1            1           4d18h   mysql        mysql/mysql-server:5.7               app=confluence,tier=mysql
my-nginx                8/8     8            8           5d23h   my-nginx     nginx                                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS             RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-7577774698-psgz2   1/1     Running            0          16m     172.20.0.17   10.1.36.46   <none>           <none>
confluence-mysql-d464855bd-9ckm9         1/1     Running            7          4d18h   172.20.0.15   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running            0          5d23h   172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running            0          5d23h   172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running            0          5d23h   172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running            0          5d23h   172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running            0          5d23h   172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running            0          5d23h   172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running            0          5d23h   172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running            0          5d23h   172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     CrashLoopBackOff   1027       4d      172.20.3.8    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   26m     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         4d16h   app=confluence,tier=mysql
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          13d     <none>
[root@k8s-master1 temp]# 




# confluence 连接 MySQL
[root@k8s-linux-worker1 volume_data]# docker exec -ti 19120f7d60ee bash
root@confluence-deployment-7577774698-psgz2:/var/atlassian/application-data/confluence# env
LC_ALL=en_US.UTF-8
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:
CONFLUENCE_INSTALL_DIR=/opt/atlassian/confluence
CONFLUENCE_SERVICE_PORT_HTTP=8090
LANG=en_US.UTF-8
CONFLUENCE_PORT_8090_TCP=tcp://10.68.241.111:8090
HOSTNAME=confluence-deployment-7577774698-psgz2
CONFLUENCE_MYSQL_SERVICE_PORT=3306
JVM_MINIMUM_MEMORY=2048m
CONFLUENCE_PORT=tcp://10.68.241.111:8090
CONFLUENCE_MYSQL_PORT_3306_TCP=tcp://10.68.89.209:3306
JAVA_HOME=/opt/java/openjdk
JVM_MAXIMUM_MEMORY=2048m
RUN_USER=daemon
KUBERNETES_PORT_443_TCP_PROTO=tcp
CONFLUENCE_SERVICE_HOST=10.68.241.111
KUBERNETES_PORT_443_TCP_ADDR=10.68.0.1
CONFLUENCE_MYSQL_PORT_3306_TCP_PROTO=tcp
JAVA_VERSION=jdk8u212-b03
KUBERNETES_PORT=tcp://10.68.0.1:443
PWD=/var/atlassian/application-data/confluence
HOME=/root
CONFLUENCE_SERVICE_PORT=8090
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP_PORT=443
RUN_GROUP=daemon
CONFLUENCE_PORT_8090_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP=tcp://10.68.0.1:443
CONFLUENCE_PORT_8090_TCP_ADDR=10.68.241.111
CONFLUENCE_HOME=/var/atlassian/application-data/confluence
TERM=xterm
CONFLUENCE_MYSQL_PORT_3306_TCP_PORT=3306
CONFLUENCE_PORT_8090_TCP_PORT=8090
SHLVL=1
LANGUAGE=en_US:en
CONFLUENCE_MYSQL_PORT_3306_TCP_ADDR=10.68.89.209
KUBERNETES_SERVICE_PORT=443
PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_SERVICE_HOST=10.68.0.1
CONFLUENCE_MYSQL_SERVICE_HOST=10.68.89.209
CONFLUENCE_MYSQL_PORT=tcp://10.68.89.209:3306
_=/usr/bin/env
root@confluence-deployment-7577774698-psgz2:/var/atlassian/application-data/confluence# 

http://10.1.36.46:24248

# confluence 数据表
mysql> show tables;
+--------------------------------+
| Tables_in_confluence           |
+--------------------------------+
| AO_187CCC_SIDEBAR_LINK         |
| AO_21D670_WHITELIST_RULES      |
| AO_21F425_MESSAGE_AO           |
| AO_21F425_MESSAGE_MAPPING_AO   |
| AO_21F425_USER_PROPERTY_AO     |
| AO_26DB7F_ENTITIES_TO_ROOMS    |
| AO_26DB7F_ENTITIES_TO_ROOM_CFG |
| AO_38321B_CUSTOM_CONTENT_LINK  |
| AO_4789DD_HEALTH_CHECK_STATUS  |
| AO_4789DD_PROPERTIES           |
| AO_4789DD_READ_NOTIFICATIONS   |
| AO_4789DD_TASK_MONITOR         |
| AO_54C900_CONTENT_BLUEPRINT_AO |
| AO_54C900_C_TEMPLATE_REF       |
| AO_54C900_SPACE_BLUEPRINT_AO   |
| AO_563AEE_ACTIVITY_ENTITY      |
| AO_563AEE_ACTOR_ENTITY         |
| AO_563AEE_MEDIA_LINK_ENTITY    |
| AO_563AEE_OBJECT_ENTITY        |
| AO_563AEE_TARGET_ENTITY        |
| AO_5F3884_FEATURE_DISCOVERY    |
| AO_5FB9D7_AOHIP_CHAT_LINK      |
| AO_5FB9D7_AOHIP_CHAT_USER      |
| AO_6384AB_DISCOVERED           |
| AO_6384AB_FEATURE_METADATA_AO  |
| AO_7CDE43_EVENT                |
| AO_7CDE43_FILTER_PARAM         |
| AO_7CDE43_NOTIFICATION         |
| AO_7CDE43_NOTIFICATION_SCHEME  |
| AO_7CDE43_RECIPIENT            |
| AO_7CDE43_SERVER_CONFIG        |
| AO_7CDE43_SERVER_PARAM         |
| AO_88BB94_BATCH_NOTIFICATION   |
| AO_92296B_AORECENTLY_VIEWED    |
| AO_9412A1_AONOTIFICATION       |
| AO_9412A1_AOREGISTRATION       |
| AO_9412A1_AOTASK               |
| AO_9412A1_AOUSER               |
| AO_9412A1_USER_APP_LINK        |
| AO_954A21_PUSH_NOTIFICATION_AO |
| AO_A0B856_WEB_HOOK_LISTENER_AO |
| AO_BAF3AA_AOINLINE_TASK        |
| AO_DC98AE_AOHELP_TIP           |
| AO_ED669C_SEEN_ASSERTIONS      |
| ATTACHMENTDATA                 |
| AUDITRECORD                    |
| AUDIT_AFFECTED_OBJECT          |
| AUDIT_CHANGED_VALUE            |
| BANDANA                        |
| BODYCONTENT                    |
| CLUSTERSAFETY                  |
| CONFANCESTORS                  |
| CONFVERSION                    |
| CONTENT                        |
| CONTENTPROPERTIES              |
| CONTENT_LABEL                  |
| CONTENT_PERM                   |
| CONTENT_PERM_SET               |
| CONTENT_RELATION               |
| DECORATOR                      |
| DIAGNOSTICS_ALERTS             |
| EVENTS                         |
| EXTRNLNKS                      |
| FOLLOW_CONNECTIONS             |
| IMAGEDETAILS                   |
| INDEXQUEUEENTRIES              |
| KEYSTORE                       |
| LABEL                          |
| LIKES                          |
| LINKS                          |
| MIG_ATTACHMENT                 |
| MIG_CLOUD_SITE                 |
| MIG_DB_CHANGELOG               |
| MIG_DB_CHANGELOG_LOCK          |
| MIG_PLAN                       |
| MIG_SEQUENCES                  |
| MIG_STATS                      |
| MIG_STEP                       |
| MIG_TASK                       |
| MIG_WORK_ITEM                  |
| NOTIFICATIONS                  |
| OS_PROPERTYENTRY               |
| PAGETEMPLATES                  |
| PLUGINDATA                     |
| SECRETS                        |
| SNAPSHOTS                      |
| SPACEPERMISSIONS               |
| SPACES                         |
| TRACKBACKLINKS                 |
| TRUSTEDAPP                     |
| TRUSTEDAPPRESTRICTION          |
| USERCONTENT_RELATION           |
| USER_RELATION                  |
| cwd_app_dir_group_mapping      |
| cwd_app_dir_mapping            |
| cwd_app_dir_operation          |
| cwd_application                |
| cwd_application_address        |
| cwd_application_attribute      |
| cwd_directory                  |
| cwd_directory_attribute        |
| cwd_directory_operation        |
| cwd_group                      |
| cwd_group_attribute            |
| cwd_membership                 |
| cwd_user                       |
| cwd_user_attribute             |
| cwd_user_credential_record     |
| hibernate_unique_key           |
| journalentry                   |
| logininfo                      |
| remembermetoken                |
| scheduler_clustered_jobs       |
| scheduler_run_details          |
| user_mapping                   |
+--------------------------------+
115 rows in set (0.01 sec)

mysql> 

[root@k8s-master1 temp]# vim confluence.yml 
[root@k8s-master1 temp]# cat confluence.yml 
---
apiVersion: v1
kind: Service
metadata:
  name: confluence
  labels:
    app: confluence
spec:
  ports:
  - name: http
    port: 8090
    targetPort: 8090
    protocol: TCP
  selector:
    app: confluence
    service: confluence
  type: NodePort
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: confluence-deployment
  labels:
    service: confluence
    app: confluence

spec:
  replicas: 1
  selector:
    matchLabels:
      app: confluence
      service: confluence
  template:
    metadata:
      labels:
        app: confluence
        service: confluence
    spec:
      containers:
        - name: confluence
          image: atlassian/confluence-server:latest
          imagePullPolicy: Always
          env:
            - name: JVM_MINIMUM_MEMORY
              value: 8g
            - name: JVM_MAXIMUM_MEMORY
              value: 8g
          ports:
            - containerPort: 8090

          volumeMounts:
          - name: confluence-home
            mountPath: /var/atlassian/application-data/confluence
          - name: confluence-install
            mountPath: /opt/atlassian/confluence

      nodeSelector:
        nodename:
          k8s-linux-worker3

      volumes:
        - name: confluence-home
          hostPath:
            path: /opt/k8s/volume_data/confluence_home/
        - name: confluence-install
          hostPath:
            path: /opt/k8s/volume_data/confluence_install/

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f ./confluence.yml 
service/confluence unchanged
deployment.apps/confluence-deployment created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                                         SELECTOR
confluence-deployment   1/1     1            1           6s      confluence   atlassian/confluence-server:latest             app=confluence,service=confluence
confluence-mysql        1/1     1            1           21m     mysql        mysql/mysql-server:5.7                         app=confluence,tier=mysql
edusoho-deployment      1/1     1            1           45m     edusoho      edusoho/edusoho                                app=edusoho,service=edusoho
edusoho-mysql           1/1     1            1           72m     mysql        mysql/mysql-server:5.7                         app=edusoho,tier=mysql
jira-deployment         1/1     1            1           8h      jira         cptactionhank/atlassian-jira-software:latest   app=jira,service=jira
my-nginx                8/8     8            8           7d11h   my-nginx     nginx                                          run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS      RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-59c98447bf-996dc   1/1     Running     0          16s     172.20.2.18   10.1.36.48   <none>           <none>
confluence-mysql-859d7f788b-24l27        1/1     Running     0          21m     172.20.0.19   10.1.36.46   <none>           <none>
edusoho-deployment-57cb7946df-9nn6l      1/1     Running     0          45m     172.20.2.17   10.1.36.48   <none>           <none>
edusoho-mysql-fc4f549f5-hv9sw            1/1     Running     0          72m     172.20.1.26   10.1.36.47   <none>           <none>
jira-deployment-ccc84bffd-r9mzz          1/1     Running     0          8h      172.20.2.16   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running     0          7d11h   172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running     0          7d11h   172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running     0          7d11h   172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running     0          7d11h   172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running     0          7d11h   172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running     0          7d11h   172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running     0          7d11h   172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running     0          7d11h   172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     Completed   0          17m     172.20.1.28   10.1.36.47   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE    SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   36h    app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         6d4h   app=confluence,tier=mysql
edusoho            NodePort    10.68.215.211   <none>        80:27118/TCP     46m    app=edusoho,service=edusoho
edusoho-mysql      ClusterIP   10.68.42.16     <none>        3306/TCP         59m    app=edusoho,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   8h     app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          15d    <none>
[root@k8s-master1 temp]# 



[root@k8s-master1 back]# ./atlassian-confluence-6.9.1-x64.bin 
Unpacking JRE ...
Starting Installer ...

This will install Confluence 6.9.1 on your computer.
OK [o, Enter], Cancel [c]
o
Click Next to continue, or Cancel to exit Setup.

Choose the appropriate installation or upgrade option.
Please choose one of the following:
Express Install (uses default settings) [1], 
Custom Install (recommended for advanced users) [2, Enter], 
Upgrade an existing Confluence installation [3]
2

Select the folder where you would like Confluence 6.9.1 to be installed,
then click Next.
Where should Confluence 6.9.1 be installed?
[/opt/atlassian/confluence]
/opt/k8s/confluence/confluence_install

Default location for Confluence data
[/var/atlassian/application-data/confluence]
/opt/k8s/confluence/confluence_home

Configure which ports Confluence will use.
Confluence requires two TCP ports that are not being used by any other
applications on this machine. The HTTP port is where you will access
Confluence through your browser. The Control port is used to Startup and
Shutdown Confluence.
Use default ports (HTTP: 8090, Control: 8000) - Recommended [1, Enter], Set custom value for HTTP and Control ports [2]
2
HTTP Port Number
[8090]
8090
Control Port Number
[8000]
8091

Confluence can be run in the background.
You may choose to run Confluence as a service, which means it will start
automatically whenever the computer restarts.
Install Confluence as Service?
Yes [y, Enter], No [n]
n

Extracting files ...
                                                                           

Please wait a few moments while we configure Confluence.

Installation of Confluence 6.9.1 is complete
Start Confluence now?
Yes [y, Enter], No [n]
y

Please wait a few moments while Confluence starts up.
Launching Confluence ...

Installation of Confluence 6.9.1 is complete
Your installation of Confluence 6.9.1 is now ready and can be accessed via
your browser.
Confluence 6.9.1 can be accessed at http://localhost:8090
Finishing installation ...
[root@k8s-master1 back]# 






```




### Jira

JIRA Core、JIRA Software、JIRA Service Desk 的区别
参考 https://blog.csdn.net/cabinhe/article/details/78165832

docker 镜像信息，dockerfile 信息

https://hub.docker.com/r/cptactionhank/atlassian-jira-software

运行 jira 对 MySQL 数据库的要求

https://confluence.atlassian.com/adminjiraserver/connecting-jira-applications-to-mysql-5-7-966063305.html

jira 对 MySQL 数据库的要求

```bash
[root@lanzhiwang-centos7 jira]# cat /etc/my.cnf
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
[root@lanzhiwang-centos7 jira]# 


```


### dockerfile

```bash
FROM openjdk:8-alpine

# Configuration variables.
ENV JIRA_HOME     /var/atlassian/jira
ENV JIRA_INSTALL  /opt/atlassian/jira
ENV JIRA_VERSION  8.2.1

# Install Atlassian JIRA and helper tools and setup initial home
# directory structure.
RUN set -x \
    && apk add --no-cache curl xmlstarlet bash ttf-dejavu libc6-compat \
    && mkdir -p                "${JIRA_HOME}" \
    && mkdir -p                "${JIRA_HOME}/caches/indexes" \
    && chmod -R 700            "${JIRA_HOME}" \
    && chown -R daemon:daemon  "${JIRA_HOME}" \
    && mkdir -p                "${JIRA_INSTALL}/conf/Catalina" \
    && curl -Ls                "https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-8.2.1.tar.gz" | tar -xz --directory "${JIRA_INSTALL}" --strip-components=1 --no-same-owner \
    && curl -Ls                "https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.38.tar.gz" | tar -xz --directory "${JIRA_INSTALL}/lib" --strip-components=1 --no-same-owner "mysql-connector-java-5.1.38/mysql-connector-java-5.1.38-bin.jar" \
    && rm -f                   "${JIRA_INSTALL}/lib/postgresql-9.1-903.jdbc4-atlassian-hosted.jar" \
    && curl -Ls                "https://jdbc.postgresql.org/download/postgresql-42.2.1.jar" -o "${JIRA_INSTALL}/lib/postgresql-42.2.1.jar" \
    && chmod -R 700            "${JIRA_INSTALL}/conf" \
    && chmod -R 700            "${JIRA_INSTALL}/logs" \
    && chmod -R 700            "${JIRA_INSTALL}/temp" \
    && chmod -R 700            "${JIRA_INSTALL}/work" \
    && chown -R daemon:daemon  "${JIRA_INSTALL}/conf" \
    && chown -R daemon:daemon  "${JIRA_INSTALL}/logs" \
    && chown -R daemon:daemon  "${JIRA_INSTALL}/temp" \
    && chown -R daemon:daemon  "${JIRA_INSTALL}/work" \
    && sed --in-place          "s/java version/openjdk version/g" "${JIRA_INSTALL}/bin/check-java.sh" \
    && echo -e                 "\njira.home=$JIRA_HOME" >> "${JIRA_INSTALL}/atlassian-jira/WEB-INF/classes/jira-application.properties" \
    && touch -d "@0"           "${JIRA_INSTALL}/conf/server.xml"

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
USER daemon:daemon

# Expose default HTTP connector port.
EXPOSE 8080

# Set volume mount points for installation and home directory. Changes to the
# home directory needs to be persisted as well as parts of the installation
# directory due to eg. logs.
VOLUME ["/var/atlassian/jira", "/opt/atlassian/jira/logs"]

# Set the default working directory as the installation directory.
WORKDIR /var/atlassian/jira

COPY "docker-entrypoint.sh" "/"
ENTRYPOINT ["/docker-entrypoint.sh"]

# Run Atlassian JIRA as a foreground process by default.
CMD ["/opt/atlassian/jira/bin/start-jira.sh", "-fg"]



```

### docker-entrypoint.sh

```bash

#!/bin/bash

# check if the `server.xml` file has been changed since the creation of this
# Docker image. If the file has been changed the entrypoint script will not
# perform modifications to the configuration file.
if [ "$(stat -c "%Y" "${JIRA_INSTALL}/conf/server.xml")" -eq "0" ]; then
  if [ -n "${X_PROXY_NAME}" ]; then
    xmlstarlet ed --inplace --pf --ps --insert '//Connector[@port="8080"]' --type "attr" --name "proxyName" --value "${X_PROXY_NAME}" "${JIRA_INSTALL}/conf/server.xml"
  fi
  if [ -n "${X_PROXY_PORT}" ]; then
    xmlstarlet ed --inplace --pf --ps --insert '//Connector[@port="8080"]' --type "attr" --name "proxyPort" --value "${X_PROXY_PORT}" "${JIRA_INSTALL}/conf/server.xml"
  fi
  if [ -n "${X_PROXY_SCHEME}" ]; then
    xmlstarlet ed --inplace --pf --ps --insert '//Connector[@port="8080"]' --type "attr" --name "scheme" --value "${X_PROXY_SCHEME}" "${JIRA_INSTALL}/conf/server.xml"
  fi
  if [ -n "${X_PATH}" ]; then
    xmlstarlet ed --inplace --pf --ps --update '//Context/@path' --value "${X_PATH}" "${JIRA_INSTALL}/conf/server.xml"
  fi
fi

exec "$@"


```












### docker 安装 jira

```bash
# https://hub.docker.com/r/cptactionhank/atlassian-jira-software
docker pull cptactionhank/atlassian-jira-software

CREATE DATABASE jiradb CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

# 基础应用
docker run --detach --publish 8080:8080 cptactionhank/atlassian-jira-software:latest
# -d, --detach                         Run container in background and print container ID

# JIRA_HOME     
/root/work/jira/jira_home:/var/atlassian/jira

# JIRA_INSTALL  
/root/work/jira/jira_install:/opt/atlassian/jira


docker run -v /root/work/jira/jira_home:/var/atlassian/jira -v /root/work/jira/jira_install:/opt/atlassian/jira --name="jira" -d -p 8080:8080 cptactionhank/atlassian-jira-software:latest

# 需要准备的软件
[root@lanzhiwang-centos7 jira]# ll
total 312016
drwxr-xr-x 13 1000 1000       282 May 27 23:37 atlassian-jira-software-8.2.1-standalone
-rw-r--r--  1 root root 314763916 May 29 15:19 atlassian-jira-software-8.2.1.tar.gz
drwxr-xr-x  4 root root       151 Dec  2  2015 mysql-connector-java-5.1.38
-rw-r--r--  1 root root   3938241 Dec  2  2015 mysql-connector-java-5.1.38.tar.gz
-rw-r--r--  1 root root    794639 Jan 25  2018 postgresql-42.2.1.jar
[root@lanzhiwang-centos7 jira]# 

[root@lanzhiwang-centos7 jira]# mkdir jira_home
[root@lanzhiwang-centos7 jira]# mkdir -p jira_home/caches/indexes
[root@lanzhiwang-centos7 jira]# chmod -R 700 jira_home/
[root@lanzhiwang-centos7 jira]# chown -R daemon:daemon jira_home/
[root@lanzhiwang-centos7 jira]#  
[root@lanzhiwang-centos7 jira]# cp -R atlassian-jira-software-8.2.1-standalone/ jira_install
[root@lanzhiwang-centos7 jira]# mkdir -p jira_install/conf/Catalina
[root@lanzhiwang-centos7 jira]# 
[root@lanzhiwang-centos7 jira]# cp mysql-connector-java-5.1.38/mysql-connector-java-5.1.38-bin.jar jira_install/lib/
[root@lanzhiwang-centos7 jira]# rm -rf jira_install/lib/postgresql-9.4.1212.jar 
[root@lanzhiwang-centos7 jira]# cp postgresql-42.2.1.jar jira_install/lib/
[root@lanzhiwang-centos7 jira]# chmod -R 700 jira_install/
[root@lanzhiwang-centos7 jira]# chown -R daemon:daemon jira_install/
[root@lanzhiwang-centos7 jira]# 
[root@lanzhiwang-centos7 jira]# sed --in-place "s/java version/openjdk version/g" "jira_install/bin/check-java.sh"  # 其实没有作用
[root@lanzhiwang-centos7 jira]# 
[root@lanzhiwang-centos7 jira]# echo -e "\njira.home=/var/atlassian/jira" >> "jira_install/atlassian-jira/WEB-INF/classes/jira-application.properties"
[root@lanzhiwang-centos7 jira]# cat jira_install//atlassian-jira/WEB-INF/classes/jira-application.properties
# Do not modify this file unless instructed. It is here to store the location of the JIRA home directory only and is typically written to by the installer.
jira.home =

jira.home=/var/atlassian/jira
[root@lanzhiwang-centos7 jira]# 

[root@lanzhiwang-centos7 jira]# ll jira_install/conf/server.xml
-rwx------ 1 daemon daemon 6466 Jun  4 19:01 jira_install/conf/server.xml
[root@lanzhiwang-centos7 jira]# 
# -d 设定时间与日期，可以使用各种不同的格式
[root@lanzhiwang-centos7 jira]# touch -d "@0" jira_install/conf/server.xml  
[root@lanzhiwang-centos7 jira]# ll jira_install/conf/server.xml
-rwx------ 1 daemon daemon 6466 Jan  1  1970 jira_install/conf/server.xml
[root@lanzhiwang-centos7 jira]# 

[root@lanzhiwang-centos7 jira]# docker run -v /root/work/jira/jira_home:/var/atlassian/jira -v /root/work/jira/jira_install:/opt/atlassian/jira --name="jira" -d -p 8080:8080 cptactionhank/atlassian-jira-software:latest
a13a1e84723071bd57e69fc22cca3d83e2d4275a74df575fc9e90389c007d1ce
[root@lanzhiwang-centos7 jira]# 
[root@lanzhiwang-centos7 jira]# docker ps -a
CONTAINER ID        IMAGE                                          COMMAND                  CREATED             STATUS              PORTS                    NAMES
a13a1e847230        cptactionhank/atlassian-jira-software:latest   "/docker-entrypoint.…"   8 seconds ago       Up 7 seconds        0.0.0.0:8080->8080/tcp   jira
[root@lanzhiwang-centos7 jira]# 
[root@lanzhiwang-centos7 jira]# docker logs a13a1e847230



[root@k8s-master1 temp]# vim jira.yml
[root@k8s-master1 temp]# cat jira.yml
apiVersion: v1
kind: Service
metadata:
  name: jira
  labels:
    app: jira
spec:
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    protocol: TCP
  selector:
    app: jira
    service: jira
  type: NodePort
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: jira-deployment
  labels:
    service: jira
    app: jira

spec:
  replicas: 1
  selector:
    matchLabels:
      app: jira
      service: jira
  template:
    metadata:
      labels:
        app: jira
        service: jira
    spec:
      containers:
        - name: jira
          image: cptactionhank/atlassian-jira-software:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080

          volumeMounts:
          - name: jira-home
            mountPath: /var/atlassian/jira
          - name: jira-install
            mountPath: /opt/atlassian/jira

      volumes:
        - name: jira-home
          hostPath:
            path: /opt/k8s/volume_data/jira_home/
        - name: jira-install
          hostPath:
            path: /opt/k8s/volume_data/jira_install/

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f ./jira.yml
service/jira unchanged
deployment.apps/jira-deployment created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   27h     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         5d19h   app=confluence,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   83s     app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          14d     <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                                         SELECTOR
confluence-deployment   1/1     1            1           27h     confluence   atlassian/confluence-server:latest             app=confluence,service=confluence
confluence-mysql        1/1     1            1           5d22h   mysql        mysql/mysql-server:5.7                         app=confluence,tier=mysql
jira-deployment         1/1     1            1           52s     jira         cptactionhank/atlassian-jira-software:latest   app=jira,service=jira
my-nginx                8/8     8            8           7d3h    my-nginx     nginx                                          run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS             RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-7577774698-psgz2   1/1     Running            0          27h     172.20.0.17   10.1.36.46   <none>           <none>
confluence-mysql-d464855bd-9ckm9         1/1     Running            7          5d22h   172.20.0.15   10.1.36.46   <none>           <none>
jira-deployment-ccc84bffd-r9mzz          1/1     Running            0          67s     172.20.2.16   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running            0          7d3h    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running            0          7d3h    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running            0          7d3h    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running            0          7d3h    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running            0          7d3h    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running            0          7d3h    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running            0          7d3h    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running            0          7d3h    172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     CrashLoopBackOff   1321       5d3h    172.20.3.8    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 










```




### MySQL

Deploying MySQL on Linux with Docker
参考 https://dev.mysql.com/doc/refman/5.7/en/linux-installation-docker.html

dockerfile
https://github.com/mysql/mysql-docker

MySQL 相关 k8s 资源配置文件参考


https://github.com/IBM/Scalable-WordPress-deployment-on-Kubernetes


环境变量
MYSQL_ROOT_PASSWORD

持久化
--mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
--mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \

log_error 在 配置文件中配置，相关目录持久化


### MySQL 容器相关

```bash

################################### MySQL 容器基础 ###################################

# 使用 mysql/mysql-server:5.7 的 MySQL 镜像
[root@lanzhiwang-centos7 ~]# docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
mysql/mysql-server            5.7                 857eadf53a54        4 weeks ago         258MB

[root@lanzhiwang-centos7 ~]# 
# 创建基本的容器
[root@lanzhiwang-centos7 ~]# docker run --name=mysql1 -d mysql/mysql-server:5.7
6c48f9a1f88a02505eb0b145563a83d649e7e54096f776444000a5bce1087733
[root@lanzhiwang-centos7 ~]# 

[root@lanzhiwang-centos7 ~]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
6c48f9a1f88a        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   5 seconds ago       Up 4 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1

# 在容器日志中确认容器启动是否正常，确认 root 初始密码
[root@lanzhiwang-centos7 ~]# docker logs mysql1
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] No password option specified for new database.
[Entrypoint]   A random onetime password will be generated.
[Entrypoint] Initializing database
[Entrypoint] Database initialized
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leapseconds' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/tzdata.zi' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
[Entrypoint] GENERATED ROOT PASSWORD: iz(3S1eD]ABlApg4qun@D)YrqoR

[Entrypoint] ignoring /docker-entrypoint-initdb.d/*

[Entrypoint] Server shut down
[Entrypoint] Setting root user as expired. Password will need to be changed before database can be used.

[Entrypoint] MySQL init process done. Ready for start up.

[Entrypoint] Starting MySQL 5.7.26-1.1.11
[root@lanzhiwang-centos7 ~]# 

# 后续可以在 /docker-entrypoint-initdb.d/ 目录中放置相关脚本，待容器启动后执行脚本做初始化的工作


# 进入容器执行相关命令
[root@lanzhiwang-centos7 ~]# docker exec -it mysql1 bash
bash-4.2# mysql
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
bash-4.2# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 5.7.26

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
# 修改 root 密码
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'rootpassword';
Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye
bash-4.2# 


# 在容器中中查看 MySQL 数据目录
bash-4.2# ls /var/lib/mysql
auto.cnf  ca-key.pem  ca.pem  client-cert.pem  client-key.pem  ib_buffer_pool  ib_logfile0  ib_logfile1  ibdata1  ibtmp1  mysql  mysql.sock  mysql.sock.lock  performance_schema  private_key.pem  public_key.pem  server-cert.pem  server-key.pem  sys
bash-4.2# 

# 在容器中中查看 MySQL 默认配置文件
bash-4.2# ls /etc/my.cnf   
/etc/my.cnf
bash-4.2# 
bash-4.2# cat /etc/my.cnf
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
skip-host-cache
skip-name-resolve
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
secure-file-priv=/var/lib/mysql-files
user=mysql

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

# 在容器中中查看 MySQL 日志文件
bash-4.2# cat /var/log/mysqld.log
bash-4.2# 
bash-4.2# exit
exit
[root@lanzhiwang-centos7 ~]# 


################################### MySQL 挂载目录启动容器 ###################################


# 绑定配置文件和数据目录启动 MySQL 容器（配置文件 /root/work/mysql/my.cnf 和 数据目录 /root/work/mysql/data 要在启动容器前准备好）
[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 \
> --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf \
> --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql \
> -d mysql/mysql-server:5.7
81a31f5a37cc16a644e6d262ad0666fb84b9ac1041aabf6005821c8f825b80d3
[root@lanzhiwang-centos7 mysql]# 

# 容器看起来启动成功（实际上没有成功）
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
81a31f5a37cc        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   10 seconds ago      Up 9 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
[root@lanzhiwang-centos7 mysql]# 

# 挂载到容器中的宿主机的数据目录和配置文件
[root@lanzhiwang-centos7 mysql]# ll
total 4
drwxr-xr-x 5 mysql mysql  314 May 30 09:49 data
drwxr-xr-x 2 root  root     6 May 30 09:47 log
-rw-r--r-- 1 root  root  1208 May 30 09:46 my.cnf
[root@lanzhiwang-centos7 mysql]# 

# 查看在宿主机上的数据目录和配置文件
[root@lanzhiwang-centos7 mysql]# ll data/
total 2109508
-rw-r----- 1 root root         56 May 30 09:49 auto.cnf
-rw------- 1 root root       1676 May 30 09:49 ca-key.pem
-rw-r--r-- 1 root root       1112 May 30 09:49 ca.pem
-rw-r--r-- 1 root root       1112 May 30 09:49 client-cert.pem
-rw------- 1 root root       1676 May 30 09:49 client-key.pem
-rw-r----- 1 root root        419 May 30 09:49 ib_buffer_pool
-rw-r----- 1 root root   12582912 May 30 09:49 ibdata1
-rw-r----- 1 root root 1073741824 May 30 09:49 ib_logfile0
-rw-r----- 1 root root 1073741824 May 30 09:49 ib_logfile1
drwxr-x--- 2 root root       4096 May 30 09:49 mysql
drwxr-x--- 2 root root       8192 May 30 09:49 performance_schema
-rw------- 1 root root       1676 May 30 09:49 private_key.pem
-rw-r--r-- 1 root root        452 May 30 09:49 public_key.pem
-rw-r--r-- 1 root root       1112 May 30 09:49 server-cert.pem
-rw------- 1 root root       1680 May 30 09:49 server-key.pem
drwxr-x--- 2 root root       8192 May 30 09:49 sys
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# ll log/
total 0
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# cat my.cnf 
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
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
bind-address=0.0.0.0

character-set-server=utf8
collation-server=utf8_bin

default-storage-engine=INNODB

max_allowed_packet=256M

innodb_log_file_size=1GB

sql_mode = NO_AUTO_VALUE_ON_ZERO

transaction-isolation=READ-COMMITTED

binlog_format=row


# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
[root@lanzhiwang-centos7 mysql]# 

# 在容器日志中确认容器启动是否正常，确认 root 初始密码（容器没有启动成功）
[root@lanzhiwang-centos7 mysql]# docker logs mysql1
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] No password option specified for new database.
[Entrypoint]   A random onetime password will be generated.
[Entrypoint] Initializing database
[Entrypoint] Database initialized
2019-05-30T01:49:57.357521Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2019-05-30T01:49:57.357639Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
2019-05-30T01:49:57.358688Z 0 [Note] mysqld (mysqld 5.7.26) starting as process 50 ...
2019-05-30T01:49:57.367125Z 0 [ERROR] Fatal error: Please read "Security" section of the manual to find out how to run mysqld as root!

2019-05-30T01:49:57.367159Z 0 [ERROR] Aborting

2019-05-30T01:49:57.367212Z 0 [Note] Binlog end
Initialization of mysqld failed: 0
2019-05-30T01:49:57.367416Z 0 [Note] mysqld: Shutdown complete

[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 

# 容器没有启动成功
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                     PORTS               NAMES
81a31f5a37cc        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   3 minutes ago       Exited (1) 2 minutes ago                       mysql1
[root@lanzhiwang-centos7 mysql]# 


# 2019-05-30T01:49:57.367125Z 0 [ERROR] Fatal error: Please read "Security" section of the manual to find out how to run mysqld as root!
# 在配置文件中增加 user=mysql
[root@lanzhiwang-centos7 mysql]# cat my.cnf 
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

character-set-server=utf8
collation-server=utf8_bin

default-storage-engine=INNODB

max_allowed_packet=256M

innodb_log_file_size=1GB

sql_mode = NO_AUTO_VALUE_ON_ZERO

transaction-isolation=READ-COMMITTED

binlog_format=row


# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

[root@lanzhiwang-centos7 mysql]# 

# 重新启动容器
[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql -d mysql/mysql-server:5.7
1590065c7d7e6005a7b9b7fa69e3ec5dd3466ac3158141f6a97b41b3d0c12e4f
[root@lanzhiwang-centos7 mysql]# 

[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
1590065c7d7e        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   8 seconds ago       Up 7 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1

[root@lanzhiwang-centos7 mysql]# docker logs mysql1
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] No password option specified for new database.
[Entrypoint]   A random onetime password will be generated.
[Entrypoint] Initializing database
[Entrypoint] Database initialized
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leapseconds' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/tzdata.zi' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
[Entrypoint] GENERATED ROOT PASSWORD: UfPUJax+UpIDX4k3vYR@l,YdcUL

[Entrypoint] ignoring /docker-entrypoint-initdb.d/*

[Entrypoint] Server shut down
[Entrypoint] Setting root user as expired. Password will need to be changed before database can be used.

[Entrypoint] MySQL init process done. Ready for start up.

[Entrypoint] Starting MySQL 5.7.26-1.1.11
[root@lanzhiwang-centos7 mysql]# 


################################### MySQL 挂载文件启动容器 ###################################


# 绑定配置文件、数据目录、日志目录启动 MySQL 容器（配置文件、数据目录、日志目录要在启动容器前准备好）
[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log,dst=/var/log -d mysql/mysql-server:5.7
a1228535445be289852e9e569a61d44b38888d80e3ad6c8dcc906e2869940c60
[root@lanzhiwang-centos7 mysql]# 

# 容器启动失败
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                     PORTS               NAMES
a1228535445b        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   7 seconds ago       Exited (1) 6 seconds ago                       mysql1
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker logs a1228535445b
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] No password option specified for new database.
[Entrypoint]   A random onetime password will be generated.
[Entrypoint] Initializing database
2019-05-30T02:04:12.351698Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2019-05-30T02:04:12.351752Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
2019-05-30T02:04:12.354868Z 0 [ERROR] Could not open file '/var/log/mysqld.log' for error logging: Permission denied
2019-05-30T02:04:12.354886Z 0 [ERROR] Aborting

[root@lanzhiwang-centos7 mysql]# 

# Could not open file '/var/log/mysqld.log' for error logging: Permission denied
# 修改宿主机日志目录所属用户和用户组
[root@lanzhiwang-centos7 mysql]# ll
total 4
drwxr-xr-x 2 mysql mysql    6 May 30 10:04 data
drwxr-xr-x 2 root  root     6 May 30 09:47 log
-rw-r--r-- 1 root  root  1221 May 30 09:57 my.cnf

[root@lanzhiwang-centos7 mysql]# chown -R mysql:mysql log
[root@lanzhiwang-centos7 mysql]# ll
total 4
drwxr-xr-x 2 mysql mysql    6 May 30 10:04 data
drwxr-xr-x 2 mysql mysql    6 May 30 09:47 log
-rw-r--r-- 1 root  root  1221 May 30 09:57 my.cnf
[root@lanzhiwang-centos7 mysql]# 

# 重新启动容器
[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log,dst=/var/log -d mysql/mysql-server:5.7
3c2ab5b463075053fd5e1318e01db9c37e5d70c95ff3e30fac52f863fa5164f4
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
3c2ab5b46307        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   5 seconds ago       Up 4 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1

[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker logs 3c2ab5b46307
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] No password option specified for new database.
[Entrypoint]   A random onetime password will be generated.
[Entrypoint] Initializing database
[Entrypoint] Database initialized
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leapseconds' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/tzdata.zi' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
[Entrypoint] GENERATED ROOT PASSWORD: APaH%0B%@sumh3HAqXiz+erefOr

[Entrypoint] ignoring /docker-entrypoint-initdb.d/*

[Entrypoint] Server shut down
[Entrypoint] Setting root user as expired. Password will need to be changed before database can be used.

[Entrypoint] MySQL init process done. Ready for start up.

[Entrypoint] Starting MySQL 5.7.26-1.1.11
[root@lanzhiwang-centos7 mysql]# 


################################### MySQL 挂载日志文件启动容器 ###################################

# 绑定配置文件、数据目录、日志文件启动 MySQL 容器（配置文件、数据目录、日志文件要在启动容器前准备好）
[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log/mysqld.log,dst=/var/log/mysqld.log -d mysql/mysql-server:5.7
cde247b1a08cd3202f2db8f5523fa82e38b1862e3526dcd5dccb511a87dd10ef
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
cde247b1a08c        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   5 seconds ago       Up 5 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker logs cde247b1a08c
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] No password option specified for new database.
[Entrypoint]   A random onetime password will be generated.
[Entrypoint] Initializing database
[Entrypoint] Database initialized
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leapseconds' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/tzdata.zi' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
[Entrypoint] GENERATED ROOT PASSWORD: YbyMQEkYgUt@q3xBUPwux^Ojhak

[Entrypoint] ignoring /docker-entrypoint-initdb.d/*

[Entrypoint] Server shut down
[Entrypoint] Setting root user as expired. Password will need to be changed before database can be used.

[Entrypoint] MySQL init process done. Ready for start up.

[Entrypoint] Starting MySQL 5.7.26-1.1.11
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 

# 进入容器修改 root 密码
[root@lanzhiwang-centos7 mysql]# docker exec -it mysql1 bash
bash-4.2# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 5.7.26

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'rootpassword';
Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye
bash-4.2# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> exit
Bye
bash-4.2# exit
exit
[root@lanzhiwang-centos7 mysql]# 




################################### MySQL 映射端口、环境变量启动容器 ###################################


[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 -e MYSQL_ROOT_PASSWORD=rootpass --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log/mysqld.log,dst=/var/log/mysqld.log -p 3306:3306 -p 33060:33060 -d mysql/mysql-server:5.7
a3deb6919015b705797e9448a6a594e1f30b97c138d68c6e362c3dec5dc8f07a
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                                              NAMES
a3deb6919015        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   3 seconds ago       Up 2 seconds (health: starting)   0.0.0.0:3306->3306/tcp, 0.0.0.0:33060->33060/tcp   mysql1

[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker logs a3deb6919015
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] Starting MySQL 5.7.26-1.1.11
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# netstat -tulnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      962/sshd            
tcp        0      0 127.0.0.1:8088          0.0.0.0:*               LISTEN      967/influxd         
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      1218/master         
tcp6       0      0 :::33060                :::*                    LISTEN      11088/docker-proxy  
tcp6       0      0 :::3306                 :::*                    LISTEN      11100/docker-proxy  
tcp6       0      0 :::8086                 :::*                    LISTEN      967/influxd         
tcp6       0      0 :::22                   :::*                    LISTEN      962/sshd            
tcp6       0      0 ::1:25                  :::*                    LISTEN      1218/master         
udp        0      0 0.0.0.0:514             0.0.0.0:*                           975/rsyslogd        
udp        0      0 0.0.0.0:68              0.0.0.0:*                           698/dhclient        
udp6       0      0 :::514                  :::*                                975/rsyslogd        
[root@lanzhiwang-centos7 mysql]# 




# 要在宿主机上直接连接容器中的MySQL，需要满足一下两个条件
1、配置文件中指定 bind-address=0.0.0.0
2、对 root 用户进行远程登录授权（需要在容器中执行下列命令）

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpassword';

flush privileges;

mysql -u root -p -e "SHOW DATABASES"

mysql -u root -p -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpassword';"

mysql -u root -p -e "flush privileges;"


[root@lanzhiwang-centos7 mysql]# ifconfig -a
docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.2.65.1  netmask 255.255.255.0  broadcast 10.2.65.255
        inet6 fe80::42:57ff:fe15:adc7  prefixlen 64  scopeid 0x20<link>
        ether 02:42:57:15:ad:c7  txqueuelen 0  (Ethernet)
        RX packets 20860  bytes 861976 (841.7 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 21874  bytes 40993258 (39.0 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
        inet6 fe80::a00:27ff:fe7b:569e  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:7b:56:9e  txqueuelen 1000  (Ethernet)
        RX packets 201808  bytes 207020353 (197.4 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 73784  bytes 6906511 (6.5 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enp0s8: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.5.106.26  netmask 255.255.255.0  broadcast 10.5.106.255
        inet6 fe80::e9f3:ab4b:a177:5e1  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:7a:4d:cf  txqueuelen 1000  (Ethernet)
        RX packets 716141  bytes 72964936 (69.5 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 12  bytes 1176 (1.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 23922  bytes 5066795 (4.8 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 23922  bytes 5066795 (4.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

veth7d86887: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::9047:deff:fe95:c6ea  prefixlen 64  scopeid 0x20<link>
        ether 92:47:de:95:c6:ea  txqueuelen 0  (Ethernet)
        RX packets 89  bytes 20598 (20.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 116  bytes 12554 (12.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@lanzhiwang-centos7 mysql]# 

# 可以通过下列地址登录
mysql -u root -p -h 10.2.65.2  # 10.2.65.2 是容器本身的 IP
mysql -u root -p -h 10.2.65.1
mysql -u root -p -h 10.0.2.15
mysql -u root -p -h 10.5.106.26
mysql -u root -p -h 127.0.0.1



```


### MySQL kubernetes 相关

```bash

# 测试将文件挂载到 kubernetes pod 中
# 将本地文件 /opt/k8s/volume_data/busybox/busybox.conf 挂载到容器 /home/busybox.conf
# 要提前将相关目录和文件准备好

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: busybox-deploy
spec:
  replicas: 1
  template:
    metadata:
      labels:
        deploy: busybox
    spec:
      containers:
      - name: busybox
        image: busybox:latest
        command:
        - sleep
        - "360000"
        volumeMounts:
        - mountPath: /home/busybox.conf
          name: conf
          subPath: busybox.conf  # 需要提前将 /opt/k8s/volume_data/busybox/busybox.conf 文件创建好
      volumes:
      - name: conf
        hostPath:
          path: /opt/k8s/volume_data/busybox/  # 需要提前创建该目录

总结：
1、subPath 指令可以挂载子目录或者文件
2、pod 启动之前需要提前创建相关目录和文件，要在所有的 kubernetes worker 节点上创建，因为不知道 pod 会被调度到哪个节点上



# 提前准备 MySQL 配置文件
[root@k8s-linux-worker4 volume_data]# cat mysql-config/my.cnf
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

character-set-server=utf8
collation-server=utf8_bin

default-storage-engine=INNODB

max_allowed_packet=256M

innodb_log_file_size=1GB

sql_mode = NO_AUTO_VALUE_ON_ZERO

transaction-isolation=READ-COMMITTED

binlog_format=row


# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

[root@k8s-linux-worker4 volume_data]# 


[root@k8s-master1 temp]# vim mysql-deployment.yml 
[root@k8s-master1 temp]# cat mysql-deployment.yml 
---
apiVersion: v1
kind: Service
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  ports:
    - port: 3306
  selector:
    app: confluence
    tier: mysql
---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: confluence
        tier: mysql
    spec:
      containers:
        - image: mysql/mysql-server:5.7
          name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: rootpass
          ports:
            - containerPort: 3306
              name: mysql
          volumeMounts:
            - name: mysql-config
              subPath: my.cnf
              mountPath: /etc/my.cnf

            - name: mysql-log  # mysqld.log 文件不要提前创建（要测试确定一下）
              subPath: mysqld.log
              mountPath: /var/log/mysqld.log

            - name: mysql-data
              mountPath: /var/lib/mysql

      volumes:
        - name: mysql-config
          hostPath:
            path: /opt/k8s/volume_data/mysql-config/  # 需要提前创建并且准备好 my.cnf 文件，修改用户和用户组为 mysql

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/mysql-log/  # 需要提前创建，修改用户和用户组为 mysql

        - name: mysql-data
          hostPath:
            path: /opt/k8s/volume_data/mysql-data  # 需要提前创建，修改用户和用户组为 mysql

[root@k8s-master1 temp]# 


# 将 Deployment 和 Service 部署成功后启动新的 pod 测试 MySQL 是否可以连接
# 在连接之前还是要进入 MySQL 的 pod 中修改 root 权限允许远程登录（后续要通过 pod 生命周期的相关指令自动执行 MySQL 中的授权指令）

[root@k8s-master1 temp]# kubectl run -i -t mysql-test --image=mysql/mysql-server:5.7 --restart=Never bash
If you don't see a command prompt, try pressing enter.
bash-4.2# 
bash-4.2# env
HOSTNAME=mysql-test
TERM=xterm
KUBERNETES_PORT=tcp://10.68.0.1:443
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_HOST=10.68.0.1
CONFLUENCE_MYSQL_PORT_3306_TCP_PORT=3306
CONFLUENCE_MYSQL_PORT_3306_TCP=tcp://10.68.89.209:3306
CONFLUENCE_MYSQL_PORT_3306_TCP_PROTO=tcp
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CONFLUENCE_MYSQL_SERVICE_HOST=10.68.89.209
CONFLUENCE_MYSQL_SERVICE_PORT=3306
PWD=/
CONFLUENCE_MYSQL_PORT=tcp://10.68.89.209:3306
HOME=/root
SHLVL=1
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_SERVICE_PORT_HTTPS=443
CONFLUENCE_MYSQL_PORT_3306_TCP_ADDR=10.68.89.209
KUBERNETES_PORT_443_TCP_ADDR=10.68.0.1
KUBERNETES_PORT_443_TCP=tcp://10.68.0.1:443
_=/usr/bin/env
bash-4.2# mysql -u root -p -h 10.68.89.209 -P 3306
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 17
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
mysql> 
mysql> 
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> 
mysql> select * from user\G



# 容器生命周期
# 通过 pod 生命周期的相关指令自动执行 MySQL 中的授权指令（不成功）
apiVersion: v1
kind: Pod
metadata:
  name: mysql-test
spec:
  containers:
  - name: mysql-test
    image: mysql/mysql-server:5.7
    lifecycle:
      postStart:
        exec:
          command: ["mysql", "-u", "root", "-p", "-e", "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpassword';", "&&", "mysql", "-u", "root", "-p", "-e", "flush privileges;"]
      preStop:
        exec:
          command: ["/usr/sbin/nginx","-s","quit"]

# 可以在 /docker-entrypoint-initdb.d/ 目录中放置相关脚本，待容器启动后执行脚本做初始化的工作

```

### 在 k8s 上部署 MySQL 相关探索

```bash

# 在 k8s 中使用持久卷和持久卷声明（在持久卷中定义卷容量、权限、使用的后端存储等信息，在持久卷声明中定义要使用的容量和权限，k8s 会自动对持久卷和持久卷声明进行绑定）
[root@k8s-master1 temp]# vim volume.yml 
[root@k8s-master1 temp]# cat volume.yml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-volume-1
  labels:
    type: local
spec:
  capacity:
    storage: 5Mi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /opt/k8s/volume_data/lv-1
  persistentVolumeReclaimPolicy: Recycle
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-volume-2
  labels:
    type: local
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /opt/k8s/volume_data/lv-2
  persistentVolumeReclaimPolicy: Recycle
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-volume-3
  labels:
    type: local
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /opt/k8s/volume_data/lv-3
  persistentVolumeReclaimPolicy: Recycle

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-config-claim
  labels:
    app: confluence
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Mi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-log-claim
  labels:
    app: confluence
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-data-claim
  labels:
    app: confluence
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
---

[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# kubectl apply -f ./volume.yml 
persistentvolume/local-volume-1 created
persistentvolume/local-volume-2 created
persistentvolume/local-volume-3 created
persistentvolumeclaim/mysql-config-claim created
persistentvolumeclaim/mysql-log-claim created
persistentvolumeclaim/mysql-data-claim created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 

# 持久卷信息（此时持久卷已经绑定）
[root@k8s-master1 temp]# kubectl get pv -o wide
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                        STORAGECLASS   REASON   AGE
local-volume-1   5Mi        RWO            Recycle          Bound    default/mysql-config-claim                           56s
local-volume-2   5Gi        RWO            Recycle          Bound    default/mysql-log-claim                              56s
local-volume-3   20Gi       RWO            Recycle          Bound    default/mysql-data-claim                             56s
[root@k8s-master1 temp]# 
# 持久卷声明信息
[root@k8s-master1 temp]# kubectl get pvc -o wide
NAME                 STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-config-claim   Bound    local-volume-1   5Mi        RWO                           60s
mysql-data-claim     Bound    local-volume-3   20Gi       RWO                           60s
mysql-log-claim      Bound    local-volume-2   5Gi        RWO                           60s
[root@k8s-master1 temp]# 

# 详细信息
[root@k8s-master1 temp]# kubectl describe pv local-volume-1
Name:            local-volume-1
Labels:          type=local
Annotations:     kubectl.kubernetes.io/last-applied-configuration:
                   {"apiVersion":"v1","kind":"PersistentVolume","metadata":{"annotations":{},"labels":{"type":"local"},"name":"local-volume-1"},"spec":{"acce...
                 pv.kubernetes.io/bound-by-controller: yes
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    
Status:          Bound
Claim:           default/mysql-config-claim
Reclaim Policy:  Recycle
Access Modes:    RWO
VolumeMode:      Filesystem
Capacity:        5Mi
Node Affinity:   <none>
Message:         
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/k8s/volume_data/lv-1
    HostPathType:  
Events:            <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl describe pvc mysql-config-claim
Name:          mysql-config-claim
Namespace:     default
StorageClass:  
Status:        Bound
Volume:        local-volume-1
Labels:        app=confluence
Annotations:   kubectl.kubernetes.io/last-applied-configuration:
                 {"apiVersion":"v1","kind":"PersistentVolumeClaim","metadata":{"annotations":{},"labels":{"app":"confluence"},"name":"mysql-config-claim","...
               pv.kubernetes.io/bind-completed: yes
               pv.kubernetes.io/bound-by-controller: yes
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:      5Mi
Access Modes:  RWO
VolumeMode:    Filesystem
Events:        <none>
Mounted By:    <none>
[root@k8s-master1 temp]# 


# 在所有的 worker 节点上下载 MySQL 镜像
docker pull mysql/mysql-server:5.7

# 定义 MySQL 在 k8s 上的相关资源（使用持久卷声明挂载相关文件或目录）
[root@k8s-master1 temp]# cat mysql-deployment.yml
---
apiVersion: v1
kind: Service
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  ports:
    - port: 3306
  selector:
    app: confluence
    tier: mysql
---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: confluence
        tier: mysql
    spec:
      containers:
        - image: mysql/mysql-server
          name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: rootpass
          ports:
            - containerPort: 3306
              name: mysql
          volumeMounts:
            - name: mysql-config
              mountPath: /etc/  # 配置错误，挂载文件应该使用文件全路径 /etc/my.cnf
              subPath: my.cnf
            - name: mysql-log
              mountPath: /var/log/  # 配置错误，挂载文件应该使用文件全路径 /var/log/mysqld.log
              subPath: mysqld.log
            - name: mysql-data
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-config
          persistentVolumeClaim:
            claimName: mysql-config-claim
        - name: mysql-log
          persistentVolumeClaim:
            claimName: mysql-log-claim
        - name: mysql-data
          persistentVolumeClaim:
            claimName: mysql-data-claim

[root@k8s-master1 temp]# 


[root@k8s-master1 temp]# kubectl apply -f ./mysql-deployment.yml
service/confluence-mysql created
deployment.extensions/confluence-mysql created
[root@k8s-master1 temp]#

# 查看相关信息
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE   SELECTOR
confluence-mysql   ClusterIP   10.68.8.175   <none>        3306/TCP   25s   app=confluence,tier=mysql
kubernetes         ClusterIP   10.68.0.1     <none>        443/TCP    8d    <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES               SELECTOR
confluence-mysql   0/1     1            0           47s   mysql        mysql/mysql-server   app=confluence,tier=mysql
my-nginx           8/8     8            8           8h    my-nginx     nginx                run=my-nginx
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# kubectl describe deployment confluence-mysql
Name:               confluence-mysql
Namespace:          default
CreationTimestamp:  Wed, 29 May 2019 18:56:15 +0800
Labels:             app=confluence
Annotations:        deployment.kubernetes.io/revision: 1
                    kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"extensions/v1beta1","kind":"Deployment","metadata":{"annotations":{},"labels":{"app":"confluence"},"name":"confluence-mysql...
Selector:           app=confluence,tier=mysql
Replicas:           1 desired | 1 updated | 1 total | 0 available | 1 unavailable
StrategyType:       Recreate
MinReadySeconds:    0
Pod Template:
  Labels:  app=confluence
           tier=mysql
  Containers:
   mysql:
    Image:      mysql/mysql-server
    Port:       3306/TCP
    Host Port:  0/TCP
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
    Mounts:
      /etc/ from mysql-config (rw,path="my.cnf")
      /var/lib/mysql from mysql-data (rw)
      /var/log/ from mysql-log (rw,path="mysqld.log")
  Volumes:
   mysql-config:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-config-claim
    ReadOnly:   false
   mysql-log:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-log-claim
    ReadOnly:   false
   mysql-data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-data-claim
    ReadOnly:   false
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
OldReplicaSets:  confluence-mysql-6c8b94bc45 (1/1 replicas created)
NewReplicaSet:   <none>
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  2m40s  deployment-controller  Scaled up replica set confluence-mysql-6c8b94bc45 to 1
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 

# 相关 pod 创建失败
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                READY   STATUS                       RESTARTS   AGE    IP            NODE         NOMINATED NODE   READINESS GATES
confluence-mysql-6c8b94bc45-c7h6r   0/1     CreateContainerConfigError   0          4m2s   172.20.2.10   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg           1/1     Running                      0          8h     172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv           1/1     Running                      0          8h     172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l           1/1     Running                      0          8h     172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq           1/1     Running                      0          8h     172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww           1/1     Running                      0          8h     172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj           1/1     Running                      0          8h     172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p           1/1     Running                      0          8h     172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq           1/1     Running                      0          8h     172.20.3.3    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# kubectl describe pod confluence-mysql-6c8b94bc45-c7h6r
Name:           confluence-mysql-6c8b94bc45-c7h6r
Namespace:      default
Node:           10.1.36.48/10.1.36.48
Start Time:     Wed, 29 May 2019 18:56:15 +0800
Labels:         app=confluence
                pod-template-hash=6c8b94bc45
                tier=mysql
Annotations:    <none>
Status:         Pending
IP:             172.20.2.10
Controlled By:  ReplicaSet/confluence-mysql-6c8b94bc45
Containers:
  mysql:
    Container ID:   
    Image:          mysql/mysql-server
    Image ID:       
    Port:           3306/TCP
    Host Port:      0/TCP
    State:          Waiting
      Reason:       CreateContainerConfigError
    Ready:          False
    Restart Count:  0
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
    Mounts:
      /etc/ from mysql-config (rw,path="my.cnf")
      /var/lib/mysql from mysql-data (rw)
      /var/log/ from mysql-log (rw,path="mysqld.log")
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-lz2dc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  mysql-config:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-config-claim
    ReadOnly:   false
  mysql-log:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-log-claim
    ReadOnly:   false
  mysql-data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-data-claim
    ReadOnly:   false
  default-token-lz2dc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-lz2dc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     <none>
Events:
  Type     Reason          Age                    From                 Message
  ----     ------          ----                   ----                 -------
  Normal   Scheduled       5m11s                  default-scheduler    Successfully assigned default/confluence-mysql-6c8b94bc45-c7h6r to 10.1.36.48
  Normal   SandboxChanged  4m48s (x2 over 4m54s)  kubelet, 10.1.36.48  Pod sandbox changed, it will be killed and re-created.
  Warning  Failed          3m51s (x7 over 4m54s)  kubelet, 10.1.36.48  Error: stat /opt/k8s/volume_data/lv-1: no such file or directory
  Normal   Pulling         3m40s (x8 over 5m10s)  kubelet, 10.1.36.48  Pulling image "mysql/mysql-server"
  Normal   Pulled          3m35s (x8 over 4m54s)  kubelet, 10.1.36.48  Successfully pulled image "mysql/mysql-server"
[root@k8s-master1 temp]# 

1、pod 被调度到 10.1.36.48 节点上，所以在 10.1.36.48 节点上要有相关的目录和文件。由于无法提前确定 pod 会被调度到哪个节点，所以最好在所有节点都创建好相关文件和目录
2、镜像配置错误，应该使用 mysql/mysql-server:5.7

# 在 10.1.36.48 节点创建目录，检查 pod 是否可以正常启动
[root@k8s-linux-worker3 volume_data]# mkdir lv-1
[root@k8s-linux-worker3 volume_data]# mkdir lv-2
[root@k8s-linux-worker3 volume_data]# mkdir lv-3

# pod 还是启动不成功并且 event 没有显示错误信息
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                READY   STATUS             RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-mysql-6c8b94bc45-c7h6r   0/1     CrashLoopBackOff   5          9m50s   172.20.2.10   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg           1/1     Running            0          8h      172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv           1/1     Running            0          8h      172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l           1/1     Running            0          8h      172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq           1/1     Running            0          8h      172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww           1/1     Running            0          8h      172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj           1/1     Running            0          8h      172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p           1/1     Running            0          8h      172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq           1/1     Running            0          8h      172.20.3.3    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl describe pod confluence-mysql-6c8b94bc45-c7h6r
Name:           confluence-mysql-6c8b94bc45-c7h6r
Namespace:      default
Node:           10.1.36.48/10.1.36.48
Start Time:     Wed, 29 May 2019 18:56:15 +0800
Labels:         app=confluence
                pod-template-hash=6c8b94bc45
                tier=mysql
Annotations:    <none>
Status:         Running
IP:             172.20.2.10
Controlled By:  ReplicaSet/confluence-mysql-6c8b94bc45
Containers:
  mysql:
    Container ID:   docker://dc8b0784bf5ddd6cac4359fb9b1fd6b5b4820907498e2c073b7c4f730488cddf
    Image:          mysql/mysql-server
    Image ID:       docker-pullable://mysql/mysql-server@sha256:8dd16a45d0e3e789f2006b608abb1bb69f1a8632a338eef89aec8d6fccda7793
    Port:           3306/TCP
    Host Port:      0/TCP
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    2
      Started:      Wed, 29 May 2019 19:05:33 +0800
      Finished:     Wed, 29 May 2019 19:05:33 +0800
    Ready:          False
    Restart Count:  5
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
    Mounts:
      /etc/ from mysql-config (rw,path="my.cnf")
      /var/lib/mysql from mysql-data (rw)
      /var/log/ from mysql-log (rw,path="mysqld.log")
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-lz2dc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  mysql-config:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-config-claim
    ReadOnly:   false
  mysql-log:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-log-claim
    ReadOnly:   false
  mysql-data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-data-claim
    ReadOnly:   false
  default-token-lz2dc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-lz2dc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     <none>
Events:
  Type     Reason          Age                    From                 Message
  ----     ------          ----                   ----                 -------
  Normal   Scheduled       10m                    default-scheduler    Successfully assigned default/confluence-mysql-6c8b94bc45-c7h6r to 10.1.36.48
  Normal   SandboxChanged  9m40s (x2 over 9m46s)  kubelet, 10.1.36.48  Pod sandbox changed, it will be killed and re-created.
  Warning  Failed          8m43s (x7 over 9m46s)  kubelet, 10.1.36.48  Error: stat /opt/k8s/volume_data/lv-1: no such file or directory
  Normal   Pulled          8m27s (x8 over 9m46s)  kubelet, 10.1.36.48  Successfully pulled image "mysql/mysql-server"
  Normal   Pulling         4m52s (x21 over 10m)   kubelet, 10.1.36.48  Pulling image "mysql/mysql-server"
[root@k8s-master1 temp]# 

# 删除 deployment 重新创建
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES               SELECTOR
confluence-mysql   0/1     1            0           20m   mysql        mysql/mysql-server   app=confluence,tier=mysql
my-nginx           8/8     8            8           8h    my-nginx     nginx                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl delete deployment confluence-mysql
deployment.extensions "confluence-mysql" deleted
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
my-nginx   8/8     8            8           8h    my-nginx     nginx    run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
my-nginx-86459cfc9f-29wdg   1/1     Running   0          8h    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv   1/1     Running   0          8h    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l   1/1     Running   0          8h    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq   1/1     Running   0          8h    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww   1/1     Running   0          8h    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj   1/1     Running   0          8h    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p   1/1     Running   0          8h    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq   1/1     Running   0          8h    172.20.3.3    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# vim  mysql-deployment.yml 
[root@k8s-master1 temp]# cat  mysql-deployment.yml 
---
apiVersion: v1
kind: Service
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  ports:
    - port: 3306
  selector:
    app: confluence
    tier: mysql
---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: confluence
        tier: mysql
    spec:
      containers:
        - image: mysql/mysql-server
          name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: rootpass
          ports:
            - containerPort: 3306
              name: mysql
          volumeMounts:
            - name: mysql-config
              mountPath: /etc/my.cnf
              subPath: my.cnf
            - name: mysql-log
              mountPath: /var/log/mysqld.log  # 正确的路径定义
              subPath: mysqld.log
            - name: mysql-data
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-config
          persistentVolumeClaim:
            claimName: mysql-config-claim
        - name: mysql-log
          persistentVolumeClaim:
            claimName: mysql-log-claim
        - name: mysql-data
          persistentVolumeClaim:
            claimName: mysql-data-claim

[root@k8s-master1 temp]# 


[root@k8s-master1 temp]# kubectl apply -f ./mysql-deployment.yml 
service/confluence-mysql unchanged
deployment.extensions/confluence-mysql created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES               SELECTOR
confluence-mysql   0/1     1            0           11s   mysql        mysql/mysql-server   app=confluence,tier=mysql
my-nginx           8/8     8            8           8h    my-nginx     nginx                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES               SELECTOR
confluence-mysql   0/1     1            0           15s   mysql        mysql/mysql-server   app=confluence,tier=mysql
my-nginx           8/8     8            8           8h    my-nginx     nginx                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                READY   STATUS                       RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
confluence-mysql-6b656b7946-rqvzc   0/1     CreateContainerConfigError   0          25s   172.20.3.4    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-29wdg           1/1     Running                      0          8h    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv           1/1     Running                      0          8h    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l           1/1     Running                      0          8h    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq           1/1     Running                      0          8h    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww           1/1     Running                      0          8h    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj           1/1     Running                      0          8h    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p           1/1     Running                      0          8h    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq           1/1     Running                      0          8h    172.20.3.3    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl describe pod confluence-mysql-6b656b7946-rqvzc
Name:           confluence-mysql-6b656b7946-rqvzc
Namespace:      default
Node:           10.1.36.49/10.1.36.49
Start Time:     Wed, 29 May 2019 19:19:01 +0800
Labels:         app=confluence
                pod-template-hash=6b656b7946
                tier=mysql
Annotations:    <none>
Status:         Running
IP:             172.20.3.4
Controlled By:  ReplicaSet/confluence-mysql-6b656b7946
Containers:
  mysql:
    Container ID:   docker://bdc2a9971b0122c7bb75c3b0797520edaf4dde862afa2ed95144d01effb2213c
    Image:          mysql/mysql-server
    Image ID:       docker-pullable://mysql/mysql-server@sha256:8dd16a45d0e3e789f2006b608abb1bb69f1a8632a338eef89aec8d6fccda7793
    Port:           3306/TCP
    Host Port:      0/TCP
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       ContainerCannotRun
      Message:      OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/8f9fa339-8203-11e9-8f1f-0017fa00a076/volume-subpaths/local-volume-1/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/20df11e8d1eff54623c7a60c34fca8acbf07c08f4ccf89752cf47bd5bc25d84c/merged\\\" at \\\"/opt/k8s/docker/overlay2/20df11e8d1eff54623c7a60c34fca8acbf07c08f4ccf89752cf47bd5bc25d84c/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
      Exit Code:    127
      Started:      Wed, 29 May 2019 19:24:23 +0800
      Finished:     Wed, 29 May 2019 19:24:23 +0800
    Ready:          False
    Restart Count:  5
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
    Mounts:
      /etc/my.cnf from mysql-config (rw,path="my.cnf")
      /var/lib/mysql from mysql-data (rw)
      /var/log/mysqld.log from mysql-log (rw,path="mysqld.log")
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-lz2dc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  mysql-config:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-config-claim
    ReadOnly:   false
  mysql-log:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-log-claim
    ReadOnly:   false
  mysql-data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-data-claim
    ReadOnly:   false
  default-token-lz2dc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-lz2dc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     <none>
Events:
  Type     Reason     Age                    From                 Message
  ----     ------     ----                   ----                 -------
  Normal   Scheduled  8m15s                  default-scheduler    Successfully assigned default/confluence-mysql-6b656b7946-rqvzc to 10.1.36.49
  Warning  Failed     7m16s (x4 over 7m57s)  kubelet, 10.1.36.49  Error: stat /opt/k8s/volume_data/lv-1: no such file or directory
  Warning  Failed     6m59s                  kubelet, 10.1.36.49  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/8f9fa339-8203-11e9-8f1f-0017fa00a076/volume-subpaths/local-volume-1/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/e64e7aebd2b9bb0d4df44f2c3bdcf4ca44bfd4a063aedd6ab8276a870dc8396d/merged\\\" at \\\"/opt/k8s/docker/overlay2/e64e7aebd2b9bb0d4df44f2c3bdcf4ca44bfd4a063aedd6ab8276a870dc8396d/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     6m34s                  kubelet, 10.1.36.49  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/8f9fa339-8203-11e9-8f1f-0017fa00a076/volume-subpaths/local-volume-1/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/e8c8cc76a7403ae41d7888bb2227a139a1f410dbd3b08692275e90962dd3289c/merged\\\" at \\\"/opt/k8s/docker/overlay2/e8c8cc76a7403ae41d7888bb2227a139a1f410dbd3b08692275e90962dd3289c/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     6m15s                  kubelet, 10.1.36.49  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/8f9fa339-8203-11e9-8f1f-0017fa00a076/volume-subpaths/local-volume-1/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/293bb6e0071f70b9bd00cc4675150acbc9bbdea362cd7f83a1ebb8f17c4780ff/merged\\\" at \\\"/opt/k8s/docker/overlay2/293bb6e0071f70b9bd00cc4675150acbc9bbdea362cd7f83a1ebb8f17c4780ff/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Normal   Pulled     6m15s (x7 over 7m57s)  kubelet, 10.1.36.49  Successfully pulled image "mysql/mysql-server"
  Normal   Created    6m15s (x3 over 7m)     kubelet, 10.1.36.49  Created container mysql
  Warning  BackOff    6m12s                  kubelet, 10.1.36.49  Back-off restarting failed container
  Normal   Pulling    3m2s (x10 over 8m14s)  kubelet, 10.1.36.49  Pulling image "mysql/mysql-server"
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 

1、在重新创建 Deployment 之前已经建立了相关的目录，但是没有创建 my.cnf 和 mysqld.log，有可能是没有创建目录导致 k8s 将 my.cnf 和 mysqld.log 看做目录，而将目录挂载到文件就会不成功
2、在使用持久卷和持久卷声明有可能不能挂载文件，这也可能是失败的原因

# 删除 deployment 重新创建
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES               SELECTOR
confluence-mysql   0/1     1            0           14m   mysql        mysql/mysql-server   app=confluence,tier=mysql
my-nginx           8/8     8            8           8h    my-nginx     nginx                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl delete deployment confluence-mysql
deployment.extensions "confluence-mysql" deleted
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
my-nginx   8/8     8            8           8h    my-nginx     nginx    run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
my-nginx-86459cfc9f-29wdg   1/1     Running   0          8h    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv   1/1     Running   0          8h    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l   1/1     Running   0          8h    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq   1/1     Running   0          8h    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww   1/1     Running   0          8h    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj   1/1     Running   0          8h    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p   1/1     Running   0          8h    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq   1/1     Running   0          8h    172.20.3.3    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 


# 不使用持久卷和持久卷声明，删除持久卷之前要先删除与之绑定的持久卷声明
[root@k8s-master1 temp]# kubectl get pv -o wide
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                        STORAGECLASS   REASON   AGE
local-volume-1   5Mi        RWO            Recycle          Bound    default/mysql-config-claim                           70m
local-volume-2   5Gi        RWO            Recycle          Bound    default/mysql-log-claim                              70m
local-volume-3   20Gi       RWO            Recycle          Bound    default/mysql-data-claim                             70m
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pvc -o wide
NAME                 STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-config-claim   Bound    local-volume-1   5Mi        RWO                           71m
mysql-data-claim     Bound    local-volume-3   20Gi       RWO                           71m
mysql-log-claim      Bound    local-volume-2   5Gi        RWO                           71m
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl delete pvc mysql-config-claim
persistentvolumeclaim "mysql-config-claim" deleted
[root@k8s-master1 temp]# kubectl delete pvc mysql-log-claim
persistentvolumeclaim "mysql-log-claim" deleted
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pvc -o wide
NAME               STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-data-claim   Bound    local-volume-3   20Gi       RWO                           71m
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pv -o wide
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                      STORAGECLASS   REASON   AGE
local-volume-1   5Mi        RWO            Recycle          Available                                                      71m
local-volume-2   5Gi        RWO            Recycle          Available                                                      71m
local-volume-3   20Gi       RWO            Recycle          Bound       default/mysql-data-claim                           71m
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl delete pv local-volume-1
persistentvolume "local-volume-1" deleted
[root@k8s-master1 temp]# kubectl delete pv local-volume-2
persistentvolume "local-volume-2" deleted
[root@k8s-master1 temp]# kubectl get pv -o wide
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                      STORAGECLASS   REASON   AGE
local-volume-3   20Gi       RWO            Recycle          Bound    default/mysql-data-claim                           72m
[root@k8s-master1 temp]# 



# 清理节点环境，重新部署 deployment
[root@k8s-linux-worker4 volume_data]# rm -rf lv-1/*
[root@k8s-linux-worker4 volume_data]# rm -rf lv-2/*
[root@k8s-linux-worker4 volume_data]# rm -rf lv-3/*
[root@k8s-linux-worker4 volume_data]# 

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# rm -rf mysql-deployment.yml 
[root@k8s-master1 temp]# vim mysql-deployment.yml 
[root@k8s-master1 temp]# cat mysql-deployment.yml 
---
apiVersion: v1
kind: Service
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  ports:
    - port: 3306
  selector:
    app: confluence
    tier: mysql
---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: confluence-mysql
  labels:
    app: confluence
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: confluence
        tier: mysql
    spec:
      containers:
        - image: mysql/mysql-server
          name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: rootpass
          ports:
            - containerPort: 3306
              name: mysql
          volumeMounts:
            - name: mysql-config
              mountPath: /etc/my.cnf
              subPath: my.cnf
            - name: mysql-log
              mountPath: /var/log/mysqld.log
              subPath: mysqld.log
            - name: mysql-data
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-config
          hostPath:
            path: /opt/k8s/volume_data/lv-1/

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/lv-2/

        - name: mysql-data
          persistentVolumeClaim:
            claimName: mysql-data-claim

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f  ./mysql-deployment.yml 
service/confluence-mysql unchanged
deployment.extensions/confluence-mysql created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME               READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES               SELECTOR
confluence-mysql   0/1     1            0           12s   mysql        mysql/mysql-server   app=confluence,tier=mysql
my-nginx           8/8     8            8           9h    my-nginx     nginx                run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                READY   STATUS              RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
confluence-mysql-7f8fbbc47c-6t6gk   0/1     RunContainerError   0          21s   172.20.2.11   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg           1/1     Running             0          9h    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv           1/1     Running             0          9h    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l           1/1     Running             0          9h    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq           1/1     Running             0          9h    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww           1/1     Running             0          9h    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj           1/1     Running             0          9h    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p           1/1     Running             0          9h    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq           1/1     Running             0          9h    172.20.3.3    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 


[root@k8s-master1 temp]# kubectl describe pod confluence-mysql-7f8fbbc47c-6t6gk
Name:           confluence-mysql-7f8fbbc47c-6t6gk
Namespace:      default
Node:           10.1.36.48/10.1.36.48
Start Time:     Wed, 29 May 2019 19:38:56 +0800
Labels:         app=confluence
                pod-template-hash=7f8fbbc47c
                tier=mysql
Annotations:    <none>
Status:         Running
IP:             172.20.2.11
Controlled By:  ReplicaSet/confluence-mysql-7f8fbbc47c
Containers:
  mysql:
    Container ID:   docker://963a6b6d7dd1ec61e0227097089da3c6459e4b8957a58ff310263c62f6876c63
    Image:          mysql/mysql-server
    Image ID:       docker-pullable://mysql/mysql-server@sha256:8dd16a45d0e3e789f2006b608abb1bb69f1a8632a338eef89aec8d6fccda7793
    Port:           3306/TCP
    Host Port:      0/TCP
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       ContainerCannotRun
      Message:      OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/57b55f66-8206-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-config/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/9bdfe585563bb23470be3d34283f1771235a48ee0d78a6bef4c71d2d7fab2751/merged\\\" at \\\"/opt/k8s/docker/overlay2/9bdfe585563bb23470be3d34283f1771235a48ee0d78a6bef4c71d2d7fab2751/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
      Exit Code:    127
      Started:      Wed, 29 May 2019 19:45:05 +0800
      Finished:     Wed, 29 May 2019 19:45:05 +0800
    Ready:          False
    Restart Count:  6
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpass
    Mounts:
      /etc/my.cnf from mysql-config (rw,path="my.cnf")
      /var/lib/mysql from mysql-data (rw)
      /var/log/mysqld.log from mysql-log (rw,path="mysqld.log")
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-lz2dc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  mysql-config:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/k8s/volume_data/lv-1/
    HostPathType:  
  mysql-log:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/k8s/volume_data/lv-2/
    HostPathType:  
  mysql-data:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mysql-data-claim
    ReadOnly:   false
  default-token-lz2dc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-lz2dc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     <none>
Events:
  Type     Reason     Age                     From                 Message
  ----     ------     ----                    ----                 -------
  Normal   Scheduled  9m19s                   default-scheduler    Successfully assigned default/confluence-mysql-7f8fbbc47c-6t6gk to 10.1.36.48
  Warning  Failed     9m13s                   kubelet, 10.1.36.48  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/57b55f66-8206-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-config/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/0d319139f32c4e8503ebda4075c8ff27f0e5177477758450de5b2effb8ddddd4/merged\\\" at \\\"/opt/k8s/docker/overlay2/0d319139f32c4e8503ebda4075c8ff27f0e5177477758450de5b2effb8ddddd4/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     9m8s                    kubelet, 10.1.36.48  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/57b55f66-8206-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-config/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/498fe0f7455549b8ab435bfb59d1816123d9ae1f4de7c71d34fae50f90f54329/merged\\\" at \\\"/opt/k8s/docker/overlay2/498fe0f7455549b8ab435bfb59d1816123d9ae1f4de7c71d34fae50f90f54329/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     8m51s                   kubelet, 10.1.36.48  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/57b55f66-8206-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-config/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/2efb544ba888d0e29ba22b3e0b3bd316a7fb9445a78da9df403ec330c5940cf5/merged\\\" at \\\"/opt/k8s/docker/overlay2/2efb544ba888d0e29ba22b3e0b3bd316a7fb9445a78da9df403ec330c5940cf5/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     8m26s                   kubelet, 10.1.36.48  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/57b55f66-8206-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-config/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/a887fa8798660b91c87410e52ab77d782c15f4499cac893666bdd37a3cc8c5fd/merged\\\" at \\\"/opt/k8s/docker/overlay2/a887fa8798660b91c87410e52ab77d782c15f4499cac893666bdd37a3cc8c5fd/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Normal   Pulling    7m35s (x5 over 9m18s)   kubelet, 10.1.36.48  Pulling image "mysql/mysql-server"
  Normal   Created    7m30s (x5 over 9m14s)   kubelet, 10.1.36.48  Created container mysql
  Normal   Pulled     7m30s (x5 over 9m14s)   kubelet, 10.1.36.48  Successfully pulled image "mysql/mysql-server"
  Warning  Failed     7m30s                   kubelet, 10.1.36.48  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/57b55f66-8206-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-config/mysql/0\\\" to rootfs \\\"/opt/k8s/docker/overlay2/81352db59cd51a0fc2de4779fe50e7f385f28edad31c602bf88a633d41402309/merged\\\" at \\\"/opt/k8s/docker/overlay2/81352db59cd51a0fc2de4779fe50e7f385f28edad31c602bf88a633d41402309/merged/etc/my.cnf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  BackOff    4m17s (x21 over 8m38s)  kubelet, 10.1.36.48  Back-off restarting failed container
[root@k8s-master1 temp]# 

1、在重新创建 Deployment 之前已经建立了相关的目录，但是没有创建 my.cnf 和 mysqld.log，有可能是没有创建目录导致 k8s 将 my.cnf 和 mysqld.log 看做目录，而将目录挂载到文件就会不成功

[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME               READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES               SELECTOR
confluence-mysql   0/1     1            0           9m42s   mysql        mysql/mysql-server   app=confluence,tier=mysql
my-nginx           8/8     8            8           9h      my-nginx     nginx                run=my-nginx
[root@k8s-master1 temp]# kubectl delete deployment confluence-mysql
deployment.extensions "confluence-mysql" deleted
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
my-nginx-86459cfc9f-29wdg   1/1     Running   0          9h    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv   1/1     Running   0          9h    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l   1/1     Running   0          9h    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq   1/1     Running   0          9h    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww   1/1     Running   0          9h    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj   1/1     Running   0          9h    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p   1/1     Running   0          9h    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq   1/1     Running   0          9h    172.20.3.3    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 


后续操作：

1、在挂载文件时要提前将文件在宿主机上创建好（日志文件 mysqld.log 要不要创建还要测试）
2、使用持久卷和持久卷声明时也提前将目录和文件创建好，测试是否可以创建成功




my.cnf


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


kubectl create configmap edusoho-mysql-config --from-file=./my.cnf

[root@k8s-master1 temp]# kubectl create configmap edusoho-mysql-config --from-file=./my.cnf
configmap/edusoho-mysql-config created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get configmap -o wide
NAME                   DATA   AGE
edusoho-mysql-config   1      28s
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl describe configmap edusoho-mysql-config
Name:         edusoho-mysql-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
my.cnf:
----
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

Events:  <none>
[root@k8s-master1 temp]# 





[root@k8s-master1 ~]# kubectl get nodes
NAME         STATUS   ROLES    AGE     VERSION
10.1.36.46   Ready    <none>   15d     v1.14.0
10.1.36.47   Ready    <none>   9d      v1.14.0
10.1.36.48   Ready    <none>   9d      v1.14.0
10.1.36.49   Ready    <none>   7d10h   v1.14.0
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl get nodes -o wide
NAME         STATUS   ROLES    AGE     VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION               CONTAINER-RUNTIME
10.1.36.46   Ready    <none>   15d     v1.14.0   10.1.36.46    <none>        CentOS Linux 7 (Core)   3.10.0-862.11.6.el7.x86_64   docker://18.9.6
10.1.36.47   Ready    <none>   9d      v1.14.0   10.1.36.47    <none>        CentOS Linux 7 (Core)   3.10.0-862.11.6.el7.x86_64   docker://18.9.6
10.1.36.48   Ready    <none>   9d      v1.14.0   10.1.36.48    <none>        CentOS Linux 7 (Core)   3.10.0-862.11.6.el7.x86_64   docker://18.9.6
10.1.36.49   Ready    <none>   7d10h   v1.14.0   10.1.36.49    <none>        CentOS Linux 7 (Core)   3.10.0-862.11.6.el7.x86_64   docker://18.9.6
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl get nodes --show-labels
NAME         STATUS   ROLES    AGE     VERSION   LABELS
10.1.36.46   Ready    <none>   15d     v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.46,kubernetes.io/os=linux
10.1.36.47   Ready    <none>   9d      v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.47,kubernetes.io/os=linux
10.1.36.48   Ready    <none>   9d      v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.48,kubernetes.io/os=linux
10.1.36.49   Ready    <none>   7d10h   v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.49,kubernetes.io/os=linux
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl label nodes 10.1.36.46 nodename=k8s-linux-worker1
node/10.1.36.46 labeled
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl label nodes 10.1.36.47 nodename=k8s-linux-worker2
node/10.1.36.47 labeled
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl label nodes 10.1.36.48 nodename=k8s-linux-worker2
node/10.1.36.48 labeled
[root@k8s-master1 ~]# kubectl label nodes 10.1.36.48 nodename=k8s-linux-worker3
error: 'nodename' already has a value (k8s-linux-worker2), and --overwrite is false
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl label nodes 10.1.36.48 nodename=k8s-linux-worker3 --overwrite
node/10.1.36.48 labeled
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl label nodes 10.1.36.49 nodename=k8s-linux-worker4
node/10.1.36.49 labeled
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl get nodes --show-labels
NAME         STATUS   ROLES    AGE     VERSION   LABELS
10.1.36.46   Ready    <none>   15d     v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.46,kubernetes.io/os=linux,nodename=k8s-linux-worker1
10.1.36.47   Ready    <none>   9d      v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.47,kubernetes.io/os=linux,nodename=k8s-linux-worker2
10.1.36.48   Ready    <none>   9d      v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.48,kubernetes.io/os=linux,nodename=k8s-linux-worker3
10.1.36.49   Ready    <none>   7d10h   v1.14.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=10.1.36.49,kubernetes.io/os=linux,nodename=k8s-linux-worker4
[root@k8s-master1 ~]# 


[root@k8s-linux-worker2 volume_data]# ll mysql-config/
total 4
-rw-r--r-- 1 root root 1466 Jun  5 14:21 my.cnf
[root@k8s-linux-worker2 volume_data]# 
[root@k8s-linux-worker2 volume_data]# ll mysql-data/
total 0
[root@k8s-linux-worker2 volume_data]# ll mysql-log/
total 0
-rw-r--r-- 1 root root 0 May 30 15:43 mysqld.log
[root@k8s-linux-worker2 volume_data]# 
[root@k8s-linux-worker2 volume_data]# rm -rf mysql-log/mysqld.log 
[root@k8s-linux-worker2 volume_data]# ll


[root@k8s-master1 temp]# vim edusoho-mysql.yml
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# cat  edusoho-mysql.yml
---
apiVersion: v1
kind: Service
metadata:
  name: edusoho-mysql
  labels:
    app: edusoho
spec:
  ports:
    - port: 3306
  selector:
    app: edusoho
    tier: mysql
  type: NodePort

---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: edusoho-mysql
  labels:
    app: edusoho
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: edusoho
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
          nodeSelector:
            nodename:
              k8s-linux-worker2

          volumeMounts:
            - name: mysql-config
              subPath: my.cnf
              mountPath: /etc/my.cnf

            - name: mysql-log
              subPath: mysqld.log
              mountPath: /var/log/mysqld.log

            - name: mysql-data
              mountPath: /var/lib/mysql

      volumes:
        - name: mysql-config
          configMap:
            name: edusoho-mysql-config

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/mysql-log/

        - name: mysql-data
          hostPath:
            path: /opt/k8s/volume_data/mysql-data/

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f ./edusoho-mysql.yml
service/edusoho-mysql created
error: error validating "./edusoho-mysql.yml": error validating data: ValidationError(Deployment.spec.template.spec.containers[0]): unknown field "nodeSelector" in io.k8s.api.core.v1.Container; if you choose to ignore these errors, turn validation off with --validate=false
[root@k8s-master1 temp]# 

错误分析：


[root@k8s-master1 temp]# vim ./edusoho-mysql.yml
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# cat  edusoho-mysql.yml

---
apiVersion: v1
kind: Service
metadata:
  name: edusoho-mysql
  labels:
    app: edusoho
spec:
  ports:
    - port: 3306
  selector:
    app: edusoho
    tier: mysql
  type: NodePort

---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: edusoho-mysql
  labels:
    app: edusoho
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: edusoho
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
          k8s-linux-worker2

      volumes:
        - name: mysql-config
          configMap:
            name: edusoho-mysql-config

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/mysql-log/

        - name: mysql-data
          hostPath:
            path: /opt/k8s/volume_data/mysql-data/

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f ./edusoho-mysql.yml
service/edusoho-mysql unchanged
deployment.extensions/edusoho-mysql created
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# kubectl describe pod edusoho-mysql-fc4f549f5-qg69m
Name:           edusoho-mysql-fc4f549f5-qg69m
Namespace:      default
Node:           10.1.36.47/10.1.36.47
Start Time:     Wed, 05 Jun 2019 20:59:29 +0800
Labels:         app=edusoho
                pod-template-hash=fc4f549f5
                tier=mysql
Annotations:    <none>
Status:         Running
IP:             172.20.1.25
Controlled By:  ReplicaSet/edusoho-mysql-fc4f549f5
Containers:
  mysql:
    Container ID:   docker://44db92fa0eecde364f5380fe3a553e491da5ac5fee96818db69cf136c92c5af0
    Image:          mysql/mysql-server:5.7
    Image ID:       docker-pullable://mysql/mysql-server@sha256:ddb046076781a15200d36cb01f8f512431c3481bedebd5e92646d8c617ae212c
    Port:           3306/TCP
    Host Port:      0/TCP
    State:          Waiting
      Reason:       RunContainerError
    Last State:     Terminated
      Reason:       ContainerCannotRun
      Message:      OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/c18afb47-8791-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-log/mysql/1\\\" to rootfs \\\"/opt/k8s/docker/overlay2/7f101db1c23fc04fec52e14d33e6442738fc4295610e7aeac7b33efc37671037/merged\\\" at \\\"/opt/k8s/docker/overlay2/7f101db1c23fc04fec52e14d33e6442738fc4295610e7aeac7b33efc37671037/merged/var/log/mysqld.log\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
      Exit Code:    127
      Started:      Wed, 05 Jun 2019 21:02:28 +0800
      Finished:     Wed, 05 Jun 2019 21:02:28 +0800
    Ready:          False
    Restart Count:  5
    Environment:
      MYSQL_ROOT_PASSWORD:  rootpassword
    Mounts:
      /etc/my.cnf from mysql-config (rw,path="my.cnf")
      /var/lib/mysql from mysql-data (rw)
      /var/log/mysqld.log from mysql-log (rw,path="mysqld.log")
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-lz2dc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  mysql-config:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      edusoho-mysql-config
    Optional:  false
  mysql-log:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/k8s/volume_data/mysql-log/
    HostPathType:  
  mysql-data:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/k8s/volume_data/mysql-data/
    HostPathType:  
  default-token-lz2dc:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-lz2dc
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  nodename=k8s-linux-worker2
Tolerations:     <none>
Events:
  Type     Reason     Age                   From                 Message
  ----     ------     ----                  ----                 -------
  Normal   Scheduled  3m26s                 default-scheduler    Successfully assigned default/edusoho-mysql-fc4f549f5-qg69m to 10.1.36.47
  Warning  Failed     3m24s                 kubelet, 10.1.36.47  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/c18afb47-8791-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-log/mysql/1\\\" to rootfs \\\"/opt/k8s/docker/overlay2/f25332bb104e1a109d9648e2367d71d1897e864dbd21e87547a1a63232503c0d/merged\\\" at \\\"/opt/k8s/docker/overlay2/f25332bb104e1a109d9648e2367d71d1897e864dbd21e87547a1a63232503c0d/merged/var/log/mysqld.log\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     3m23s                 kubelet, 10.1.36.47  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/c18afb47-8791-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-log/mysql/1\\\" to rootfs \\\"/opt/k8s/docker/overlay2/2df94ab1f4d962275960099377a302b8c5ff5afad684dea7cdba09b0fe58e5ff/merged\\\" at \\\"/opt/k8s/docker/overlay2/2df94ab1f4d962275960099377a302b8c5ff5afad684dea7cdba09b0fe58e5ff/merged/var/log/mysqld.log\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     3m9s                  kubelet, 10.1.36.47  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/c18afb47-8791-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-log/mysql/1\\\" to rootfs \\\"/opt/k8s/docker/overlay2/07ee8dc9d8c208bb540fd716e4e1e0931ba04035417927ebdbecd00577a6c6f1/merged\\\" at \\\"/opt/k8s/docker/overlay2/07ee8dc9d8c208bb540fd716e4e1e0931ba04035417927ebdbecd00577a6c6f1/merged/var/log/mysqld.log\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  Failed     2m38s                 kubelet, 10.1.36.47  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/c18afb47-8791-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-log/mysql/1\\\" to rootfs \\\"/opt/k8s/docker/overlay2/c54ed7fd1b13e0321ed2a03d1d1ecfa98d152c612a165981ad9f9ba5c6f1a160/merged\\\" at \\\"/opt/k8s/docker/overlay2/c54ed7fd1b13e0321ed2a03d1d1ecfa98d152c612a165981ad9f9ba5c6f1a160/merged/var/log/mysqld.log\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Normal   Created    112s (x5 over 3m24s)  kubelet, 10.1.36.47  Created container mysql
  Normal   Pulled     112s (x5 over 3m25s)  kubelet, 10.1.36.47  Container image "mysql/mysql-server:5.7" already present on machine
  Warning  Failed     111s                  kubelet, 10.1.36.47  Error: failed to start container "mysql": Error response from daemon: OCI runtime create failed: container_linux.go:345: starting container process caused "process_linux.go:424: container init caused \"rootfs_linux.go:58: mounting \\\"/opt/k8s/kubelet/pods/c18afb47-8791-11e9-8f1f-0017fa00a076/volume-subpaths/mysql-log/mysql/1\\\" to rootfs \\\"/opt/k8s/docker/overlay2/cac1755678dc0367e40e346f442730c2f8ee28d4e9b5806c6dc6da0271b6f5e5/merged\\\" at \\\"/opt/k8s/docker/overlay2/cac1755678dc0367e40e346f442730c2f8ee28d4e9b5806c6dc6da0271b6f5e5/merged/var/log/mysqld.log\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type
  Warning  BackOff    73s (x10 over 3m23s)  kubelet, 10.1.36.47  Back-off restarting failed container
[root@k8s-master1 temp]# 

错误分析：

[root@k8s-linux-worker2 volume_data]# touch mysql-log/mysqld.log
[root@k8s-linux-worker2 volume_data]# 
[root@k8s-linux-worker2 volume_data]# chmod -R 777  mysql-log
[root@k8s-linux-worker2 volume_data]# 

[root@k8s-master1 temp]# kubectl apply -f ./edusoho-mysql.yml
service/edusoho-mysql unchanged
deployment.extensions/edusoho-mysql created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                                         SELECTOR
confluence-deployment   1/1     1            1           35h     confluence   atlassian/confluence-server:latest             app=confluence,service=confluence
confluence-mysql        0/1     1            0           6h44m   mysql        mysql/mysql-server:5.7                         app=confluence,tier=mysql
edusoho-mysql           1/1     1            1           6s      mysql        mysql/mysql-server:5.7                         app=edusoho,tier=mysql
jira-deployment         1/1     1            1           7h20m   jira         cptactionhank/atlassian-jira-software:latest   app=jira,service=jira
my-nginx                8/8     8            8           7d10h   my-nginx     nginx                                          run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS             RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-7577774698-psgz2   1/1     Running            0          35h     172.20.0.17   10.1.36.46   <none>           <none>
confluence-mysql-d464855bd-cp7sz         0/1     CrashLoopBackOff   80         6h44m   172.20.3.10   10.1.36.49   <none>           <none>
edusoho-mysql-fc4f549f5-hv9sw            1/1     Running            0          25s     172.20.1.26   10.1.36.47   <none>           <none>
jira-deployment-ccc84bffd-r9mzz          1/1     Running            0          7h21m   172.20.2.16   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running            0          7d10h   172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running            0          7d10h   172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running            0          7d10h   172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running            0          7d10h   172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running            0          7d10h   172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running            0          7d10h   172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running            0          7d10h   172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running            0          7d10h   172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     CrashLoopBackOff   71         5d11h   172.20.3.8    10.1.36.49   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   35h     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         6d3h    app=confluence,tier=mysql
edusoho-mysql      NodePort    10.68.125.174   <none>        3306:23160/TCP   15m     app=edusoho,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   7h22m   app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          15d     <none>
[root@k8s-master1 temp]# 


[root@k8s-linux-worker2 volume_data]# docker exec -ti d56b7b0f9a9f bash
bash-4.2# mysql -u root -p
Enter password: rootpassword
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 

mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpassword';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> 
mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)

mysql> exit
Bye
bash-4.2# 


# mysql service 去掉 type: NodePort
[root@k8s-master1 temp]# vim edusoho-mysql.yml 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# cat edusoho-mysql.yml 
---
apiVersion: v1
kind: Service
metadata:
  name: edusoho-mysql
  labels:
    app: edusoho
spec:
  ports:
    - port: 3306
  selector:
    app: edusoho
    tier: mysql

---

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: edusoho-mysql
  labels:
    app: edusoho
spec:
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: edusoho
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
          k8s-linux-worker2

      volumes:
        - name: mysql-config
          configMap:
            name: edusoho-mysql-config

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/mysql-log/

        - name: mysql-data
          hostPath:
            path: /opt/k8s/volume_data/mysql-data/

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f  ./edusoho-mysql.yml 
deployment.extensions/edusoho-mysql unchanged
The Service "edusoho-mysql" is invalid: spec.ports[0].nodePort: Forbidden: may not be used when `type` is 'ClusterIP'
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   35h     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         6d3h    app=confluence,tier=mysql
edusoho-mysql      NodePort    10.68.125.174   <none>        3306:23160/TCP   26m     app=edusoho,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   7h34m   app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          15d     <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl delete service edusoho-mysql
service "edusoho-mysql" deleted
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f  ./edusoho-mysql.yml 
service/edusoho-mysql created
deployment.extensions/edusoho-mysql unchanged
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   35h     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         6d3h    app=confluence,tier=mysql
edusoho-mysql      ClusterIP   10.68.42.16     <none>        3306/TCP         4s      app=edusoho,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   7h34m   app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          15d     <none>
[root@k8s-master1 temp]# 



[root@k8s-master1 temp]# kubectl run -i -t mysql-test --image=mysql/mysql-server:5.7 --restart=Never bash
If you don't see a command prompt, try pressing enter.
bash-4.2# env
EDUSOHO_MYSQL_PORT_3306_TCP_PROTO=tcp
JIRA_SERVICE_PORT=8080
HOSTNAME=mysql-test
CONFLUENCE_PORT=tcp://10.68.241.111:8090
TERM=xterm
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT=tcp://10.68.0.1:443
EDUSOHO_MYSQL_PORT_3306_TCP_PORT=3306
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_HOST=10.68.0.1
CONFLUENCE_MYSQL_PORT_3306_TCP_PORT=3306
EDUSOHO_MYSQL_SERVICE_HOST=10.68.42.16
CONFLUENCE_PORT_8090_TCP_PORT=8090
CONFLUENCE_MYSQL_PORT_3306_TCP=tcp://10.68.89.209:3306
CONFLUENCE_PORT_8090_TCP_ADDR=10.68.241.111
CONFLUENCE_MYSQL_PORT_3306_TCP_PROTO=tcp
JIRA_SERVICE_PORT_HTTP=8080
CONFLUENCE_SERVICE_PORT_HTTP=8090
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CONFLUENCE_MYSQL_SERVICE_HOST=10.68.89.209
JIRA_PORT=tcp://10.68.191.95:8080
JIRA_PORT_8080_TCP_PORT=8080
CONFLUENCE_MYSQL_SERVICE_PORT=3306
PWD=/
EDUSOHO_MYSQL_PORT_3306_TCP_ADDR=10.68.42.16
EDUSOHO_MYSQL_SERVICE_PORT=3306
CONFLUENCE_MYSQL_PORT=tcp://10.68.89.209:3306
JIRA_PORT_8080_TCP_ADDR=10.68.191.95
JIRA_PORT_8080_TCP_PROTO=tcp
EDUSOHO_MYSQL_PORT_3306_TCP=tcp://10.68.42.16:3306
EDUSOHO_MYSQL_PORT=tcp://10.68.42.16:3306
HOME=/root
SHLVL=1
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_SERVICE_PORT_HTTPS=443
CONFLUENCE_MYSQL_PORT_3306_TCP_ADDR=10.68.89.209
JIRA_SERVICE_HOST=10.68.191.95
CONFLUENCE_SERVICE_HOST=10.68.241.111
CONFLUENCE_PORT_8090_TCP=tcp://10.68.241.111:8090
KUBERNETES_PORT_443_TCP_ADDR=10.68.0.1
CONFLUENCE_PORT_8090_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP=tcp://10.68.0.1:443
CONFLUENCE_SERVICE_PORT=8090
JIRA_PORT_8080_TCP=tcp://10.68.191.95:8080
_=/usr/bin/env
bash-4.2# mysql -u root -p -h 10.68.42.16
Enter password: rootpassword
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 




[root@k8s-master1 temp]# cat jira.yml 
apiVersion: v1
kind: Service
metadata:
  name: jira
  labels:
    app: jira
spec:
  ports:
  - name: http
    port: 8080
    targetPort: 8080
    protocol: TCP
  selector:
    app: jira
    service: jira
  type: NodePort
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: jira-deployment
  labels:
    service: jira
    app: jira

spec:
  replicas: 1
  selector:
    matchLabels:
      app: jira
      service: jira
  template:
    metadata:
      labels:
        app: jira
        service: jira
    spec:
      containers:
        - name: jira
          image: cptactionhank/atlassian-jira-software:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080

          volumeMounts:
          - name: jira-home
            mountPath: /var/atlassian/jira
          - name: jira-install
            mountPath: /opt/atlassian/jira

      volumes:
        - name: jira-home
          hostPath:
            path: /opt/k8s/volume_data/jira_home/
        - name: jira-install
          hostPath:
            path: /opt/k8s/volume_data/jira_install/
[root@k8s-master1 temp]# 




```

