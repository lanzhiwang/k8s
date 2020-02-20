### mercurial

```bash
[root@lanzhiwang-centos7 ~]# rpm -ql mercurial-2.6.2-8.el7_4.x86_64
/etc/bash_completion.d
/etc/bash_completion.d/mercurial.sh
/etc/mercurial
/etc/mercurial/hgrc.d
/etc/mercurial/hgrc.d/certs.rc
/etc/mercurial/hgrc.d/mergetools.rc
/usr/bin/hg
/usr/bin/hg-ssh
/usr/lib64/python2.7/site-packages/hgext
[root@lanzhiwang-centos7 ~]# 

/usr/share/doc/mercurial-2.6.2/hgweb.cgi
/usr/share/doc/mercurial-2.6.2/hgweb.fcgi


[root@lanzhiwang-centos7 hg]# cat /usr/share/doc/mercurial-2.6.2/sample.hgrc
### --- User interface

[ui]

### show changed files and be a bit more verbose if True

# verbose = True

### username data to appear in comits
### it usually takes the form: Joe User <joe.user@host.com>

# username = Joe User <j.user@example.com>

### --- Extensions

[extensions]

### each extension has its own 'extension_name=path' line
### the default python library path is used when path is left blank
### the hgext dir is used when 'hgext.extension_name=' is written

### acl - Access control lists
### hg help acl

# hgext.acl =

### bisect - binary search changesets to detect bugs
### hg help bisect

# hgext.hbisect =

### bugzilla - update bugzilla bugs when changesets mention them
### hg help bugzilla

# hgext.bugzilla =

### extdiff - Use external diff application instead of builtin one

# hgext.extdiff =

### gpg - GPG checks and signing
### hg help gpg

# hgext.gpg =

### graphlog - ASCII graph log
### hg help glog

# hgext.graphlog =

### hgk - GUI repository browser
### hg help view

# hgext.hgk =

### mq - Mercurial patch queues
### hg help mq

# hgext.mq =

### notify - Template driven e-mail notifications
### hg help notify

# hgext.notify =

### patchbomb - send changesets as a series of patch emails
### hg help email

# hgext.patchbomb =

### churn - create a graph showing who changed the most lines
### hg help churn

# hgext.churn = /home/user/hg/hg/contrib/churn.py

### eol - automatic management of line endings

# hgext.eol =

### --- hgk additional configuration

[hgk]

### set executable path

# path = /home/user/hg/hg/contrib/hgk

### --- Hook to Mercurial actions - See hgrc man page for avaliable hooks

[hooks]

### Example notify hooks (load hgext.notify extension before use)

# incoming.notify = python:hgext.notify.hook
# changegroup.notify = python:hgext.notify.hook

### Email configuration for the notify and patchbomb extensions

[email]

### Your email address

# from = user@example.com

### Method to send email - smtp or /usr/sbin/sendmail or other program name

# method = smtp

### smtp server to send email to

[smtp]

# host = mail
# port = 25
# tls = false
# username = user
# password = blivet
# local_hostname = myhost

### --- Email notification hook for server

[notify]
### multiple sources can be specified as a whitespace or comma separated list

# sources = serve push pull bundle

### set this to False when you're ready for mail to start sending

# test = True

### path to config file with names of subscribers

# config = /path/to/subscription/file
[root@lanzhiwang-centos7 hg]# 

[root@lanzhiwang-centos7 hg]# cp /usr/share/doc/mercurial-2.6.2/sample.hgrc /root/.hgrc
[root@lanzhiwang-centos7 hg]# 
[root@lanzhiwang-centos7 hg]# vim /root/.hgrc
[root@lanzhiwang-centos7 hg]# cat /root/.hgrc
### --- User interface

[ui]

### show changed files and be a bit more verbose if True

verbose = True

### username data to appear in comits
### it usually takes the form: Joe User <joe.user@host.com>

username = huzhi <huz01@mingyuanyun.com>

### --- Extensions

[extensions]

### each extension has its own 'extension_name=path' line
### the default python library path is used when path is left blank
### the hgext dir is used when 'hgext.extension_name=' is written

### acl - Access control lists
### hg help acl

# hgext.acl =

### bisect - binary search changesets to detect bugs
### hg help bisect

# hgext.hbisect =

### bugzilla - update bugzilla bugs when changesets mention them
### hg help bugzilla

# hgext.bugzilla =

### extdiff - Use external diff application instead of builtin one

# hgext.extdiff =

### gpg - GPG checks and signing
### hg help gpg

# hgext.gpg =

### graphlog - ASCII graph log
### hg help glog

# hgext.graphlog =

### hgk - GUI repository browser
### hg help view

# hgext.hgk =

### mq - Mercurial patch queues
### hg help mq

# hgext.mq =

### notify - Template driven e-mail notifications
### hg help notify

# hgext.notify =

### patchbomb - send changesets as a series of patch emails
### hg help email

# hgext.patchbomb =

### churn - create a graph showing who changed the most lines
### hg help churn

# hgext.churn = /home/user/hg/hg/contrib/churn.py

### eol - automatic management of line endings

# hgext.eol =

### --- hgk additional configuration

[hgk]

### set executable path

# path = /home/user/hg/hg/contrib/hgk

### --- Hook to Mercurial actions - See hgrc man page for avaliable hooks

[hooks]

### Example notify hooks (load hgext.notify extension before use)

# incoming.notify = python:hgext.notify.hook
# changegroup.notify = python:hgext.notify.hook

### Email configuration for the notify and patchbomb extensions

[email]

### Your email address

# from = user@example.com

### Method to send email - smtp or /usr/sbin/sendmail or other program name

# method = smtp

### smtp server to send email to

[smtp]

# host = mail
# port = 25
# tls = false
# username = user
# password = blivet
# local_hostname = myhost

### --- Email notification hook for server

[notify]
### multiple sources can be specified as a whitespace or comma separated list

# sources = serve push pull bundle

### set this to False when you're ready for mail to start sending

# test = True

### path to config file with names of subscribers

# config = /path/to/subscription/file
[root@lanzhiwang-centos7 hg]# 


[root@lanzhiwang-centos7 hg]# pwd
/root/work/hg
[root@lanzhiwang-centos7 hg]# ll -a
total 4
drwxr-xr-x   2 root root    6 Jun 12 12:48 .
drwxr-xr-x. 13 root root 4096 Jun 12 12:48 ..
[root@lanzhiwang-centos7 hg]# hg init
[root@lanzhiwang-centos7 hg]# echo "hello, mercurial" > sample.txt
[root@lanzhiwang-centos7 hg]# ll -a
total 8
drwxr-xr-x   3 root root   35 Jun 12 13:23 .
drwxr-xr-x. 13 root root 4096 Jun 12 12:48 ..
drwxr-xr-x   3 root root   56 Jun 12 13:23 .hg
-rw-r--r--   1 root root   17 Jun 12 13:23 sample.txt
[root@lanzhiwang-centos7 hg]# hg add 
adding sample.txt
[root@lanzhiwang-centos7 hg]# hg ci
sample.txt
committed changeset 0:8f4670cd1ae5
[root@lanzhiwang-centos7 hg]# hg st
[root@lanzhiwang-centos7 hg]# 

[root@lanzhiwang-centos7 hg]# hg serve -p 8002 
listening at http://lanzhiwang-centos7:8002/ (bound to *:8002)
127.0.0.1 - - [12/Jun/2019 13:26:36] "GET /?cmd=capabilities HTTP/1.1" 200 -
127.0.0.1 - - [12/Jun/2019 13:26:59] "GET /?cmd=capabilities HTTP/1.1" 200 -
127.0.0.1 - - [12/Jun/2019 13:26:59] "GET /?cmd=batch HTTP/1.1" 200 - x-hgarg-1:cmds=heads+%3Bknown+nodes%3D
1 changesets found
127.0.0.1 - - [12/Jun/2019 13:26:59] "GET /?cmd=getbundle HTTP/1.1" 200 - x-hgarg-1:common=0000000000000000000000000000000000000000&heads=8f4670cd1ae5bfccc57f84d4362732aeb16a07d3
127.0.0.1 - - [12/Jun/2019 13:26:59] "GET /?cmd=listkeys HTTP/1.1" 200 - x-hgarg-1:namespace=phases
127.0.0.1 - - [12/Jun/2019 13:26:59] "GET /?cmd=listkeys HTTP/1.1" 200 - x-hgarg-1:namespace=bookmarks
10.5.106.11 - - [12/Jun/2019 13:29:14] "GET / HTTP/1.1" 200 -
10.5.106.11 - - [12/Jun/2019 13:29:14] "GET /static/mercurial.js HTTP/1.1" 200 -
10.5.106.11 - - [12/Jun/2019 13:29:14] "GET /static/feed-icon-14x14.png HTTP/1.1" 200 -
10.5.106.11 - - [12/Jun/2019 13:29:14] "GET /static/style-paper.css HTTP/1.1" 200 -
10.5.106.11 - - [12/Jun/2019 13:29:14] "GET /static/hglogo.png HTTP/1.1" 200 -
10.5.106.11 - - [12/Jun/2019 13:29:14] "GET /static/hgicon.png HTTP/1.1" 200 -

http://10.5.106.26:8002/



[root@lanzhiwang-centos7 ~]# mkdir test
[root@lanzhiwang-centos7 ~]# cd test
[root@lanzhiwang-centos7 test]# hg clone http://localhost:8002/
destination directory: .
requesting all changes
adding changesets
adding manifests
adding file changes
added 1 changesets with 1 changes to 1 files
updating to branch default
resolving manifests
getting sample.txt
1 files updated, 0 files merged, 0 files removed, 0 files unresolved

[root@lanzhiwang-centos7 test]# ll -a
total 8
drwxr-xr-x  3 root root   35 Jun 12 13:26 .
dr-xr-x---. 7 root root 4096 Jun 12 13:26 ..
drwxr-xr-x  4 root root  190 Jun 12 13:26 .hg
-rw-r--r--  1 root root   17 Jun 12 13:26 sample.txt
[root@lanzhiwang-centos7 test]# 
[root@lanzhiwang-centos7 test]# cat .hg/hgrc 
[paths]
default = http://localhost:8002/
[root@lanzhiwang-centos7 test]# 

[root@lanzhiwang-centos7 test]# cat .hg/hgrc 
[paths]
default = http://localhost:8002/
[root@lanzhiwang-centos7 test]# 
[root@lanzhiwang-centos7 test]# 
[root@lanzhiwang-centos7 test]# 
[root@lanzhiwang-centos7 test]# ll -a
total 8
drwxr-xr-x  3 root root   35 Jun 12 13:26 .
dr-xr-x---. 7 root root 4096 Jun 12 13:26 ..
drwxr-xr-x  4 root root  190 Jun 12 13:26 .hg
-rw-r--r--  1 root root   17 Jun 12 13:26 sample.txt
[root@lanzhiwang-centos7 test]# 
[root@lanzhiwang-centos7 test]# 
[root@lanzhiwang-centos7 test]# echo "qwe" > sample2.txt 
[root@lanzhiwang-centos7 test]# hg status
? sample2.txt
[root@lanzhiwang-centos7 test]# hg add
adding sample2.txt
[root@lanzhiwang-centos7 test]# hg status
A sample2.txt
[root@lanzhiwang-centos7 test]# hg ci
sample2.txt
committed changeset 1:ff5c983488f7
[root@lanzhiwang-centos7 test]# hg status
[root@lanzhiwang-centos7 test]# hg push 
pushing to http://localhost:8002/
searching for changes
1 changesets found
abort: HTTP Error 403: ssl required
[root@lanzhiwang-centos7 test]# vim .hg/hgrc 
[root@lanzhiwang-centos7 test]# hg push 
pushing to http://localhost:8002/
searching for changes
1 changesets found
abort: HTTP Error 403: ssl required
[root@lanzhiwang-centos7 test]# vim .hg/hgrc 
[root@lanzhiwang-centos7 test]# hg push 
pushing to http://localhost:8002/
searching for changes
1 changesets found
abort: HTTP Error 403: ssl required
[root@lanzhiwang-centos7 test]# hg push 
pushing to http://localhost:8002/
searching for changes
1 changesets found
abort: authorization failed
[root@lanzhiwang-centos7 test]# 



[root@lanzhiwang-centos7 ~]# groupadd huzhi
[root@lanzhiwang-centos7 ~]# useradd -g huzhi huzhi
[root@lanzhiwang-centos7 huzhi]# passwd huzhi
qwerty!@#









```