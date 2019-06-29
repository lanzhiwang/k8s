```
PS C:\k> .\start.ps1 -ManagementIP 10.1.36.50 -NetworkMode overlay  -ClusterCIDR 172.20.0.0/16 -ServiceCIDR 10.68.0.0/16 -KubeDnsServiceIP 10.68.0.2 -LogDir F:\k8s\kubernetes\node\bin\log
Creating Kubernetes directories
Downloading Windows Kubernetes scripts
File c:\k\hns.psm1 already exists.
File c:\k\Dockerfile already exists.
File c:\k\stop.ps1 already exists.
File c:\k\start-kubelet.ps1 already exists.
File c:\k\start-Kubeproxy.ps1 already exists.
Downloading Flannel binaries
File c:\k\flanneld.exe already exists.
Downloading CNI binaries
File c:\k\net-conf.json already exists.
File c:\k\cni\config\cni.conf already exists.
File c:\k\cni\flannel.exe already exists.
File c:\k\cni\host-local.exe already exists.
File c:\k\cni\win-overlay.exe already exists.
Copying Flannel setup files
警告: 模块“hns”中的某些导入命令的名称包含未批准的动词，这些动词可能导致这些命令名不易被发现。若要查找具有未批准的动词的命令，请使用 Verbose 参数再次运行 Import-Module 命令。有关批准的动词列表，请键入 Get-Verb。
Generated CNI Config [@{cniVersion=0.2.0; name=vxlan0; type=flannel; delegate=}]
Generated net-conf Config [@{Network=172.20.0.0/16; Backend=}]
Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the target machine actively refused it.
Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the target machine actively refused it.
waiting to discover node registration status
Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the target machine actively refused it.
waiting to discover node registration status
Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the target machine actively refused it.
waiting to discover node registration status
PS C:\k> 

错误分析：
不能连接 8080 端口，8080 端口是 kube-apiserver 启动的一个端口，如下所示，该端口只监听 127.0.0.1 网卡，需要修改 apiserver 配置，实践证明需要使用配置文件 C:\k\config ，在配置文件中使用证书

[root@k8s-master2 ssl]# netstat -tulnp | grep kube-apiserve
tcp        0      0 10.1.36.44:6443         0.0.0.0:*               LISTEN      76377/kube-apiserve 
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      76377/kube-apiserve 
[root@k8s-master2 ssl]# 

1、将根证书导入受信任站点
2、
[root@k8s-master1 .kube]# cat /root/.kube/config 
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUUtFd05yT0hNeER6QU5CZ05WQkFzVEJsTjVjM1JsYlRFVE1CRUdBMVVFCkF4TUthM1ZpWlhKdVpYUmxjekFlRncweE9UQTFNakF3TVRVNE1EQmFGdzB6TkRBMU1UWXdNVFU0TURCYU1Ha3gKQ3pBSkJnTlZCQVlUQWtOT01STXdFUVlEVlFRSUV3cG9kV0psYVhOb1pXNW5NUkV3RHdZRFZRUUhFd2gzZFdoaApibk5vYVRFTU1Bb0dBMVVFQ2hNRGF6aHpNUTh3RFFZRFZRUUxFd1pUZVhOMFpXMHhFekFSQmdOVkJBTVRDbXQxClltVnlibVYwWlhNd2dnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUURmVGw5Ri9sUzUKOUJIWDVxNnBQNWhwc0xSbnZzZ1RqZE5KNUZHMjRKem5CMGhZTDBSME96YlRBc0h4cEZ4SjRoaXRmTk9meG96OQpBZnpRMDMyN3RTellEb3pnNzBERzh3NWRZa3ZzNDlwVURiU3BKcW5ZdDJNYnZoOE1KRXc0UDkyaWk1dFpwK3A4CnZreExINjBwbTgydGFyTU5IRVhudFJLbVdVYUdkbnFYZnBKMUFSaEphc1o5MUVWaE83bkwxME0zVXNHQnRBY2sKVE9pY1JpMXR0OUNMaGkwMzdVNjhqV0YweVRtSng4WHNDd3EzeEQ2YVJ4RTFTRGRZY3VwYTJBRDMzdC9oSy9wWApza0o2Tk43dGdSR2pRSmRWeFJ0Uk81WEhrSkFyQml5eXFWRFVUUzNLVnZubUp2bnh5a1F0VkoyTVB0cHE2NFBXCi9KbEhRaEtUc3dtMUFnTUJBQUdqWmpCa01BNEdBMVVkRHdFQi93UUVBd0lCQmpBU0JnTlZIUk1CQWY4RUNEQUcKQVFIL0FnRUNNQjBHQTFVZERnUVdCQlF0bmFweDBjYWF2TGo4UUV0WlpNNlRuZmtjbURBZkJnTlZIU01FR0RBVwpnQlF0bmFweDBjYWF2TGo4UUV0WlpNNlRuZmtjbURBTkJna3Foa2lHOXcwQkFRc0ZBQU9DQVFFQTNZRUEyYTl3CnRNdGQrVERrNlVMT3FVckcrZUtUeER2MHIyaVF3MEJQK3cyQkJCL0ZjcVVGK1YrWjJueE0vWk94dUdmeWZXb0UKcXRvOVUwWUZkb0QvSmdHVkVLbWVXWkdObml2K091YTc2SFZ3V0FNNVA4TXhhamV1Z2FZQlRZc2pwVDB0cDlLTAp0NTZmb0hoeVZ3R1lRKzNMNU1xMGtoRFRaVkszRHYzR3lJaGR1cnZndERsNTdrQ1JuYjhMTmZiK2U1ODBRODVaCmFzZU5LYVdTcUVsQm9yaWo5SUZJdjh4SWY3QUFXaUViUXpKYjFOYWt5emdMcnYzNHJFbFhjR1NoOHk1RTNDVS8KQi9ZSXB2MGFERDBZcjJlMDUwVEJJZ1puNzU3b3FWc2FoMzJ4YXN5Q3M4eGc4c0xCdG93YnBQZG9yMHRiNU93bgo1bmpWT3lzYVB4VEs0QT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    server: https://10.1.36.43:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: admin
  name: kubernetes
current-context: kubernetes
kind: Config
preferences: {}
users:
- name: admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUQ1VENDQXMyZ0F3SUJBZ0lVTFRCcGZSQURvMFlmUHBWNWdRREthWmRDQ3Rrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUUtFd05yT0hNeER6QU5CZ05WQkFzVEJsTjVjM1JsYlRFVE1CRUdBMVVFCkF4TUthM1ZpWlhKdVpYUmxjekFlRncweE9UQTFNakF3TWpJME1EQmFGdzB5T1RBMU1UY3dNakkwTURCYU1HOHgKQ3pBSkJnTlZCQVlUQWtOT01STXdFUVlEVlFRSUV3cG9kV0psYVhOb1pXNW5NUkV3RHdZRFZRUUhFd2gzZFdoaApibk5vYVRFWE1CVUdBMVVFQ2hNT2MzbHpkR1Z0T20xaGMzUmxjbk14RHpBTkJnTlZCQXNUQmxONWMzUmxiVEVPCk1Bd0dBMVVFQXhNRllXUnRhVzR3Z2dFaU1BMEdDU3FHU0liM0RRRUJBUVVBQTRJQkR3QXdnZ0VLQW9JQkFRREEKWk01TytXUjg4dlJuMTU4a2VvTlJpU1FXMXBoNU5vTXdOUUFCYWFZY3dhOWlkcys5OUpzUGhyOVBIZ2NkOFZ1RgpDVVpNaFlpL2dSZjZ1OEFWazFyaHNKbXBBcEhSbjNJdjNQdnNpaHZFcnQ5VTVzNVZHYTExLy9JcFZSUnpIL2RKClJBN3R5ZmRGTDBDTXd1bGpkbGpGYmRJb05vSk9lY3lzaEZOdkRpbEtGSTJLQVZCNlZxSlZWcHpWMWZmbzM3YnkKRkVzSnNwQU9pYWtYZTNkLzNsNkRNSjFTdDFFbzlUekwyMnlUZmE5UmFRZS8wRllRMTlGdW5udVlrRjRBekNKYwoxZDFSUnVvK2laQU9qK2RscFpPMGYrYkFlelVQMHplVFlqbStKY0NhcE0wa09nM3VUd29NK2o2VmhWKythZUF6CjdpaDlLSGIvUG5WMXZEZ0N5eTZiQWdNQkFBR2pmekI5TUE0R0ExVWREd0VCL3dRRUF3SUZvREFkQmdOVkhTVUUKRmpBVUJnZ3JCZ0VGQlFjREFRWUlLd1lCQlFVSEF3SXdEQVlEVlIwVEFRSC9CQUl3QURBZEJnTlZIUTRFRmdRVQpwYXlndUtWeHZKbGdvWmZGdHNobVJIVjZ4WE13SHdZRFZSMGpCQmd3Rm9BVUxaMnFjZEhHbXJ5NC9FQkxXV1RPCms1MzVISmd3RFFZSktvWklodmNOQVFFTEJRQURnZ0VCQUZubmhoeityZC9LYm10anhYYjRSSHl0VVd1MmJKWW0KRVBoODUxcUNmbGQ2MERxSWU3T001bHFubUtrSElmeS8vVTMvenI1QnFpc1ZuVmZMRmFWeFRvM0VMSkR4VzdVWQpOdnNyUjdKeUtrVGNDamxhUlFlbzRaSmljaC9Gd1g4ZEpYdlk5czFGZ2ZIaTZicS9xSzBNZ0w2amU2K1p6anVOCklycWZjVVhSUEJJS2pzRFJHYjhFdlZzRmZ2SGpxMmlPMUFvSFN2SlA0eGNUS2I0ZWFJanNPaE8vZ244UDFwRFYKNHR3VUgxaUhkbFdFRHJkUXNUUHJrT2JTTE0yT1NLZ3M4RDRwQzgwVU1kUTFrVXJTK25iWU1IZElaTmg0MUtoMQpUc1VGS3pTRllETFdXZ0Q4eUpTejBGUEUxb1NFNVJxeGlldThWaUc4Y0ppbHhzVitHQjl2RHFRPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBd0dUT1R2bGtmUEwwWjllZkpIcURVWWtrRnRhWWVUYURNRFVBQVdtbUhNR3ZZbmJQCnZmU2JENGEvVHg0SEhmRmJoUWxHVElXSXY0RVgrcnZBRlpOYTRiQ1pxUUtSMFo5eUw5ejc3SW9ieEs3ZlZPYk8KVlJtdGRmL3lLVlVVY3gvM1NVUU83Y24zUlM5QWpNTHBZM1pZeFczU0tEYUNUbm5NcklSVGJ3NHBTaFNOaWdGUQplbGFpVlZhYzFkWDM2TisyOGhSTENiS1FEb21wRjN0M2Y5NWVnekNkVXJkUktQVTh5OXRzazMydlVXa0h2OUJXCkVOZlJicDU3bUpCZUFNd2lYTlhkVVVicVBvbVFEby9uWmFXVHRIL213SHMxRDlNM2sySTV2aVhBbXFUTkpEb04KN2s4S0RQbytsWVZmdm1uZ00rNG9mU2gyL3o1MWRidzRBc3N1bXdJREFRQUJBb0lCQVFDS3VpVnBITHN3dlo4dQpJWFJIUVcvZkl4dzZ1NUpHRk9DVHFpUE80UGMrVlFxNTNTSCt2cG53b0NEaVU2eWVFcU1EVXFTMkdMTjZJd08vCmNCSVpmSjlUalp1L0duTTZ5OVh5WFUzcVNjdXNEc3hLMUFLRHFuaEJWY1N2dVFGOTRkYlZwWlYrTU50enI1YkQKNk9lUktJenFEejR5Y051VTZvNkM5d2VTVkl2Qk5jQ09VV2dxZDNEbnl6Z3JhVXluU0hOR1BWZmZaR1E5NitoNwowcDhPTmJXSDRVajBpYXc1Uk5ZbHNUeXhzRXRBVk9XN3BBMmR1bFVxMzZER2hEYkxGRUJ3a090TXlkdkxTd0RnCkxZckZCOHA4VTJRTmdZYUFKdTUzUWg1S2d0Sk1JMVhkWmdLVWVXZFZ3SUNxSE9qRXpZTWpPaGVWcXR4bEtGaUkKZlFqNjUwZkJBb0dCQU9QMmtxVTJiVkQ3eVF1bmYwT0swd3h3R0cxQmgwSWI3QklkWkgvK2M5ZjhsbXIrMXNUYgp2QmFyVjI1U1QxaFd5dUpzQlhtWG44dXEwRVo1WDI5NU9lbHA4UkVQSVFiZnRXM1pRdWo2MkJ0aDVhcVFNWmRqCnllYTBYa0tIbURMTFo0MXovd0FFWW4xSGNHRVJ4aFZkVUxyMmwybnB3SUdlN3JvWkEvRGFwK1ozQW9HQkFOZ08KVkZQVXFmQlJ1dEFIZE1mMEJCMVJmQjFybmxrbzZ2VWNBY0k4OVgzVDdLcEJ2MWpCbjkwMzFjS0V0L1N2SHhhTAp4cWFOQmxkTXI0RVBqL0d5ZGEvTXlyc0ZxYmh2LzBhdWtmajhaK01zUW0zdnJ1QkdLV1RSRHE3OGVUUENDS3NlCnp5OW1vV0ZrK3o5Rm5QTnU0NTl6TGg4QlRJNjFHVnJNdUM3dVVxMzlBb0dCQUtQbnVON0RPR3crN1BuTkw4clAKZVJsN1M0VGExYmFwdnQzemRqdzFKdlBIOEJyMEtsV1dyREVjZHh1aVlOeGlZelBUZVVoSXhhTTVxTkRUR2RSYgp0RkRvVkdUd25NMkZjYnlPdHZZdXpjMDZZVmgybnNGOEJVSTBzNFZnV3dWQ2pLei9GdnpiS2pscmNSaktIOE5pCnVkWUQwVEJjMm9ZWVVRdExTek1VOUIzWEFvR0FPdHNrYzdYQ0dYcGFOcU5oVjdzTWgrUVR1SHdCcGU0MG0xTG0KMDhBQmJDYVlHUVZTRjk2Zkt3Y3p6d3FTaGpCU2VyVFhCN1h4SFVVQnBsblQ3NWFhNHFvYUsvcHQ4cFZuNkJ4VQpIWXk4ekREWlk5TmdReTQ1eG9JQXl3QnlEL3h5bWhNSmc3TWtrVUNPQlAxMHRRZm5NQitUVjlUbHd4Wm9jc2pECi85emlYdzBDZ1lFQXRDQk4zVlBIUGF4Njk5bHp2VVJtd0NrWjQzUGhJR3Z1aStmd01ZaUwrTHVlUDZnclVWVGoKNGU2TUtzM05ZTnRRR0FIeENvSlBoMVhBeVgvTFNLTENSV1RyL1p3dCtRVEY0YXdVbHBaYSswS1dGekVOcVZzdQpWT0l5N2M1R0s5cHBxZmlUQm50dUFyNWJETXo0WmJVUC9DcHZna25xTlhaNkJSaXVodkMyOUJJPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
[root@k8s-master1 .kube]# 


PS C:\k> .\kubectl.exe --kubeconfig=C:\k\config  get nodes
NAME              STATUS     ROLES    AGE   VERSION
10.1.36.46        Ready      <none>   38d   v1.14.0
10.1.36.47        Ready      <none>   33d   v1.14.0
10.1.36.48        Ready      <none>   32d   v1.14.0
10.1.36.49        Ready      <none>   31d   v1.14.0
k8s-win-worker1   NotReady   <none>   33m   v1.14.0
PS C:\k>






































kubectl 使用的证书
################
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://10.1.36.43:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: admin
  name: kubernetes
current-context: kubernetes
kind: Config
preferences: {}
users:
- name: admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUQ1VENDQXMyZ0F3SUJBZ0lVTFRCcGZSQURvMFlmUHBWNWdRREthWmRDQ3Rrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBd0dUT1R2bGtmUEwwWjllZkpIcURVWWtrRnRhWWVUYURNRFVBQVdtbUhNR3ZZbmJQCnZmU2JENGEvVHg0SEhmRmJoUWxHVElXSXY0RVgrcnZBRlpOYTRiQ1pxUUtSMFo5eUw5ejc3SW9ieEs3ZlZPYk8KVlJtdGRmL3lLVlVVY3gvM1NVUU



kubelet 使用的证书
################    
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR4akNDQXE2Z0F3SUJBZ0lVS2N0enNHZ2FXbkh5N3VWN2lUeHhyVm1tRHYwd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    server: https://10.1.36.43:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: system:node:10.1.36.50
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: system:node:10.1.36.50
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUVCRENDQXV5Z0F3SUJBZ0lVWkUwaFdiQnN0aC9BTFA3U0pQWEdFQzZ2OFA0d0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FURUxNQWtHQTFVRUJoTUNRMDR4RXpBUkJnTlZCQWdUQ21oMVltVnBjMmhsYm1jeEVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBdXhxalFsR3RhTGVIUzdYay9WSXNBTDk0Q2NnSW4wYXEvbDZzaUNkSTdraU0yRmE2ClBJRTFEZENRYUs2U3QvSUtWSWVEb29UVkg4UEJ6aGN0YWgweTY2KzJVQTRicWhjTm5va2hXNGdHMTYvTE1VRHgKanFsNms1ektCTXhxN2hkMHFWcm


PS C:\k> .\start.ps1 -ManagementIP 10.1.36.50 -NetworkMode overlay  -ClusterCIDR 172.20.0.0/16 -ServiceCIDR 10.68.0.0/16 -KubeDnsServiceIP 10.68.0.2 -LogDir F:\k8s\kubernetes\node\bin\log
Creating Kubernetes directories
Downloading Windows Kubernetes scripts
File c:\k\hns.psm1 already exists.
File c:\k\Dockerfile already exists.
File c:\k\stop.ps1 already exists.
File c:\k\start-kubelet.ps1 already exists.
File c:\k\start-Kubeproxy.ps1 already exists.
Downloading Flannel binaries
File c:\k\flanneld.exe already exists.
Downloading CNI binaries
File c:\k\net-conf.json already exists.
File c:\k\cni\config\cni.conf already exists.
File c:\k\cni\flannel.exe already exists.
File c:\k\cni\host-local.exe already exists.
File c:\k\cni\win-overlay.exe already exists.
Copying Flannel setup files
警告: 模块“hns”中的某些导入命令的名称包含未批准的动词，这些动词可能导致这些命令名不易被发现。若要查找具有未批准的动词的命令，请使用 Verbose 参数再次运行 Import-Module 命令。有关批准的动词列表，请键入 Get-Verb。
Generated CNI Config [@{cniVersion=0.2.0; name=vxlan0; type=flannel; delegate=}]
Generated net-conf Config [@{Network=172.20.0.0/16; Backend=}]
error: Error loading config file "c:\k\config": v1.Config.Contexts: []v1.NamedContext: Clusters: []v1.NamedCluster: v1.NamedCluster.Name: Cluster: v1.Cluster.Server: CertificateAuthorityData: decode base64: illegal base64 data at input byte 240, error found in #10 byte of ...|2dZRFZRUU","server":|..., bigger context ...|EVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU","server":"https://10.1.36.43:6443"},"name":"kuber|...
error: Error loading config file "c:\k\config": v1.Config.Contexts: []v1.NamedContext: Clusters: []v1.NamedCluster: v1.NamedCluster.Name: Cluster: v1.Cluster.Server: CertificateAuthorityData: decode base64: illegal base64 data at input byte 240, error found in #10 byte of ...|2dZRFZRUU","server":|..., bigger context ...|EVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU","server":"https://10.1.36.43:6443"},"name":"kuber|...
waiting to discover node registration status
error: Error loading config file "c:\k\config": v1.Config.Contexts: []v1.NamedContext: Clusters: []v1.NamedCluster: v1.NamedCluster.Name: Cluster: v1.Cluster.Server: CertificateAuthorityData: decode base64: illegal base64 data at input byte 240, error found in #10 byte of ...|2dZRFZRUU","server":|..., bigger context ...|EVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU","server":"https://10.1.36.43:6443"},"name":"kuber|...
waiting to discover node registration status
error: Error loading config file "c:\k\config": v1.Config.Contexts: []v1.NamedContext: Clusters: []v1.NamedCluster: v1.NamedCluster.Name: Cluster: v1.Cluster.Server: CertificateAuthorityData: decode base64: illegal base64 data at input byte 240, error found in #10 byte of ...|2dZRFZRUU","server":|..., bigger context ...|EVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU","server":"https://10.1.36.43:6443"},"name":"kuber|...
waiting to discover node registration status
error: Error loading config file "c:\k\config": v1.Config.Contexts: []v1.NamedContext: Clusters: []v1.NamedCluster: v1.NamedCluster.Name: Cluster: v1.Cluster.Server: CertificateAuthorityData: decode base64: illegal base64 data at input byte 240, error found in #10 byte of ...|2dZRFZRUU","server":|..., bigger context ...|EVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU","server":"https://10.1.36.43:6443"},"name":"kuber|...
waiting to discover node registration status
error: Error loading config file "c:\k\config": v1.Config.Contexts: []v1.NamedContext: Clusters: []v1.NamedCluster: v1.NamedCluster.Name: Cluster: v1.Cluster.Server: CertificateAuthorityData: decode base64: illegal base64 data at input byte 240, error found in #10 byte of ...|2dZRFZRUU","server":|..., bigger context ...|EVUQVBCZ05WQkFjVApDSGQxYUdGdWMyaHBNUXd3Q2dZRFZRUU","server":"https://10.1.36.43:6443"},"name":"kuber|...
waiting to discover node registration status
PS C:\k>



http://pkg.cfssl.org/
cfssl_windows-amd64.exe
cfssljson_windows-amd64.exe

ca.pem
ca-key.pem
ca-config.json
admin-csr.json

PS C:\k\ssl> .\cfssl_windows-amd64.exe gencert -ca=.\ca.pem -ca-key=.\ca-key.pem -config=.\ca-config.json -profile=kubernetes admin-csr.json
invalid character '-' in numeric literal
PS C:\k\ssl>


PS C:\k\ssl> dir


    目录: C:\k\ssl


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        2019/6/29      6:09            233 admin_csr.json
-a----        2019/6/29      6:09           1371 ca.pem
-a----        2019/6/29      6:11            292 ca_config.json
-a----        2019/6/29      6:12           1700 ca_key.pem
-a----        2019/6/29      6:01        2375680 cfssljson_windows-amd64.exe
-a----        2019/6/29      6:01       10416128 cfssl_windows-amd64.exe


PS C:\k\ssl> .\cfssl_windows-amd64.exe gencert -ca=.\ca.pem -ca-key=.\ca_key.pem -config=.\ca_config.json -profile=kubernetes admin_csr.json
invalid character '-' in numeric literal
PS C:\k\ssl>











# 准备 kubelet 证书签名请求，以 10.1.36.50 为例
[root@k8s-linux-worker1 ssl]# vim ./kubelet-csr.json 
[root@k8s-linux-worker1 ssl]# cat ./kubelet-csr.json 
{
  "CN": "system:node:10.1.36.50",
  "hosts": [
    "127.0.0.1",
    "10.1.36.50"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "hubeisheng",
      "L": "wuhanshi",
      "O": "system:nodes",
      "OU": "System"
    }
  ]
}

http://pkg.cfssl.org/
cfssl_windows-amd64.exe
cfssljson_windows-amd64.exe


./cfssl_windows-amd64.exe gencert -ca=./ca.pem -ca-key=./ca-key.pem -config=./ca-config.json -profile=kubernetes admin-csr.json | ./cfssljson_windows-amd64.exe -bare admin







```