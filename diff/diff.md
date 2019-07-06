## 相关服务器需要检查的项目

* Linux 操作系统平台和版本
* CPU逻辑核数和架构
* 可用内存
* 磁盘类型、容量和挂载参数
* 网卡配置
* 网络端口
* 网络连接互联网
* Python 版本
* 是否有相关用户以及用户是否有相关权限
* 机器之间是否可用密钥登录
* 相关工具是否安装
* 已安装工具版本是否符合要求
* 安装方式是否符合要求（本质就是目录文件结构是否符合要求）
* 是否有相关服务，服务版本是否符合要求

## 思路

1. 在主机上获取相关信息
	* Python + 第三方模块（例如 psutil）获取主机信息
	* 如果没有合适的第三方模块直接利用 subprocess 模块执行相关命令

2. 汇总信息，比较信息
	* 在需要获取配置信息的机器上简单安装一个代理服务，简单的 flask，调用相关获取配置信息的方法统一返回信息
	* 利用现有的 ansible 模块或者自定义模块，类似于 setup 模块

## 示例(为显示只做部分输出)

```bash
pip install -r requirements,txt
python diff.py > diff.log


------------ 获取系统基本信息 ------------
{'node': 'localhost.localdomain', 'linux_distribution': ('CentOS Linux', '7.5.1804', 'Core'), 'uname': ('Linux', 'localhost.localdomain', '3.10.0-862.11.6.el7.x86_64', '#1 SMP Tue Aug 14 21:49:04 UTC 2018', 'x86_64', 'x86_64'), 'system': 'Linux', 'machine': 'x86_64', 'platform': 'Linux-3.10.0-862.11.6.el7.x86_64-x86_64-with-centos-7.5.1804-Core', 'version': '#1 SMP Tue Aug 14 21:49:04 UTC 2018', 'architecture': ('64bit', 'ELF'), 'processor': 'x86_64'}



------------ 获取系统的所有进程信息 ------------
{'status': 'sleeping', 'username': 'root', 'exe': '/usr/bin/docker-containerd-shim', 'cpu_times': pcputimes(user=35.0, system=16.34, children_user=0.04, children_system=0.07), 'name': 'docker-containerd-shim', 'parent': psutil.Process(pid=1181, name='docker-containerd', started='2019-05-31 03:39:35'), 'num_threads': 10, 'connections': [], 'children': [psutil.Process(pid=65434, name='nginx', started='2019-05-31 07:41:46')], 'terminal': None, 'cmdline': ['docker-containerd-shim', '-namespace', 'moby', '-workdir', '/data/docker/workspace/containerd/daemon/io.containerd.runtime.v1.linux/moby/8e785e03889e0e4f06b0414b841712507c109a6b35b8c5f792c086071a315424', '-address', '/var/run/docker/containerd/docker-containerd.sock', '-containerd-binary', '/usr/bin/docker-containerd', '-runtime-root', '/var/run/docker/runtime-runc'], 'memory_info': pmem(rss=2105344, vms=7667712, shared=1552384, text=2150400, lib=0, data=3493888, dirty=0), 'create_time': 1559288506.8, 'threads': [pthread(id=1639, user_time=9.78, system_time=3.08), pthread(id=65415, user_time=0.0, system_time=0.0), pthread(id=65416, user_time=0.57, system_time=2.67), pthread(id=65417, user_time=0.0, system_time=0.0), pthread(id=65418, user_time=0.0, system_time=0.01), pthread(id=65419, user_time=9.22, system_time=3.13), pthread(id=65420, user_time=1.7, system_time=0.72), pthread(id=65421, user_time=0.0, system_time=0.0), pthread(id=65422, user_time=6.08, system_time=2.17), pthread(id=65423, user_time=9.16, system_time=2.99)], 'environ': {'LANG': 'en_US.UTF-8', 'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin'}, 'open_files': [], 'ppid': 1181, 'cwd': '/run/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/8e785e03889e0e4f06b0414b841712507c109a6b35b8c5f792c086071a315424'}
{'status': 'sleeping', 'username': 'root', 'exe': '/usr/sbin/nginx', 'cpu_times': pcputimes(user=0.0, system=0.01, children_user=0.0, children_system=0.0), 'name': 'nginx', 'parent': psutil.Process(pid=65415, name='docker-containerd-shim', started='2019-05-31 07:41:46'), 'num_threads': 1, 'connections': [], 'children': [psutil.Process(pid=65472, name='nginx', started='2019-05-31 07:41:47')], 'terminal': '/dev/pts/0', 'cmdline': ['nginx:', 'master', 'process', 'nginx', '-g', 'daemon', 'off;'], 'memory_info': pmem(rss=1118208, vms=33398784, shared=290816, text=1175552, lib=0, data=987136, dirty=0), 'create_time': 1559288506.83, 'threads': [pthread(id=65434, user_time=0.0, system_time=0.01)], 'environ': {}, 'open_files': [], 'ppid': 65415, 'cwd': '/'}
{'status': 'sleeping', 'username': '101', 'exe': '/usr/sbin/nginx', 'cpu_times': pcputimes(user=0.09, system=0.38, children_user=0.0, children_system=0.0), 'name': 'nginx', 'parent': psutil.Process(pid=65434, name='nginx', started='2019-05-31 07:41:46'), 'num_threads': 1, 'connections': [], 'children': [], 'terminal': '/dev/pts/0', 'cmdline': ['nginx:', 'worker', 'process'], 'memory_info': pmem(rss=1597440, vms=33861632, shared=311296, text=1175552, lib=0, data=1445888, dirty=0), 'create_time': 1559288507.0, 'threads': [pthread(id=65472, user_time=0.09, system_time=0.38)], 'environ': {}, 'open_files': [], 'ppid': 65434, 'cwd': '/'}



------------ 获取所有加载的模块 ------------
['iptable_security', 'iptable_raw', 'iptable_mangle', 'tcp_diag', 'inet_diag', 'cfg80211', 'rfkill', 'veth', 'xt_nat', 'ipt_MASQUERADE', 'nf_nat_masquerade_ipv4', 'nf_conntrack_netlink', 'nfnetlink', 'iptable_nat', 'nf_conntrack_ipv4', 'nf_defrag_ipv4', 'nf_nat_ipv4', 'xt_addrtype', 'xt_conntrack', 'nf_nat', 'br_netfilter', 'bridge', 'stp', 'llc', 'binfmt_misc', 'ip6table_filter', 'ip6_tables', 'iptable_filter', 'nf_conntrack_ftp', 'nf_conntrack', 'overlay', 'ext4', 'mbcache', 'jbd2', 'iosf_mbi', 'crc32_pclmul', 'joydev', 'ghash_clmulni_intel', 'hv_utils', 'ptp', 'aesni_intel', 'sg', 'pps_core', 'i2c_piix4', 'lrw', 'gf128mul', 'hv_balloon', 'glue_helper', 'i2c_core', 'ablk_helper', 'pcspkr', 'cryptd', 'ip_tables', 'xfs', 'libcrc32c', 'sr_mod', 'sd_mod', 'cdrom', 'crc_t10dif', 'crct10dif_generic', 'ata_generic', 'pata_acpi', 'hv_storvsc', 'hv_netvsc', 'scsi_transport_fc', 'scsi_tgt', 'hid_hyperv', 'hyperv_keyboard', 'ata_piix', 'libata', 'crct10dif_pclmul', 'crct10dif_common', 'crc32c_intel', 'serio_raw', 'hyperv_fb', 'hv_vmbus', 'floppy', 'dm_mirror', 'dm_region_hash', 'dm_log', 'dm_mod']



------------ 获取某一模块的信息(以 veth 模块为例) ------------
{'sig_key': 'D4:11:5F:11:00:55:DB:56:C8:D6:05:AB:75:21:73:CF:B1:AC:54:D8', 'rhelversion': '7.5', 'description': 'Virtual Ethernet Tunnel', 'license': 'GPL v2', 'filename': '/lib/modules/3.10.0-862.11.6.el7.x86_64/kernel/drivers/net/veth.ko.xz', 'alias': 'rtnl-link-veth', 'depends': '', 'srcversion': '4DFC082347BBDCFF4B4B80A', 'retpoline': 'Y', 'intree': 'Y', 'signer': 'CentOS Linux kernel signing key', 'sig_hashalgo': 'sha256', 'vermagic': '3.10.0-862.11.6.el7.x86_64 SMP mod_unload modversions'}



------------ 获取 iptable 信息 ------------
{
'filter': {},
'raw': {u'OUTPUT': [], u'PREROUTING': []}, 
'security': {u'FORWARD': [], u'INPUT': [], u'OUTPUT': []}, 
'mangle': {u'FORWARD': [], u'INPUT': [], u'POSTROUTING': [], u'PREROUTING': [], u'OUTPUT': []}, 
'nat': {}
}



------------ 获取网络接口信息 ------------
{'veth96766e5': [snicaddr(family=10, address='fe80::c4ea:4bff:fea0:f278%veth96766e5', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='c6:ea:4b:a0:f2:78', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth3d41e9b': [snicaddr(family=10, address='fe80::80b2:9bff:fed8:5e13%veth3d41e9b', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='82:b2:9b:d8:5e:13', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'docker0': [snicaddr(family=2, address='172.17.0.1', netmask='255.255.0.0', broadcast='172.17.255.255', ptp=None), snicaddr(family=10, address='fe80::42:7ff:feea:a39%docker0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='02:42:07:ea:0a:39', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth164480d': [snicaddr(family=10, address='fe80::21:94ff:fec8:ab5e%veth164480d', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='02:21:94:c8:ab:5e', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth627209f': [snicaddr(family=10, address='fe80::d4c5:e6ff:fe5e:9905%veth627209f', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='d6:c5:e6:5e:99:05', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth7477cc1': [snicaddr(family=10, address='fe80::e86f:37ff:fefc:c397%veth7477cc1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='ea:6f:37:fc:c3:97', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'vetha87b633': [snicaddr(family=10, address='fe80::b836:e5ff:fee9:244d%vetha87b633', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='ba:36:e5:e9:24:4d', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth2a3f8de': [snicaddr(family=10, address='fe80::38fb:67ff:fe18:377%veth2a3f8de', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='3a:fb:67:18:03:77', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth7da9c62': [snicaddr(family=10, address='fe80::6c95:41ff:feaf:2101%veth7da9c62', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='6e:95:41:af:21:01', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth8f5dedf': [snicaddr(family=10, address='fe80::f092:c0ff:fe40:b463%veth8f5dedf', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='f2:92:c0:40:b4:63', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'br-25ec3c1c0206': [snicaddr(family=2, address='172.19.0.1', netmask='255.255.0.0', broadcast='172.19.255.255', ptp=None), snicaddr(family=17, address='02:42:04:2b:9e:ed', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth759c39d': [snicaddr(family=10, address='fe80::644b:39ff:fe6d:1969%veth759c39d', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='66:4b:39:6d:19:69', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'eth0': [snicaddr(family=2, address='10.5.10.118', netmask='255.255.255.0', broadcast='10.5.10.255', ptp=None), snicaddr(family=10, address='fe80::215:5dff:fe0a:1c2a%eth0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='00:15:5d:0a:1c:2a', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'br-7fbed4772293': [snicaddr(family=2, address='172.23.0.1', netmask='255.255.0.0', broadcast='172.23.255.255', ptp=None), snicaddr(family=10, address='fe80::42:72ff:fe1d:aa27%br-7fbed4772293', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='02:42:72:1d:aa:27', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'vethe2e1c6d': [snicaddr(family=10, address='fe80::784a:afff:fe26:748e%vethe2e1c6d', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='7a:4a:af:26:74:8e', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'vetheb254a5': [snicaddr(family=10, address='fe80::a00d:d7ff:fea3:66%vetheb254a5', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='a2:0d:d7:a3:00:66', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'lo': [snicaddr(family=2, address='127.0.0.1', netmask='255.0.0.0', broadcast=None, ptp=None), snicaddr(family=10, address='::1', netmask='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', broadcast=None, ptp=None), snicaddr(family=17, address='00:00:00:00:00:00', netmask=None, broadcast=None, ptp=None)], 'br-9421749825c5': [snicaddr(family=2, address='172.20.0.1', netmask='255.255.0.0', broadcast='172.20.255.255', ptp=None), snicaddr(family=17, address='02:42:29:53:cd:46', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth113b4fe': [snicaddr(family=10, address='fe80::44ae:14ff:fe4e:62c3%veth113b4fe', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='46:ae:14:4e:62:c3', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'vethc1936d8': [snicaddr(family=10, address='fe80::d001:eff:fe0b:d27a%vethc1936d8', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='d2:01:0e:0b:d2:7a', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'br-7984fc49a9d2': [snicaddr(family=2, address='172.18.0.1', netmask='255.255.0.0', broadcast='172.18.255.255', ptp=None), snicaddr(family=17, address='02:42:06:30:96:b3', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'veth19ed909': [snicaddr(family=10, address='fe80::50da:64ff:fe2b:786e%veth19ed909', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='52:da:64:2b:78:6e', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'vethab1b7fa': [snicaddr(family=10, address='fe80::a0dc:5bff:fef3:b17e%vethab1b7fa', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='a2:dc:5b:f3:b1:7e', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)], 'br-c316ebcc673c': [snicaddr(family=2, address='172.16.238.1', netmask='255.255.255.0', broadcast='172.16.238.255', ptp=None), snicaddr(family=10, address='fe80::42:7cff:fed7:bd4d%br-c316ebcc673c', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None), snicaddr(family=17, address='02:42:7c:d7:bd:4d', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)]}



------------ 获取系统的所有网络连接信息 ------------
sconn(fd=3, family=2, type=1, laddr=addr(ip='0.0.0.0', port=22), raddr=(), status='LISTEN', pid=899)
sconn(fd=4, family=10, type=1, laddr=addr(ip='::', port=33060), raddr=(), status='LISTEN', pid=23840)
sconn(fd=4, family=10, type=1, laddr=addr(ip='::', port=18081), raddr=(), status='LISTEN', pid=3318)
sconn(fd=4, family=10, type=1, laddr=addr(ip='::', port=7083), raddr=(), status='LISTEN', pid=4675)
sconn(fd=4, family=10, type=1, laddr=addr(ip='::', port=1783), raddr=(), status='LISTEN', pid=4692)
sconn(fd=13, family=2, type=1, laddr=addr(ip='0.0.0.0', port=8087), raddr=(), status='LISTEN', pid=38931)
sconn(fd=4, family=10, type=1, laddr=addr(ip='::', port=7880), raddr=(), status='LISTEN', pid=4662)
sconn(fd=4, family=10, type=1, laddr=addr(ip='::', port=7087), raddr=(), status='LISTEN', pid=3267)



------------ 获取系统的所有被占用的端口 ------------
[22, 33060, 18081, 7083, 80, 8443, 1786, 8012, 8091, 8097, 40010, 38838, 8868, 8090, 80, 80, 7882, 7883, 1873, 8060, 22, 8096, 8083, 1883, 8081, 7085, 8070, 1787, 1784, 1863, 8880, 8022, 5000, 22, 25, 3883, 8066, 25, 7084, 9443, 9022, 3306, 18082, 7881, 22, 18083, 9000, 9012, 32784, 8878, 22, 7086, 1785, 2883, 7884, 1783, 8087, 7880, 7087]



------------ 获取 CPU 信息 ------------
{'logical': 4, 'physical': 4}



------------ 获取 memory 信息 ------------
{'virtual_memory': svmem(total=16252796928, available=2476195840, percent=84.8, used=13230264320, free=219246592, active=9982287872, inactive=4670234624, buffers=132702208, cached=2670583808, shared=205213696, slab=1014296576), 'swap_memory': sswap(total=5368705024, used=1279524864, free=4089180160, percent=23.8, sin=484745216, sout=1587122176)}



------------ 获取 disk 信息 ------------
{'disk_partitions': [sdiskpart(device='/dev/mapper/centos-root', mountpoint='/', fstype='xfs', opts='rw,relatime,attr2,inode64,noquota'), sdiskpart(device='/dev/sda1', mountpoint='/boot', fstype='xfs', opts='rw,relatime,attr2,inode64,noquota'), sdiskpart(device='/dev/sdb1', mountpoint='/data', fstype='ext4', opts='rw,relatime,data=ordered')], 'disk_usage': {'/boot': sdiskusage(total=517713920, used=171859968, free=345853952, percent=33.2), '/data': sdiskusage(total=528309551104, used=29487542272, free=471961739264, percent=5.9), '/': sdiskusage(total=47724642304, used=13445124096, free=34279518208, percent=28.2)}, 'disk_io_counters': sdiskio(read_count=2222435, write_count=36628234, read_bytes=82571729408, write_bytes=547495456768, read_time=34250869, write_time=28811009, read_merged_count=100617, write_merged_count=43694265, busy_time=23678954)}



------------ 获取系统登录用户信息 ------------
[suser(name='root', terminal='pts/0', host='10.5.106.84', started=1562292736.0, pid=26014), suser(name='root', terminal='pts/1', host='10.5.113.86', started=1562429824.0, pid=24528)]



------------ 获取系统的所有用户信息 ------------
[linuxUser(name='root', password='x', uid='0', gid='0', group='root', home='/root', shell='/bin/bash'), linuxUser(name='bin', password='x', uid='1', gid='1', group='bin', home='/bin', shell='/sbin/nologin'), linuxUser(name='daemon', password='x', uid='2', gid='2', group='daemon', home='/sbin', shell='/sbin/nologin'), linuxUser(name='adm', password='x', uid='3', gid='4', group='adm', home='/var/adm', shell='/sbin/nologin'), linuxUser(name='lp', password='x', uid='4', gid='7', group='lp', home='/var/spool/lpd', shell='/sbin/nologin'), linuxUser(name='sync', password='x', uid='5', gid='0', group='sync', home='/sbin', shell='/bin/sync'), linuxUser(name='shutdown', password='x', uid='6', gid='0', group='shutdown', home='/sbin', shell='/sbin/shutdown'), linuxUser(name='halt', password='x', uid='7', gid='0', group='halt', home='/sbin', shell='/sbin/halt'), linuxUser(name='mail', password='x', uid='8', gid='12', group='mail', home='/var/spool/mail', shell='/sbin/nologin'), linuxUser(name='operator', password='x', uid='11', gid='0', group='operator', home='/root', shell='/sbin/nologin'), linuxUser(name='games', password='x', uid='12', gid='100', group='games', home='/usr/games', shell='/sbin/nologin'), linuxUser(name='ftp', password='x', uid='14', gid='50', group='FTP User', home='/var/ftp', shell='/sbin/nologin'), linuxUser(name='nobody', password='x', uid='99', gid='99', group='Nobody', home='/', shell='/sbin/nologin'), linuxUser(name='avahi-autoipd', password='x', uid='170', gid='170', group='Avahi IPv4LL Stack', home='/var/lib/avahi-autoipd', shell='/sbin/nologin'), linuxUser(name='systemd-bus-proxy', password='x', uid='999', gid='997', group='systemd Bus Proxy', home='/', shell='/sbin/nologin'), linuxUser(name='systemd-network', password='x', uid='998', gid='996', group='systemd Network Management', home='/', shell='/sbin/nologin'), linuxUser(name='dbus', password='x', uid='81', gid='81', group='System message bus', home='/', shell='/sbin/nologin'), linuxUser(name='polkitd', password='x', uid='997', gid='995', group='User for polkitd', home='/', shell='/sbin/nologin'), linuxUser(name='tss', password='x', uid='59', gid='59', group='Account used by the trousers package to sandbox the tcsd daemon', home='/dev/null', shell='/sbin/nologin'), linuxUser(name='postfix', password='x', uid='89', gid='89', group='', home='/var/spool/postfix', shell='/sbin/nologin'), linuxUser(name='sshd', password='x', uid='74', gid='74', group='Privilege-separated SSH', home='/var/empty/sshd', shell='/sbin/nologin'), linuxUser(name='nginx', password='x', uid='996', gid='992', group='Nginx web server', home='/var/lib/nginx', shell='/sbin/nologin'), linuxUser(name='sonarqube', password='x', uid='995', gid='991', group='', home='/home/sonarqube', shell='/bin/bash')]



------------ 获取某一用户具体信息 ------------
pwd.struct_passwd(pw_name='root', pw_passwd='x', pw_uid=0, pw_gid=0, pw_gecos='root', pw_dir='/root', pw_shell='/bin/bash')



------------ 获取系统的所有环境变量或者某个环境变量 ------------
{'LESSOPEN': '||/usr/bin/lesspipe.sh %s', 'SSH_CLIENT': '10.5.113.86 23727 22', 'LOGNAME': 'root', 'USER': 'root', 'HOME': '/root', 'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin', 'LANG': 'en_US.UTF-8', 'TERM': 'xterm', 'SHELL': '/bin/bash', 'SHLVL': '1', 'HISTSIZE': '1000', 'XDG_RUNTIME_DIR': '/run/user/0', 'XDG_SESSION_ID': '53672', '_': '/usr/bin/python', 'SSH_CONNECTION': '10.5.113.86 23727 10.5.10.118 22', 'SSH_TTY': '/dev/pts/1', 'OLDPWD': '/root', 'HOSTNAME': 'localhost.localdomain', 'HISTCONTROL': 'ignoredups', 'PWD': '/root/work', 'MAIL': '/var/spool/mail/root', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:'}



------------ 获取某个路径下的所有可执行文件 ------------
/usr/local/bin/docker-compose
/usr/local/bin/docker-machine
/usr/local/bin/redis-server
/usr/local/bin/redis-benchmark
/usr/local/bin/redis-cli
/usr/local/bin/redis-check-rdb
/usr/bin/nl-class-list
/usr/bin/setmetamode
/usr/bin/flipdiff
/usr/bin/pip2.7
/usr/bin/grepdiff
/usr/bin/interdiff
/usr/bin/lsdiff
/usr/bin/easy_install
/usr/bin/merge
/usr/bin/rcsdiff
/usr/bin/gdk-pixbuf-query-loaders-64
/usr/bin/gdk-pixbuf-thumbnailer
/usr/bin/gtk-query-immodules-2.0-64
/usr/bin/easy_install-2.7



------------ 获取文件或者目录的权限信息 ------------
posix.stat_result(st_mode=16877, st_ino=204015482, st_dev=64768L, st_nlink=4, st_uid=0, st_gid=0, st_size=40, st_atime=1562405425, st_mtime=1560762596, st_ctime=1560762596)



------------ 判断用户对文件或者目录是否可读 ------------
True



------------ 判断用户对文件或者目录是否可写 ------------
True



------------ 判断用户对文件是否执行 ------------
True



------------ 获取系统的包管理工具 ------------
['/usr/bin/rpm', '/usr/bin/yum']



------------ 获取系统已经安装的软件列表 ------------
['pcre2-tools-10.23-2.el7.x86_64', 'NetworkManager-1.10.2-16.el7_5.x86_64', 'glib2-2.56.1-4.el7_6.x86_64', 'libxshmfence-1.2-1.el7.x86_64', 'mesa-libgbm-18.0.5-4.el7_6.x86_64'}



------------ 获取某种软件的具体信息 ------------
Name        : vim-enhanced
Epoch       : 2
Version     : 7.4.160
Release     : 4.el7
Architecture: x86_64
Install Date: Mon 27 Aug 2018 05:07:15 AM UTC
Group       : Applications/Editors
Size        : 2296714
License     : Vim
Signature   : RSA/SHA256, Wed 25 Apr 2018 11:50:34 AM UTC, Key ID 24c6a8a7f4a80eb5
Source RPM  : vim-7.4.160-4.el7.src.rpm
Build Date  : Tue 10 Apr 2018 11:55:09 PM UTC
Build Host  : x86-01.bsys.centos.org
Relocations : (not relocatable)
Packager    : CentOS BuildSystem <http://bugs.centos.org>
Vendor      : CentOS
URL         : http://www.vim.org/
Summary     : A version of the VIM editor which includes recent enhancements
Description :
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.



```