# Kubernetes 默认认证和授权机制

## 默认集群角色绑定

| ClusterRoleBindings                | ClusterRole                             | Subjects                                                    |
| ---------------------------------- | --------------------------------------- | ----------------------------------------------------------- |
| admin-cluster-admin-binding        | cluster-admin                           | User  admin                                                 |
| system:kube-controller-manager     | system:kube-controller-manager          | User  system:kube-controller-manager                        |
| system:kube-scheduler              | system:kube-scheduler                   | User  system:kube-scheduler                                 |
| system:volume-scheduler            | system:volume-scheduler                 | User  system:kube-scheduler                                 |
| system:node-proxier                | system:node-proxier                     | User  system:kube-proxy                                     |
| system:node                        | system:node                             | User  system:node:fake                                      |
| cityinthesky-cluster-admin-binding | cluster-admin                           | User  cityinthesky                                          |
| cluster-admin                      | cluster-admin                           | Group  system:masters                                       |
| system:basic-user                  | system:basic-user                       | Group system:authenticated<br/>Group system:unauthenticated |
| system:discovery                   | system:discovery                        | Group system:authenticated<br/>Group system:unauthenticated |
| system:controller:node-controller  | system:controller:deployment-controller | ServiceAccount  deployment-controller                       |

## 默认角色绑定

| RoleBindings                                   | Role                                           | Subjects                                |
| ---------------------------------------------- | ---------------------------------------------- | --------------------------------------- |
| system:controller:bootstrap-signer             | system:controller:bootstrap-signer             | ServiceAccount  bootstrap-signer        |
| system::leader-locking-kube-controller-manager | system::leader-locking-kube-controller-manager | ServiceAccount  kube-controller-manager |
| system::leader-locking-kube-scheduler          | system::leader-locking-kube-scheduler          | ServiceAccount  kube-scheduler          |
| system:controller:bootstrap-signer             | system:controller:bootstrap-signer             | ServiceAccount  bootstrap-signer        |
| system:controller:cloud-provider               | system:controller:cloud-provider               | ServiceAccount  cloud-provider          |
| system:controller:token-cleaner                | system:controller:token-cleaner                | ServiceAccount  token-cleaner           |

ps:

**Kubernetes 没有相应的 API 创建 user 和 group，也就是 kubernetes 只存在默认的 user 和 group。**