# glusterfs

## Quick Start Guide

### Installing GlusterFS - a Quick Start Guide

#### Purpose of this document

This document is intended to provide a step-by-step guide to setting up GlusterFS for the first time. For the purposes of this guide, it is required to use Fedora 26 (or, higher) virtual machine instances.  本文档旨在提供首次设置GlusterFS的分步指南。 出于本指南的目的，需要使用Fedora 26（或更高版本）虚拟机实例。

After you deploy GlusterFS by following these steps, we recommend that you read the GlusterFS Admin Guide to learn how to administer GlusterFS and how to select a volume type that fits your needs. Read the GlusterFS Install Guide for a more detailed explanation of the steps we took here. We want you to be successful in as short a time as possible.  按照以下步骤部署GlusterFS后，我们建议您阅读GlusterFS管理员指南，了解如何管理GlusterFS以及如何选择适合您需求的卷类型。 阅读GlusterFS安装指南，以获取有关我们在此处采取的步骤的更详细说明。 我们希望您在尽可能短的时间内取得成功。

If you would like a more detailed walkthrough with instructions for installing using different methods (in local virtual machines, EC2 and baremetal) and different distributions, then have a look at the Install guide.  如果您想要更详细的演练，其中包含使用不同方法（在本地虚拟机，EC2和裸设备中）和不同发行版进行安装的说明，请查看安装指南。

#### Using Ansible to deploy and manage GlusterFS

If you are already an Ansible user, and are more comfortable with setting up distributed systems with Ansible, we recommend you to skip all these and move over to gluster-ansible repository, which gives most of the details to get the systems running faster.  如果您已经是Ansible用户，并且更熟悉使用Ansible设置分布式系统，我们建议您跳过所有这些并转移到gluster-ansible存储库，它提供了大部分细节以使系统运行得更快。

#### Deploying GlusterFS with GlusterD2, the next gen management interface of Gluster  使用GlusterD2，Gluster的下一代管理界面部署GlusterFS

While GlusterD2 project continues to be under active development, contributors can start by setting up the cluster to understand the aspect of peer and volume management.Please refer to GD2 quick start guide here. Feedback on the new CLI and the ReST APIs are welcome at gluster-users@gluster.org & gluster-devel@gluster.org.  虽然GlusterD2项目仍在积极开发中，但贡献者可以从设置集群开始了解同行和卷管理的方面。请参阅此处的GD2快速入门指南。 有关新CLI和ReST API的反馈，欢迎访问gluster-users@gluster.org和gluster-devel@gluster.org。

#### Automatically deploying GlusterFS with Puppet-Gluster+Vagrant

To deploy GlusterFS using scripted methods, please read this article.  要使用脚本方法部署GlusterFS，请阅读本文。

##### Step 1 – Have at least three nodes  至少有三个节点

* Fedora 26 (or later) on 3 nodes named "server1", "server2" and "server3"  名为“server1”，“server2”和“server3”的3个节点上的Fedora 26（或更高版本）

* A working network connection  一个有效的网络连接

* At least two virtual disks, one for the OS installation, and one to be used to serve GlusterFS storage (sdb), on each of these VMs. This will emulate a real-world deployment, where you would want to separate GlusterFS storage from the OS install.  每个虚拟机上至少有两个虚拟磁盘，一个用于操作系统安装，另一个用于服务GlusterFS存储（sdb）。 这将模拟真实世界的部署，您可能希望将GlusterFS存储与操作系统安装分开。

* Setup NTP on each of these servers to get the proper functioning of many applications on top of filesystem.  在每个服务器上设置NTP，以便在文件系统之上正常运行许多应用程序。

Note: GlusterFS stores its dynamically generated configuration files at /var/lib/glusterd. If at any point in time GlusterFS is unable to write to these files (for example, when the backing filesystem is full), it will at minimum cause erratic behavior for your system; or worse, take your system offline completely. It is recommended to create separate partitions for directories such as `/var /log` to reduce the chances of this happening.  注意：GlusterFS将其动态生成的配置文件存储在/var/lib/glusterd 中。 如果在任何时间点GlusterFS无法写入这些文件（例如，当后备文件系统已满时），它将至少导致系统出现不稳定行为; 或者更糟糕的是，让您的系统完全脱机。 建议为 /var /log等目录创建单独的分区，以减少发生这种情况的可能性。

##### Step 2 - Format and mount the bricks  格式化并安装砖块

Perform this step on all the nodes, "server{1,2,3}"  在所有节点上执行此步骤，“server {1,2,3}”

Note: We are going to use the XFS filesystem for the backend bricks. But Gluster is designed to work on top of any filesystem, which supports extended attributes.  注意：我们将使用XFS文件系统作为后端块。 但Gluster旨在处理任何支持扩展属性的文件系统。

The following examples assume that the brick will be residing on /dev/sdb1.  以下示例假定brick将驻留在/ dev / sdb1上。

```bash
    mkfs.xfs -i size=512 /dev/sdb1
    mkdir -p /data/brick1
    echo '/dev/sdb1 /data/brick1 xfs defaults 1 2' >> /etc/fstab
    mount -a && mount
```

You should now see sdb1 mounted at /data/brick1

##### Step 3 - Installing GlusterFS

Install the software

```bash
    yum install glusterfs-server
```

Start the GlusterFS management daemon:

```bash
    service glusterd start
    service glusterd status
    glusterd.service - LSB: glusterfs server
           Loaded: loaded (/etc/rc.d/init.d/glusterd)
       Active: active (running) since Mon, 13 Aug 2012 13:02:11 -0700; 2s ago
      Process: 19254 ExecStart=/etc/rc.d/init.d/glusterd start (code=exited, status=0/SUCCESS)
       CGroup: name=systemd:/system/glusterd.service
           ├ 19260 /usr/sbin/glusterd -p /run/glusterd.pid
           ├ 19304 /usr/sbin/glusterfsd --xlator-option georep-server.listen-port=24009 -s localhost...
           └ 19309 /usr/sbin/glusterfs -f /var/lib/glusterd/nfs/nfs-server.vol -p /var/lib/glusterd/...
```

##### Step 4 - Configure the firewall

The gluster processes on the nodes need to be able to communicate with each other. To simplify this setup, configure the firewall on each node to accept all traffic from the other node.  节点上的gluster进程需要能够相互通信。 要简化此设置，请在每个节点上配置防火墙以接受来自其他节点的所有流量。

```bash
    iptables -I INPUT -p all -s <ip-address> -j ACCEPT
```
where ip-address is the address of the other node.

##### Step 5 - Configure the trusted pool

From "server1"

```bash
    gluster peer probe server2
    gluster peer probe server3
```
Note: When using hostnames, the first server needs to be probed from one other server to set its hostname.  注意：使用主机名时，需要从另一台服务器探测第一台服务器以设置其主机名。

From "server2"

```bash
    gluster peer probe server1
```
Note: Once this pool has been established, only trusted members may probe new servers into the pool. A new server cannot probe the pool, it must be probed from the pool.  注意：建立此池后，只有受信任的成员才能将新服务器探测到池中。 新服务器无法探测池，必须从池中进行探测。

Check the peer status on server1

```bash
    gluster peer status
```

You should see something like this (the UUID will differ)

```bash
            Number of Peers: 2

            Hostname: server2
            Uuid: f0e7b138-4874-4bc0-ab91-54f20c7068b4
            State: Peer in Cluster (Connected)

            Hostname: server3
            Uuid: f0e7b138-4532-4bc0-ab91-54f20c701241
            State: Peer in Cluster (Connected)
```

##### Step 6 - Set up a GlusterFS volume

On all servers:

```bash
    mkdir -p /data/brick1/gv0
```

From any single server:

```bash
    gluster volume create gv0 replica 3 server1:/data/brick1/gv0 server2:/data/brick1/gv0 server3:/data/brick1/gv0
    gluster volume start gv0
```

Confirm that the volume shows "Started":

```bash
    gluster volume info
```

You should see something like this (the Volume ID will differ):

```bash
            Volume Name: gv0
            Type: Replicate
            Volume ID: f25cc3d8-631f-41bd-96e1-3e22a4c6f71f
            Status: Started
            Snapshot Count: 0
            Number of Bricks: 1 x 3 = 3
            Transport-type: tcp
            Bricks:
            Brick1: server1:/data/brick1/gv0
            Brick2: server2:/data/brick1/gv0
            Brick3: server3:/data/brick1/gv0
            Options Reconfigured:
            transport.address-family: inet
```

Note: If the volume does not show "Started", the files under /var/log/glusterfs/glusterd.log should be checked in order to debug and diagnose the situation. These logs can be looked at on one or, all the servers configured.  注意：如果卷未显示“已启动”，则应检查/var/log/glusterfs/glusterd.log下的文件，以便调试和诊断该情况。 可以在配置的一个或所有服务器上查看这些日志。

##### Step 7 - Testing the GlusterFS volume

For this step, we will use one of the servers to mount the volume. Typically, you would do this from an external machine, known as a "client". Since using this method would require additional packages to be installed on the client machine, we will use one of the servers as a simple place to test first , as if it were that "client".  对于此步骤，我们将使用其中一个服务器来装入卷。 通常，您可以从外部计算机（称为“客户端”）执行此操作。 由于使用此方法需要在客户端计算机上安装其他软件包，因此我们将使用其中一个服务器作为首先进行测试的简单位置，就像它是“客户端”一样。

```bash
    mount -t glusterfs server1:/gv0 /mnt
      for i in `seq -w 1 100`; do cp -rp /var/log/messages /mnt/copy-test-$i; done
```

First, check the client mount point:

```bash
    ls -lA /mnt/copy* | wc -l
```

You should see 100 files returned. Next, check the GlusterFS brick mount points on each server:  您应该看到返回100个文件。 接下来，检查每台服务器上的GlusterFS砖安装点：

```bash
    ls -lA /data/brick1/gv0/copy*
```
You should see 100 files on each server using the method we listed here. Without replication, in a distribute only volume (not detailed here), you should see about 33 files on each one.  您应该使用我们在此处列出的方法在每台服务器上看到100个文件。 如果没有复制，在仅分发卷（此处未详述）中，您应该在每个卷上看到大约33个文件。

