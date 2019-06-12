### Docker Registry

Docker Registry 相关内容：

* 使用 Docker Registry 的两种主要方式：
	* 通过容器方式运行
	* 通过本地安装运行并注册为系统服务

* 添加 Nginx 反向代理

* 添加用户认证功能

* Docker Registry 配置文件中各个选项的含义和使用

* 使用 Registry 的通知系统来支持更多应用场景




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




```





