### Docker Registry

Docker Registry 相关内容：

* 使用 Docker Registry 的两种主要方式：
	* 通过容器方式运行
	* 通过本地安装运行并注册为系统服务

* 添加 Nginx 反向代理

* 添加用户认证功能

* Docker Registry 配置文件中各个选项的含义和使用

* 使用 Registry 的通知系统来支持更多应用场景

参考：
https://www.cnblogs.com/wade-luffy/p/6590849.html

https://docs.docker.com/registry/



```bash

# 指定配置文件
# 默认配置文件的位置是 /etc/docker/registry/config.yml
# 配置文件可以从已经运行的容器中拷贝出来
docker run -d -p 5000:5000 --restart=always --name registry \
             -v `pwd`/config.yml:/etc/docker/registry/config.yml \
             registry:2

# Registry 数据的默认的存储位置为 /var/lib/registry，可以通过 -v 参数来映射本地的路径到容器内。
-v /opt/data/registry:/var/lib/registry

# 配置 TLS 证书
# 生成过程中会提示填入各种信息，注意 CN 一栏的信息要填入跟访问的地址相同的域名，例如这里应该为 myrepo.com
# 生成结果为秘钥文件 domain.key，以及证书文件 domain.crt

# 其中证书文件需要发送给用户，并且配置到用户 Docker Host上，注意路径需要跟域名一致，例如：/etc/docker/certs.d/myrepo.com:443/domain.crt

$ docker run -d \
  --restart=always \
  --name registry \
  -v "$(pwd)"/certs:/certs \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -p 443:443 \
  registry:2


[root@lanzhiwang-centos7 ~]# docker pull registry
[root@lanzhiwang-centos7 ~]# docker images
registry                                latest              f32a97de94e1        3 months ago        25.8MB
[root@lanzhiwang-centos7 ~]# 


# 测试基础功能
[root@lanzhiwang-centos7 ~]# docker run -d -p 5000:5000 --name registry registry
159008c35cce37133de3023a3397dfd346ee2c46c8877fba97228361d02a8d54
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
159008c35cce        registry            "/entrypoint.sh /etc…"   6 seconds ago       Up 5 seconds        0.0.0.0:5000->5000/tcp   registry
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# docker pull ubuntu
[root@lanzhiwang-centos7 ~]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                                  latest              7698f282e524        3 weeks ago         69.9MB
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# docker image tag ubuntu localhost:5000/myfirstimage
[root@lanzhiwang-centos7 ~]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                                  latest              7698f282e524        3 weeks ago         69.9MB
localhost:5000/myfirstimage             latest              7698f282e524        3 weeks ago         69.9MB
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# docker push localhost:5000/myfirstimage
The push refers to repository [localhost:5000/myfirstimage]
8d267010480f: Pushed 
270f934787ed: Pushed 
02571d034293: Pushed 
latest: digest: sha256:b36667c98cf8f68d4b7f1fb8e01f742c2ed26b5f0c965a788e98dfe589a4b3e4 size: 943
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# 

# 启动基础容器拷贝配置文件
[root@lanzhiwang-centos7 ~]# docker cp 159008c35cce:/etc/docker/registry/config.yml ./
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# ls
config.yml
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# cat config.yml 
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
[root@lanzhiwang-centos7 ~]# 
# 基础的配置文件内容太少，需要使用官方配置文件或者使用更多的选项启动容器





# 测试 TLS 
# 生成 RSA private key
[root@lanzhiwang-centos7 certs]# openssl genrsa -aes128 -out domain.key 2048
Generating RSA private key, 2048 bit long modulus
......+++
...................................................................+++
e is 65537 (0x10001)
Enter pass phrase for domain.key: huzhi123456
Verifying - Enter pass phrase for domain.key:
[root@lanzhiwang-centos7 certs]# ll
total 4
-rw-r--r-- 1 root root 1766 Jun 12 18:28 domain.key
[root@lanzhiwang-centos7 certs]# 

# 根据 private key 生成 RSA public key
[root@lanzhiwang-centos7 certs]# openssl rsa -in domain.key -pubout -out domain-public.key
Enter pass phrase for domain.key:
writing RSA key
[root@lanzhiwang-centos7 certs]# ll
total 8
-rw-r--r-- 1 root root 1766 Jun 12 18:28 domain.key
-rw-r--r-- 1 root root  451 Jun 12 18:30 domain-public.key
[root@lanzhiwang-centos7 certs]# 

# 根据 private key 生成 CSR 文件
[root@lanzhiwang-centos7 certs]# openssl req -new -key domain.key -out domain.csr
Enter pass phrase for domain.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:CN
State or Province Name (full name) []:hubeisheng
Locality Name (eg, city) [Default City]:wuhanshi
Organization Name (eg, company) [Default Company Ltd]:mingyuanyun
Organizational Unit Name (eg, section) []:rdc
Common Name (eg, your name or your server's hostname) []:hub.mingyuanyun.com
Email Address []:huz01@mingyuanyun.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
[root@lanzhiwang-centos7 certs]# ll
total 12
-rw-r--r-- 1 root root 1078 Jun 12 18:34 domain.csr
-rw-r--r-- 1 root root 1766 Jun 12 18:28 domain.key
-rw-r--r-- 1 root root  451 Jun 12 18:30 domain-public.key
[root@lanzhiwang-centos7 certs]# 

# 生成证书 
[root@lanzhiwang-centos7 certs]# openssl x509 -req -days 365 -in domain.csr -signkey domain.key -out domain.crt
Signature ok
subject=/C=CN/ST=hubeisheng/L=wuhanshi/O=mingyuanyun/OU=rdc/CN=hub.mingyuanyun.com/emailAddress=huz01@mingyuanyun.com
Getting Private key
Enter pass phrase for domain.key:
[root@lanzhiwang-centos7 certs]# ll
total 16
-rw-r--r-- 1 root root 1350 Jun 12 18:38 domain.crt
-rw-r--r-- 1 root root 1078 Jun 12 18:34 domain.csr
-rw-r--r-- 1 root root 1766 Jun 12 18:28 domain.key
-rw-r--r-- 1 root root  451 Jun 12 18:30 domain-public.key
[root@lanzhiwang-centos7 certs]# 

[root@lanzhiwang-centos7 certs]# docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -p 443:443 registry
05a955fac1ca9b5d88275606e0ccdf44fefb13aaff6632528fce66a544624db8
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                        PORTS               NAMES
05a955fac1ca        registry            "/entrypoint.sh /etc…"   7 seconds ago       Restarting (1) 1 second ago                       registry

[root@lanzhiwang-centos7 certs]# docker logs 05a955fac1ca
time="2019-06-12T10:39:45.452141464Z" level=warning msg="No HTTP secret provided - generated random secret. This may cause problems with uploads if multiple registries are behind a load-balancer. To provide a shared secret, fill in http.secret in the configuration file or set the REGISTRY_HTTP_SECRET environment variable." go.version=go1.11.2 instance.id=0c6b0c2d-29ba-400c-8370-d0ae640ba169 service=registry version=v2.7.1 
time="2019-06-12T10:39:45.452384667Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=0c6b0c2d-29ba-400c-8370-d0ae640ba169 service=registry version=v2.7.1 
time="2019-06-12T10:39:45.452194709Z" level=info msg="Starting upload purge in 32m0s" go.version=go1.11.2 instance.id=0c6b0c2d-29ba-400c-8370-d0ae640ba169 service=registry version=v2.7.1 
time="2019-06-12T10:39:45.460751715Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=0c6b0c2d-29ba-400c-8370-d0ae640ba169 service=registry version=v2.7.1 
time="2019-06-12T10:39:45.461270556Z" level=fatal msg="tls: failed to parse private key" 

错误分析：
使用的私钥有问题，然后使用不同的算法生成证书和私钥

# 生成 DSA private key
[root@lanzhiwang-centos7 certs]# openssl dsaparam -genkey 2048 | openssl dsa -out domain.key -aes128
read DSA key
Generating DSA parameters, 2048 bit long prime
This could take some time
..+........................+......+......+........+..........+....+..............+.......+.....................+.................+..+.........+....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
..+......................+....................+........+...........+.+........+........+.+.....+........+.+.....+........+.....+.+.................+..+........+........+........+.....+............+.....+...........+..................+......+......+.+................+.+..........+............+.......+......+..........+..+........+.....+...+..................+.........+.......+......+.+......................+.........+.......................+...........+..............+....+......+........+...+........+....+......+...+.....+..+....................+.+......+...................+....+..+..........+.+..+.......+....+..+..........+....+.+....+.....+.+.........+....+...+......+....+.+....+.+...+.+.........+...+...........+...............+..+....+................+.+.............+......+..+.+............+.......+.........+.+....+.................+.......+..........+...+...........+...............+.....+.........+.......+........+..+..+.......+........+.............+.....+...+.....+.................+..............+.............+.+.....+.....+..+............+....+.........+....................+...............................+....+.+...........+..............................+............+.....+.........+.................+...........+..+....+.......+..............+..+.....+...+..+......+...+...+.+...+............+......+..............+.....+..........+.............+........+...................+...........+...+............+......+...+......+..+.....+......+...+....+.......+.+.....+.........+.....+.......+.+.+....+...+......+.+.....+.......+............................+.+...+....+..+.+.+..+.+...........................+......+..+......+..........................+...........+......................................+....+.+.....+................+........+.+.+....+...+..+........+....+..+..................+........+.+..+.+.................+..........+.+.....+.......+.....+..............+........+...............+..........+.+...............................+.+..+.....................+.+................+..+....+........+........................+..........................+.+......................+.......+.......+..+........+............+....................+.........+.......+....+.+.................+...+.............+...+............+.......+...+...+.....+.......+.........+.+..............+.....+.........+............+.....+.....+.....................+.....+........................+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*
writing DSA key
Enter PEM pass phrase: huzhi123456
Verifying - Enter PEM pass phrase:
[root@lanzhiwang-centos7 certs]# ll
total 4
-rw-r--r-- 1 root root 1311 Jun 12 19:46 domain.key
[root@lanzhiwang-centos7 certs]# 

# 公钥
[root@lanzhiwang-centos7 certs]# openssl dsa -in domain.key -pubout -out domain-public.key
read DSA key
Enter pass phrase for domain.key:
writing DSA key
[root@lanzhiwang-centos7 certs]# ll
total 8
-rw-r--r-- 1 root root 1311 Jun 12 19:46 domain.key
-rw-r--r-- 1 root root 1194 Jun 12 19:48 domain-public.key
[root@lanzhiwang-centos7 certs]# 

[root@lanzhiwang-centos7 certs]# openssl req -new -key domain.key -out domain.csr
Enter pass phrase for domain.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:CN
State or Province Name (full name) []:hubeisheng
Locality Name (eg, city) [Default City]:wuhanshi
Organization Name (eg, company) [Default Company Ltd]:mingyuanyun
Organizational Unit Name (eg, section) []:rdc
Common Name (eg, your name or your server's hostname) []:hub.mingyuanyun.com
Email Address []:huz01@mingyuanyun.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# ll
total 12
-rw-r--r-- 1 root root 1565 Jun 12 19:50 domain.csr
-rw-r--r-- 1 root root 1311 Jun 12 19:46 domain.key
-rw-r--r-- 1 root root 1194 Jun 12 19:48 domain-public.key
[root@lanzhiwang-centos7 certs]# 

[root@lanzhiwang-centos7 certs]# openssl x509 -req -days 365 -in domain.csr -signkey domain.key -out domain.crt
Signature ok
subject=/C=CN/ST=hubeisheng/L=wuhanshi/O=mingyuanyun/OU=rdc/CN=hub.mingyuanyun.com/emailAddress=huz01@mingyuanyun.com
Getting Private key
Enter pass phrase for domain.key:
[root@lanzhiwang-centos7 certs]# ll
total 16
-rw-r--r-- 1 root root 1834 Jun 12 19:51 domain.crt
-rw-r--r-- 1 root root 1565 Jun 12 19:50 domain.csr
-rw-r--r-- 1 root root 1311 Jun 12 19:46 domain.key
-rw-r--r-- 1 root root 1194 Jun 12 19:48 domain-public.key
[root@lanzhiwang-centos7 certs]# 

错误分析：
DSA 算法生成的私钥还是有问题，然后使用不同的算法生成证书和私钥


# 直接生成私钥和证书
[root@lanzhiwang-centos7 certs]# openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key -x509 -days 365 -subj '/CN=hub.mingyuanyun.com/' -out domain.crt
Generating a 4096 bit RSA private key
............++
........................................................................................................................................................................................................................................................................................................................++
writing new private key to 'domain.key'
-----
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# ll
total 8
-rw-r--r-- 1 root root 1814 Jun 12 20:15 domain.crt
-rw-r--r-- 1 root root 3272 Jun 12 20:15 domain.key
[root@lanzhiwang-centos7 certs]# 

# 配置客户端使用证书，此时的客户端是 dockerd，服务端是 registry，配置成功后有可能要重启 dockerd
[root@lanzhiwang-centos7 certs]# mkdir -p /etc/docker/certs.d/hub.mingyuanyun.com:443
[root@lanzhiwang-centos7 certs]# cp domain.crt /etc/docker/certs.d/hub.mingyuanyun.com:443/ca.crt
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -p 443:443 registry
b20e9ccf4fad0a0786225496c9e3247d1299393e1b740fd51850f3ecd67b0b06
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                            NAMES
b20e9ccf4fad        registry            "/entrypoint.sh /etc…"   7 seconds ago       Up 6 seconds        0.0.0.0:443->443/tcp, 5000/tcp   registry
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# docker logs b20e9ccf4fad
time="2019-06-12T12:16:29.14524515Z" level=warning msg="No HTTP secret provided - generated random secret. This may cause problems with uploads if multiple registries are behind a load-balancer. To provide a shared secret, fill in http.secret in the configuration file or set the REGISTRY_HTTP_SECRET environment variable." go.version=go1.11.2 instance.id=ec93e3d2-d5f7-481e-b869-8ed0634114a4 service=registry version=v2.7.1 
time="2019-06-12T12:16:29.145373719Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=ec93e3d2-d5f7-481e-b869-8ed0634114a4 service=registry version=v2.7.1 
time="2019-06-12T12:16:29.145531587Z" level=info msg="Starting upload purge in 39m0s" go.version=go1.11.2 instance.id=ec93e3d2-d5f7-481e-b869-8ed0634114a4 service=registry version=v2.7.1 
time="2019-06-12T12:16:29.153631426Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=ec93e3d2-d5f7-481e-b869-8ed0634114a4 service=registry version=v2.7.1 
time="2019-06-12T12:16:29.154187141Z" level=info msg="listening on [::]:443, tls" go.version=go1.11.2 instance.id=ec93e3d2-d5f7-481e-b869-8ed0634114a4 service=registry version=v2.7.1 
[root@lanzhiwang-centos7 certs]# 



[root@lanzhiwang-centos7 registry]# vim /etc/hosts
[root@lanzhiwang-centos7 registry]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
127.0.0.1   hub.mingyuanyun.com
[root@lanzhiwang-centos7 registry]# 

[root@lanzhiwang-centos7 registry]# docker image tag ubuntu hub.mingyuanyun.com:443/myfirstimage
[root@lanzhiwang-centos7 registry]#  
[root@lanzhiwang-centos7 registry]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                                  latest              7698f282e524        4 weeks ago         69.9MB
hub.mingyuanyun.com:443/myfirstimage    latest              7698f282e524        4 weeks ago         69.9MB
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker push hub.mingyuanyun.com:443/myfirstimage
The push refers to repository [hub.mingyuanyun.com:443/myfirstimage]
8d267010480f: Pushed 
270f934787ed: Pushed 
02571d034293: Pushed 
latest: digest: sha256:b36667c98cf8f68d4b7f1fb8e01f742c2ed26b5f0c965a788e98dfe589a4b3e4 size: 943
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker rmi hub.mingyuanyun.com:443/myfirstimage
Untagged: hub.mingyuanyun.com:443/myfirstimage:latest
Untagged: hub.mingyuanyun.com:443/myfirstimage@sha256:b36667c98cf8f68d4b7f1fb8e01f742c2ed26b5f0c965a788e98dfe589a4b3e4
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                                  latest              7698f282e524        4 weeks ago         69.9MB
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker pull hub.mingyuanyun.com:443/myfirstimage
Using default tag: latest
latest: Pulling from myfirstimage
Digest: sha256:b36667c98cf8f68d4b7f1fb8e01f742c2ed26b5f0c965a788e98dfe589a4b3e4
Status: Downloaded newer image for hub.mingyuanyun.com:443/myfirstimage:latest
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                                  latest              7698f282e524        4 weeks ago         69.9MB
hub.mingyuanyun.com:443/myfirstimage    latest              7698f282e524        4 weeks ago         69.9MB
[root@lanzhiwang-centos7 registry]# 

# 测试使用 TLS，并且使用 5000 端口

openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key -x509 -days 365 -subj '/CN=hub.mingyuanyun.com/' -out domain.crt

mkdir -p /etc/docker/certs.d/hub.mingyuanyun.com:5000

cp domain.crt /etc/docker/certs.d/hub.mingyuanyun.com:5000/ca.crt

systemctl restart docker.service

systemctl status docker.service

docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -p 5000:5000 registry

cat /etc/hosts

docker image tag ubuntu hub.mingyuanyun.com:5000/myfirstimage

docker push hub.mingyuanyun.com:5000/myfirstimage

docker rmi hub.mingyuanyun.com:5000/myfirstimage

docker pull hub.mingyuanyun.com:5000/myfirstimage



# 使用简单的用户名和密码认证
# 生成需要的用户名密码文件
[root@lanzhiwang-centos7 ~]# yum install httpd-tools
[root@lanzhiwang-centos7 ~]# rpm -ql httpd-tools.x86_64
[root@lanzhiwang-centos7 ~]# htpasswd -c ./docker-registry-htpasswd admin
New password: MMY@2019@Admin
Re-type new password: MMY@2019@Admin
Adding password for user admin
[root@lanzhiwang-centos7 ~]# cat ./docker-registry-htpasswd
admin:$apr1$S/e42N5R$y89WMbsqD3xsEV1sIAtNS.
[root@lanzhiwang-centos7 ~]# 
# 不要使用 -c 选项生成文件
[root@lanzhiwang-centos7 ~]# htpasswd ./docker-registry-htpasswd rdc-pub
New password: MMY@2019@Admin
Re-type new password: MMY@2019@Admin
Adding password for user rdc-pub
[root@lanzhiwang-centos7 ~]# 
[root@lanzhiwang-centos7 ~]# cat ./docker-registry-htpasswd
admin:$apr1$S/e42N5R$y89WMbsqD3xsEV1sIAtNS.
rdc-pub:$apr1$sWFJkK80$OQ/JBqa/xGd2F2HP5WYRd1
[root@lanzhiwang-centos7 ~]# 

[root@lanzhiwang-centos7 registry]# pwd
/root/work/registry
[root@lanzhiwang-centos7 registry]# ll
total 4
-rw-r--r-- 1 root root 90 Jun 12 18:15 docker-registry-htpasswd
[root@lanzhiwang-centos7 registry]# 

# 另一种生成需要的用户名密码文件的方法
[root@lanzhiwang-centos7 certs]# docker run --entrypoint htpasswd registry -Bbn testuser testpassword > ./htpasswd
[root@lanzhiwang-centos7 certs]# ll
total 4
-rw-r--r-- 1 root root 71 Jun 12 20:07 htpasswd
[root@lanzhiwang-centos7 certs]# cat htpasswd 
testuser:$2y$05$oguk58DuSATOhsRHP0vqsOrA/3g4wqVX5Ioyo1/KSIXvevrLMH.TK


[root@lanzhiwang-centos7 registry]# ll auth/
total 4
-rw-r--r-- 1 root root 90 Jun 12 20:28 docker-registry-htpasswd
[root@lanzhiwang-centos7 registry]# ll certs/
total 8
-rw-r--r-- 1 root root 1814 Jun 12 20:15 domain.crt
-rw-r--r-- 1 root root 3272 Jun 12 20:15 domain.key
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# 

[root@lanzhiwang-centos7 registry]# docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/docker-registry-htpasswd -p 5000:5000 registry
207464519fda2be861c0a33c4c9e40d27e0303787d4bad7cfa7dfc5a4239c9c3
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker push hub.mingyuanyun.com:5000/myfirstimage
The push refers to repository [hub.mingyuanyun.com:5000/myfirstimage]
8d267010480f: Preparing 
270f934787ed: Preparing 
02571d034293: Preparing 
no basic auth credentials
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker login hub.mingyuanyun.com:5000
Username: admin
Password: 
Error response from daemon: login attempt to https://hub.mingyuanyun.com:5000/v2/ failed with status: 401 Unauthorized
[root@lanzhiwang-centos7 registry]# 

错误分析：
不能 push 镜像到仓库，然而也不能登录

解决办法：使用 registry 自带的方法生成用户名密码文件，并且修改文件名

[root@lanzhiwang-centos7 auth]# docker run --entrypoint htpasswd registry -Bbn testuser testpassword > ./htpasswd
[root@lanzhiwang-centos7 auth]# ll
total 8
-rw-r--r-- 1 root root 71 Jun 13 10:21 htpasswd
[root@lanzhiwang-centos7 auth]# cat htpasswd 
testuser:$2y$05$7yrI5AK.tNTkCU987Mvc8u4s2noTZDZxEHhgGNs9SNwc46Zexhna6

[root@lanzhiwang-centos7 auth]# 

[root@lanzhiwang-centos7 auth]# docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd -p 5000:5000 registry
a3a60116a36e334c0dfd15c4ef1f082414d428c430f247e0bdd0ebeb3b5d4e21
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
a3a60116a36e        registry            "/entrypoint.sh /etc…"   8 seconds ago       Up 7 seconds        0.0.0.0:5000->5000/tcp   registry
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# docker logs a3a60116a36e
time="2019-06-13T02:23:44.904386822Z" level=warning msg="No HTTP secret provided - generated random secret. This may cause problems with uploads if multiple registries are behind a load-balancer. To provide a shared secret, fill in http.secret in the configuration file or set the REGISTRY_HTTP_SECRET environment variable." go.version=go1.11.2 instance.id=0dc2468d-92ef-4572-b26e-f2c645d77a12 service=registry version=v2.7.1 
time="2019-06-13T02:23:44.904441882Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=0dc2468d-92ef-4572-b26e-f2c645d77a12 service=registry version=v2.7.1 
time="2019-06-13T02:23:44.906235823Z" level=info msg="Starting upload purge in 48m0s" go.version=go1.11.2 instance.id=0dc2468d-92ef-4572-b26e-f2c645d77a12 service=registry version=v2.7.1 
time="2019-06-13T02:23:44.911696771Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=0dc2468d-92ef-4572-b26e-f2c645d77a12 service=registry version=v2.7.1 
time="2019-06-13T02:23:44.912204744Z" level=info msg="listening on [::]:5000, tls" go.version=go1.11.2 instance.id=0dc2468d-92ef-4572-b26e-f2c645d77a12 service=registry version=v2.7.1 
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# docker push hub.mingyuanyun.com:5000/myfirstimage
The push refers to repository [hub.mingyuanyun.com:5000/myfirstimage]
8d267010480f: Preparing 
270f934787ed: Preparing 
02571d034293: Preparing 
no basic auth credentials
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# docker login hub.mingyuanyun.com:5000
Username: testuser
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[root@lanzhiwang-centos7 auth]# docker push hub.mingyuanyun.com:5000/myfirstimage
The push refers to repository [hub.mingyuanyun.com:5000/myfirstimage]
8d267010480f: Pushed 
270f934787ed: Pushed 
02571d034293: Pushed 
latest: digest: sha256:b36667c98cf8f68d4b7f1fb8e01f742c2ed26b5f0c965a788e98dfe589a4b3e4 size: 943
[root@lanzhiwang-centos7 auth]# 

[root@lanzhiwang-centos7 auth]# docker logout hub.mingyuanyun.com:5000
Removing login credentials for hub.mingyuanyun.com:5000
[root@lanzhiwang-centos7 auth]# 

[root@lanzhiwang-centos7 auth]# docker push hub.mingyuanyun.com:5000/myfirstimage
The push refers to repository [hub.mingyuanyun.com:5000/myfirstimage]
8d267010480f: Preparing 
270f934787ed: Preparing 
02571d034293: Preparing 
no basic auth credentials
[root@lanzhiwang-centos7 auth]# 

# 测试挂载数据目录
docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd -v /root/work/registry/data:/var/lib/registry -p 5000:5000 registry


# 测试配置文件
# 使用比较多的选项启动容器配置文件也比较少，测试使用比较少的配置文件看能不能成功运行容器
[root@lanzhiwang-centos7 registry]# docker cp a3a60116a36e:/etc/docker/registry/config.yml ./
[root@lanzhiwang-centos7 registry]# cat config.yml 
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
[root@lanzhiwang-centos7 registry]# 

docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd -v /root/work/registry/data:/var/lib/registry -v /root/work/registry/config/config.yml:/etc/docker/registry/config.yml -p 5000:5000 registry

[root@lanzhiwang-centos7 registry]# docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd -v /root/work/registry/data:/var/lib/registry -v /root/work/registry/config/config.yml:/etc/docker/registry/config.yml -p 5000:5000 registry
69263ca8c23de95ecd27c3b60972e472490eab0188c52f0bc0686d0d521a883a
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
69263ca8c23d        registry            "/entrypoint.sh /etc…"   9 seconds ago       Up 8 seconds        0.0.0.0:5000->5000/tcp   registry
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker logs 69263ca8c23d
time="2019-06-13T02:52:07.967683542Z" level=warning msg="No HTTP secret provided - generated random secret. This may cause problems with uploads if multiple registries are behind a load-balancer. To provide a shared secret, fill in http.secret in the configuration file or set the REGISTRY_HTTP_SECRET environment variable." go.version=go1.11.2 instance.id=bf1d773e-ca22-478d-a5be-fa8bb28d7041 service=registry version=v2.7.1 
time="2019-06-13T02:52:07.967746627Z" level=info msg="redis not configured" go.version=go1.11.2 instance.id=bf1d773e-ca22-478d-a5be-fa8bb28d7041 service=registry version=v2.7.1 
time="2019-06-13T02:52:07.969029161Z" level=info msg="Starting upload purge in 1m0s" go.version=go1.11.2 instance.id=bf1d773e-ca22-478d-a5be-fa8bb28d7041 service=registry version=v2.7.1 
time="2019-06-13T02:52:07.974583792Z" level=info msg="using inmemory blob descriptor cache" go.version=go1.11.2 instance.id=bf1d773e-ca22-478d-a5be-fa8bb28d7041 service=registry version=v2.7.1 
time="2019-06-13T02:52:07.975192264Z" level=info msg="listening on [::]:5000, tls" go.version=go1.11.2 instance.id=bf1d773e-ca22-478d-a5be-fa8bb28d7041 service=registry version=v2.7.1 
[root@lanzhiwang-centos7 registry]# 

# 测试 log 挂载

# docker registry ui









https://hub.docker.com/publishers/microsoftowner


# 在 Linux 上存储 windows 镜像
[root@lanzhiwang-centos7 registry]# docker pull mcr.microsoft.com/windows/servercore:ltsc2019
ltsc2019: Pulling from windows/servercore
no matching manifest for linux/amd64 in the manifest list entries
[root@lanzhiwang-centos7 registry]# 
[root@lanzhiwang-centos7 registry]# docker pull mcr.microsoft.com/windows/servercore:ltsc2019-amd64
ltsc2019-amd64: Pulling from windows/servercore
65014b3c3121: Downloading 
266cffe9d908: Downloading 
image operating system "windows" cannot be used on this platform


# 在 windows 上存储 windows 镜像
PS C:\Users\huz01> docker -H  tcp://0.0.0.0:2376 pull mcr.microsoft.com/windows/servercore:ltsc2019-amd64
ltsc2019-amd64: Pulling from windows/servercore
a Windows version 10.0.17763-based image is incompatible with a 10.0.14393 host



PS C:\Users\huz01> docker -H  tcp://0.0.0.0:2376 pull mcr.microsoft.com/windows/servercore:ltsc2016-amd64
ltsc2016-amd64: Pulling from windows/servercore
3889bb8d808b: Downloading [>                                                  ]   17.4MB/4.07GB
b39d5d9be066: Downloading [=>                                                 ]  48.54MB/1.64GB

PS C:\Users\huz01> docker -H  tcp://0.0.0.0:2376 image tag mcr.microsoft.com/windows/servercore:ltsc2016-amd64 10.5.10.118:5000/windows/servercore
PS C:\Users\huz01>
PS C:\Users\huz01>
PS C:\Users\huz01> docker -H  tcp://0.0.0.0:2376 images
REPOSITORY                             TAG                 IMAGE ID            CREATED             SIZE
10.5.10.118:5000/windows/servercore    latest              9c52998a9f27        34 hours ago        11.1GB
mcr.microsoft.com/windows/servercore   ltsc2016-amd64      9c52998a9f27        34 hours ago        11.1GB
registry.mingyuanyun.com:5000/mysoft   hello-world         2c911f8d79db        5 months ago        1.17GB
10.1.36.26:5000/mysoft                 test                ad07b2022f07        14 months ago       1.13GB
stefanscherer/registry-windows         2.6.2-1607          ad07b2022f07        14 months ago       1.13GB
PS C:\Users\huz01>
PS C:\Users\huz01> docker -H  tcp://0.0.0.0:2376 push  10.5.10.118:5000/windows/servercore
The push refers to repository [10.5.10.118:5000/windows/servercore]
Get https://10.5.10.118:5000/v2/: http: server gave HTTP response to HTTPS client



docker pull mcr.microsoft.com/dotnet/core/samples:aspnetapp-nanoserver-sac2016

docker run -it --rm -p 8000:80 --name aspnetcore_sample mcr.microsoft.com/dotnet/core/samples:aspnetapp-nanoserver-sac2016

http://localhost:8000

PS C:\Windows\system32> docker info
Containers: 0
 Running: 0
 Paused: 0
 Stopped: 0
Images: 1
Server Version: 18.09.2
Storage Driver: windowsfilter



docker run -d --restart=always --name registry 
-p 5000:5000 
-v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key 
-v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd 
-v /root/work/registry/data:/var/lib/registry 
-v /root/work/registry/config/config.yml:/etc/docker/registry/config.yml 
registry

kubectl create configmap docker-registry-auth --from-file=./htpasswd

kubectl create configmap docker-registry-config --from-file=./config.yml

docker run --entrypoint htpasswd registry -Bbn rdc-pub Mysoft@rdc2019!  > ./htpasswd
docker run --entrypoint htpasswd registry -Bbn admin Mysoft@rdc2019!  > ./htpasswd

[root@k8s-master1 registry]# vim config.yml
[root@k8s-master1 registry]# cat config.yml
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
[root@k8s-master1 registry]# 


[root@k8s-master1 ~]# kubectl create secret --help
Create a secret using specified subcommand.

Available Commands:
  docker-registry Create a secret for use with a Docker registry
  generic         Create a secret from a local file, directory or literal value
  tls             Create a TLS secret

Usage:
  kubectl create secret [flags] [options]

Use "kubectl <command> --help" for more information about a given command.
Use "kubectl options" for a list of global command-line options (applies to all commands).
[root@k8s-master1 ~]# 


kubectl create secret docker-registry --help


[root@k8s-master1 registry]# vim docker-registry.yml
[root@k8s-master1 registry]# cat docker-registry.yml
---
apiVersion: v1
kind: Service
metadata:
  name: docker-registry
  labels:
    app: docker-registry
spec:
  ports:
  - name: http
    port: 5000
    targetPort: 5000
    protocol: TCP
  selector:
    app: docker-registry
    service: docker-registry
  type: NodePort
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-registry
  labels:
    service: docker-registry
    app: docker-registry
spec:
  replicas: 1
  selector:
    matchLabels:
      app: docker-registry
      service: docker-registry
  template:
    metadata:
      labels:
        app: docker-registry
        service: docker-registry
    spec:
      containers:
        - name: docker-registry
          image: registry:latest
          imagePullPolicy: Always
          env:
            - name: REGISTRY_HTTP_ADDR
              value: 0.0.0.0:5000

            - name: REGISTRY_HTTP_TLS_CERTIFICATE
              value: /certs/domain.crt

            - name: REGISTRY_HTTP_TLS_KEY
              value: /certs/domain.key

            - name: REGISTRY_AUTH
              value: htpasswd

            - name: REGISTRY_AUTH_HTPASSWD_REALM
              value: Registry Realm

            - name: REGISTRY_AUTH_HTPASSWD_PATH
              value: /auth/htpasswd

          ports:
            - containerPort: 5000

          volumeMounts:
          - name: docker-registry-certs
            mountPath: /certs
            readOnly: true

          - name: docker-registry-data
            mountPath: /var/lib/registry

          - name: docker-registry-auth
            subPath: htpasswd
            mountPath: /auth/htpasswd
            readOnly: true

          - name: docker-registry-config
            subPath: config.yml
            mountPath: /etc/docker/registry/config.yml
            readOnly: true

      nodeSelector:
        nodename:
          k8s-linux-worker2

      volumes:
        - name: docker-registry-certs
          hostPath:
            path: /opt/k8s/volume_data/registry/certs/

        - name: docker-registry-data
          hostPath:
            path: /opt/k8s/volume_data/registry/data/

        - name: docker-registry-auth
          configMap:
            name: docker-registry-auth

        - name: docker-registry-config
          configMap:
            name: docker-registry-config

---

[root@k8s-master1 registry]# 



[root@localhost ~]# docker push hub.mingyuanyun.com:36496/myfirstimage
The push refers to repository [hub.mingyuanyun.com:36496/myfirstimage]
73d61bf022fd: Preparing 
5bbc5831d696: Preparing 
d5974ddb5a45: Preparing 
f641ef7a37ad: Preparing 
d9ff549177a9: Preparing 
no basic auth credentials
[root@localhost ~]# 
[root@localhost ~]# docker login hub.mingyuanyun.com:36496
Username: rdc-pub
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
You have new mail in /var/spool/mail/root
[root@localhost ~]# 
[root@localhost ~]# docker push hub.mingyuanyun.com:36496/myfirstimage
The push refers to repository [hub.mingyuanyun.com:36496/myfirstimage]
73d61bf022fd: Pushed 
5bbc5831d696: Pushed 
d5974ddb5a45: Pushed 
f641ef7a37ad: Pushed 
d9ff549177a9: Pushed 
latest: digest: sha256:b1165286043f2745f45ea637873d61939bff6d9a59f76539d6228abf79f87774 size: 1363
[root@localhost ~]# 

[root@localhost ~]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! -k -X GET https://hub.mingyuanyun.com:36496/v2/
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
* skipping SSL peer certificate verification
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/ HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Length: 2
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:09:29 GMT
< 
* Connection #0 to host hub.mingyuanyun.com left intact
{}
You have new mail in /var/spool/mail/root
[root@localhost ~]# 

[root@localhost ~]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! -k -X GET https://hub.mingyuanyun.com:36496/v2/myfirstimage/tags/list
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
* skipping SSL peer certificate verification
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/myfirstimage/tags/list HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:12:32 GMT
< Content-Length: 42
< 
{"name":"myfirstimage","tags":["latest"]}
* Connection #0 to host hub.mingyuanyun.com left intact
[root@localhost ~]# 


[root@localhost ~]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! -k -X GET https://hub.mingyuanyun.com:36496/v2/myfirstimage/manifests/latest
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
* skipping SSL peer certificate verification
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/myfirstimage/manifests/latest HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Length: 6868
< Content-Type: application/vnd.docker.distribution.manifest.v1+prettyjws
< Docker-Content-Digest: sha256:1f57f7cdfdf1a7fd7a5beb2b459628de0665556684a16bf5aae10591741238c9
< Docker-Distribution-Api-Version: registry/2.0
< Etag: "sha256:1f57f7cdfdf1a7fd7a5beb2b459628de0665556684a16bf5aae10591741238c9"
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:15:30 GMT
< 
{
   "schemaVersion": 1,
   "name": "myfirstimage",
   "tag": "latest",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:b4541f6d3db6307e43bad1ca823a3221d4c2689bcae8bbd8a312371815e1d1bf"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:e8afc091c171595794b2c72071946d2e34c0ecbc00de8b5f8a80dda0f7dfc801"
      },
      {
         "blobSum": "sha256:54d33bcb37f53c65d2678796a458525d291c18058ff65c137d0aea45849e3f14"
      },
      {
         "blobSum": "sha256:1cc8e0bb44dfaefdc7f0d0ce35f7bcb5bd2b91467a0ad7501499e34de27e3ee4"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:c87736221ed0bcaa60b8e92a19bec2284899ef89226f2a07968677cf59e637a4"
      }
   ],
   "history": [
      {
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"ExposedPorts\":{\"5000/tcp\":{}},\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/etc/docker/registry/config.yml\"],\"ArgsEscaped\":true,\"Image\":\"sha256:fa75451235d0beeed53ad924de2045ecd96c1819814e947af52eaf3105a470e8\",\"Volumes\":{\"/var/lib/registry\":{}},\"WorkingDir\":\"\",\"Entrypoint\":[\"/entrypoint.sh\"],\"OnBuild\":null,\"Labels\":null},\"container\":\"065d383f87625190f4b217ee6e13809dd3d59477c32e1813222e4f2ff7b3b6c9\",\"container_config\":{\"Hostname\":\"065d383f8762\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"ExposedPorts\":{\"5000/tcp\":{}},\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"#(nop) \",\"CMD [\\\"/etc/docker/registry/config.yml\\\"]\"],\"ArgsEscaped\":true,\"Image\":\"sha256:fa75451235d0beeed53ad924de2045ecd96c1819814e947af52eaf3105a470e8\",\"Volumes\":{\"/var/lib/registry\":{}},\"WorkingDir\":\"\",\"Entrypoint\":[\"/entrypoint.sh\"],\"OnBuild\":null,\"Labels\":{}},\"created\":\"2019-03-08T02:46:39.207047736Z\",\"docker_version\":\"18.06.1-ce\",\"id\":\"f99738109191228433031ef0465bd0acf74f4415cce820ca1103a3bae96c1735\",\"os\":\"linux\",\"parent\":\"e003ce632a6db08f325675d85a822d530fa57ffe0e06efbf7f3e5ca6601f1d64\",\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"e003ce632a6db08f325675d85a822d530fa57ffe0e06efbf7f3e5ca6601f1d64\",\"parent\":\"0065ebdad215bd0c8770ed6935fd7779919c1d7a098f48af4cbba383dfc76e1c\",\"created\":\"2019-03-08T02:46:38.959067866Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  ENTRYPOINT [\\\"/entrypoint.sh\\\"]\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"0065ebdad215bd0c8770ed6935fd7779919c1d7a098f48af4cbba383dfc76e1c\",\"parent\":\"a2f981cd64ba8170b7cdab49f76e31cabbed044f0327be575ee0135393b05f32\",\"created\":\"2019-03-08T02:46:38.727415035Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) COPY file:507caa54f88c1f3862e5876e09a108b2083630ba24c57ad124e356a2de861d62 in /entrypoint.sh \"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"a2f981cd64ba8170b7cdab49f76e31cabbed044f0327be575ee0135393b05f32\",\"parent\":\"d33041cd457724bc9953ecbf487c81734909cf01de770d0fd1118d7ea0621bdb\",\"created\":\"2019-03-08T02:46:38.427513209Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  EXPOSE 5000\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"d33041cd457724bc9953ecbf487c81734909cf01de770d0fd1118d7ea0621bdb\",\"parent\":\"d0f44026bcfdbf5c0e9567bcaa4adf006ce1724d1351a271c383cea66fca5b38\",\"created\":\"2019-03-08T02:46:38.191326162Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  VOLUME [/var/lib/registry]\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"d0f44026bcfdbf5c0e9567bcaa4adf006ce1724d1351a271c383cea66fca5b38\",\"parent\":\"1a6638ea4ae60b9fd80a928e9d3483148d1a2e6d70c00e9a89f2a6fcf01250ff\",\"created\":\"2019-03-08T02:46:37.944406267Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) COPY file:4544cc1555469403b322faecc1cf1ca584667c43a6a60b17300f97840c04196e in /etc/docker/registry/config.yml \"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"1a6638ea4ae60b9fd80a928e9d3483148d1a2e6d70c00e9a89f2a6fcf01250ff\",\"parent\":\"ee207260066f7648f038bae812cf94f1f90529e9a9c6a983ef1f43a4246c9681\",\"created\":\"2019-03-08T02:46:37.679249576Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) COPY file:21256ff7df5369f7ad2e19c6d020a644303aded200bdbec4d46648f38d55df78 in /bin/registry \"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"ee207260066f7648f038bae812cf94f1f90529e9a9c6a983ef1f43a4246c9681\",\"parent\":\"5051fe558ac9a3a77a13fe215bfc7f315990f69fe4fc90a043727d239bf6db48\",\"created\":\"2019-03-08T02:46:37.128907849Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c set -ex     \\u0026\\u0026 apk add --no-cache ca-certificates apache2-utils\"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"5051fe558ac9a3a77a13fe215bfc7f315990f69fe4fc90a043727d239bf6db48\",\"parent\":\"3ade34601851dd2693d99fa15d4d10a5f35a8c7ea87195a96a65dfa22a6a28e1\",\"created\":\"2019-03-07T22:19:46.815331171Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  CMD [\\\"/bin/sh\\\"]\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"3ade34601851dd2693d99fa15d4d10a5f35a8c7ea87195a96a65dfa22a6a28e1\",\"created\":\"2019-03-07T22:19:46.661698137Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) ADD file:38bc6b51693b13d84a63e281403e2f6d0218c44b1d7ff12157c4523f9f0ebb1e in / \"]}}"
      }
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "EF2G:QXGS:4LXQ:F36M:RQPC:RBDV:5ZJH:E3CN:HPTQ:P7AR:IHA3:OMZA",
               "kty": "EC",
               "x": "Cdtg9Uc1hL-RdlrcZ-EAHoNSD8S2nq0J0szuWSpB-UA",
               "y": "fdJPSHfpKNG_vy1RaPDvoArggjBKZXlyCe1SRm-snhI"
            },
            "alg": "ES256"
         },
         "signature": "jv56tAx5MzhdoWbSawOoHB3Vj32GsLSicwkQ6yAFlFr1aVpIg7nupKVqCmc6-fxh9UHkDt6RwkOz2R49BO2R7A",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjYyMjEsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAxOS0wNi0xNFQwODoxNTozMFoifQ"
      }
   ]
* Connection #0 to host hub.mingyuanyun.com left intact
}
[root@localhost ~]# 


[root@localhost ~]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! -k -X GET https://hub.mingyuanyun.com:36496/v2/myfirstimage/manifests/sha256:b1165286043f2745f45ea637873d61939bff6d9a59f76539d6228abf79f87774
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
* skipping SSL peer certificate verification
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/myfirstimage/manifests/sha256:b1165286043f2745f45ea637873d61939bff6d9a59f76539d6228abf79f87774 HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Length: 1363
< Content-Type: application/vnd.docker.distribution.manifest.v2+json
< Docker-Content-Digest: sha256:b1165286043f2745f45ea637873d61939bff6d9a59f76539d6228abf79f87774
< Docker-Distribution-Api-Version: registry/2.0
< Etag: "sha256:b1165286043f2745f45ea637873d61939bff6d9a59f76539d6228abf79f87774"
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:16:59 GMT
< 
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
   "config": {
      "mediaType": "application/vnd.docker.container.image.v1+json",
      "size": 3168,
      "digest": "sha256:f32a97de94e13d29835a19851acd6cbc7979d1d50f703725541e44bb89a1ce91"
   },
   "layers": [
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 2207176,
         "digest": "sha256:c87736221ed0bcaa60b8e92a19bec2284899ef89226f2a07968677cf59e637a4"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 627158,
         "digest": "sha256:1cc8e0bb44dfaefdc7f0d0ce35f7bcb5bd2b91467a0ad7501499e34de27e3ee4"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 6823927,
         "digest": "sha256:54d33bcb37f53c65d2678796a458525d291c18058ff65c137d0aea45849e3f14"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 371,
         "digest": "sha256:e8afc091c171595794b2c72071946d2e34c0ecbc00de8b5f8a80dda0f7dfc801"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 214,
         "digest": "sha256:b4541f6d3db6307e43bad1ca823a3221d4c2689bcae8bbd8a312371815e1d1bf"
      }
   ]
* Connection #0 to host hub.mingyuanyun.com left intact
}
[root@localhost ~]# 

##############################################################################################################

# 解决 curl 使用 ssl 证书的问题
# 使用 -k 选项允许使用无证书的不安全SSL进行连接和传输。但这不安全，还是需要使用证书
[root@localhost nssdb]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! -k -X GET https://hub.mingyuanyun.com:36496/v2/
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
* skipping SSL peer certificate verification
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/ HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Length: 2
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:28:38 GMT
< 
* Connection #0 to host hub.mingyuanyun.com left intact
{}
[root@localhost nssdb]# 


# 不使用 -k 选项，观察 curl 使用证书的过程
[root@localhost nssdb]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! -X GET https://hub.mingyuanyun.com:36496/v2/
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
*   CAfile: /etc/pki/tls/certs/ca-bundle.crt
  CApath: none
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* NSS error -8172 (SEC_ERROR_UNTRUSTED_ISSUER)
* Peer's certificate issuer has been marked as not trusted by the user.
* Closing connection 0
curl: (60) Peer's certificate issuer has been marked as not trusted by the user.
More details here: http://curl.haxx.se/docs/sslcerts.html

curl performs SSL certificate verification by default, using a "bundle"
 of Certificate Authority (CA) public keys (CA certs). If the default
 bundle file isn't adequate, you can specify an alternate file
 using the --cacert option.
If this HTTPS server uses a certificate signed by a CA represented in
 the bundle, the certificate verification probably failed due to a
 problem with the certificate (it might be expired, or the name might
 not match the domain name in the URL).
If you'd like to turn off curl's verification of the certificate, use
 the -k (or --insecure) option.

# 从输出可以看出，curl 默认会从 /etc/pki/tls/certs/ 目录中读取相关证书，所以可以将自定义证书放在该目录下，并且需要注意文件权限，文件权限就和已有的证书权限一样

[root@localhost nssdb]# 
[root@localhost nssdb]# cd /etc/pki/tls/certs/
[root@localhost certs]# ll
total 12
lrwxrwxrwx. 1 root root   49 Aug 27  2018 ca-bundle.crt -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
lrwxrwxrwx. 1 root root   55 Aug 27  2018 ca-bundle.trust.crt -> /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
-rwxr-xr-x. 1 root root  610 Apr 11  2018 make-dummy-cert
-rw-r--r--. 1 root root 2516 Apr 11  2018 Makefile
-rwxr-xr-x. 1 root root  829 Apr 11  2018 renew-dummy-cert
[root@localhost certs]# ll /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
-r--r--r--. 1 root root 398934 Aug 27  2018 /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
You have new mail in /var/spool/mail/root
[root@localhost certs]# 
[root@localhost certs]# cp /etc/docker/certs.d/hub.mingyuanyun.com:36496/ca.crt ./
[root@localhost certs]# ll
total 16
lrwxrwxrwx. 1 root root   49 Aug 27  2018 ca-bundle.crt -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
lrwxrwxrwx. 1 root root   55 Aug 27  2018 ca-bundle.trust.crt -> /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
-rw-r--r--  1 root root 1814 Jun 14 08:31 ca.crt
-rwxr-xr-x. 1 root root  610 Apr 11  2018 make-dummy-cert
-rw-r--r--. 1 root root 2516 Apr 11  2018 Makefile
-rwxr-xr-x. 1 root root  829 Apr 11  2018 renew-dummy-cert
[root@localhost certs]# chmod 444 ca.crt
You have new mail in /var/spool/mail/root
[root@localhost certs]# ll
total 16
lrwxrwxrwx. 1 root root   49 Aug 27  2018 ca-bundle.crt -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
lrwxrwxrwx. 1 root root   55 Aug 27  2018 ca-bundle.trust.crt -> /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
-r--r--r--  1 root root 1814 Jun 14 08:31 ca.crt
-rwxr-xr-x. 1 root root  610 Apr 11  2018 make-dummy-cert
-rw-r--r--. 1 root root 2516 Apr 11  2018 Makefile
-rwxr-xr-x. 1 root root  829 Apr 11  2018 renew-dummy-cert
[root@localhost certs]# 
[root@localhost certs]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! --cacert /etc/pki/tls/certs/ca.crt  -X GET https://hub.mingyuanyun.com:36496/v2/
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
*   CAfile: /etc/pki/tls/certs/ca.crt
  CApath: none
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/ HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Length: 2
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:32:53 GMT
< 
* Connection #0 to host hub.mingyuanyun.com left intact
{}
[root@localhost certs]# 

# 不使用 ca.crt 这个文件名，容易产生歧义，修改为 hub.mingyuanyum.com.crt
[root@localhost certs]# mv ca.crt hub.mingyuanyum.com.crt
[root@localhost certs]# ll
total 16
lrwxrwxrwx. 1 root root   49 Aug 27  2018 ca-bundle.crt -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
lrwxrwxrwx. 1 root root   55 Aug 27  2018 ca-bundle.trust.crt -> /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
-r--r--r--  1 root root 1814 Jun 14 08:31 hub.mingyuanyum.com.crt
-rwxr-xr-x. 1 root root  610 Apr 11  2018 make-dummy-cert
-rw-r--r--. 1 root root 2516 Apr 11  2018 Makefile
-rwxr-xr-x. 1 root root  829 Apr 11  2018 renew-dummy-cert
[root@localhost certs]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! --cacert /etc/pki/tls/certs/hub.mingyuanyum.com.crt  -X GET https://hub.mingyuanyun.com:36496/v2/
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
*   CAfile: /etc/pki/tls/certs/hub.mingyuanyum.com.crt
  CApath: none
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/ HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Length: 2
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:44:03 GMT
< 
* Connection #0 to host hub.mingyuanyun.com left intact
{}
[root@localhost certs]# 

# 测试是否可以将证书放入任意位置
[root@localhost ~]# pwd
/root
[root@localhost ~]# mv /etc/pki/tls/certs/hub.mingyuanyum.com.crt ./
[root@localhost ~]# ll hub.mingyuanyum.com.crt 
-r--r--r-- 1 root root 1814 Jun 14 08:31 hub.mingyuanyum.com.crt
[root@localhost ~]# 
[root@localhost ~]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! --cacert ./hub.mingyuanyum.com.crt  -X GET https://hub.mingyuanyun.com:36496/v2/
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
*   CAfile: ./hub.mingyuanyum.com.crt
  CApath: none
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/ HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Length: 2
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:46:14 GMT
< 
* Connection #0 to host hub.mingyuanyun.com left intact
{}
[root@localhost ~]# 

[root@localhost ~]# curl -vvv -H "Host: hub.mingyuanyun.com" --user admin:Mysoft@rdc2019! --cacert ./hub.mingyuanyum.com.crt -X GET https://hub.mingyuanyun.com:36496/v2/myfirstimage/tags/list
* About to connect() to hub.mingyuanyun.com port 36496 (#0)
*   Trying 10.1.36.47...
* Connected to hub.mingyuanyun.com (10.1.36.47) port 36496 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
*   CAfile: ./hub.mingyuanyum.com.crt
  CApath: none
* SSL connection using TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
* Server certificate:
* 	subject: CN=hub.mingyuanyun.com
* 	start date: Jun 14 07:21:01 2019 GMT
* 	expire date: Jun 13 07:21:01 2020 GMT
* 	common name: hub.mingyuanyun.com
* 	issuer: CN=hub.mingyuanyun.com
* Server auth using Basic with user 'admin'
> GET /v2/myfirstimage/tags/list HTTP/1.1
> Authorization: Basic YWRtaW46TXlzb2Z0QHJkYzIwMTkh
> User-Agent: curl/7.29.0
> Accept: */*
> Host: hub.mingyuanyun.com
> 
< HTTP/1.1 200 OK
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< X-Content-Type-Options: nosniff
< Date: Fri, 14 Jun 2019 08:47:31 GMT
< Content-Length: 42
< 
{"name":"myfirstimage","tags":["latest"]}
* Connection #0 to host hub.mingyuanyun.com left intact
[root@localhost ~]# 



```





