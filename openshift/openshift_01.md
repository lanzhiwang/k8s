# openshift

## 文档

https://docs.openshift.com/

## 红帽账号

https://access.redhat.com/logout

账号：it@daocloud.io

密码： 7758521abc@r

7758521abc@r



```bash

subscription-manager register --username it@daocloud.io --password 7758521abc@r --auto-attach


```






## openhift 相关产品

* OpenShift Online
* OpenShift Container Platform
* Azure Red Hat OpenShift
* OpenShift Container Engine (OCE)
* OpenShift Dedicated  OpenShift专用
* OKD (openshift/origin)

### OpenShift Online
Red Hat's public cloud application deployment and hosting platform.  红帽的公共云应用程序部署和托管平台

https://manage.openshift.com/



### OpenShift Container Platform
Red Hat's private, on-premise cloud application deployment and hosting platform.  Red Hat的私有，内部部署云应用程序部署和托管平台。

### Azure Red Hat OpenShift
Azure Red Hat OpenShift provides single-tenant, high-availability Kubernetes clusters on Azure, supported by Red Hat and Microsoft.  Azure Red Hat OpenShift在Azure上提供单租户，高可用性Kubernetes集群，由Red Hat和Microsoft提供支持。

### OpenShift Container Engine (OCE)
The OpenShift Container Engine is the core of the OpenShift Container Platform. Use OpenShift Container Platform docs links for OpenShift Container Engine documentation.  OpenShift容器引擎是OpenShift容器平台的核心。 使用OpenShift Container Platform文档链接获取OpenShift Container Engine文档。

Red Hat OpenShift Container Engine is a new product offering from Red Hat that lets you use OpenShift Container Platform as a production platform for launching containers. You download and install OpenShift Container Engine in the same way as OpenShift Container Platform, but OpenShift Container Engine offers a subset of the features that OpenShift Container Platform does.   Red Hat OpenShift Container Engine是Red Hat的新产品，它允许您使用OpenShift Container Platform作为启动容器的生产平台。 您以与OpenShift Container Platform相同的方式下载和安装OpenShift Container Engine，但OpenShift Container Engine提供了OpenShift Container Platform所具有的功能的子集。

OpenShift Container Platform 的功能比 OpenShift Container Engine 的功能多些。OpenShift Container Platform 在 OpenShift Container Engine 功能的基础做了一些扩展。

### OpenShift Dedicated  OpenShift专用
Red Hat's managed public cloud application deployment and hosting service.  Red Hat管理的公共云应用程序部署和托管服务。

### OKD(OpenShift Origin)

OpenShift's open source, upstream project.   OpenShift的开源上游项目。

OKD is a distribution of Kubernetes optimized for continuous application development and multi-tenant deployment. OKD also serves as the upstream code base upon which Red Hat OpenShift Online and Red Hat OpenShift Container Platform are built.  OKD是Kubernetes的发行版，针对持续应用程序开发和多租户部署进行了优化。 OKD还可以作为构建Red Hat OpenShift Online和Red Hat OpenShift Container Platform的上游代码库。

对应到 GitHub 上的 https://github.com/openshift/origin 项目


## 红帽订阅功能

https://access.redhat.com/zh_CN/solutions/1119463

```bash
yum -y install subscription-manager
```

## 使用 OKD (openshift/origin)

```bash
# https://github.com/openshift/origin/releases

# 安装 docker

[root@huzhi-code ~]# wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz

[root@huzhi-code ~]# tar -zxvf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz 

[root@huzhi-code ~]# ll
total 235092
-rwxrwxr-x 1 root root 120350344 Oct 11  2018 kubectl
-rw-rwxr-- 1 root root     10759 Oct 11  2018 LICENSE
-rwxrwxr-x 1 root root 120350344 Oct 11  2018 oc
-rw-rwxr-- 1 root root     15834 Oct 11  2018 README.md
[root@huzhi-code ~]# 

[root@huzhi-code ~]# cp ./oc /usr/bin/oc

##############################################

[[root@huzhi-code ~]# oc version
oc v3.11.0+0cbc58b
kubernetes v1.11.0+d4cacc0
features: Basic-Auth GSSAPI Kerberos SPNEGO
[root@huzhi-code openshift]# 

第一次执行：

[root@huzhi-code ~]# oc cluster up
Getting a Docker client ...
Checking if image openshift/origin-control-plane:v3.11 is available ...
Pulling image openshift/origin-control-plane:v3.11
E0805 15:27:46.798909    6917 helper.go:179] Reading docker config from /root/.docker/config.json failed: open /root/.docker/config.json: no such file or directory, will attempt to pull image docker.io/openshift/origin-control-plane:v3.11 anonymously
Pulled 2/5 layers, 41% complete
Pulled 3/5 layers, 66% complete
Pulled 3/5 layers, 74% complete
Pulled 3/5 layers, 84% complete
Pulled 4/5 layers, 90% complete
Pulled 4/5 layers, 96% complete
Pulled 5/5 layers, 100% complete
Extracting
Image pull complete
Pulling image openshift/origin-cli:v3.11
E0805 15:30:26.511506    6917 helper.go:179] Reading docker config from /root/.docker/config.json failed: open /root/.docker/config.json: no such file or directory, will attempt to pull image docker.io/openshift/origin-cli:v3.11 anonymously
Image pull complete
Pulling image openshift/origin-node:v3.11
E0805 15:30:31.606629    6917 helper.go:179] Reading docker config from /root/.docker/config.json failed: open /root/.docker/config.json: no such file or directory, will attempt to pull image docker.io/openshift/origin-node:v3.11 anonymously
Pulled 5/6 layers, 84% complete
Pulled 5/6 layers, 90% complete
Pulled 5/6 layers, 97% complete
Pulled 6/6 layers, 100% complete
Extracting
Image pull complete
Checking type of volume mount ...
Determining server IP ...
Checking if OpenShift is already running ...
Checking for supported Docker version (=>1.22) ...
Checking if insecured registry is configured properly in Docker ...
error: did not detect an --insecure-registry argument on the Docker daemon
[root@huzhi-code openshift]# 

##############################################

相关镜像

openshift/origin-control-plane:v3.11
openshift/origin-cli:v3.11
openshift/origin-node:v3.11

客户端配置文件，但命令执行完毕后没有该文件
/root/.docker/config.json

在 oc cluster up 执行的当期目录中生成 openshift.local.clusterup 目录
/root/work/openshift/openshift.local.clusterup
[root@huzhi-code openshift.local.clusterup]# tree -a .
.
├── components.json
├── etcd
├── openshift.local.pv
└── openshift.local.volumes

3 directories, 1 file
[root@huzhi-code openshift.local.clusterup]# 


第二次执行：
[root@huzhi-code ~]# oc cluster up --help
Starts an OpenShift cluster using Docker containers, provisioning a registry, router, initial templates, and a default
project. 

This command will attempt to use an existing connection to a Docker daemon. Before running the command, ensure that you
can execute docker commands successfully (i.e. 'docker ps'). 

By default, the OpenShift cluster will be setup to use a routing suffix that ends in nip.io. This is to allow dynamic
host names to be created for routes. An alternate routing suffix can be specified using the --routing-suffix flag. 

A public hostname can also be specified for the server with the --public-hostname flag.

Usage:
  oc cluster up [flags]

Examples:
  # Start OpenShift using a specific public host name
  oc cluster up --public-hostname=my.address.example.com

Options:
      --base-dir='': Directory on Docker host for cluster up configuration
      --enable=[*]: A list of components to enable.  '*' enables all on-by-default components, 'foo' enables the
component named 'foo', '-foo' disables the component named 'foo'.
All components: automation-service-broker, centos-imagestreams, persistent-volumes, registry, rhel-imagestreams, router,
sample-templates, service-catalog, template-service-broker, web-console
Disabled-by-default components: automation-service-broker, rhel-imagestreams, service-catalog, template-service-broker
      --forward-ports=false: Use Docker port-forwarding to communicate with origin container. Requires 'socat' locally.
      --http-proxy='': HTTP proxy to use for master and builds
      --https-proxy='': HTTPS proxy to use for master and builds
      --image='openshift/origin-${component}:${version}': Specify the images to use for OpenShift
      --no-proxy=[]: List of hosts or subnets for which a proxy should not be used
      --public-hostname='': Public hostname for OpenShift cluster
      --routing-suffix='': Default suffix for server routes
      --server-loglevel=0: Log level for OpenShift server
      --skip-registry-check=false: Skip Docker daemon registry check
      --write-config=false: Write the configuration files into host config dir

Use "oc options" for a list of global command-line options (applies to all commands).
[root@huzhi-code ~]# 

[root@huzhi-code openshift-cluster]# oc cluster up --base-dir=/root/work/openshift/openshift-cluster --write-config=true --skip-registry-check=true
Getting a Docker client ...
Checking if image openshift/origin-control-plane:v3.11 is available ...
Checking type of volume mount ...
Determining server IP ...
Checking if OpenShift is already running ...
Checking for supported Docker version (=>1.22) ...
Checking if required ports are available ...
Checking if OpenShift client is configured properly ...
Checking if image openshift/origin-control-plane:v3.11 is available ...
Starting OpenShift using openshift/origin-control-plane:v3.11 ...
I0805 16:09:03.212590    7913 config.go:40] Running "create-master-config"
I0805 16:09:05.252789    7913 config.go:46] Running "create-node-config"
Wrote config to: "/root/work/openshift/openshift-cluster"
[root@huzhi-code openshift-cluster]# 
[root@huzhi-code openshift-cluster]# 
[root@huzhi-code openshift-cluster]# ll
total 16
-rw-r--r-- 1 root root  113 Aug  5 16:09 components.json
drwxr-xr-x 2 root root    6 Aug  5 16:09 etcd
drwxr-xr-x 2 root root 4096 Aug  5 16:09 kube-apiserver
drwx------ 2 root root  228 Aug  5 16:09 kubedns
drwxr-xr-x 2 root root  158 Aug  5 16:09 logs
drwx------ 2 root root  209 Aug  5 16:09 node
drwxr-xr-x 2 root root 4096 Aug  5 16:09 openshift-apiserver
drwxr-xr-x 2 root root 4096 Aug  5 16:09 openshift-controller-manager
drwxr-xr-x 2 root root    6 Aug  5 16:09 openshift.local.pv
drwxr-xr-x 2 root root    6 Aug  5 16:09 openshift.local.volumes
drwxr-xr-x 2 root root  108 Aug  5 16:09 static-pod-manifests
[root@huzhi-code openshift-cluster]# 

客户端配置文件，但第二次命令执行完毕后没有该文件
/root/.docker/config.json

[root@huzhi-code openshift-cluster]# tree -a .
.
├── components.json
├── etcd
├── kube-apiserver
│   ├── admin.crt
│   ├── admin.key
│   ├── admin.kubeconfig
│   ├── ca-bundle.crt
│   ├── ca.crt
│   ├── ca.key
│   ├── ca.serial.txt
│   ├── etcd.server.crt
│   ├── etcd.server.key
│   ├── frontproxy-ca.crt
│   ├── frontproxy-ca.key
│   ├── frontproxy-ca.serial.txt
│   ├── master-config.yaml
│   ├── master.etcd-client.crt
│   ├── master.etcd-client.key
│   ├── master.kubelet-client.crt
│   ├── master.kubelet-client.key
│   ├── master.proxy-client.crt
│   ├── master.proxy-client.key
│   ├── master.server.crt
│   ├── master.server.key
│   ├── openshift-aggregator.crt
│   ├── openshift-aggregator.key
│   ├── openshift-master.crt
│   ├── openshift-master.key
│   ├── openshift-master.kubeconfig
│   ├── serviceaccounts.private.key
│   ├── serviceaccounts.public.key
│   ├── service-signer.crt
│   └── service-signer.key
├── kubedns
│   ├── ca.crt
│   ├── master-client.crt
│   ├── master-client.key
│   ├── node-client-ca.crt
│   ├── node-config.yaml
│   ├── node.kubeconfig
│   ├── node-registration.json
│   ├── resolv.conf
│   ├── server.crt
│   └── server.key
├── logs
│   ├── create-master-config-001.stderr
│   ├── create-master-config-001.stdout
│   ├── create-node-config-001.stderr
│   └── create-node-config-001.stdout
├── node
│   ├── ca.crt
│   ├── master-client.crt
│   ├── master-client.key
│   ├── node-client-ca.crt
│   ├── node-config.yaml
│   ├── node.kubeconfig
│   ├── node-registration.json
│   ├── server.crt
│   └── server.key
├── openshift-apiserver
│   ├── admin.crt
│   ├── admin.key
│   ├── admin.kubeconfig
│   ├── ca-bundle.crt
│   ├── ca.crt
│   ├── ca.key
│   ├── ca.serial.txt
│   ├── etcd.server.crt
│   ├── etcd.server.key
│   ├── frontproxy-ca.crt
│   ├── frontproxy-ca.key
│   ├── frontproxy-ca.serial.txt
│   ├── master-config.yaml
│   ├── master.etcd-client.crt
│   ├── master.etcd-client.key
│   ├── master.kubelet-client.crt
│   ├── master.kubelet-client.key
│   ├── master.proxy-client.crt
│   ├── master.proxy-client.key
│   ├── master.server.crt
│   ├── master.server.key
│   ├── openshift-aggregator.crt
│   ├── openshift-aggregator.key
│   ├── openshift-master.crt
│   ├── openshift-master.key
│   ├── openshift-master.kubeconfig
│   ├── serviceaccounts.private.key
│   ├── serviceaccounts.public.key
│   ├── service-signer.crt
│   └── service-signer.key
├── openshift-controller-manager
│   ├── admin.crt
│   ├── admin.key
│   ├── admin.kubeconfig
│   ├── ca-bundle.crt
│   ├── ca.crt
│   ├── ca.key
│   ├── ca.serial.txt
│   ├── etcd.server.crt
│   ├── etcd.server.key
│   ├── frontproxy-ca.crt
│   ├── frontproxy-ca.key
│   ├── frontproxy-ca.serial.txt
│   ├── master-config.yaml
│   ├── master.etcd-client.crt
│   ├── master.etcd-client.key
│   ├── master.kubelet-client.crt
│   ├── master.kubelet-client.key
│   ├── master.proxy-client.crt
│   ├── master.proxy-client.key
│   ├── master.server.crt
│   ├── master.server.key
│   ├── openshift-aggregator.crt
│   ├── openshift-aggregator.key
│   ├── openshift-master.crt
│   ├── openshift-master.key
│   ├── openshift-master.kubeconfig
│   ├── serviceaccounts.private.key
│   ├── serviceaccounts.public.key
│   ├── service-signer.crt
│   └── service-signer.key
├── openshift.local.pv
├── openshift.local.volumes
└── static-pod-manifests
    ├── apiserver.yaml
    ├── etcd.yaml
    ├── kube-controller-manager.yaml
    └── kube-scheduler.yaml

10 directories, 118 files
[root@huzhi-code openshift-cluster]# 

##############################################

[root@huzhi-code openshift-cluster]# oc help
OpenShift Client 

This client helps you develop, build, deploy, and run your applications on any OpenShift or Kubernetes compatible
platform. It also includes the administrative commands for managing a cluster under the 'adm' subcommand.

Usage:
  oc [flags]

Basic Commands:
  types           An introduction to concepts and types
  login           Log in to a server
  new-project     Request a new project
  new-app         Create a new application
  status          Show an overview of the current project
  project         Switch to another project
  projects        Display existing projects
  explain         Documentation of resources
  cluster         Start and stop OpenShift cluster

Build and Deploy Commands:
  rollout         Manage a Kubernetes deployment or OpenShift deployment config
  rollback        Revert part of an application back to a previous deployment
  new-build       Create a new build configuration
  start-build     Start a new build
  cancel-build    Cancel running, pending, or new builds
  import-image    Imports images from a Docker registry
  tag             Tag existing images into image streams

Application Management Commands:
  get             Display one or many resources
  describe        Show details of a specific resource or group of resources
  edit            Edit a resource on the server
  set             Commands that help set specific features on objects
  label           Update the labels on a resource
  annotate        Update the annotations on a resource
  expose          Expose a replicated application as a service or route
  delete          Delete one or more resources
  scale           Change the number of pods in a deployment
  autoscale       Autoscale a deployment config, deployment, replication controller, or replica set
  secrets         Manage secrets
  serviceaccounts Manage service accounts in your project

Troubleshooting and Debugging Commands:
  logs            Print the logs for a resource
  rsh             Start a shell session in a pod
  rsync           Copy files between local filesystem and a pod
  port-forward    Forward one or more local ports to a pod
  debug           Launch a new instance of a pod for debugging
  exec            Execute a command in a container
  proxy           Run a proxy to the Kubernetes API server
  attach          Attach to a running container
  run             Run a particular image on the cluster
  cp              Copy files and directories to and from containers.
  wait            Experimental: Wait for one condition on one or many resources

Advanced Commands:
  adm             Tools for managing a cluster
  create          Create a resource from a file or from stdin.
  replace         Replace a resource by filename or stdin
  apply           Apply a configuration to a resource by filename or stdin
  patch           Update field(s) of a resource using strategic merge patch
  process         Process a template into list of resources
  export          Export resources so they can be used elsewhere
  extract         Extract secrets or config maps to disk
  idle            Idle scalable resources
  observe         Observe changes to resources and react to them (experimental)
  policy          Manage authorization policy
  auth            Inspect authorization
  convert         Convert config files between different API versions
  import          Commands that import applications
  image           Useful commands for managing images
  registry        Commands for working with the registry
  api-versions    Print the supported API versions on the server, in the form of "group/version"
  api-resources   Print the supported API resources on the server

Settings Commands:
  logout          End the current server session
  config          Change configuration files for the client
  whoami          Return information about the current session
  completion      Output shell completion code for the specified shell (bash or zsh)

Other Commands:
  ex              Experimental commands under active development
  help            Help about any command
  plugin          Runs a command-line plugin
  version         Display client and server versions

Use "oc <command> --help" for more information about a given command.
Use "oc options" for a list of global command-line options (applies to all commands).
[root@huzhi-code openshift-cluster]# 



[root@huzhi-code logs]# cat create-master-config-001.stdout 
Wrote master config to: /var/lib/origin/openshift.local.config/master-config.yaml
[root@huzhi-code logs]# 
[root@huzhi-code logs]# cat create-node-config-001.stdout 
Generating node credentials ...
Created node config for localhost in /var/lib/origin/openshift.local.config
[root@huzhi-code logs]# 






[root@huzhi-code openshift-cluster]# cat /etc/docker/daemon.json
{
 "insecure-registries": ["172.30.0.0/16"]
}
[root@huzhi-code openshift-cluster]# 
[root@huzhi-code openshift-cluster]# systemctl restart docker.service

# 关闭防火墙

[root@huzhi-code openshift-cluster]# oc cluster up
Getting a Docker client ...
Checking if image openshift/origin-control-plane:v3.11 is available ...
Checking type of volume mount ...
Determining server IP ...
Checking if OpenShift is already running ...
Checking for supported Docker version (=>1.22) ...
Checking if insecured registry is configured properly in Docker ...
Checking if required ports are available ...
Checking if OpenShift client is configured properly ...
Checking if image openshift/origin-control-plane:v3.11 is available ...
Starting OpenShift using openshift/origin-control-plane:v3.11 ...
I0805 17:08:22.869749   10256 config.go:40] Running "create-master-config"
I0805 17:08:25.483043   10256 config.go:46] Running "create-node-config"
I0805 17:08:26.956352   10256 flags.go:30] Running "create-kubelet-flags"
I0805 17:08:27.513521   10256 run_kubelet.go:49] Running "start-kubelet"
I0805 17:08:27.720387   10256 run_self_hosted.go:181] Waiting for the kube-apiserver to be ready ...
I0805 17:11:11.738140   10256 interface.go:26] Installing "kube-proxy" ...
I0805 17:11:11.738167   10256 interface.go:26] Installing "kube-dns" ...
I0805 17:11:11.738180   10256 interface.go:26] Installing "openshift-service-cert-signer-operator" ...
I0805 17:11:11.738191   10256 interface.go:26] Installing "openshift-apiserver" ...
I0805 17:11:11.738245   10256 apply_template.go:81] Installing "openshift-apiserver"
I0805 17:11:11.738569   10256 apply_template.go:81] Installing "kube-proxy"
I0805 17:11:11.738605   10256 apply_template.go:81] Installing "kube-dns"
I0805 17:11:11.738621   10256 apply_template.go:81] Installing "openshift-service-cert-signer-operator"
I0805 17:11:14.512208   10256 interface.go:41] Finished installing "kube-proxy" "kube-dns" "openshift-service-cert-signer-operator" "openshift-apiserver"
I0805 17:15:09.584940   10256 run_self_hosted.go:242] openshift-apiserver available
I0805 17:15:09.584978   10256 interface.go:26] Installing "openshift-controller-manager" ...
I0805 17:15:09.584998   10256 apply_template.go:81] Installing "openshift-controller-manager"
I0805 17:15:11.873980   10256 interface.go:41] Finished installing "openshift-controller-manager"
Adding default OAuthClient redirect URIs ...
Adding registry ...
Adding sample-templates ...
Adding persistent-volumes ...
Adding web-console ...
Adding centos-imagestreams ...
Adding router ...
I0805 17:15:11.891047   10256 interface.go:26] Installing "openshift-image-registry" ...
I0805 17:15:11.891058   10256 interface.go:26] Installing "sample-templates" ...
I0805 17:15:11.891066   10256 interface.go:26] Installing "persistent-volumes" ...
I0805 17:15:11.891078   10256 interface.go:26] Installing "openshift-web-console-operator" ...
I0805 17:15:11.891085   10256 interface.go:26] Installing "centos-imagestreams" ...
I0805 17:15:11.891091   10256 interface.go:26] Installing "openshift-router" ...
I0805 17:15:11.892484   10256 interface.go:26] Installing "sample-templates/postgresql" ...
I0805 17:15:11.892498   10256 interface.go:26] Installing "sample-templates/rails quickstart" ...
I0805 17:15:11.892505   10256 interface.go:26] Installing "sample-templates/sample pipeline" ...
I0805 17:15:11.892516   10256 interface.go:26] Installing "sample-templates/mysql" ...
I0805 17:15:11.892522   10256 interface.go:26] Installing "sample-templates/mariadb" ...
I0805 17:15:11.892529   10256 interface.go:26] Installing "sample-templates/cakephp quickstart" ...
I0805 17:15:11.892535   10256 interface.go:26] Installing "sample-templates/dancer quickstart" ...
I0805 17:15:11.892546   10256 interface.go:26] Installing "sample-templates/django quickstart" ...
I0805 17:15:11.892553   10256 interface.go:26] Installing "sample-templates/nodejs quickstart" ...
I0805 17:15:11.892559   10256 interface.go:26] Installing "sample-templates/jenkins pipeline ephemeral" ...
I0805 17:15:11.892566   10256 interface.go:26] Installing "sample-templates/mongodb" ...
I0805 17:15:11.892800   10256 apply_list.go:67] Installing "sample-templates/mongodb"
I0805 17:15:11.893007   10256 apply_list.go:67] Installing "sample-templates/mariadb"
I0805 17:15:11.893232   10256 apply_list.go:67] Installing "sample-templates/cakephp quickstart"
I0805 17:15:11.893424   10256 apply_list.go:67] Installing "sample-templates/postgresql"
I0805 17:15:11.893578   10256 apply_list.go:67] Installing "sample-templates/dancer quickstart"
I0805 17:15:11.893818   10256 apply_list.go:67] Installing "sample-templates/rails quickstart"
I0805 17:15:11.894073   10256 apply_list.go:67] Installing "sample-templates/django quickstart"
I0805 17:15:11.894183   10256 apply_list.go:67] Installing "sample-templates/sample pipeline"
I0805 17:15:11.894555   10256 apply_list.go:67] Installing "sample-templates/mysql"
I0805 17:15:11.894563   10256 apply_list.go:67] Installing "sample-templates/nodejs quickstart"
I0805 17:15:11.895754   10256 apply_list.go:67] Installing "sample-templates/jenkins pipeline ephemeral"
I0805 17:15:11.897647   10256 apply_list.go:67] Installing "centos-imagestreams"
I0805 17:15:11.898852   10256 apply_template.go:81] Installing "openshift-web-console-operator"
I0805 17:15:19.747914   10256 interface.go:41] Finished installing "sample-templates/postgresql" "sample-templates/rails quickstart" "sample-templates/sample pipeline" "sample-templates/mysql" "sample-templates/mariadb" "sample-templates/cakephp quickstart" "sample-templates/dancer quickstart" "sample-templates/django quickstart" "sample-templates/nodejs quickstart" "sample-templates/jenkins pipeline ephemeral" "sample-templates/mongodb"
I0805 17:16:36.912005   10256 interface.go:41] Finished installing "openshift-image-registry" "sample-templates" "persistent-volumes" "openshift-web-console-operator" "centos-imagestreams" "openshift-router"
Login to server ...
Creating initial project "myproject" ...
Server Information ...
OpenShift server started.

The server is accessible via web console at:
    https://127.0.0.1:8443

You are logged in as:
    User:     developer
    Password: <any value>

To login as administrator:
    oc login -u system:admin

[root@huzhi-code openshift-cluster]# ll
total 0
drwxr-xr-x 12 root root 250 Aug  5 17:08 openshift.local.clusterup
[root@huzhi-code openshift-cluster]# ll openshift.local.clusterup/
total 24
-rw-r--r--   1 root root  113 Aug  5 17:08 components.json
drwxr-xr-x   3 root root   20 Aug  5 17:09 etcd
drwxr-xr-x   2 root root 4096 Aug  5 17:15 kube-apiserver
drwx------   2 root root  228 Aug  5 17:08 kubedns
drwxr-xr-x   2 root root 4096 Aug  5 17:15 logs
drwx------   2 root root  209 Aug  5 17:08 node
drwxr-xr-x   2 root root 4096 Aug  5 17:08 openshift-apiserver
drwxr-xr-x   2 root root 4096 Aug  5 17:08 openshift-controller-manager
drwxr-xr-x 103 root root 4096 Aug  5 17:16 openshift.local.pv
drwxr-xr-x   5 root root   83 Aug  5 17:08 openshift.local.volumes
drwxr-xr-x   2 root root  108 Aug  5 17:08 static-pod-manifests
[root@huzhi-code openshift-cluster]# 
[root@huzhi-code openshift-cluster]# 
[root@huzhi-code openshift-cluster]# 
[root@huzhi-code openshift-cluster]# 


oc cluster up --base-dir='/root/work/openshift/openshift-cluster' --write-config=true --public-hostname='10.0.8.11'

# --write-config=true 选项不能使用

# https://medium.com/@fabiojose/working-with-oc-cluster-up-a052339ea219
[root@huzhi-openshift openshift-cluster]# oc cluster up --base-dir='/root/work/openshift/openshift-cluster' --public-hostname='10.0.8.11'
Getting a Docker client ...
Checking if image openshift/origin-control-plane:v3.11 is available ...
Checking type of volume mount ...
Determining server IP ...
Using public hostname IP 10.0.8.11 as the host IP
Checking if OpenShift is already running ...
Checking for supported Docker version (=>1.22) ...
Checking if insecured registry is configured properly in Docker ...
Checking if required ports are available ...
Checking if OpenShift client is configured properly ...
Checking if image openshift/origin-control-plane:v3.11 is available ...
Starting OpenShift using openshift/origin-control-plane:v3.11 ...
I0805 18:54:36.163335    9414 config.go:40] Running "create-master-config"
I0805 18:54:39.803681    9414 config.go:46] Running "create-node-config"
I0805 18:54:40.954607    9414 flags.go:30] Running "create-kubelet-flags"
I0805 18:54:41.492137    9414 run_kubelet.go:49] Running "start-kubelet"
I0805 18:54:41.702749    9414 run_self_hosted.go:181] Waiting for the kube-apiserver to be ready ...
I0805 18:55:07.719877    9414 interface.go:26] Installing "kube-proxy" ...
I0805 18:55:07.719902    9414 interface.go:26] Installing "kube-dns" ...
I0805 18:55:07.719909    9414 interface.go:26] Installing "openshift-service-cert-signer-operator" ...
I0805 18:55:07.719915    9414 interface.go:26] Installing "openshift-apiserver" ...
I0805 18:55:07.719947    9414 apply_template.go:81] Installing "openshift-apiserver"
I0805 18:55:07.720166    9414 apply_template.go:81] Installing "kube-proxy"
I0805 18:55:07.720348    9414 apply_template.go:81] Installing "kube-dns"
I0805 18:55:07.720483    9414 apply_template.go:81] Installing "openshift-service-cert-signer-operator"
I0805 18:55:12.683229    9414 interface.go:41] Finished installing "kube-proxy" "kube-dns" "openshift-service-cert-signer-operator" "openshift-apiserver"
I0805 18:57:00.714298    9414 run_self_hosted.go:242] openshift-apiserver available
I0805 18:57:00.714358    9414 interface.go:26] Installing "openshift-controller-manager" ...
I0805 18:57:00.714395    9414 apply_template.go:81] Installing "openshift-controller-manager"
I0805 18:57:04.039392    9414 interface.go:41] Finished installing "openshift-controller-manager"
Adding default OAuthClient redirect URIs ...
Adding router ...
Adding sample-templates ...
Adding web-console ...
Adding centos-imagestreams ...
Adding registry ...
Adding persistent-volumes ...
I0805 18:57:04.066782    9414 interface.go:26] Installing "openshift-router" ...
I0805 18:57:04.066796    9414 interface.go:26] Installing "sample-templates" ...
I0805 18:57:04.066805    9414 interface.go:26] Installing "openshift-web-console-operator" ...
I0805 18:57:04.066813    9414 interface.go:26] Installing "centos-imagestreams" ...
I0805 18:57:04.066825    9414 interface.go:26] Installing "openshift-image-registry" ...
I0805 18:57:04.066833    9414 interface.go:26] Installing "persistent-volumes" ...
I0805 18:57:04.067684    9414 interface.go:26] Installing "sample-templates/dancer quickstart" ...
I0805 18:57:04.067697    9414 interface.go:26] Installing "sample-templates/nodejs quickstart" ...
I0805 18:57:04.067704    9414 interface.go:26] Installing "sample-templates/jenkins pipeline ephemeral" ...
I0805 18:57:04.067710    9414 interface.go:26] Installing "sample-templates/mysql" ...
I0805 18:57:04.067717    9414 interface.go:26] Installing "sample-templates/postgresql" ...
I0805 18:57:04.067724    9414 interface.go:26] Installing "sample-templates/cakephp quickstart" ...
I0805 18:57:04.067730    9414 interface.go:26] Installing "sample-templates/rails quickstart" ...
I0805 18:57:04.067738    9414 interface.go:26] Installing "sample-templates/sample pipeline" ...
I0805 18:57:04.067748    9414 interface.go:26] Installing "sample-templates/mongodb" ...
I0805 18:57:04.067754    9414 interface.go:26] Installing "sample-templates/mariadb" ...
I0805 18:57:04.067760    9414 interface.go:26] Installing "sample-templates/django quickstart" ...
I0805 18:57:04.067810    9414 apply_list.go:67] Installing "sample-templates/django quickstart"
I0805 18:57:04.068185    9414 apply_template.go:81] Installing "openshift-web-console-operator"
I0805 18:57:04.068356    9414 apply_list.go:67] Installing "centos-imagestreams"
I0805 18:57:04.068805    9414 apply_list.go:67] Installing "sample-templates/dancer quickstart"
I0805 18:57:04.068925    9414 apply_list.go:67] Installing "sample-templates/nodejs quickstart"
I0805 18:57:04.069022    9414 apply_list.go:67] Installing "sample-templates/jenkins pipeline ephemeral"
I0805 18:57:04.069153    9414 apply_list.go:67] Installing "sample-templates/mysql"
I0805 18:57:04.069257    9414 apply_list.go:67] Installing "sample-templates/postgresql"
I0805 18:57:04.069361    9414 apply_list.go:67] Installing "sample-templates/cakephp quickstart"
I0805 18:57:04.069463    9414 apply_list.go:67] Installing "sample-templates/rails quickstart"
I0805 18:57:04.069559    9414 apply_list.go:67] Installing "sample-templates/sample pipeline"
I0805 18:57:04.069667    9414 apply_list.go:67] Installing "sample-templates/mongodb"
I0805 18:57:04.069761    9414 apply_list.go:67] Installing "sample-templates/mariadb"
I0805 18:57:22.033276    9414 interface.go:41] Finished installing "sample-templates/dancer quickstart" "sample-templates/nodejs quickstart" "sample-templates/jenkins pipeline ephemeral" "sample-templates/mysql" "sample-templates/postgresql" "sample-templates/cakephp quickstart" "sample-templates/rails quickstart" "sample-templates/sample pipeline" "sample-templates/mongodb" "sample-templates/mariadb" "sample-templates/django quickstart"
I0805 18:58:25.122639    9414 interface.go:41] Finished installing "openshift-router" "sample-templates" "openshift-web-console-operator" "centos-imagestreams" "openshift-image-registry" "persistent-volumes"
Login to server ...
Creating initial project "myproject" ...
Server Information ...
OpenShift server started.

The server is accessible via web console at:
    https://10.0.8.11:8443

You are logged in as:
    User:     developer
    Password: <any value>

To login as administrator:
    oc login -u system:admin

[root@huzhi-openshift openshift-cluster]# 



[root@huzhi-openshift openshift-cluster]# docker images
REPOSITORY                                     TAG                 IMAGE ID            CREATED             SIZE
openshift/origin-node                          v3.11               d6927fc5ba5a        3 days ago          1.17GB
openshift/origin-control-plane                 v3.11               03084b1fc8ee        3 days ago          829MB
openshift/origin-haproxy-router                v3.11               b8d699e7ec3b        3 days ago          410MB
openshift/origin-deployer                      v3.11               cda3de3ce150        3 days ago          384MB
openshift/origin-cli                           v3.11               cb2578263b76        3 days ago          384MB
openshift/origin-hypershift                    v3.11               13c28db44b13        3 days ago          549MB
openshift/origin-hyperkube                     v3.11               b43ef554bffc        3 days ago          509MB
openshift/origin-pod                           v3.11               cb333986045d        3 days ago          262MB
openshift/origin-docker-registry               v3.11               9dffb2abf1dd        6 months ago        310MB
openshift/origin-web-console                   v3.11               be30b6cce5fa        9 months ago        339MB
openshift/origin-service-serving-cert-signer   v3.11               47dadf9d43b6        9 months ago        276MB
[root@huzhi-openshift openshift-cluster]# 




openshift/origin-node
openshift/origin-control-plane
openshift/origin-haproxy-router
openshift/origin-deployer
openshift/origin-cli
openshift/origin-hypershift
openshift/origin-hyperkube
openshift/origin-pod
openshift/origin-docker-registry
openshift/origin-web-console
openshift/origin-service-serving-cert-signer





[root@huzhi-openshift openshift-cluster]# docker ps -a
CONTAINER ID        IMAGE                                          COMMAND                  CREATED             STATUS                     PORTS               NAMES

e8bafcfb9a73        openshift/origin-docker-registry               "/bin/sh -c '/usr/bi…"   2 minutes ago       Up 2 minutes                                   k8s_registry_docker-registry-1-7bg8g_default_da2ebc38-b76f-11e9-a716-0050569bdb5d_0

be2cf2531e5c        openshift/origin-haproxy-router                "/usr/bin/openshift-…"   4 minutes ago       Up 4 minutes                                   k8s_router_router-1-8dlnq_default_d8526c77-b76f-11e9-a716-0050569bdb5d_0

fc3ff5b2508b        be30b6cce5fa                                   "/usr/bin/origin-web…"   4 minutes ago       Up 4 minutes                                   k8s_webconsole_webconsole-85d8d4f95f-fcnqw_openshift-web-console_f6e48959-b76f-11e9-a716-0050569bdb5d_0

5dc1486bd271        openshift/origin-pod:v3.11                     "/usr/bin/pod"           4 minutes ago       Up 4 minutes                                   k8s_POD_webconsole-85d8d4f95f-fcnqw_openshift-web-console_f6e48959-b76f-11e9-a716-0050569bdb5d_0

8311964baf24        openshift/origin-pod:v3.11                     "/usr/bin/pod"           5 minutes ago       Up 5 minutes                                   k8s_POD_docker-registry-1-7bg8g_default_da2ebc38-b76f-11e9-a716-0050569bdb5d_0

dccede8f33bf        openshift/origin-pod:v3.11                     "/usr/bin/pod"           5 minutes ago       Up 5 minutes                                   k8s_POD_router-1-8dlnq_default_d8526c77-b76f-11e9-a716-0050569bdb5d_0

978c2524b8d6        openshift/origin-hypershift                    "hypershift experime…"   5 minutes ago       Up 5 minutes                                   k8s_operator_openshift-web-console-operator-664b974ff5-rrbtw_openshift-core-operators_cd5f27c5-b76f-11e9-a716-0050569bdb5d_0

f6a730437be7        openshift/origin-pod:v3.11                     "/usr/bin/pod"           5 minutes ago       Up 5 minutes                                   k8s_POD_openshift-web-console-operator-664b974ff5-rrbtw_openshift-core-operators_cd5f27c5-b76f-11e9-a716-0050569bdb5d_0

a302bcfe4b5c        openshift/origin-hypershift                    "hypershift openshif…"   5 minutes ago       Up 5 minutes                                   k8s_c_openshift-controller-manager-twt2s_openshift-controller-manager_c2c9ba9b-b76f-11e9-a716-0050569bdb5d_0

527a17f3200d        cb2578263b76                                   "/bin/bash -c '#/bin…"   5 minutes ago       Exited (0) 4 minutes ago                       k8s_setup-persistent-volumes_persistent-volume-setup-9ztnd_default_c2ad8182-b76f-11e9-a716-0050569bdb5d_0

0cddb73da47c        openshift/origin-pod:v3.11                     "/usr/bin/pod"           5 minutes ago       Up 5 minutes                                   k8s_POD_openshift-controller-manager-twt2s_openshift-controller-manager_c2c9ba9b-b76f-11e9-a716-0050569bdb5d_0

f66341040ac1        openshift/origin-pod:v3.11                     "/usr/bin/pod"           5 minutes ago       Exited (0) 4 minutes ago                       k8s_POD_persistent-volume-setup-9ztnd_default_c2ad8182-b76f-11e9-a716-0050569bdb5d_0

fcc25d56c685        openshift/origin-hypershift                    "hypershift openshif…"   6 minutes ago       Up 6 minutes                                   k8s_apiserver_openshift-apiserver-xf46v_openshift-apiserver_983df5c6-b76f-11e9-a716-0050569bdb5d_0

31f3879a1a16        openshift/origin-control-plane                 "openshift start net…"   6 minutes ago       Up 6 minutes                                   k8s_kube-dns_kube-dns-wmd4t_kube-dns_9839fd70-b76f-11e9-a716-0050569bdb5d_0

ced0f86f9a76        openshift/origin-pod:v3.11                     "/usr/bin/pod"           6 minutes ago       Up 6 minutes                                   k8s_POD_openshift-apiserver-xf46v_openshift-apiserver_983df5c6-b76f-11e9-a716-0050569bdb5d_0

6868036f3167        47dadf9d43b6                                   "service-serving-cer…"   6 minutes ago       Up 6 minutes                                   k8s_apiservice-cabundle-injector-controller_apiservice-cabundle-injector-8ffbbb6dc-8d4bx_openshift-service-cert-signer_9f30d8f9-b76f-11e9-a716-0050569bdb5d_0

1c46788e3056        openshift/origin-pod:v3.11                     "/usr/bin/pod"           6 minutes ago       Up 6 minutes                                   k8s_POD_apiservice-cabundle-injector-8ffbbb6dc-8d4bx_openshift-service-cert-signer_9f30d8f9-b76f-11e9-a716-0050569bdb5d_0

6294fb769e8f        47dadf9d43b6                                   "service-serving-cer…"   6 minutes ago       Up 6 minutes                                   k8s_service-serving-cert-signer-controller_service-serving-cert-signer-668c45d5f-22nm9_openshift-service-cert-signer_9de25486-b76f-11e9-a716-0050569bdb5d_0

d9fdaf77ec3a        openshift/origin-pod:v3.11                     "/usr/bin/pod"           6 minutes ago       Up 6 minutes                                   k8s_POD_service-serving-cert-signer-668c45d5f-22nm9_openshift-service-cert-signer_9de25486-b76f-11e9-a716-0050569bdb5d_0

673d1904f190        openshift/origin-service-serving-cert-signer   "service-serving-cer…"   6 minutes ago       Up 6 minutes                                   k8s_operator_openshift-service-cert-signer-operator-6d477f986b-kgkm4_openshift-core-operators_984296ba-b76f-11e9-a716-0050569bdb5d_0

596ee6af36a1        openshift/origin-control-plane                 "openshift start net…"   6 minutes ago       Up 6 minutes                                   k8s_kube-proxy_kube-proxy-7v5bl_kube-proxy_98390322-b76f-11e9-a716-0050569bdb5d_0

58c46d746678        openshift/origin-pod:v3.11                     "/usr/bin/pod"           6 minutes ago       Up 6 minutes                                   k8s_POD_kube-dns-wmd4t_kube-dns_9839fd70-b76f-11e9-a716-0050569bdb5d_0

713c86569f68        openshift/origin-pod:v3.11                     "/usr/bin/pod"           6 minutes ago       Up 6 minutes                                   k8s_POD_openshift-service-cert-signer-operator-6d477f986b-kgkm4_openshift-core-operators_984296ba-b76f-11e9-a716-0050569bdb5d_0

e25470e070d9        openshift/origin-pod:v3.11                     "/usr/bin/pod"           6 minutes ago       Up 6 minutes                                   k8s_POD_kube-proxy-7v5bl_kube-proxy_98390322-b76f-11e9-a716-0050569bdb5d_0

bcbdd36cb1d8        openshift/origin-hyperkube                     "hyperkube kube-sche…"   7 minutes ago       Up 7 minutes                                   k8s_scheduler_kube-scheduler-localhost_kube-system_8e265dc3e75a5053144d89852d80f23b_0

354b3a9a53ae        openshift/origin-hyperkube                     "hyperkube kube-cont…"   7 minutes ago       Up 7 minutes                                   k8s_controllers_kube-controller-manager-localhost_kube-system_798ac9bea17b88f583045bdacb34d44c_0

bca595e2ebda        openshift/origin-control-plane                 "/bin/bash -c '#!/bi…"   7 minutes ago       Up 7 minutes                                   k8s_etcd_master-etcd-localhost_kube-system_dc3995e07d9f0b73a2910ef71e8dd6bb_0

0565b50022d0        openshift/origin-hypershift                    "/bin/bash -c '#!/bi…"   8 minutes ago       Up 7 minutes                                   k8s_api_master-api-localhost_kube-system_a438b2aa25c91c9137c9871deb8e9388_0

fd1145fc8c88        openshift/origin-pod:v3.11                     "/usr/bin/pod"           8 minutes ago       Up 8 minutes                                   k8s_POD_kube-scheduler-localhost_kube-system_8e265dc3e75a5053144d89852d80f23b_0

346a4b1eeb51        openshift/origin-pod:v3.11                     "/usr/bin/pod"           8 minutes ago       Up 8 minutes                                   k8s_POD_kube-controller-manager-localhost_kube-system_798ac9bea17b88f583045bdacb34d44c_0

c4712a0fcd50        openshift/origin-pod:v3.11                     "/usr/bin/pod"           8 minutes ago       Up 8 minutes                                   k8s_POD_master-etcd-localhost_kube-system_dc3995e07d9f0b73a2910ef71e8dd6bb_0

3c3580f5ece8        openshift/origin-pod:v3.11                     "/usr/bin/pod"           8 minutes ago       Up 8 minutes                                   k8s_POD_master-api-localhost_kube-system_a438b2aa25c91c9137c9871deb8e9388_0

85695c6c3242        openshift/origin-node:v3.11                    "hyperkube kubelet -…"   8 minutes ago       Up 8 minutes                                   origin

[root@huzhi-openshift openshift-cluster]# 



```





https://medium.com/@adilsonbna/installing-a-highly-available-openshift-origin-cluster-f3493cbdb644



http://uncontained.io/articles/openshift-ha-installation/



https://subscription.packtpub.com/book/application_development/9781788992329/4/ch04lvl1sec49/openshift-architecture









