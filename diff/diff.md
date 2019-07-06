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

## 示例

### 在主机上获取相关信息

```python

########### platform 模块获取 Linux 版本相关信息 ###########

>>> import platform

# 获取操作系统及版本信息
>>> platform.platform()
'Linux-3.10.0-862.11.6.el7.x86_64-x86_64-with-centos-7.5.1804-Core'

# 获取系统版本号
>>> platform.version()
'#1 SMP Tue Aug 14 21:49:04 UTC 2018'

# 获取系统名称
>>> platform.system()
'Linux'

# 系统位数(例如：32Bit, 64bit)
>>> platform.architecture()
('64bit', 'ELF')

# 计算机类型，例如：x86, AMD64
>>> platform.machine()
'x86_64'

# 计算机名称
>>> platform.node()
'localhost.localdomain'

# 处理器类型
>>> platform.processor()
'x86_64'

# 以上所有信息
>>> platform.uname()
('Linux', 'localhost.localdomain', '3.10.0-862.11.6.el7.x86_64', '#1 SMP Tue Aug 14 21:49:04 UTC 2018', 'x86_64', 'x86_64')


########### psutil 模块 ###########
CPU
Memory、swap_memory
Disks
Network
Sensors
Other system info（boot_time、users）
Processes

psutil可以获取网络接口 ifconfig 和网络连接信息 netstat

进程信息
>>> psutil.pids() # 所有进程ID
[3865, 3864, 3863, 3856, 3855, 3853, 3776, ..., 45, 44, 1, 0]
>>> p = psutil.Process(3776) # 获取指定进程ID=3776，其实就是当前Python交互环境
>>> p.name() # 进程名称
'python3.6'
>>> p.exe() # 进程exe路径
'/Users/michael/anaconda3/bin/python3.6'
>>> p.cwd() # 进程工作目录
'/Users/michael'
>>> p.cmdline() # 进程启动的命令行
['python3']
>>> p.ppid() # 父进程ID
3765
>>> p.parent() # 父进程
<psutil.Process(pid=3765, name='bash') at 4503144040>
>>> p.children() # 子进程列表
[]
>>> p.status() # 进程状态
'running'
>>> p.username() # 进程用户名
'michael'
>>> p.create_time() # 进程创建时间
1511052731.120333
>>> p.terminal() # 进程终端
'/dev/ttys002'
>>> p.cpu_times() # 进程使用的CPU时间
pcputimes(user=0.081150144, system=0.053269812, children_user=0.0, children_system=0.0)
>>> p.memory_info() # 进程使用的内存
pmem(rss=8310784, vms=2481725440, pfaults=3207, pageins=18)
>>> p.open_files() # 进程打开的文件
[]
>>> p.connections() # 进程相关网络连接
[]
>>> p.num_threads() # 进程的线程数量
1
>>> p.threads() # 所有线程信息
[pthread(id=1, user_time=0.090318, system_time=0.062736)]
>>> p.environ() # 进程环境变量
{'SHELL': '/bin/bash', 'PATH': '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:...', 'PWD': '/Users/michael', 'LANG': 'zh_CN.UTF-8', ...}
>>> p.terminate() # 结束进程
Terminated: 15 <-- 自己把自己结束了





########### paramiko 模块判断 ssh 连接信息 ###########

########### 判断软件是否安装 ###########

因为 linux 安装软件的方式比较多，所以没有一个通用的办法能查到某些软件是否安装了。总结起来就是这样几类：

1、rpm 包安装的，可以用 rpm -qa 看到，如果要查找某软件包是否安装，用 rpm -qa | grep “软件或者包的名字”
[root@hexuweb102 ~] rpm -qa | grep ruby

2、以 deb 包安装的，可以用 dpkg -l 能看到。如果是查找指定软件包，用dpkg -l | grep “软件或者包的名字”
[root@hexuweb102~] dpkg-l | grepruby

3、yum 方法安装的，可以用 yum list installed 查找，如果是查找指定包，命令后加 | grep “软件名或者包名”
[root@hexuweb102 ~] yum list installed | grep ruby

4、如果是以源码包自己编译安装的，例如.tar.gz或者tar.bz2形式的，这个只能看可执行文件是否存在了

########### 获取环境变量 ###########
import os
os.getenv('ENV_PORT')




# Linux 操作系统平台和版本
>>> import delegator
>>> c = delegator.run('cat /etc/os-release')
>>> c.out
'NAME="CentOS Linux"\nVERSION="7 (Core)"\nID="centos"\nID_LIKE="rhel fedora"\nVERSION_ID="7"\nPRETTY_NAME="CentOS Linux 7 (Core)"\nANSI_COLOR="0;31"\nCPE_NAME="cpe:/o:centos:centos:7"\nHOME_URL="https://www.centos.org/"\nBUG_REPORT_URL="https://bugs.centos.org/"\n\nCENTOS_MANTISBT_PROJECT="CentOS-7"\nCENTOS_MANTISBT_PROJECT_VERSION="7"\nREDHAT_SUPPORT_PRODUCT="centos"\nREDHAT_SUPPORT_PRODUCT_VERSION="7"\n\n'
>>> 
>>> c = delegator.run('uname -r')
>>> c.out
'3.10.0-862.11.6.el7.x86_64\n'
>>> 

# CPU逻辑核数和架构
>>> c = delegator.run('lscpu')
>>> c.out
'Architecture:          x86_64\nCPU op-mode(s):        32-bit, 64-bit\nByte Order:            Little Endian\nCPU(s):                4\nOn-line CPU(s) list:   0-3\nThread(s) per core:    1\nCore(s) per socket:    4\nSocket(s):             1\nNUMA node(s):          1\nVendor ID:             GenuineIntel\nCPU family:            6\nModel:                 85\nModel name:            Intel(R) Xeon(R) Gold 6132 CPU @ 2.60GHz\nStepping:              4\nCPU MHz:               2593.909\nBogoMIPS:              5187.81\nHypervisor vendor:     Microsoft\nVirtualization type:   full\nL1d cache:             32K\nL1i cache:             32K\nL2 cache:              1024K\nL3 cache:              19712K\nNUMA node0 CPU(s):     0-3\nFlags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology eagerfpu pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ibrs ibpb stibp fsgsbase bmi1 hle avx2 smep bmi2 erms invpcid rtm mpx avx512f avx512dq rdseed adx smap clflushopt avx512cd avx512bw avx512vl xsaveopt xsavec spec_ctrl intel_stibp\n'
>>> 

# 使用 psutil 模块获取内存信息
>>> import psutil
>>> mem = psutil.virtual_memory()
>>> mem.total
16252796928
>>> mem.available 
2476765184
>>> 

# 获取主机上是否已经运行了 mysql 服务，是否有 mysqld 进程
>>> import delegator
>>> c = delegator.run('ps -ef').pipe('grep -v grep').pipe('grep mysqld')
>>> c.out
u'27       23880 23861  0 Jun17 ?        00:26:59 mysqld\n'
>>> 

# 判断 3306 端口是否被占用，端口存在不会抛出异常，端口不存在会抛出异常
>>> import socket
>>> s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
>>> s.connect(('127.0.0.1', 3306))
>>> s.close()
>>> 

>>> import socket
>>> s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
>>> s.connect(('127.0.0.1', 3306))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib64/python2.7/socket.py", line 224, in meth
    return getattr(self._sock,name)(*args)
socket.error: [Errno 111] Connection refused
>>> s.close()
>>> 

# 检查软件安装方式，例如是直接编译mysql到/usr/local/mysql，还是使用包管理的安装方式
# 当然存在编译之后再次做成服务的方式

# 使用命令行查看 mysqls.service 服务是否存在，存在初步可以判断为包安装方式，不存在初步判断为编译安装方式
>>> import delegator
>>> 
>>> c = delegator.run('systemctl status mysqld.service')
>>> c.out
''
>>> c.err
'Unit mysqld.service could not be found.\n'
>>> 

```

### 汇总信息，比较信息

```python
# 我比较熟悉 flask 框架，简单驱动盖框架，调用相关接口返回主机信息

from flask import Flask

import psutil

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getCPUInfo')
def get_cpu_info():
    cpu_count = psutil.cpu_count(logical=True)
    return 'cpu_count: %d' % cpu_count

if __name__ == '__main__':
    app.run(port=8888)


[root@localhost ~]# curl http://localhost:8888
Hello World!
[root@localhost ~]# 
[root@localhost ~]# curl http://localhost:8888/getCPUInfo
cpu_count: 4
[root@localhost ~]# 

# 后续统一接口参数，可以在一个接口中返回所有的信息，也可以单独请求一个主机信息
# 统一返回信息


```
