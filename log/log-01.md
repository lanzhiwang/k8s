# Logging Architecture

Application and systems logs can help you understand what is happening inside your cluster. The logs are particularly useful for debugging problems and monitoring cluster activity. Most modern applications have some kind of logging mechanism; as such, most container engines are likewise designed to support some kind of logging. The easiest and most embraced logging method for containerized applications is to write to the standard output and standard error streams.  应用程序和系统日志可以帮助您了解群集内部发生的情况。 日志对于调试问题和监视集群活动特别有用。 大多数现代应用都有某种记录机制; 因此，大多数集装箱发动机同样设计用于支持某种伐木。 容器化应用程序最简单，最受欢迎的日志记录方法是写入标准输出和标准错误流。

However, the native functionality provided by a container engine or runtime is usually not enough for a complete logging solution. For example, if a container crashes, a pod is evicted, or a node dies, you’ll usually still want to access your application’s logs. As such, logs should have a separate storage and lifecycle independent of nodes, pods, or containers. This concept is called cluster-level-logging. Cluster-level logging requires a separate backend to store, analyze, and query logs. Kubernetes provides no native storage solution for log data, but you can integrate many existing logging solutions into your Kubernetes cluster.  但是，容器引擎或运行时提供的本机功能通常不足以构建完整的日志记录解决方案。 例如，如果容器崩溃，pod被驱逐，或节点死亡，您通常仍然希望访问应用程序的日志。 因此，日志应具有独立于节点，pod或容器的单独存储和生命周期。 这个概念称为集群级日志记录。 群集级日志记录需要单独的后端来存储，分析和查询日志。 Kubernetes不提供日志数据的本机存储解决方案，但您可以将许多现有的日志记录解决方案集成到Kubernetes集群中。

* [Basic logging in Kubernetes]()
* [Logging at the node level]()
* [Cluster-level logging architectures]()

Cluster-level logging architectures are described in assumption that a logging backend is present inside or outside of your cluster. If you’re not interested in having cluster-level logging, you might still find the description of how logs are stored and handled on the node to be useful.  假设集群内部或外部存在日志记录后端，将描述集群级日志记录体系结构。 如果您对集群级日志记录不感兴趣，您可能仍会在节点上找到有关如何存储和处理日志的说明，以便有用。

## Basic logging in Kubernetes

In this section, you can see an example of basic logging in Kubernetes that outputs data to the standard output stream. This demonstration uses a pod specification with a container that writes some text to standard output once per second.  在本节中，您可以看到Kubernetes中基本日志记录的示例，该示例将数据输出到标准输出流。 此演示使用pod规范和容器，该容器每秒将一些文本写入标准输出一次。

```
apiVersion: v1
kind: Pod
metadata:
  name: counter
spec:
  containers:
  - name: count
    image: busybox
    args: [/bin/sh, -c,
            'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done']

```

To run this pod, use the following command:

```bash
kubectl apply -f https://k8s.io/examples/debug/counter-pod.yaml
pod/counter created

```

To fetch the logs, use the `kubectl logs` command, as follows:

```
kubectl logs counter
0: Mon Jan  1 00:00:00 UTC 2001
1: Mon Jan  1 00:00:01 UTC 2001
2: Mon Jan  1 00:00:02 UTC 2001
...

```

You can use kubectl logs to retrieve logs from a previous instantiation of a container with --previous flag, in case the container has crashed. If your pod has multiple containers, you should specify which container’s logs you want to access by appending a container name to the command. See the kubectl logs documentation for more details.  如果容器已崩溃，您可以使用kubectl日志从带有--previous标志的容器的先前实例化中检索日志。 如果您的pod有多个容器，则应通过在命令中附加容器名称来指定要访问的容器的日志。 有关更多详细信息，请参阅kubectl logs文档。

## Logging at the node level



## Cluster-level logging architectures


