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
