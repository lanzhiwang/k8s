# gitlab 数据迁移

[参考1](https://pikedom.com/migrate-gitlab-instance-to-new-host/)

[参考2](https://docs.gitlab.com/ee/raketasks/backup_restore.html)

使用 docker 安装 gitlab

```bash
[root@gitlab gitlab-test-data]# cat docker-compose.yml 
web:
  image: 'gitlab/gitlab-ce:11.1.4-ce.0'
  restart: always
  hostname: '10.1.36.45'
  container_name: gitlab-test
  environment:
    GITLAB_OMNIBUS_CONFIG: |
      external_url 'http://10.1.36.45:9090'
      gitlab_rails['gitlab_shell_ssh_port'] = 2224
  ports:
    - '9090:9090'
    - '2224:22'
  volumes:
    - '/data/gitlab-test-data/config:/etc/gitlab'
    - '/data/gitlab-test-data/logs:/var/log/gitlab'
    - '/data/gitlab-test-data/data:/var/opt/gitlab'

[root@gitlab gitlab-test-data]# 

docker-compose up -d


```




先迁移配置，后迁移数据

迁移配置：

只需要迁移 

```bash
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   config/gitlab-secrets.json
        modified:   config/gitlab.rb
        modified:   config/ssh_host_ecdsa_key
        modified:   config/ssh_host_ecdsa_key.pub
        modified:   config/ssh_host_ed25519_key
        modified:   config/ssh_host_ed25519_key.pub
        modified:   config/ssh_host_rsa_key
        modified:   config/ssh_host_rsa_key.pub

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        config/gitlab22.rb

no changes added to commit (use "git add" and/or "git commit -a")

Administrator@DESKTOP-U76UFCL MINGW64 /d/lanzhiwang_work/code/gitlab (master)
$


# 比较 config 目录中的数据后，只需要将 config/gitlab-secrets.json 和 config/gitlab.rb 文件转移到新机器上

# config/gitlab-secrets.json 文件完全不用修改

# config/gitlab.rb 文件要按照实际情况修改
# 这次只要修改选项 external_url 'http://10.1.36.45:9090'

# 将两个配置文件转移过来后执行下列命令：

docker exec -ti 8e873e0e915d  gitlab-ctl reconfigure


```

迁移数据

```bash

# 备份数据
gitlab-rake gitlab:backup:create

# 拷贝到新机器后的操作
chown -v git:git 1563178988_2019_07_15_11.1.4_gitlab_backup.tar

gitlab-rake gitlab:backup:restore BACKUP=1563178988_2019_07_15_11.1.4

note: 需要重建 authorized_keys 文件
This will rebuild an authorized_keys file.
You will lose any data stored in authorized_keys file.
Do you want to continue (yes/no)? yes


gitlab-ctl start

gitlab-rake gitlab:check SANITIZE=true

```
