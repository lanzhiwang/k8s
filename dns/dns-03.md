```bash
[root@k8s-master1 kubernetes]# bash deploy.sh 
+++ dirname deploy.sh
++ cd .
++ pwd
+ DIR=/opt/k8s/temp/dns/deployment/kubernetes
+ CLUSTER_DOMAIN=cluster.local
+ YAML_TEMPLATE=/opt/k8s/temp/dns/deployment/kubernetes/coredns.yaml.sed
+ STUBDOMAINS=
+ UPSTREAM='\/etc\/resolv.conf'
+ FEDERATIONS=
+ getopts hsr:i:d:t:k: opt
+ [[ -z '' ]]
+ REVERSE_CIDRS='in-addr.arpa ip6.arpa'
+ [[ -z '' ]]
++ kubectl get service --namespace kube-system kube-dns -o 'jsonpath={.spec.clusterIP}'
Error from server (NotFound): services "kube-dns" not found
+ CLUSTER_DNS_IP=
+ '[' 1 -ne 0 ']'
+ echo 'Error! The IP address for DNS service couldn'\''t be determined automatically. Please specify the DNS-IP with the '\''-i'\'' option.'
Error! The IP address for DNS service couldn't be determined automatically. Please specify the DNS-IP with the '-i' option.
+ exit 2
[root@k8s-master1 kubernetes]# 

##############################################################################

[root@k8s-master1 kubernetes]# bash deploy.sh -i 10.68.0.2
+++ dirname deploy.sh
++ cd .
++ pwd
+ DIR=/opt/k8s/temp/dns/deployment/kubernetes
+ CLUSTER_DOMAIN=cluster.local
+ YAML_TEMPLATE=/opt/k8s/temp/dns/deployment/kubernetes/coredns.yaml.sed
+ STUBDOMAINS=
+ UPSTREAM='\/etc\/resolv.conf'
+ FEDERATIONS=
+ getopts hsr:i:d:t:k: opt
+ case "$opt" in
+ CLUSTER_DNS_IP=10.68.0.2
+ getopts hsr:i:d:t:k: opt
+ [[ -z '' ]]
+ REVERSE_CIDRS='in-addr.arpa ip6.arpa'
+ [[ -z 10.68.0.2 ]]
+ [[ '' -ne 1 ]]
+ translate-kube-dns-configmap
+ kube-dns-federation-to-coredns
++ kubectl -n kube-system get configmap kube-dns '-ojsonpath={.data.federations}'
++ jq .
++ tr -d '":,'
+ fed=
+ [[ ! -z '' ]]
+ kube-dns-upstreamnameserver-to-coredns
++ kubectl -n kube-system get configmap kube-dns '-ojsonpath={.data.upstreamNameservers}'
++ tr -d '[",]'
+ up=
+ [[ ! -z '' ]]
+ kube-dns-stubdomains-to-coredns
+ STUBDOMAIN_TEMPLATE='
    SD_DOMAIN:53 {
      errors
      cache 30
      loop
      forward . SD_DESTINATION
    }'
++ kubectl -n kube-system get configmap kube-dns '-ojsonpath={.data.stubDomains}'
+ sd=
++ parse_stub_domains ''
++ sd=
+++ echo -n
+++ jq 'keys[]'
++ sd_keys=
+ STUBDOMAINS=
+ orig='
'
+ replace='\
'
+ sed -e s/CLUSTER_DNS_IP/10.68.0.2/g -e s/CLUSTER_DOMAIN/cluster.local/g -e 's?REVERSE_CIDRS?in-addr.arpa ip6.arpa?g' -e s@STUBDOMAINS@@g -e s@FEDERATIONS@@g -e 's/UPSTREAMNAMESERVER/\/etc\/resolv.conf/g' /opt/k8s/temp/dns/deployment/kubernetes/coredns.yaml.sed
apiVersion: v1
kind: ServiceAccount
metadata:
  name: coredns
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: system:coredns
rules:
- apiGroups:
  - ""
  resources:
  - endpoints
  - services
  - pods
  - namespaces
  verbs:
  - list
  - watch
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: system:coredns
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:coredns
subjects:
- kind: ServiceAccount
  name: coredns
  namespace: kube-system
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coredns
  namespace: kube-system
  labels:
    k8s-app: kube-dns
    kubernetes.io/name: "CoreDNS"
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  selector:
    matchLabels:
      k8s-app: kube-dns
  template:
    metadata:
      labels:
        k8s-app: kube-dns
    spec:
      priorityClassName: system-cluster-critical
      serviceAccountName: coredns
      tolerations:
        - key: "CriticalAddonsOnly"
          operator: "Exists"
      nodeSelector:
        beta.kubernetes.io/os: linux
      containers:
      - name: coredns
        image: coredns/coredns:1.5.0
        imagePullPolicy: IfNotPresent
        resources:
          limits:
            memory: 170Mi
          requests:
            cpu: 100m
            memory: 70Mi
        args: [ "-conf", "/etc/coredns/Corefile" ]
        volumeMounts:
        - name: config-volume
          mountPath: /etc/coredns
          readOnly: true
        ports:
        - containerPort: 53
          name: dns
          protocol: UDP
        - containerPort: 53
          name: dns-tcp
          protocol: TCP
        - containerPort: 9153
          name: metrics
          protocol: TCP
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            add:
            - NET_BIND_SERVICE
            drop:
            - all
          readOnlyRootFilesystem: true
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 60
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8181
            scheme: HTTP
      dnsPolicy: Default
      volumes:
        - name: config-volume
          configMap:
            name: coredns
            items:
            - key: Corefile
              path: Corefile
---
apiVersion: v1
kind: Service
metadata:
  name: kube-dns
  namespace: kube-system
  annotations:
    prometheus.io/port: "9153"
    prometheus.io/scrape: "true"
  labels:
    k8s-app: kube-dns
    kubernetes.io/cluster-service: "true"
    kubernetes.io/name: "CoreDNS"
spec:
  selector:
    k8s-app: kube-dns
  clusterIP: 10.68.0.2
  ports:
  - name: dns
    port: 53
    protocol: UDP
  - name: dns-tcp
    port: 53
    protocol: TCP
  - name: metrics
    port: 9153
    protocol: TCP
[root@k8s-master1 kubernetes]# 


##############################################################################












```