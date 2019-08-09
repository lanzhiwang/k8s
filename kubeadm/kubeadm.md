# Kubeadm – Bootstrap a kubernetes cluster

Building a cluster through various steps – kubeadm is the preferred way to start up a cluster.  In the following order, kubeadm

1. Kubeadm init
2. Pre Flight Checks – Pull container images  and check for available host resources
3. Creates a Certificate Authority
4. Generates Kubeconfig Files
5. Generate Static Pod Manifests – for Control Plane Pods
6. Starts up the Control Plane
7. Taints the Master (System Pods on master node)
8. Generates a Bootstrap Token
9. Starts Add On Pods:  DNS and Kube Proxy

[参考1](https://www.anujvarma.com/kubeadm-bootstrap-a-kubernetes-cluster/)

[参考2](https://juejin.im/entry/5c00d149e51d4522143b9c78)

```bash
[root@huzhi-code ~]# ./kubeadm init --dry-run > kubeadm.log
I0808 18:02:44.169994    7385 version.go:96] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get https://dl.k8s.io/release/stable-1.txt: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
I0808 18:02:44.170122    7385 version.go:97] falling back to the local client version: v1.14.5
	[WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd". Please follow the guide at https://kubernetes.io/docs/setup/cri/
	[WARNING FileExisting-socat]: socat not found in system path
	[WARNING SystemVerification]: this Docker version is not on the list of validated versions: 19.03.1. Latest validated version: 18.09
	[WARNING Hostname]: hostname "huzhi-code" could not be reached
	[WARNING Hostname]: hostname "huzhi-code": lookup huzhi-code on 119.29.29.29:53: no such host
	[WARNING Service-Kubelet]: kubelet service is not enabled, please run 'systemctl enable kubelet.service'
[root@huzhi-code ~]#
[root@huzhi-code ~]# vim kubeadm.log


[root@huzhi-code ~]# cat /tmp/kubeadm-init-dryrun301362558/kubeadm-flags.env
KUBELET_KUBEADM_ARGS=--cgroup-driver=cgroupfs --network-plugin=cni --pod-infra-container-image=k8s.gcr.io/pause:3.1
[root@huzhi-code ~]#

[root@huzhi-code ~]# cat /tmp/kubeadm-init-dryrun301362558/config.yaml
address: 0.0.0.0
apiVersion: kubelet.config.k8s.io/v1beta1
authentication:
  anonymous:
    enabled: false
  webhook:
    cacheTTL: 2m0s
    enabled: true
  x509:
    clientCAFile: /etc/kubernetes/pki/ca.crt
authorization:
  mode: Webhook
  webhook:
    cacheAuthorizedTTL: 5m0s
    cacheUnauthorizedTTL: 30s
cgroupDriver: cgroupfs
cgroupsPerQOS: true
clusterDNS:
- 10.96.0.10
clusterDomain: cluster.local
configMapAndSecretChangeDetectionStrategy: Watch
containerLogMaxFiles: 5
containerLogMaxSize: 10Mi
contentType: application/vnd.kubernetes.protobuf
cpuCFSQuota: true
cpuCFSQuotaPeriod: 100ms
cpuManagerPolicy: none
cpuManagerReconcilePeriod: 10s
enableControllerAttachDetach: true
enableDebuggingHandlers: true
enforceNodeAllocatable:
- pods
eventBurst: 10
eventRecordQPS: 5
evictionHard:
  imagefs.available: 15%
  memory.available: 100Mi
  nodefs.available: 10%
  nodefs.inodesFree: 5%
evictionPressureTransitionPeriod: 5m0s
failSwapOn: true
fileCheckFrequency: 20s
hairpinMode: promiscuous-bridge
healthzBindAddress: 127.0.0.1
healthzPort: 10248
httpCheckFrequency: 20s
imageGCHighThresholdPercent: 85
imageGCLowThresholdPercent: 80
imageMinimumGCAge: 2m0s
iptablesDropBit: 15
iptablesMasqueradeBit: 14
kind: KubeletConfiguration
kubeAPIBurst: 10
kubeAPIQPS: 5
makeIPTablesUtilChains: true
maxOpenFiles: 1000000
maxPods: 110
nodeLeaseDurationSeconds: 40
nodeStatusReportFrequency: 1m0s
nodeStatusUpdateFrequency: 10s
oomScoreAdj: -999
podPidsLimit: -1
port: 10250
registryBurst: 10
registryPullQPS: 5
resolvConf: /etc/resolv.conf
rotateCertificates: true
runtimeRequestTimeout: 2m0s
serializeImagePulls: true
staticPodPath: /etc/kubernetes/manifests
streamingConnectionIdleTimeout: 4h0m0s
syncFrequency: 1m0s
volumeStatsAggPeriod: 1m0s
[root@huzhi-code ~]#
```