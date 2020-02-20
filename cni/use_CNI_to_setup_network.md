# [Understand Container 7: use CNI to setup network](https://pierrchen.blogspot.com/2018/06/understand-container-7-cni.html)

CNI means `Container Runtime Interface`, originated from coreOs for rkt's network solution, and beat Docker's CNM as being adopted by [k8s](https://kubernetes.io/blog/2016/01/why-kubernetes-doesnt-use-libnetwork/) as the network plugin interface.  CNI的意思是Container Runtime Interface，它源自rkt的网络解决方案的coreOs，并击败了k8s用作网络插件接口的Docker的CNM。

In this blog we are going to see how to use CNI, to be specific, the bridge plugin, to setup the network for containers spawned by runc and achieve the same result/topology as we did in the last blog using netns as the hook.  在此博客中，我们将了解如何使用CNI（具体而言，是网桥插件）为runc生成的容器设置网络，并获得与上一个博客中使用netn作为挂钩的结果/拓扑相同的结果/拓扑。

## Overview

The caller/user of CNI (eg: you calling from a shell, a container runtime/orchestrator, such as runc or k8s) interact with a plugin using two things: a network configuration file and some environment variables. The configuration files has the [configs of network (or subnet)](https://github.com/containernetworking/cni/blob/master/SPEC.md#network-configuration) the container supposed to connect to; the environment variables include the path regarding where to find the plugin binary and network configuration files, *plus* "add/delete which container to/from which network namespace", which can well be implemented by passing arguments to the plugin (instead of using environment variable). It's not a big issue but looks a little bit "unusual" to use environment to pass arguments.  CNI的调用者/用户（例如：您从外壳，容器运行时/协调器（例如runc或k8s）进行调用）与插件交互使用了两件事：网络配置文件和一些环境变量。 配置文件具有容器应该连接到的网络（或子网）的配置； 环境变量包括有关在哪里可以找到插件二进制文件和网络配置文件的路径，以及“向/从哪个网络名称空间添加/删除哪个容器”的方法，可以通过将参数传递给插件来实现（而不是使用环境变量） ）。 这不是一个大问题，但是使用环境来传递参数看起来有点“不寻常”。

For a more detailed introduction of CNI, see [here](https://www.slideshare.net/weaveworks/introduction-to-the-container-network-interface-cni) and [here](https://github.com/containernetworking/cni/blob/master/SPEC.md).

## Use CNI plugins

### build/install plugins

```
go get github.com/containernetworking/plugins
cd $GOPATH/src/github.com/containernetworking/plugins
./build.sh
mkdir -p /opt/cni/bin/bridge
sudo cp bin/* c
```

## Use CNI

We'll be using following simple (and dirty) script to exercise CNI with runc. It covers all the essential concepts in one place, which is nice.  我们将使用以下简单（肮脏的）脚本在runc上执行CNI。 它涵盖了所有基本概念，非常好。

```bash
$ cat runc_cni.sh
#!/bin/sh

# need run with root
# ADD or DEL or VERSION
action=$1 
cid=$2
pid=$(runc ps $cid | sed '1d' | awk '{print $2}')
plugin=/opt/cni/bin/bridge

export CNI_PATH=/opt/cni/bin/
export CNI_IFNAME=eth0
export CNI_COMMAND=$action
export CNI_CONTAINERID=$cid
export CNI_NETNS=/proc/$pid/ns/net

$plugin <<EOF
{
    "cniVersion": "0.2.0",
    "name": "mynet",
    "type": "bridge",
    "bridge": "cnibr0",             
    "isGateway": true,
    "ipMasq": true,
    "ipam": {
        "type": "host-local",
        "subnet": "172.19.1.0/24",
        "routes": [
            { "dst": "0.0.0.0/0" }
        ],
     "dataDir": "/run/ipam-state"
    },
    "dns": {
      "nameservers": [ "8.8.8.8" ]
    }
}
EOF
```

It may be not obvious to a newcomer that we are using two plugins here, [bridge plugin](https://github.com/containernetworking/plugins/tree/master/plugins/main/bridge) and [host-local](https://github.com/containernetworking/plugins/tree/master/plugins/ipam/host-local). The format is to set up a bridge network (as well as veth pair) and the late is to set up allocate and assign ip to the containers (and the bridge gateway), which is called `ipam` (IP Address Management), as you might have noticed in the config key.  对于新手来说，我们在这里使用两个插件（bridge plugin和host-local）可能并不明显。 格式是建立一个桥接网络（以及veth对），后期是设置为容器（和桥接网关）分配和分配ip，这可能称为ipam（IP地址管理）。 已经注意到在配置键。

The internal working of the bridge plugging is almost same as the `netns` does and we are not going to repeat it here.  桥接的内部工作几乎与netns相同，在此我们不再赘述。

Start a container called `c1`, `sudo runc run c1`.

Then, put `c1` into the network:

```
sudo ./runc_cni.sh ADD c1
```

Below is the output, telling you the *ip* and *gateway* of `c1`, among other things.

```
{
    "cniVersion": "0.2.0",
    "ip4": {
        "ip": "172.19.1.6/24",
        "gateway": "172.19.1.1",
        "routes": [
            {
                "dst": "0.0.0.0/0",
                "gw": "172.19.1.1"
            }
        ]
    },
    "dns": {
        "nameservers": [
            "8.8.8.8"
        ]
    }
}
```

You can create another container `c2` and put it into the same network in a similar way, and now we create a subnet with two containers inside. They can talk to the each other and call can ping outside IPs, thanks route setting and IP masquerade. However, the dns won't work.  您可以创建另一个容器“ c2”，并以类似的方式将其放入同一网络，现在我们创建一个内部有两个容器的子网。 由于路由设置和IP伪装，他们可以互相交谈，并且可以在IP外部ping通呼叫。 但是，DNS无法正常工作。

You can also remove a container from the network, after which the container won't be connected to the bridge anymore.

```
sudo ./runc_cni.sh DEL c1
```

However, the IP resource won't be reclaimed automatically, you have to do that "manually".  但是，IP资源不会自动回收，您必须“手动”进行。

That is it, as we said this will be a short ride. Have fun with CNI.  就是这样，正如我们所说的那样，这只是一小段路程。 享受CNI的乐趣。



