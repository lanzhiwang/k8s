### 需求

有2个相互隔离的网络，拓扑见下图。ServerA想直接访问到ServerB连接的私有网络

```
                                                  |
            1.1.1.1               2.2.2.2         |
            +---------+  Public   +---------+     | Private
            | ServerA +-----------+ ServerB +-----+
            +---------+  Network  +---------+     | Network
                                                  |
                                                  | 192.168.1.0/24 
```

### 实现

通过ip tunnel建立ipip隧道，再通过iptables进行nat，便可以实现。

#### Step 1. 建立ip隧道

ServerA配置iptunnel,并给tunnel接口配置上ip

```bash
ip tunnel add a2b mode ipip remote 2.2.2.2 local 1.1.1.1
ifconfig a2b 192.168.2.1 netmask 255.255.255.0
```

ServerB配置iptunnel,并给tunnel接口配置上ip

```bash
ip tunnel add a2b mode ipip remote 1.1.1.1 local 2.2.2.2
ifconfig a2b 192.168.2.2 netmask 255.255.255.0
```

隧道配置完成后，请在ServerA上192.168.2.2，看是否可以ping通，ping通则继续，ping不通需要再看一下上面的命令执行是否有报错

#### Step 2. 添加路由和nat

ServerA上，添加到192.168.1.0/24的路由

```bash
/sbin/route add -net 192.168.1.0/24 gw 192.168.2.2
```

ServerB上，添加iptables nat，将ServerA过了访问192.168.1.0/24段的包进行NAT，并开启ip foward功能

```bash
iptables -t nat -A POSTROUTING -s 192.168.2.1 -d 192.168.1.0/24 -j MASQUERADE
sysctl -w net.ipv4.ip_forward=1
sed -i '/net.ipv4.ip_forward/ s/0/1/'  /etc/sysctl.conf
```

至此，完成了两端的配置，ServerA可以直接访问ServerB 所接的私网了。
