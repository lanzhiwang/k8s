# Kubernetes on Windows

[参考](https://docs.microsoft.com/en-us/virtualization/windowscontainers/kubernetes/getting-started-kubernetes-windows)

This page serves as an overview for getting started with Kubernetes on Windows by joining Windows nodes to a Linux-based cluster. With the release of Kubernetes 1.14 on Windows Server version 1809, users can take advantage of the following features in Kubernetes on Windows:  此页面通过将Windows节点加入基于Linux的群集，作为Windows上Kubernetes入门的概述。 随着Windows Server版本1809上Kubernetes 1.14的发布，用户可以利用Windows上Kubernetes的以下功能：

* overlay networking: use Flannel in vxlan mode to configure a virtual overlay network
	* requires either Windows Server 2019 with KB4489899 installed or Windows Server vNext Insider Preview Build 18317+
	* requires Kubernetes v1.14 (or above) with `WinOverlay` feature gate enabled
	* requires Flannel v0.11.0 (or above)
* simplified network management: use Flannel in host-gateway mode for automatic route management between nodes.
* scalability improvements: enjoy faster and more reliable container start-up times thanks to deviceless vNICs for Windows Server containers.  可扩展性改进：借助适用于Windows Server容器的无设备vNIC，可以更快，更可靠地启动容器启动时间。
* Hyper-V isolation (alpha): orchestrate Hyper-V isolation with kernel-mode isolation for enhanced security. For more information, Windows container types.  Hyper-V隔离（alpha）：使用内核模式隔离协调Hyper-V隔离以增强安全性。 有关Windows容器类型的更多信息。
	* requires Kubernetes v1.10 (or above) with `HyperVContainer` feature gate enabled.
* storage plugins: use the FlexVolume storage plugin with SMB and iSCSI support for Windows containers.

## Prerequisites

### Plan IP addressing for your cluster

As Kubernetes clusters introduce new subnets for pods and services, it is important to ensure that none of them collide with any other existing networks in your environment. Here are all the address spaces that need to be freed up in order to deploy Kubernetes successfully:  由于Kubernetes集群为pod和服务引入了新的子网，因此确保它们都不会与环境中的任何其他现有网络发生冲突非常重要。 以下是为了成功部署Kubernetes而需要释放的所有地址空间：

| Subnet / Address range | Description | Default Value | Actual Value |
| ---- | ---- | ---- | ---- |
| Service Subnet | A non-routable, purely virtual subnet that is used by pods to uniformally access services without caring about the network topology. It is translated to/from routable address space by `kube-proxy` running on the nodes.  一个不可路由的纯虚拟子网，由pod用于统一访问服务，而无需关心网络拓扑。 它通过在节点上运行的kube-proxy转换为可路由地址空间/从可路由地址空间转换。| "10.96.0.0/12" |      |
| Cluster Subnet | This is a global subnet that is used by all pods in the cluster. Each nodes is assigned a smaller /24 subnet from this for their pods to use. It must be large enough to accommodate all pods used in your cluster. To calculate minimum subnet size: (number of nodes) + (number of nodes * maximum pods per node that you configure)  这是群集中所有pod使用的全局子网。 为每个节点分配一个较小的/ 24子网，供其pod使用。 它必须足够大，以容纳群集中使用的所有pod。Example for a 5 node cluster for 100 pods per node: (5) + (5 * 100) = 505. | "10.244.0.0/16" |      |
| Kubernetes DNS Service IP | IP address of "kube-dns" service that will be used for DNS resolution & cluster service discovery. | "10.96.0.10" |      |

Note:
There is another Docker network (NAT) that gets created by default when you install Docker. It is not needed to operate Kubernetes on Windows as we assign IPs from the cluster subnet instead.  安装Docker时，默认情况下会创建另一个Docker网络（NAT）。 我们不需要在Windows上运行Kubernetes，因为我们从群集子网中分配IP。

## Next steps

In this section, we talked about important pre-requisites & assumptions needed to deploy Kubernetes on Windows successfully today. Continue to learn how to setup a Kubernetes master:  在本节中，我们讨论了今天在Windows上成功部署Kubernetes所需的重要先决条件和假设。 继续学习如何设置Kubernetes master：

