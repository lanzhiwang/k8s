### bitbucket

```bash
[root@lanzhiwang-centos7 ~]# docker pull atlassian/bitbucket-server

[root@lanzhiwang-centos7 work]# mkdir bitbucket
[root@lanzhiwang-centos7 work]# cd bitbucket
[root@lanzhiwang-centos7 bitbucket]# pwd
/root/work/bitbucket
[root@lanzhiwang-centos7 bitbucket]# 

[root@lanzhiwang-centos7 bitbucket]# docker run -v /root/work/bitbucket:/var/atlassian/application-data/bitbucket --name="bitbucket" -d -p 7990:7990 -p 7999:7999 atlassian/bitbucket-server
6b4c2519b413e4d41819cb269dfeb78cede7279526c35b57fa13f6fe7074a125
[root@lanzhiwang-centos7 bitbucket]# 
[root@lanzhiwang-centos7 bitbucket]# docker ps -a
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS              PORTS                                            NAMES
6b4c2519b413        atlassian/bitbucket-server   "/tini -- /entrypoin…"   32 seconds ago      Up 31 seconds       0.0.0.0:7990->7990/tcp, 0.0.0.0:7999->7999/tcp   bitbucket
[root@lanzhiwang-centos7 bitbucket]# 
[root@lanzhiwang-centos7 bitbucket]# 

```