# IPAM and DNS with CNI

In the[ first post ](https://www.dasblinkenlichten.com/understanding-cni-container-networking-interface/)of this series we talked about some of the CNI basics.  We then followed that up with a [second post](https://www.dasblinkenlichten.com/using-cni-docker/) showing a more real world example of how you could use CNI to network a container.  We’ve covered IPAM lightly at this point since CNI relies on it for IP allocation but we haven’t talked about what it’s doing or how it works.  In addition – DNS was discussed from a parameter perspective in the first post where we talked about the CNI spec but that’s about it.  The reason for that is that CNI doesn’t actually configure container DNS.  Confused?  I was too.  I mean why is it in the spec if I can’t configure it?  在本系列的第一篇文章中，我们讨论了一些CNI基础知识。 然后，我们在第二篇文章中继续介绍了如何使用CNI来联网容器的更真实的示例。 由于CNI依靠IPAM进行IP分配，因此我们在此不做介绍。但是我们尚未谈论IPAM的工作或工作方式。 此外，在第一篇文章中我们从参数角度讨论了DNS，但我们仅讨论了CNI规范。 原因是CNI实际上没有配置容器DNS。 困惑？ 我也是。 我的意思是为什么我不能配置它在规范中呢？

To answer these questions, and see how IPAM and DNS work with CNI, I think a deep dive into an actual CNI implementation would be helpful.  That is – let’s look at a tool that actually implements CNI to see how it uses it.  To do that we’re going to look at the container runtime from the folks at CoreOS – Rocket (rkt).  Rkt can be installed fairly easily using this set of commands…  为了回答这些问题，并了解IPAM和DNS如何与CNI配合使用，我认为深入研究实际的CNI实施将很有帮助。 也就是说–让我们看一下实际实现CNI的工具，看看它如何使用它。 为此，我们将从CoreOS – Rocket（rkt）的人员那里了解容器运行时。 使用这组命令可以相当容易地安装Rkt。

```
wget https://github.com/coreos/rkt/releases/download/v1.25.0/rkt_1.25.0-1_amd64.deb
wget https://github.com/coreos/rkt/releases/download/v1.25.0/rkt_1.25.0-1_amd64.deb.asc
gpg --keyserver keys.gnupg.net --recv-key 18AD5014C99EF7E3BA5F6CE950BDD3E0FC8A365E
gpg --verify rkt_1.25.0-1_amd64.deb.asc
sudo dpkg -i rkt_1.25.0-1_amd64.deb
```

After you install rkt check to make sure it’s working…

```
user@ubuntu-1:~$ sudo rkt version
rkt Version: 1.25.0
appc Version: 0.8.10
Go Version: go1.7.4
Go OS/Arch: linux/amd64
Features: -TPM +SDJOURNAL
user@ubuntu-1:~$
```

*Note: This post is not intended to be a ‘How to get started with rkt’ guide.  I might do something similar in the future but right now the focus is on CNI.*  注意：本文并非旨在作为“如何使用rkt入门”指南。 将来我可能会做类似的事情，但现在的重点是CNI。

Great so now what? I mentioned above that rkt implements CNI. In other words, rkt uses CNI to configure a containers network interface.  Before we jump into that though – let’s talk about what’s already in place from the work we did in the first two posts. Let’s take a look at some files on the system to see what CNI has done up to this point…  太好了，现在呢？ 我在上面提到rkt实现了CNI。 换句话说，rkt使用CNI来配置容器网络接口。 在开始讨论之前，让我们先谈谈前两篇文章中所做的工作。 让我们看一下系统上的一些文件，以了解到目前为止，CNI已经完成了哪些工作……

```
user@ubuntu-1:~/cni$ sudo su
root@ubuntu-1:/home/user/cni# cd /var/lib/cni/networks
root@ubuntu-1:/var/lib/cni/networks# ls
mybridge
root@ubuntu-1:/var/lib/cni/networks#
```

Notice we switched over to the root user to make looking at these files easier. If we look in the ‘/var/lib/cni/networks’ path we should see a directory using the name of the network we defined. If you go back and look at the two previous posts you’ll notice that despite the networks being different – I neglected to change the name of the network between definitions. I only changed the ‘bridge’ parameter. If we look in the ‘mybridge’ folder we should see a few files…  请注意，我们已切换到root用户，以便于查看这些文件。 如果我们在“ /var/lib/cni/networks”路径中查找，我们应该会看到一个使用我们定义的网络名称的目录。 如果您回头看看前两篇文章，您会注意到尽管网络不同，但我忽略了在定义之间更改网络的名称。 我只更改了“ bridge”参数。 如果我们在“ mybridge”文件夹中查找，我们应该会看到一些文件…

```
root@ubuntu-1:/var/lib/cni/networks# cd mybridge/
root@ubuntu-1:/var/lib/cni/networks/mybridge# ls
10.15.20.2  10.15.30.100  last_reserved_ip
root@ubuntu-1:/var/lib/cni/networks/mybridge# more 10.15.20.2
1234567890
root@ubuntu-1:/var/lib/cni/networks/mybridge# more 10.15.30.100
1018026ebc02fa0cbf2be35325f4833ec1086cf6364c7b2cf17d80255d7d4a27
root@ubuntu-1:/var/lib/cni/networks/mybridge# more last_reserved_ip
10.15.30.100
root@ubuntu-1:/var/lib/cni/networks/mybridge#
```

Looking at the files we see some familiar values. The ‘10.15.20.2’ file has ‘1234567890’ in it which is the name of the network namespace from the first post. The ‘10.15.30.100’ file has the value of ‘1018026ebc02fa0cbf2be35325f4833ec1086cf6364c7b2cf17d80255d7d4a27’ which is the container ID we passed to CNI when we connected a Docker container with CNI in the second post. The last file is called ‘last_reserved_ip’ and has the value of 10.15.30.100 in it.  The last_reserved_ip file is sort of a helper file to tell CNI what the next IP is that it can allocate.  In this case, since the last IP was allocated out of the 10.15.30.0/24 network it lists that IP address.  查看文件，我们会看到一些熟悉的值。 “ 10.15.20.2”文件中包含“ 1234567890”，这是第一篇文章中网络名称空间的名称。 “ 10.15.30.100”文件的值为“ 1018026ebc02fa0cbf2be35325f4833ec1086cf6364c7b2cf17d80255d7d4a27”，这是我们在第二篇文章中将Docker容器与CNI连接时传递给CNI的容器ID。 最后一个文件称为“ last_reserved_ip”，其中的值为10.15.30.100。 last_reserved_ip文件是一种帮助程序文件，用于告诉CNI它可以分配的下一个IP是什么。 在这种情况下，由于最后一个IP是从10.15.30.0/24网络中分配的，因此它将列出该IP地址。

So why are these files here?  Well they’re here because in both of the previous posts we told CNI to use the ‘host-local’ IPAM driver.  This is what host-local does, it stores all of the allocation locally on the host.  Pretty straight forward.  Let’s create another network definition on this host and use in conjunction with rkt so you can see it in action…  那么为什么这些文件在这里？ 好吧，他们在这里是因为在之前的两个帖子中，我们都告诉CNI使用“本地主机” IPAM驱动程序。 这是本地主机所做的，它将所有分配本地存储在主机上。 非常简单。 让我们在此主机上创建另一个网络定义，并将其与rkt结合使用，以便您可以实际使用它…

```
root@ubuntu-1:~# mkdir /etc/rkt/net.d
root@ubuntu-1:~# cd /etc/rkt/net.d
root@ubuntu-1:/etc/rkt/net.d#
root@ubuntu-1:/etc/rkt/net.d# cat > custom_rkt_bridge.conf <<"EOF"
> {
>     "cniVersion": "0.2.0",
>     "name": "customrktbridge",
>     "type": "bridge",
>     "bridge": "cni0",
>     "isGateway": true,
>     "ipMasq": true,
>     "ipam": {
>         "type": "host-local",
>         "subnet": "10.11.0.0/16",
>         "routes": [
>             { "dst": "0.0.0.0/0" }
>         ]
>     }
> }
> EOF
root@ubuntu-1:/etc/rkt/net.d#
```

The first thing we want to do is to create a new network definition.  In the previous posts, we were storing that in our ‘~/cni’ directory and passing it directly to the CNI plugin.  In this case, we want rkt to consume the configuration so we need to put it where rkt can find it.  In this case, the default directory rkt searches for network configuration files is ‘/etc/rkt/net.d/’.  So we’ll create the ‘net.d’ directory and then create this new network configuration in it.  Notice that the name of this network is ‘customrktbridge’.  Now let’s run a simple container on the host using rkt…  我们要做的第一件事是创建一个新的网络定义。 在之前的文章中，我们将其存储在“〜/ cni”目录中，并将其直接传递给CNI插件。 在这种情况下，我们希望rkt使用配置，因此我们需要将其放在rkt可以找到它的位置。 在这种情况下，搜索网络配置文件的默认目录rkt是“ /etc/rkt/net.d/”。 因此，我们将创建“ net.d”目录，然后在其中创建此新的网络配置。 请注意，该网络的名称为“ customrktbridge”。 现在，让我们使用rkt在主机上运行一个简单的容器…

```
user@ubuntu-1:~$ sudo rkt run --interactive --net=customrktbridge quay.io/coreos/alpine-sh
pubkey: prefix: "quay.io/coreos/alpine-sh"
key: "https://quay.io/aci-signing-key"
gpg key fingerprint is: BFF3 13CD AA56 0B16 A898 7B8F 72AB F5F6 799D 33BC
 Quay.io ACI Converter (ACI conversion signing key) <support@quay.io>
Are you sure you want to trust this key (yes/no)?
yes
Trusting "https://quay.io/aci-signing-key" for prefix "quay.io/coreos/alpine-sh" after fingerprint review.
Added key for prefix "quay.io/coreos/alpine-sh" at "/etc/rkt/trustedkeys/prefix.d/quay.io/coreos/alpine-sh/bff313cdaa560b16a8987b8f72abf5f6799d33bc"
Downloading signature: [=======================================] 473 B/473 B
Downloading ACI: [=============================================] 2.65 MB/2.65 MB
image: signature verified:
 Quay.io ACI Converter (ACI conversion signing key) <support@quay.io>
/ #
/ # ifconfig
eth0 Link encap:Ethernet HWaddr 62:5C:46:9F:57:3A
 inet addr:10.11.0.2 Bcast:0.0.0.0 Mask:255.255.0.0
 inet6 addr: fe80::605c:46ff:fe9f:573a/64 Scope:Link
 UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
 RX packets:6 errors:0 dropped:0 overruns:0 frame:0
 TX packets:7 errors:0 dropped:0 overruns:0 carrier:0
 collisions:0 txqueuelen:0
 RX bytes:508 (508.0 B) TX bytes:578 (578.0 B)

eth1 Link encap:Ethernet HWaddr A2:EE:49:17:03:EA
 inet addr:172.17.0.2 Bcast:0.0.0.0 Mask:255.255.0.0
 inet6 addr: fe80::a0ee:49ff:fe17:3ea/64 Scope:Link
 UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
 RX packets:7 errors:0 dropped:0 overruns:0 frame:0
 TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
 collisions:0 txqueuelen:0
 RX bytes:578 (578.0 B) TX bytes:508 (508.0 B)

lo Link encap:Local Loopback
 inet addr:127.0.0.1 Mask:255.0.0.0
 inet6 addr: ::1/128 Scope:Host
 UP LOOPBACK RUNNING MTU:65536 Metric:1
 RX packets:0 errors:0 dropped:0 overruns:0 frame:0
 TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
 collisions:0 txqueuelen:1
 RX bytes:0 (0.0 B) TX bytes:0 (0.0 B)

/ #
/ # Container rkt-596c724a-f3de-4892-aebf-83529d0f386f terminated by signal KILL.
user@ubuntu-1:~$
```

*To exit the containers interactive shell use the key sequence Ctrl + ]]]*

The command we executed told rkt to run a container in interactive mode, using the network ‘customrktbridge’, from the container ‘quay.io/coreos/alpine-sh’.  Once the container was running we looked at it’s interfaces and found that in addition to a loopback interface, it also has a eth0 and eth1 interface.  Eth0 seems to line up with what we defined as part of our custom CNI network but what about eth1?  Well eth1 is an interface on what rkt refers to as the ‘default-restricted’ network.  This is one of the built in network types that rkt provides by default.  So now you’re wondering what rkt provides by default.  There are two networks that rkt defines by default.  They are the ‘default’ and the ‘default-restricted’ networks. As you might expect, the definitions for these networks are in CNI and you can take a look at them right [here in the GitHub repo](https://github.com/coreos/rkt/tree/master/stage1/net/rootfs/etc/rkt/net.d).  Let’s review them quickly so we can get an idea of what each provides…  我们执行的命令告诉rkt使用网络“ customrktbridge”从容器“ quay.io/coreos/alpine-sh”以交互模式运行容器。 容器运行后，我们查看了其接口，发现除了回送接口之外，它还具有eth0和eth1接口。 eth0似乎与我们定义为自定义CNI网络的一部分一致，但是eth1呢？ eth1是rkt称为“默认限制”网络的接口。 这是rkt默认提供的内置网络类型之一。 因此，现在您想知道rkt默认提供的功能。 rkt默认定义两个网络。 它们是“默认”和“默认限制”网络。 如您所料，这些网络的定义在CNI中，您可以在GitHub存储库中的此处进行查看。 让我们快速查看一下它们，以便我们对它们各自提供的功能有所了解...

```
{
	"cniVersion": "0.1.0",
	"name": "default",
	"type": "ptp",
	"ipMasq": true,
	"ipam": {
		"type": "host-local",
		"subnet": "172.16.28.0/24",
		"routes": [
			{ "dst": "0.0.0.0/0" }
		]
	}
}
```

The above CNI network definition describes the default network.  We can tell that this network uses the ‘ptp’ CNI driver, enables outbound masquerading, uses the host-local IPAM plugin, allocates container IPs from the 172.16.28.0/24 subnet, and installs a default route in the container.  Most of this seems pretty straight forward except for the ptp type.  That’s something we haven’t talked about yet but for now just know that it creates a VETH pair for each container.  One end lives on the host and the other lives in the container.  This is different from the default Docker model where the host side of the VETH pair goes into the docker0 bridge which acts as the container’s gateway.  In the ptp case, the host side VETH pairs are IP’d.  In fact – they’re IP’d using the same IP.  If you created multiple containers with rkt using the default network you’d see a bunch of VETH pair interfaces on the host all with 172.16.28.1/24.  In addition, you’d see routes for each container on the host pointing to the host side VETH pair for each destination IP in the container.  上面的CNI网络定义描述了默认网络。我们可以知道，该网络使用了“ ptp” CNI驱动程序，启用了出站伪装，使用了主机本地IPAM插件，从172.16.28.0/24子网分配了容器IP，并在容器中安装了默认路由。除ptp类型外，其中大多数似乎很简单。我们还没有讨论过这一点，但是现在就知道它为每个容器创建了一个VETH对。一端住在主机上，另一端住在容器中。这与默认的Docker模型不同，在默认的Docker模型中，VETH对的主机侧进入充当容器网关的docker0网桥。在ptp情况下，主机端VETH对是IP。实际上，它们是使用相同IP的IP。如果您使用默认网络通过rkt创建了多个容器，则会在主机上看到一堆VETH对接口，所有接口均为172.16.28.1/24。此外，您会看到主机上每个容器的路由，指向该容器中每个目标IP的主机侧VETH对。

```
{
	"cniVersion": "0.1.0",
	"name": "default-restricted",
	"type": "ptp",
	"ipMasq": false,
	"ipam": {
		"type": "host-local",
		"subnet": "172.17.0.0/16"
	}
}
```

The above shows the CNI network definition for the default-restricted network which is what we saw in our output above.  We can tell this network uses the ptp CNI driver, disables out bound masquerading, uses the host-local IPAM plugin, and allocates container IPs out of the 172.17.0.0/16 subnet.  So the real question is why does our container have an interface on this network?  The answer lies in the docs (taken from [here](https://coreos.com/rkt/docs/latest/networking/overview.html))…  上面显示了默认受限网络的CNI网络定义，这是我们在上面的输出中看到的。 我们可以告诉该网络使用ptp CNI驱动程序，禁用绑定伪装，使用主机本地IPAM插件，并在172.17.0.0/16子网中分配容器IP。 因此，真正的问题是为什么我们的容器在此网络上具有接口？ 答案在于文档（从此处获取）…

> The *default-restricted* network does not set up the default route and IP masquerading. It only allows communication with the host via the veth interface and thus enables the pod to communicate with the metadata service which runs on the host. If *default* is not among the specified networks, the *default-restricted* network will be added to the list of networks automatically. It can also be loaded directly by explicitly passing `--net=default-restricted`.  默认受限网络不会设置默认路由和IP伪装。 它仅允许通过veth接口与主机进行通信，因此使pod可以与在主机上运行的元数据服务进行通信。 如果默认值不在指定的网络中，则默认限制的网络将自动添加到网络列表中。 也可以通过显式传递--net = default-restricted直接加载。

So that interfaces is put there intentionally for communication to the metadata service.  Again – this article isnt intended to be a deep drive on rkt networking – but I felt it was important to explain where all the container interfaces come from.  Ok – So now that we ran our container – let’s now go and look at our ‘/var/lib/cni/networks’ directory again…  因此，有意将接口放置在此处以便与元数据服务进行通信。 再说一次-本文并非旨在深入探讨rkt网络-但我认为解释所有容器接口的来源很重要。 好的–现在我们运行了容器–现在让我们再次查看“ /var/lib/cni/networks”目录…

```
user@ubuntu-1:~$ sudo su
[sudo] password for user:
root@ubuntu-1:/home/user# cd /var/lib/cni/networks/
root@ubuntu-1:/var/lib/cni/networks# ls
customrktbridge  default-restricted  mybridge
root@ubuntu-1:/var/lib/cni/networks#
root@ubuntu-1:/var/lib/cni/networks# cd customrktbridge/
root@ubuntu-1:/var/lib/cni/networks/customrktbridge# ls
10.11.0.2
root@ubuntu-1:/var/lib/cni/networks/customrktbridge# more 10.11.0.2
8d7152a7-9c53-48d8-859e-c8469d5adbdb
root@ubuntu-1:/var/lib/cni/networks/customrktbridge# cd ..
root@ubuntu-1:/var/lib/cni/networks# cd default-restricted/
root@ubuntu-1:/var/lib/cni/networks/default-restricted# ls
172.17.0.2
root@ubuntu-1:/var/lib/cni/networks/default-restricted# more 172.17.0.2
8d7152a7-9c53-48d8-859e-c8469d5adbdb
root@ubuntu-1:/var/lib/cni/networks/default-restricted#
```

This is what I’d expect to see. Rkt launched a container using CNI that ended up having two interfaces. One of which was the ‘customrktnetwork’ we defined and the other was the ‘default-restricted’ network that rkt connected for us by default. Since both plugins use the host-local IPAM driver they both got folders in ‘/var/lib/cni/networks’/ and they both have entries showing the assigned IP address as well and the container ID.  这就是我希望看到的。 Rkt使用CNI启动了一个容器，该容器最终具有两个接口。 其中一个是我们定义的“ customrktnetwork”，另一个是rkt默认为我们连接的“默认限制”网络。 由于这两个插件都使用本地主机IPAM驱动程序，因此它们都在“ /var/lib/cni/networks” /中获得了文件夹，并且都具有显示分配的IP地址和容器ID的条目。

*If you did a ‘sudo rkt list –full’ you’d see the full container ID which is ‘8d7152a7-9c53-48d8-859e-c8469d5adbdb’*

At this point – we’ve shown how rkt uses CNI to provision container networks and how the host-local IPAM driver stores that information on the host locally.  You might now be wondering if there are other options for IPAM (I know I was).  If so – you’re in luck because by default, CNI also comes with the DHCP IPAM plugin.  So let’s take a look at a custom CNI network definition that uses DHCP for IPAM…  至此，我们已经展示了rkt如何使用CNI来配置容器网络，以及本地主机IPAM驱动程序如何将该信息存储在本地主机上。 您现在可能想知道IPAM是否还有其他选择（我知道是）。 如果是这样，那么您会很幸运，因为默认情况下，CNI还附带了DHCP IPAM插件。 因此，让我们看一下使用DHCP进行IPAM的自定义CNI网络定义…

```
user@ubuntu-1:/etc/rkt/net.d$ sudo su
root@ubuntu-1:/etc/rkt/net.d# cd /etc/rkt/net.d
root@ubuntu-1:/etc/rkt/net.d#
root@ubuntu-1:/etc/rkt/net.d# cat > custom_rkt_bridge_dhcp.conf <<"EOF" > {
>     "cniVersion": "0.2.0",
>     "name": "customrktbridgedhcp",
>     "type": "macvlan",
>     "master": "ens32",
>     "ipam": {
>         "type": "dhcp"
>     }
> }
> EOF
root@ubuntu-1:/etc/rkt/net.d# exit
exit
user@ubuntu-1:/etc/rkt/net.d$t
```

There are again some new things in this CNI network definition. Namely – you should see that the type of this network is being defined as MacVLAN. In order to use an external DHCP service we need to get the containers network interface right onto the physical network. The easiest way to do this is to use MacVLAN which will put the containers interface directly onto the host network. This isn’t a post on MacVLAN so I’ll be leaving the details of how that works out. For now just know that this works by using the hosts interface (in this case ens32) as the parent or master interface for the containers interface. You’ll also note that we are now using an IPAM type of dhcp rather than host-local. DHCP acts just the way you’d expect, it relies on an external DHCP server to get IP address information for the container. The only catch is that for this to work we need to run CNI’s DHCP daemon to allow the container to get a DHCP address. The DHCP process will act as a proxy between the client in the container and the DHCP service that’s preexisting on your network. If you’ve completed the first two posts in this series you already have that binary in your ~/cni directory. To test this we’ll need two SSH sessions to our server. In the first, we’ll start CNI’s DHCP binary…  这个CNI网络定义中又有一些新事物。即–您应该看到该网络的类型被定义为MacVLAN。为了使用外部DHCP服务，我们需要将容器网络接口直接连接到物理网络。最简单的方法是使用MacVLAN，它将容器接口直接放置到主机网络上。这不是MacVLAN上的帖子，因此我将详细说明其工作原理。现在，只知道可以通过使用hosts接口（在本例中为ens32）作为容器接口的父接口或master接口来工作。您还将注意到，我们现在使用的是IPAM类型的dhcp，而不是本地主机。 DHCP的运行方式与您期望的一样，它依赖于外部DHCP服务器来获取容器的IP地址信息。唯一要注意的是，要使此方法起作用，我们需要运行CNI的DHCP守护程序，以允许容器获取DHCP地址。 DHCP进程将充当容器中的客户端与网络上预先存在的DHCP服务之间的代理。如果您已完成本系列的前两篇文章，则您的〜/ cni目录中已经具有该二进制文件。要进行测试，我们需要两个到服务器的SSH会话。首先，我们将启动CNI的DHCP二进制文件…

```
user@ubuntu-1:~/cni$ cd ~/cni
user@ubuntu-1:~/cni$ sudo ./dhcp daemon
```

Since we’re just running the executable here the process will just hang until it needs to do something. In our second window, let’s start a new container using our new network definition…  由于我们仅在此处运行可执行文件，因此该过程将挂起，直到需要执行某些操作为止。 在第二个窗口中，让我们使用新的网络定义来启动新的容器...

```
user@ubuntu-1:~$ sudo rkt run --interactive --net=customrktbridgedhcp quay.io/coreos/alpine-sh
/ # ifconfig
eth0      Link encap:Ethernet  HWaddr 92:97:2C:B5:6A:B7
          inet addr:10.20.30.152  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::9097:2cff:feb5:6ab7/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:6 errors:0 dropped:0 overruns:0 frame:0
          TX packets:9 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:936 (936.0 B)  TX bytes:1206 (1.1 KiB)

eth1      Link encap:Ethernet  HWaddr FE:55:51:EF:27:48
          inet addr:172.17.0.8  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::fc55:51ff:feef:2748/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:6 errors:0 dropped:0 overruns:0 frame:0
          TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:508 (508.0 B)  TX bytes:508 (508.0 B)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

/ #
```

In this case, my DHCP server is allocating IP addresses out of 10.20.30.0/24 so our container ended up with 10.20.30.152. However, if we check the routing table, we’ll see that the container does not have a default route (this seems like something that should work so I opened a GH issue on it [here](https://github.com/containernetworking/cni/issues/389).  In other words – there’s a chance I’m doing this wrong but I don’t think I am)…  在这种情况下，我的DHCP服务器分配了10.20.30.0/24之外的IP地址，因此我们的容器最终分配了10.20.30.152。 但是，如果我们检查路由表，就会发现该容器没有默认路由（这似乎应该可以工作，所以我在这里打开了GH问题。换句话说，我有机会 做错了，但我不认为我是…）

```
/ # ip route
10.20.30.0/24 dev eth0  src 10.20.30.152
172.17.0.0/16 via 172.17.0.1 dev eth1  src 172.17.0.8
172.17.0.1 dev eth1  src 172.17.0.8
/ #
```

My assumption was that this should have been added by the DHCP plugin and captured as a DHCP option but it was not. If we look back at our first window we can see that the DHCP daemon is working though…  我的假设是应该由DHCP插件添加它并将其捕获为DHCP选项，但事实并非如此。 如果我们回头看第一个窗口，可以看到DHCP守护进程正在运行……

```
user@ubuntu-1:~/cni$ sudo ./dhcp daemon
2017/03/02 22:41:40 6f4945b1-9a03-4b72-88e8-049c2a1e24ea/customrktbridgedhcp: acquiring lease
2017/03/02 22:41:40 Link "eth0" down. Attempting to set up
2017/03/02 22:41:40 network is down
2017/03/02 22:41:46 6f4945b1-9a03-4b72-88e8-049c2a1e24ea/customrktbridgedhcp: lease acquired, expiration is 2017-03-03 09:41:46.125345466 -0600 CST
```

So we can see how the DHCP plugin can work – but in it’s current state it doesn’t seem quite usable to me.  I will stress that the CNI plugins provided by default are meant to showcase the possibilities for what CNI can do. I don’t believe all of them are meant to be or are used in ‘production’. As we’ll see in later posts – other systems use CNI and write their own CNI compatible plugins.  因此，我们可以看到DHCP插件如何工作-但在目前的状态下，它对我来说似乎不太可用。 我会强调，默认情况下提供的CNI插件旨在展示CNI可以做什么的可能性。 我不认为所有这些都是“生产”中使用或用于“生产”中的。 正如我们将在以后的文章中看到的那样-其他系统使用CNI并编写自己的CNI兼容插件。

So what about DNS? We haven’t touched on that yet. Do you recall from our first and second post that when we manually ran the CNI plugin we got a JSON return? Here’s a copy and paste from the first post of the output Im referring to…  那么DNS呢？ 我们还没有涉及。 您还记得第一篇和第二篇文章中的内容，当我们手动运行CNI插件时，我们得到了JSON返回值？ 这是输出Im的第一篇文章的副本和粘贴，指的是…

```
{
    "ip4": {
        "ip": "10.15.20.2/24",
        "gateway": "10.15.20.1",
        "routes": [
            {
                "dst": "0.0.0.0/0"
            },
            {
                "dst": "1.1.1.1/32",
                "gw": "10.15.20.1"
            }
        ]
    },
    "dns": {}
```

See that empty DNS dictionary at the bottom? It’s empty because we were using the host-local IPAM driver which doesn’t currently support DNS. But what does supporting DNS even mean in the context of CNI? It doesnt mean what I thought it meant initially. My assumption was that I could pass DNS related parameters to CNI and have it install those settings (DNS name server, search domain, etc) in the container. That was an incorrect assumption. The DNS parameters are return parameters that CNI can pass to whatever invoked it. In the case of DHCP – you could see how that would be useful as CNI could return information it learned from the DHCP server back to rkt in order to configure DNS in the container. Unfortunately, both the default bundled IPAM drivers (host-local and DHCP) don’t currently support returning DNS related information which is why you see an empty DNS return in the CNI JSON response.  There is a [current PR](https://github.com/containernetworking/cni/pull/321) in the repo for adding this functionality to the DHCP plugin so if and when that happens we’ll revist it.  看到底部的空DNS字典了吗？它为空，因为我们使用的是主机本地IPAM驱动程序，该驱动程序当前不支持DNS。但是在CNI的背景下，支持DNS甚至意味着什么？这并不意味着我最初的想法。我的假设是我可以将DNS相关的参数传递给CNI，并让它在容器中安装那些设置（DNS名称服务器，搜索域等）。那是一个错误的假设。 DNS参数是CNI可以传递给调用它的任何对象的返回参数。在使用DHCP的情况下–您将看到CNI将从DHCP服务器学到的信息返回给rkt以便配置容器中的DNS的好处。不幸的是，默认捆绑的IPAM驱动程序（主机本地和DHCP）目前均不支持返回DNS相关信息，这就是为什么您在CNI JSON响应中看到空DNS返回的原因。存储库中有一个当前PR，用于将此功能添加到DHCP插件中，因此，如果发生这种情况，我们将对其进行修正。

Next up we’re going to revisit another system that uses CNI (cough, Kubernetes, cough).  下一步，我们将重新审视使用CNI的另一个系统（咳嗽，Kubernetes，咳嗽）。

[来源](https://www.dasblinkenlichten.com/ipam-dns-cni/)

