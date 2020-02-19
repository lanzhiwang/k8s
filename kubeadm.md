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