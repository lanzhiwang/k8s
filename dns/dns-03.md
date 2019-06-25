# deploy.sh 脚本注释

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

#!/bin/bash

set -x

# Deploys CoreDNS to a cluster currently running Kube-DNS.

show_help () {
cat << USAGE
usage: $0 [ -r REVERSE-CIDR ] [ -i DNS-IP ] [ -d CLUSTER-DOMAIN ] [ -t YAML-TEMPLATE ]

    -r : Define a reverse zone for the given CIDR. You may specifcy this option more
         than once to add multiple reverse zones. If no reverse CIDRs are defined,
         then the default is to handle all reverse zones (i.e. in-addr.arpa and ip6.arpa)
    -i : Specify the cluster DNS IP address. If not specificed, the IP address of
         the existing "kube-dns" service is used, if present.
    -s : Skips the translation of kube-dns configmap to the corresponding CoreDNS Corefile configuration.

USAGE
exit 0
}

# Simple Defaults
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"  # DIR=/opt/k8s/temp/dns/deployment/kubernetes
CLUSTER_DOMAIN=cluster.local  # CLUSTER_DOMAIN=cluster.local
YAML_TEMPLATE="$DIR/coredns.yaml.sed"  # YAML_TEMPLATE=/opt/k8s/temp/dns/deployment/kubernetes/coredns.yaml.sed
STUBDOMAINS=""  # STUBDOMAINS=
UPSTREAM=\\/etc\\/resolv\.conf  # UPSTREAM='\/etc\/resolv.conf'
FEDERATIONS=""  # FEDERATIONS=


# Translates the kube-dns ConfigMap to equivalent CoreDNS Configuration.
function translate-kube-dns-configmap {
    kube-dns-federation-to-coredns
    kube-dns-upstreamnameserver-to-coredns
    kube-dns-stubdomains-to-coredns
}

function kube-dns-federation-to-coredns {
  fed=$(kubectl -n kube-system get configmap kube-dns  -ojsonpath='{.data.federations}' 2> /dev/null | jq . | tr -d '":,')  # kubectl -n kube-system get configmap kube-dns '-ojsonpath={.data.federations}'
  if [[ ! -z ${fed} ]]; then
  FEDERATIONS=$(sed -e '1s/^/federation /' -e 's/^/        /' -e '1i\\' <<< "${fed}") # add federation to the stanza
  fi
}

function kube-dns-upstreamnameserver-to-coredns {
  up=$(kubectl -n kube-system get configmap kube-dns  -ojsonpath='{.data.upstreamNameservers}' 2> /dev/null | tr -d '[",]')  # kubectl -n kube-system get configmap kube-dns '-ojsonpath={.data.upstreamNameservers}'
  if [[ ! -z ${up} ]]; then
    UPSTREAM=${up}
  fi
}

function kube-dns-stubdomains-to-coredns {
  STUBDOMAIN_TEMPLATE='
    SD_DOMAIN:53 {
      errors
      cache 30
      loop
      forward . SD_DESTINATION
    }'

  function dequote {
    str=${1#\"} # delete leading quote
    str=${str%\"} # delete trailing quote
    echo ${str}
  }

  # parse_stub_domains ''
  function parse_stub_domains() {
    sd=$1

  # get keys - each key is a domain
  sd_keys=$(echo -n $sd | jq keys[])  # sd_keys=

  # For each domain ...
  for dom in $sd_keys; do
    dst=$(echo -n $sd | jq '.['$dom'][0]') # get the destination

    dom=$(dequote $dom)
    dst=$(dequote $dst)

    sd_stanza=${STUBDOMAIN_TEMPLATE/SD_DOMAIN/$dom} # replace SD_DOMAIN
    sd_stanza=${sd_stanza/SD_DESTINATION/$dst} # replace SD_DESTINATION
    echo "$sd_stanza"
  done
}

  sd=$(kubectl -n kube-system get configmap kube-dns  -ojsonpath='{.data.stubDomains}' 2> /dev/null)  # kubectl -n kube-system get configmap kube-dns '-ojsonpath={.data.stubDomains}'
  STUBDOMAINS=$(parse_stub_domains "$sd")  # STUBDOMAINS=
}


# Get Opts
while getopts "hsr:i:d:t:k:" opt; do
    case "$opt" in
    h)  show_help
        ;;
    s)  SKIP=1
        ;;
    r)  REVERSE_CIDRS="$REVERSE_CIDRS $OPTARG"
        ;;
    i)  CLUSTER_DNS_IP=$OPTARG  # CLUSTER_DNS_IP=10.68.0.2
        ;;
    d)  CLUSTER_DOMAIN=$OPTARG
        ;;
    t)  YAML_TEMPLATE=$OPTARG
        ;;
    esac
done

# Conditional Defaults
if [[ -z $REVERSE_CIDRS ]]; then
  REVERSE_CIDRS="in-addr.arpa ip6.arpa"  # REVERSE_CIDRS='in-addr.arpa ip6.arpa'
fi
if [[ -z $CLUSTER_DNS_IP ]]; then
  # Default IP to kube-dns IP
  CLUSTER_DNS_IP=$(kubectl get service --namespace kube-system kube-dns -o jsonpath="{.spec.clusterIP}")
  if [ $? -ne 0 ]; then
      >&2 echo "Error! The IP address for DNS service couldn't be determined automatically. Please specify the DNS-IP with the '-i' option."
      exit 2
  fi
fi

if [[ "${SKIP}" -ne 1 ]] ; then
    translate-kube-dns-configmap
fi

orig=$'\n'
replace=$'\\\n'
sed -e "s/CLUSTER_DNS_IP/$CLUSTER_DNS_IP/g" \
    -e "s/CLUSTER_DOMAIN/$CLUSTER_DOMAIN/g" \
    -e "s?REVERSE_CIDRS?$REVERSE_CIDRS?g" \
    -e "s@STUBDOMAINS@${STUBDOMAINS//$orig/$replace}@g" \
    -e "s@FEDERATIONS@${FEDERATIONS//$orig/$replace}@g" \
    -e "s/UPSTREAMNAMESERVER/$UPSTREAM/g" \
    "${YAML_TEMPLATE}"

# sed -e s/CLUSTER_DNS_IP/10.68.0.2/g -e s/CLUSTER_DOMAIN/cluster.local/g -e 's?REVERSE_CIDRS?in-addr.arpa ip6.arpa?g' -e s@STUBDOMAINS@@g -e s@FEDERATIONS@@g -e 's/UPSTREAMNAMESERVER/\/etc\/resolv.conf/g' /opt/k8s/temp/dns/deployment/kubernetes/coredns.yaml.sed



[root@k8s-master1 temp]# kubectl apply -f ./coredns.yaml
serviceaccount/coredns created
clusterrole.rbac.authorization.k8s.io/system:coredns created
clusterrolebinding.rbac.authorization.k8s.io/system:coredns created
configmap/coredns created
deployment.apps/coredns created
service/kube-dns created
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# kubectl run -i -t busybox-test --image=busybox --restart=Never sh
If you don't see a command prompt, try pressing enter.
/ # cat /etc/resolv.conf 
nameserver 10.68.0.2
search default.svc.cluster.local. svc.cluster.local. cluster.local. reddog.microsoft.com
options ndots:5
/ # 




```