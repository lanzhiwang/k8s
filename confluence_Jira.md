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



### MySQL 容器相关

```bash
[root@lanzhiwang-centos7 ~]# docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
atlassian/confluence-server   latest              d843736462f7        13 days ago         862MB
redis                         latest              d3e3588af517        2 weeks ago         95MB
mysql/mysql-server            5.7                 857eadf53a54        4 weeks ago         258MB
k8s.gcr.io/kube-scheduler     v1.14.0             00638a24688b        2 months ago        81.6MB
k8s.gcr.io/kube-apiserver     v1.14.0             ecf910f40d6e        2 months ago        210MB
quay.io/coreos/flannel        v0.11.0-arm         ef3b5d63729b        4 months ago        48.9MB
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# docker run --name=mysql1 -d mysql/mysql-server:5.7
6c48f9a1f88a02505eb0b145563a83d649e7e54096f776444000a5bce1087733
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
6c48f9a1f88a        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   5 seconds ago       Up 4 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6379
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# 
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
[root@lanzhiwang-centos7 ~]# 
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
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'rootpassword';
Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye
bash-4.2# 
bash-4.2# ls /var/lib/mysql
auto.cnf  ca-key.pem  ca.pem  client-cert.pem  client-key.pem  ib_buffer_pool  ib_logfile0  ib_logfile1  ibdata1  ibtmp1  mysql  mysql.sock  mysql.sock.lock  performance_schema  private_key.pem  public_key.pem  server-cert.pem  server-key.pem  sys
bash-4.2# 
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
bash-4.2# cat /var/log/mysqld.log
2019-05-30T01:33:47.429597Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2019-05-30T01:33:48.321762Z 0 [Warning] InnoDB: New log files created, LSN=45790
2019-05-30T01:33:48.493017Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
2019-05-30T01:33:48.563670Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: f8f067fa-827a-11e9-82e5-02420a024102.
2019-05-30T01:33:48.567250Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2019-05-30T01:33:48.726427Z 0 [Warning] CA certificate ca.pem is self signed.
2019-05-30T01:33:48.806882Z 1 [Warning] root@localhost is created with an empty password ! Please consider switching off the --initialize-insecure option.
2019-05-30T01:33:52.148665Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2019-05-30T01:33:52.151833Z 0 [Note] mysqld (mysqld 5.7.26) starting as process 50 ...
2019-05-30T01:33:52.163977Z 0 [Note] InnoDB: PUNCH HOLE support available
2019-05-30T01:33:52.164005Z 0 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2019-05-30T01:33:52.164010Z 0 [Note] InnoDB: Uses event mutexes
2019-05-30T01:33:52.164014Z 0 [Note] InnoDB: GCC builtin __atomic_thread_fence() is used for memory barrier
2019-05-30T01:33:52.164018Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2019-05-30T01:33:52.164022Z 0 [Note] InnoDB: Using Linux native AIO
2019-05-30T01:33:52.164233Z 0 [Note] InnoDB: Number of pools: 1
2019-05-30T01:33:52.164310Z 0 [Note] InnoDB: Using CPU crc32 instructions
2019-05-30T01:33:52.167159Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2019-05-30T01:33:52.207375Z 0 [Note] InnoDB: Completed initialization of buffer pool
2019-05-30T01:33:52.211823Z 0 [Note] InnoDB: If the mysqld execution user is authorized, page cleaner thread priority can be changed. See the man page of setpriority().
2019-05-30T01:33:52.228074Z 0 [Note] InnoDB: Highest supported file format is Barracuda.
2019-05-30T01:33:52.241616Z 0 [Note] InnoDB: Creating shared tablespace for temporary tables
2019-05-30T01:33:52.241684Z 0 [Note] InnoDB: Setting file './ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
2019-05-30T01:33:52.338899Z 0 [Note] InnoDB: File './ibtmp1' size is now 12 MB.
2019-05-30T01:33:52.339694Z 0 [Note] InnoDB: 96 redo rollback segment(s) found. 96 redo rollback segment(s) are active.
2019-05-30T01:33:52.339704Z 0 [Note] InnoDB: 32 non-redo rollback segment(s) are active.
2019-05-30T01:33:52.341585Z 0 [Note] InnoDB: 5.7.26 started; log sequence number 2524985
2019-05-30T01:33:52.341990Z 0 [Note] InnoDB: Loading buffer pool(s) from /var/lib/mysql/ib_buffer_pool
2019-05-30T01:33:52.342286Z 0 [Note] Plugin 'FEDERATED' is disabled.
2019-05-30T01:33:52.346291Z 0 [Note] InnoDB: Buffer pool(s) load completed at 190530  1:33:52
2019-05-30T01:33:52.353411Z 0 [Note] Found ca.pem, server-cert.pem and server-key.pem in data directory. Trying to enable SSL support using them.
2019-05-30T01:33:52.353428Z 0 [Note] Skipping generation of SSL certificates as certificate files are present in data directory.
2019-05-30T01:33:52.356769Z 0 [Warning] CA certificate ca.pem is self signed.
2019-05-30T01:33:52.356808Z 0 [Note] Skipping generation of RSA key pair as key files are present in data directory.
2019-05-30T01:33:52.370659Z 0 [Note] Event Scheduler: Loaded 0 events
2019-05-30T01:33:52.372363Z 0 [Note] mysqld: ready for connections.
Version: '5.7.26'  socket: '/var/lib/mysql/mysql.sock'  port: 0  MySQL Community Server (GPL)
2019-05-30T01:33:54.878235Z 0 [Note] Giving 0 client threads a chance to die gracefully
2019-05-30T01:33:54.878253Z 0 [Note] Shutting down slave threads
2019-05-30T01:33:54.878259Z 0 [Note] Forcefully disconnecting 0 remaining clients
2019-05-30T01:33:54.878268Z 0 [Note] Event Scheduler: Purging the queue. 0 events
2019-05-30T01:33:54.878298Z 0 [Note] Binlog end
2019-05-30T01:33:54.878634Z 0 [Note] Shutting down plugin 'ngram'
2019-05-30T01:33:54.878640Z 0 [Note] Shutting down plugin 'partition'
2019-05-30T01:33:54.878643Z 0 [Note] Shutting down plugin 'ARCHIVE'
2019-05-30T01:33:54.878646Z 0 [Note] Shutting down plugin 'BLACKHOLE'
2019-05-30T01:33:54.878649Z 0 [Note] Shutting down plugin 'MRG_MYISAM'
2019-05-30T01:33:54.878653Z 0 [Note] Shutting down plugin 'CSV'
2019-05-30T01:33:54.878656Z 0 [Note] Shutting down plugin 'PERFORMANCE_SCHEMA'
2019-05-30T01:33:54.878681Z 0 [Note] Shutting down plugin 'MEMORY'
2019-05-30T01:33:54.878684Z 0 [Note] Shutting down plugin 'INNODB_SYS_VIRTUAL'
2019-05-30T01:33:54.878687Z 0 [Note] Shutting down plugin 'INNODB_SYS_DATAFILES'
2019-05-30T01:33:54.878690Z 0 [Note] Shutting down plugin 'INNODB_SYS_TABLESPACES'
2019-05-30T01:33:54.878693Z 0 [Note] Shutting down plugin 'INNODB_SYS_FOREIGN_COLS'
2019-05-30T01:33:54.878695Z 0 [Note] Shutting down plugin 'INNODB_SYS_FOREIGN'
2019-05-30T01:33:54.878698Z 0 [Note] Shutting down plugin 'INNODB_SYS_FIELDS'
2019-05-30T01:33:54.878701Z 0 [Note] Shutting down plugin 'INNODB_SYS_COLUMNS'
2019-05-30T01:33:54.878715Z 0 [Note] Shutting down plugin 'INNODB_SYS_INDEXES'
2019-05-30T01:33:54.878721Z 0 [Note] Shutting down plugin 'INNODB_SYS_TABLESTATS'
2019-05-30T01:33:54.878723Z 0 [Note] Shutting down plugin 'INNODB_SYS_TABLES'
2019-05-30T01:33:54.878726Z 0 [Note] Shutting down plugin 'INNODB_FT_INDEX_TABLE'
2019-05-30T01:33:54.878729Z 0 [Note] Shutting down plugin 'INNODB_FT_INDEX_CACHE'
2019-05-30T01:33:54.878731Z 0 [Note] Shutting down plugin 'INNODB_FT_CONFIG'
2019-05-30T01:33:54.878734Z 0 [Note] Shutting down plugin 'INNODB_FT_BEING_DELETED'
2019-05-30T01:33:54.878737Z 0 [Note] Shutting down plugin 'INNODB_FT_DELETED'
2019-05-30T01:33:54.878739Z 0 [Note] Shutting down plugin 'INNODB_FT_DEFAULT_STOPWORD'
2019-05-30T01:33:54.878768Z 0 [Note] Shutting down plugin 'INNODB_METRICS'
2019-05-30T01:33:54.878772Z 0 [Note] Shutting down plugin 'INNODB_TEMP_TABLE_INFO'
2019-05-30T01:33:54.878774Z 0 [Note] Shutting down plugin 'INNODB_BUFFER_POOL_STATS'
2019-05-30T01:33:54.878777Z 0 [Note] Shutting down plugin 'INNODB_BUFFER_PAGE_LRU'
2019-05-30T01:33:54.878780Z 0 [Note] Shutting down plugin 'INNODB_BUFFER_PAGE'
2019-05-30T01:33:54.878782Z 0 [Note] Shutting down plugin 'INNODB_CMP_PER_INDEX_RESET'
2019-05-30T01:33:54.878785Z 0 [Note] Shutting down plugin 'INNODB_CMP_PER_INDEX'
2019-05-30T01:33:54.878787Z 0 [Note] Shutting down plugin 'INNODB_CMPMEM_RESET'
2019-05-30T01:33:54.878790Z 0 [Note] Shutting down plugin 'INNODB_CMPMEM'
2019-05-30T01:33:54.878793Z 0 [Note] Shutting down plugin 'INNODB_CMP_RESET'
2019-05-30T01:33:54.878795Z 0 [Note] Shutting down plugin 'INNODB_CMP'
2019-05-30T01:33:54.878798Z 0 [Note] Shutting down plugin 'INNODB_LOCK_WAITS'
2019-05-30T01:33:54.878801Z 0 [Note] Shutting down plugin 'INNODB_LOCKS'
2019-05-30T01:33:54.878803Z 0 [Note] Shutting down plugin 'INNODB_TRX'
2019-05-30T01:33:54.878806Z 0 [Note] Shutting down plugin 'InnoDB'
2019-05-30T01:33:54.878843Z 0 [Note] InnoDB: FTS optimize thread exiting.
2019-05-30T01:33:54.879017Z 0 [Note] InnoDB: Starting shutdown...
2019-05-30T01:33:54.983927Z 0 [Note] InnoDB: Dumping buffer pool(s) to /var/lib/mysql/ib_buffer_pool
2019-05-30T01:33:54.989643Z 0 [Note] InnoDB: Buffer pool(s) dump completed at 190530  1:33:54
2019-05-30T01:33:56.440184Z 0 [Note] InnoDB: Shutdown completed; log sequence number 11899954
2019-05-30T01:33:56.441580Z 0 [Note] InnoDB: Removed temporary tablespace data file: "ibtmp1"
2019-05-30T01:33:56.441591Z 0 [Note] Shutting down plugin 'MyISAM'
2019-05-30T01:33:56.441601Z 0 [Note] Shutting down plugin 'sha256_password'
2019-05-30T01:33:56.441604Z 0 [Note] Shutting down plugin 'mysql_native_password'
2019-05-30T01:33:56.441702Z 0 [Note] Shutting down plugin 'binlog'
2019-05-30T01:33:56.442279Z 0 [Note] mysqld: Shutdown complete

2019-05-30T01:33:57.069890Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2019-05-30T01:33:57.070662Z 0 [Note] mysqld (mysqld 5.7.26) starting as process 1 ...
2019-05-30T01:33:57.080483Z 0 [Note] InnoDB: PUNCH HOLE support available
2019-05-30T01:33:57.080504Z 0 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2019-05-30T01:33:57.080509Z 0 [Note] InnoDB: Uses event mutexes
2019-05-30T01:33:57.080513Z 0 [Note] InnoDB: GCC builtin __atomic_thread_fence() is used for memory barrier
2019-05-30T01:33:57.080518Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
2019-05-30T01:33:57.080522Z 0 [Note] InnoDB: Using Linux native AIO
2019-05-30T01:33:57.080818Z 0 [Note] InnoDB: Number of pools: 1
2019-05-30T01:33:57.080904Z 0 [Note] InnoDB: Using CPU crc32 instructions
2019-05-30T01:33:57.081967Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2019-05-30T01:33:57.092446Z 0 [Note] InnoDB: Completed initialization of buffer pool
2019-05-30T01:33:57.094010Z 0 [Note] InnoDB: If the mysqld execution user is authorized, page cleaner thread priority can be changed. See the man page of setpriority().
2019-05-30T01:33:57.110274Z 0 [Note] InnoDB: Highest supported file format is Barracuda.
2019-05-30T01:33:57.117560Z 0 [Note] InnoDB: Creating shared tablespace for temporary tables
2019-05-30T01:33:57.117614Z 0 [Note] InnoDB: Setting file './ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
2019-05-30T01:33:57.189932Z 0 [Note] InnoDB: File './ibtmp1' size is now 12 MB.
2019-05-30T01:33:57.190583Z 0 [Note] InnoDB: 96 redo rollback segment(s) found. 96 redo rollback segment(s) are active.
2019-05-30T01:33:57.190592Z 0 [Note] InnoDB: 32 non-redo rollback segment(s) are active.
2019-05-30T01:33:57.191375Z 0 [Note] InnoDB: 5.7.26 started; log sequence number 11899954
2019-05-30T01:33:57.191659Z 0 [Note] InnoDB: Loading buffer pool(s) from /var/lib/mysql/ib_buffer_pool
2019-05-30T01:33:57.191712Z 0 [Note] Plugin 'FEDERATED' is disabled.
2019-05-30T01:33:57.193518Z 0 [Note] InnoDB: Buffer pool(s) load completed at 190530  1:33:57
2019-05-30T01:33:57.196624Z 0 [Note] Found ca.pem, server-cert.pem and server-key.pem in data directory. Trying to enable SSL support using them.
2019-05-30T01:33:57.196636Z 0 [Note] Skipping generation of SSL certificates as certificate files are present in data directory.
2019-05-30T01:33:57.197251Z 0 [Warning] CA certificate ca.pem is self signed.
2019-05-30T01:33:57.197284Z 0 [Note] Skipping generation of RSA key pair as key files are present in data directory.
2019-05-30T01:33:57.197500Z 0 [Note] Server hostname (bind-address): '*'; port: 3306
2019-05-30T01:33:57.197524Z 0 [Note] IPv6 is available.
2019-05-30T01:33:57.197532Z 0 [Note]   - '::' resolves to '::';
2019-05-30T01:33:57.197547Z 0 [Note] Server socket created on IP: '::'.
2019-05-30T01:33:57.207854Z 0 [Note] Event Scheduler: Loaded 0 events
2019-05-30T01:33:57.208016Z 0 [Note] Execution of init_file '/var/lib/mysql-files/VzmRY242yA' started.
2019-05-30T01:33:57.208584Z 0 [Note] Execution of init_file '/var/lib/mysql-files/VzmRY242yA' ended.
2019-05-30T01:33:57.208693Z 0 [Note] mysqld: ready for connections.
Version: '5.7.26'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  MySQL Community Server (GPL)
2019-05-30T01:35:15.944303Z 5 [Note] Access denied for user 'root'@'localhost' (using password: NO)
bash-4.2# 
bash-4.2# exit
exit
[root@lanzhiwang-centos7 ~]# 





[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 \
> --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf \
> --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql \
> -d mysql/mysql-server:5.7
81a31f5a37cc16a644e6d262ad0666fb84b9ac1041aabf6005821c8f825b80d3
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
81a31f5a37cc        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   10 seconds ago      Up 9 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6379
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# ll
total 4
drwxr-xr-x 5 mysql mysql  314 May 30 09:49 data
drwxr-xr-x 2 root  root     6 May 30 09:47 log
-rw-r--r-- 1 root  root  1208 May 30 09:46 my.cnf
[root@lanzhiwang-centos7 mysql]# 
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
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
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
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                     PORTS               NAMES
81a31f5a37cc        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   3 minutes ago       Exited (1) 2 minutes ago                       mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                       redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                       redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6379
[root@lanzhiwang-centos7 mysql]# 




[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql -d mysql/mysql-server:5.7
1590065c7d7e6005a7b9b7fa69e3ec5dd3466ac3158141f6a97b41b3d0c12e4f
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
1590065c7d7e        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   8 seconds ago       Up 7 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6379
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
1590065c7d7e        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   10 seconds ago      Up 9 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6379
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





[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log,dst=/var/log -d mysql/mysql-server:5.7
a1228535445be289852e9e569a61d44b38888d80e3ad6c8dcc906e2869940c60
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                     PORTS               NAMES
a1228535445b        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   7 seconds ago       Exited (1) 6 seconds ago                       mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                       redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                       redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                         redis-6379
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
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# ll
total 4
drwxr-xr-x 2 mysql mysql    6 May 30 10:04 data
drwxr-xr-x 2 root  root     6 May 30 09:47 log
-rw-r--r-- 1 root  root  1221 May 30 09:57 my.cnf
[root@lanzhiwang-centos7 mysql]# ll data/
total 0
[root@lanzhiwang-centos7 mysql]# ll log/
total 0
[root@lanzhiwang-centos7 mysql]# mkdir -R mysql:mysql log
mkdir: invalid option -- 'R'
Try 'mkdir --help' for more information.
[root@lanzhiwang-centos7 mysql]# chown -R mysql:mysql log
[root@lanzhiwang-centos7 mysql]# ll
total 4
drwxr-xr-x 2 mysql mysql    6 May 30 10:04 data
drwxr-xr-x 2 mysql mysql    6 May 30 09:47 log
-rw-r--r-- 1 root  root  1221 May 30 09:57 my.cnf
[root@lanzhiwang-centos7 mysql]# 


[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log,dst=/var/log -d mysql/mysql-server:5.7
3c2ab5b463075053fd5e1318e01db9c37e5d70c95ff3e30fac52f863fa5164f4
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
3c2ab5b46307        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   5 seconds ago       Up 4 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6379
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





[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log/mysqld.log,dst=/var/log/mysqld.log -d mysql/mysql-server:5.7
cde247b1a08cd3202f2db8f5523fa82e38b1862e3526dcd5dccb511a87dd10ef
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
cde247b1a08c        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   5 seconds ago       Up 5 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6379
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

[root@lanzhiwang-centos7 mysql]# mysql -u root -p -h 10.2.65.2
Enter password: 
ERROR 1130 (HY000): Host '10.2.65.1' is not allowed to connect to this MySQL server
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# mysql -u root -p -h 10.2.65.1
Enter password: 
ERROR 2003 (HY000): Can't connect to MySQL server on '10.2.65.1' (111)
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# mysql -u root -p -h 10.2.65.1
Enter password: 
ERROR 2003 (HY000): Can't connect to MySQL server on '10.2.65.1' (111)
[root@lanzhiwang-centos7 mysql]# 


[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 -e MYSQL_ROOT_PASSWORD=rootpass --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log/mysqld.log,dst=/var/log/mysqld.log -d mysql/mysql-server:5.7
1251a121e7310c48acc17ebf6bc0355ea363a0d7bbfa67bfdf70bb1854d2e44d
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                 NAMES
1251a121e731        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   4 seconds ago       Up 2 seconds (health: starting)   3306/tcp, 33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                  redis-6379
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker logs 1251a121e731
[Entrypoint] MySQL Docker Image 5.7.26-1.1.11
[Entrypoint] Starting MySQL 5.7.26-1.1.11
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker exec -ti 1251a121e731 bash
bash-4.2# mysql -u root -p 
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> exit
Bye
bash-4.2# 





[root@lanzhiwang-centos7 mysql]# docker run --name=mysql1 -e MYSQL_ROOT_PASSWORD=rootpass --mount type=bind,src=/root/work/mysql/my.cnf,dst=/etc/my.cnf --mount type=bind,src=/root/work/mysql/data,dst=/var/lib/mysql --mount type=bind,src=/root/work/mysql/log/mysqld.log,dst=/var/log/mysqld.log -p 3306:3306 -p 33060:33060 -d mysql/mysql-server:5.7
a3deb6919015b705797e9448a6a594e1f30b97c138d68c6e362c3dec5dc8f07a
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# docker ps -a
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS                            PORTS                                              NAMES
a3deb6919015        mysql/mysql-server:5.7   "/entrypoint.sh mysq…"   3 seconds ago       Up 2 seconds (health: starting)   0.0.0.0:3306->3306/tcp, 0.0.0.0:33060->33060/tcp   mysql1
0ca22722e545        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                                               sentinel_26381
6c26d0758742        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                                               sentinel_26380
603c9b84d7e7        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                                               sentinel_26379
8b6e35ee6daf        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                                               redis-6384
f1af3a9f9fa2        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                                               redis-6383
159e22139cc5        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                                               redis-6382
ec0d0f0a0961        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                                             redis-6381
95a15915ca56        redis                    "docker-entrypoint.s…"   12 days ago         Exited (137) 12 days ago                                                             redis-6380
438c5b405b8e        redis                    "docker-entrypoint.s…"   12 days ago         Exited (0) 12 days ago                                                               redis-6379
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

mysql -u root -p -h 10.2.65.2
mysql -u root -p -h 10.2.65.1
mysql -u root -p -h 10.0.2.15
mysql -u root -p -h 10.5.106.26
mysql -u root -p -h 127.0.0.1


[root@lanzhiwang-centos7 mysql]# mysql -u root -p -h 10.2.65.2
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 54
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> exit
Bye
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 

[root@lanzhiwang-centos7 mysql]# mysql -u root -p -h 10.2.65.1
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 58
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> exit
Bye
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# 
[root@lanzhiwang-centos7 mysql]# mysql -u root -p -h 10.0.2.15
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 60
Server version: 5.7.26 MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 



```


### confluence 容器相关

```bash

[root@lanzhiwang-centos7 ~]# docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
atlassian/confluence-server   latest              d843736462f7        13 days ago         862MB
redis                         latest              d3e3588af517        2 weeks ago         95MB
nginx                         latest              53f3fd8007f7        3 weeks ago         109MB
nicolaka/netshoot             latest              b2b51767b54a        3 weeks ago         203MB
mysql/mysql-server            5.7                 857eadf53a54        4 weeks ago         258MB
k8s.gcr.io/kube-scheduler     v1.14.0             00638a24688b        2 months ago        81.6MB
k8s.gcr.io/kube-apiserver     v1.14.0             ecf910f40d6e        2 months ago        210MB
quay.io/coreos/flannel        v0.11.0-arm         ef3b5d63729b        4 months ago        48.9MB
[root@lanzhiwang-centos7 ~]# 


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


[root@lanzhiwang-centos7 docker_data]# docker run -v /root/work/confluence/docker_data/confluence_home:/var/atlassian/application-data/confluence -v /root/work/confluence/docker_data/confluence_install:/opt/atlassian/confluence --name="confluence" -d -p 8090:8090 -p 8091:8091 atlassian/confluence-server
4a50262c5a8b13e64444c063009c554be74f11f0f1c6fc58c9345f59ac968972
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# docker ps -a
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                              NAMES
4a50262c5a8b        atlassian/confluence-server   "/tini -- /entrypoin…"   6 seconds ago       Up 4 seconds        0.0.0.0:8090-8091->8090-8091/tcp   confluence
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll
total 0
drwx------  3 bin    bin     18 May 30 12:01 confluence_home
drwxr-xr-x 12 daemon daemon 314 May  8 11:10 confluence_install
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_home/
total 0
drwxr-x--- 2 bin bin 102 May 30 12:01 logs
[root@lanzhiwang-centos7 docker_data]# 
[root@lanzhiwang-centos7 docker_data]# ll confluence_install/
total 204
drwxr-xr-x  3 daemon daemon  4096 May 30 12:00 bin
-rw-r--r--  1 daemon daemon 19743 Apr 12 23:24 BUILDING.txt
drwxr-xr-x  3 daemon daemon   256 May 30 12:00 conf
drwxr-xr-x 27 daemon daemon  4096 May 30 12:00 confluence
-rw-r--r--  1 daemon daemon  5543 Apr 12 23:24 CONTRIBUTING.md
drwxr-xr-x  2 daemon daemon  4096 May 30 12:00 lib
-rw-r--r--  1 daemon daemon 58153 Apr 12 23:24 LICENSE
drwxr-xr-x  2 daemon daemon 45056 May 30 12:00 licenses
drwxr-xr-x  2 daemon daemon     6 Apr 12 23:22 logs
-rw-r--r--  1 daemon daemon  2401 Apr 12 23:24 NOTICE
-rw-r--r--  1 daemon daemon  2294 May  8 11:09 README.html
-rw-r--r--  1 daemon daemon  3334 Apr 12 23:24 README.md
-rw-r--r--  1 daemon daemon  1204 May  8 11:09 README.txt
-rw-r--r--  1 daemon daemon  7025 Apr 12 23:24 RELEASE-NOTES
-rw-r--r--  1 daemon daemon 16738 Apr 12 23:24 RUNNING.txt
drwxr-xr-x  4 daemon daemon    37 May 30 12:00 synchrony-proxy
drwxr-xr-x  2 daemon daemon    30 May 30 12:00 temp
drwxr-xr-x  2 daemon daemon     6 May  8 11:10 webapps
drwxr-xr-x  2 daemon daemon     6 Apr 12 23:22 work
[root@lanzhiwang-centos7 docker_data]# 





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
          subPath: busybox.conf
      volumes:
      - name: conf
        hostPath:
          path: /opt/k8s/volume_data/busybox/



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
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
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

            - name: mysql-log  # mysqld.log 文件不要提交创建
              subPath: mysqld.log
              mountPath: /var/log/mysqld.log

            - name: mysql-data
              mountPath: /var/lib/mysql

      volumes:
        - name: mysql-config
          hostPath:
            path: /opt/k8s/volume_data/mysql-config/

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/mysql-log/

        - name: mysql-data
          hostPath:
            path: /opt/k8s/volume_data/mysql-data

[root@k8s-master1 temp]# 




[root@k8s-master1 temp]# rm -rf mysql-deployment.yml 
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
  clusterIP: None
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

            - name: mysql-log
              subPath: mysqld.log
              mountPath: /var/log/mysqld.log

            - name: mysql-data
              mountPath: /var/lib/mysql

      volumes:
        - name: mysql-config
          hostPath:
            path: /opt/k8s/volume_data/mysql-config/

        - name: mysql-log
          hostPath:
            path: /opt/k8s/volume_data/mysql-log/

        - name: mysql-data
          hostPath:
            path: /opt/k8s/volume_data/mysql-data

[root@k8s-master1 temp]# 



[root@k8s-master1 temp]# kubectl run -i -t mysql-test --image=mysql/mysql-server:5.7 --restart=Never bash
If you don't see a command prompt, try pressing enter.
bash-4.2# env
HOSTNAME=mysql-test
TERM=xterm
KUBERNETES_PORT=tcp://10.68.0.1:443
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_HOST=10.68.0.1
CONFLUENCE_MYSQL_PORT_3306_TCP_PORT=3306
CONFLUENCE_MYSQL_PORT_3306_TCP=tcp://10.68.8.175:3306
CONFLUENCE_MYSQL_PORT_3306_TCP_PROTO=tcp
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CONFLUENCE_MYSQL_SERVICE_HOST=10.68.8.175
CONFLUENCE_MYSQL_SERVICE_PORT=3306
PWD=/
CONFLUENCE_MYSQL_PORT=tcp://10.68.8.175:3306
HOME=/root
SHLVL=1
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_SERVICE_PORT_HTTPS=443
CONFLUENCE_MYSQL_PORT_3306_TCP_ADDR=10.68.8.175
KUBERNETES_PORT_443_TCP_ADDR=10.68.0.1
KUBERNETES_PORT_443_TCP=tcp://10.68.0.1:443
_=/usr/bin/env
bash-4.2# 
bash-4.2# mysql -u root -p -h 10.68.8.175 -P 3306
Enter password: 
ERROR 1045 (28000): Access denied for user 'root'@'172.20.3.7' (using password: YES)
bash-4.2# mysql -u root -p -h 172.20.0.15 -P 3306


[root@k8s-master1 ~]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE   SELECTOR
confluence-mysql   ClusterIP   10.68.89.209   <none>        3306/TCP   51s   app=confluence,tier=mysql
kubernetes         ClusterIP   10.68.0.1      <none>        443/TCP    9d    <none>
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl describe service confluence-mysql
Name:              confluence-mysql
Namespace:         default
Labels:            app=confluence
Annotations:       kubectl.kubernetes.io/last-applied-configuration:
                     {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"app":"confluence"},"name":"confluence-mysql","namespace":"defa...
Selector:          app=confluence,tier=mysql
Type:              ClusterIP
IP:                10.68.89.209
Port:              <unset>  3306/TCP
TargetPort:        3306/TCP
Endpoints:         172.20.0.15:3306
Session Affinity:  None
Events:            <none>
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl get pod -o wide
NAME                               READY   STATUS    RESTARTS   AGE    IP            NODE         NOMINATED NODE   READINESS GATES
confluence-mysql-d464855bd-9ckm9   1/1     Running   7          133m   172.20.0.15   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-29wdg          1/1     Running   0          31h    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv          1/1     Running   0          31h    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l          1/1     Running   0          31h    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq          1/1     Running   0          31h    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww          1/1     Running   0          31h    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj          1/1     Running   0          31h    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p          1/1     Running   0          31h    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq          1/1     Running   0          31h    172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                         1/1     Running   0          19s    172.20.0.16   10.1.36.46   <none>           <none>
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 


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


```




