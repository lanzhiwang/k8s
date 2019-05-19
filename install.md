## k8s install



安装 docker 时要设置 Docker Root Dir 选项



### 相关文件下载

```bash

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
UUID=4ab4484f-c385-4eba-8f33-c736800fe874 /opt/k8s                ext4    defaults        0 0
[root@k8s-master1 ~]# 
重启系统检查 hostname 和挂载是否生效





[root@k8s-master1 ssl]# pwd
/opt/k8s/temp/ssl
# 准备 CA 配置文件
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
# 准备 CA 签名请求文件，CA 证书请求文件有 ca 字段，其他的请求文件没有该字段
[root@k8s-master1 ssl]# cat ./ca-csr.json 
{
  "CN": "www.mingyuanyun.com/emailAddress=huz01@mingyuanyun.com",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "mingyuanyun",
      "OU": "Technical Support"
    }
  ],
  "ca": {
    "expiry": "131400h"
  }
}
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# ./cfssl gencert -initca ca-csr.json | ./cfssljson -bare ca
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# ll
total 18828
-rw-r--r-- 1 root root      292 May 19 13:53 ca-config.json
-rw-r--r-- 1 root root     1094 May 19 14:00 ca.csr
-rw-r--r-- 1 root root      314 May 19 13:56 ca-csr.json
-rw------- 1 root root     1679 May 19 14:00 ca-key.pem
-rw-r--r-- 1 root root     1541 May 19 14:00 ca.pem
-rwxr-xr-x 1 root root 10376657 Mar 30  2016 cfssl
-rwxr-xr-x 1 root root  6595195 Mar 30  2016 cfssl-certinfo
-rwxr-xr-x 1 root root  2277873 Mar 30  2016 cfssljson
[root@k8s-master1 ssl]# 

ca-config.json
ca-csr.json 

ca.csr  # CA 证书请求文件
ca-key.pem  # CA 私钥
ca.pem  # CA 证书


# 准备 kubectl 使用的 admin 证书签名请求，缺少 hosts 自动
[root@k8s-master1 ssl]# cat ./admin-csr.json
{
  "CN": "www.mingyuanyun.com/emailAddress=huz01@mingyuanyun.com",
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
      "O": "mingyuanyun",
      "OU": "Technical Support"
    }
  ]
}
[root@k8s-master1 ssl]# 
[root@k8s-master1 ssl]# ./cfssl gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes admin-csr.json | ./cfssljson -bare admin
2019/05/19 14:17:32 [INFO] generate received request
2019/05/19 14:17:32 [INFO] received CSR
2019/05/19 14:17:32 [INFO] generating key: rsa-2048
2019/05/19 14:17:33 [INFO] encoded CSR
2019/05/19 14:17:33 [INFO] signed certificate with serial number 317145352576000474480959839956652034649539483191
2019/05/19 14:17:33 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
[root@k8s-master1 ssl]# 

admin-csr.json

admin.csr
admin-key.pem
admin.pem


[root@k8s-master1 temp]# rpm -qa | grep firewall
firewalld-0.4.4.4-14.el7.noarch
firewalld-filesystem-0.4.4.4-14.el7.noarch
python-firewall-0.4.4.4-14.el7.noarch
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# yum erase firewalld-0.4.4.4-14.el7.noarch firewalld-filesystem-0.4.4.4-14.el7.noarch python-firewall-0.4.4.4-14.el7.noarch
[root@k8s-master1 temp]# 
[root@k8s-master1 temp]# rpm -qa | grep firewall
[root@k8s-master1 temp]# 

[root@k8s-master1 temp]# yum install conntrack-tools psmisc nfs-utils jq socat bash-completion rsync ipset ipvsadm


# 永久关闭 selinux
vim /etc/selinux/config
"SELINUX=disabled"

# 禁止 rsyslog 获取 journald 日志，注释掉下面两行，重启 rsyslog 服务
[root@k8s-master1 temp]# cat /etc/rsyslog.conf | grep "ModLoad imjournal"
$ModLoad imjournal # provides access to the systemd journal
[root@k8s-master1 temp]# 
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




```






