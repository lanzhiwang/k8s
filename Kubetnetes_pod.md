# Kubetnetes 调度过程，也就是 Kubetnetes 中 pod 创建流程

Pod 是 Kubernetes 中最基本的部署调度单元，可以包含 container，逻辑上表示某种应用的一个实例。例如一个web 站点应用由前端、后端及数据库构建而成，这三个组件将运行在各自的容器中，那么我们可以创建包含三个container 的 pod。

Kubetnetes 中 pod 创建流程如下图所示

![](./images/kubernetes_schedule.svg)

具体的创建步骤包括：

1. 客户端提交创建请求，可以通过 API Server 的 Restful API，也可以使用 kubectl 命令行工具。支持的数据类型包括JSON和YAML。
2. API Server 处理用户请求，存储 Pod 数据到 etcd。
3. schedule 通过 API Server 查看未绑定的 Pod，尝试为 Pod 分配主机。
4. 过滤主机 (调度预选)：调度器用一组规则过滤掉不符合要求的主机。比如 Pod 指定了所需要的资源量，那么可用资源比 Pod 需要的资源量少的主机会被过滤掉。
5. 主机打分(调度优选)：对第一步筛选出的符合要求的主机进行打分，在主机打分阶段，调度器会考虑一些整体优化策略，比如把一个 Replication Controller 的副本分布到不同的主机上，使用最低负载的主机等。
6. 选择主机：选择打分最高的主机，进行 binding 操作，结果存储到 etcd 中。
7. kubelet 根据调度结果执行 Pod 创建操作： 绑定成功后，scheduler 会调用 APIServer 的 API 在 etcd 中创建一个 boundpod 对象，描述在一个工作节点上绑定运行的所有 pod 信息。运行在每个工作节点上的 kubelet 也会定期与 APIServer 同步 boundpod 信息，一旦发现应该在该工作节点上运行的 boundpod 对象没有更新，则调用Docker API 创建并启动 pod 内的容器。


# Kubetnetes 的预选策略(predicate)和优选策略(priority)

Kubernetes Scheduler 提供的调度流程分三步:

1. 预选策略(predicate): 遍历 nodelist，选择出符合要求的候选节点，Kubernetes 内置了多种预选规则供用户选择。
2. 优选策略(priority): 在选择出符合要求的候选节点中，采用优选规则计算出每个节点的积分，最后选择得分最高的。
3. 选定(select): 如果最高得分有好几个节点，select 就会从中随机选择一个节点。

### 常用的预选策略 

[参考源码](https://github.com/kubernetes/kubernetes/blob/master/pkg/scheduler/algorithm/predicates/predicates.go)

```go
const (
	// MatchInterPodAffinityPred defines the name of predicate MatchInterPodAffinity.
	MatchInterPodAffinityPred = "MatchInterPodAffinity"
    
	// CheckVolumeBindingPred defines the name of predicate CheckVolumeBinding.
	CheckVolumeBindingPred = "CheckVolumeBinding"
    // CheckVolumeBindingPred （检查是否可以绑定（默认没有启动））
    
	// CheckNodeConditionPred defines the name of predicate CheckNodeCondition.
	CheckNodeConditionPred = "CheckNodeCondition"
    // CheckNodeConditionPred 检查节点是否正常
    
	// GeneralPred defines the name of predicate GeneralPredicates.
	GeneralPred = "GeneralPredicates"
    
	// HostNamePred defines the name of predicate HostName.
	HostNamePred = "HostName"
    // HostNamePred(如果pod定义hostname属性，会检查节点是否匹配。pod.spec.hostname)
    
	// PodFitsHostPortsPred defines the name of predicate PodFitsHostPorts.
	PodFitsHostPortsPred = "PodFitsHostPorts"
    // PodFitsHostPortsPred（检查pod要暴露的hostpors是否被占用。pod.spec.containers.ports.hostPort）
    
	// MatchNodeSelectorPred defines the name of predicate MatchNodeSelector.
	MatchNodeSelectorPred = "MatchNodeSelector"
    // MatchNodeSelectorPred（pod.spec.nodeSelector 看节点标签能否适配 pod 定义的 nodeSelector）
    
	// PodFitsResourcesPred defines the name of predicate PodFitsResources.
	PodFitsResourcesPred = "PodFitsResources"
    // PodFitsResourcesPred（判断节点的资源能够满足Pod的定义，如果一个pod定义最少需要2C4G node上的低于此资源的将不被调度。用kubectl describe node NODE名称 可以查看资源使用情况）
    
	// NoDiskConflictPred defines the name of predicate NoDiskConflict.
	NoDiskConflictPred = "NoDiskConflict"
    // NoDiskConflictPred （判断pod定义的存储是否在node节点上使用。默认没有启用）
    
	// PodToleratesNodeTaintsPred defines the name of predicate PodToleratesNodeTaints.
	PodToleratesNodeTaintsPred = "PodToleratesNodeTaints"
    // PodToleratesNodeTaintsPred （检查pod上Tolerates的能否容忍污点（pod.spec.tolerations））
    
	// CheckNodeUnschedulablePred defines the name of predicate CheckNodeUnschedulablePredicate.
	CheckNodeUnschedulablePred = "CheckNodeUnschedulable"
    
	// PodToleratesNodeNoExecuteTaintsPred defines the name of predicate PodToleratesNodeNoExecuteTaints.
	PodToleratesNodeNoExecuteTaintsPred = "PodToleratesNodeNoExecuteTaints"
    
	// CheckNodeLabelPresencePred defines the name of predicate CheckNodeLabelPresence.
	CheckNodeLabelPresencePred = "CheckNodeLabelPresence"
    // CheckNodeLabelPresencePred （检查节点上的标志是否存在 （默认没有启动））
    
	// CheckServiceAffinityPred defines the name of predicate checkServiceAffinity.
	CheckServiceAffinityPred = "CheckServiceAffinity"
    // CheckServiceAffinity （根据 pod 所属的 service。将相同 service 上的 pod 尽量放到同一个节点（默认没有启动））
    
	// MaxEBSVolumeCountPred defines the name of predicate MaxEBSVolumeCount.
	// DEPRECATED
	// All cloudprovider specific predicates are deprecated in favour of MaxCSIVolumeCountPred.
	MaxEBSVolumeCountPred = "MaxEBSVolumeCount"
    
	// MaxGCEPDVolumeCountPred defines the name of predicate MaxGCEPDVolumeCount.
	// DEPRECATED
	// All cloudprovider specific predicates are deprecated in favour of MaxCSIVolumeCountPred.
	MaxGCEPDVolumeCountPred = "MaxGCEPDVolumeCount"
    
	// MaxAzureDiskVolumeCountPred defines the name of predicate MaxAzureDiskVolumeCount.
	// DEPRECATED
	// All cloudprovider specific predicates are deprecated in favour of MaxCSIVolumeCountPred.
	MaxAzureDiskVolumeCountPred = "MaxAzureDiskVolumeCount"
    
	// MaxCinderVolumeCountPred defines the name of predicate MaxCinderDiskVolumeCount.
	// DEPRECATED
	// All cloudprovider specific predicates are deprecated in favour of MaxCSIVolumeCountPred.
	MaxCinderVolumeCountPred = "MaxCinderVolumeCount"
    
	// MaxCSIVolumeCountPred defines the predicate that decides how many CSI volumes should be attached
	MaxCSIVolumeCountPred = "MaxCSIVolumeCountPred"
    
	// NoVolumeZoneConflictPred defines the name of predicate NoVolumeZoneConflict.
	NoVolumeZoneConflictPred = "NoVolumeZoneConflict"
    // NoVolumeZoneConflictPred （检查是否在一起区域（默认没有启动））
    
	// CheckNodeMemoryPressurePred defines the name of predicate CheckNodeMemoryPressure.
	CheckNodeMemoryPressurePred = "CheckNodeMemoryPressure"
    // CheckNodeMemoryPressurePred （检查内存是否存在压力）
    
	// CheckNodeDiskPressurePred defines the name of predicate CheckNodeDiskPressure.
	CheckNodeDiskPressurePred = "CheckNodeDiskPressure"
    // CheckNodeDiskPressurePred （检查磁盘IO压力是否过大）
    
	// CheckNodePIDPressurePred defines the name of predicate CheckNodePIDPressure.
	CheckNodePIDPressurePred = "CheckNodePIDPressure"
    // CheckNodePIDPressurePred （检查pid资源是否过大）

	// DefaultMaxGCEPDVolumes defines the maximum number of PD Volumes for GCE
	// GCE instances can have up to 16 PD volumes attached.
	DefaultMaxGCEPDVolumes = 16
    
	// DefaultMaxAzureDiskVolumes defines the maximum number of PD Volumes for Azure
	// Larger Azure VMs can actually have much more disks attached.
	// TODO We should determine the max based on VM size
	DefaultMaxAzureDiskVolumes = 16

	// KubeMaxPDVols defines the maximum number of PD Volumes per kubelet
	KubeMaxPDVols = "KUBE_MAX_PD_VOLS"

	// EBSVolumeFilterType defines the filter name for EBSVolumeFilter.
	EBSVolumeFilterType = "EBS"
    
	// GCEPDVolumeFilterType defines the filter name for GCEPDVolumeFilter.
	GCEPDVolumeFilterType = "GCE"
    
	// AzureDiskVolumeFilterType defines the filter name for AzureDiskVolumeFilter.
	AzureDiskVolumeFilterType = "AzureDisk"
    
	// CinderVolumeFilterType defines the filter name for CinderVolumeFilter.
	CinderVolumeFilterType = "Cinder"
)

```

### 常用的优选策略 

[参考源码](https://github.com/kubernetes/kubernetes/blob/master/pkg/scheduler/algorithm/priorities/priorities.go)

```go
const (
	// EqualPriority defines the name of prioritizer function that gives an equal weight of one to all nodes.
	EqualPriority = "EqualPriority"
    // EqualPriority定义优先级函数的名称，该函数给予所有节点相同权重。
    
	// MostRequestedPriority defines the name of prioritizer function that gives used nodes higher priority.
	MostRequestedPriority = "MostRequestedPriority"
    // MostRequestedPriority定义优先级函数的名称，该函数为使用的节点提供更高的优先级。
    // most_requested 选择消耗最大的节点上（尽量将一个节点上的资源用完）
    
	// RequestedToCapacityRatioPriority defines the name of RequestedToCapacityRatioPriority.
	RequestedToCapacityRatioPriority = "RequestedToCapacityRatioPriority"
    
	// SelectorSpreadPriority defines the name of prioritizer function that spreads pods by minimizing
	// the number of pods (belonging to the same service or replication controller) on the same node.
	SelectorSpreadPriority = "SelectorSpreadPriority"
    // selector_spreading 与services上其他pod尽量不在同一个节点上，节点上通一个service的pod越少得分越高。
    
	// ServiceSpreadingPriority is largely replaced by "SelectorSpreadPriority".
	ServiceSpreadingPriority = "ServiceSpreadingPriority"
    
	// InterPodAffinityPriority defines the name of prioritizer function that decides which pods should or
	// should not be placed in the same topological domain as some other pods.
	InterPodAffinityPriority = "InterPodAffinityPriority"
    // interpod_affinity 遍历node上的亲和性条目，匹配项越多的得分越高
    
	// LeastRequestedPriority defines the name of prioritizer function that prioritize nodes by least
	// requested utilization.
	LeastRequestedPriority = "LeastRequestedPriority"
    // least_requested 选择消耗最小的节点（根据空闲比率评估 cpu(总容量-sum(已使用)*10/总容量) ）
    
	// BalancedResourceAllocation defines the name of prioritizer function that prioritizes nodes
	// to help achieve balanced resource usage.
	BalancedResourceAllocation = "BalancedResourceAllocation"
    // balanced_resource_allocation 从节点列表中选出各项资源使用率最均衡的节点（CPU和内存）
    
	// NodePreferAvoidPodsPriority defines the name of prioritizer function that priorities nodes according to
	// the node annotation "scheduler.alpha.kubernetes.io/preferAvoidPods".
	NodePreferAvoidPodsPriority = "NodePreferAvoidPodsPriority"
    // node_prefer_avoid_pods 节点倾向
    
	// NodeAffinityPriority defines the name of prioritizer function that prioritizes nodes which have labels
	// matching NodeAffinity.
	NodeAffinityPriority = "NodeAffinityPriority"
    // node_label 根据节点标签得分，存在标签既得分，没有标签没得分。标签越多 得分越高。
    
	// TaintTolerationPriority defines the name of prioritizer function that prioritizes nodes that marked
	// with taint which pod can tolerate.
	TaintTolerationPriority = "TaintTolerationPriority"
    // taint_toleration 将pod对象的spec.toleration与节点的taints列表项进行匹配度检查，匹配的条目越多，得分越低。
    
	// ImageLocalityPriority defines the name of prioritizer function that prioritizes nodes that have images
	// requested by the pod present.
	ImageLocalityPriority = "ImageLocalityPriority"
    // image_locality 节点上有所需要的镜像既得分，所需镜像越多得分越高。（根据已有镜像体积大小之和）
    
	// ResourceLimitsPriority defines the nodes of prioritizer function ResourceLimitsPriority.
	ResourceLimitsPriority = "ResourceLimitsPriority"
)

```

## Kubetnetes 节点亲和性

[参考](https://www.cnblogs.com/breezey/p/9101666.html)

```
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/e2e-az-name
            operator: In
            values:
            - e2e-az1
            - e2e-az2
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
            - another-node-label-value
  containers:
  - name: with-node-affinity
    image: gcr.io/google_containers/pause:2.0

```

目前主要的 nodeAffinity: 

* requiredDuringSchedulingIgnoredDuringExecution
表示 pod 必须部署到满足条件的节点上，如果没有满足条件的节点，就不停重试。其中 IgnoreDuringExecution 表示 pod 部署之后运行的时候，如果节点标签发生了变化，不再满足 pod 指定的条件，pod也会继续运行。

* requiredDuringSchedulingRequiredDuringExecution
表示 pod 必须部署到满足条件的节点上，如果没有满足条件的节点，就不停重试。其中 RequiredDuringExecution表示 pod 部署之后运行的时候，如果节点标签发生了变化，不再满足 pod 指定的条件，则重新选择符合要求的节点。

* preferredDuringSchedulingIgnoredDuringExecution
表示优先部署到满足条件的节点上，如果没有满足条件的节点，就忽略这些条件，按照正常逻辑部署。其中IgnoredDuringExecution表示如果后面节点标签发生了变化，满足了条件，也不重新调度到满足条件的节点。

* preferredDuringSchedulingRequiredDuringExecution
表示优先部署到满足条件的节点上，如果没有满足条件的节点，就忽略这些条件，按照正常逻辑部署。其中RequiredDuringExecution表示如果后面节点标签发生了变化，满足了条件，则重新调度到满足条件的节点。

## Kubetnetes pod 亲和性

[参考](https://www.cnblogs.com/breezey/p/9101675.html)

Pod Affinity
K8S 调度的 `nodeAffinity` 说明在调度的时候让 pod 灵活的选择 node，但有些时候我们希望调度能够考虑pod 之间的关系，而不只是 pod 与 node 的关系。于是在 kubernetes 1.4 的时候引入了`pod affinity`。

为什么有这样的需求呢？举个例子，我们系统服务 A 和服务 B 尽量部署在同个主机、机房、城市，因为它们网络沟通比较多；再比如，我们系统数据服务 C 和数据服务 D 尽量分开，因为如果它们分配到一起，然后主机或者机房出了问题，会导致应用完全不可用，如果它们是分开的，应用虽然有影响，但还是可用的。

pod affinity 可以这样理解：调度的时候选择（或者不选择）这样的节点 N ，这些节点上已经运行了满足条件 X。条件 X 是一组 label 选择器，它必须指明作用的 namespace（也可以作用于所有的 namespace），因为 pod 是运行在某个 namespace 中的。

这里的X指的是集群中的节点、机架、区域等概念，通过kubernetes内置节点标签中的key来进行声明。这个key的名字为 topologyKey，意为表达节点所属的 topology 范围：

kubernetes.io/hostname
failure-domain.beta.kubernetes.io/zone
failure-domain.beta.kubernetes.io/region

和 node affinity 相似，pod affinity 也有 requiredDuringSchedulingIgnoredDuringExecution 和 preferredDuringSchedulingIgnoredDuringExecution，意义也和之前一样。如果有使用亲和性，在 affinity 下面添加 podAffinity 字段，如果要使用互斥性，在 affinity 下面添加 podAntiAffinity 字段。

先定义一个参照目标pod：

```
apiVersion: v1
kind: Pod
metadata:
  name: pod-flag
  labels:
    security: "S1"
    app: "nginx"
spec:
  containers:
  - name: nginx
    image: nginx
```

下面是一个亲和性调度的示例

```
apiVersion: v1
kind: Pod
metadata:
  name: pod-affinity
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: security
            operator: In
            values:
            - S1
        topologyKey: kubernetes.io/hostname
  containers:
  - name: with-pod-affinity
    image: gcr.io/google_containers/pause:2.0

```

下面是一个互斥性调度的示例：

```
apiVersion: v1
kind: Pod
metadata:
  name: with-pod-affinity
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: security
            operator: In
            values:
            - S1
        topologyKey: "failure-domain.beta.kubernetes.io/zone"
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: security
              operator: In
              values:
              - S2
          topologyKey: kubernetes.io/hostname
  containers:
  - name: with-pod-affinity
    image: gcr.io/google_containers/pause:2.0

```



## Kubetnetes Taints and Tolerations

[参考](https://www.cnblogs.com/breezey/p/9101677.html)

Taints 和 Tolerations（ 污点和容忍）

在 NodeAffinity 节点亲和性，是在 pod 上定义的一种属性，使得 Pod 能够被调度到某些 node 上运行。Taint 刚好相反，它让 node 拒绝 Pod 的运行。

Taint 需要与 Toleration 配合使用，让 pod 避开那些不合适的 node。

在 node 上设置一个或多个 Taint 后，除非 pod 明确声明能够容忍这些“污点”，否则无法在这些 node 上运行。Toleration 是 pod 的属性，让 pod 能够（注意，只是能够，而非必须）运行在标注了 Taint 的 node 上。

设置污点:

```
kubectl taint node [node] key=value:[effect]
其中[effect]可取值： [ NoSchedule | PreferNoSchedule | NoExecute ]
NoSchedule ：一定不能被调度。
PreferNoSchedule：尽量不要调度。
NoExecute：不仅不会调度，还会驱逐 Node 上已有的Pod。

# 示例：
kubectl taint node 10.3.1.16 test=16:NoSchedule    
```

去除污点

```
# 去除指定 key 及其 effect (这里的key不用指定value)
kubectl taint nodes node_name key:[effect]-

# 去除指定 key 所有的 effect
kubectl taint nodes node_name key-

# 示例

kubectl taint node 10.3.1.16 test=16:NoSchedule
kubectl taint node 10.3.1.16 test=16:NoExecute

kubectl taint node 10.3.1.16 test:NoSchedule-
kubectl taint node 10.3.1.16 test:NoExecute-
kubectl taint node 10.3.1.16 test-
```

下面是一个简单的示例：

在 node1 上加一个Taint，该 Taint 的键为 key，值为 value，Taint 的效果是 NoSchedule。这意味着除非pod明确声明可以容忍这个 Taint，否则就不会被调度到 node1 上

```
kubectl taint nodes node1  key=value:NoSchedule
```

然后需要在 pod 上声明 Toleration。下面的 Toleration 设置为可以容忍具有该 Taint 的 Node，使得 pod 能够被调度到 node1 上

```
apiVersion: v1
kind: Pod
metadata:
  name: pod-taints
spec:
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
  containers:
    - name: pod-taints
      image: busybox:latest
```

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


