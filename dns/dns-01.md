# An Introduction to the Kubernetes DNS Service

[来源](https://www.digitalocean.com/community/tutorials/an-introduction-to-the-kubernetes-dns-service)

### Introduction

The Domain Name System (DNS) is a system for associating various types of information – such as IP addresses – with easy-to-remember names. By default most Kubernetes clusters automatically configure an internal DNS service to provide a lightweight mechanism for service discovery. Built-in service discovery makes it easier for applications to find and communicate with each other on Kubernetes clusters, even when pods and services are being created, deleted, and shifted between nodes.  域名系统（DNS）是一种用于将各种类型的信息（例如IP地址）与易于记忆的名称相关联的系统。 默认情况下，大多数Kubernetes群集会自动配置内部DNS服务，以便为服务发现提供轻量级机制。 内置的服务发现使应用程序更容易在Kubernetes集群上相互查找和通信，即使在节点之间创建，删除和移动pod和服务时也是如此。

The implementation details of the Kubernetes DNS service have changed in recent versions of Kubernetes. In this article we will take a look at both the **kube-dns** and **CoreDNS** versions of the Kubernetes DNS service. We will review how they operate and the DNS records that Kubernetes generates.  最近版本的Kubernetes中Kubernetes DNS服务的实现细节已经改变。 在本文中，我们将介绍Kubernetes DNS服务的kube-dns和CoreDNS版本。 我们将审查它们的运作方式以及Kubernetes生成的DNS记录。

To gain a more thorough understanding of DNS before you begin, please read [*An Introduction to DNS Terminology, Components, and Concepts*](https://www.digitalocean.com/community/tutorials/an-introduction-to-dns-terminology-components-and-concepts). For any Kubernetes topics you may be unfamiliar with, you could read [*An Introduction to Kubernetes*](https://www.digitalocean.com/community/tutorials/an-introduction-to-kubernetes).  要在开始之前更全面地了解DNS，请阅读“DNS术语，组件和概念简介”。 对于您可能不熟悉的任何Kubernetes主题，您可以阅读Kubernetes简介。



## What Does the Kubernetes DNS Service Provide?

Before Kubernetes version 1.11, the Kubernetes DNS service was based on **kube-dns**. Version 1.11 introduced **CoreDNS** to address some security and stability concerns with kube-dns.  在Kubernetes版本1.11之前，Kubernetes DNS服务基于kube-dns。 1.11版引入了CoreDNS来解决kube-dns的一些安全性和稳定性问题。

Regardless of the software handling the actual DNS records, both implementations work in a similar manner:  无论处理实际DNS记录的软件如何，两种实现都以类似的方式工作：

- A service named `kube-dns` and one or more pods are created.

- The `kube-dns` service listens for **service** and **endpoint** events from the Kubernetes API and updates its DNS records as needed. These events are triggered when you create, update or delete Kubernetes services and their associated pods.  kube-dns服务侦听来自Kubernetes API的服务和端点事件，并根据需要更新其DNS记录。 创建，更新或删除Kubernetes服务及其关联的pod时会触发这些事件。

- kubelet sets each new pod’s `/etc/resolv.conf` `nameserver` option to the cluster IP of the `kube-dns` service, with appropriate `search` options to allow for shorter hostnames to be used:  kubelet将每个新pod的/etc/resolv.conf名称服务器选项设置为kube-dns服务的集群IP，并使用适当的搜索选项以允许使用更短的主机名：

  ```
  # resolv.conf
  nameserver 10.32.0.10
  search namespace.svc.cluster.local svc.cluster.local cluster.local
  options ndots:5
  ```

- Applications running in containers can then resolve hostnames such as `example-service.namespace` into the correct cluster IP addresses.  然后，在容器中运行的应用程序可以将主机名（例如example-service.namespace）解析为正确的群集IP地址。

### Example Kubernetes DNS Records

The full DNS `A` record of a Kubernetes service will look like the following example:

```
service.namespace.svc.cluster.local
```

A pod would have a record in this format, reflecting the actual IP address of the pod:  一个pod会有这种格式的记录，反映了pod的实际IP地址：

```
10.32.0.125.namespace.pod.cluster.local
```

Additionally, `SRV` records are created for a Kubernetes service’s named ports:

```
_port-name._protocol.service.namespace.svc.cluster.local
```

The result of all this is a built-in, DNS-based service discovery mechanism, where your application or microservice can target a simple and consistent hostname to access other services or pods on the cluster.  所有这些的结果是一个内置的，基于DNS的服务发现机制，您的应用程序或微服务可以在其中定位一个简单一致的主机名来访问群集上的其他服务或pod。

### Search Domains and Resolving Shorter Hostnames

Because of the search domain suffixes listed in the `resolv.conf` file, you often won’t need to use the full hostname to contact another service. If you’re addressing a service in the same namespace, you can use just the service name to contact it:  由于resolv.conf文件中列出的搜索域后缀，您通常不需要使用完整主机名来联系其他服务。 如果要在同一名称空间中寻址服务，则只需使用服务名称即可联系它：

```
other-service
```

If the service is in a different namespace, add it to the query:

```
other-service.other-namespace
```

If you’re targeting a pod, you’ll need to use at least the following:

```
pod-ip.other-namespace.pod
```

As we saw in the default `resolv.conf` file, only `.svc` suffixes are automatically completed, so make sure you specify everything up to `.pod`.  正如我们在默认的resolv.conf文件中看到的那样，只有.svc后缀会自动完成，因此请确保指定.pod之前的所有内容。

Now that we know the practical uses of the Kubernetes DNS service, let’s run through some details on the two different implementations.  现在我们已经了解了Kubernetes DNS服务的实际用途，让我们来看看两个不同实现的一些细节。



## Kubernetes DNS Implementation Details

As noted in the previous section, Kubernetes version 1.11 introduced new software to handle the `kube-dns` service. The motivation for the change was to increase the performance and security of the service. Let’s take a look at the original `kube-dns` implementation first.  如前一节所述，Kubernetes版本1.11引入了用于处理“ kube-dns”服务的新软件。 进行更改的动机是提高服务的性能和安全性。 首先让我们看一下原始的“ kube-dns”实现。

### kube-dns

The `kube-dns` service prior to Kubernetes 1.11 is made up of three containers running in a `kube-dns` pod in the `kube-system` namespace. The three containers are:  Kubernetes 1.11之前的kube-dns服务由在kube-system命名空间中的kube-dns pod中运行的三个容器组成。 这三个容器是：

- **kube-dns:** a container that runs [SkyDNS](https://github.com/skynetservices/skydns), which performs DNS query resolution
- **dnsmasq:** a popular lightweight DNS resolver and cache that caches the responses from SkyDNS
- **sidecar:** a sidecar container that handles metrics reporting and responds to health checks for the service

Security vulnerabilities in Dnsmasq, and scaling performance issues with SkyDNS led to the creation of a replacement system, CoreDNS.  Dnsmasq中的安全漏洞以及SkyDNS的扩展性能问题导致创建了替换系统CoreDNS。

### CoreDNS

As of Kubernetes 1.11 a new Kubernetes DNS service, **CoreDNS** has been promoted to General Availability. This means that it’s ready for production use and will be the default cluster DNS service for many installation tools and managed Kubernetes providers.  从Kubernetes 1.11开始，新的Kubernetes DNS服务，CoreDNS已升级为通用可用性。 这意味着它已准备好用于生产，并且将成为许多安装工具和托管Kubernetes提供程序的默认群集DNS服务。

CoreDNS is a single process, written in Go, that covers all of the functionality of the previous system. A single container resolves and caches DNS queries, responds to health checks, and provides metrics.  CoreDNS是一个用Go编写的单一过程，涵盖了先前系统的所有功能。 单个容器可解析和缓存DNS查询，响应运行状况检查并提供指标。

In addition to addressing performance- and security-related issues, CoreDNS fixes some other minor bugs and adds some new features:  除了解决与性能和安全相关的问题之外，CoreDNS还修复了一些其他小错误并添加了一些新功能：

- Some issues with incompatibilities between using stubDomains and external services have been fixed  修复了使用stubDomains和外部服务之间不兼容的一些问题
- CoreDNS can enhance DNS-based round-robin load balancing by randomizing the order in which it returns certain records  CoreDNS可以通过随机化返回某些记录的顺序来增强基于DNS的循环负载平衡
- A feature called `autopath` can improve DNS response times when resolving external hostnames, by being smarter about iterating through each of the search domain suffixes listed in `resolv.conf`  一个名为autopath的功能可以在解析外部主机名时改善DNS响应时间，通过更好地迭代resolv.conf中列出的每个搜索域后缀
- With kube-dns `10.32.0.125.namespace.pod.cluster.local` would always resolve to `10.32.0.125`, even if the pod doesn’t actually exist. CoreDNS has a “pods verified” mode that will only resolve successfully if a pod exists with the right IP and in the right namespace.  使用kube-dns 10.32.0.125.namespace.pod.cluster.local将始终解析为10.32.0.125，即使pod实际上不存在。 CoreDNS具有“已验证的pod”模式，只有当存在具有正确IP且位于右侧命名空间的pod时，才会成功解析。

For more information on CoreDNS and how it differs from kube-dns, you can read [the Kubernetes CoreDNS GA announcement](https://kubernetes.io/blog/2018/07/10/coredns-ga-for-kubernetes-cluster-dns/).



## Additional Configuration Options

Kubernetes operators often want to customize how their pods and containers resolve certain custom domains, or need to adjust the upstream nameservers or search domain suffixes configured in `resolv.conf`. You can do this with the `dnsConfig` option of your pod’s spec:  Kubernetes运营商通常希望自定义其pod和容器如何解析某些自定义域，或者需要调整上游名称服务器或搜索resolv.conf中配置的域后缀。 您可以使用pod规范的dnsConfig选项执行此操作：

example_pod.yaml

```
apiVersion: v1
kind: Pod
metadata:
  namespace: example
  name: custom-dns
spec:
  containers:
    - name: example
      image: nginx
  dnsPolicy: "None"
  dnsConfig:
    nameservers:
      - 203.0.113.44
    searches:
      - custom.dns.local
```

Updating this config will rewrite a pod’s `resolv.conf` to enable the changes. The configuration maps directly to the standard `resolv.conf` options, so the above config would create a file with `nameserver 203.0.113.44` and `search custom.dns.local` lines.  更新此配置将重写pod的resolv.conf以启用更改。 配置直接映射到标准的resolv.conf选项，因此上面的配置将创建一个名为serverserver 203.0.113.44的文件并搜索custom.dns.local行。



## Conclusion

In this article we covered the basics of what the Kubernetes DNS service provides to developers, showed some example DNS records for services and pods, discussed how the system is implemented on different Kubernetes versions, and highlighted some additional configuration options available to customize how your pods resolve DNS queries.  在本文中，我们介绍了Kubernetes DNS服务为开发人员提供的基础知识，显示了服务和pod的一些示例DNS记录，讨论了如何在不同的Kubernetes版本上实现系统，并突出显示了一些可用于自定义pod的方案的其他配置选项 解析DNS查询。

For more information on the Kubernetes DNS service, please refer to [the official Kubernetes *DNS for Services and Pods* documentation](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).
