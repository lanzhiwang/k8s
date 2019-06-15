# DNS 相关插件

* kube-dns

* CoreDNS

使用 kubectl 命令查看集群信息，看集群安装了哪些插件


# Configure DNS for a Cluster

[参考](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/)

## Kubernetes DNS example

This is a toy example demonstrating how to use Kubernetes DNS.  这是一个演示如何使用Kubernetes DNS的玩具示例。

### Step Zero: Prerequisites

This example assumes that you have forked the repository and turned up a Kubernetes cluster. Make sure DNS is enabled in your setup, see DNS doc.  此示例假定您已经分叉了存储库并打开了Kubernetes集群。 确保在您的设置中启用了DNS，请参阅DNS文档。






# Customizing DNS Service

[参考](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/)

This page explains how to configure your DNS Pod and customize the DNS resolution process. In Kubernetes version 1.11 and later, CoreDNS is at GA and is installed by default with kubeadm. See CoreDNS ConfigMap options and Using CoreDNS for Service Discovery.  此页面说明如何配置DNS Pod并自定义DNS解析过程。 在Kubernetes 1.11及更高版本中，CoreDNS位于GA，默认情况下使用kubeadm安装。 请参阅CoreDNS ConfigMap选项和使用CoreDNS进行服务发现。

* [Before you begin]()
* [Introduction]()
* [CoreDNS]()
* [Kube-dns]()
* [CoreDNS configuration equivalent to kube-dns]()
* [Migration to CoreDNS]()
* [What’s next]()

## Before you begin

* You need to have a Kubernetes cluster, and the kubectl command-line tool must be configured to communicate with your cluster. If you do not already have a cluster, you can create one by using Minikube, or you can use one of these Kubernetes playgrounds:

* [Katacoda](https://www.katacoda.com/courses/kubernetes/playground)

* [Play with Kubernetes](http://labs.play-with-k8s.com/)

* To check the version, enter **kubectl version**.

* Kubernetes version 1.6 or later. To work with CoreDNS, version 1.9 or later.

* The appropriate add-on: kube-dns or CoreDNS. To install with kubeadm, see the kubeadm reference documentation.

## Introduction

DNS is a built-in Kubernetes service launched automatically using the addon manager cluster add-on.  DNS是使用插件管理器集群附加组件自动启动的内置Kubernetes服务。

As of Kubernetes v1.12, CoreDNS is the recommended DNS Server, replacing kube-dns. However, kube-dns may still be installed by default with certain Kubernetes installer tools. Refer to the documentation provided by your installer to know which DNS server is installed by default.  从Kubernetes v1.12开始，CoreDNS是推荐的DNS服务器，取代了kube-dns。 但是，默认情况下仍可以使用某些Kubernetes安装程序工具安装kube-dns。 请参阅安装程序提供的文档，以了解默认安装的DNS服务器。

The CoreDNS Deployment is exposed as a Kubernetes Service with a static IP. Both the CoreDNS and kube-dns Service are named **kube-dns** in the **metadata.name** field. This is done so that there is greater interoperability with workloads that relied on the legacy **kube-dns** Service name to resolve addresses internal to the cluster. It abstracts away the implementation detail of which DNS provider is running behind that common endpoint. The kubelet passes DNS to each container with the **--cluster-dns=<dns-service-ip>** flag.  CoreDNS部署作为具有静态IP的Kubernetes服务公开。 CoreDNS和kube-dns服务都在metadata.name字段中命名为kube-dns。 这样做是为了与依赖于传统kube-dns服务名称的工作负载具有更强的互操作性，以解析集群内部的地址。 它抽象出了DNS提供程序在该公共端点后面运行的实现细节。 kubelet使用--cluster-dns = <dns-service-ip>标志将DNS传递给每个容器

DNS names also need domains. You configure the local domain in the kubelet with the flag **--cluster-domain=<default-local-domain>**.









# Using CoreDNS for Service Discovery





