## k8s install

[kubernetes高可用架构](https://blog.csdn.net/sinat_35930259/article/details/80411878)


### 相关配置

```
# 集群网络插件，可以支持calico, flannel, kube-router, cilium
CLUSTER_NETWORK="flannel"

# 服务网段 (Service CIDR），注意不要与内网已有网段冲突
SERVICE_CIDR="10.68.0.0/16"

# kubernetes 服务 IP (预分配，一般是 SERVICE_CIDR 中第一个IP)
CLUSTER_KUBERNETES_SVC_IP="10.68.0.1"

# 集群 DNS 服务 IP (从 SERVICE_CIDR 中预分配)
CLUSTER_DNS_SVC_IP="10.68.0.2"

# POD 网段 (Cluster CIDR），注意不要与内网已有网段冲突
CLUSTER_CIDR="172.20.0.0/16"

# 服务端口范围 (NodePort Range)
NODE_PORT_RANGE="20000-40000"

# 集群 DNS 域名
CLUSTER_DNS_DOMAIN="cluster.local."

# 需要说明的是集群的 apiserver 地址应该是负载均衡的地址
# MASTER_IP 为负载均衡主节点地址
# MASTER_IP="192.168.1.12"
# KUBE_APISERVER="https://192.168.1.12:8443"

MASTER_IP="10.1.36.43"
KUBE_APISERVER="https://10.1.36.43:6443"


# 集群 basic auth 使用的用户名和密码，用于 basic-auth.csv
BASIC_AUTH_USER="admin"
BASIC_AUTH_PASS="admin"
```

### 相关文件下载

```bash

# 整个工作目录
[root@k8s-master1 temp]# pwd
/opt/k8s/temp
[root@k8s-master1 temp]# 


# k8s 暂时通过公司的 VPN 服务器下载，flannel 镜像可以直接下载
$ wget https://dl.k8s.io/v1.14.0/kubernetes-server-linux-amd64.tar.gz
[root@k8s-master1 temp]# tree -a kubernetes
kubernetes
├── addons
├── kubernetes-src.tar.gz
├── LICENSES
└── server
    └── bin
        ├── apiextensions-apiserver
        ├── cloud-controller-manager
        ├── cloud-controller-manager.docker_tag
        ├── cloud-controller-manager.tar
        ├── hyperkube
        ├── kubeadm
        ├── kube-apiserver
        ├── kube-apiserver.docker_tag
        ├── kube-apiserver.tar  
        ├── kube-controller-manager
        ├── kube-controller-manager.docker_tag
        ├── kube-controller-manager.tar
        ├── kubectl
        ├── kubelet
        ├── kube-proxy
        ├── kube-proxy.docker_tag
        ├── kube-proxy.tar
        ├── kube-scheduler
        ├── kube-scheduler.docker_tag
        ├── kube-scheduler.tar
        └── mounter

3 directories, 23 files
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# ll kubernetes/server/bin/
total 1569736
-rwxr-xr-x 1 root root  42785408 Mar 26 00:32 apiextensions-apiserver
-rwxr-xr-x 1 root root 100320960 Mar 26 00:32 cloud-controller-manager
-rw-r--r-- 1 root root         8 Mar 26 00:28 cloud-controller-manager.docker_tag
-rw-r--r-- 1 root root 144212480 Mar 26 00:28 cloud-controller-manager.tar
-rwxr-xr-x 1 root root 211089600 Mar 26 00:32 hyperkube
-rwxr-xr-x 1 root root  39574816 Mar 26 00:32 kubeadm
-rwxr-xr-x 1 root root 167464288 Mar 26 00:32 kube-apiserver
-rw-r--r-- 1 root root         8 Mar 26 00:28 kube-apiserver.docker_tag
-rw-r--r-- 1 root root 211355648 Mar 26 00:28 kube-apiserver.tar # 相关 docker 镜像
-rwxr-xr-x 1 root root 115497504 Mar 26 00:32 kube-controller-manager
-rw-r--r-- 1 root root         8 Mar 26 00:28 kube-controller-manager.docker_tag
-rw-r--r-- 1 root root 159389184 Mar 26 00:28 kube-controller-manager.tar
-rwxr-xr-x 1 root root  43103040 Mar 26 00:32 kubectl
-rwxr-xr-x 1 root root 127850432 Mar 26 00:32 kubelet
-rwxr-xr-x 1 root root  36681344 Mar 26 00:32 kube-proxy
-rw-r--r-- 1 root root         8 Mar 26 00:29 kube-proxy.docker_tag
-rw-r--r-- 1 root root  83978752 Mar 26 00:29 kube-proxy.tar
-rwxr-xr-x 1 root root  39254208 Mar 26 00:32 kube-scheduler
-rw-r--r-- 1 root root         8 Mar 26 00:28 kube-scheduler.docker_tag
-rw-r--r-- 1 root root  83145728 Mar 26 00:28 kube-scheduler.tar
-rwxr-xr-x 1 root root   1648224 Mar 26 00:32 mounter
[root@k8s-master1 temp]# 

[root@lanzhiwang-centos7 bin]# docker load -i kube-apiserver.tar
[root@lanzhiwang-centos7 bin]# docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
k8s.gcr.io/kube-apiserver     v1.14.0             ecf910f40d6e        7 weeks ago         210MB
quay.io/coreos/flannel        v0.11.0-arm         ef3b5d63729b        3 months ago        48.9MB


$ docker pull quay.io/coreos/flannel
其中 quay.io 是 https://quay.io 镜像仓库网站

https://quay.io Docker 镜像私有库
k8s.gcr.io Docker 镜像私有库

quay.io/coreos/flannel:v0.11.0-arm Docker 镜像私有库 / 镜像所属个人或组织 / 镜像名称：tag


# etcd
$ wget https://github.com/coreos/etcd/releases/download/v3.3.13/etcd-v3.3.13-linux-amd64.tar.gz

# docker docker-compose

# cfssl cfssljson cfssl-certinfo
$ wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
$ wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
$ wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
$ mv -f cfssl_linux-amd64 cfssl
$ mv -f cfssljson_linux-amd64 cfssljson
$ mv -f cfssl-certinfo_linux-amd64 cfssl-certinfo

# cni
$ wget https://github.com/containernetworking/plugins/releases/download/v0.8.0/cni-plugins-linux-amd64-v0.8.0.tgz




```



### 机器初始化设置

```bash
$ ntpdate time.windows.com ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com ntp4.aliyun.com  
$ vim /etc/crontab 
*/10  *  *  *  * root  ntpdate time.windows.com ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com ntp4.aliyun.com 


[root@k8s-master1 ~]# cat /etc/fstab 

#
# /etc/fstab
# Created by anaconda on Wed Aug 15 20:43:40 2018
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
UUID=316f8b9b-386f-49df-9fca-f2971f86d0d1 /                       xfs     defaults        0 0
UUID=683349a4-c15d-4889-b476-7f39f8753959 /boot                   xfs     defaults        0 0
[root@k8s-master1 ~]# 



$ fdisk -l
[root@k8s-master1 ~]# fdisk /dev/sdc
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x4636a4e9.

The device presents a logical sector size that is smaller than
the physical sector size. Aligning to a physical sector (or optimal
I/O) size boundary is recommended, or performance may be impacted.

Command (m for help): m
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

Command (m for help): p

Disk /dev/sdc: 536.9 GB, 536870912000 bytes, 1048576000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0x4636a4e9

   Device Boot      Start         End      Blocks   Id  System

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 
First sector (2048-1048575999, default 2048): 
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-1048575999, default 1048575999): 
Using default value 1048575999
Partition 1 of type Linux and of size 500 GiB is set

Command (m for help): p

Disk /dev/sdc: 536.9 GB, 536870912000 bytes, 1048576000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0x4636a4e9

   Device Boot      Start         End      Blocks   Id  System
/dev/sdc1            2048  1048575999   524286976   83  Linux

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
[root@k8s-master1 ~]# fdisk -l

Disk /dev/sda: 32.2 GB, 32212254720 bytes, 62914560 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0x000b9d1d

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     1026047      512000   83  Linux
/dev/sda2         1026048    62914559    30944256   83  Linux

Disk /dev/sdc: 536.9 GB, 536870912000 bytes, 1048576000 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0x4636a4e9

   Device Boot      Start         End      Blocks   Id  System
/dev/sdc1            2048  1048575999   524286976   83  Linux

Disk /dev/sdb: 30.1 GB, 30064771072 bytes, 58720256 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0xfb6852ba

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1             128    58718207    29359040   83  Linux
[root@k8s-master1 ~]# 


mkfs -t ext4 /dev/sdc1

[root@k8s-master1 ~]# mkfs -t ext4 /dev/sdc1
mke2fs 1.42.9 (28-Dec-2013)
Discarding device blocks: done                            
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
32768000 inodes, 131071744 blocks
6553587 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=2279604224
4000 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
	4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968, 
	102400000

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done     

[root@k8s-master1 ~]# 

mount -t ext4 -o defaults /dev/sdc1 /opt/k8s

[root@k8s-master1 ~]# mkdir -p /opt/k8s
[root@k8s-master1 ~]# mount -t ext4 -o defaults /dev/sdc1 /opt/k8s
[root@k8s-master1 ~]# mount | grep /dev/sdc1
/dev/sdc1 on /opt/k8s type ext4 (rw,relatime,data=ordered)
[root@k8s-master1 ~]# 



[root@k8s-master1 ~]# ls -l /dev/disk/by-uuid/
total 0
lrwxrwxrwx 1 root root 10 May 16 17:12 029694db-3f2d-43e1-b7d1-966e0953a4f1 -> ../../sdb1
lrwxrwxrwx 1 root root 10 May 16 17:12 316f8b9b-386f-49df-9fca-f2971f86d0d1 -> ../../sda2
lrwxrwxrwx 1 root root 10 May 16 17:12 683349a4-c15d-4889-b476-7f39f8753959 -> ../../sda1
lrwxrwxrwx 1 root root 10 May 16 17:39 6c772e2d-ecdb-4653-a459-eefd99455f68 -> ../../sdc1
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# blkid
/dev/sda1: UUID="683349a4-c15d-4889-b476-7f39f8753959" TYPE="xfs" 
/dev/sda2: UUID="316f8b9b-386f-49df-9fca-f2971f86d0d1" TYPE="xfs" 
/dev/sdc1: UUID="6c772e2d-ecdb-4653-a459-eefd99455f68" TYPE="ext4" 
/dev/sdb1: UUID="029694db-3f2d-43e1-b7d1-966e0953a4f1" TYPE="ext4" 
[root@k8s-master1 ~]# 


[root@k8s-master1 ~]# vim /etc/fstab
UUID=852da811-4d2e-4108-bb17-8eb51d49689e /opt/k8s                ext4    defaults        0 0
[root@k8s-master1 ~]# 
重启系统检查 hostname 和挂载是否生效


```

### 安装 master 节点

```bash
[root@k8s-master1 ssl]# pwd
/opt/k8s/temp/ssl
# 准备 CA 配置文件
[root@k8s-master1 ssl]# vim ./ca-config.json 
[root@k8s-master1 ssl]# cat ./ca-config.json
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
[root@k8s-master1 ssl]# 

[root@k8s-master1 ssl]# 
# 准备 CA 签名请求文件，CA 证书请求文件有 ca 字段，其他的请求文件没有该字段
[root@k8s-master1 ssl]# vim ./ca-csr.json 
[root@k8s-master1 ssl]# cat ./ca-csr.json
{
  "CN": "kubernetes",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "k8s",
      "OU": "System"
    }
  ],
  "ca": {
    "expiry": "131400h"
  }
}
[root@k8s-master1 ssl]# 

ca-config.json
ca-csr.json 

[root@k8s-master1 ssl]# ./cfssl gencert -initca ca-csr.json | ./cfssljson -bare ca 
[root@k8s-master1 ssl]# ll
total 18828
-rw-r--r-- 1 root root      292 May 20 09:58 ca-config.json
-rw-r--r-- 1 root root     1005 May 20 10:02 ca.csr
-rw-r--r-- 1 root root      251 May 20 10:01 ca-csr.json
-rw------- 1 root root     1675 May 20 10:02 ca-key.pem
-rw-r--r-- 1 root root     1371 May 20 10:02 ca.pem
-rwxr-xr-x 1 root root 10376657 Mar 30  2016 cfssl
-rwxr-xr-x 1 root root  6595195 Mar 30  2016 cfssl-certinfo
-rwxr-xr-x 1 root root  2277873 Mar 30  2016 cfssljson
[root@k8s-master1 ssl]# 

ca-config.json
ca-csr.json 

ca.csr  # CA 证书请求文件
ca-key.pem  # CA 私钥
ca.pem  # CA 证书

# 查看证书信息
[root@k8s-master1 ssl]# ./cfssl-certinfo -cert ./ca.pem
[root@k8s-master1 ssl]# openssl x509 -in ca.pem -noout -text | grep "CA:TRUE"
                CA:TRUE, pathlen:2
[root@k8s-master1 ssl]# 
# 查看证书请求文件
[root@k8s-master1 ssl]# openssl req -text -in ca.csr -noout





# 准备 kubectl 使用的 admin 证书签名请求，缺少 hosts 自动
[root@k8s-master1 ssl]# vim ./admin-csr.json
[root@k8s-master1 ssl]# cat ./admin-csr.json
{
  "CN": "admin",
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
      "O": "system:masters",
      "OU": "System"
    }
  ]
}
[root@k8s-master1 ssl]# 

admin-csr.json

[root@k8s-master1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes admin-csr.json | ./cfssljson -bare admin
2019/05/20 10:29:01 [INFO] generate received request
2019/05/20 10:29:01 [INFO] received CSR
2019/05/20 10:29:01 [INFO] generating key: rsa-2048
2019/05/20 10:29:01 [INFO] encoded CSR
2019/05/20 10:29:01 [INFO] signed certificate with serial number 257984209803207484856031741658634617026284489433
2019/05/20 10:29:01 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
[root@k8s-master1 ssl]# 

admin-csr.json

admin.csr
admin-key.pem
admin.pem

# 查看证书信息
[root@k8s-master1 ssl]# openssl x509 -in admin.pem -noout -text | grep "CA"
                CA:FALSE
[root@k8s-master1 ssl]# 



# 所有节点的准备工作

[root@k8s-master1 temp]# rpm -qa | grep firewall
firewalld-0.4.4.4-14.el7.noarch
firewalld-filesystem-0.4.4.4-14.el7.noarch
python-firewall-0.4.4.4-14.el7.noarch
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# yum erase -y firewalld-0.4.4.4-14.el7.noarch firewalld-filesystem-0.4.4.4-14.el7.noarch python-firewall-0.4.4.4-14.el7.noarch
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# rpm -qa | grep firewall
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# yum install -y conntrack-tools psmisc nfs-utils jq socat bash-completion rsync ipset ipvsadm


# 永久关闭 selinux
vim /etc/selinux/config
"SELINUX=disabled"

# 禁止 rsyslog 获取 journald 日志，注释掉下面两行，重启 rsyslog 服务
[root@k8s-master1 temp]# cat /etc/rsyslog.conf | grep "ModLoad imjournal"
$ModLoad imjournal # provides access to the systemd journal
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# cat /etc/rsyslog.conf | grep "IMJournalStateFile"
$IMJournalStateFile imjournal.state
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# vim /etc/rsyslog.conf
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# cat /etc/rsyslog.conf | grep "ModLoad imjournal"
#$ModLoad imjournal # provides access to the systemd journal
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# cat /etc/rsyslog.conf | grep "IMJournalStateFile"
#$IMJournalStateFile imjournal.state
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# systemctl restart rsyslog.service
[root@k8s-master1 temp]# systemctl status rsyslog.service
● rsyslog.service - System Logging Service
   Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2019-05-19 14:42:16 CST; 1s ago
     Docs: man:rsyslogd(8)
           http://www.rsyslog.com/doc/
 Main PID: 123408 (rsyslogd)
   CGroup: /system.slice/rsyslog.service
           └─123408 /usr/sbin/rsyslogd -n

May 19 14:42:16 k8s-master1 systemd[1]: Starting System Logging Service...
May 19 14:42:16 k8s-master1 rsyslogd[123408]:  [origin software="rsyslogd" swVersion="8.24.0" x-pid="123408" x-info="http://www.rsyslog.com"] start
May 19 14:42:16 k8s-master1 systemd[1]: Started System Logging Service.
[root@k8s-master1 temp]# 


# 查看 vm.swappiness 设置值
[root@k8s-master1 temp]# sysctl -a | grep vm.swappiness
sysctl: reading key "net.ipv6.conf.all.stable_secret"
sysctl: reading key "net.ipv6.conf.default.stable_secret"
sysctl: reading key "net.ipv6.conf.eth0.stable_secret"
sysctl: reading key "net.ipv6.conf.lo.stable_secret"
vm.swappiness = 30
[root@k8s-master1 temp]# 
# 禁用系统 swap，临时改变 vm.swappiness 的值
[root@k8s-master1 temp]# swapoff -a && sysctl -w vm.swappiness=0
vm.swappiness = 0
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# sysctl -a | grep vm.swappiness
sysctl: reading key "net.ipv6.conf.all.stable_secret"
sysctl: reading key "net.ipv6.conf.default.stable_secret"
sysctl: reading key "net.ipv6.conf.eth0.stable_secret"
sysctl: reading key "net.ipv6.conf.lo.stable_secret"
vm.swappiness = 0
[root@k8s-master1 temp]# 

# 注释 /etc/fstab 中的 swap 相关配置，swap 在 /etc/fstab 中的挂载点是 swap，文件类型也是 swap
cat /etc/fstab | grep swap
/dev/mapper/centos-swap swap                    swap    defaults        0 0
 




# lsmod 查看已经安装好的模块，也可以查看 /proc/modules 文件的内容。实际上，lsmod 命令就是通过查看 /proc/modules 的内容来显示模块信息的。
# 已经安装 br_netfilter 模块
[root@lanzhiwang-centos7 bin]# lsmod | grep br_netfilter
br_netfilter           22256  0 
bridge                146976  1 br_netfilter
[root@lanzhiwang-centos7 bin]# 
# 没有安装 ip_vs 模块
[root@lanzhiwang-centos7 bin]# lsmod | grep ip_vs
[root@lanzhiwang-centos7 bin]# 

# modinfo 显示模块信息，无论模块是否安装都可以显示模块信息
[root@lanzhiwang-centos7 bin]# modinfo br_netfilter
filename:       /lib/modules/3.10.0-862.el7.x86_64/kernel/net/bridge/br_netfilter.ko.xz
description:    Linux ethernet netfilter firewall bridge
author:         Bart De Schuymer <bdschuym@pandora.be>
author:         Lennert Buytenhek <buytenh@gnu.org>
license:        GPL
retpoline:      Y
rhelversion:    7.5
srcversion:     C4DE536495D55C12BA6A8A8
depends:        bridge
intree:         Y
vermagic:       3.10.0-862.el7.x86_64 SMP mod_unload modversions 
signer:         CentOS Linux kernel signing key
sig_key:        3A:F3:CE:8A:74:69:6E:F1:BD:0F:37:E5:52:62:7B:71:09:E3:2B:96
sig_hashalgo:   sha256
[root@lanzhiwang-centos7 bin]# 
[root@lanzhiwang-centos7 bin]# modinfo ip_vs
filename:       /lib/modules/3.10.0-862.el7.x86_64/kernel/net/netfilter/ipvs/ip_vs.ko.xz
license:        GPL
retpoline:      Y
rhelversion:    7.5
srcversion:     D6411BDB090FBEFAFD8AFB6
depends:        nf_conntrack,libcrc32c
intree:         Y
vermagic:       3.10.0-862.el7.x86_64 SMP mod_unload modversions 
signer:         CentOS Linux kernel signing key
sig_key:        3A:F3:CE:8A:74:69:6E:F1:BD:0F:37:E5:52:62:7B:71:09:E3:2B:96
sig_hashalgo:   sha256
parm:           conn_tab_bits:Set connections' hash size (int)
[root@lanzhiwang-centos7 bin]# 

# insmod 加载模块，需要指定完整的路径、模块名字、模块依赖及路径信息，这样可以成功加载需要模块。查看模块依赖关系可用 modinfo 命令

# rmmod 卸载模块，但是内核会认为卸载模块不安全，可以添加命令强制卸载。

# modprobe 命令可以查看、加载、卸载模块。加载模块不需要指定路径，它会到默认路径下寻找模块

lsmod | grep br_netfilter
lsmod | grep ip_vs
lsmod | grep ip_vs_rr
lsmod | grep ip_vs_wrr
lsmod | grep ip_vs_sh


$ lsmod | grep br_netfilter
br_netfilter           22256  0 
bridge                146976  1 br_netfilter


$ lsmod | grep ip_vs
$ modprobe ip_vs
$ lsmod | grep ip_vs
ip_vs                 141432  0 
nf_conntrack          133053  7 ip_vs,nf_nat,nf_nat_ipv4,xt_conntrack,nf_nat_masquerade_ipv4,nf_conntrack_netlink,nf_conntrack_ipv4
libcrc32c              12644  4 xfs,ip_vs,nf_nat,nf_conntrack

$ lsmod | grep ip_vs_rr
$ modprobe ip_vs_rr
$ lsmod | grep ip_vs_rr
ip_vs_rr               12600  0 
ip_vs                 141432  2 ip_vs_rr

$ lsmod | grep ip_vs_wrr
$ modprobe ip_vs_wrr
$ lsmod | grep ip_vs_wrr
ip_vs_wrr              12697  0 
ip_vs                 141432  4 ip_vs_rr,ip_vs_wrr

$ lsmod | grep ip_vs_sh
$ modprobe ip_vs_sh
$ lsmod | grep ip_vs_sh
ip_vs_sh               12688  0 
ip_vs                 141432  6 ip_vs_rr,ip_vs_sh,ip_vs_wrr

# 查看内核版本
$ cat /proc/version
Linux version 3.10.0-862.el7.x86_64 (builder@kbuilder.dev.centos.org) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-28) (GCC) ) #1 SMP Fri Apr 20 16:44:24 UTC 2018

$ uname -a
Linux lanzhiwang-centos7 3.10.0-862.el7.x86_64 #1 SMP Fri Apr 20 16:44:24 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

$ uname -r
3.10.0-862.el7.x86_64

# 内核版本 >= 4.19，加载内核模块 nf_conntrack
# 内核版本 < 4.19，加载内核模块 nf_conntrack_ipv4
# 其实无论内核什么版本，可以把 nf_conntrack_ipv4 和 nf_conntrack 模块都加载

# 加载相关内核模块
br_netfilter、ip_vs、ip_vs_rr、ip_vs_wrr、ip_vs_sh、nf_conntrack_ipv4、nf_conntrack

# 启用 systemd 自动加载模块服务

# 增加内核模块开机加载配置
$ vim /etc/modules-load.d/10-k8s-modules.conf
$ cat /etc/modules-load.d/10-k8s-modules.conf
br_netfilter
ip_vs
ip_vs_rr
ip_vs_wrr
ip_vs_sh
nf_conntrack_ipv4
nf_conntrack
$
# 启动 systemd-modules-load 前要在 /etc/modules-load.d 目录中指定相关文件
$ systemctl status systemd-modules-load
$ systemctl start systemd-modules-load  
$ systemctl status systemd-modules-load
$ systemctl daemon-reload
$ systemctl enable systemd-modules-load


# 设置系统参数
$ vim /etc/sysctl.d/95-k8s-sysctl.conf
$ cat /etc/sysctl.d/95-k8s-sysctl.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-arptables = 1 
net.netfilter.nf_conntrack_max=1000000
vm.swappiness = 0
vm.max_map_count=655360
fs.file-max=655360
# 生效系统参数
sysctl -p /etc/sysctl.d/95-k8s-sysctl.conf

# 设置系统 ulimits
$ vim /etc/security/limits.d/30-k8s-ulimits.conf
$ cat /etc/security/limits.d/30-k8s-ulimits.conf
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536

# 把SCTP列入内核模块黑名单
$ vim /etc/modprobe.d/sctp.conf
$ cat /etc/modprobe.d/sctp.conf
# put sctp into blacklist
install sctp /bin/true


# scp


$ yum install -y yum-utils device-mapper-persistent-data lvm2
$ yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
$ yum makecache fast
$ yum install -y docker-ce
[root@k8s-master1 temp]# mkdir -p /etc/docker /opt/k8s/docker
[root@k8s-master1 temp]# vim /etc/docker/daemon.json
[root@k8s-master1 temp]# cat /etc/docker/daemon.json
{
  "max-concurrent-downloads": 10,
  "log-driver": "json-file",
  "log-level": "warn",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
    },
  "data-root": "/opt/k8s/docker"
}
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# systemctl daemon-reload
[root@k8s-master1 temp]# systemctl enable docker.service
[root@k8s-master1 temp]# systemctl start docker.service
[root@k8s-master1 temp]# systemctl status docker.service 
[root@k8s-master1 temp]# docker info
Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
Images: 0
Server Version: 18.09.6
Storage Driver: overlay2
 Backing Filesystem: extfs
 Supports d_type: true
 Native Overlay Diff: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins:
 Volume: local
 Network: bridge host macvlan null overlay
 Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Init Binary: docker-init
containerd version: bb71b10fd8f58240ca47fbb579b9d1028eea7c84
runc version: 2b18fe1d885ee5083ef9f0838fee39b62d653e30
init version: fec3683
Security Options:
 seccomp
  Profile: default
Kernel Version: 3.10.0-862.11.6.el7.x86_64
Operating System: CentOS Linux 7 (Core)
OSType: linux
Architecture: x86_64
CPUs: 4
Total Memory: 13.69GiB
Name: k8s-master1
ID: 4TZL:XLU3:FEO5:CYEJ:XHGV:KL4K:PCD6:MK6A:5SV6:VVSY:NFBB:VIDZ
Docker Root Dir: /opt/k8s/docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
Labels:
Experimental: false
Insecure Registries:
 127.0.0.0/8
Live Restore Enabled: false
Product License: Community Engine

[root@k8s-master1 temp]# ll /opt/k8s/docker/
total 48
drwx------ 2 root root 4096 May 20 14:54 builder
drwx------ 4 root root 4096 May 20 14:54 buildkit
drwx------ 2 root root 4096 May 20 14:54 containers
drwx------ 3 root root 4096 May 20 14:54 image
drwxr-x--- 3 root root 4096 May 20 14:54 network
drwx------ 3 root root 4096 May 20 14:54 overlay2
drwx------ 4 root root 4096 May 20 14:54 plugins
drwx------ 2 root root 4096 May 20 14:54 runtimes
drwx------ 2 root root 4096 May 20 14:54 swarm
drwx------ 2 root root 4096 May 20 14:54 tmp
drwx------ 2 root root 4096 May 20 14:54 trust
drwx------ 2 root root 4096 May 20 14:54 volumes
[root@k8s-master1 temp]# 


[root@k8s-master1 temp]# curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
[root@k8s-master1 temp]# chmod +x /usr/local/bin/docker-compose
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
[root@k8s-master1 temp]# ln -s /usr/local/bin/docker-compose /usr/sbin/docker-compose
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# docker-compose --version
docker-compose version 1.24.0, build 0aa59064
[root@k8s-master1 temp]# 

```


### 安装 etcd

10.1.36.43
10.1.36.44
10.1.36.45

```bash

# 创建 etcd 证书请求文件
[root@k8s-master1 ssl]# vim ./etcd-csr.json
[root@k8s-master1 ssl]# cat ./etcd-csr.json
{
  "CN": "etcd",
  "hosts": [
    "127.0.0.1",
    "10.1.36.43",
    "10.1.36.44",
    "10.1.36.45"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
[root@k8s-master1 ssl]# 

[root@k8s-master1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes etcd-csr.json | ./cfssljson -bare etcd

etcd-csr.json

etcd.csr
etcd-key.pem
etcd.pem


mkdir -p /opt/k8s/etcd
mkdir -p /opt/k8s/bin
etcd
etcdctl

mkdir -p /opt/k8s/ssl

etcd.pem
etcd-key.pem
ca.pem
  
# 创建etcd的 systemd unit 文件，以 10.1.36.43 NODE_NAME=etcd1 为例
[root@k8s-master1 k8s]# vim /etc/systemd/system/etcd.service
[root@k8s-master1 k8s]# cat /etc/systemd/system/etcd.service
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/coreos

[Service]
Type=notify
WorkingDirectory=/opt/k8s/etcd
ExecStart=/opt/k8s/bin/etcd \
  --name=etcd1 \
  --cert-file=/opt/k8s/ssl/etcd.pem \
  --key-file=/opt/k8s/ssl/etcd-key.pem \
  --trusted-ca-file=/opt/k8s/ssl/ca.pem \
  --peer-cert-file=/opt/k8s/ssl/etcd.pem \
  --peer-key-file=/opt/k8s/ssl/etcd-key.pem \
  --peer-trusted-ca-file=/opt/k8s/ssl/ca.pem \
  --initial-advertise-peer-urls=https://10.1.36.43:2380 \
  --listen-peer-urls=https://10.1.36.43:2380 \
  --listen-client-urls=https://10.1.36.43:2379,http://127.0.0.1:2379 \
  --advertise-client-urls=https://10.1.36.43:2379 \
  --initial-cluster-token=etcd-cluster \
  --initial-cluster=etcd1=https://10.1.36.43:2380,etcd2=https://10.1.36.44:2380,etcd3=https://10.1.36.45:2380 \
  --initial-cluster-state=new \
  --data-dir=/opt/k8s/etcd
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
[root@k8s-master1 k8s]# 


# 开机启用etcd服务
systemctl enable etcd （ systemctl disable etcd ）
# 开启etcd服务
systemctl daemon-reload
systemctl restart etcd
systemctl status etcd.service

# 查看日志
journalctl -xe
journalctl -u etcd

# 检查服务是否正常
ETCDCTL_API=3 /opt/k8s/bin/etcdctl --endpoints=https://10.1.36.43:2379 --cacert=/opt/k8s/ssl/ca.pem --cert=/opt/k8s/ssl/etcd.pem --key=/opt/k8s/ssl/etcd-key.pem endpoint health

ETCDCTL_API=3 /opt/k8s/bin/etcdctl --endpoints=https://10.1.36.43:2379 --cacert=/opt/k8s/ssl/ca.pem --cert=/opt/k8s/ssl/etcd.pem --key=/opt/k8s/ssl/etcd-key.pem endpoint status
ETCDCTL_API=3 /opt/k8s/bin/etcdctl -w table --endpoints=https://10.1.36.43:2379 --cacert=/opt/k8s/ssl/ca.pem --cert=/opt/k8s/ssl/etcd.pem --key=/opt/k8s/ssl/etcd-key.pem endpoint status


netstat -tulnp | grep 2379
netstat -tulnp | grep 2380

[root@k8s-master1 etcd]# ETCDCTL_API=3 /opt/k8s/bin/etcdctl -w table --endpoints=https://10.1.36.43:2379 --cacert=/opt/k8s/ssl/ca.pem --cert=/opt/k8s/ssl/etcd.pem --key=/opt/k8s/ssl/etcd-key.pem member list
+------------------+---------+-------+-------------------------+-------------------------+
|        ID        | STATUS  | NAME  |       PEER ADDRS        |      CLIENT ADDRS       |
+------------------+---------+-------+-------------------------+-------------------------+
| 342124d005cfc514 | started | etcd2 | https://10.1.36.44:2380 | https://10.1.36.44:2379 |
| 693065fae82f839e | started | etcd3 | https://10.1.36.45:2380 | https://10.1.36.45:2379 |
| e2051cb26200bca6 | started | etcd1 | https://10.1.36.43:2380 | https://10.1.36.43:2379 |
+------------------+---------+-------+-------------------------+-------------------------+
[root@k8s-master1 etcd]# 


[root@k8s-master1 etcd]# ETCDCTL_API=3 /opt/k8s/bin/etcdctl --endpoints=https://10.1.36.43:2379 --cacert=/opt/k8s/ssl/ca.pem --cert=/opt/k8s/ssl/etcd.pem --key=/opt/k8s/ssl/etcd-key.pem check perf
 60 / 60 Booooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo! 100.00%1m0s
PASS: Throughput is 150 writes/s
PASS: Slowest request took 0.065082s
PASS: Stddev is 0.007099s
PASS
[root@k8s-master1 etcd]# 

note: 如果重新部署，使用一下步骤：
1、删除 /opt/k8s/etcd 目录下的所有内容
2、systemctl disable etcd
3、再重复执行上述过程


# 创建etcd的 systemd unit 文件，以 10.1.36.44 NODE_NAME=etcd2 为例
vim /etc/systemd/system/etcd.service
cat /etc/systemd/system/etcd.service
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/coreos

[Service]
Type=notify
WorkingDirectory=/opt/k8s/etcd
ExecStart=/opt/k8s/bin/etcd \
  --name=etcd2 \
  --cert-file=/opt/k8s/ssl/etcd.pem \
  --key-file=/opt/k8s/ssl/etcd-key.pem \
  --trusted-ca-file=/opt/k8s/ssl/ca.pem \
  --peer-cert-file=/opt/k8s/ssl/etcd.pem \
  --peer-key-file=/opt/k8s/ssl/etcd-key.pem \
  --peer-trusted-ca-file=/opt/k8s/ssl/ca.pem \
  --initial-advertise-peer-urls=https://10.1.36.44:2380 \
  --listen-peer-urls=https://10.1.36.44:2380 \
  --listen-client-urls=https://10.1.36.44:2379,http://127.0.0.1:2379 \
  --advertise-client-urls=https://10.1.36.44:2379 \
  --initial-cluster-token=etcd-cluster \
  --initial-cluster=etcd1=https://10.1.36.43:2380,etcd2=https://10.1.36.44:2380,etcd3=https://10.1.36.45:2380 \
  --initial-cluster-state=new \
  --data-dir=/opt/k8s/etcd
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target


# 创建etcd的 systemd unit 文件，以 10.1.36.45 NODE_NAME=etcd3 为例
vim /etc/systemd/system/etcd.service
cat /etc/systemd/system/etcd.service
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/coreos

[Service]
Type=notify
WorkingDirectory=/opt/k8s/etcd
ExecStart=/opt/k8s/bin/etcd \
  --name=etcd3 \
  --cert-file=/opt/k8s/ssl/etcd.pem \
  --key-file=/opt/k8s/ssl/etcd-key.pem \
  --trusted-ca-file=/opt/k8s/ssl/ca.pem \
  --peer-cert-file=/opt/k8s/ssl/etcd.pem \
  --peer-key-file=/opt/k8s/ssl/etcd-key.pem \
  --peer-trusted-ca-file=/opt/k8s/ssl/ca.pem \
  --initial-advertise-peer-urls=https://10.1.36.45:2380 \
  --listen-peer-urls=https://10.1.36.45:2380 \
  --listen-client-urls=https://10.1.36.45:2379,http://127.0.0.1:2379 \
  --advertise-client-urls=https://10.1.36.45:2379 \
  --initial-cluster-token=etcd-cluster \
  --initial-cluster=etcd1=https://10.1.36.43:2380,etcd2=https://10.1.36.44:2380,etcd3=https://10.1.36.45:2380 \
  --initial-cluster-state=new \
  --data-dir=/opt/k8s/etcd
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target



10.1.36.43
10.1.36.44
10.1.36.45


[root@k8s-master1 ssl]# vim ./kubernetes-csr.json
[root@k8s-master1 ssl]# cat ./kubernetes-csr.json
{
  "CN": "kubernetes",
  "hosts": [
    "127.0.0.1",
    "10.1.36.43",
    "10.1.36.44",
    "10.1.36.45",
    "10.68.0.2",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes kubernetes-csr.json | ./cfssljson -bare kubernetes

kubernetes-csr.json

kubernetes.csr
kubernetes-key.pem
kubernetes.pem

# 测试 kubernetes.pem 证书是否可以连接 etcd 集群
[root@k8s-master1 ssl]# ETCDCTL_API=3 /opt/k8s/bin/etcdctl -w table --endpoints=https://10.1.36.43:2379 --cacert=./ca.pem --cert=./kubernetes.pem --key=./kubernetes-key.pem member list
+------------------+---------+-------+-------------------------+-------------------------+
|        ID        | STATUS  | NAME  |       PEER ADDRS        |      CLIENT ADDRS       |
+------------------+---------+-------+-------------------------+-------------------------+
| 342124d005cfc514 | started | etcd2 | https://10.1.36.44:2380 | https://10.1.36.44:2379 |
| 693065fae82f839e | started | etcd3 | https://10.1.36.45:2380 | https://10.1.36.45:2379 |
| e2051cb26200bca6 | started | etcd1 | https://10.1.36.43:2380 | https://10.1.36.43:2379 |
+------------------+---------+-------+-------------------------+-------------------------+
[root@k8s-master1 ssl]# 

# 查看证书内容验证 user 和 group
[root@k8s-master1 ssl]# openssl x509 -in kubernetes.pem -noout -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            0f:6d:5c:12:78:78:69:8e:c7:f9:2c:ae:77:4e:49:3a:f5:87:b8:06
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=CN, ST=hubeisheng, L=wuhanshi, O=k8s, OU=System, CN=kubernetes
        Validity
            Not Before: May 20 12:21:00 2019 GMT
            Not After : May 17 12:21:00 2029 GMT
        Subject: C=CN, ST=hubeisheng, L=wuhanshi, O=k8s, OU=System, CN=kubernetes
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:b1:87:83:6f:c1:5e:83:80:3d:e9:6e:09:79:6e:
                    24:4a:ef:62:2a:af:d0:67:57:5a:f0:0e:80:41:db:
                    15:5f:41:cd:60:b5:cd:9c:dc:a7:3d:b3:b5:e0:14:
                    3a:7d:af:6e:0c:93:50:6e:7e:0a:6f:eb:bd:ad:6d:
                    92:e0:e5:d7:bc:a5:2e:c8:8e:53:bb:2b:14:44:ee:
                    b4:b2:a4:a9:f7:ed:ca:eb:77:51:62:3f:9e:6f:70:
                    48:22:29:76:f3:bd:de:8d:72:02:ef:85:66:5f:db:
                    3a:53:aa:dc:4a:67:de:75:48:2f:b7:74:f4:38:ba:
                    51:c8:5b:47:47:5e:15:ae:51:2f:13:e9:05:0a:ca:
                    04:ab:79:7d:1c:d8:a2:e1:c3:47:e5:fc:86:45:7e:
                    2e:dd:65:75:ca:26:ee:bd:4d:b9:d2:2c:3f:08:08:
                    8a:83:aa:38:56:92:b8:46:75:3f:9d:d4:de:08:0a:
                    67:bf:95:fd:bf:58:ed:6a:56:2a:73:89:a1:ae:9a:
                    e6:69:ec:51:77:88:8b:d9:09:2d:69:25:67:58:eb:
                    ec:78:b7:25:66:94:03:07:39:19:e7:86:1e:81:f8:
                    54:c4:ca:fd:1a:58:f1:b7:5f:d5:97:b6:8f:7a:62:
                    c8:98:cc:da:2b:dd:0f:a4:15:76:c9:3a:00:82:3c:
                    16:f1
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment
            X509v3 Extended Key Usage: 
                TLS Web Server Authentication, TLS Web Client Authentication
            X509v3 Basic Constraints: critical
                CA:FALSE
            X509v3 Subject Key Identifier: 
                86:35:89:ED:05:CB:B9:D2:EF:1A:8E:B7:D2:57:F4:B8:24:1D:A4:95
            X509v3 Authority Key Identifier: 
                keyid:2D:9D:AA:71:D1:C6:9A:BC:B8:FC:40:4B:59:64:CE:93:9D:F9:1C:98

            X509v3 Subject Alternative Name: 
                DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:10.1.36.43, IP Address:10.1.36.44, IP Address:10.1.36.45, IP Address:10.68.0.2
    Signature Algorithm: sha256WithRSAEncryption
         a0:ac:86:cd:d8:73:fe:7b:64:27:12:ca:1a:91:7d:26:a9:e5:
         b7:67:72:a5:be:b0:5d:61:0d:17:fd:06:1e:9c:8a:04:72:a7:
         61:5d:d2:dd:13:2e:44:6e:3a:fd:65:15:33:c1:cd:90:bd:91:
         c3:f7:46:17:50:40:07:21:a0:e1:e3:f9:4b:8e:b8:b8:90:f6:
         c8:07:12:10:ff:25:05:e7:1a:39:16:35:92:5e:11:4d:6c:67:
         45:6b:7b:39:0a:fc:b2:1d:f8:eb:7d:d6:50:a9:4e:06:c6:08:
         56:76:13:ea:0f:7d:8c:78:4c:c0:f8:ca:af:aa:0f:43:7b:fe:
         bd:9b:3d:46:1c:4f:f6:34:92:9e:a1:e6:ae:1f:7a:c0:c2:a2:
         75:00:12:23:0d:45:72:7c:8e:1a:03:e7:32:71:e2:06:53:9b:
         7c:13:f9:32:c8:c7:40:10:08:94:05:29:9c:94:67:a2:25:76:
         e5:e2:61:94:70:bf:3f:fd:cb:58:e0:11:62:ea:a4:36:bb:c5:
         27:77:d8:e8:44:6f:cc:a7:9a:92:87:97:81:61:9c:79:3a:20:
         e0:41:4f:f7:f2:09:e8:5a:e7:97:63:98:90:89:f1:49:fc:fc:
         f7:19:9a:0d:35:dc:36:96:05:af:13:a0:5f:7b:4d:9b:9a:9b:
         d2:f6:e3:f0
[root@k8s-master1 ssl]# 


# 创建 aggregator proxy 证书签名请求
[root@k8s-master1 ssl]# vim ./aggregator-proxy-csr.json
[root@k8s-master1 ssl]# cat ./aggregator-proxy-csr.json
{
  "CN": "aggregator",
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
      "O": "k8s",
      "OU": "System"
    }
  ]
}
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes aggregator-proxy-csr.json | ./cfssljson -bare aggregator-proxy

aggregator-proxy-csr.json

aggregator-proxy.csr
aggregator-proxy-key.pem
aggregator-proxy.pem

[root@k8s-master1 ssl]# vim ./basic-auth.csv
[root@k8s-master1 ssl]# cat ./basic-auth.csv
admin,admin,1
readonly,readonly,2
[root@k8s-master1 ssl]# 


10.1.36.43
10.1.36.44
10.1.36.45

/opt/k8s/bin/
kube-apiserver

/opt/k8s/ssl
ca.pem
ca-key.pem
kubernetes.pem
kubernetes-key.pem
basic-auth.csv
admin.pem
admin-key.pem
aggregator-proxy.pem
aggregator-proxy-key.pem

/opt/k8s/log/
audit.log
apiserver.log

# 创建 kube-apiserver 的 systemd unit 文件，以 10.1.36.43 为例
[root@k8s-master1 temp]# vim /etc/systemd/system/kube-apiserver.service
[root@k8s-master1 temp]# cat /etc/systemd/system/kube-apiserver.service
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
ExecStart=/opt/k8s/bin/kube-apiserver \
  --etcd-cafile=/opt/k8s/ssl/ca.pem \
  --etcd-certfile=/opt/k8s/ssl/kubernetes.pem \
  --etcd-keyfile=/opt/k8s/ssl/kubernetes-key.pem \
  --etcd-servers=https://10.1.36.43:2379,https://10.1.36.44:2379,https://10.1.36.45:2379 \
  --bind-address=10.1.36.43 \
  --tls-cert-file=/opt/k8s/ssl/kubernetes.pem \
  --tls-private-key-file=/opt/k8s/ssl/kubernetes-key.pem \
  --insecure-bind-address=127.0.0.1 \
  --audit-log-maxage=30 \
  --audit-log-maxbackup=3 \
  --audit-log-maxsize=100 \
  --audit-log-path=/opt/k8s/log/audit.log \
  --enable-swagger-ui=true \
  --anonymous-auth=false \
  --basic-auth-file=/opt/k8s/ssl/basic-auth.csv \
  --client-ca-file=/opt/k8s/ssl/ca.pem \
  --service-account-key-file=/opt/k8s/ssl/ca-key.pem \
  --requestheader-client-ca-file=/opt/k8s/ssl/ca.pem \
  --requestheader-allowed-names= \
  --requestheader-extra-headers-prefix=X-Remote-Extra- \
  --requestheader-group-headers=X-Remote-Group \
  --requestheader-username-headers=X-Remote-User \
  --authorization-mode=Node,RBAC \
  --runtime-config=batch/v2alpha1=true \
  --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook \
  --kubelet-https=true \
  --kubelet-client-certificate=/opt/k8s/ssl/admin.pem \
  --kubelet-client-key=/opt/k8s/ssl/admin-key.pem \
  --service-cluster-ip-range=10.68.0.0/16 \
  --service-node-port-range=20000-40000 \
  --endpoint-reconciler-type=lease \
  --allow-privileged=true \
  --event-ttl=1h \
  --proxy-client-cert-file=/opt/k8s/ssl/aggregator-proxy.pem \
  --proxy-client-key-file=/opt/k8s/ssl/aggregator-proxy-key.pem \
  --enable-aggregator-routing=true \
  --v=2 \
  --log-file=/opt/k8s/log/apiserver.log
  
Restart=on-failure
RestartSec=5
Type=notify
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

[root@k8s-master1 temp]# 


# 创建 kube-apiserver 的 systemd unit 文件，以 10.1.36.44 为例
[root@k8s-master1 temp]# vim /etc/systemd/system/kube-apiserver.service
[root@k8s-master1 temp]# cat /etc/systemd/system/kube-apiserver.service
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
ExecStart=/opt/k8s/bin/kube-apiserver \
  --etcd-cafile=/opt/k8s/ssl/ca.pem \
  --etcd-certfile=/opt/k8s/ssl/kubernetes.pem \
  --etcd-keyfile=/opt/k8s/ssl/kubernetes-key.pem \
  --etcd-servers=https://10.1.36.43:2379,https://10.1.36.44:2379,https://10.1.36.45:2379 \
  --bind-address=10.1.36.44 \
  --tls-cert-file=/opt/k8s/ssl/kubernetes.pem \
  --tls-private-key-file=/opt/k8s/ssl/kubernetes-key.pem \
  --insecure-bind-address=127.0.0.1 \
  --audit-log-maxage=30 \
  --audit-log-maxbackup=3 \
  --audit-log-maxsize=100 \
  --audit-log-path=/opt/k8s/log/audit.log \
  --enable-swagger-ui=true \
  --anonymous-auth=false \
  --basic-auth-file=/opt/k8s/ssl/basic-auth.csv \
  --client-ca-file=/opt/k8s/ssl/ca.pem \
  --service-account-key-file=/opt/k8s/ssl/ca-key.pem \
  --requestheader-client-ca-file=/opt/k8s/ssl/ca.pem \
  --requestheader-allowed-names= \
  --requestheader-extra-headers-prefix=X-Remote-Extra- \
  --requestheader-group-headers=X-Remote-Group \
  --requestheader-username-headers=X-Remote-User \
  --authorization-mode=Node,RBAC \
  --runtime-config=batch/v2alpha1=true \
  --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,ResourceQuota,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook \
  --kubelet-https=true \
  --kubelet-client-certificate=/opt/k8s/ssl/admin.pem \
  --kubelet-client-key=/opt/k8s/ssl/admin-key.pem \
  --service-cluster-ip-range=10.68.0.0/16 \
  --service-node-port-range=20000-40000 \
  --endpoint-reconciler-type=lease \
  --allow-privileged=true \
  --event-ttl=1h \
  --proxy-client-cert-file=/opt/k8s/ssl/aggregator-proxy.pem \
  --proxy-client-key-file=/opt/k8s/ssl/aggregator-proxy-key.pem \
  --enable-aggregator-routing=true \
  --v=2 \
  --log-file=/opt/k8s/log/apiserver.log
  
Restart=on-failure
RestartSec=5
Type=notify
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target



# 验证版本
[root@k8s-master1 bin]# ./kube-apiserver --version
Kubernetes v1.14.0
[root@k8s-master1 bin]# 


systemctl enable kube-apiserver.service （ systemctl disable kube-apiserver.service ）
systemctl daemon-reload
systemctl restart kube-apiserver.service
systemctl status kube-apiserver.service

# 查看日志
journalctl -xe
journalctl -u kube-apiserver

[root@k8s-master2 ssl]# netstat -tulnp | grep kube-apiserve
tcp        0      0 10.1.36.44:6443         0.0.0.0:*               LISTEN      76377/kube-apiserve 
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      76377/kube-apiserve 
[root@k8s-master2 ssl]# 


[root@k8s-master1 temp]# netstat -tulnp | grep kube
tcp        0      0 10.1.36.43:6443         0.0.0.0:*               LISTEN      98043/kube-apiserve 
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      98043/kube-apiserve 
[root@k8s-master1 temp]# 



/opt/k8s/bin
kube-controller-manager

/opt/k8s/ssl
ca.pem
ca-key.pem

/opt/k8s/log/
kube-controller-manager.log


# 创建 kube-controller-manager 的 systemd unit 文件
[root@k8s-master1 bin]# vim /etc/systemd/system/kube-controller-manager.service
[root@k8s-master1 bin]# cat /etc/systemd/system/kube-controller-manager.service
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/opt/k8s/bin/kube-controller-manager \
  --allocate-node-cidrs=true \
  --cluster-cidr=172.20.0.0/16 \
  --cluster-name=kubernetes \
  --leader-elect=true \
  --address=127.0.0.1 \
  --cluster-signing-cert-file=/opt/k8s/ssl/ca.pem \
  --cluster-signing-key-file=/opt/k8s/ssl/ca-key.pem \
  --horizontal-pod-autoscaler-use-rest-clients=true \
  --service-cluster-ip-range=10.68.0.0/16 \
  --service-account-private-key-file=/opt/k8s/ssl/ca-key.pem \
  --root-ca-file=/opt/k8s/ssl/ca.pem \
  --master=http://127.0.0.1:8080 \
  --log-file=/opt/k8s/log/kube-controller-manager.log
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
[root@k8s-master1 bin]# 



systemctl enable kube-controller-manager.service （ systemctl disable kube-controller-manager.service ）
systemctl daemon-reload
systemctl restart kube-controller-manager.service
systemctl status kube-controller-manager.service


[root@k8s-master1 bin]# netstat -tulnp | grep kube-controll
tcp        0      0 127.0.0.1:10252         0.0.0.0:*               LISTEN      99302/kube-controll 
tcp6       0      0 :::10257                :::*                    LISTEN      99302/kube-controll 
[root@k8s-master1 bin]# 


/opt/k8s/bin/
kube-scheduler

/opt/k8s/log/
kube-scheduler.log

# 创建 kube-scheduler 的 systemd unit 文件
[root@k8s-master1 bin]# vim /etc/systemd/system/kube-scheduler.service
[root@k8s-master1 bin]# cat /etc/systemd/system/kube-scheduler.service
[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
ExecStart=/opt/k8s/bin/kube-scheduler \
  --address=127.0.0.1 \
  --master=http://127.0.0.1:8080 \
  --leader-elect=true \
  --log-file=/opt/k8s/log/kube-scheduler.log
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

[root@k8s-master1 bin]# 


systemctl enable kube-scheduler.service （ systemctl disable kube-scheduler.service ）
systemctl daemon-reload
systemctl restart kube-scheduler.service
systemctl status kube-scheduler.service

[root@k8s-master1 bin]# netstat -tulnp | grep kube-schedul
tcp        0      0 127.0.0.1:10251         0.0.0.0:*               LISTEN      100194/kube-schedul 
tcp6       0      0 :::10259                :::*                    LISTEN      100194/kube-schedul 
[root@k8s-master1 bin]# 


# 为 kubectl 设置集群参数，指定 CA 证书和 apiserver 地址
# [root@k8s-master1 bin]# ./kubectl config set-cluster kubernetes --certificate-authority=/opt/k8s/ssl/ca.pem --embed-certs=true --server=https://10.1.36.43:6443
[root@k8s-master1 bin]# ./kubectl config set-cluster kubernetes --certificate-authority=/opt/k8s/ssl/ca.pem --embed-certs=true --server=https://127.0.0.1:8443
Cluster "kubernetes" set.
[root@k8s-master1 bin]# 
[root@k8s-master1 bin]# 
[root@k8s-master1 bin]# cat ~/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://10.1.36.43:6443
  name: kubernetes
contexts: []
current-context: ""
kind: Config
preferences: {}
users: []
[root@k8s-master1 bin]# 

# 设置客户端 kubectl 认证参数，指定使用 admin 证书和私钥
[root@k8s-master1 bin]# ./kubectl config set-credentials admin --client-certificate=/opt/k8s/ssl/admin.pem --embed-certs=true --client-key=/opt/k8s/ssl/admin-key.pem
User "admin" set.
[root@k8s-master1 bin]# cat ~/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://10.1.36.43:6443
  name: kubernetes
contexts: []
current-context: ""
kind: Config
preferences: {}
users:
- name: admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUQ1VENDQXMyZ0F3SUJBZ0lVTFRCcGZSQURvMFlmUHBWNWdRREthWmRDQ3Rrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBd0dUT1R2bGtmUEwwWjllZkpIcURVWWtrRnRhWWVUYURNRFVBQVdtbUhNR3ZZbmJQCnZmU2JENGEvVHg0SEhmRmJoUWxHVElXSXY0RVgrcnZBRlpOYTRiQ1pxUUtSMFo5eUw5ejc3SW9ieEs3ZlZPYk8KVlJtdGRmL3lLVlVVY3gvM1NVUU
[root@k8s-master1 bin]# 


# 设置上下文参数，说明使用 cluster 集群和用户 admin
[root@k8s-master1 bin]# ./kubectl config set-context kubernetes --cluster=kubernetes --user=admin
Context "kubernetes" created.
[root@k8s-master1 bin]# cat ~/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://10.1.36.43:6443
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
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUQ1VENDQXMyZ0F3SUJBZ0lVTFRCcGZSQURvMFlmUHBWNWdRREthWmRDQ3Rrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBd0dUT1R2bGtmUEwwWjllZkpIcURVWWtrRnRhWWVUYURNRFVBQVdtbUhNR3ZZbmJQCnZmU2JENGEvVHg0SEhmRmJoUWxHVElXSXY0RVgrcnZBRlpOYTRiQ1pxUUtSMFo5eUw5ejc3SW9ieEs3ZlZPYk8KVlJtdGRmL3lLVlVVY3gvM1NVUU
[root@k8s-master1 bin]# 

# 选择默认上下文
[root@k8s-master1 bin]# ./kubectl config use-context kubernetes
Switched to context "kubernetes".
[root@k8s-master1 bin]# cat ~/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://10.1.36.43:6443
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
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUQ1VENDQXMyZ0F3SUJBZ0lVTFRCcGZSQURvMFlmUHBWNWdRREthWmRDQ3Rrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBd0dUT1R2bGtmUEwwWjllZkpIcURVWWtrRnRhWWVUYURNRFVBQVdtbUhNR3ZZbmJQCnZmU2JENGEvVHg0SEhmRmJoUWxHVElXSXY0RVgrcnZBRlpOYTRiQ1pxUUtSMFo5eUw5ejc3SW9ieEs3ZlZPYk8KVlJtdGRmL3lLVlVVY3gvM1NVUU
[root@k8s-master1 bin]# 

[root@k8s-master1 bin]# ./kubectl cluster-info
Kubernetes master is running at https://10.1.36.43:6443

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
[root@k8s-master1 bin]# 






# linux 网桥相关操作
$ brctl show
bridge name	bridge id		STP enabled	interfaces
docker0		8000.0242e0b35f6c	no		
mynet0		8000.7a584473c0b2	no		
 
$ brctl delbr mynet0
bridge mynet0 is still up; can't delete it

$ ifconfig mynet0
mynet0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 172.20.0.1  netmask 255.255.0.0  broadcast 172.20.255.255
        inet6 fe80::1064:b3ff:fe95:82fa  prefixlen 64  scopeid 0x20<link>
        ether 12:64:b3:95:82:fa  txqueuelen 1000  (Ethernet)
        RX packets 2  bytes 56 (56.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 8  bytes 648 (648.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


$ ifconfig mynet0 down

$ brctl show
bridge name	bridge id		STP enabled	interfaces
cni0		8000.46f5a3773999	no		veth26168cae
							veth62a55947
							vetha9fee21d
							vethd83107da
docker0		8000.0242efe67638	no		
mynet0		8000.1264b39582fa	no		

$ brctl delbr mynet0

$ brctl show
bridge name	bridge id		STP enabled	interfaces
cni0		8000.46f5a3773999	no		veth26168cae
							veth62a55947
							vetha9fee21d
							vethd83107da
docker0		8000.0242efe67638	no		
 







# 这个文件不需要
# 使 kubelet 设置 CNI 支持，cni 配置文件
[root@k8s-linux-worker1 k8s]# vim /opt/k8s/cni/net.d/10-default.conf
[root@k8s-linux-worker1 k8s]# cat /opt/k8s/cni/net.d/10-default.conf
{
  "name": "mynet",
  "type": "bridge",
  "bridge": "mynet0",
  "isDefaultGateway": true,
  "ipMasq": true,
  "hairpinMode": true,
  "ipam": {
    "type": "host-local",
    "subnet": "172.20.0.0/16"
  }
}
    
[root@k8s-linux-worker1 k8s]# 

# 这个镜像不需要
[root@k8s-linux-worker1 k8s]# docker pull mirrorgooglecontainers/pause-amd64:3.1
3.1: Pulling from mirrorgooglecontainers/pause-amd64
67ddbfb20a22: Pull complete 
Digest: sha256:59eec8837a4d942cc19a52b8c09ea75121acc38114a2c68b98983ce9356b8610
Status: Downloaded newer image for mirrorgooglecontainers/pause-amd64:3.1
[root@k8s-linux-worker1 k8s]# 
[root@k8s-linux-worker1 k8s]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
mirrorgooglecontainers/pause-amd64   3.1                 da86e6ba6ca1        17 months ago       742kB
[root@k8s-linux-worker1 k8s]# 
[root@k8s-linux-worker1 k8s]# 
[root@k8s-linux-worker1 k8s]# 


# https://github.com/kubernetes/kubernetes/issues/52711
# 准备 kubelet 证书签名请求，以 10.1.36.46 为例
[root@k8s-linux-worker1 ssl]# vim ./kubelet-csr.json 
[root@k8s-linux-worker1 ssl]# cat ./kubelet-csr.json 
{
  "CN": "system:node:10.1.36.46",
  "hosts": [
    "127.0.0.1",
    "10.1.36.46"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "system:nodes",
      "OU": "System"
    }
  ]
}
[root@k8s-linux-worker1 ssl]# 

# 准备 kubelet 证书签名请求，以 10.1.36.47 为例
[root@k8s-linux-worker1 ssl]# vim ./kubelet-csr.json 
[root@k8s-linux-worker1 ssl]# cat ./kubelet-csr.json 
{
  "CN": "system:node:10.1.36.47",
  "hosts": [
    "127.0.0.1",
    "10.1.36.47"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "system:nodes",
      "OU": "System"
    }
  ]
}

# 准备 kubelet 证书签名请求，以 10.1.36.48 为例
[root@k8s-linux-worker1 ssl]# vim ./kubelet-csr.json 
[root@k8s-linux-worker1 ssl]# cat ./kubelet-csr.json 
{
  "CN": "system:node:10.1.36.48",
  "hosts": [
    "127.0.0.1",
    "10.1.36.48"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "system:nodes",
      "OU": "System"
    }
  ]
}


[root@k8s-linux-worker1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes kubelet-csr.json | ./cfssljson -bare kubelet

kubelet-csr.json 

kubelet.csr
kubelet-key.pem
kubelet.pem


# 设置 kubelet 集群参数（apiserver 地址使用 nginx 负载均衡的 8443 端口）
# [root@k8s-linux-worker1 bin]# ./kubectl config set-cluster kubernetes --certificate-authority=/opt/k8s/ssl/ca.pem --embed-certs=true --server=https://10.1.36.43:6443 --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig
[root@k8s-linux-worker1 bin]# ./kubectl config set-cluster kubernetes --certificate-authority=/opt/k8s/ssl/ca.pem --embed-certs=true --server=https://127.0.0.1:8443 --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig
Cluster "kubernetes" set.
[root@k8s-linux-worker1 bin]# 
[root@k8s-linux-worker1 bin]# cat /opt/k8s/temp/ssl/kubelet.kubeconfig
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://127.0.0.1:8443
  name: kubernetes
contexts: []
current-context: ""
kind: Config
preferences: {}
users: []
[root@k8s-linux-worker1 bin]# 

# 设置 kubelet 客户端认证参数，以 10.1.36.46 为例
[root@k8s-linux-worker1 bin]# ./kubectl config set-credentials system:node:10.1.36.46 --client-certificate=/opt/k8s/ssl/kubelet.pem --embed-certs=true --client-key=/opt/k8s/ssl/kubelet-key.pem --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig
User "system:node:10.1.36.46" set.
[root@k8s-linux-worker1 bin]# 

# 设置 kubelet 客户端认证参数，以 10.1.36.47 为例
[root@k8s-linux-worker1 bin]# ./kubectl config set-credentials system:node:10.1.36.47 --client-certificate=/opt/k8s/ssl/kubelet.pem --embed-certs=true --client-key=/opt/k8s/ssl/kubelet-key.pem --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig

# 设置 kubelet 客户端认证参数，以 10.1.36.48 为例
[root@k8s-linux-worker1 bin]# ./kubectl config set-credentials system:node:10.1.36.48 --client-certificate=/opt/k8s/ssl/kubelet.pem --embed-certs=true --client-key=/opt/k8s/ssl/kubelet-key.pem --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig

[root@k8s-linux-worker1 bin]# cat /opt/k8s/temp/ssl/kubelet.kubeconfig
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://127.0.0.1:8443
  name: kubernetes
contexts: []
current-context: ""
kind: Config
preferences: {}
users:
- name: system:node:10.1.36.46
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUVCRENDQXV5Z0F3SUJBZ0lVWkUwaFdiQnN0aC9BTFA3U0pQWEdFQzZ2OFA0d0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBdXhxalFsR3RhTGVIUzdYay9WSXNBTDk0Q2NnSW4wYXEvbDZzaUNkSTdraU0yRmE2ClBJRTFEZENRYUs2U3QvSUtWSWVEb29UVkg4UEJ6aGN0YWgweTY2KzJVQTRicWhjTm5va2hXNGdHMTYvTE1VRHgKanFsNms1ektCTXhxN2hkMHFWcm
[root@k8s-linux-worker1 bin]# 

# 设置 kubelet 上下文参数，以 10.1.36.46 为例
[root@k8s-linux-worker1 bin]# ./kubectl config set-context default --cluster=kubernetes --user=system:node:10.1.36.46 --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig
Context "default" created.
[root@k8s-linux-worker1 bin]# 

# 设置 kubelet 上下文参数，以 10.1.36.47 为例
[root@k8s-linux-worker1 bin]# ./kubectl config set-context default --cluster=kubernetes --user=system:node:10.1.36.47 --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig

# 设置 kubelet 上下文参数，以 10.1.36.48 为例
[root@k8s-linux-worker1 bin]# ./kubectl config set-context default --cluster=kubernetes --user=system:node:10.1.36.48 --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig


[root@k8s-linux-worker1 bin]# cat /opt/k8s/temp/ssl/kubelet.kubeconfig
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://127.0.0.1:8443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: system:node:10.1.36.46
  name: default
current-context: ""
kind: Config
preferences: {}
users:
- name: system:node:10.1.36.46
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUVCRENDQXV5Z0F3SUJBZ0lVWkUwaFdiQnN0aC9BTFA3U0pQWEdFQzZ2OFA0d0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBdXhxalFsR3RhTGVIUzdYay9WSXNBTDk0Q2NnSW4wYXEvbDZzaUNkSTdraU0yRmE2ClBJRTFEZENRYUs2U3QvSUtWSWVEb29UVkg4UEJ6aGN0YWgweTY2KzJVQTRicWhjTm5va2hXNGdHMTYvTE1VRHgKanFsNms1ektCTXhxN2hkMHFWcm
[root@k8s-linux-worker1 bin]# 

# 选择默认上下文
[root@k8s-linux-worker1 bin]# ./kubectl config use-context default --kubeconfig=/opt/k8s/temp/ssl/kubelet.kubeconfig
Switched to context "default".
[root@k8s-linux-worker1 bin]# cat /opt/k8s/temp/ssl/kubelet.kubeconfig
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://127.0.0.1:8443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: system:node:10.1.36.46
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: system:node:10.1.36.46
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUVCRENDQXV5Z0F3SUJBZ0lVWkUwaFdiQnN0aC9BTFA3U0pQWEdFQzZ2OFA0d0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBdXhxalFsR3RhTGVIUzdYay9WSXNBTDk0Q2NnSW4wYXEvbDZzaUNkSTdraU0yRmE2ClBJRTFEZENRYUs2U3QvSUtWSWVEb29UVkg4UEJ6aGN0YWgweTY2KzJVQTRicWhjTm5va2hXNGdHMTYvTE1VRHgKanFsNms1ektCTXhxN2hkMHFWcm
[root@k8s-linux-worker1 bin]# 

[root@k8s-linux-worker2 temp]# cp bridge /opt/k8s/bin/
[root@k8s-linux-worker2 temp]# cp host-local /opt/k8s/bin/
[root@k8s-linux-worker2 temp]# cp loopback /opt/k8s/bin/
[root@k8s-linux-worker2 temp]# cp flannel /opt/k8s/bin/
[root@k8s-linux-worker2 temp]# cp portmap /opt/k8s/bin/
[root@k8s-linux-worker2 temp]# 



10.1.36.46
10.1.36.47
10.1.36.48
10.1.36.49


mkdir -p /opt/k8s/kubelet

mkdir -p /opt/k8s/cni/net.d
10-default.conf


/opt/k8s/bin
kubelet

/opt/k8s/ssl
ca.pem
ca-key.pem
kubelet.pem
kubelet-key.pem
kubelet.kubeconfig

/opt/k8s/log/
Kubelet.log

docker 镜像
k8s.gcr.io/pause:3.1
mirrorgooglecontainers/pause-amd64:3.1


# 创建 kubelet 的systemd unit文件，以 10.1.36.46 为例
[root@k8s-linux-worker1 bin]# vim /etc/systemd/system/kubelet.service
[root@k8s-linux-worker1 bin]# cat /etc/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
WorkingDirectory=/opt/k8s/kubelet
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/cpuset/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/hugetlb/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/memory/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/pids/system.slice/kubelet.service
ExecStart=/opt/k8s/bin/kubelet \
  --address=10.1.36.46 \
  --allow-privileged=true \
  --anonymous-auth=false \
  --authentication-token-webhook \
  --authorization-mode=Webhook \
  --client-ca-file=/opt/k8s/ssl/ca.pem \
  --cluster-dns=10.68.0.2 \
  --cluster-domain=cluster.local. \
  --cni-bin-dir=/opt/k8s/bin \
  --cni-conf-dir=/opt/k8s/cni/net.d \
  --fail-swap-on=false \
  --hairpin-mode hairpin-veth \
  --hostname-override=10.1.36.46 \
  --kubeconfig=/opt/k8s/ssl/kubelet.kubeconfig \
  --max-pods=110 \
  --network-plugin=cni \
  --pod-infra-container-image=k8s.gcr.io/pause:3.1 \
  --register-node=true \
  --root-dir=/opt/k8s/kubelet \
  --tls-cert-file=/opt/k8s/ssl/kubelet.pem \
  --tls-private-key-file=/opt/k8s/ssl/kubelet-key.pem \
  --cgroups-per-qos=true \
  --cgroup-driver=cgroupfs \
  --enforce-node-allocatable=pods,kube-reserved \
  --kube-reserved=cpu=200m,memory=500Mi,ephemeral-storage=1Gi \
  --kube-reserved-cgroup=/system.slice/kubelet.service \
  --eviction-hard=memory.available<200Mi,nodefs.available<10% \
  --log-file=/opt/k8s/log/Kubelet.log \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
[root@k8s-linux-worker1 bin]# 


# 创建 kubelet 的systemd unit文件，以 10.1.36.47 为例
[root@k8s-linux-worker1 bin]# vim /etc/systemd/system/kubelet.service
[root@k8s-linux-worker1 bin]# cat /etc/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
WorkingDirectory=/opt/k8s/kubelet
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/cpuset/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/hugetlb/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/memory/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/pids/system.slice/kubelet.service
ExecStart=/opt/k8s/bin/kubelet \
  --address=10.1.36.47 \
  --allow-privileged=true \
  --anonymous-auth=false \
  --authentication-token-webhook \
  --authorization-mode=Webhook \
  --client-ca-file=/opt/k8s/ssl/ca.pem \
  --cluster-dns=10.68.0.2 \
  --cluster-domain=cluster.local. \
  --cni-bin-dir=/opt/k8s/bin \
  --cni-conf-dir=/opt/k8s/cni/net.d \
  --fail-swap-on=false \
  --hairpin-mode hairpin-veth \
  --hostname-override=10.1.36.47 \
  --kubeconfig=/opt/k8s/ssl/kubelet.kubeconfig \
  --max-pods=110 \
  --network-plugin=cni \
  --pod-infra-container-image=k8s.gcr.io/pause:3.1 \
  --register-node=true \
  --root-dir=/opt/k8s/kubelet \
  --tls-cert-file=/opt/k8s/ssl/kubelet.pem \
  --tls-private-key-file=/opt/k8s/ssl/kubelet-key.pem \
  --cgroups-per-qos=true \
  --cgroup-driver=cgroupfs \
  --enforce-node-allocatable=pods,kube-reserved \
  --kube-reserved=cpu=200m,memory=500Mi,ephemeral-storage=1Gi \
  --kube-reserved-cgroup=/system.slice/kubelet.service \
  --eviction-hard=memory.available<200Mi,nodefs.available<10% \
  --log-file=/opt/k8s/log/Kubelet.log \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

# 创建 kubelet 的systemd unit文件，以 10.1.36.48 为例
[root@k8s-linux-worker1 bin]# vim /etc/systemd/system/kubelet.service
[root@k8s-linux-worker1 bin]# cat /etc/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
WorkingDirectory=/opt/k8s/kubelet
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/cpuset/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/hugetlb/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/memory/system.slice/kubelet.service
ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/pids/system.slice/kubelet.service
ExecStart=/opt/k8s/bin/kubelet \
  --address=10.1.36.48 \
  --allow-privileged=true \
  --anonymous-auth=false \
  --authentication-token-webhook \
  --authorization-mode=Webhook \
  --client-ca-file=/opt/k8s/ssl/ca.pem \
  --cluster-dns=10.68.0.2 \
  --cluster-domain=cluster.local. \
  --cni-bin-dir=/opt/k8s/bin \
  --cni-conf-dir=/opt/k8s/cni/net.d \
  --fail-swap-on=false \
  --hairpin-mode hairpin-veth \
  --hostname-override=10.1.36.48 \
  --kubeconfig=/opt/k8s/ssl/kubelet.kubeconfig \
  --max-pods=110 \
  --network-plugin=cni \
  --pod-infra-container-image=k8s.gcr.io/pause:3.1 \
  --register-node=true \
  --root-dir=/opt/k8s/kubelet \
  --tls-cert-file=/opt/k8s/ssl/kubelet.pem \
  --tls-private-key-file=/opt/k8s/ssl/kubelet-key.pem \
  --cgroups-per-qos=true \
  --cgroup-driver=cgroupfs \
  --enforce-node-allocatable=pods,kube-reserved \
  --kube-reserved=cpu=200m,memory=500Mi,ephemeral-storage=1Gi \
  --kube-reserved-cgroup=/system.slice/kubelet.service \
  --eviction-hard=memory.available<200Mi,nodefs.available<10% \
  --log-file=/opt/k8s/log/Kubelet.log \
  --v=2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

systemctl enable kubelet.service （ systemctl disable kubelet.service ）
systemctl daemon-reload
systemctl restart kubelet.service
systemctl status kubelet.service


[root@k8s-linux-worker1 bin]# netstat -tulnp | grep kubelet
tcp        0      0 127.0.0.1:45125         0.0.0.0:*               LISTEN      53132/kubelet       
tcp        0      0 127.0.0.1:10248         0.0.0.0:*               LISTEN      53132/kubelet       
tcp        0      0 10.1.36.46:10250        0.0.0.0:*               LISTEN      53132/kubelet       
tcp        0      0 10.1.36.46:10255        0.0.0.0:*               LISTEN      53132/kubelet       
[root@k8s-linux-worker1 bin]# 








# 准备 kube-proxy 证书签名请求
[root@k8s-linux-worker1 ssl]# vim ./kube-proxy-csr.json
[root@k8s-linux-worker1 ssl]# cat ./kube-proxy-csr.json
{
  "CN": "system:kube-proxy",
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
      "O": "k8s",
      "OU": "System"
    }
  ]
}
[root@k8s-linux-worker1 ssl]# 

# 创建 kube-proxy 证书与私钥
[root@k8s-linux-worker1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes kube-proxy-csr.json | ./cfssljson -bare kube-proxy

kube-proxy-csr.json

kube-proxy.csr
kube-proxy-key.pem
kube-proxy.pem

# 为 kube-proxy 设置集群参数，参数保存到 kube-proxy.kubeconfig 文件中（apiserver 地址使用 nginx 负载均衡的 8443 端口）
# [root@k8s-linux-worker1 bin]# ./kubectl config set-cluster kubernetes --certificate-authority=/opt/k8s/ssl/ca.pem --embed-certs=true --server=https://10.1.36.43:6443 --kubeconfig=/opt/k8s/temp/ssl/kube-proxy.kubeconfig
[root@k8s-linux-worker1 bin]# ./kubectl config set-cluster kubernetes --certificate-authority=/opt/k8s/ssl/ca.pem --embed-certs=true --server=https://127.0.0.1:8443 --kubeconfig=/opt/k8s/temp/ssl/kube-proxy.kubeconfig
Cluster "kubernetes" set.
[root@k8s-linux-worker1 bin]# 

# 设置 kube-proxy 认证参数
[root@k8s-linux-worker1 bin]# ./kubectl config set-credentials kube-proxy --client-certificate=/opt/k8s/ssl/kube-proxy.pem --client-key=/opt/k8s/ssl/kube-proxy-key.pem --embed-certs=true --kubeconfig=/opt/k8s/temp/ssl/kube-proxy.kubeconfig
User "kube-proxy" set.
[root@k8s-linux-worker1 bin]# 

# 设置上下文参数
[root@k8s-linux-worker1 bin]# ./kubectl config set-context default --cluster=kubernetes --user=kube-proxy --kubeconfig=/opt/k8s/temp/ssl/kube-proxy.kubeconfig
Context "default" created.
[root@k8s-linux-worker1 bin]# 

# 选择默认上下文
[root@k8s-linux-worker1 bin]# ./kubectl config use-context default --kubeconfig=/opt/k8s/temp/ssl/kube-proxy.kubeconfig
Switched to context "default".
[root@k8s-linux-worker1 bin]# 




mkdir -p /opt/k8s/kube-proxy

/opt/k8s/bin/
kube-proxy

/opt/k8s/ssl/
kube-proxy.kubeconfig

# 创建 kube-proxy 服务文件，以 10.1.36.46 为例
[root@k8s-linux-worker1 bin]# vim /etc/systemd/system/kube-proxy.service
[root@k8s-linux-worker1 bin]# 
[root@k8s-linux-worker1 bin]# cat /etc/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube-Proxy Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
WorkingDirectory=/opt/k8s/kube-proxy
ExecStart=/opt/k8s/bin/kube-proxy \
  --bind-address=10.1.36.46 \
  --hostname-override=10.1.36.46 \
  --kubeconfig=/opt/k8s/ssl/kube-proxy.kubeconfig \
  --logtostderr=true \
  --proxy-mode=iptables
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
[root@k8s-linux-worker1 bin]# 


# 创建 kube-proxy 服务文件，以 10.1.36.47 为例
[root@k8s-linux-worker1 bin]# vim /etc/systemd/system/kube-proxy.service
[root@k8s-linux-worker1 bin]# 
[root@k8s-linux-worker1 bin]# cat /etc/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube-Proxy Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
WorkingDirectory=/opt/k8s/kube-proxy
ExecStart=/opt/k8s/bin/kube-proxy \
  --bind-address=10.1.36.47 \
  --hostname-override=10.1.36.47 \
  --kubeconfig=/opt/k8s/ssl/kube-proxy.kubeconfig \
  --logtostderr=true \
  --proxy-mode=iptables
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
[root@k8s-linux-worker1 bin]# 


# 创建 kube-proxy 服务文件，以 10.1.36.48 为例
[root@k8s-linux-worker1 bin]# vim /etc/systemd/system/kube-proxy.service
[root@k8s-linux-worker1 bin]# 
[root@k8s-linux-worker1 bin]# cat /etc/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube-Proxy Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
WorkingDirectory=/opt/k8s/kube-proxy
ExecStart=/opt/k8s/bin/kube-proxy \
  --bind-address=10.1.36.48 \
  --hostname-override=10.1.36.48 \
  --kubeconfig=/opt/k8s/ssl/kube-proxy.kubeconfig \
  --logtostderr=true \
  --proxy-mode=iptables
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
[root@k8s-linux-worker1 bin]# 


systemctl enable kube-proxy.service （ systemctl disable kube-proxy.service ）
systemctl daemon-reload
systemctl restart kube-proxy.service
systemctl status kube-proxy.service

[root@k8s-linux-worker1 bin]# netstat -tulnp | grep kube-proxy
tcp        0      0 127.0.0.1:10249         0.0.0.0:*               LISTEN      55989/kube-proxy    
tcp6       0      0 :::10256                :::*                    LISTEN      55989/kube-proxy    
[root@k8s-linux-worker1 bin]# 

kubectl api-resources


```



### 部署 flannel

```bash

# 参考 https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/

flannel 部署以下资源
PodSecurityPolicy
ClusterRole
ClusterRoleBinding
ServiceAccount
ConfigMap
DaemonSet

[root@k8s-master1 temp]# kubectl apply -f ./kube-flannel.yml 
podsecuritypolicy.extensions/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.extensions/kube-flannel-ds-amd64 created
daemonset.extensions/kube-flannel-ds-arm64 created
daemonset.extensions/kube-flannel-ds-arm created
daemonset.extensions/kube-flannel-ds-ppc64le created
daemonset.extensions/kube-flannel-ds-s390x created

[root@k8s-master1 ~]# kubectl get PodSecurityPolicy 
NAME                       PRIV    CAPS        SELINUX    RUNASUSER   FSGROUP    SUPGROUP   READONLYROOTFS   VOLUMES
psp.flannel.unprivileged   false   NET_ADMIN   RunAsAny   RunAsAny    RunAsAny   RunAsAny   false            configMap,secret,emptyDir,hostPath
[root@k8s-master1 ~]# 

[root@k8s-master1 ~]# kubectl get ClusterRole --all-namespaces
NAME                                                                   AGE
admin                                                                  2d19h
cluster-admin                                                          2d19h
edit                                                                   2d19h
flannel                                                                2d15h
system:aggregate-to-admin                                              2d19h
system:aggregate-to-edit                                               2d19h
system:aggregate-to-view                                               2d19h
system:auth-delegator                                                  2d19h
system:aws-cloud-provider                                              2d19h
system:basic-user                                                      2d19h
system:certificates.k8s.io:certificatesigningrequests:nodeclient       2d19h
system:certificates.k8s.io:certificatesigningrequests:selfnodeclient   2d19h
system:controller:attachdetach-controller                              2d19h
system:controller:certificate-controller                               2d19h
system:controller:clusterrole-aggregation-controller                   2d19h
system:controller:cronjob-controller                                   2d19h
system:controller:daemon-set-controller                                2d19h
system:controller:deployment-controller                                2d19h
system:controller:disruption-controller                                2d19h
system:controller:endpoint-controller                                  2d19h
system:controller:expand-controller                                    2d19h
system:controller:generic-garbage-collector                            2d19h
system:controller:horizontal-pod-autoscaler                            2d19h
system:controller:job-controller                                       2d19h
system:controller:namespace-controller                                 2d19h
system:controller:node-controller                                      2d19h
system:controller:persistent-volume-binder                             2d19h
system:controller:pod-garbage-collector                                2d19h
system:controller:pv-protection-controller                             2d19h
system:controller:pvc-protection-controller                            2d19h
system:controller:replicaset-controller                                2d19h
system:controller:replication-controller                               2d19h
system:controller:resourcequota-controller                             2d19h
system:controller:route-controller                                     2d19h
system:controller:service-account-controller                           2d19h
system:controller:service-controller                                   2d19h
system:controller:statefulset-controller                               2d19h
system:controller:ttl-controller                                       2d19h
system:csi-external-attacher                                           2d19h
system:csi-external-provisioner                                        2d19h
system:discovery                                                       2d19h
system:heapster                                                        2d19h
system:kube-aggregator                                                 2d19h
system:kube-controller-manager                                         2d19h
system:kube-dns                                                        2d19h
system:kube-scheduler                                                  2d19h
system:kubelet-api-admin                                               2d19h
system:node                                                            2d19h
system:node-bootstrapper                                               2d19h
system:node-problem-detector                                           2d19h
system:node-proxier                                                    2d19h
system:persistent-volume-provisioner                                   2d19h
system:public-info-viewer                                              2d19h
system:volume-scheduler                                                2d19h
view                                                                   2d19h
[root@k8s-master1 ~]# 

[root@k8s-master1 ~]# kubectl get ClusterRoleBinding --all-namespaces
NAME                                                   AGE
cluster-admin                                          2d19h
flannel                                                2d15h
system:aws-cloud-provider                              2d19h
system:basic-user                                      2d19h
system:controller:attachdetach-controller              2d19h
system:controller:certificate-controller               2d19h
system:controller:clusterrole-aggregation-controller   2d19h
system:controller:cronjob-controller                   2d19h
system:controller:daemon-set-controller                2d19h
system:controller:deployment-controller                2d19h
system:controller:disruption-controller                2d19h
system:controller:endpoint-controller                  2d19h
system:controller:expand-controller                    2d19h
system:controller:generic-garbage-collector            2d19h
system:controller:horizontal-pod-autoscaler            2d19h
system:controller:job-controller                       2d19h
system:controller:namespace-controller                 2d19h
system:controller:node-controller                      2d19h
system:controller:persistent-volume-binder             2d19h
system:controller:pod-garbage-collector                2d19h
system:controller:pv-protection-controller             2d19h
system:controller:pvc-protection-controller            2d19h
system:controller:replicaset-controller                2d19h
system:controller:replication-controller               2d19h
system:controller:resourcequota-controller             2d19h
system:controller:route-controller                     2d19h
system:controller:service-account-controller           2d19h
system:controller:service-controller                   2d19h
system:controller:statefulset-controller               2d19h
system:controller:ttl-controller                       2d19h
system:discovery                                       2d19h
system:kube-controller-manager                         2d19h
system:kube-dns                                        2d19h
system:kube-scheduler                                  2d19h
system:node                                            2d19h
system:node-proxier                                    2d19h
system:public-info-viewer                              2d19h
system:volume-scheduler                                2d19h
[root@k8s-master1 ~]# 

[root@k8s-master1 ~]# kubectl get ServiceAccount --all-namespaces
NAMESPACE         NAME                   SECRETS   AGE
default           default                1         2d18h
kube-node-lease   default                1         2d18h
kube-public       default                1         2d18h
kube-system       default                1         2d18h
kube-system       flannel                1         2d15h
kube-system       kubernetes-dashboard   1         2d15h
[root@k8s-master1 ~]# 

[root@k8s-master1 ~]# kubectl get ConfigMap --all-namespaces
NAMESPACE     NAME                                 DATA   AGE
kube-system   extension-apiserver-authentication   6      2d19h
kube-system   kube-flannel-cfg                     2      2d15h
[root@k8s-master1 ~]# 

[root@k8s-master1 temp]# kubectl get daemonsets --all-namespaces
NAMESPACE     NAME                      DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                     AGE
kube-system   kube-flannel-ds-amd64     1         1         0       1            0           beta.kubernetes.io/arch=amd64     2m41s
kube-system   kube-flannel-ds-arm       0         0         0       0            0           beta.kubernetes.io/arch=arm       2m41s
kube-system   kube-flannel-ds-arm64     0         0         0       0            0           beta.kubernetes.io/arch=arm64     2m41s
kube-system   kube-flannel-ds-ppc64le   0         0         0       0            0           beta.kubernetes.io/arch=ppc64le   2m41s
kube-system   kube-flannel-ds-s390x     0         0         0       0            0           beta.kubernetes.io/arch=s390x     2m41s
[root@k8s-master1 temp]# 

# 修改 ./kube-flannel.yml 文件，指定网段为：172.20.0.0/16，重新部署
[root@k8s-master1 temp]# kubectl apply -f ./kube-flannel.yml 
podsecuritypolicy.extensions/psp.flannel.unprivileged configured
clusterrole.rbac.authorization.k8s.io/flannel unchanged
clusterrolebinding.rbac.authorization.k8s.io/flannel unchanged
serviceaccount/flannel unchanged
configmap/kube-flannel-cfg configured ## 修改
daemonset.extensions/kube-flannel-ds-amd64 unchanged
daemonset.extensions/kube-flannel-ds-arm64 unchanged
daemonset.extensions/kube-flannel-ds-arm unchanged
daemonset.extensions/kube-flannel-ds-ppc64le unchanged
daemonset.extensions/kube-flannel-ds-s390x unchanged
[root@k8s-master1 temp]# 


# 启动 flannel 相关 pod 错误
[root@k8s-master1 temp]# kubectl get pods --all-namespaces
NAMESPACE     NAME                          READY   STATUS             RESTARTS   AGE
kube-system   kube-flannel-ds-amd64-vlwws   0/1     CrashLoopBackOff   4          2m44s
[root@k8s-master1 temp]# 

# 排查 pod 启动错误
kubectl describe pod kube-flannel-ds-amd64-vlwws -n kube-system

kubectl logs kube-flannel-ds-amd64-vlwws -n kube-system

[root@k8s-master1 temp]# kubectl logs kube-flannel-ds-amd64-vlwws -n kube-system
I0521 12:11:07.515060       1 main.go:514] Determining IP address of default interface
I0521 12:11:07.516002       1 main.go:527] Using interface with name eth0 and address 10.1.36.46
I0521 12:11:07.516065       1 main.go:544] Defaulting external address to interface address (10.1.36.46)
E0521 12:11:07.719918       1 main.go:241] Failed to create SubnetManager: error retrieving pod spec for 'kube-system/kube-flannel-ds-amd64-vlwws': Get https://10.68.0.1:443/api/v1/namespaces/kube-system/pods/kube-flannel-ds-amd64-vlwws: x509: certificate is valid for 127.0.0.1, 10.1.36.43, 10.1.36.44, 10.1.36.45, 10.68.0.2, not 10.68.0.1
[root@k8s-master1 temp]# 

# 10.68.0.1 验证失败
# 在 hosts 中增加 10.68.0.1
[root@k8s-master1 ssl]# vim ./kubernetes-csr.json
[root@k8s-master1 ssl]# cat ./kubernetes-csr.json
{
  "CN": "kubernetes",
  "hosts": [
    "127.0.0.1",
    "10.1.36.43",
    "10.1.36.44",
    "10.1.36.45",
    "10.68.0.2",
    "10.68.0.1",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
[root@k8s-master1 ssl]# 

# 重启服务

[root@k8s-master1 ssl]# kubectl get pods --all-namespaces
NAMESPACE     NAME                                    READY   STATUS              RESTARTS   AGE
kube-system   kube-flannel-ds-amd64-vlwws             1/1     Running             16         58m
[root@k8s-master1 ssl]# 



# 修改 flannel 挂载目录

```




### 部署 dashboard

```bash

# 参考 https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
# 参考 http://dockone.io/article/4884

Dashboard 部署以下资源 
Secrets
ServiceAccount
Role & Role Binding
Deployment
Service

[root@k8s-master1 temp]# kubectl apply -f ./kubernetes-dashboard.yaml 
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
serviceaccount/kubernetes-dashboard created
role.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
deployment.apps/kubernetes-dashboard created
service/kubernetes-dashboard created
[root@k8s-master1 temp]# 

# 修改 service type 为 NodePort
[root@k8s-master1 temp]# kubectl get service --all-namespaces
NAMESPACE     NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
default       kubernetes             ClusterIP   10.68.0.1       <none>        443/TCP   3h38m
kube-system   kubernetes-dashboard   ClusterIP   10.68.173.192   <none>        443/TCP   97s
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl --namespace=kube-system get service kubernetes-dashboard -o yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"k8s-app":"kubernetes-dashboard"},"name":"kubernetes-dashboard","namespace":"kube-system"},"spec":{"ports":[{"port":443,"targetPort":8443}],"selector":{"k8s-app":"kubernetes-dashboard"}}}
  creationTimestamp: "2019-05-21T11:42:49Z"
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
  resourceVersion: "22524"
  selfLink: /api/v1/namespaces/kube-system/services/kubernetes-dashboard
  uid: 8f8f4ea1-7bbd-11e9-8eb2-0017fa00a076
spec:
  clusterIP: 10.68.173.192
  ports:
  - port: 443
    protocol: TCP
    targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# kubectl --namespace=kube-system edit service kubernetes-dashboard
service/kubernetes-dashboard edited
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl --namespace=kube-system get service kubernetes-dashboard -o yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"k8s-app":"kubernetes-dashboard"},"name":"kubernetes-dashboard","namespace":"kube-system"},"spec":{"ports":[{"port":443,"targetPort":8443}],"selector":{"k8s-app":"kubernetes-dashboard"}}}
  creationTimestamp: "2019-05-21T11:42:49Z"
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
  resourceVersion: "23273"
  selfLink: /api/v1/namespaces/kube-system/services/kubernetes-dashboard
  uid: 8f8f4ea1-7bbd-11e9-8eb2-0017fa00a076
spec:
  clusterIP: 10.68.173.192
  externalTrafficPolicy: Cluster
  ports:
  - nodePort: 29118
    port: 443
    protocol: TCP
    targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  sessionAffinity: None
  type: NodePort
status:
  loadBalancer: {}
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# kubectl --namespace=kube-system get service kubernetes-dashboard
NAME                   TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
kubernetes-dashboard   NodePort   10.68.173.192   <none>        443:29118/TCP   9m59s
[root@k8s-master1 temp]# 

# 访问地址
https://139.217.0.156:29118/
http://10.1.36.43:29118/

http://139.217.6.21:29118/
http://10.1.36.46:29118/

# 检查 dashboard 相关 pod 状态
[root@k8s-master1 ssl]# kubectl get pods --all-namespaces
NAMESPACE     NAME                                    READY   STATUS              RESTARTS   AGE
kube-system   kube-flannel-ds-amd64-vlwws             1/1     Running             16         58m
kube-system   kubernetes-dashboard-5f7b999d65-9xqtz   0/1     ContainerCreating   0          50m
[root@k8s-master1 ssl]# 

[root@k8s-master1 ssl]# kubectl logs kubernetes-dashboard-5f7b999d65-9xqtz -n kube-system
Error from server (BadRequest): container "kubernetes-dashboard" in pod "kubernetes-dashboard-5f7b999d65-9xqtz" is waiting to start: ContainerCreating
[root@k8s-master1 ssl]# 
# 查看 pod 相关联的 event
[root@k8s-master1 temp]# kubectl describe pod kubernetes-dashboard-5f7b999d65-52qzn --namespace=kube-system

Events:
  Type     Reason                  Age                   From                 Message

----     ------                  ----                  ----                 -------
  Normal   Scheduled               5m27s                 default-scheduler    Successfully assigned kube-system/kubernetes-dashboard-5f7b999d65-52qzn to 10.1.36.46
  Warning  FailedCreatePodSandBox  5m25s                 kubelet, 10.1.36.46  Failed create pod sandbox: rpc error: code = Unknown desc = [failed to set up sandbox container "fd1ea6ccf31d86cfe17163190a45d3683174de9803ec74b3b970b528a9e7a4e2" network for pod "kubernetes-dashboard-5f7b999d65-52qzn": NetworkPlugin cni failed to set up pod "kubernetes-dashboard-5f7b999d65-52qzn_kube-system" network: failed to find plugin "loopback" in path [/opt/k8s/bin], failed to clean up sandbox container "fd1ea6ccf31d86cfe17163190a45d3683174de9803ec74b3b970b528a9e7a4e2" network for pod "kubernetes-dashboard-5f7b999d65-52qzn": NetworkPlugin cni failed to teardown pod "kubernetes-dashboard-5f7b999d65-52qzn_kube-system" network: failed to find plugin "bridge" in path [/opt/k8s/bin]]
  Normal   SandboxChanged          18s (x26 over 5m24s)  kubelet, 10.1.36.46  Pod sandbox changed, it will be killed and re-created.
[root@k8s-master1 temp]# 

# 相关工具没有找到
# 在 /opt/k8s/bin/ 目录中增加 bridge、host-local、loopback、flannel、portmap 工具
[root@k8s-linux-worker1 temp]# ll /opt/k8s/bin/
total 180236
-rwxr-xr-x 1 root root   5009327 May 21 21:43 bridge
-rwxr-xr-x 1 root root   3069034 May 21 22:15 flannel
-rwxr-xr-x 1 root root   3957620 May 21 22:09 host-local
-rwxr-xr-x 1 root root 127850432 May 21 17:32 kubelet
-rwxr-xr-x 1 root root  36681344 May 21 18:38 kube-proxy
-rwxr-xr-x 1 root root   3650379 May 21 22:09 loopback
-rwxr-xr-x 1 root root   4327403 May 21 22:17 portmap
[root@k8s-linux-worker1 temp]# 

[root@k8s-master1 ~]# kubectl get pods --all-namespaces
NAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGE
kube-system   kube-flannel-ds-amd64-vlwws             1/1     Running   0          2d16h
kube-system   kubernetes-dashboard-5f7b999d65-52qzn   1/1     Running   0          2d14h
[root@k8s-master1 ~]# 


# 检查网络是否可用
[root@k8s-master1 ~]# kubectl describe pod --namespace kube-system kubernetes-dashboard-5f7b999d65-52qzn
Name:           kubernetes-dashboard-5f7b999d65-52qzn
Namespace:      kube-system
Node:           10.1.36.46/10.1.36.46
Start Time:     Tue, 21 May 2019 21:35:47 +0800
Labels:         k8s-app=kubernetes-dashboard
                pod-template-hash=5f7b999d65
Annotations:    <none>
Status:         Running
IP:             172.20.0.2
Controlled By:  ReplicaSet/kubernetes-dashboard-5f7b999d65
Containers:
  kubernetes-dashboard:
    Container ID:  docker://9f2d1b2a6bba0874ade8776113ce48b7e35eb295c9cab263c2a5c81d4c4241c4
    Image:         k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1
    Image ID:      docker://sha256:f9aed6605b814b69e92dece6a50ed1e4e730144eb1cc971389dde9cb3820d124
    Port:          8443/TCP
    Host Port:     0/TCP
    Args:
      --auto-generate-certificates
    State:          Running
      Started:      Tue, 21 May 2019 22:10:09 +0800
    Ready:          True
    Restart Count:  0
    Liveness:       http-get https://:8443/ delay=30s timeout=30s period=10s #success=1 #failure=3
    Environment:    <none>
    Mounts:
      /certs from kubernetes-dashboard-certs (rw)
      /tmp from tmp-volume (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kubernetes-dashboard-token-w6fdt (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kubernetes-dashboard-certs:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kubernetes-dashboard-certs
    Optional:    false
  tmp-volume:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     
    SizeLimit:  <unset>
  kubernetes-dashboard-token-w6fdt:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kubernetes-dashboard-token-w6fdt
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node-role.kubernetes.io/master:NoSchedule
Events:          <none>
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# ping 172.20.0.2
PING 172.20.0.2 (172.20.0.2) 56(84) bytes of data.
^C
--- 172.20.0.2 ping statistics ---
4 packets transmitted, 0 received, 100% packet loss, time 2999ms

[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# ping 172.20.0.2
PING 172.20.0.2 (172.20.0.2) 56(84) bytes of data.
^C
--- 172.20.0.2 ping statistics ---
17 packets transmitted, 0 received, 100% packet loss, time 15999ms

[root@k8s-master1 ~]# 


[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# pwd
/opt/k8s/cni/net.d
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# mv 10-default.conf 10-default.conf_back
[root@k8s-linux-worker1 net.d]# cat  10-default.conf_back
{
  "name": "mynet",
  "type": "bridge",
  "bridge": "mynet0",
  "isDefaultGateway": true,
  "ipMasq": true,
  "hairpinMode": true,
  "ipam": {
    "type": "host-local",
    "subnet": "172.20.0.0/16"
  }
}
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# pwd
/opt/k8s/cni/net.d
[root@k8s-linux-worker1 net.d]# systemctl restart kubelet.service
[root@k8s-linux-worker1 net.d]# systemctl status kubelet.service
● kubelet.service - Kubernetes Kubelet
   Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2019-05-24 14:26:49 CST; 7s ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
  Process: 49050 ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/pids/system.slice/kubelet.service (code=exited, status=0/SUCCESS)
  Process: 49046 ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/memory/system.slice/kubelet.service (code=exited, status=0/SUCCESS)
  Process: 49043 ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/hugetlb/system.slice/kubelet.service (code=exited, status=0/SUCCESS)
  Process: 49040 ExecStartPre=/bin/mkdir -p /sys/fs/cgroup/cpuset/system.slice/kubelet.service (code=exited, status=0/SUCCESS)
 Main PID: 49054 (kubelet)
    Tasks: 25
   Memory: 32.1M
   CGroup: /system.slice/kubelet.service
           └─49054 /opt/k8s/bin/kubelet --address=10.1.36.46 --allow-privileged=true --anonymous-auth=false --authentication-token-webhook --authorization-mode=Webhook --client-ca-file=/opt/k8s/ssl/ca.pem --cluster-dns=10.68.0.2 --cluster-domain=cluster.local. --cni-...

May 24 14:26:49 k8s-linux-worker1 kubelet[49054]: I0524 14:26:49.962306   49054 reconciler.go:252] operationExecutor.MountVolume started for volume "tmp-volume" (UniqueName: "kubernetes.io/empty-dir/578ed9bb-7bcd-11e9-8f1f-0017fa00a076-tmp-volume")...8f1f-0017fa00a076")
May 24 14:26:49 k8s-linux-worker1 kubelet[49054]: I0524 14:26:49.962547   49054 operation_generator.go:669] MountVolume.SetUp succeeded for volume "tmp-volume" (UniqueName: "kubernetes.io/empty-dir/578ed9bb-7bcd-11e9-8f1f-0017fa00a076-tmp-volume") ...8f1f-0017fa00a076")
May 24 14:26:49 k8s-linux-worker1 kubelet[49054]: I0524 14:26:49.962570   49054 operation_generator.go:669] MountVolume.SetUp succeeded for volume "kubernetes-dashboard-certs" (UniqueName: "kubernetes.io/secret/578ed9bb-7bcd-11e9-8f1f-0017fa00a076-kubernetes-dashboar...
May 24 14:26:49 k8s-linux-worker1 kubelet[49054]: I0524 14:26:49.963322   49054 operation_generator.go:669] MountVolume.SetUp succeeded for volume "kubernetes-dashboard-token-w6fdt" (UniqueName: "kubernetes.io/secret/578ed9bb-7bcd-11e9-8f1f-0017fa00a076-kubernetes-da...
May 24 14:26:50 k8s-linux-worker1 kubelet[49054]: E0524 14:26:50.500985   49054 pod_workers.go:190] Error syncing pod 578ed9bb-7bcd-11e9-8f1f-0017fa00a076 ("kubernetes-dashboard-5f7b999d65-52qzn_kube-system(578ed9bb-7bcd-11e9-8f1f-0017fa00a076)"), skipping: network i...
May 24 14:26:52 k8s-linux-worker1 kubelet[49054]: E0524 14:26:52.457404   49054 pod_workers.go:190] Error syncing pod 578ed9bb-7bcd-11e9-8f1f-0017fa00a076 ("kubernetes-dashboard-5f7b999d65-52qzn_kube-system(578ed9bb-7bcd-11e9-8f1f-0017fa00a076)"), skipping: network i...
May 24 14:26:54 k8s-linux-worker1 kubelet[49054]: W0524 14:26:54.375708   49054 cni.go:213] Unable to update cni config: No networks found in /opt/k8s/cni/net.d
May 24 14:26:54 k8s-linux-worker1 kubelet[49054]: E0524 14:26:54.457395   49054 pod_workers.go:190] Error syncing pod 578ed9bb-7bcd-11e9-8f1f-0017fa00a076 ("kubernetes-dashboard-5f7b999d65-52qzn_kube-system(578ed9bb-7bcd-11e9-8f1f-0017fa00a076)"), skipping: network i...
May 24 14:26:54 k8s-linux-worker1 kubelet[49054]: E0524 14:26:54.681143   49054 kubelet.go:2170] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
May 24 14:26:56 k8s-linux-worker1 kubelet[49054]: E0524 14:26:56.457345   49054 pod_workers.go:190] Error syncing pod 578ed9bb-7bcd-11e9-8f1f-0017fa00a076 ("kubernetes-dashboard-5f7b999d65-52qzn_kube-system(578ed9bb-7bcd-11e9-8f1f-0017fa00a076)"), skipping: network i...
Hint: Some lines were ellipsized, use -l to show in full.
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# docker ps -a
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS                  PORTS               NAMES
b8f872324f46        ff281650a721           "cp -f /etc/kube-fla…"   2 days ago          Exited (0) 2 days ago                       k8s_install-cni_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_0
8fb84df67835        ff281650a721           "/opt/bin/flanneld -…"   2 days ago          Up 2 days                                   k8s_kube-flannel_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_0
b4ccab357b38        k8s.gcr.io/pause:3.1   "/pause"                 2 days ago          Up 2 days                                   k8s_POD_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_2
9f2d1b2a6bba        f9aed6605b81           "/dashboard --insecu…"   2 days ago          Up 2 days                                   k8s_kubernetes-dashboard_kubernetes-dashboard-5f7b999d65-52qzn_kube-system_578ed9bb-7bcd-11e9-8f1f-0017fa00a076_0
9609353660a9        k8s.gcr.io/pause:3.1   "/pause"                 2 days ago          Up 2 days                                   k8s_POD_kubernetes-dashboard-5f7b999d65-52qzn_kube-system_578ed9bb-7bcd-11e9-8f1f-0017fa00a076_1
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# docker stop $(docker ps -aq)
b8f872324f46
8fb84df67835
b4ccab357b38
9f2d1b2a6bba
9609353660a9
[root@k8s-linux-worker1 net.d]# docker rm $(docker ps -aq)
0a1c7e3e6498
8fb84df67835
b4ccab357b38
9f2d1b2a6bba
9609353660a9
Error response from daemon: You cannot remove a running container 737bfd1141f8349924c7a8437b8820ebff4b2571192d9ae24a6cf2554a908f2e. Stop the container before attempting removal or force remove
Error response from daemon: You cannot remove a running container 0c6a01d3da7de9ca7a6ad39aa5c856d2c27b8c196828b92b22aa1db2881fa74b. Stop the container before attempting removal or force remove
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# docker ps -a
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS               NAMES
737bfd1141f8        ff281650a721           "/opt/bin/flanneld -…"   39 seconds ago      Up 37 seconds                           k8s_kube-flannel_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_1
0c6a01d3da7d        k8s.gcr.io/pause:3.1   "/pause"                 40 seconds ago      Up 39 seconds                           k8s_POD_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_3
[root@k8s-linux-worker1 net.d]# 


[root@k8s-master1 ~]# kubectl get pods --all-namespaces
NAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGE
kube-system   kube-flannel-ds-amd64-vlwws             1/1     Running   1          2d18h
kube-system   kubernetes-dashboard-5f7b999d65-52qzn   0/1     Error     0          2d16h
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl logs kubernetes-dashboard-5f7b999d65-52qzn -n kube-system
Unable to retrieve container logs for docker://9f2d1b2a6bba0874ade8776113ce48b7e35eb295c9cab263c2a5c81d4c4241c4
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# kubectl describe pod kubernetes-dashboard-5f7b999d65-52qzn -n kube-system
Name:           kubernetes-dashboard-5f7b999d65-52qzn
Namespace:      kube-system
Node:           10.1.36.46/10.1.36.46
Start Time:     Tue, 21 May 2019 21:35:47 +0800
Labels:         k8s-app=kubernetes-dashboard
                pod-template-hash=5f7b999d65
Annotations:    <none>
Status:         Running
IP:             
Controlled By:  ReplicaSet/kubernetes-dashboard-5f7b999d65
Containers:
  kubernetes-dashboard:
    Container ID:  docker://9f2d1b2a6bba0874ade8776113ce48b7e35eb295c9cab263c2a5c81d4c4241c4
    Image:         k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1
    Image ID:      docker://sha256:f9aed6605b814b69e92dece6a50ed1e4e730144eb1cc971389dde9cb3820d124
    Port:          8443/TCP
    Host Port:     0/TCP
    Args:
      --auto-generate-certificates
    State:          Terminated
      Reason:       Error
      Exit Code:    2
      Started:      Tue, 21 May 2019 22:10:09 +0800
      Finished:     Fri, 24 May 2019 14:27:41 +0800
    Ready:          False
    Restart Count:  0
    Liveness:       http-get https://:8443/ delay=30s timeout=30s period=10s #success=1 #failure=3
    Environment:    <none>
    Mounts:
      /certs from kubernetes-dashboard-certs (rw)
      /tmp from tmp-volume (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kubernetes-dashboard-token-w6fdt (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  kubernetes-dashboard-certs:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kubernetes-dashboard-certs
    Optional:    false
  tmp-volume:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     
    SizeLimit:  <unset>
  kubernetes-dashboard-token-w6fdt:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  kubernetes-dashboard-token-w6fdt
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node-role.kubernetes.io/master:NoSchedule
Events:
  Type     Reason           Age                      From                 Message
  ----     ------           ----                     ----                 -------
  Warning  NetworkNotReady  2m53s (x154 over 7m54s)  kubelet, 10.1.36.46  network is not ready: runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized
[root@k8s-master1 ~]# 



[root@k8s-linux-worker1 net.d]# pwd
/opt/k8s/cni/net.d
[root@k8s-linux-worker1 net.d]# mv 10-default.conf_back 10-default.conf
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# systemctl restart kubelet.service
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# docker ps -a
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS                     PORTS               NAMES
c67316285a4a        f9aed6605b81           "/dashboard --insecu…"   13 seconds ago      Up 12 seconds                                  k8s_kubernetes-dashboard_kubernetes-dashboard-5f7b999d65-52qzn_kube-system_578ed9bb-7bcd-11e9-8f1f-0017fa00a076_0
ad5e361ac3ad        k8s.gcr.io/pause:3.1   "/pause"                 14 seconds ago      Up 13 seconds                                  k8s_POD_kubernetes-dashboard-5f7b999d65-52qzn_kube-system_578ed9bb-7bcd-11e9-8f1f-0017fa00a076_0
4f383592385b        ff281650a721           "cp -f /etc/kube-fla…"   7 minutes ago       Exited (0) 7 minutes ago                       k8s_install-cni_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_0
737bfd1141f8        ff281650a721           "/opt/bin/flanneld -…"   8 minutes ago       Up 8 minutes                                   k8s_kube-flannel_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_1
0c6a01d3da7d        k8s.gcr.io/pause:3.1   "/pause"                 8 minutes ago       Up 8 minutes                                   k8s_POD_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_3
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# docker rm $(docker ps -aq)
4f383592385b
Error response from daemon: You cannot remove a running container c67316285a4a9b09c3007898da29cf42c7a9f25d4ccf90482cef4ecb3f1ada50. Stop the container before attempting removal or force remove
Error response from daemon: You cannot remove a running container ad5e361ac3adcb943d74a66efcf744b81198a014292d8ea074e9b08be6ebb2cc. Stop the container before attempting removal or force remove
Error response from daemon: You cannot remove a running container 737bfd1141f8349924c7a8437b8820ebff4b2571192d9ae24a6cf2554a908f2e. Stop the container before attempting removal or force remove
Error response from daemon: You cannot remove a running container 0c6a01d3da7de9ca7a6ad39aa5c856d2c27b8c196828b92b22aa1db2881fa74b. Stop the container before attempting removal or force remove
[root@k8s-linux-worker1 net.d]# 
[root@k8s-linux-worker1 net.d]# docker ps -a
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS               NAMES
c67316285a4a        f9aed6605b81           "/dashboard --insecu…"   40 seconds ago      Up 39 seconds                           k8s_kubernetes-dashboard_kubernetes-dashboard-5f7b999d65-52qzn_kube-system_578ed9bb-7bcd-11e9-8f1f-0017fa00a076_0
ad5e361ac3ad        k8s.gcr.io/pause:3.1   "/pause"                 41 seconds ago      Up 40 seconds                           k8s_POD_kubernetes-dashboard-5f7b999d65-52qzn_kube-system_578ed9bb-7bcd-11e9-8f1f-0017fa00a076_0
737bfd1141f8        ff281650a721           "/opt/bin/flanneld -…"   8 minutes ago       Up 8 minutes                            k8s_kube-flannel_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_1
0c6a01d3da7d        k8s.gcr.io/pause:3.1   "/pause"                 8 minutes ago       Up 8 minutes                            k8s_POD_kube-flannel-ds-amd64-vlwws_kube-system_5064723c-7bbc-11e9-8eb2-0017fa00a076_3
[root@k8s-linux-worker1 net.d]# 





[root@k8s-master1 ~]# kubectl run my-nginx --image=nginx --replicas=5 --port=80
kubectl run --generator=deployment/apps.v1 is DEPRECATED and will be removed in a future version. Use kubectl run --generator=run-pod/v1 or kubectl create instead.
deployment.apps/my-nginx created
[root@k8s-master1 ~]# 
[root@k8s-master1 ~]# 
[root@k8s-master1 ssl]# kubectl get pod  -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE         NOMINATED NODE   READINESS GATES
my-nginx-86459cfc9f-2mbqq   1/1     Running   0          24m   172.20.2.2    10.1.36.48   <none>           <none>
my-nginx-86459cfc9f-8ftlm   1/1     Running   0          24m   172.20.1.14   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-cr7rh   1/1     Running   0          24m   172.20.0.2    10.1.36.46   <none>           <none>
my-nginx-86459cfc9f-fqs4n   1/1     Running   0          24m   172.20.1.15   10.1.36.47   <none>           <none>
my-nginx-86459cfc9f-klhw9   1/1     Running   0          24m   172.20.0.3    10.1.36.46   <none>           <none>
[root@k8s-master1 ssl]# 

[root@k8s-master1 ~]# 

[root@k8s-master2 ~]# kubectl get deployment  -o wide
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
my-nginx   5/5     5            5           15h   my-nginx     nginx    run=my-nginx
[root@k8s-master2 ~]# 


kubectl delete deployment  my-nginx

root@my-nginx-86459cfc9f-klhw9:/etc/apt/sources.list.d# ping www.baidu.com
PING www.a.shifen.com (180.97.33.107): 56 data bytes
64 bytes from 180.97.33.107: icmp_seq=0 ttl=48 time=33.908 ms
64 bytes from 180.97.33.107: icmp_seq=1 ttl=48 time=33.988 ms
64 bytes from 180.97.33.107: icmp_seq=2 ttl=48 time=34.005 ms
64 bytes from 180.97.33.107: icmp_seq=3 ttl=48 time=34.096 ms
64 bytes from 180.97.33.107: icmp_seq=4 ttl=48 time=34.045 ms
64 bytes from 180.97.33.107: icmp_seq=5 ttl=48 time=34.010 ms
64 bytes from 180.97.33.107: icmp_seq=6 ttl=48 time=34.079 ms
^C--- www.a.shifen.com ping statistics ---
7 packets transmitted, 7 packets received, 0% packet loss
round-trip min/avg/max/stddev = 33.908/34.019/34.096/0.058 ms
root@my-nginx-86459cfc9f-klhw9:/etc/apt/sources.list.d# 
root@my-nginx-86459cfc9f-klhw9:/etc/apt/sources.list.d# ping 172.20.2.2
PING 172.20.2.2 (172.20.2.2): 56 data bytes
64 bytes from 172.20.2.2: icmp_seq=0 ttl=62 time=1.372 ms
64 bytes from 172.20.2.2: icmp_seq=1 ttl=62 time=1.072 ms
64 bytes from 172.20.2.2: icmp_seq=2 ttl=62 time=1.069 ms
64 bytes from 172.20.2.2: icmp_seq=3 ttl=62 time=0.978 ms
64 bytes from 172.20.2.2: icmp_seq=4 ttl=62 time=1.144 ms
64 bytes from 172.20.2.2: icmp_seq=5 ttl=62 time=1.121 ms
^C--- 172.20.2.2 ping statistics ---
6 packets transmitted, 6 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.978/1.126/1.372/0.122 ms
root@my-nginx-86459cfc9f-klhw9:/etc/apt/sources.list.d# 















```


### 负载均衡

nginx 做四层和七层负载均衡

```bash
[root@k8s-master1 ~]# rpm -ql nginx.x86_64
/etc/logrotate.d/nginx
/etc/nginx
/etc/nginx/conf.d
/etc/nginx/conf.d/default.conf
/etc/nginx/fastcgi_params
/etc/nginx/koi-utf
/etc/nginx/koi-win
/etc/nginx/mime.types
/etc/nginx/modules
/etc/nginx/nginx.conf
/etc/nginx/scgi_params
/etc/nginx/uwsgi_params
/etc/nginx/win-utf
/etc/sysconfig/nginx
/etc/sysconfig/nginx-debug
/usr/lib/systemd/system/nginx-debug.service
/usr/lib/systemd/system/nginx.service
/usr/lib64/nginx
/usr/lib64/nginx/modules
/usr/libexec/initscripts/legacy-actions/nginx
/usr/libexec/initscripts/legacy-actions/nginx/check-reload
/usr/libexec/initscripts/legacy-actions/nginx/upgrade
/usr/sbin/nginx
/usr/sbin/nginx-debug
/usr/share/doc/nginx-1.16.0
/usr/share/doc/nginx-1.16.0/COPYRIGHT
/usr/share/man/man8/nginx.8.gz
/usr/share/nginx
/usr/share/nginx/html
/usr/share/nginx/html/50x.html
/usr/share/nginx/html/index.html
/var/cache/nginx
/var/log/nginx
[root@k8s-master1 ~]# 


[root@k8s-master1 nginx]# cat nginx.conf 

user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
[root@k8s-master1 nginx]# 


[root@k8s-master1 nginx]# cat conf.d/default.conf 
server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}

[root@k8s-master1 nginx]# 


# nginx 做七层负载均衡
[root@k8s-master1 nginx]# cat conf.d/k8s.conf
upstream k8s {
    server 10.1.36.43:6443;
    server 10.1.36.44:6443;
}

server {
    listen 8443;
    
    location / {
        proxy_pass http://k8s;
    }
}


# nginx 做四层负载均衡

nginx 在 1.9.0 的时候，增加了一个 stream 模块，用来实现四层协议（网络层和传输层）的转发、代理、负载均衡等。stream 模块的用法跟 http 的用法类似，允许我们配置一组 TCP 或者 UDP 等协议的监听，然后通过 proxy_pass 来转发我们的请求，通过 upstream 添加多个后端服务，实现负载均衡。

nginx 默认是没有编译这个模块的，要使用 stream 模块，编译的时候记得加上 --with-stream 这个参数即可。

# 检查是否编译了 stream 模块（是否包含 --with-stream 选项）
[root@k8s-master1 nginx]# /usr/sbin/nginx -V
nginx version: nginx/1.16.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC) 
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -pie'
[root@k8s-master1 nginx]# 




在 nginx.conf 默认配置文件里面，默认没有 stream 的配置。stream 模块的配置跟 http 配置是同级的，因此要注意不要写到http里面。

[root@k8s-master1 nginx]# cat nginx.conf 

user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}

# nginx 做四层负载均衡
stream {
    log_format main '$remote_addr $upstream_addr - [$time_local] $status $upstream_bytes_sent';
    access_log /var/log/nginx/k8s-access.log main;
    upstream k8s-apiserver {
        server 10.1.36.43:6443;
        server 10.1.36.44:6443;
    }
    server {
        listen 8443;
        proxy_pass k8s-apiserver;
    }
}

[root@k8s-master1 nginx]# 

# 检查配置是否正确
[root@k8s-master1 nginx]# /usr/sbin/nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
[root@k8s-master1 nginx]# 

[root@k8s-linux-worker3 ssl]# netstat -tulnp | grep 8443
tcp        0      0 0.0.0.0:8443            0.0.0.0:*               LISTEN      109929/nginx: maste 
[root@k8s-linux-worker3 ssl]# 






# https://www.jianshu.com/p/c6d560d12d50
# 准备 dashboard 使用的证书签名请求
[root@k8s-master1 ssl]# vim ./dashboard.json
[root@k8s-master1 ssl]# cat ./dashboard.json
{
  "CN": "admin",
  "hosts": [
    "127.0.0.1",
    "10.1.36.43",
    "10.1.36.44",
    "10.1.36.45",
    "10.1.36.46",
    "10.1.36.47",
    "10.1.36.48",
    "10.1.36.49",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "system:masters",
      "OU": "System"
    }
  ]
}
[root@k8s-master1 ssl]# 

[root@k8s-master1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes dashboard.json | ./cfssljson -bare dashboard
2019/05/28 15:31:27 [INFO] generate received request
2019/05/28 15:31:27 [INFO] received CSR
2019/05/28 15:31:27 [INFO] generating key: rsa-2048
2019/05/28 15:31:27 [INFO] encoded CSR
2019/05/28 15:31:27 [INFO] signed certificate with serial number 26305284186960759903685091901735121795326008234
2019/05/28 15:31:27 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# 

dashboard.json

dashboard.csr
dashboard-key.pem
dashboard.pem


[root@k8s-master1 ssl]# kubectl get secret --all-namespaces -o wide
NAMESPACE         NAME                               TYPE                                  DATA   AGE
default           default-token-lz2dc                kubernetes.io/service-account-token   3      6d23h
kube-node-lease   default-token-wr6r8                kubernetes.io/service-account-token   3      6d23h
kube-public       default-token-l9mvf                kubernetes.io/service-account-token   3      6d23h
kube-system       default-token-w8zxk                kubernetes.io/service-account-token   3      6d23h
kube-system       flannel-token-4f2g9                kubernetes.io/service-account-token   3      6d20h
kube-system       kubernetes-dashboard-certs         Opaque                                0      6d19h
kube-system       kubernetes-dashboard-csrf          Opaque                                1      6d19h
kube-system       kubernetes-dashboard-key-holder    Opaque                                2      6d17h
kube-system       kubernetes-dashboard-token-w6fdt   kubernetes.io/service-account-token   3      6d19h
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl delete secret -n kube-system kubernetes-dashboard-certs
secret "kubernetes-dashboard-certs" deleted
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl get secret --all-namespaces -o wide
NAMESPACE         NAME                               TYPE                                  DATA   AGE
default           default-token-lz2dc                kubernetes.io/service-account-token   3      6d23h
kube-node-lease   default-token-wr6r8                kubernetes.io/service-account-token   3      6d23h
kube-public       default-token-l9mvf                kubernetes.io/service-account-token   3      6d23h
kube-system       default-token-w8zxk                kubernetes.io/service-account-token   3      6d23h
kube-system       flannel-token-4f2g9                kubernetes.io/service-account-token   3      6d20h
kube-system       kubernetes-dashboard-csrf          Opaque                                1      6d19h
kube-system       kubernetes-dashboard-key-holder    Opaque                                2      6d17h
kube-system       kubernetes-dashboard-token-w6fdt   kubernetes.io/service-account-token   3      6d19h
[root@k8s-master1 ssl]# 

[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl -n kube-system create secret generic kubernetes-dashboard-certs --from-file=./dashboard-key.pem --from-file=./dashboard.pem
secret/kubernetes-dashboard-certs created
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl get secret --all-namespaces -o wide
NAMESPACE         NAME                               TYPE                                  DATA   AGE
default           default-token-lz2dc                kubernetes.io/service-account-token   3      6d23h
kube-node-lease   default-token-wr6r8                kubernetes.io/service-account-token   3      6d23h
kube-public       default-token-l9mvf                kubernetes.io/service-account-token   3      6d23h
kube-system       default-token-w8zxk                kubernetes.io/service-account-token   3      6d23h
kube-system       flannel-token-4f2g9                kubernetes.io/service-account-token   3      6d20h
kube-system       kubernetes-dashboard-certs         Opaque                                2      3s
kube-system       kubernetes-dashboard-csrf          Opaque                                1      6d19h
kube-system       kubernetes-dashboard-key-holder    Opaque                                2      6d17h
kube-system       kubernetes-dashboard-token-w6fdt   kubernetes.io/service-account-token   3      6d19h
[root@k8s-master1 ssl]# 



[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl config set-cluster kubernetes --certificate-authority=./ca.pem --embed-certs=true --server=https://10.1.36.43:6443 --kubeconfig=./dashboard.kubeconfig
Cluster "kubernetes" set.
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl config set-credentials admin --client-certificate=./dashboard.pem --embed-certs=true --client-key=./dashboard-key.pem --kubeconfig=./dashboard.kubeconfig
User "admin" set.
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl config set-context kubernetes --cluster=kubernetes --user=admin --kubeconfig=./dashboard.kubeconfig
Context "kubernetes" created.
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# kubectl config use-context kubernetes --kubeconfig=./dashboard.kubeconfig
Switched to context "kubernetes".
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# sz dashboard.kubeconfig 

[root@k8s-master1 ssl]# 

# https://www.cnblogs.com/xzkzzz/p/9920743.html
# https://www.cnblogs.com/linuxk/p/9783510.html













```


