# Configure RBAC In Your Kubernetes Cluster

## Introduction

This guide will go through the basic Kubernetes Role-Based Access Control (RBAC) API Objects, together with two common use cases (create a user with limited access, and enable Helm). At the end of this guide, you should have enough knowledge to implement RBAC policies in your cluster. The examples here described were tested in Minikube, but they can be applied to any Kubernetes cluster.  本指南将介绍基本的Kubernetes基于角色的访问控制（RBAC）API对象，以及两个常见用例（创建具有有限访问权限的用户，并启用Helm）。 在本指南的最后，您应该有足够的知识在集群中实施RBAC策略。 这里描述的示例在Minikube中进行了测试，但它们可以应用于任何Kubernetes集群。

From Kubernetes 1.6 onwards, RBAC policies are enabled by default. RBAC policies are vital for the correct management of your cluster, as they allow you to specify which types of actions are permitted depending on the user and their role in your organization. Examples include:  从Kubernetes 1.6开始，默认情况下启用RBAC策略。 RBAC策略对于正确管理群集至关重要，因为它们允许您根据用户及其在组织中的角色指定允许的操作类型。 例子包括：

* Secure your cluster by granting privileged operations (accessing secrets, for example) only to admin users.

* Force user authentication in your cluster.

* Limit resource creation (such as pods, persistent volumes, deployments) to specific namespaces. You can also use quotas to ensure that resource usage is limited and under control.

* Have a user only see resources in their authorized namespace. This allows you to isolate resources within your organization (for example, between departments).

As a consequence of having RBAC enabled by default, you may have found errors like this when configuring network overlays (such as flanneld) or making Helm work in your cluster:  由于默认情况下启用了RBAC，因此在配置网络覆盖（例如flanneld）或使Helm在群集中工作时，您可能会发现这样的错误：

```
the server does not allow access to the requested resource
```

This guide will show you how to work with RBAC so you can properly deal with issues like these.

## Prerequisites And Assumptions

This guide makes the following assumptions:

* You have Minikube installed on your local computer with RBAC enabled:

```bash
minikube start --extra-config=apiserver.Authorization.Mode=RBAC
```

* You have a Kubernetes cluster running.

* You have the kubectl command line (kubectl CLI) installed.

* You have Helm and Tiller installed.

* You have intermediate level of understanding of how Kubernetes works, and its core resources and operations. You are expected to be familiar with concepts like:

  * Pods
  * Deployments
  * Namespaces
  * Secrets
  * Replicasets
  * PersistentVolumes
  * ConfigMaps
  * Nodes

* You have OpenSSL installed locally.

## RBAC API Objects

One basic Kubernetes feature is that all its resources are modeled API objects, which allow CRUD (Create, Read, Update, Delete) operations. Examples of resources are:

* Pods.
* PersistentVolumes.
* ConfigMaps.
* Deployments.
* Nodes.
* Secrets.
* Namespaces.
* 
Examples of possible operations over these resources are:

* create
* get
* delete
* list
* update
* edit
* watch
* exec

At a higher level, resources are associated with API Groups (for example, Pods belong to the core API group whereas Deployments belong to the apps API group). For more information about all available resources, operations, and API groups, check the Official Kubernetes API Reference.

To manage RBAC in Kubernetes, apart from resources and operations, we need the following elements:  要管理Kubernetes中的RBAC，除资源和运营外，我们还需要以下要素：

* Rules: A rule is a set of operations (verbs) that can be carried out on a group of resources which belong to different API Groups.

* Roles and ClusterRoles: Both consist of rules. The difference between a Role and a ClusterRole is the scope: in a Role, the rules are applicable to a single namespace, whereas a ClusterRole is cluster-wide, so the rules are applicable to more than one namespace. ClusterRoles can define rules for cluster-scoped resources (such as nodes) as well. Both Roles and ClusterRoles are mapped as API Resources inside our cluster.

* Subjects: These correspond to the entity that attempts an operation in the cluster. There are three types of subjects:

	* User Accounts: These are global, and meant for humans or processes living outside the cluster. There is no associated resource API Object in the Kubernetes cluster.

	* Service Accounts: This kind of account is namespaced and meant for intra-cluster processes running inside pods, which want to authenticate against the API.

	* Groups: This is used for referring to multiple accounts. There are some groups created by default such as cluster-admin (explained in later sections).

* RoleBindings and ClusterRoleBindings: Just as the names imply, these bind subjects to roles (i.e. the operations a given user can perform). As for Roles and ClusterRoles, the difference lies in the scope: a RoleBinding will make the rules effective inside a namespace, whereas a ClusterRoleBinding will make the rules effective in all namespaces.

You can find examples of each API element in the Kubernetes official documentation.


## Use Case 1: Create User With Limited Namespace Access

In this example, we will create the following User Account:

* Username: employee
* Group: bitnami

We will add the necessary RBAC policies so this user can fully manage deployments (i.e. use kubectl run command) only inside the office namespace. At the end, we will test the policies to make sure they work as expected.

### Step 1: Create The Office Namespace

Execute the kubectl create command to create the namespace (as the admin user):

```bash
kubectl create namespace office
```

### Step 2: Create The User Credentials 证书

As previously mentioned, Kubernetes does not have API Objects for User Accounts. Of the available ways to manage authentication (see Kubernetes official documentation for a complete list), we will use OpenSSL certificates for their simplicity. The necessary steps are:  如前所述，Kubernetes没有用户帐户的API对象。 在管理身份验证的可用方法中（有关完整列表，请参阅Kubernetes官方文档），我们将使用OpenSSL证书来简化它们。 必要的步骤是：

* Create a private key for your user. In this example, we will name the file employee.key:

```bash
openssl genrsa -out employee.key 2048
```

* Create a certificate sign request employee.csr using the private key you just created (employee.key in this example). Make sure you specify your username and group in the -subj section (**CN is for the username and O for the group**). As previously mentioned, we will use employee as the name and bitnami as the group:

```bash
openssl req -new -key employee.key -out employee.csr -subj "/CN=employee/O=bitnami"
```

* Locate your Kubernetes cluster certificate authority (CA). This will be responsible for approving the request and generating the necessary certificate to access the cluster API. Its location is normally /etc/kubernetes/pki/. In the case of Minikube, it would be ~/.minikube/. Check that the files ca.crt and ca.key exist in the location.

* Generate the final certificate employee.crt by approving the certificate sign request, employee.csr, you made earlier. Make sure you substitute the CA_LOCATION placeholder with the location of your cluster CA. In this example, the certificate will be valid for 500 days:

```bash
openssl x509 -req -in employee.csr -CA CA_LOCATION/ca.crt -CAkey CA_LOCATION/ca.key -CAcreateserial -out employee.crt -days 500
```

* Save both employee.crt and employee.key in a safe location (in this example we will use /home/employee/.certs/).

* Add a new context with the new credentials for your Kubernetes cluster. This example is for a Minikube cluster but it should be similar for others:

```bash
kubectl config set-credentials employee --client-certificate=/home/employee/.certs/employee.crt  --client-key=/home/employee/.certs/employee.key

kubectl config set-context employee-context --cluster=minikube --namespace=office --user=employee
```

Now you should get an access denied error when using the kubectl CLI with this configuration file. This is expected as we have not defined any permitted operations for this user.

```bash
kubectl --context=employee-context get pods
```

### Step 3: Create The Role For Managing Deployments

* Create a role-deployment-manager.yaml file with the content below. In this yaml file we are creating the rule that allows a user to execute several operations on Deployments, Pods and ReplicaSets (necessary for creating a Deployment), which belong to the core (expressed by “” in the yaml file), apps, and extensions API Groups:

```
kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  namespace: office
  name: deployment-manager
rules:
- apiGroups: ["", "extensions", "apps"]
  resources: ["deployments", "replicasets", "pods"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"] # You can also use ["*"]
```

* Create the Role in the cluster using the kubectl create role command:

```basn
kubectl create -f role-deployment-manager.yaml
```

### Step 4: Bind The Role To The Employee User

* Create a rolebinding-deployment-manager.yaml file with the content below. In this file, we are binding the deployment-manager Role to the User Account employee inside the office namespace:

```
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: deployment-manager-binding
  namespace: office
subjects:
- kind: User
  name: employee
  apiGroup: ""
roleRef:
  kind: Role
  name: deployment-manager
  apiGroup: ""
```

* Deploy the RoleBinding by running the kubectl create command:

```bash
kubectl create -f rolebinding-deployment-manager.yaml
```

### Step 5: Test The RBAC Rule

Now you should be able to execute the following commands without any issues:

```bash
kubectl --context=employee-context run --image bitnami/dokuwiki mydokuwiki
kubectl --context=employee-context get pods
```

If you run the same command with the --namespace=default argument, it will fail, as the employee user does not have access to this namespace.

```bash
kubectl --context=employee-context get pods --namespace=default
```

Now you have created a user with limited permissions in your cluster.

## Use Case 2: Enable Helm In Your Cluster

> NOTE: This guide assumes that you have Helm installed in your cluster. Check this link for instructions.

Helm comprises of two parts: a client and a server (Tiller) inside the kube-system namespace. Tiller runs inside your Kubernetes cluster, and manages releases (installations) of your charts. To be able to do this, Tiller needs access to the Kubernetes API. By default, RBAC policies will not allow Tiller to carry out these operations, so we need to do the following:

* Create a Service Account tiller for the Tiller server (in the kube-system namespace). As we mentioned before, Service Accounts are meant for intra-cluster processes running in Pods.

* Bind the cluster-admin ClusterRole to this Service Account. We will use ClusterRoleBindings as we want it to be applicable in all namespaces. The reason is that we want Tiller to manage resources in all namespaces.

* Update the existing Tiller deployment (tiller-deploy) to associate its pod with the Service Account tiller.

The cluster-admin ClusterRole exists by default in your Kubernetes cluster, and allows superuser operations in all of the cluster resources. The reason for binding this role is because with Helm charts, you can have deployments consisting of a wide variety of Kubernetes resources. For instance:

* Pods.
* PersistentVolumes.
* ConfigMaps.
* Deployments.
* Secrets.
* Namespaces.
* Replicasets,
* Roles.
* RoleBindings.

So to make Helm compatible with any existing chart, binding the cluster-admin to the tiller Service Account is the best option. However, if you plan to use a very specific type of Helm chart (for example, one that only creates ConfigMaps, Pods, PersistentVolumes and Secrets), you could create more restrictive RBAC rules.

### Step 1: Create The Tiller Service Account

Create a tiller-serviceaccount.yaml file using kubectl:

```bash
kubectl create serviceaccount tiller --namespace kube-system
```

### Step 2: Bind The Tiller Service Account To The Cluster-Admin Role

* Create a tiller-clusterrolebinding.yaml file with the following contents:

```
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: tiller-clusterrolebinding
subjects:
- kind: ServiceAccount
  name: tiller
  namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: ""
```

* Deploy the ClusterRoleBinding:

```bash
kubectl create -f tiller-clusterrolebinding.yaml
```

### Step 3: Update The Existing Tiller Deployment

* Update the existing tiller-deploy deployment with the Service Account you created earlier:

```bash
helm init --service-account tiller --upgrade
```

* Wait a few seconds for the Tiller server to be redeployed.

### Step 4: Test The New Helm RBAC Rules

* All being well, you should be able to execute this command without errors:

```bash
helm ls
```

And that’s it! You have configured Helm RBAC rules in your Kubernetes cluster.


## Useful Links

* https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/
