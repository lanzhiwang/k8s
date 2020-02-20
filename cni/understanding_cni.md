# Understanding CNI (Container Networking Interface)

If you’ve been paying attention to the discussions around container networking you’ve likely heard the acronym CNI being used.  CNI stands for Container Networking Interface and it’s goal is to create a generic plugin-based networking solution for containers.  CNI is defined by a [spec ](https://github.com/containernetworking/cni/blob/master/SPEC.md)(read it now, its not very long) that has some interesting language in it.  Here are a couple of points I found interesting during my first read through…  如果您一直关注有关容器网络的讨论，您可能已经听过使用CNI的首字母缩略词。 CNI代表容器网络接口，它的目标是为容器创建一个通用的基于插件的网络解决方案。 CNI由一个规范定义（现在读它，它不是很长），其中有一些有趣的语言。 以下是我在第一次阅读时发现有趣的几点......

- The spec defines a container as being a Linux network namespace.  We should be comfortable with that definition as container runtimes like Docker create a new network namespace for each container.  规范将容器定义为Linux网络命名空间。 我们应该熟悉这个定义，因为像Docker这样的容器运行时为每个容器创建一个新的网络命名空间。
- Network definitions for CNI are stored as JSON files.
- The network definitions are streamed to the plugin through STDIN.  That is – there are no configuration files sitting on the host for the network configuration.  网络定义通过STDIN流式传输到插件。 也就是说 - 主机上没有用于网络配置的配置文件。
- Other arguments are passed to the plugin via environmental variables
- A CNI plugin is implemented as an executable.
- The CNI plugin is responsible wiring up the container.  That is – it needs to do all the work to get the container on the network.  In Docker, this would include connecting the container network namespace back to the host somehow.  CNI插件负责连接容器。 也就是说 - 它需要完成所有工作才能将容器放到网络上。 在Docker中，这将包括以某种方式将容器网络命名空间连接回主机。
- The CNI plugin is responsible for IPAM which includes IP address assignment and installing any required routes.

If you’re used to dealing with Docker this doesn’t quite seem to fit the mold.  It’s apparent to me that the CNI plugin is responsible for the network end of the container, but it wasn’t initially clear to me how that was actually implemented.  So the next question might be, can I use CNI with Docker?  The answer is yes, but not as an all in one solution.  Docker has it’s own network plugin system called CNM.  CNM allows plugins to interact directly with Docker.  A CNM plugin can be registered to Docker and used directly from it.  That is, you can use Docker to run containers and directly assign their network to the CNM registered plugin.  This works well, but because Docker has CNM, they dont directly integrate with CNI (as far as I can tell).  That does not mean however, that you can’t use CNI with Docker.  Recall from the sixth bullet above that the plugin is responsible for wiring up the container.  So it seems possible that Docker could be the container runtime – but not handle the networking end of things (more on this in a future post).  如果您习惯于与Docker打交道，那么这似乎并不适合模具。对我来说很明显，CNI插件负责容器的网络端，但我最初并不清楚它是如何实际实现的。那么下一个问题可能是，我可以将CNI与Docker一起使用吗？答案是肯定的，但不是一体化的解决方案。 Docker拥有自己的网络插件系统CNM。 CNM允许插件直接与Docker交互。 CNM插件可以注册到Docker并直接从它使用。也就是说，您可以使用Docker运行容器并直接将其网络分配给CNM注册的插件。这很好用，但由于Docker有CNM，他们不直接与CNI集成（据我所知）。但这并不意味着您不能将CNI与Docker一起使用。回想一下上面的第六个子弹，该插件负责连接容器。所以Docker似乎可能是容器运行时 - 但是没有处理网络端的事情（在未来的帖子中更多关于此）。

At this point – I think its fair to start looking at what CNI actually does to try to get a better feel for how it fits into the picture.  Let’s look at a quick example of using one of the plugins.  在这一点上 - 我认为公平地开始考虑CNI实际上做了什么来试图更好地了解它如何适应图片。 让我们看一个使用其中一个插件的快速示例。

Let’s start by downloading the pre-built CNI binaries…

```
user@ubuntu-1:~$ mkdir cni
user@ubuntu-1:~$ cd cni
user@ubuntu-1:~/cni$ curl -O -L https://github.com/containernetworking/cni/releases/download/v0.4.0/cni-amd64-v0.4.0.tgz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   597    0   597    0     0   1379      0 --:--:-- --:--:-- --:--:--  1381
100 15.3M  100 15.3M    0     0  4606k      0  0:00:03  0:00:03 --:--:-- 5597k
user@ubuntu-1:~/cni$
user@ubuntu-1:~/cni$ tar -xzvf cni-amd64-v0.4.0.tgz
./
./macvlan
./dhcp
./loopback
./ptp
./ipvlan
./bridge
./tuning
./noop
./host-local
./cnitool
./flannel
user@ubuntu-1:~/cni$
user@ubuntu-1:~/cni$ ls
bridge  cni-amd64-v0.4.0.tgz  cnitool  dhcp  flannel  host-local  ipvlan  loopback  macvlan  noop  ptp  tuning
```

Ok – let’s make sure we understand what we just did there.  We first created a directory called ‘cni’ to store the binaries in.  We then used the curl command to download the CNI release bundle.  When using curl to download a file we need to pass the ‘O’ parameter to tell curl to output to a file.  We also need to pass the ‘L’ parameter in this case to allow curl to follow redirects since the URL we’re downloading from is actually redirecting us elsewhere.  Once downloaded, we unpack the archive using the tar command.  好的 - 让我们确保我们理解我们刚刚在那里做了什么。 我们首先创建了一个名为“cni”的目录来存储二进制文件。然后我们使用curl命令下载CNI版本包。 当使用curl下载文件时，我们需要传递'O'参数来告诉curl输出到文件。 在这种情况下，我们还需要传递'L'参数以允许curl遵循重定向，因为我们下载的URL实际上是将我们重定向到其他地方。 下载完成后，我们使用tar命令解压缩归档文件。

After all of that we can see that we have a few new files.  For right now, let’s focus on the ‘bridge’ file which is the bridge plugin.  Bridge is one of the included plugins that ships with CNI.  It’s job, as you might have guessed, is to attach a container to a bridge interface.  So now that we have the plugins, how do we actually use them?  One of the earlier bullet points mentioned that network configuration is streamed into the plugin through STDIN.  So we know we need to use STDIN to get information about the network into the plugin but that’s not all the info the plugin needs.  The plugin also needs more information such as the action you wish to perform, the namespace you wish to work with, and other various information.  This information is passed to the plugin via environmental variables.  Confused?  No worries, let’s walk through an example.  Let’s first define a network configuration file we wish to use for our bridge…  毕竟，我们可以看到我们有一些新文件。 现在，让我们关注作为桥接插件的“桥”文件。 Bridge是CNI附带的插件之一。 正如您可能已经猜到的那样，它的工作是将容器连接到桥接接口。 那么现在我们有了插件，我们如何实际使用它们？ 早期的一个要点提到网络配置通过STDIN流入插件。 所以我们知道我们需要使用STDIN将有关网络的信息添加到插件中，但这不是插件所需的全部信息。 该插件还需要更多信息，例如您希望执行的操作，您希望使用的命名空间以及其他各种信息。 此信息通过环境变量传递给插件。 困惑？ 不用担心，让我们来看一个例子吧。 让我们首先定义一个我们希望用于桥梁的网络配置文件......

```
cat > mybridge.conf <<"EOF"
{
    "cniVersion": "0.2.0",
    "name": "mybridge",
    "type": "bridge",
    "bridge": "cni_bridge0",
    "isGateway": true,
    "ipMasq": true,
    "ipam": {
        "type": "host-local",
        "subnet": "10.15.20.0/24",
        "routes": [
            { "dst": "0.0.0.0/0" },
            { "dst": "1.1.1.1/32", "gw":"10.15.20.1"}
        ]
    }
}
EOF
```

Above we create a JSON definition for our bridge network.  There are some CNI generic definitions listed above as well as some specific to the bridge plugin itself.  Let’s walk through them one at a time.

## CNI generic parameters

- **cniVersion**: The version of the CNI spec in which the definition works with
- **name**: The network name
- **type**: The name of the plugin you wish to use.  In this case, the actual name of the plugin executable
- args: Optional additional parameters
- **ipMasq**: Configure outbound masquerade (source NAT) for this network
- **ipam**
  - **type**: The name of the IPAM plugin executable
  - **subnet**: The subnet to allocate out of (this is actually part of the IPAM plugin)
  - **routes**
    - **dst**: The subnet you wish to reach
    - **gw**: The IP address of the next hop to reach the dst.  If not specified the default gateway for the subnet is assumed
- dns:
  - nameservers: A list of nameservers you wish to use with this network
  - domain: The search domain to use for DNS requests
  - search: A list of search domains
  - options: A list of options to be passed to the receiver

## Plugin (bridge) specific parameters

- **isgateway**: If true, assigns an IP address to the bridge so containers connected to it may use it as a gateway.
- isdefaultgateway: If true, sets the assigned IP address as the default route.
- forceAddress: Tells the plugin to allocate a new IP address if the previous value has changed.
- mtu: Define the MTU of the bridge.
- hairpinMode: Set hairpin mode for the interfaces on the bridge

The items that are in bold above are the ones we’re using in this example.  You should play around with the others to get a feeling for how they work but most are fairly straight forward.  You’ll also note that one of the items is part of the IPAM plugin.  We arent going to cover those in this post (we will later!) but for now just know that we’re using multiple CNI plugins to make this work.  上面以粗体显示的项目是我们在此示例中使用的项目。 你应该与其他人一起玩，以了解他们的工作方式，但大多数都是相当直接的。 您还会注意到其中一个项目是IPAM插件的一部分。 我们不打算介绍这篇文章中的内容（我们稍后会发布！）但是现在只知道我们正在使用多个CNI插件来完成这项工作。

Ok – so now that we have our network definition, we want to run it.  However – at this point we’ve only defined characteristics of the bridge.  The point of CNI is to network containers so we need to tell the plugin about the container we want to work with as well.  These variables are passed to the plugin via environmental variables.  So our command might look like this…  好的 - 现在我们有了网络定义，我们想要运行它。 但是 - 此时我们只定义了桥梁的特征。 CNI的目的是网络容器，所以我们需要告诉插件我们想要使用的容器。 这些变量通过环境变量传递给插件。 所以我们的命令可能看起来像这样......

```
sudo CNI_COMMAND=ADD CNI_CONTAINERID=1234567890 CNI_NETNS=/var/run/netns/1234567890 CNI_IFNAME=eth12 CNI_PATH=`pwd` ./bridge <mybridge.conf
```

Let’s walk through this.  I think most of you are probably familiar with using environmental variables on systems by setting them at the shell or system level.  In addition to that, you can also pass them directly to a command.  When you do this, they will be used only by the executable you are calling and only during that execution.  So in this case, the following variables will be passed to the bridge executable…  让我们来看看这个。 我想大多数人可能都熟悉在系统上使用环境变量，方法是在shell或系统级别设置环境变量。 除此之外，您还可以将它们直接传递给命令。 执行此操作时，它们将仅由您正在调用的可执行文件使用，并且仅在执行期间使用。 所以在这种情况下，以下变量将传递给桥接可执行文件...

- **CNI_COMMAND=ADD** – We are telling CNI that we want to add a connection
- **CNI_CONTAINER=1234567890** – We’re telling CNI that the network namespace we want to work is called ‘1234567890’ (more on this below)
- **CNI_NETNS=/var/run/netns/1234567890** – The path to the namespace in question
- **CNI_IFNAME=eth12** – The name of the interface we wish to use on the container side of the connection
- **CNI_PATH=`pwd`** – We always need to tell CNI where the plugin executables live.  In this case, since we’re already in the ‘cni’ directory we just have the variable reference pwd (present working directory). You need the ticks around the command pwd for it to evaluate correctly. Formatting here seems to be removing them but they are in the command above correctly

Once the variables you wish to pass to the executable are defined, we then pick the plugin we want to use which in this case is bridge.  Lastly – we feed the network configuration file into the plugin using STDIN.  To do this just use the left facing bracket ‘<‘.  Before we run the command, we need to create the network namespace that the plugin is going to work with.  Tpically the container runtime would handle this but since we’re keeping things simple this first go around we’ll just create one ourselves…  一旦定义了您希望传递给可执行文件的变量，我们就会选择我们想要使用的插件，在这种情况下是桥接器。 最后 - 我们使用STDIN将网络配置文件提供给插件。 要做到这一点，只需使用左向支架'<'。 在运行命令之前，我们需要创建插件将要使用的网络命名空间。 通常情况下，容器运行时会处理这个问题但是由于我们保持简单，所以首先我们只是自己创建一个......

```
sudo ip netns add 1234567890
```

Once that’s created let’s run the plugin…

```
user@ubuntu-1:~/cni$ sudo CNI_COMMAND=ADD CNI_CONTAINERID=1234567890 CNI_NETNS=/var/run/netns/1234567890 CNI_IFNAME=eth12 CNI_PATH=`pwd` ./bridge <mybridge.conf
2017/02/17 09:46:01 Error retriving last reserved ip: Failed to retrieve last reserved ip: open /var/lib/cni/networks/mybridge/last_reserved_ip: no such file or directory
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
}user@ubuntu-1:~/cni$
```

Running the command returns a couple of things.  First – it returns an error since the IPAM driver can’t find the file it uses to store IP information locally.  If we ran this again for a different namespace, we wouldn’t get this error since the file is created the first time we run the plugin.  The second thing we get is a JSON return indicating the relevant IP configuration that was configured by the plugin.  In this case, the bridge itself should have received the IP address of 10.15.20.1/24 and the namespace interface would have received 10.15.20.2/24.  It also added the default route and the 1.1.1.1/32 route that we defined in the network configuration JSON.  So let’s look and see what it did…  运行该命令会返回一些内容。 首先 - 它返回一个错误，因为IPAM驱动程序找不到它用于在本地存储IP信息的文件。 如果我们再次为不同的命名空间运行它，我们就不会收到此错误，因为文件是在我们第一次运行插件时创建的。 我们得到的第二件事是JSON返回，指示插件配置的相关IP配置。 在这种情况下，网桥本身应该已经收到10.15.20.1/24的IP地址，并且命名空间接口将收到10.15.20.2/24。 它还添加了我们在网络配置JSON中定义的默认路由和1.1.1.1/32路由。 那么让我们来看看它做了什么......

```
user@ubuntu-1:~/cni$ ifconfig
cni_bridge0 Link encap:Ethernet  HWaddr 0a:58:0a:0f:14:01
          inet addr:10.15.20.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::3cd5:6cff:fef9:9066/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:536 (536.0 B)  TX bytes:648 (648.0 B)

ens32     Link encap:Ethernet  HWaddr 00:0c:29:3e:49:51
          inet addr:10.20.30.71  Bcast:10.20.30.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe3e:4951/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:17431176 errors:0 dropped:1240 overruns:0 frame:0
          TX packets:14162993 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:2566654572 (2.5 GB)  TX bytes:9257712049 (9.2 GB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:45887226 errors:0 dropped:0 overruns:0 frame:0
          TX packets:45887226 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:21016155576 (21.0 GB)  TX bytes:21016155576 (21.0 GB)

veth1fbfe91d Link encap:Ethernet  HWaddr 26:68:37:93:26:4a
          inet6 addr: fe80::2468:37ff:fe93:264a/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:8 errors:0 dropped:0 overruns:0 frame:0
          TX packets:16 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:648 (648.0 B)  TX bytes:1296 (1.2 KB)

user@ubuntu-1:~/cni$
```

Notice we now have a bridge interface called ‘cni_bridge0’ which has the IP interface we expected to see.  Also note at the bottom we have one side of a veth pair.  Recall that we also asked it to enable masquerading.  If we look at our hosts iptables rules we’ll see the masquerade and accept rule…  请注意，我们现在有一个名为“cni_bridge0”的桥接接口，它具有我们希望看到的IP接口。 另请注意，在底部我们有一个veth对的一侧。 回想一下，我们还要求它启用伪装。 如果我们看看我们的主机iptables规则，我们会看到伪装和接受规则......

```
user@ubuntu-1:~/cni$ sudo iptables-save | grep mybridge
-A POSTROUTING -s 10.15.20.0/24 -m comment --comment "name: \"mybridge\" id: \"1234567890\"" -j CNI-26633426ea992aa1f0477097
-A CNI-26633426ea992aa1f0477097 -d 10.15.20.0/24 -m comment --comment "name: \"mybridge\" id: \"1234567890\"" -j ACCEPT
-A CNI-26633426ea992aa1f0477097 ! -d 224.0.0.0/4 -m comment --comment "name: \"mybridge\" id: \"1234567890\"" -j MASQUERADE
user@ubuntu-1:~/cni$
```

Let’s now look in the network namespace…

```
user@ubuntu-1:~/cni$ sudo ip netns exec 1234567890 ifconfig
eth12     Link encap:Ethernet  HWaddr 0a:58:0a:0f:14:02
          inet addr:10.15.20.2  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::d861:8ff:fe46:33ac/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:16 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1296 (1.2 KB)  TX bytes:648 (648.0 B)

user@ubuntu-1:~/cni$ sudo ip netns exec 1234567890 ip route
default via 10.15.20.1 dev eth12
1.1.1.1 via 10.15.20.1 dev eth12
10.15.20.0/24 dev eth12  proto kernel  scope link  src 10.15.20.2
user@ubuntu-1:~/cni$
```

Our namespace is also configured as we expected.  The namespace has an interface named ‘eth12’ with an IP address of 10.15.20.2/24 and the routes we defined are also there.  So it worked!  

This was a simple example but I think it highlights how CNI is implemented and works.  Next week we’ll dig further into the CNI plugins as we examine an example of how to use CNI with a container runtime.  这是一个简单的例子，但我认为它突出了CNI是如何实现和运作的。 下周我们将深入研究CNI插件，我们将研究如何将CNI与容器运行时一起使用的示例。

Before I wrap up – I do want to comment briefly on one item that I initially got hung up on and that’s how the plugin is actually called.  In our example – we’re calling a specific plugin directly.  As such – I was initially confused as to why you needed to specify the location of the plugins with the ‘CNI_PATH’.  After all – we’re calling a plugin directly so obviously we already know where it is.  The reason for this is that this is not how CNI is typically used.  Typically – you have a another application or system that is reading the CNI network definitions and running them.  In those cases, the CNI_PATH will already be defined within the system.  Since the network configuration file defines what plugin to use (in our case bridge) all the system would need to know is where to find the plugins.  To find them, it references the CNI_PATH variable.  We’ll talk more about this in future posts where we discuss what other applications use CNI (cough, Kubernetes, cough) so for now just know that the example above shows how CNI works, but does not show a typical use case outside of testing.  在我结束之前 - 我想简要评论一下我最初挂起的一个项目，这就是插件实际调用的方式。在我们的示例中 - 我们直接调用特定的插件。因此 - 我最初对于为什么需要使用'CNI_PATH'指定插件的位置感到困惑。毕竟 - 我们直接调用一个插件，所以显然我们已经知道它在哪里。原因是这不是CNI通常使用的方式。通常 - 您有另一个应用程序或系统正在读取CNI网络定义并运行它们。在这些情况下，CNI_PATH将已在系统中定义。由于网络配置文件定义了要使用的插件（在我们的案例中是桥接器），因此所有系统都需要知道在哪里找到插件。要查找它们，它会引用CNI_PATH变量。我们将在未来的帖子中详细讨论这个问题，我们将讨论其他应用程序使用CNI（咳嗽，Kubernetes，咳嗽）的问题，所以现在只知道上面的例子显示了CNI如何工作，但没有显示测试之外的典型用例。

[来源](https://www.dasblinkenlichten.com/understanding-cni-container-networking-interface/)

