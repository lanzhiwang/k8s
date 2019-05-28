```bash


ClusterRoleBinding
ClusterRole
RoleBinding
Role




[root@k8s-master1 ssl]# kubectl get ClusterRole -o wide
NAME                                                                   AGE
admin                                                                  7d1h
cluster-admin                                                          7d1h
edit                                                                   7d1h
flannel                                                                6d21h
system:aggregate-to-admin                                              7d1h
system:aggregate-to-edit                                               7d1h
system:aggregate-to-view                                               7d1h
system:auth-delegator                                                  7d1h
system:aws-cloud-provider                                              7d1h
system:basic-user                                                      7d1h
system:certificates.k8s.io:certificatesigningrequests:nodeclient       7d1h
system:certificates.k8s.io:certificatesigningrequests:selfnodeclient   7d1h
system:controller:attachdetach-controller                              7d1h
system:controller:certificate-controller                               7d1h
system:controller:clusterrole-aggregation-controller                   7d1h
system:controller:cronjob-controller                                   7d1h
system:controller:daemon-set-controller                                7d1h
system:controller:deployment-controller                                7d1h
system:controller:disruption-controller                                7d1h
system:controller:endpoint-controller                                  7d1h
system:controller:expand-controller                                    7d1h
system:controller:generic-garbage-collector                            7d1h
system:controller:horizontal-pod-autoscaler                            7d1h
system:controller:job-controller                                       7d1h
system:controller:namespace-controller                                 7d1h
system:controller:node-controller                                      7d1h
system:controller:persistent-volume-binder                             7d1h
system:controller:pod-garbage-collector                                7d1h
system:controller:pv-protection-controller                             7d1h
system:controller:pvc-protection-controller                            7d1h
system:controller:replicaset-controller                                7d1h
system:controller:replication-controller                               7d1h
system:controller:resourcequota-controller                             7d1h
system:controller:route-controller                                     7d1h
system:controller:service-account-controller                           7d1h
system:controller:service-controller                                   7d1h
system:controller:statefulset-controller                               7d1h
system:controller:ttl-controller                                       7d1h
system:csi-external-attacher                                           7d1h
system:csi-external-provisioner                                        7d1h
system:discovery                                                       7d1h
system:heapster                                                        7d1h
system:kube-aggregator                                                 7d1h
system:kube-controller-manager                                         7d1h
system:kube-dns                                                        7d1h
system:kube-scheduler                                                  7d1h
system:kubelet-api-admin                                               7d1h
system:node                                                            7d1h
system:node-bootstrapper                                               7d1h
system:node-problem-detector                                           7d1h
system:node-proxier                                                    7d1h
system:persistent-volume-provisioner                                   7d1h
system:public-info-viewer                                              7d1h
system:volume-scheduler                                                7d1h
view                                                                   7d1h
[root@k8s-master1 ssl]# 


[root@k8s-master1 ssl]# kubectl describe ClusterRole  admin
Name:         admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
PolicyRule:
  Resources                                       Non-Resource URLs  Resource Names  Verbs
  ---------                                       -----------------  --------------  -----
  rolebindings.rbac.authorization.k8s.io          []                 []              [create delete deletecollection get list patch update watch]
  roles.rbac.authorization.k8s.io                 []                 []              [create delete deletecollection get list patch update watch]
  configmaps                                      []                 []              [create delete deletecollection patch update get list watch]
  endpoints                                       []                 []              [create delete deletecollection patch update get list watch]
  persistentvolumeclaims                          []                 []              [create delete deletecollection patch update get list watch]
  pods                                            []                 []              [create delete deletecollection patch update get list watch]
  replicationcontrollers/scale                    []                 []              [create delete deletecollection patch update get list watch]
  replicationcontrollers                          []                 []              [create delete deletecollection patch update get list watch]
  services                                        []                 []              [create delete deletecollection patch update get list watch]
  daemonsets.apps                                 []                 []              [create delete deletecollection patch update get list watch]
  deployments.apps/scale                          []                 []              [create delete deletecollection patch update get list watch]
  deployments.apps                                []                 []              [create delete deletecollection patch update get list watch]
  replicasets.apps/scale                          []                 []              [create delete deletecollection patch update get list watch]
  replicasets.apps                                []                 []              [create delete deletecollection patch update get list watch]
  statefulsets.apps/scale                         []                 []              [create delete deletecollection patch update get list watch]
  statefulsets.apps                               []                 []              [create delete deletecollection patch update get list watch]
  horizontalpodautoscalers.autoscaling            []                 []              [create delete deletecollection patch update get list watch]
  cronjobs.batch                                  []                 []              [create delete deletecollection patch update get list watch]
  jobs.batch                                      []                 []              [create delete deletecollection patch update get list watch]
  daemonsets.extensions                           []                 []              [create delete deletecollection patch update get list watch]
  deployments.extensions/scale                    []                 []              [create delete deletecollection patch update get list watch]
  deployments.extensions                          []                 []              [create delete deletecollection patch update get list watch]
  ingresses.extensions                            []                 []              [create delete deletecollection patch update get list watch]
  networkpolicies.extensions                      []                 []              [create delete deletecollection patch update get list watch]
  replicasets.extensions/scale                    []                 []              [create delete deletecollection patch update get list watch]
  replicasets.extensions                          []                 []              [create delete deletecollection patch update get list watch]
  replicationcontrollers.extensions/scale         []                 []              [create delete deletecollection patch update get list watch]
  ingresses.networking.k8s.io                     []                 []              [create delete deletecollection patch update get list watch]
  networkpolicies.networking.k8s.io               []                 []              [create delete deletecollection patch update get list watch]
  poddisruptionbudgets.policy                     []                 []              [create delete deletecollection patch update get list watch]
  deployments.apps/rollback                       []                 []              [create delete deletecollection patch update]
  deployments.extensions/rollback                 []                 []              [create delete deletecollection patch update]
  localsubjectaccessreviews.authorization.k8s.io  []                 []              [create]
  pods/attach                                     []                 []              [get list watch create delete deletecollection patch update]
  pods/exec                                       []                 []              [get list watch create delete deletecollection patch update]
  pods/portforward                                []                 []              [get list watch create delete deletecollection patch update]
  pods/proxy                                      []                 []              [get list watch create delete deletecollection patch update]
  secrets                                         []                 []              [get list watch create delete deletecollection patch update]
  services/proxy                                  []                 []              [get list watch create delete deletecollection patch update]
  bindings                                        []                 []              [get list watch]
  events                                          []                 []              [get list watch]
  limitranges                                     []                 []              [get list watch]
  namespaces/status                               []                 []              [get list watch]
  namespaces                                      []                 []              [get list watch]
  pods/log                                        []                 []              [get list watch]
  pods/status                                     []                 []              [get list watch]
  replicationcontrollers/status                   []                 []              [get list watch]
  resourcequotas/status                           []                 []              [get list watch]
  resourcequotas                                  []                 []              [get list watch]
  controllerrevisions.apps                        []                 []              [get list watch]
  serviceaccounts                                 []                 []              [impersonate create delete deletecollection patch update get list watch]
[root@k8s-master1 ssl]# 

[root@k8s-master1 ssl]# kubectl describe ClusterRole  cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  *.*        []                 []              [*]
             [*]                []              [*]
[root@k8s-master1 ssl]# 






[root@k8s-master1 ssl]# kubectl get ClusterRoleBinding  -o wide
NAME                                                   AGE     ROLE                                                               USERS                            GROUPS                                         SERVICEACCOUNTS
cluster-admin                                          7d1h    ClusterRole/cluster-admin                                                                           system:masters                                 
flannel                                                6d21h   ClusterRole/flannel                                                                                                                                kube-system/flannel
system:aws-cloud-provider                              7d1h    ClusterRole/system:aws-cloud-provider                                                                                                              kube-system/aws-cloud-provider
system:basic-user                                      7d1h    ClusterRole/system:basic-user                                                                       system:authenticated                           
system:controller:attachdetach-controller              7d1h    ClusterRole/system:controller:attachdetach-controller                                                                                              kube-system/attachdetach-controller
system:controller:certificate-controller               7d1h    ClusterRole/system:controller:certificate-controller                                                                                               kube-system/certificate-controller
system:controller:clusterrole-aggregation-controller   7d1h    ClusterRole/system:controller:clusterrole-aggregation-controller                                                                                   kube-system/clusterrole-aggregation-controller
system:controller:cronjob-controller                   7d1h    ClusterRole/system:controller:cronjob-controller                                                                                                   kube-system/cronjob-controller
system:controller:daemon-set-controller                7d1h    ClusterRole/system:controller:daemon-set-controller                                                                                                kube-system/daemon-set-controller
system:controller:deployment-controller                7d1h    ClusterRole/system:controller:deployment-controller                                                                                                kube-system/deployment-controller
system:controller:disruption-controller                7d1h    ClusterRole/system:controller:disruption-controller                                                                                                kube-system/disruption-controller
system:controller:endpoint-controller                  7d1h    ClusterRole/system:controller:endpoint-controller                                                                                                  kube-system/endpoint-controller
system:controller:expand-controller                    7d1h    ClusterRole/system:controller:expand-controller                                                                                                    kube-system/expand-controller
system:controller:generic-garbage-collector            7d1h    ClusterRole/system:controller:generic-garbage-collector                                                                                            kube-system/generic-garbage-collector
system:controller:horizontal-pod-autoscaler            7d1h    ClusterRole/system:controller:horizontal-pod-autoscaler                                                                                            kube-system/horizontal-pod-autoscaler
system:controller:job-controller                       7d1h    ClusterRole/system:controller:job-controller                                                                                                       kube-system/job-controller
system:controller:namespace-controller                 7d1h    ClusterRole/system:controller:namespace-controller                                                                                                 kube-system/namespace-controller
system:controller:node-controller                      7d1h    ClusterRole/system:controller:node-controller                                                                                                      kube-system/node-controller
system:controller:persistent-volume-binder             7d1h    ClusterRole/system:controller:persistent-volume-binder                                                                                             kube-system/persistent-volume-binder
system:controller:pod-garbage-collector                7d1h    ClusterRole/system:controller:pod-garbage-collector                                                                                                kube-system/pod-garbage-collector
system:controller:pv-protection-controller             7d1h    ClusterRole/system:controller:pv-protection-controller                                                                                             kube-system/pv-protection-controller
system:controller:pvc-protection-controller            7d1h    ClusterRole/system:controller:pvc-protection-controller                                                                                            kube-system/pvc-protection-controller
system:controller:replicaset-controller                7d1h    ClusterRole/system:controller:replicaset-controller                                                                                                kube-system/replicaset-controller
system:controller:replication-controller               7d1h    ClusterRole/system:controller:replication-controller                                                                                               kube-system/replication-controller
system:controller:resourcequota-controller             7d1h    ClusterRole/system:controller:resourcequota-controller                                                                                             kube-system/resourcequota-controller
system:controller:route-controller                     7d1h    ClusterRole/system:controller:route-controller                                                                                                     kube-system/route-controller
system:controller:service-account-controller           7d1h    ClusterRole/system:controller:service-account-controller                                                                                           kube-system/service-account-controller
system:controller:service-controller                   7d1h    ClusterRole/system:controller:service-controller                                                                                                   kube-system/service-controller
system:controller:statefulset-controller               7d1h    ClusterRole/system:controller:statefulset-controller                                                                                               kube-system/statefulset-controller
system:controller:ttl-controller                       7d1h    ClusterRole/system:controller:ttl-controller                                                                                                       kube-system/ttl-controller
system:discovery                                       7d1h    ClusterRole/system:discovery                                                                        system:authenticated                           
system:kube-controller-manager                         7d1h    ClusterRole/system:kube-controller-manager                         system:kube-controller-manager                                                  
system:kube-dns                                        7d1h    ClusterRole/system:kube-dns                                                                                                                        kube-system/kube-dns
system:kube-scheduler                                  7d1h    ClusterRole/system:kube-scheduler                                  system:kube-scheduler                                                           
system:node                                            7d1h    ClusterRole/system:node                                                                                                                            
system:node-proxier                                    7d1h    ClusterRole/system:node-proxier                                    system:kube-proxy                                                               
system:public-info-viewer                              7d1h    ClusterRole/system:public-info-viewer                                                               system:authenticated, system:unauthenticated   
system:volume-scheduler                                7d1h    ClusterRole/system:volume-scheduler                                system:kube-scheduler                                                           
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl describe ClusterRoleBinding  cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind   Name            Namespace
  ----   ----            ---------
  Group  system:masters  
[root@k8s-master1 ssl]# 



[root@k8s-master1 ssl]# kubectl get ServiceAccount --all-namespaces -o wide
NAMESPACE         NAME                   SECRETS   AGE
default           default                1         7d
kube-node-lease   default                1         7d
kube-public       default                1         7d
kube-system       default                1         7d
kube-system       flannel                1         6d21h
kube-system       kubernetes-dashboard   1         6d21h
[root@k8s-master1 ssl]# 


[root@k8s-master1 ssl]# kubectl describe ServiceAccount default  -n kube-system  
Name:                default
Namespace:           kube-system
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   default-token-w8zxk
Tokens:              default-token-w8zxk
Events:              <none>
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl describe ServiceAccount flannel  -n kube-system  
Name:                flannel
Namespace:           kube-system
Labels:              <none>
Annotations:         kubectl.kubernetes.io/last-applied-configuration:
                       {"apiVersion":"v1","kind":"ServiceAccount","metadata":{"annotations":{},"name":"flannel","namespace":"kube-system"}}
Image pull secrets:  <none>
Mountable secrets:   flannel-token-4f2g9
Tokens:              flannel-token-4f2g9
Events:              <none>
[root@k8s-master1 ssl]# 

[root@k8s-master1 ssl]# kubectl describe secrets  default-token-w8zxk  -n kube-system  
Name:         default-token-w8zxk
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: default
              kubernetes.io/service-account.uid: 854e0b8f-7ba1-11e9-8eb2-0017fa00a076

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1371 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkZWZhdWx0LXRva2VuLXc4enhrIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImRlZmF1bHQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI4NTRlMGI4Zi03YmExLTExZTktOGViMi0wMDE3ZmEwMGEwNzYiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06ZGVmYXVsdCJ9.Zd8GD2Q73mYOQkKcgg1YYeJ6y-fhrfFungacB0Aoh_9liBURpGiLSobYP_cVu-XtEg7tVjnmiOqIq4JElKWvSfaNJIUazQBkR5BMfhznhrYYBE3ypc7wmv6px3hX6cTo5fVRT65tMgUq71u7hDLAIAR1jYuYIEvw6DNaRrcT4CByp93sXTGk89EQFNQhYhEv5CBIDkpaE5MT2AdUDs_7oWRXpCuDNZgXEdKA9d-wa0UJorY0iN4rsGvTQ4DZ4Sb3lwlFhuWuxg9P8yqTKDN_P6Cw_uj7uGB_eotahID-wjVny4tz4YW0uXfRwGYIbEWQjT4-9yYzgi_1Pv02sfpNCQ
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# 



[root@k8s-master1 ssl]# kubectl get secrets --all-namespaces -o wide
NAMESPACE         NAME                               TYPE                                  DATA   AGE
default           default-token-lz2dc                kubernetes.io/service-account-token   3      7d1h
kube-node-lease   default-token-wr6r8                kubernetes.io/service-account-token   3      7d1h
kube-public       default-token-l9mvf                kubernetes.io/service-account-token   3      7d1h
kube-system       default-token-w8zxk                kubernetes.io/service-account-token   3      7d1h
kube-system       flannel-token-4f2g9                kubernetes.io/service-account-token   3      6d21h
kube-system       kubernetes-dashboard-certs         Opaque                                0      97m
kube-system       kubernetes-dashboard-csrf          Opaque                                1      6d21h
kube-system       kubernetes-dashboard-key-holder    Opaque                                2      6d19h
kube-system       kubernetes-dashboard-token-w6fdt   kubernetes.io/service-account-token   3      6d21h
[root@k8s-master1 ssl]# 























```