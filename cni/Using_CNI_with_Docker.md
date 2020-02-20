# Using CNI with Docker

In[ our last post](https://www.dasblinkenlichten.com/understanding-cni-container-networking-interface/) we introduced ourselves to CNI (if you haven’t read that yet, I suggest you start there) as we worked through a simple example of connecting a network namespace to a bridge.  CNI managed both the creation of the bridge as well as connecting the namespace to the bridge using a VETH pair.  In this post we’ll explore how to do this same thing but with a container created by Docker.  As you’ll see, the process is largely the same.  Let’s jump right in.  在上一篇文章中，我们通过一个将网络名称空间连接到网桥的简单示例介绍了CNI（如果您还没有读过，我建议您从这里开始）。 CNI管理桥接的创建以及使用VETH对将名称空间连接到桥接。 在本文中，我们将探讨如何使用Docker创建的容器来执行相同的操作。 如您所见，过程大致相同。 让我们跳进去。

*This post assumes that you followed the steps in the first post (Understanding CNI) and have a ‘cni’ directory (~/cni) that contains the CNI binaries.  If you don’t have that – head back to the first post and follow the steps to download the pre-compiled CNI binaries.  It also assumes that you have a default Docker installation.  In my case, Im using Docker version 1.12.*  本文假定您已按照第一篇文章（了解CNI）中的步骤进行操作，并拥有一个包含CNI二进制文件的“ cni”目录（〜/ cni）。 如果没有，请返回第一篇文章，并按照步骤下载预编译的CNI二进制文件。 它还假定您具有默认的Docker安装。 就我而言，我使用的是Docker 1.12版。

The first thing we need to do is to create a Docker container.  To do that we’ll run this command…

```
user@ubuntu-2:~/cni$ sudo docker run --name cnitest --net=none -d jonlangemak/web_server_1
835583cdf382520283c709b5a5ee866b9dccf4861672b95eccbc7b7688109b56
user@ubuntu-2:~/cni$
```

Notice that when we ran the command we told Docker to use a network of ‘none’. When Docker is told to do this, it will create the network namespace for the container, but it will not attempt to connect the containers network namespace to anything else.  If we look in the container we should see that it only has a loopback interface…  请注意，当我们运行命令时，我们告诉Docker使用“无”网络。 当Docker被告知执行此操作时，它将为容器创建网络名称空间，但不会尝试将容器的网络名称空间连接到其他任何内容。 如果我们查看容器，我们应该看到它只有一个环回接口…

```
user@ubuntu-2:~/cni$ sudo docker exec cnitest ifconfig
lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

user@ubuntu-2:~/cni$
```

So now we want to use CNI to connect the container to something. Before we do that we need some information. Namely, we need a network definition for CNI to consume as well as some information about the container itself.  For the network definition, we’ll create a new definition and specify a few more options to see how they work.  Create the configuration with this command (I assume you’re creating this file in ~/cni)…  因此，现在我们要使用CNI将容器连接到某物。 在此之前，我们需要一些信息。 即，我们需要一个供CNI使用的网络定义以及有关容器本身的一些信息。 对于网络定义，我们将创建一个新定义，并指定其他一些选项以查看其工作方式。 使用此命令创建配置（假设您正在〜/ cni中创建此文件）…

```
cat > mybridge2.conf <<"EOF"
{
    "cniVersion": "0.2.0",
    "name": "mybridge",
    "type": "bridge",
    "bridge": "cni_bridge1",
    "isGateway": true,
    "ipMasq": true,
    "ipam": {
        "type": "host-local",
        "subnet": "10.15.30.0/24",
        "routes": [
            { "dst": "0.0.0.0/0" },
            { "dst": "1.1.1.1/32", "gw":"10.15.30.1"}
        ],
        "rangeStart": "10.15.30.100",
        "rangeEnd": "10.15.30.200",
        "gateway": "10.15.30.99"
    }
}
EOF
```

In addition to the parameters we saw in the last post, we’ve also added the following…

- **rangeStart**: Defines where CNI should start allocating container IPs from within the defined subnet
- **rangeEnd**: Defines the end of the range CNI can use to allocate container IPs
- **gateway**: Defines the gateway that should be defined.  Previously we hadnt defined this so CNI picked the first IP for use as the bridge interface.

One thing you’ll notice that’s lacking in this configuration is anything related to DNS.  Hold that thought for now (it’s the topic of the next post).  您会注意到，此配置中缺少的一件事是与DNS相关的任何内容。 暂时保持这种想法（这是下一篇文章的主题）。

So now that the network is defined we need some info about the container. Specifically we need the path to the container network namespace as well as the container ID. To get that info, we can grep the info from the ‘docker inspect’ command…  因此，既然已经定义了网络，我们就需要有关容器的一些信息。 具体来说，我们需要容器网络名称空间的路径以及容器ID。 要获取该信息，我们可以从“ docker inspect”命令中获取信息。

```
user@ubuntu-1:~/cni$ sudo docker inspect cnitest | grep -E 'SandboxKey|Id'
        "Id": "1018026ebc02fa0cbf2be35325f4833ec1086cf6364c7b2cf17d80255d7d4a27",
            "SandboxKey": "/var/run/docker/netns/2e4813b1a912",
user@ubuntu-1:~/cni$
```

In this example I used the ‘-E’ flag with grep to tell it to do expression or pattern matching as Im looking for both the container ID as well as the SandboxKey. In the world of Docker, the network namespace file location is referred to as the ‘SandboxKey’ and the ‘Id’ is the container ID assigned by Docker.  So now that we have that info, we can build the environmental variables that we’re going to use with the CNI plugin.  Those would be…  在此示例中，我使用了带有-grep的“ -E”标志来告诉它进行表达式或模式匹配，因为Im既要查找容器ID，也要查找SandboxKey。 在Docker世界中，网络名称空间文件位置被称为“ SandboxKey”，而“ Id”是Docker分配的容器ID。 现在，有了这些信息，我们就可以构建将要与CNI插件一起使用的环境变量。 那会是...

- **CNI_COMMAND**=ADD
- **CNI_CONTAINERID**=1018026ebc02fa0cbf2be35325f4833ec1086cf6364c7b2cf17d80255d7d4a27
- **CNI_NETNS**=/var/run/docker/netns/2e4813b1a912
- **CNI_IFNAME**=eth0
- **CNI_PATH**=`pwd`

Put that all together in a command and you end up with this…

```
sudo CNI_COMMAND=ADD CNI_CONTAINERID=1018026ebc02fa0cbf2be35325f4833ec1086cf6364c7b2cf17d80255d7d4a27 CNI_NETNS=/var/run/docker/netns/2e4813b1a912 CNI_IFNAME=eth0 CNI_PATH=`pwd` ./bridge <mybridge2.conf
```

The only thing left to do at this point is to run the plugin…

```
user@ubuntu-1:~/cni$ sudo CNI_COMMAND=ADD CNI_CONTAINERID=1018026ebc02fa0cbf2be35325f4833ec1086cf6364c7b2cf17d80255d7d4a27 CNI_NETNS=/var/run/docker/netns/2e4813b1a912 CNI_IFNAME=eth0 CNI_PATH=`pwd` ./bridge <mybridge2.conf
{
    "ip4": {
        "ip": "10.15.30.100/24",
        "gateway": "10.15.30.99",
        "routes": [
            {
                "dst": "0.0.0.0/0"
            },
            {
                "dst": "1.1.1.1/32",
                "gw": "10.15.30.1"
            }
        ]
    },
    "dns": {}
}user@ubuntu-1:~/cni$
```

As we saw in the last post, the plugin executes and then provides us some return JSON about what it did.  So let’s look at our host and container again to see what we have…

```
user@ubuntu-1:~/cni$ ifconfig
cni_bridge0 Link encap:Ethernet  HWaddr 0a:58:0a:0f:14:01
          inet addr:10.15.20.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::a464:72ff:fe98:2652/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:536 (536.0 B)  TX bytes:648 (648.0 B)

cni_bridge1 Link encap:Ethernet  HWaddr 0a:58:0a:0f:1e:63
          inet addr:10.15.30.99  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::88f:bbff:fed9:118f/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:536 (536.0 B)  TX bytes:648 (648.0 B)

docker0   Link encap:Ethernet  HWaddr 02:42:65:43:f5:a7
          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

ens32     Link encap:Ethernet  HWaddr 00:0c:29:3e:49:51
          inet addr:10.20.30.71  Bcast:10.20.30.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe3e:4951/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:2568909 errors:0 dropped:67 overruns:0 frame:0
          TX packets:2057136 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:478331698 (478.3 MB)  TX bytes:1336636840 (1.3 GB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:5519471 errors:0 dropped:0 overruns:0 frame:0
          TX packets:5519471 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:2796275357 (2.7 GB)  TX bytes:2796275357 (2.7 GB)

veth719c8174 Link encap:Ethernet  HWaddr aa:bb:6e:c7:cc:d8
          inet6 addr: fe80::a8bb:6eff:fec7:ccd8/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:15 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:648 (648.0 B)  TX bytes:1206 (1.2 KB)

vethb125661a Link encap:Ethernet  HWaddr fa:54:99:46:65:08
          inet6 addr: fe80::f854:99ff:fe46:6508/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:15 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:648 (648.0 B)  TX bytes:1206 (1.2 KB)

user@ubuntu-1:~/cni$
```

From a host perspective, we have quite a few interfaces now. Since we picked up right where we left off with the last post we still have the cni_bridge0 interface along with it’s associated VETH pair. We now also have the cni_bridge1 bridge that we just created along with it’s associated VETH pair interface.  You can see that the cni_bridge1 interface has the IP address we defined as the ‘gateway’ as part of the network configuration.  You’ll also notice that the docker0 bridge is there since it was created by default when Docker was installed.  从主机角度来看，我们现在有很多接口。 由于我们从上一条帖子的结尾处开始选取，因此我们仍然拥有cni_bridge0接口及其关联的VETH对。 现在，我们还有刚刚创建的cni_bridge1桥及其关联的VETH对接口。 您可以看到cni_bridge1接口具有我们定义为网络配置一部分的“网关”的IP地址。 您还会注意到docker0桥在那里，因为它是在安装Docker时默认创建的。

So now what about our container?  Let’s look…

```
user@ubuntu-1:~/cni$ sudo docker exec cnitest ifconfig
eth0      Link encap:Ethernet  HWaddr 0a:58:0a:0f:1e:64
          inet addr:10.15.30.100  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::f09e:73ff:fe3e:838c/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:15 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1206 (1.2 KB)  TX bytes:648 (648.0 B)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

user@ubuntu-1:~/cni$ sudo docker exec cnitest ip route
default via 10.15.30.99 dev eth0
1.1.1.1 via 10.15.30.1 dev eth0
10.15.30.0/24 dev eth0  proto kernel  scope link  src 10.15.30.100
user@ubuntu-1:~/cni$
```

As you can see, the container has the network configuration we’d expect…

- It has an IP address within the defined range (10.15.30.100)
- Its interface is named ‘eth0’
- It has a default route pointing at the gateway IP address of 10.15.30.99
- It has an additional route for 1.1.1.1/32 pointing at 10.15.30.1

And as a final quick test we can attempt to access the service in the container from the host…

```
user@ubuntu-1:~/cni$ curl http://10.15.30.100
<body>
<html>
<h1><span style="color:#FF0000;font-size:72px;">Web Server #1 - Running on port 80</span></h1>
</body>
</html>
user@ubuntu-1:~/cni$
```

So as you can see – connecting a Docker container wasn’t much different than connecting a network namespace. In fact – the process was identical, we just had to account for where Docker stores it’s network namespace definitions. In our next post we’re going to talk about DNS related setting for a container and how those play into CNI.  正如您所看到的-连接Docker容器与连接网络名称空间没有太大不同。 实际上，过程是相同的，我们只需要考虑Docker将其网络名称空间定义存储在何处。 在我们的下一篇文章中，我们将讨论容器的DNS相关设置以及它们如何作用于CNI。

[来源](https://www.dasblinkenlichten.com/using-cni-docker/)

