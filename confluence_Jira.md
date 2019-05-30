## Confluence、Jira、MySQL

### atlassian/confluence-server

#### Dockerfile

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

目录

/var/atlassian/application-data/confluence

/opt/atlassian/confluence

挂载点 参考 https://www.cnblogs.com/51kata/p/5266626.html

tini 的作用 https://github.com/krallin/tini



环境变量

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









### Jira

JIRA Core、JIRA Software、JIRA Service Desk 的区别
参考 https://blog.csdn.net/cabinhe/article/details/78165832


### MySQL

Deploying MySQL on Linux with Docker
参考 https://dev.mysql.com/doc/refman/5.7/en/linux-installation-docker.html

dockerfile
https://github.com/mysql/mysql-docker


https://github.com/IBM/Scalable-WordPress-deployment-on-Kubernetes


环境变量
MYSQL_ROOT_PASSWORD

持久化
--mount type=bind,src=/path-on-host-machine/my.cnf,dst=/etc/my.cnf \
--mount type=bind,src=/path-on-host-machine/datadir,dst=/var/lib/mysql \

log_error 在 配置文件中配置，相关目录持久化


```bash

[root@k8s-master1 temp]# vim volume.yml
[root@k8s-master1 temp]# 
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
[root@k8s-master1 temp]# kubectl get pv -o wide
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                        STORAGECLASS   REASON   AGE
local-volume-1   5Mi        RWO            Recycle          Bound    default/mysql-config-claim                           56s
local-volume-2   5Gi        RWO            Recycle          Bound    default/mysql-log-claim                              56s
local-volume-3   20Gi       RWO            Recycle          Bound    default/mysql-data-claim                             56s
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pvc -o wide
NAME                 STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mysql-config-claim   Bound    local-volume-1   5Mi        RWO                           60s
mysql-data-claim     Bound    local-volume-3   20Gi       RWO                           60s
mysql-log-claim      Bound    local-volume-2   5Gi        RWO                           60s
[root@k8s-master1 temp]# 

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


docker pull mysql/mysql-server:5.7


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
              mountPath: /etc/
              subPath: my.cnf
            - name: mysql-log
              mountPath: /var/log/
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
[root@k8s-master1 temp]# 
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

10.1.36.48

[root@k8s-linux-worker3 volume_data]# mkdir lv-1
[root@k8s-linux-worker3 volume_data]# mkdir lv-2
[root@k8s-linux-worker3 volume_data]# mkdir lv-3


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
[root@k8s-master1 temp]# 
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
              mountPath: /var/log/mysqld.log
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



清理节点环境

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


清理节点环境

[root@k8s-linux-worker4 volume_data]# rm -rf lv-1/*
[root@k8s-linux-worker4 volume_data]# rm -rf lv-2/*
[root@k8s-linux-worker4 volume_data]# rm -rf lv-3/*
[root@k8s-linux-worker4 volume_data]# 

[root@k8s-linux-worker3 volume_data]# rm -rf lv-1/*
[root@k8s-linux-worker3 volume_data]# rm -rf lv-2/*
[root@k8s-linux-worker3 volume_data]# rm -rf lv-3/*
[root@k8s-linux-worker3 volume_data]# 


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
              mountPath: /etc
            - name: mysql-log
              mountPath: /var/log
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
[root@k8s-master1 temp]# 




























```





