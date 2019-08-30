# Default User and Group

```bash
[root@master01 ~]# kubectl get serviceaccounts --all-namespaces
NAMESPACE       NAME                                 SECRETS   AGE
chenguanwei     default                              1         92d
dce-system      default                              1         106d
dcs             coredns                              1         66d
dcs             default                              1         66d
default         coredns                              1         99d
default         dce-ceph-cephrbd-provisioner         1         20d
default         default                              1         106d
dev             default                              1         64d
devops          default                              1         57d
dmp             default                              1         77d
elk             default                              1         29d
elk             elasticsearch-admin                  1         21d
huangliang      default                              1         44d
ingress-nginx   default                              1         94d
ingress-nginx   nginx-ingress-serviceaccount         1         94d
jenkins         default                              1         10d
kube-public     default                              1         106d
kube-system     attachdetach-controller              1         106d
kube-system     bootstrap-signer                     1         106d
kube-system     calico-kube-controllers              1         106d
kube-system     calico-node                          1         106d
kube-system     certificate-controller               1         106d
kube-system     clusterrole-aggregation-controller   1         106d
kube-system     coredns                              1         70d
kube-system     cronjob-controller                   1         106d
kube-system     daemon-set-controller                1         106d
kube-system     default                              1         106d
kube-system     deployment-controller                1         106d
kube-system     disruption-controller                1         106d
kube-system     endpoint-controller                  1         106d
kube-system     generic-garbage-collector            1         106d
kube-system     horizontal-pod-autoscaler            1         106d
kube-system     ingress01                            1         76d
kube-system     job-controller                       1         106d
kube-system     metrics-server                       1         56d
kube-system     namespace-controller                 1         106d
kube-system     node-controller                      1         106d
kube-system     persistent-volume-binder             1         106d
kube-system     pod-garbage-collector                1         106d
kube-system     prometheus                           1         48d
kube-system     pv-protection-controller             1         106d
kube-system     pvc-protection-controller            1         106d
kube-system     replicaset-controller                1         106d
kube-system     replication-controller               1         106d
kube-system     resourcequota-controller             1         106d
kube-system     service-account-controller           1         106d
kube-system     service-controller                   1         106d
kube-system     statefulset-controller               1         106d
kube-system     tiller                               1         94d
kube-system     token-cleaner                        1         106d
kube-system     ttl-controller                       1         106d
minyiyun        default                              1         36d
prometheus      default                              1         48d
prometheus      nfs-client-provisioner               1         48d
test            default                              1         80d
[root@master01 ~]#

########################################################

[root@master01 ~]# kubectl get rolebindings  --all-namespaces
NAMESPACE       NAME                                             AGE
default         dce-ceph-cephrbd-provisioner                     20d
devops          prometheus-admin                                 37d
huangliang      daocloud.io:cluster_role_dce:tenant-admin        44d
huangliang      daocloud.io:cluster_role_dce:tenant-default      44d
ingress-nginx   nginx-ingress-role-nisa-binding                  94d
kube-public     system:controller:bootstrap-signer               107d
kube-system     ingress01                                        76d
kube-system     metrics-server-auth-reader                       56d
kube-system     system::leader-locking-kube-controller-manager   107d
kube-system     system::leader-locking-kube-scheduler            107d
kube-system     system:controller:bootstrap-signer               107d
kube-system     system:controller:cloud-provider                 107d
kube-system     system:controller:token-cleaner                  107d
test            daocloud.io:cluster_role_dce:tenant-admin        80d
test            daocloud.io:cluster_role_dce:tenant-default      80d
[root@master01 ~]#
[root@master01 ~]#

kubectl describe rolebindings dce-ceph-cephrbd-provisioner -n default
Name:         dce-ceph-cephrbd-provisioner
Labels:       dce.daocloud.io/app=dce-ceph
Annotations:  <none>
Role:
  Kind:  Role
  Name:  dce-ceph-cephrbd-provisioner
Subjects:
  Kind            Name                          Namespace
  ----            ----                          ---------
  ServiceAccount  dce-ceph-cephrbd-provisioner

kubectl describe rolebindings prometheus-admin -n devops
Name:         prometheus-admin
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind            Name     Namespace
  ----            ----     ---------
  ServiceAccount  default  default

kubectl describe rolebindings daocloud.io:cluster_role_dce:tenant-admin -n huangliang
Name:         daocloud.io:cluster_role_dce:tenant-admin
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce:tenant-admin
Subjects:
  Kind   Name                              Namespace
  ----   ----                              ---------
  Group  1cae2b56e78f4c12b1273930e592edd0

kubectl describe rolebindings daocloud.io:cluster_role_dce:tenant-default -n huangliang
Name:         daocloud.io:cluster_role_dce:tenant-default
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce:tenant-default
Subjects:
  Kind   Name                              Namespace
  ----   ----                              ---------
  Group  1cae2b56e78f4c12b1273930e592edd0

kubectl describe rolebindings nginx-ingress-role-nisa-binding -n ingress-nginx
Name:         nginx-ingress-role-nisa-binding
Labels:       app.kubernetes.io/name=ingress-nginx
              app.kubernetes.io/part-of=ingress-nginx
Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"rbac.authorization.k8s.io/v1beta1","kind":"RoleBinding","metadata":{"annotations":{},"labels":{"app.kubernetes.io/name":"ingress-nginx",...
Role:
  Kind:  Role
  Name:  nginx-ingress-role
Subjects:
  Kind            Name                          Namespace
  ----            ----                          ---------
  ServiceAccount  nginx-ingress-serviceaccount  ingress-nginx

kubectl describe rolebindings system:controller:bootstrap-signer -n kube-public
Name:         system:controller:bootstrap-signer
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  Role
  Name:  system:controller:bootstrap-signer
Subjects:
  Kind            Name              Namespace
  ----            ----              ---------
  ServiceAccount  bootstrap-signer  kube-system

kubectl describe rolebindings ingress01 -n kube-system
Name:         ingress01
Labels:       io.daocloud.dce.ingress.controller.name=ingress01
Annotations:  <none>
Role:
  Kind:  Role
  Name:  ingress01
Subjects:
  Kind            Name       Namespace
  ----            ----       ---------
  ServiceAccount  ingress01  kube-system

kubectl describe rolebindings metrics-server-auth-reader -n kube-system
Name:         metrics-server-auth-reader
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  Role
  Name:  extension-apiserver-authentication-reader
Subjects:
  Kind            Name            Namespace
  ----            ----            ---------
  ServiceAccount  metrics-server  kube-system

kubectl describe rolebindings system::leader-locking-kube-controller-manager -n kube-system
Name:         system::leader-locking-kube-controller-manager
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  Role
  Name:  system::leader-locking-kube-controller-manager
Subjects:
  Kind            Name                     Namespace
  ----            ----                     ---------
  ServiceAccount  kube-controller-manager  kube-system

kubectl describe rolebindings system::leader-locking-kube-scheduler -n kube-system
Name:         system::leader-locking-kube-scheduler
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  Role
  Name:  system::leader-locking-kube-scheduler
Subjects:
  Kind            Name            Namespace
  ----            ----            ---------
  ServiceAccount  kube-scheduler  kube-system

kubectl describe rolebindings system:controller:bootstrap-signer -n kube-system
Name:         system:controller:bootstrap-signer
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  Role
  Name:  system:controller:bootstrap-signer
Subjects:
  Kind            Name              Namespace
  ----            ----              ---------
  ServiceAccount  bootstrap-signer  kube-system

kubectl describe rolebindings system:controller:cloud-provider -n kube-system
Name:         system:controller:cloud-provider
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  Role
  Name:  system:controller:cloud-provider
Subjects:
  Kind            Name            Namespace
  ----            ----            ---------
  ServiceAccount  cloud-provider  kube-system

kubectl describe rolebindings system:controller:token-cleaner -n kube-system
Name:         system:controller:token-cleaner
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  Role
  Name:  system:controller:token-cleaner
Subjects:
  Kind            Name           Namespace
  ----            ----           ---------
  ServiceAccount  token-cleaner  kube-system

kubectl describe rolebindings daocloud.io:cluster_role_dce:tenant-admin -n test
Name:         daocloud.io:cluster_role_dce:tenant-admin
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce:tenant-admin
Subjects:
  Kind   Name                              Namespace
  ----   ----                              ---------
  Group  06e8b16b81344994bec260a587b17453

kubectl describe rolebindings daocloud.io:cluster_role_dce:tenant-default -n test
Name:         daocloud.io:cluster_role_dce:tenant-default
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce:tenant-default
Subjects:
  Kind   Name                              Namespace
  ----   ----                              ---------
  Group  06e8b16b81344994bec260a587b17453




########################################################

[root@master01 ~]# kubectl get clusterrolebindings  --all-namespaces
NAME                                                   AGE
admin-cluster-admin-binding                            94d
calico-kube-controllers                                107d
calico-node                                            107d
cityinthesky-cluster-admin-binding                     94d
cluster-admin                                          107d
daocloud.io:dce:cluster-admin                          80d
daocloud.io:dce:cluster-role-1e4be994                  77d
dce-ceph-cephrbd-provisioner                           20d
dce:cluster-default                                    107d
ingress01                                              76d
metrics-server:system:auth-delegator                   56d
nginx-ingress-clusterrole-nisa-binding                 94d
prometheus                                             48d
run-nfs-client-provisioner                             48d
system:aws-cloud-provider                              107d
system:basic-user                                      107d
system:controller:attachdetach-controller              107d
system:controller:certificate-controller               107d
system:controller:clusterrole-aggregation-controller   107d
system:controller:cronjob-controller                   107d
system:controller:daemon-set-controller                107d
system:controller:deployment-controller                107d
system:controller:disruption-controller                107d
system:controller:endpoint-controller                  107d
system:controller:generic-garbage-collector            107d
system:controller:horizontal-pod-autoscaler            107d
system:controller:job-controller                       107d
system:controller:namespace-controller                 107d
system:controller:node-controller                      107d
system:controller:persistent-volume-binder             107d
system:controller:pod-garbage-collector                107d
system:controller:pv-protection-controller             107d
system:controller:pvc-protection-controller            107d
system:controller:replicaset-controller                107d
system:controller:replication-controller               107d
system:controller:resourcequota-controller             107d
system:controller:route-controller                     107d
system:controller:service-account-controller           107d
system:controller:service-controller                   107d
system:controller:statefulset-controller               107d
system:controller:ttl-controller                       107d
system:coredns                                         70d
system:discovery                                       107d
system:kube-controller-manager                         107d
system:kube-dns                                        107d
system:kube-scheduler                                  107d
system:metrics-server                                  56d
system:node                                            107d
system:node-proxier                                    107d
system:volume-scheduler                                107d
tiller                                                 94d
tiller-cluster-rule                                    94d
[root@master01 ~]#



kubectl describe clusterrolebindings admin-cluster-admin-binding
Name:         admin-cluster-admin-binding
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind  Name   Namespace
  ----  ----   ---------
  User  admin

kubectl describe clusterrolebindings calico-kube-controllers
Name:         calico-kube-controllers
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  calico-kube-controllers
Subjects:
  Kind            Name                     Namespace
  ----            ----                     ---------
  ServiceAccount  calico-kube-controllers  kube-system

kubectl describe clusterrolebindings calico-node
Name:         calico-node
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  calico-node
Subjects:
  Kind            Name         Namespace
  ----            ----         ---------
  ServiceAccount  calico-node  kube-system

kubectl describe clusterrolebindings cityinthesky-cluster-admin-binding
Name:         cityinthesky-cluster-admin-binding
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind  Name          Namespace
  ----  ----          ---------
  User  cityinthesky

kubectl describe clusterrolebindings cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind   Name            Namespace
  ----   ----            ---------
  Group  system:masters

kubectl describe clusterrolebindings daocloud.io:dce:cluster-admin
Name:         daocloud.io:dce:cluster-admin
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce:cluster-admin
Subjects:
  Kind  Name      Namespace
  ----  ----      ---------
  User  testUser

kubectl describe clusterrolebindings daocloud.io:dce:cluster-role-1e4be994
Name:         daocloud.io:dce:cluster-role-1e4be994
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce:cluster-role-1e4be994
Subjects:
  Kind  Name  Namespace
  ----  ----  ---------
  User  pwj
  User  001

kubectl describe clusterrolebindings dce-ceph-cephrbd-provisioner
Name:         dce-ceph-cephrbd-provisioner
Labels:       dce.daocloud.io/app=dce-ceph
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce-ceph-cephrbd-provisioner
Subjects:
  Kind            Name                          Namespace
  ----            ----                          ---------
  ServiceAccount  dce-ceph-cephrbd-provisioner  default

kubectl describe clusterrolebindings dce:cluster-default
Name:         dce:cluster-default
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  dce:cluster-default
Subjects:
  Kind   Name              Namespace
  ----   ----              ---------
  Group  dce:normal-users

kubectl describe clusterrolebindings ingress01
Name:         ingress01
Labels:       io.daocloud.dce.ingress.controller.name=ingress01
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  ingress01
Subjects:
  Kind            Name       Namespace
  ----            ----       ---------
  ServiceAccount  ingress01  kube-system

kubectl describe clusterrolebindings metrics-server:system:auth-delegator
Name:         metrics-server:system:auth-delegator
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  system:auth-delegator
Subjects:
  Kind            Name            Namespace
  ----            ----            ---------
  ServiceAccount  metrics-server  kube-system

kubectl describe clusterrolebindings nginx-ingress-clusterrole-nisa-binding
Name:         nginx-ingress-clusterrole-nisa-binding
Labels:       app.kubernetes.io/name=ingress-nginx
              app.kubernetes.io/part-of=ingress-nginx
Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"rbac.authorization.k8s.io/v1beta1","kind":"ClusterRoleBinding","metadata":{"annotations":{},"labels":{"app.kubernetes.io/name":"ingress-...
Role:
  Kind:  ClusterRole
  Name:  nginx-ingress-clusterrole
Subjects:
  Kind            Name                          Namespace
  ----            ----                          ---------
  ServiceAccount  nginx-ingress-serviceaccount  ingress-nginx

kubectl describe clusterrolebindings prometheus
Name:         prometheus
Labels:       addonmanager.kubernetes.io/mode=Reconcile
              kubernetes.io/cluster-service=true
Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"rbac.authorization.k8s.io/v1","kind":"ClusterRoleBinding","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reco...
Role:
  Kind:  ClusterRole
  Name:  prometheus
Subjects:
  Kind            Name        Namespace
  ----            ----        ---------
  ServiceAccount  prometheus  kube-system

kubectl describe clusterrolebindings run-nfs-client-provisioner
Name:         run-nfs-client-provisioner
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"rbac.authorization.k8s.io/v1","kind":"ClusterRoleBinding","metadata":{"annotations":{},"name":"run-nfs-client-provisioner","namespace":"...
Role:
  Kind:  ClusterRole
  Name:  nfs-client-provisioner-runner
Subjects:
  Kind            Name                    Namespace
  ----            ----                    ---------
  ServiceAccount  nfs-client-provisioner  prometheus

kubectl describe clusterrolebindings system:aws-cloud-provider
Name:         system:aws-cloud-provider
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:aws-cloud-provider
Subjects:
  Kind            Name                Namespace
  ----            ----                ---------
  ServiceAccount  aws-cloud-provider  kube-system

kubectl describe clusterrolebindings system:basic-user
Name:         system:basic-user
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:basic-user
Subjects:
  Kind   Name                    Namespace
  ----   ----                    ---------
  Group  system:authenticated
  Group  system:unauthenticated

kubectl describe clusterrolebindings system:controller:attachdetach-controller
Name:         system:controller:attachdetach-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:attachdetach-controller
Subjects:
  Kind            Name                     Namespace
  ----            ----                     ---------
  ServiceAccount  attachdetach-controller  kube-system

kubectl describe clusterrolebindings system:controller:certificate-controller
Name:         system:controller:certificate-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:certificate-controller
Subjects:
  Kind            Name                    Namespace
  ----            ----                    ---------
  ServiceAccount  certificate-controller  kube-system

kubectl describe clusterrolebindings system:controller:clusterrole-aggregation-controller
Name:         system:controller:clusterrole-aggregation-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:clusterrole-aggregation-controller
Subjects:
  Kind            Name                                Namespace
  ----            ----                                ---------
  ServiceAccount  clusterrole-aggregation-controller  kube-system

kubectl describe clusterrolebindings system:controller:cronjob-controller
Name:         system:controller:cronjob-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:cronjob-controller
Subjects:
  Kind            Name                Namespace
  ----            ----                ---------
  ServiceAccount  cronjob-controller  kube-system

kubectl describe clusterrolebindings system:controller:daemon-set-controller
Name:         system:controller:daemon-set-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:daemon-set-controller
Subjects:
  Kind            Name                   Namespace
  ----            ----                   ---------
  ServiceAccount  daemon-set-controller  kube-system

kubectl describe clusterrolebindings system:controller:deployment-controller
Name:         system:controller:deployment-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:deployment-controller
Subjects:
  Kind            Name                   Namespace
  ----            ----                   ---------
  ServiceAccount  deployment-controller  kube-system

kubectl describe clusterrolebindings system:controller:disruption-controller
Name:         system:controller:disruption-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:disruption-controller
Subjects:
  Kind            Name                   Namespace
  ----            ----                   ---------
  ServiceAccount  disruption-controller  kube-system

kubectl describe clusterrolebindings system:controller:endpoint-controller
Name:         system:controller:endpoint-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:endpoint-controller
Subjects:
  Kind            Name                 Namespace
  ----            ----                 ---------
  ServiceAccount  endpoint-controller  kube-system

kubectl describe clusterrolebindings system:controller:generic-garbage-collector
Name:         system:controller:generic-garbage-collector
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:generic-garbage-collector
Subjects:
  Kind            Name                       Namespace
  ----            ----                       ---------
  ServiceAccount  generic-garbage-collector  kube-system

kubectl describe clusterrolebindings system:controller:horizontal-pod-autoscaler
Name:         system:controller:horizontal-pod-autoscaler
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:horizontal-pod-autoscaler
Subjects:
  Kind            Name                       Namespace
  ----            ----                       ---------
  ServiceAccount  horizontal-pod-autoscaler  kube-system

kubectl describe clusterrolebindings system:controller:job-controller
Name:         system:controller:job-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:job-controller
Subjects:
  Kind            Name            Namespace
  ----            ----            ---------
  ServiceAccount  job-controller  kube-system

kubectl describe clusterrolebindings system:controller:namespace-controller
Name:         system:controller:namespace-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:namespace-controller
Subjects:
  Kind            Name                  Namespace
  ----            ----                  ---------
  ServiceAccount  namespace-controller  kube-system

kubectl describe clusterrolebindings system:controller:node-controller
Name:         system:controller:node-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:node-controller
Subjects:
  Kind            Name             Namespace
  ----            ----             ---------
  ServiceAccount  node-controller  kube-system

kubectl describe clusterrolebindings system:controller:persistent-volume-binder
Name:         system:controller:persistent-volume-binder
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:persistent-volume-binder
Subjects:
  Kind            Name                      Namespace
  ----            ----                      ---------
  ServiceAccount  persistent-volume-binder  kube-system

kubectl describe clusterrolebindings system:controller:pod-garbage-collector
Name:         system:controller:pod-garbage-collector
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:pod-garbage-collector
Subjects:
  Kind            Name                   Namespace
  ----            ----                   ---------
  ServiceAccount  pod-garbage-collector  kube-system

kubectl describe clusterrolebindings system:controller:pv-protection-controller
Name:         system:controller:pv-protection-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:pv-protection-controller
Subjects:
  Kind            Name                      Namespace
  ----            ----                      ---------
  ServiceAccount  pv-protection-controller  kube-system

kubectl describe clusterrolebindings system:controller:pvc-protection-controller
Name:         system:controller:pvc-protection-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:pvc-protection-controller
Subjects:
  Kind            Name                       Namespace
  ----            ----                       ---------
  ServiceAccount  pvc-protection-controller  kube-system

kubectl describe clusterrolebindings system:controller:replicaset-controller
Name:         system:controller:replicaset-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:replicaset-controller
Subjects:
  Kind            Name                   Namespace
  ----            ----                   ---------
  ServiceAccount  replicaset-controller  kube-system

kubectl describe clusterrolebindings system:controller:replication-controller
Name:         system:controller:replication-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:replication-controller
Subjects:
  Kind            Name                    Namespace
  ----            ----                    ---------
  ServiceAccount  replication-controller  kube-system

kubectl describe clusterrolebindings system:controller:resourcequota-controller
Name:         system:controller:resourcequota-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:resourcequota-controller
Subjects:
  Kind            Name                      Namespace
  ----            ----                      ---------
  ServiceAccount  resourcequota-controller  kube-system

kubectl describe clusterrolebindings system:controller:route-controller
Name:         system:controller:route-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:route-controller
Subjects:
  Kind            Name              Namespace
  ----            ----              ---------
  ServiceAccount  route-controller  kube-system

kubectl describe clusterrolebindings system:controller:service-account-controller
Name:         system:controller:service-account-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:service-account-controller
Subjects:
  Kind            Name                        Namespace
  ----            ----                        ---------
  ServiceAccount  service-account-controller  kube-system

kubectl describe clusterrolebindings system:controller:service-controller
Name:         system:controller:service-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:service-controller
Subjects:
  Kind            Name                Namespace
  ----            ----                ---------
  ServiceAccount  service-controller  kube-system

kubectl describe clusterrolebindings system:controller:statefulset-controller
Name:         system:controller:statefulset-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:statefulset-controller
Subjects:
  Kind            Name                    Namespace
  ----            ----                    ---------
  ServiceAccount  statefulset-controller  kube-system

kubectl describe clusterrolebindings system:controller:ttl-controller
Name:         system:controller:ttl-controller
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:controller:ttl-controller
Subjects:
  Kind            Name            Namespace
  ----            ----            ---------
  ServiceAccount  ttl-controller  kube-system

kubectl describe clusterrolebindings system:coredns
Name:         system:coredns
Labels:       addonmanager.kubernetes.io/mode=EnsureExists
              kubernetes.io/bootstrapping=rbac-defaults
Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"rbac.authorization.k8s.io/v1","kind":"ClusterRoleBinding","metadata":{"annotations":{"rbac.authorization.kubernetes.io/autoupdate":"true...
              rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:coredns
Subjects:
  Kind            Name     Namespace
  ----            ----     ---------
  ServiceAccount  coredns  kube-system

kubectl describe clusterrolebindings system:discovery
Name:         system:discovery
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:discovery
Subjects:
  Kind   Name                    Namespace
  ----   ----                    ---------
  Group  system:authenticated
  Group  system:unauthenticated

kubectl describe clusterrolebindings system:kube-controller-manager
Name:         system:kube-controller-manager
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:kube-controller-manager
Subjects:
  Kind  Name                            Namespace
  ----  ----                            ---------
  User  system:kube-controller-manager

kubectl describe clusterrolebindings system:kube-dns
Name:         system:kube-dns
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:kube-dns
Subjects:
  Kind            Name      Namespace
  ----            ----      ---------
  ServiceAccount  kube-dns  kube-system

kubectl describe clusterrolebindings system:kube-scheduler
Name:         system:kube-scheduler
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:kube-scheduler
Subjects:
  Kind  Name                   Namespace
  ----  ----                   ---------
  User  system:kube-scheduler

kubectl describe clusterrolebindings system:metrics-server
Name:         system:metrics-server
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  system:metrics-server
Subjects:
  Kind            Name            Namespace
  ----            ----            ---------
  ServiceAccount  metrics-server  kube-system

kubectl describe clusterrolebindings system:node
Name:         system:node
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:node
Subjects:
  Kind  Name              Namespace
  ----  ----              ---------
  User  system:node:fake

kubectl describe clusterrolebindings system:node-proxier
Name:         system:node-proxier
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:node-proxier
Subjects:
  Kind  Name               Namespace
  ----  ----               ---------
  User  system:kube-proxy

kubectl describe clusterrolebindings system:volume-scheduler
Name:         system:volume-scheduler
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:volume-scheduler
Subjects:
  Kind  Name                   Namespace
  ----  ----                   ---------
  User  system:kube-scheduler

kubectl describe clusterrolebindings tiller
Name:         tiller
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"rbac.authorization.k8s.io/v1beta1","kind":"ClusterRoleBinding","metadata":{"annotations":{},"name":"tiller","namespace":""},"roleRef":{"...
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind            Name    Namespace
  ----            ----    ---------
  ServiceAccount  tiller  kube-system

kubectl describe clusterrolebindings tiller-cluster-rule
Name:         tiller-cluster-rule
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind            Name    Namespace
  ----            ----    ---------
  ServiceAccount  tiller  kube-system


```

# User

```bash

User  admin

User  system:kube-controller-manager

User  system:kube-scheduler

User  system:kube-scheduler

User  system:kube-proxy

User  system:node:fake

User  cityinthesky


kubectl describe clusterrolebindings admin-cluster-admin-binding
Name:         admin-cluster-admin-binding
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind  Name   Namespace
  ----  ----   ---------
  User  admin

kubectl describe clusterrolebindings system:kube-controller-manager
Name:         system:kube-controller-manager
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:kube-controller-manager
Subjects:
  Kind  Name                            Namespace
  ----  ----                            ---------
  User  system:kube-controller-manager

kubectl describe clusterrolebindings system:kube-scheduler
Name:         system:kube-scheduler
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:kube-scheduler
Subjects:
  Kind  Name                   Namespace
  ----  ----                   ---------
  User  system:kube-scheduler

kubectl describe clusterrolebindings system:volume-scheduler
Name:         system:volume-scheduler
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:volume-scheduler
Subjects:
  Kind  Name                   Namespace
  ----  ----                   ---------
  User  system:kube-scheduler

kubectl describe clusterrolebindings system:node-proxier
Name:         system:node-proxier
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:node-proxier
Subjects:
  Kind  Name               Namespace
  ----  ----               ---------
  User  system:kube-proxy

kubectl describe clusterrolebindings system:node
Name:         system:node
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:  ClusterRole
  Name:  system:node
Subjects:
  Kind  Name              Namespace
  ----  ----              ---------
  User  system:node:fake

kubectl describe clusterrolebindings cityinthesky-cluster-admin-binding
Name:         cityinthesky-cluster-admin-binding
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind  Name          Namespace
  ----  ----          ---------
  User  cityinthesky




```