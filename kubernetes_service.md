# kubernetes service

参考：
* https://blog.csdn.net/liukuan73/article/details/82585732
* https://blog.csdn.net/m0_37556444/article/details/84991535

根据创建 Service 的 type 类型不同，可分成4种模式：

* ClusterIP： 默认方式。根据是否生成 ClusterIP 又可分为普通 Service 和 Headless Service 两类：
	* 普通 Service：通过为 Kubernetes 的 Service 分配一个集群内部可访问的固定虚拟IP（Cluster IP），实现集群内的访问。为最常见的方式。
	* Headless Service：该服务不会分配 Cluster IP，也不通过 kube-proxy 做反向代理和负载均衡。而是通过DNS 提供稳定的网络 ID 来访问，DNS 会将 headless service 的后端直接解析为 podIP 列表。主要供 StatefulSet使用。

* NodePort：除了使用 Cluster IP 之外，还通过将 service 的 port 映射到集群内每个节点的相同一个端口，实现通过 nodeIP:nodePort 从集群外访问服务。

* LoadBalancer：和 nodePort 类似，不过除了使用一个 Cluster IP 和 nodePort 之外，还会向所使用的公有云申请一个负载均衡器(负载均衡器后端映射到各节点的nodePort)，实现从集群外通过 LB 访问服务。

* ExternalName：是 Service 的特例。此模式主要面向运行在集群外部的服务，通过它可以将外部服务映射进 k8s 集群，且具备k8s内服务的一些特征（如具备namespace等属性），来为集群内部提供服务。此模式要求 kube-dns 的版本为1.7或以上。这种模式和前三种模式（除 headless service ）最大的不同是重定向依赖的是 dns层次，而不是通过 kube-proxy。比如，在service定义中指定externalName的值"my.database.example.com"：此时 k8s 集群内的 DNS 服务会给集群内的服务名 <service-name>.<namespace>.svc.cluster.local 创建一个CNAME记录，其值为指定的"my.database.example.com"。当查询 k8s 集群内的服务 my-service.prod.svc.cluster.local时，集群的 DNS 服务将返回映射的CNAME记录"my.database.example.com"。

备注：
* 前3种模式，定义服务的时候通过 selector 指定服务对应的 pods，根据 pods 的地址创建出 endpoints 作为服务后端；Endpoints Controller 会 watch Service 以及 pod 的变化，维护对应的 Endpoint 信息。kube-proxy 根据Service 和 Endpoint 来维护本地的路由规则。当 Endpoint 发生变化，即 Service 以及关联的 pod 发生变化，kube-proxy 都会在每个节点上更新 iptables，实现一层负载均衡。而 ExternalName 模式则不指定 selector，相应的也就没有 port 和 endpoints。

* ExternalName 和 ClusterIP 中的 Headles Service 同属于 Headless Service 的两种情况。Headless Service 主要是指不分配 Service IP，且不通过 kube-proxy 做反向代理和负载均衡的服务。


