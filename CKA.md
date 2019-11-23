```
https://mymonocloud.com/login
city_lin@126.com
lin.liu@daocloud.io

https://portal.linuxfoundation.org/portal
zhihu
huzhi%^&@##huzhi

```


### 24 题，160分钟。

### 1. (5%) 日志

监控 Pod *bar* 的日志，并：

- 提取与错误 file-not-found 相对应的日志行
- 将这些日志行写入 /opt/dir/bar

```bash
kubectl logs bar | grep 'file-not-found' > /opt/dir/bar
kubectl logs bar | grep file-not-found > /opt/dir/bar
```

### 2. (3%) PV按大小排序

按 capacity 排序列出所有 persistent volumes, 将完整的 kubectl 输出保存到 /opt/dir/volume_list。

使用 kubectl 的自带功能对输出排序，不要做其他任何处理。

```bash
kubectl get pv --sort-by='{.spec.capacity.storage}' > /opt/dir/volume_list
kubectl get pv -o json
        {
            "apiVersion": "v1",
            "kind": "PersistentVolume",
            "metadata": {
                "annotations": {
                    "pv.kubernetes.io/provisioned-by": "ceph.rook.io/block"
                },
                "creationTimestamp": "2019-10-27T12:26:33Z",
                "finalizers": [
                    "kubernetes.io/pv-protection"
                ],
                "name": "pvc-fcc16c09-f8b4-11e9-bbff-0242ac120002",
                "namespace": "",
                "resourceVersion": "4531144",
                "selfLink": "/api/v1/persistentvolumes/pvc-fcc16c09-f8b4-11e9-bbff-0242ac120002",
                "uid": "02cd8cc7-f8b5-11e9-bbff-0242ac120002"
            },
            "spec": {
                "accessModes": [
                    "ReadWriteMany"
                ],
                "capacity": {
                    "storage": "2Gi"
                },
                "claimRef": {
                    "apiVersion": "v1",
                    "kind": "PersistentVolumeClaim",
                    "name": "nfs-ceph-claim",
                    "namespace": "rook-nfs",
                    "resourceVersion": "4531133",
                    "uid": "fcc16c09-f8b4-11e9-bbff-0242ac120002"
                },
                "flexVolume": {
                    "driver": "ceph.rook.io/rook-ceph",
                    "fsType": "ext4",
                    "options": {
                        "clusterNamespace": "rook-ceph",
                        "dataBlockPool": "",
                        "image": "pvc-fcc16c09-f8b4-11e9-bbff-0242ac120002",
                        "pool": "replicapool",
                        "storageClass": "rook-ceph-block"
                    }
                },
                "persistentVolumeReclaimPolicy": "Delete",
                "storageClassName": "rook-ceph-block"
            },
            "status": {
                "phase": "Bound"
            }
        }

kubectl get pv --sort-by='{.spec.capacity.storage}' > /opt/dir/volume_list
               --sort-by=  .spec.capacity.storage
kubectl get pv --sort-by='{.spec.capacity.storage}' > opt/dir/volume_list

```



### 3. (3%) 创建Pod

按如下要求创建一个Pod：

- 名称：jenkins
- 使用 image: jenkins
- 在名为 website-frontend 的 **新** kubernetes namespace 中

```bash
$ kubectl get namespaces
$ kubectl create namespace website-frontend

apiVersion: v1
kind: Namespace
metadata:
  name: website-frontend


apiVersion: v1
kind: Pod
metadata:
  name: jenkins
  namespace: website-frontend
spec:
  containers:
  - image: jenkins
    name: jenkins


```

### 4. (4%) EmptyDir

按如下要求创建一个Pod：

- 名称：non-persistent-redis
- Container image: redis
- Persistent volume name: cache-control
- Mount Path: /data/redis

应在 staging namespace中发布，且该 volume **必须不能**是永久的。


```bash

$ kubectl get namespaces
$ kubectl create namespace staging

apiVersion: v1
kind: Pod
metadata:
  name: non-persistent-redis
  namespace: staging
spec:
  containers:
  - name: redis
    image: redis
    volumeMounts:
    - name: redis-storage
      mountPath: /data/redis
  volumes:
  - name: cache-control
    emptyDir: {}


```


### 5. (3%) DaemonSet

确保在 Kubernetes cluster 的每个node上都运行 pod nginx 的一个实例，此处，nginx 也表示必须使用的image 名称。切勿覆盖当前存在的任何taint。???

使用DaemonSet完成此任务，并使用 ds-kubesc12345 作为DaemonSet名称。



```
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ds-kubesc12345
  labels:
    name: ds-kubesc12345
spec:
  selector:
    matchLabels:
      name: ds-kubesc12345
  template:
    metadata:
      labels:
        name: ds-kubesc12345
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: ds-kubesc12345
        image: nginx
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
      






```






### 6. (4%) Deployment

按如下要求创建一个 Deployment:

- Name: nginx-app
- Image: nginx, Tag: 1.10.2-alpine
- Replicas: 3

然后，执行滚动更新，使用新版本 1.11.13-alpine 部署应用并记录此更新。

最后，将此更新回滚至之前版本 1.10.2-alpine



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.10.2-alpine


kubectl set image deployment.v1.apps/nginx-app nginx=nginx:1.11.13-alpine --record=true
kubectl set image deployment.v1.apps/nginx-app nginx=nginx:1.10.2-alpine --record=true

kubectl rollout status deployment.v1.apps/nginx-app

kubectl rollout history deployment.v1.apps/nginx-app
kubectl rollout history deployment.v1.apps/nginx-app --revision=xxx

kubectl rollout undo deployment.v1.apps/nginx-app
kubectl rollout undo deployment.v1.apps/nginx-app --to-revision=2

```





### 7. (3%) Deployment YAML

创建一个Deployment的 spec 文件：

- Image: nginx
- Replicas: 4
- Label: app_env_stage=prod
- Name: kual12345

将此spec文件的副本保存至 /opt/dir/deployment_spec.yaml (或 .json)。

完成后，清理(删除)执行此任务时生成的任何新 Kubernetes API 对象。



```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kual12345
  labels:
    app_env_stage: prod
spec:
  replicas: 4
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx


kubectl apply -f /opt/dir/deployment_spec.yaml
kubectl delete -f /opt/dir/deployment_spec.yaml



```












### 8. (7%) init container

执行以下任务：

- 添加一个 init container 至 bumpy-llama (已在 spec 文件 /opt/dir/Pod-spec-12345.yaml 中定义)
- init container 应该：创建一个名为 /workdir/faithful.txt 的 空文件
- 如果未检测到 /workdir/failthful.txt , Pod 应退出
- 一旦使用 init container 定义更新 spec 文件，则应创建Pod





```bash
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'if [ -f /workdir/faithful.txt ]; then sleep 10000; else exit 1; fi']
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: ['sh', '-c', 'touch /workdir/faithful.txt']


if [ -f /workdir/faithful.txt ]; then
     sleep 10000;
else
     exit 1;
fi

if [ -f /workdir/faithful.txt ]; then sleep 10000; else exit 1; fi


```











### 9. (9%) Secret

按如下要求创建一个 Kubernetes secret:

- Name: super-secret
- credential: alice

使用 **redis** image 创建一个名为 pod-secrets-via-file 的Pod，该Pod在 /secrets 目录下挂载名为 super-secret 的 Secret。

使用 **redis** image 创建另一个名为 pod-secrets-via-env 的 Pod，将 **credential** 导出为 CONFIDENTIAL 





```bash

echo -n 'alice' | base64
YWRtaW4=

apiVersion: v1
kind: Secret
metadata:
  name: super-secret
type: Opaque
data:
  credential: YWRtaW4=


apiVersion: v1
kind: Pod
metadata:
  name: pod-secrets-via-file
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/secrets"
      readOnly: true
  volumes:
  - name: foo
    secret:
      secretName: super-secret

apiVersion: v1
kind: Pod
metadata:
  name: pod-secrets-via-env
spec:
  containers:
  - name: mycontainer
    image: redis
    env:
      - name: CONFIDENTIAL
        valueFrom:
          secretKeyRef:
            name: super-secret
            key: credential
  restartPolicy: Never

```














### 10. (4%) Service  Endpoints ???

创建和配置 front-end-service service, 以便可通过 NodePort 访问该 service 并将其路由到名为 front-end 的现有Pod



```bash
kubectl expose pod nginx-nginx-58d78b945f-fxlz5 --name=front-end-service --type=NodePort --port=80


apiVersion: v1
kind: Service
metadata:
  name: front-end-service
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort



apiVersion: v1
kind: Endpoints
metadata:
  name: front-end-service
subsets:
  - addresses:
      - ip: 172.28.30.201
      - ip: 172.28.36.229
      - ip: 172.28.36.247
    ports:
      - port: 80
      
172.28.30.201:80
172.28.36.229:80
172.28.36.247:80

172.28.36.229
172.28.30.201
172.28.36.247





```







### 11. (4%) 多容器Pod

创建一个名为 kucc3 的Pod，在Pod里面分别为以下每个image单独运行一个 app container（可能会有1～4个images）:

nginx + redis + memcached + consul

```bash
apiVersion: v1
kind: Pod
metadata:
  name: kucc3
spec:
  containers:

  - name: nginx-container
    image: nginx

  - name: redis-container
    image: redis

  - name: memcached-container
    image: memcached

  - name: consul-container
    image: consul


```



### 12. (3%) Label

创建文件: /opt/dir/kucc12345.txt, 该文件列出在命名空间 baz 下关联服务 development 的所有 Pods。

文件格式应为每行只列一个 Pod 名称。

```bash
kubectl get svc -n baz --show-labels -o wide 
kubectl get pods -n baz --show-labels -o wide

kubectl get svc -n baz -o wide
kubectl get pods -n baz --show-labels -l dce.daocloud.io/app=nginx,dce.daocloud.io/component=nginx-nginx,pod-template-hash=1483465019



```



### 13. (2%) Node Selector

按如下要求调度一个Pod：

- 名称：nginx-kucc2345
- Image： nginx
- Node Selector: disk=spinning

```bash
$ kubectl label nodes <node-name> <label-key>=<label-value>

kubectl label nodes node01.daocloud.io disk=spinning

apiVersion: v1
kind: Pod
metadata:
  name: nginx-kucc2345
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disk: spinning

```


### 14. (3%) PV hostPath

创建名为 app-config 的Persistent Volume，容量为 1Gi, 访问模式为 ReadWriteOnce。Volume 类型为 hostPath，位于 /srv/app-config。

```bash
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-config
  labels:
    type: local
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/srv/app-config"

```



### 15. (4%) 集群故障排查

提供一个非完全正常运行的 Kubernetes Cluster, 在该Cluster中找出故障征兆。

确定node和出现故障的服务，采取措施修复故障服务，使 Cluster 恢复正常。确保所有更改永久有效。

提示：

- 可使用 ssh node-name 通过 ssh 命令连接到相应 node
- 可使用 sudo -i 命令在该 cluster 的任何node上获取更高权限

```bash
$ kubectl get componentstatuses -o wide
$ ssh 
$ systemctl list-units
$ systemctl status kubelet.service  # --pod-manifest-path=/etc/kubernetes/manifests 配置选项写错
$ systemctl show kubelet
$ systemctl enable kubelet
```




### 16. (4%) 节点故障排查

名为 **wk8s-node-0** 的 Kubernetes worker node 处于 **NotReady** 状态。

调查发生这种情况的原因，并采取相应措施将 Node 恢复为 **Ready** 状态，确保所做的任何更改永久有效。

提示：

- 可使用命令 ssh wk8s-node-0 连接到故障节点
- 可使用命令 sudo -i 在该节点上获取更高权限

```bash
$ kubectl get pods --show-labels
$ ssh 
$ systemctl list-units
$ systemctl status kubelet.service  # 发现没有启动
$ systemctl restart kubelet.service
$ systemctl show kubelet
$ systemctl daemon-reload  # 重载所有修改过的配置文件
$ systemctl enable kubelet.service  # 设置开机启动

```





### 17. (8%) 增加节点??? (Kubernetes 集群自动引导)

在本任务中，将配置一个新Node ik8s-node-0 并将其加入一个 Kubernetes Cluster, 方法如下：

- 配置 kubelet 以便自动轮换证书，且通过使用RBAC确保服务器和客户端的CSRs 能够得到自动批准和签署
- 确保创建合适的 cluster-info ConfigMap, 并在正确的Namespace中进行相应的配置，以便后续的Nodes能够轻松加入该集群
- 用于引导的 kubeconfig 应创建在新Node的 /etc/kubernetes/bootstrap-kubelet.conf 上(切勿在Node成功加入集群后移除此文件)
- 相应的集群级CA证书位于Node的 /etc/kubernetes/pki/ca.crt 上，应确保所有自动签发的证书都安装到Node的 /var/lib/kubelet/pki 目录上，并且成功引导后，将在 /etc/kubernetes/kubelet.conf 渲染 kubelet 的 kubeconfig 文件
- 使用额外的组引导尝试加入集群的Nodes，组的名称应为 system:bootstrappers:cka:default-node-token 
- 解决方案应在系统启动时随着 kubelet 的 systemd service unit 文件(可在 /etc/systemd/system/kubelet.service 中找到) 一起自动启动



要测试解决方案，应通过位于 /opt/dir/kube-flannel.yaml 的spec文件创建相应的资源。该过程将创建必要的资源和 kube-flannel-ds DaemonSet。应确保将此 DaemonSet 正确部署到集群的单个(应该是 **每个** )Node。

提示：

- 对于此任务，未在 ik8s-master-0 上配置或运行 kubelet, 请勿尝试配置
- 您将使用TLS引导来完成此任务
- 可通过以下命令获取 Kubernetes API服务器的IP地址： ssh ik8s-node-0 getent hosts ik8s-master-0
- API 服务器正在侦听常用端口 6443/tcp，且只会处理TLS请求
- kubelet 二进制文件已安装到 ik8s-node-0 的 /usr/bin/kubelet 上。执行此任务期间，无需将 kube-proxy 部署到集群
- 可以使用 ssh ik8s-node-0 来连接到 Worker Node
- 可以使用 ssh ik8s-master-0 来连接到 Master Node
- 无需进一步配置在 ik8s-master-0 上运行的 Control Plane 服务
- 可使用 sudo -i 在这两个 Nodes 上获取更高权限
- 已在 ik8s-node-0 上安装并运行 Docker



### 18. (4%) Drain

将名为 **ek8s-node-1** 的Node设置为不可用，并重新调度该Node上所有运行的Pods。

```bash
$ kubectl get nodes --show-labels
$ kubectl drain ek8s-node-1 --force
$ kubectl get pods -o wide --show-labels
$ kubectl delete pod baz foo


  cordon         标记 node 为 unschedulable
  uncordon       标记 node 为 schedulable
  drain          Drain node in preparation for maintenance
  
$ kubectl cordon node02.daocloud.io
$ kubectl uncordon node02.daocloud.io
$ kubectl drain node02.daocloud.io --force --ignore-daemonsets

```



https://blog.csdn.net/stonexmx/article/details/73543185







### 19. (7%) Etcd

为在 [https://127.0.0.1:2379](https://127.0.0.1:2379/) 运行的 etcd 实例创建快照，并将快照保存至文件路径 /data/backup/etcd-snapshot.db。

Etcd 实例运行的 etcd 版本为 3.3.10。

以下TLS证书密钥用于通过 etcdctl 连接服务器：

- CA证书：/opt/dir/ca.crt
- 客户端证书：/opt/dir/etcd-client.crt
- 客户端密钥：/opt/dir/etcd-client.key

```bash
ETCDCTL_API=3 etcdctl -h

ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
--cacert=/opt/dir/ca.crt \
--cert=/opt/dir/etcd-client.crt \
--key=/opt/dir/etcd-client.key \
member list

ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
--cacert=/opt/dir/ca.crt \
--cert=/opt/dir/etcd-client.crt \
--key=/opt/dir/etcd-client.key \
snapshot save /data/backup/etcd-snapshot.db

etcdctl -h
--cacert=""                verify certificates证书 of TLS-enabled secure servers using this CA bundle
      --cert=""                    identify secure client using this TLS certificate证书 file
      --command-timeout=5s            timeout for short running command (excluding dial timeout)
      --debug[=false]                enable client-side debug logging
      --dial-timeout=2s                dial timeout for client connections
      --endpoints=[127.0.0.1:2379]        gRPC endpoints
      --hex[=false]                print byte strings as hex encoded strings
      --insecure-skip-tls-verify[=false]    skip server certificate verification
      --insecure-transport[=true]        disable transport security for client connections
      --key=""                    identify secure client using this TLS key file
      --user=""                    username[:password] for authentication (prompt if password is not supplied)
  -w, --write-out="simple"            set the output format (fields, json, protobuf, simple, table)

```

### 20. (7%) DNS

按如下要求创建一个Deployment：

- 名称：nginx-random
- 通过 Service 暴露：nginx-random
- 确保 Service 和 Pod 可通过各自的 DNS 记录访问
- 在此 Deployment 中运行的任何 Pod 内的 Container 都应使用 **nginx** image

接下来，使用实用工具 nslookup 查询该 Service 和 Pod 的 DNS 记录，并将输出结果分别写入 /opt/dir/service.dns 和 /opt/dir/Pod.dns。

确保在任何测试中使用 busybox:1.28 image(或更早版本)，因为最新发布的的版本存在 Upstream 漏洞，会影响使用 nslookup。

```bash
$ kubectl get pods -o wide --show-labels
$ kubectl get deployments -o wide --show-labels
$ kubectl get services -o wide --show-labels

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-random
  labels:
    app: nginx
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: 12.100.1.3/centrin-1/nginx:1.14.1
        ports:
        - containerPort: 80

---

apiVersion: v1
kind: Service
metadata:
  name: nginx-random
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80


$ kubectl get pods -o wide --show-labels
$ kubectl get deployments -o wide --show-labels
$ kubectl get services -o wide --show-labels

kubectl run busybox -it --rm --image=busybox:1.28 sh
nslookup nginx-random
nslookup xxx

```



### 21. (2%) CPU

通过Pod Label **name=cpu-user**，找到运行时占用大量CPU的Pod，并将占用CPU最高的Pod名称写入文件 /opt/dir/1234.txt (已存在)。

```bash
kubectl top pod -l name=cpu-user
kubectl top pod -l name=cpu-user --all-namespaces

```

### 22. (2%) Taint: NoSchedule

检查有多少Nodes已准备就绪(不包括被打上**Taint: NoSchedule** 的节点)，并将数量写入 /opt/dir/nodes.txt。

```bash
$ kubectl get nodes -o wide --show-labels
$ kubectl describe nodes xxx | grep -E '(Roles|Taints)'

```



### 23. (1%) Scale

将 Deployment /  **loadbalancer** 扩展至 5 Pods。

```bash
$ kubectl get deployments -o wide --show-labels
$ kubectl get pods -o wide --show-labels
$ kubectl scale --replicas=5 deployment/loadbalancer
$ kubectl get deployments -o wide --show-labels
$ kubectl get pods -o wide --show-labels

```



### 24. (4%) Manifests

在标签 **name=wk8s-node-1** 的Node上配置 kubelet systemd managed service,  以自动启动包含名称为 nginx、image 为 app 的单 Container 的 Pod。

所需的所有 spec 文件应该在该 Node 的 /etc/kubernetes/manifests 目录中。

提示：

- 可使用命令 ssh wk8s-node- 连接到相应节点
- 可使用命令 sudo -i 在该节点上获取更高权限

```bash
$ kubectl get nodes --show-labels
$ ssh 
$ sudo -i 
$ cat /etc/kubernetes/manifests/static-web.yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-web
spec:
  containers:
  - name: nginx
    image: app

$ systemctl list-units
$ systemctl status kubelet.service
$ systemctl show kubelet.service | grep -i path

--pod-manifest-path=/etc/kubernetes/manifests/

$ systemctl status kubelet
$ systemctl restart kubelet
$ kubectl get pods -o wide --show-labels

```