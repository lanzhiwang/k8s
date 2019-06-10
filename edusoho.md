```bash

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

[root@k8s-master1 temp]# vim ./edusoho.yml 
[root@k8s-master1 temp]# cat ./edusoho.yml 
apiVersion: v1
kind: Service
metadata:
  name: edusoho
  labels:
    app: edusoho
spec:
  ports:
  - name: http
    port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: edusoho
    service: edusoho
  type: NodePort
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: edusoho-deployment
  labels:
    service: edusoho
    app: edusoho

spec:
  replicas: 1
  selector:
    matchLabels:
      app: edusoho
      service: edusoho
  template:
    metadata:
      labels:
        app: edusoho
        service: edusoho
    spec:
      containers:
        - name: edusoho
          image: edusoho/edusoho
          imagePullPolicy: Always
          ports:
            - containerPort: 80
          env:
            - name: DOMAIN
              value: course.mingyuanyun.com
            - name: MYSQL_USER
              value: root
            - name: MYSQL_PASSWORD
              value: rootpassword

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f ./edusoho.yml 
service/edusoho created
deployment.apps/edusoho-deployment created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                                         SELECTOR
confluence-deployment   1/1     1            1           35h     confluence   atlassian/confluence-server:latest             app=confluence,service=confluence
confluence-mysql        0/1     1            0           7h11m   mysql        mysql/mysql-server:5.7                         app=confluence,tier=mysql
edusoho-deployment      1/1     1            1           22s     edusoho      edusoho/edusoho                                app=edusoho,service=edusoho
edusoho-mysql           1/1     1            1           26m     mysql        mysql/mysql-server:5.7                         app=edusoho,tier=mysql
jira-deployment         1/1     1            1           7h47m   jira         cptactionhank/atlassian-jira-software:latest   app=jira,service=jira
my-nginx                8/8     8            8           7d10h   my-nginx     nginx                                          run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                     READY   STATUS             RESTARTS   AGE     IP            NODE         NOMINATED NODE   READINESS GATES
confluence-deployment-7577774698-psgz2   1/1     Running            0          35h     172.20.0.17   10.1.36.46   <none>           <none>
confluence-mysql-d464855bd-cp7sz         0/1     CrashLoopBackOff   86         7h11m   172.20.3.10   10.1.36.49   <none>           <none>
edusoho-deployment-57cb7946df-9nn6l      1/1     Running            0          38s     172.20.2.17   10.1.36.48   <none>           <none>
edusoho-mysql-fc4f549f5-hv9sw            1/1     Running            0          27m     172.20.1.26   10.1.36.47   <none>           <none>
jira-deployment-ccc84bffd-r9mzz          1/1     Running            0          7h47m   172.20.2.16   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg                1/1     Running            0          7d10h   172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv                1/1     Running            0          7d10h   172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l                1/1     Running            0          7d10h   172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq                1/1     Running            0          7d10h   172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww                1/1     Running            0          7d10h   172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj                1/1     Running            0          7d10h   172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p                1/1     Running            0          7d10h   172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq                1/1     Running            0          7d10h   172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                               0/1     Completed          0          12m     172.20.1.27   10.1.36.47   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   35h     app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         6d3h    app=confluence,tier=mysql
edusoho            NodePort    10.68.215.211   <none>        80:27118/TCP     81s     app=edusoho,service=edusoho
edusoho-mysql      ClusterIP   10.68.42.16     <none>        3306/TCP         14m     app=edusoho,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   7h49m   app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          15d     <none>
[root@k8s-master1 temp]# 


http://www.mayanpeng.cn/archives/78.html


######################################################################
apiVersion: v1
kind: Service
metadata:
  name: edusoho
  labels:
    app: edusoho
spec:
  ports:
  - name: http
    port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: edusoho
    service: edusoho
  type: NodePort
  externalTrafficPolicy: Local
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: edusoho-deployment
  labels:
    service: edusoho
    app: edusoho

spec:
  replicas: 1
  selector:
    matchLabels:
      app: edusoho
      service: edusoho
  template:
    metadata:
      labels:
        app: edusoho
        service: edusoho
    spec:
      containers:
        - name: edusoho
          image: edusoho/edusoho
          imagePullPolicy: Always
          ports:
            - containerPort: 80
          env:
            - name: DOMAIN
              value: course.mingyuanyun.com
            - name: MYSQL_USER
              value: root
            - name: MYSQL_PASSWORD
              value: rootpassword
 
 ###################################################################
 
 [root@k8s-master1 temp]# vim edusoho.yml 
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# cat edusoho.yml 
apiVersion: v1
kind: Service
metadata:
  name: edusoho
  labels:
    app: edusoho
spec:
  ports:
  - name: http
    port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: edusoho
    service: edusoho
  type: NodePort
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: edusoho-deployment
  labels:
    service: edusoho
    app: edusoho

spec:
  replicas: 1
  selector:
    matchLabels:
      app: edusoho
      service: edusoho
  template:
    metadata:
      labels:
        app: edusoho
        service: edusoho
    spec:
      containers:
        - name: edusoho
          image: edusoho/edusoho
          imagePullPolicy: Always
          ports:
            - containerPort: 80
          env:
            - name: DOMAIN
              value: course.mingyuanyun.com
            - name: MYSQL_USER
              value: root
            - name: MYSQL_PASSWORD
              value: rootpassword
          volumeMounts:
            - name: edusoho-data
              mountPath: /var/www

      nodeSelector:
        nodename:
          k8s-linux-worker4

      volumes:
        - name: edusoho-data
          hostPath:
            path: /opt/k8s/volume_data/edusoho-data/

[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl apply -f  ./edusoho.yml 
service/edusoho created
deployment.apps/edusoho-deployment created
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get deployment -o wide
NAME                 READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                                         SELECTOR
confluence-mysql     1/1     1            1           19h   mysql        mysql/mysql-server:5.7                         app=confluence,tier=mysql
edusoho-deployment   1/1     1            1           7s    edusoho      edusoho/edusoho                                app=edusoho,service=edusoho
edusoho-mysql        1/1     1            1           20h   mysql        mysql/mysql-server:5.7                         app=edusoho,tier=mysql
jira-deployment      1/1     1            1           27h   jira         cptactionhank/atlassian-jira-software:latest   app=jira,service=jira
my-nginx             8/8     8            8           8d    my-nginx     nginx                                          run=my-nginx
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get pod -o wide
NAME                                  READY   STATUS      RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
confluence-mysql-859d7f788b-24l27     1/1     Running     0          19h   172.20.0.19   10.1.36.46   <none>           <none>
edusoho-deployment-64bc89766b-78hxk   1/1     Running     0          17s   172.20.3.11   10.1.36.49   <none>           <none>
edusoho-mysql-fc4f549f5-hv9sw         1/1     Running     0          20h   172.20.1.26   10.1.36.47   <none>           <none>
jira-deployment-ccc84bffd-r9mzz       1/1     Running     0          27h   172.20.2.16   10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-29wdg             1/1     Running     0          8d    172.20.2.7    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-6fgzv             1/1     Running     0          8d    172.20.1.21   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-csg5l             1/1     Running     0          8d    172.20.1.20   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-lvthq             1/1     Running     0          8d    172.20.3.2    10.1.36.49   <none>           <none>
my-nginx-86459cfc9f-qhjww             1/1     Running     0          8d    172.20.0.11   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-qwclj             1/1     Running     0          8d    172.20.0.12   10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-stx7p             1/1     Running     0          8d    172.20.2.6    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-wx2hq             1/1     Running     0          8d    172.20.3.3    10.1.36.49   <none>           <none>
mysql-test                            0/1     Completed   0          19h   172.20.1.28   10.1.36.47   <none>           <none>
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl get service -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE     SELECTOR
confluence         NodePort    10.68.241.111   <none>        8090:24248/TCP   2d7h    app=confluence,service=confluence
confluence-mysql   ClusterIP   10.68.89.209    <none>        3306/TCP         6d23h   app=confluence,tier=mysql
edusoho            NodePort    10.68.148.20    <none>        80:29812/TCP     29s     app=edusoho,service=edusoho
edusoho-mysql      ClusterIP   10.68.42.16     <none>        3306/TCP         20h     app=edusoho,tier=mysql
jira               NodePort    10.68.191.95    <none>        8080:26286/TCP   27h     app=jira,service=jira
kubernetes         ClusterIP   10.68.0.1       <none>        443/TCP          16d     <none>
[root@k8s-master1 temp]# 









```