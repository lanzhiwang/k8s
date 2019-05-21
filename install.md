## k8s install



安装 docker 时要设置 Docker Root Dir 选项



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



10.1.36.43
10.1.36.44
10.1.36.45

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
[root@k8s-master1 bin]# ./kubectl config set-cluster kubernetes --certificate-authority=/opt/k8s/ssl/ca.pem --embed-certs=true --server=https://10.1.36.43:6443
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













```








