# Creating a Kubernetes Master

Note:
This guide was validated on Kubernetes v1.14. Because of the volatility of Kubernetes from version to version, this section may make assumptions that do not hold true for all future versions. Official documentation for initializing Kubernetes masters using kubeadm can be found here. Simply enable mixed-OS scheduling section on top of that.  本指南在Kubernetes v1.14上得到验证。 由于Kubernetes从版本到版本的波动性，本节可能会做出对所有未来版本都不适用的假设。 可在此处找到使用kubeadm初始化Kubernetes主人的官方文档。 简单地启用混合OS调度部分。

Note:
A recently-updated Linux machine is required to follow along; Kubernetes master resources like kube-dns, kube-scheduler, and kube-apiserver have not been ported to Windows yet.  最近更新的Linux机器需要遵循; Kubernetes主要资源如kube-dns，kube-scheduler和kube-apiserver尚未移植到Windows。

Tip:
The Linux instructions are tailored towards Ubuntu 16.04. Other Linux distributions certified to run Kubernetes should also offer equivalent commands that you can substitute. They will also interoperate successfully with Windows.  Linux指令是针对Ubuntu 16.04量身定制的。 其他经过认证可运行Kubernetes的Linux发行版也应提供可替代的等效命令。 他们还将与Windows成功互操作。

## Initialization using kubeadm

Unless explicitly specified otherwise, run any commands below as root.  除非另有明确说明，否则以root身份运行以下任何命令。

First, get into an elevated root shell:

```bash
sudo –s
```

Make sure your machine is up to date:

```bash
apt-get update -y && apt-get upgrade -y
```

### Install Docker

To be able to use containers, you need a container engine, such as Docker. To get the most recent version, you can use these instructions for Docker installation. You can verify that docker is installed correctly by running a `hello-world` container:

```bash
docker run hello-world
```

### Install kubeadm

Download kubeadm binaries for your Linux distribution and initialize your cluster.

Important:
Depending on your Linux distribution, you may need to replace `kubernetes-xenial` below with the correct codename.

```bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update && apt-get install -y kubelet kubeadm kubectl
```

### Prepare the master node

Kubernetes on Linux requires swap space to be turned off:

```bash
nano /etc/fstab  # (remove a line referencing 'swap.img' , if it exists)
swapoff -a
```

### Initialize master

Note down your cluster subnet (e.g. 10.244.0.0/16) and service subnet (e.g. 10.96.0.0/12) and initialize your master using kubeadm:

```bash
kubeadm init --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12
```

This may take a few minutes. Once completed, you should see a screen like this confirming your master has been initialized:

![](../images/kubeadm-init.png)

Tip:
You should take note of this kubeadm join command. Shoud the kubeadm token expire, you can use `kubeadm token create --print-join-command` to create a new token.

Tip:
Tip

If you have a desired Kubernetes version you'd like to use, you can pass the `--kubernetes-version` flag to kubeadm.

We are not done yet. To use kubectl as a regular user, run the following in an unelevated, non-root user shell

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Now you can use kubectl to edit or view information about your cluster.

### Enable mixed-OS scheduling

By default, certain Kubernetes resources are written in such a way that they're scheduled on all nodes. However, in a multi-OS environment we don't want Linux resources to interfere or be double-scheduled onto Windows nodes, and vice-versa. For this reason, we need to apply NodeSelector labels.  默认情况下，某些Kubernetes资源的编写方式是在所有节点上进行调度。 但是，在多操作系统环境中，我们不希望Linux资源干扰或双重调度到Windows节点上，反之亦然。 因此，我们需要应用NodeSelector标签。

In this regard, we are going to patch the linux kube-proxy DaemonSet to target Linux only.  在这方面，我们将修改linux kube-proxy DaemonSet以仅针对Linux。

First, let's create a directory to store .yaml manifest files:

```bash
mkdir -p kube/yaml && cd kube/yaml
```

Confirm that the update strategy of kube-proxy DaemonSet is set to RollingUpdate:  确认kube-proxy DaemonSet的更新策略设置为RollingUpdate：

```bash
kubectl get ds/kube-proxy -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}' --namespace=kube-system
```

Next, patch the DaemonSet by downloading this nodeSelector and apply it to only target Linux:  接下来，通过下载此nodeSelector来修补DaemonSet并将其应用于仅针对目标Linux：

```bash
wget https://raw.githubusercontent.com/Microsoft/SDN/master/Kubernetes/flannel/l2bridge/manifests/node-selector-patch.yml
cat node-selector-patch.yml
spec:
  template:
    spec:
      nodeSelector:
        beta.kubernetes.io/os: linux

kubectl patch ds/kube-proxy --patch "$(cat node-selector-patch.yml)" -n=kube-system
```

Once successful, you should see "Node Selectors" of `kube-proxy` and any other DaemonSets set to `beta.kubernetes.io/os=linux`

```bash
kubectl get ds -n kube-system
```

![](../images/kube-proxy-ds.png)

### Collect cluster information 收集群集信息

To successfully join future nodes to the master, you should keep track of the following information:  要成功将未来节点加入主节点，您应该跟踪以下信息：

1. kubeadm join command from output
* Example: `kubeadm join <Master_IP>:6443 --token <some_token> --discovery-token-ca-cert-hash <some_hash>`

2. Cluster subnet defined during kubeadm init
* Example: `10.244.0.0/16`

3. Service subnet defined during kubeadm init (here)
* Example: `10.96.0.0/12`
* Can also be found using `kubectl cluster-info dump | grep -i service-cluster-ip-range`

4. Kube-dns service IP
* Example: `10.96.0.10`
* Can be found in "Cluster IP" field using `kubectl get svc/kube-dns -n kube-system`

5. Kubernetes `config` file generated after `kubeadm init` . If you followed the instructions, this can be found in the following paths:
* `/etc/kubernetes/admin.conf`
* `$HOME/.kube/config`

## Verifying the master

After a few minutes, the system should be in the following state:

* Under `kubectl get pods -n kube-system`, there will be pods for the Kubernetes master components in Running state.
* Calling `kubectl cluster-info` will show information about the Kubernetes master API server in addition to DNS addons.

Tip:
Since kubeadm does not setup networking, DNS pods may still be in ContainerCreating or Pending state. They will switch to Running state after choosing a network solution.  由于kubeadm未设置网络，因此DNS pod可能仍处于ContainerCreating或Pending状态。 选择网络解决方案后，它们将切换到运行状态。

## Next steps

In this section we covered how to setup a Kubernetes master using kubeadm. Now you are ready for step 3:
