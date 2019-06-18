## java

```bash
[root@git-new ~]# docker exec -ti 55a3e30bc08c bash
bash-4.4# java -version
openjdk version "1.8.0_151"
OpenJDK Runtime Environment (IcedTea 3.6.0) (Alpine 8.151.12-r0)
OpenJDK 64-Bit Server VM (build 25.151-b12, mixed mode)
bash-4.4# 


yum install java-1.8.0-openjdk-devel.x86_64

[root@git-new ~]# rpm -ql java-1.8.0-openjdk-devel.x86_64
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jaas-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jaas-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jaas.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jce-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jce-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jce.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jdbc-stdext-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jdbc-stdext-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jdbc-stdext-3.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jdbc-stdext.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-cos-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-cos-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-cos.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-ldap-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-ldap-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-ldap.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-rmi-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-rmi-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi-rmi.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jndi.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jsse-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jsse-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jsse.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/sasl-1.8.0.212.b04.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/sasl-1.8.0.jar
/usr/lib/jvm-exports/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/sasl.jar
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/appletviewer
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/clhsdb
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/extcheck
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/hsdb
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/idlj
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jar
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jarsigner
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/java
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/java-rmi.cgi
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/javac
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/javadoc
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/javah
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/javap
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jcmd
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jconsole
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jdb
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jdeps
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jhat
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jinfo
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jjs
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jmap
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jps
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jrunscript
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jsadebugd
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jstack
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jstat
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/jstatd
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/keytool
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/native2ascii
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/orbd
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/pack200
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/policytool
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/rmic
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/rmid
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/rmiregistry
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/schemagen
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/serialver
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/servertool
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/tnameserv
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/unpack200
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/wsgen
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/wsimport
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin/xjc
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/classfile_constants.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/jawt.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/jdwpTransport.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/jni.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/jvmti.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/jvmticmlr.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/linux
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/linux/jawt_md.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/include/linux/jni_md.h
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/amd64
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/amd64/jli
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/amd64/jli/libjli.so
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/amd64/libjawt.so
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/ct.sym
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/dt.jar
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/ir.idl
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/jconsole.jar
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/jexec
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/orb.idl
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/sa-jdi.jar
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/lib/tools.jar
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/tapset
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/tapset/hotspot-1.8.0.212.b04-0.el7_6.x86_64.stp
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/tapset/hotspot_gc-1.8.0.212.b04-0.el7_6.x86_64.stp
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/tapset/hotspot_jni-1.8.0.212.b04-0.el7_6.x86_64.stp
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/tapset/jstack-1.8.0.212.b04-0.el7_6.x86_64.stp
/usr/share/applications/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64-jconsole.desktop
/usr/share/doc/java-1.8.0-openjdk-devel-1.8.0.212.b04
/usr/share/doc/java-1.8.0-openjdk-devel-1.8.0.212.b04/ASSEMBLY_EXCEPTION
/usr/share/doc/java-1.8.0-openjdk-devel-1.8.0.212.b04/LICENSE
/usr/share/doc/java-1.8.0-openjdk-devel-1.8.0.212.b04/THIRD_PARTY_README
/usr/share/man/man1/appletviewer-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/extcheck-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/idlj-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jar-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jarsigner-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/javac-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/javadoc-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/javah-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/javap-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jcmd-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jconsole-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jdb-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jdeps-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jhat-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jinfo-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jmap-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jps-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jrunscript-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jsadebugd-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jstack-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jstat-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/jstatd-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/native2ascii-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/rmic-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/schemagen-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/serialver-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/wsgen-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/wsimport-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/man/man1/xjc-java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64.1.gz
/usr/share/systemtap
/usr/share/systemtap/tapset/x86_64
/usr/share/systemtap/tapset/x86_64/hotspot-1.8.0.212.b04-0.el7_6.x86_64.stp
/usr/share/systemtap/tapset/x86_64/hotspot_gc-1.8.0.212.b04-0.el7_6.x86_64.stp
/usr/share/systemtap/tapset/x86_64/hotspot_jni-1.8.0.212.b04-0.el7_6.x86_64.stp
/usr/share/systemtap/tapset/x86_64/jstack-1.8.0.212.b04-0.el7_6.x86_64.stp
[root@git-new ~]# 

export PATH=${PATH}:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/bin



ubuntu 
apt-get update
apt-get install openjdk-8-jdk





Alpine




jstack(查看线程)
jmap(查看内存)
jstat(性能分析)

top cpu排序

top -p -H 87726 shift + h 

[root@git-new ~]# printf "%x\n" 87837
1571d
[root@git-new ~]# 

jstack 87726
jstack 87726 | grep -A 30 "nid=0x + 1571d"





```