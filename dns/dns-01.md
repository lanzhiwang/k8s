# An Introduction to the Kubernetes DNS Service

[参考](https://www.digitalocean.com/community/tutorials/an-introduction-to-the-kubernetes-dns-service)

## Introduction

The Domain Name System (DNS) is a system for associating various types of information – such as IP addresses – with easy-to-remember names. By default most Kubernetes clusters automatically configure an internal DNS service to provide a lightweight mechanism for service discovery. Built-in service discovery makes it easier for applications to find and communicate with each other on Kubernetes clusters, even when pods and services are being created, deleted, and shifted between nodes.  域名系统（DNS）是一种用于将各种类型的信息（例如IP地址）与易于记忆的名称相关联的系统。 默认情况下，大多数Kubernetes群集会自动配置内部DNS服务，以便为服务发现提供轻量级机制。 内置的服务发现使应用程序更容易在Kubernetes集群上相互查找和通信，即使在节点之间创建，删除和移动pod和服务时也是如此。

The implementation details of the Kubernetes DNS service have changed in recent versions of Kubernetes. In this article we will take a look at both the **kube-dns** and **CoreDNS** versions of the Kubernetes DNS service. We will review how they operate and the DNS records that Kubernetes generates.  最近版本的Kubernetes中Kubernetes DNS服务的实现细节已经改变。 在本文中，我们将介绍Kubernetes DNS服务的kube-dns和CoreDNS版本。 我们将审查它们的运作方式以及Kubernetes生成的DNS记录。

To gain a more thorough understanding of DNS before you begin, please read An Introduction to DNS Terminology, Components, and Concepts. For any Kubernetes topics you may be unfamiliar with, you could read An Introduction to Kubernetes.  要在开始之前更全面地了解DNS，请阅读“DNS术语，组件和概念简介”。 对于您可能不熟悉的任何Kubernetes主题，您可以阅读Kubernetes简介。

## What Does the Kubernetes DNS Service Provide?

Before Kubernetes version 1.11, the Kubernetes DNS service was based on **kube-dns**. Version 1.11 introduced **CoreDNS** to address some security and stability concerns with kube-dns.  在Kubernetes版本1.11之前，Kubernetes DNS服务基于kube-dns。 1.11版引入了CoreDNS来解决kube-dns的一些安全性和稳定性问题。

Regardless of the software handling the actual DNS records, both implementations work in a similar manner:  无论处理实际DNS记录的软件如何，两种实现都以类似的方式工作：

* A service named `kube-dns` and one or more pods are created.

* The `kube-dns` service listens for **service** and **endpoint** events from the Kubernetes API and updates its DNS records as needed. These events are triggered when you create, update or delete Kubernetes services and their associated pods.  kube-dns服务侦听来自Kubernetes API的服务和端点事件，并根据需要更新其DNS记录。 创建，更新或删除Kubernetes服务及其关联的pod时会触发这些事件。






