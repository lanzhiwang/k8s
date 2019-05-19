## 工作节点准备工作

### 工作节点执行下列操作

1. 下载所有用到的二进制文件，docker 镜像等
2. 生成 CA 证书、私钥、请求文件、配置文件
3. 为客户端 kubectl 创建 kubeconfig 文件 /root/.kube/config
	* 准备 kubectl 使用的 admin 证书签名请求
	* 创建 admin 证书与私钥
	* 设置集群参数，指定 CA 证书和 apiserver 地址
	* 设置客户端 kubectl 认证参数，指定使用 admin 证书和私钥
	* 设置上下文参数，说明使用 cluster 集群和用户 admin
	* 选择默认上下文

4. 为 kube-proxy 创建 kube-proxy.kubeconfig 配置文件 /root/kube-proxy.kubeconfig
	* 准备 kube-proxy 证书签名请求
	* 创建 kube-proxy 证书与私钥
	* 设置集群参数
	* 设置 kube-proxy 认证参数
	* 设置上下文参数
	* 选择默认上下文

### 相关操作的命令如下

```bash
# 建立相关目录
mkdir -p /opt/kube/bin/ /etc/kubernetes/ssl/ /etc/ansible/ /etc/kubernetes

# 事先已经将相关文件下载到 /etc/ansible 目录中
# 下载证书工具 cfssl 和 kubectl
cp /etc/ansible/bin/{cfssl, cfssl-certinfo, cfssljson, kubectl} /opt/kube/bin/

##### 生成 CA 证书、私钥、请求文件、配置文件 #####

# 准备 CA 配置文件
cat /etc/kubernetes/ssl/ca-config.json
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "kubernetes": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      }
    }
  }
}

# 准备 CA 签名请求文件，CA 证书请求文件有 ca 字段，其他的请求文件没有该字段
cat /etc/kubernetes/ssl/ca-csr.json
{
  "CN": "www.antiy.com/emailAddress=huzhi@antiy.cn",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "wuhanantiy",
      "OU": "Technical Support"
    }
  ],
  "ca": {
    "expiry": "131400h"
  }
}

# 生成 CA 证书和私钥
cd /etc/kubernetes/ssl && /opt/kube/bin/cfssl gencert -initca ca-csr.json | /opt/kube/bin/cfssljson -bare ca

ca.csr  # CA 证书请求文件
ca-key.pem  # CA 私钥
ca.pem  # CA 证书



##### 为客户端 kubectl 创建 kubeconfig 文件 /root/.kube/config #####

# 准备 kubectl 使用的 admin 证书签名请求
cat /etc/kubernetes/ssl/admin-csr.json
{
  "CN": "www.antiy.com/emailAddress=admin@antiy.cn",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "wuhanantiy",
      "OU": "Technical Support"
    }
  ]
}

# 创建 admin 证书与私钥
cd /etc/kubernetes/ssl && /opt/kube/bin/cfssl gencert \
        -ca=/etc/kubernetes/ssl/ca.pem \
        -ca-key=/etc/kubernetes/ssl/ca-key.pem \
        -config=/etc/kubernetes/ssl/ca-config.json \
        -profile=kubernetes admin-csr.json | /opt/kube/bin/cfssljson -bare admin

admin.csr  # admin 证书请求文件
admin-csr.json
admin-key.pem  # admin 私钥
admin.pem  # admin 证书


# 为 kubectl 设置集群参数，指定 CA 证书和 apiserver 地址
/opt/kube/bin/kubectl config set-cluster kubernetes \
        --certificate-authority=/etc/kubernetes/ssl/ca.pem \
        --embed-certs=true \
        --server=https://192.168.1.12:8443

$ cat ~/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: k1JSUVLakNDQXhLZ0F3SUJBZ0lVUlE5MHZyOHUvZkNLZTd
    server: https://192.168.1.12:8443
  name: kubernetes
contexts: []
current-context: ""
kind: Config
preferences: {}
users: []
$


# 设置客户端 kubectl 认证参数，指定使用 admin 证书和私钥
/opt/kube/bin/kubectl config set-credentials admin \
        --client-certificate=/etc/kubernetes/ssl/admin.pem \
        --embed-certs=true \
        --client-key=/etc/kubernetes/ssl/admin-key.pem

$ cat ~/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: k1JSUVLakNDQXhLZ0F3SUJBZ0lVUlE5MHZyOHUvZkNLZTd
    server: https://192.168.1.12:8443
  name: kubernetes
contexts: []
current-context: ""
kind: Config
preferences: {}
users:
- name: admin
  user:
    client-certificate-data: 0tCk1JSUVRekNDQXl1Z0F3SUJBZ0lVZDcxVDl2anl4ZXIyK3p
    client-key-data: LRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBeEErZHpObkEwZnZYQkF
$


# 设置上下文参数，说明使用 cluster 集群和用户 admin
/opt/kube/bin/kubectl config set-context kubernetes \
        --cluster=kubernetes --user=admin

$ cat ~/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: k1JSUVLakNDQXhLZ0F3SUJBZ0lVUlE5MHZyOHUvZkNLZTd
    server: https://192.168.1.12:8443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: admin
  name: kubernetes
current-context: ""
kind: Config
preferences: {}
users:
- name: admin
  user:
    client-certificate-data: 0tCk1JSUVRekNDQXl1Z0F3SUJBZ0lVZDcxVDl2anl4ZXIyK3p
    client-key-data: LRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBeEErZHpObkEwZnZYQkF
$


# 选择默认上下文
/opt/kube/bin/kubectl config use-context kubernetes

[root@lanzhiwang-centos7 k8s]# cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: k1JSUVLakNDQXhLZ0F3SUJBZ0lVUlE5MHZyOHUvZkNLZTd
    server: https://192.168.1.12:8443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: admin
  name: kubernetes
current-context: kubernetes
kind: Config
preferences: {}
users:
- name: admin
  user:
    client-certificate-data: 0tCk1JSUVRekNDQXl1Z0F3SUJBZ0lVZDcxVDl2anl4ZXIyK3p
    client-key-data: LRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBeEErZHpObkEwZnZYQkF
$



##### 为 kube-proxy 创建 kube-proxy.kubeconfig 配置文件 /root/kube-proxy.kubeconfig #####

# 准备 kube-proxy 证书签名请求
cat /etc/kubernetes/ssl/kube-proxy-csr.json
{
  "CN": "www.antiy.com/emailAddress=kube-procy@antiy.cn",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "wuhanantiy",
      "OU": "Technical Support"
    }
  ]
}

# 创建 kube-proxy 证书与私钥
cd /etc/kubernetes/ssl && /opt/kube/bin/cfssl gencert \
        -ca=/etc/kubernetes/ssl/ca.pem \
        -ca-key=/etc/kubernetes/ssl/ca-key.pem \
        -config=/etc/kubernetes/ssl/ca-config.json \
        -profile=kubernetes kube-proxy-csr.json | /opt/kube/bin/cfssljson -bare kube-proxy

# 为 kube-proxy 设置集群参数，参数保存到 kube-proxy.kubeconfig 文件中
/opt/kube/bin/kubectl config set-cluster kubernetes \
        --certificate-authority=/etc/kubernetes/ssl/ca.pem \
        --embed-certs=true \
        --server=https://192.168.1.12:8443 \
        --kubeconfig=./kube-proxy.kubeconfig

# 设置 kube-proxy 认证参数
/opt/kube/bin/kubectl config set-credentials kube-proxy \
        --client-certificate=/etc/kubernetes/ssl/kube-proxy.pem \
        --client-key=/etc/kubernetes/ssl/kube-proxy-key.pem \
        --embed-certs=true \
        --kubeconfig=./kube-proxy.kubeconfig

# 设置上下文参数
/opt/kube/bin/kubectl config set-context default \
        --cluster=kubernetes \
        --user=kube-proxy \
        --kubeconfig=./kube-proxy.kubeconfig

# 选择默认上下文
/opt/kube/bin/kubectl config use-context default --kubeconfig=./kube-proxy.kubeconfig

# 移动 kube-proxy.kubeconfig
mv ./kube-proxy.kubeconfig /etc/kubernetes/

```


