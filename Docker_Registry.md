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
# 从已经运行的容器中拷贝出来
docker run -d -p 5000:5000 --restart=always --name registry \
             -v `pwd`/config.yml:/etc/docker/registry/config.yml \
             registry:2

# Registry 默认的存储位置为 /var/lib/registry，可以通过 -v 参数来映射本地的路径到容器内。
-v /opt/data/registry:/var/lib/registry

# 配置 TLS 证书
# 生成过程中会提示填入各种信息，注意 CN 一栏的信息要填入跟访问的地址相同的域名，例如这里应该为myrepo.com
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

docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -p 443:443 registry

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
使用的私钥有问题

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

# 
[root@lanzhiwang-centos7 certs]# openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key -x509 -days 365 -subj '/CN=hub.mingyuanyun.com/' -out domain.crt
Generating a 4096 bit RSA private key
............++
........................................................................................................................................................................................................................................................................................................................++
writing new private key to 'domain.key'
-----
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# ll
total 8
-rw-r--r-- 1 root root 1814 Jun 12 20:15 domain.crt
-rw-r--r-- 1 root root 3272 Jun 12 20:15 domain.key
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# 
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


[root@lanzhiwang-centos7 certs]# mkdir -p /etc/docker/certs.d/hub.mingyuanyun.com:443
[root@lanzhiwang-centos7 certs]# cp domain.crt /etc/docker/certs.d/hub.mingyuanyun.com:443/ca.crt
[root@lanzhiwang-centos7 certs]# 

[root@lanzhiwang-centos7 registry]# vim /etc/hosts
[root@lanzhiwang-centos7 registry]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
127.0.0.1   hub.mingyuanyun.com
[root@lanzhiwang-centos7 registry]# 



[root@lanzhiwang-centos7 certs]# docker image tag ubuntu localhost:443/myfirstimage
[root@lanzhiwang-centos7 certs]# docker push localhost:443/myfirstimage
The push refers to repository [localhost:443/myfirstimage]
8d267010480f: Pushed 
270f934787ed: Pushed 
02571d034293: Pushed 
latest: digest: sha256:b36667c98cf8f68d4b7f1fb8e01f742c2ed26b5f0c965a788e98dfe589a4b3e4 size: 943
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# docker image tag ubuntu localhost:5000/myfirstimage
[root@lanzhiwang-centos7 certs]# docker push localhost:5000/myfirstimage
The push refers to repository [localhost:5000/myfirstimage]
Get http://localhost:5000/v2/: dial tcp [::1]:5000: connect: connection refused
[root@lanzhiwang-centos7 certs]# 

[root@lanzhiwang-centos7 certs]# docker pull localhost:443/myfirstimage
Using default tag: latest
latest: Pulling from myfirstimage
Digest: sha256:b36667c98cf8f68d4b7f1fb8e01f742c2ed26b5f0c965a788e98dfe589a4b3e4
Status: Downloaded newer image for localhost:443/myfirstimage:latest
[root@lanzhiwang-centos7 certs]# 
[root@lanzhiwang-centos7 certs]# docker pull localhost:5000/myfirstimage
Using default tag: latest
Error response from daemon: Get http://localhost:5000/v2/: dial tcp [::1]:5000: connect: connection refused
[root@lanzhiwang-centos7 certs]# 























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

# 
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

[root@lanzhiwang-centos7 auth]# docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/docker-registry-htpasswd -p 443:443 registry
4f55c7a476b7696a05a2021dc5641a7b1401d2fb9c85cba2fab62529913e3799
[root@lanzhiwang-centos7 auth]# 
[root@lanzhiwang-centos7 auth]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                            NAMES
4f55c7a476b7        registry            "/entrypoint.sh /etc…"   10 seconds ago      Up 9 seconds        0.0.0.0:443->443/tcp, 5000/tcp   registry
[root@lanzhiwang-centos7 auth]# 



[root@lanzhiwang-centos7 auth]# docker push localhost:443/myfirstimage
The push refers to repository [localhost:443/myfirstimage]
8d267010480f: Preparing 
270f934787ed: Preparing 
02571d034293: Preparing 
no basic auth credentials
[root@lanzhiwang-centos7 auth]# docker login localhost:443
Username: admin
Password: 
Error response from daemon: login attempt to https://localhost:443/v2/ failed with status: 401 Unauthorized
[root@lanzhiwang-centos7 auth]# docker ps -a










docker run -d -p 5000:5000 --restart=always --name registry registry
docker run -d -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 -v /root/work/registry/data:/var/lib/registry -p 5000:5000 --restart=always --name registry registry

docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -p 443:443 registry

docker run -d --restart=always --name registry -v /root/work/registry/certs:/certs -e REGISTRY_HTTP_ADDR=0.0.0.0:443 -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key -v /root/work/registry/auth:/auth -e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/docker-registry-htpasswd -p 443:443 registry

docker run -d -p 443:443 \
  --restart=always \
  --name registry \
  -v "$(pwd)"/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -v "$(pwd)"/certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  registry:2


```





