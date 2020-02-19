# how to deploy CoreDNS in Kubernetes.

[来源](https://github.com/coredns/deployment/tree/master/kubernetes)

# Kubernetes

## Description

CoreDNS can run in place of the standard Kube-DNS in Kubernetes. Using the *kubernetes* plugin, CoreDNS will read zone data from a Kubernetes cluster. It implements the spec defined for Kubernetes DNS-Based service discovery:  CoreDNS可以代替Kubernetes中的标准Kube-DNS运行。 使用kubernetes插件，CoreDNS将从Kubernetes集群读取区域数据。 它实现了为Kubernetes基于DNS的服务发现定义的规范：

https://github.com/kubernetes/dns/blob/master/docs/specification.md

## deploy.sh and coredns.yaml.sed

`deploy.sh` is a convenience script to generate a manifest for running CoreDNS on a cluster that is currently running standard kube-dns. Using the `coredns.yaml.sed` file as a template, it creates a ConfigMap and a CoreDNS deployment, then updates the Kube-DNS service selector to use the CoreDNS deployment. By re-using the existing service, there is no disruption in servicing requests.  deploy.sh是一个便捷脚本，用于生成在当前运行标准kube-dns的集群上运行CoreDNS的清单。 使用coredns.yaml.sed文件作为模板，它创建ConfigMap和CoreDNS部署，然后更新Kube-DNS服务选择器以使用CoreDNS部署。 通过重新使用现有服务，服务请求不会中断。

By default, the deployment script also translates the existing kube-dns configuration into the equivalent CoreDNS Corefile. By providing the `-s` option, the deployment script will skip the translation of the ConfigMap from kube-dns to CoreDNS.  默认情况下，部署脚本还会将现有的kube-dns配置转换为等效的CoreDNS Corefile。 通过提供-s选项，部署脚本将跳过ConfigMap从kube-dns到CoreDNS的转换。

The script doesn't delete the kube-dns deployment or replication controller - you'll have to do that manually, after deploying CoreDNS.  该脚本不会删除kube-dns部署或复制控制器 - 在部署CoreDNS之后，您必须手动执行此操作。

You should examine the manifest carefully and make sure it is correct for your particular cluster. Depending on how you have built your cluster and the version you are running, some modifications to the manifest may be needed.  您应仔细检查清单，并确保它对您的特定群集是正确的。 根据您构建群集的方式以及正在运行的版本，可能需要对清单进行一些修改。

In the best case scenario, all that's needed to replace Kube-DNS are these commands:  在最好的情况下，替换Kube-DNS所需的全部是这些命令：

```
$ ./deploy.sh | kubectl apply -f -
$ kubectl delete --namespace=kube-system deployment kube-dns
```

**NOTE:** You will need to delete the kube-dns deployment (as above) since while CoreDNS and kube-dns are running at the same time, queries may randomly hit either one.  您将需要删除kube-dns部署（如上所述），因为当CoreDNS和kube-dns同时运行时，查询可能会随机命中一个。

For non-RBAC deployments, you'll need to edit the resulting yaml before applying it:  对于非RBAC部署，您需要在应用之前编辑生成的yaml：

1. Remove the line `serviceAccountName: coredns` from the `Deployment` section.
2. Remove the `ServiceAccount`, `ClusterRole`, and `ClusterRoleBinding` sections.

## Rollback to kube-dns

In case one wants to revert a Kubernetes cluster running CoreDNS back to kube-dns, the `rollback.sh` script generates the kube-dns manifest to install kube-dns. This uses the existing service, there is no disruption in servicing requests.  如果想要将运行CoreDNS的Kubernetes集群恢复为kube-dns，rollback.sh脚本会生成kube-dns清单以安装kube-dns。 这使用现有服务，服务请求没有中断。

The script doesn't delete the CoreDNS deployment or replication controller - you'll have to do that manually, after deploying kube-dns.  该脚本不会删除CoreDNS部署或复制控制器 - 在部署kube-dns之后，您必须手动执行此操作。

These commands will deploy kube-dns replacing CoreDNS:

```
$ ./rollback.sh | kubectl apply -f -
$ kubectl delete --namespace=kube-system deployment coredns
```

**NOTE:** You will need to delete the CoreDNS deployment (as above) since while CoreDNS and kube-dns are running at the same time, queries may randomly hit either one.  您将需要删除CoreDNS部署（如上所述），因为当CoreDNS和kube-dns同时运行时，查询可能会随机命中任何一个。

