# Resource Limits

* [Understanding resource limits in kubernetes: memory](https://medium.com/@betz.mark/understanding-resource-limits-in-kubernetes-memory-6b41e9a955f9)
* [中文翻译](https://mp.weixin.qq.com/s/j2FfqUHSRTzczNcfPuwRQw)

```bash
$ kubectl run limit-test --image=busybox --command -- /bin/sh -c "while true; do sleep 2; done"
deployment.apps "limit-test" created

$ kubectl get pods limit-test-7cff9996fc-zpjps -o=jsonpath='{.spec.containers[0].resources}'
map[]

$ docker ps | grep busy | cut -d' ' -f1
5c3af3101afb

$ docker inspect 5c3af3101afb -f "{{.HostConfig.Memory}}"
0

$ ps ax | grep /bin/sh
   9513 ?        Ss     0:00 /bin/sh -c while true; do sleep 2; done

$ sudo cat /proc/9513/cgroup
...
6:memory:/kubepods/burstable/podfbc202d3-da21-11e8-ab5e-42010a80014b/0a1b22ec1361a97c3511db37a4bae932d41b22264e5b97611748f8b662312574

$ ls -l /sys/fs/cgroup/memory/kubepods/burstable/podfbc202d3-da21-11e8-ab5e-42010a80014b/0a1b22ec1361a97c3511db37a4bae932d41b22264e5b97611748f8b662312574
...
-rw-r--r-- 1 root root 0 Oct 27 19:53 memory.limit_in_bytes
-rw-r--r-- 1 root root 0 Oct 27 19:53 memory.soft_limit_in_bytes

$ sudo cat /sys/fs/cgroup/memory/kubepods/burstable/podfbc202d3-da21-11e8-ab5e-42010a80014b/0a1b22ec1361a97c3511db37a4bae932d41b22264e5b97611748f8b662312574/memory.limit_in_bytes
9223372036854771712

##########################################################

$ kubectl run limit-test --image=busybox --limits "memory=100Mi" --command -- /bin/sh -c "while true; do sleep 2; done"
deployment.apps "limit-test" created

$ kubectl get pods limit-test-5f5c7dc87d-8qtdx -o=jsonpath='{.spec.containers[0].resources}'
map[limits:map[memory:100Mi] requests:map[memory:100Mi]]

$ docker ps | grep busy | cut -d' ' -f1
8fec6c7b6119

$ docker inspect 8fec6c7b6119 --format '{{.HostConfig.Memory}}'
104857600

$ ps ax | grep /bin/sh
   29532 ?      Ss     0:00 /bin/sh -c while true; do sleep 2; done

$ sudo cat /proc/29532/cgroup
...
6:memory:/kubepods/burstable/pod88f89108-daf7-11e8-b1e1-42010a800070/8fec6c7b61190e74cd9f88286181dd5fa3bbf9cf33c947574eb61462bc254d11

$ sudo cat /sys/fs/cgroup/memory/kubepods/burstable/pod88f89108-daf7-11e8-b1e1-42010a800070/8fec6c7b61190e74cd9f88286181dd5fa3bbf9cf33c947574eb61462bc254d11/memory.limit_in_bytes
104857600

$ sudo cat /sys/fs/cgroup/memory/kubepods/burstable/pod88f89108-daf7-11e8-b1e1-42010a800070/8fec6c7b61190e74cd9f88286181dd5fa3bbf9cf33c947574eb61462bc254d11/memory.soft_limit_in_bytes
9223372036854771712

```

* [Understanding resource limits in kubernetes: cpu time](https://medium.com/@betz.mark/understanding-resource-limits-in-kubernetes-cpu-time-9eff74d3161b)
* [中文翻译](https://www.yangcs.net/posts/understanding-resource-limits-in-kubernetes-cpu-time/)

```bash
$ kubectl run limit-test --image=busybox --requests "cpu=50m" --command -- /bin/sh -c "while true; do sleep 2; done"
deployment.apps "limit-test" created

$ kubectl get pods limit-test-5b4c495556-p2xkr -o=jsonpath='{.spec.containers[0].resources}'
map[requests:map[cpu:50m]]

$ docker ps | grep busy | cut -d' ' -f1
f2321226620e

$ docker inspect f2321226620e --format '{{.HostConfig.CpuShares}}'
51

$ ps ax | grep /bin/sh
   60554 ?      Ss     0:00 /bin/sh -c while true; do sleep 2; done

$ sudo cat /proc/60554/cgroup
...
4:cpu,cpuacct:/kubepods/burstable/pode12b33b1-db07-11e8-b1e1-42010a800070/3be263e7a8372b12d2f8f8f9b4251f110b79c2a3bb9e6857b2f1473e640e8e75

$ ls -l /sys/fs/cgroup/cpu,cpuacct/kubepods/burstable/pode12b33b1-db07-11e8-b1e1-42010a800070/3be263e7a8372b12d2f8f8f9b4251f110b79c2a3bb9e6857b2f1473e640e8e75
total 0
drwxr-xr-x 2 root root 0 Oct 28 23:19 .
drwxr-xr-x 4 root root 0 Oct 28 23:19 ..
...
-rw-r--r-- 1 root root 0 Oct 28 23:19 cpu.shares

$ sudo cat /sys/fs/cgroup/cpu,cpuacct/kubepods/burstable/podb5c03ddf-db10-11e8-b1e1-42010a800070/64b5f1b636dafe6635ddd321c5b36854a8add51931c7117025a694281fb11444/cpu.shares
51

##########################################################

$ kubectl run limit-test --image=busybox --requests "cpu=50m" --limits "cpu=100m" --command -- /bin/sh -c "while true; do
sleep 2; done"
deployment.apps "limit-test" created

$ kubectl get pods limit-test-5b4fb64549-qpd4n -o=jsonpath='{.spec.containers[0].resources}'
map[limits:map[cpu:100m] requests:map[cpu:50m]]

$ docker ps | grep busy | cut -d' ' -f1
f2321226620e

$ docker inspect 472abbce32a5 --format '{{.HostConfig.CpuShares}} {{.HostConfig.CpuQuota}} {{.HostConfig.CpuPeriod}}'
51 10000 100000

$ sudo cat /sys/fs/cgroup/cpu,cpuacct/kubepods/burstable/pod2f1b50b6-db13-11e8-b1e1-42010a800070/f0845c65c3073e0b7b0b95ce0c1eb27f69d12b1fe2382b50096c4b59e78cdf71/cpu.cfs_period_us
100000

$ sudo cat /sys/fs/cgroup/cpu,cpuacct/kubepods/burstable/pod2f1b50b6-db13-11e8-b1e1-42010a800070/f0845c65c3073e0b7b0b95ce0c1eb27f69d12b1fe2382b50096c4b59e78cdf71/cpu.cfs_quota_us
10000

```
