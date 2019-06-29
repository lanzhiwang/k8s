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
Node k8s-win-worker1 already registered
警告: 模块“hns”中的某些导入命令的名称包含未批准的动词，这些动词可能导致这些命令名不易被发现。若要查找具有未批准的动词的命令，请使用 Verbose 参数再次运行 Import-Module 命令。有关批准的动词列表，请键入 Get-Verb。
详细信息: Invoke-HNSRequest Method[GET] Path[/networks] Data[]
详细信息: Result :
{"Output":[{"ActivityId":"84473089-EDC9-436D-A1E1-3A7882850FD5","AdditionalParams":{},"CurrentEndpointCount":0,"DNSServerCompartment":3,"DrMacAddress":"00-15-5D-BB-6E-B1","Extensions":[{"Id":"E7C3B2F0-F3C5-48DF-AF2B-10FED6D72E7A","IsEnabled":false,"Name":"Microsoft
Windows 筛选平台"},{"Id":"E9B59CFA-2BE1-4B21-828F-B6FBDBDDC017","IsEnabled":true,"Name":"Microsoft Azure VFP Switch Extension"},{"Id":"EA24CD6C-D17A-4348-9190-09F0D5BE83DD","IsEnabled":true,"Name":"Microsoft NDIS
捕获"}],"Flags":0,"Health":{"LastErrorCode":0,"LastUpdateTime":132062690972642312},"ID":"9B219D6E-6847-43FC-8258-81DB4B63C09C","IPv6":false,"LayeredOn":"395B983F-DCC7-4E77-BF04-F01084CFC7DD","MacPools":[{"EndMacAddress":"00-15-5D-69-3F-FF","StartMacAddress":"00-15-5D-69
-30-00"}],"ManagementIP":"10.1.36.50","MaxConcurrentEndpoints":0,"Name":"External","Policies":[],"Resources":{"AdditionalParams":{},"AllocationOrder":0,"Allocators":[{"AdditionalParams":{},"AllocationOrder":0,"Health":{"LastErrorCode":0,"LastUpdateTime":1320626909699861
14},"ID":"2D72E7C0-9E9D-4A01-8057-66E7938D0EE0","IsPolicy":false,"Isolation_0":9999,"PortId":"81C0D794-C201-4707-9D12-F1AF435C1916","RDID":"9B219D6E-6847-43FC-8258-81DB4B63C09C","State":3,"SwitchId":"30081EA2-DE0E-4771-82BF-3FDBE9AA31BB","Tag":"RDID"}],"Health":{"LastEr
rorCode":0,"LastUpdateTime":132062690969986114},"ID":"84473089-EDC9-436D-A1E1-3A7882850FD5","PortOperationTime":0,"State":1,"SwitchOperationTime":0,"VfpOperationTime":0,"parentId":"325555C6-D065-4A90-A92A-DD7A5EED5B9B"},"State":1,"Subnets":[{"AdditionalParams":{},"Addre
ssPrefix":"192.168.255.0/30","GatewayAddress":"192.168.255.1","Health":{"LastErrorCode":0,"LastUpdateTime":132062690972642312},"ID":"A8D5A7AB-DD0D-4A01-8E37-10681D2A494A","ObjectType":5,"Policies":[{"Type":"VSID","VSID":9999}],"State":0}],"TotalEndpoints":0,"Type":"over
lay","Version":38654705666},{"ActivityId":"C9CAE6EF-217C-44D1-8942-56B09EB89577","AdditionalParams":{},"CurrentEndpointCount":0,"Extensions":[{"Id":"E7C3B2F0-F3C5-48DF-AF2B-10FED6D72E7A","IsEnabled":false,"Name":"Microsoft Windows
筛选平台"},{"Id":"E9B59CFA-2BE1-4B21-828F-B6FBDBDDC017","IsEnabled":false,"Name":"Microsoft Azure VFP Switch Extension"},{"Id":"EA24CD6C-D17A-4348-9190-09F0D5BE83DD","IsEnabled":true,"Name":"Microsoft NDIS
捕获"}],"Flags":0,"Health":{"AddressNotificationMissedCount":0,"AddressNotificationSequenceNumber":0,"InterfaceNotificationMissedCount":0,"InterfaceNotificationSequenceNumber":0,"LastErrorCode":0,"LastUpdateTime":132062691024261116,"RouteNotificationMissedCount":0,"Rout
eNotificationSequenceNumber":0},"ID":"B4E14E41-5EE4-441A-9675-138F88C43DB0","IPv6":false,"LayeredOn":"1D68A2E3-C9B1-40DC-88BC-C215F750B048","MacPools":[{"EndMacAddress":"00-15-5D-4F-8F-FF","StartMacAddress":"00-15-5D-4F-80-00"}],"MaxConcurrentEndpoints":0,"Name":"nat","
NatName":"ICSBEDB5686-6B22-44B5-A3AF-385BD261F365","Policies":[],"Resources":{"AdditionalParams":{},"AllocationOrder":2,"Allocators":[{"AdapterNetCfgInstanceId":"{BEDB5686-6B22-44B5-A3AF-385BD261F365}","AdditionalParams":{},"AllocationOrder":0,"CompartmendId":0,"Connect
ed":true,"DevicelessNic":false,"EndpointNicGuid":"58D5547C-7040-4BD3-ABB6-E1EE878E6CAD","EndpointPortGuid":"AB26FE6E-B628-4E6B-AC8A-56824F0B44DF","Health":{"LastErrorCode":0,"LastUpdateTime":132062691026403111},"Hidden":false,"ID":"88AE1A7A-77BD-42DF-931B-F7F219C13F9A",
"InterfaceGuid":"BEDB5686-6B22-44B5-A3AF-385BD261F365","IsPolicy":false,"IsolationId":0,"MTU":1450,"MacAddress":"00-15-5D-4F-87-08","ManagementPort":true,"NicFriendlyName":"nat","PreferredPortFriendlyName":"Container NIC
88ae1a7a","State":3,"SwitchId":"AEBE7EB6-3486-43DF-BF4D-431CF2615513","Tag":"Host
Vnic","WaitForIpv6Interface":false,"nonPersistentPort":false},{"AdditionalParams":{},"AllocationOrder":1,"Dhcp":false,"Dns":false,"ExternalInterfaceConstraint":0,"Health":{"DHCPState":1,"DNSState":1,"ICSState":2,"LastErrorCode":0,"LastUpdateTime":132062691028748165},"IC
SFlags":0,"ID":"C015E1CB-3FDF-46A8-BCEF-3FE7AC53B831","IsPolicy":false,"Prefix":20,"PrivateInterfaceGUID":"BEDB5686-6B22-44B5-A3AF-385BD261F365","State":3,"SubnetIPAddress":"172.25.192.0","Tag":"ICS"}],"Health":{"LastErrorCode":0,"LastUpdateTime":132062691026403111},"ID
":"C9CAE6EF-217C-44D1-8942-56B09EB89577","PortOperationTime":0,"State":1,"SwitchOperationTime":0,"VfpOperationTime":0,"parentId":"630083EE-297A-445E-82F1-2B4950A1F129"},"State":1,"Subnets":[{"AdditionalParams":{},"AddressPrefix":"172.25.192.0/20","GatewayAddress":"172.2
5.192.1","Health":{"LastErrorCode":0,"LastUpdateTime":132062691026403111},"ID":"9472AD80-BCEE-440C-8ADB-7458C95532EA","Policies":[],"State":0}],"TotalEndpoints":0,"Type":"nat","Version":38654705666}],"Success":true}
Waiting for the Network to be created
I0629 08:09:11.421046    1256 main.go:450] Searching for interface using 10.1.36.50
I0629 08:09:11.681436    1256 main.go:210] Could not find valid interface matching 10.1.36.50: error looking up interface 10.1.36.50: no index found for interface ""
E0629 08:09:11.681436    1256 main.go:234] Failed to find interface to use that matches the interfaces and/or regexes provided
详细信息: Invoke-HNSRequest Method[GET] Path[/networks] Data[]
详细信息: Result :
{"Output":[{"ActivityId":"84473089-EDC9-436D-A1E1-3A7882850FD5","AdditionalParams":{},"CurrentEndpointCount":0,"DNSServerCompartment":3,"DrMacAddress":"00-15-5D-BB-6E-B1","Extensions":[{"Id":"E7C3B2F0-F3C5-48DF-AF2B-10FED6D72E7A","IsEnabled":false,"Name":"Microsoft
Windows 筛选平台"},{"Id":"E9B59CFA-2BE1-4B21-828F-B6FBDBDDC017","IsEnabled":true,"Name":"Microsoft Azure VFP Switch Extension"},{"Id":"EA24CD6C-D17A-4348-9190-09F0D5BE83DD","IsEnabled":true,"Name":"Microsoft NDIS
捕获"}],"Flags":0,"Health":{"LastErrorCode":0,"LastUpdateTime":132062690972642312},"ID":"9B219D6E-6847-43FC-8258-81DB4B63C09C","IPv6":false,"LayeredOn":"395B983F-DCC7-4E77-BF04-F01084CFC7DD","MacPools":[{"EndMacAddress":"00-15-5D-69-3F-FF","StartMacAddress":"00-15-5D-69
-30-00"}],"ManagementIP":"10.1.36.50","MaxConcurrentEndpoints":0,"Name":"External","Policies":[],"Resources":{"AdditionalParams":{},"AllocationOrder":0,"Allocators":[{"AdditionalParams":{},"AllocationOrder":0,"Health":{"LastErrorCode":0,"LastUpdateTime":1320626909699861
14},"ID":"2D72E7C0-9E9D-4A01-8057-66E7938D0EE0","IsPolicy":false,"Isolation_0":9999,"PortId":"81C0D794-C201-4707-9D12-F1AF435C1916","RDID":"9B219D6E-6847-43FC-8258-81DB4B63C09C","State":3,"SwitchId":"30081EA2-DE0E-4771-82BF-3FDBE9AA31BB","Tag":"RDID"}],"Health":{"LastEr
rorCode":0,"LastUpdateTime":132062690969986114},"ID":"84473089-EDC9-436D-A1E1-3A7882850FD5","PortOperationTime":0,"State":1,"SwitchOperationTime":0,"VfpOperationTime":0,"parentId":"325555C6-D065-4A90-A92A-DD7A5EED5B9B"},"State":1,"Subnets":[{"AdditionalParams":{},"Addre
ssPrefix":"192.168.255.0/30","GatewayAddress":"192.168.255.1","Health":{"LastErrorCode":0,"LastUpdateTime":132062690972642312},"ID":"A8D5A7AB-DD0D-4A01-8E37-10681D2A494A","ObjectType":5,"Policies":[{"Type":"VSID","VSID":9999}],"State":0}],"TotalEndpoints":0,"Type":"over
lay","Version":38654705666},{"ActivityId":"C9CAE6EF-217C-44D1-8942-56B09EB89577","AdditionalParams":{},"CurrentEndpointCount":0,"Extensions":[{"Id":"E7C3B2F0-F3C5-48DF-AF2B-10FED6D72E7A","IsEnabled":false,"Name":"Microsoft Windows
筛选平台"},{"Id":"E9B59CFA-2BE1-4B21-828F-B6FBDBDDC017","IsEnabled":false,"Name":"Microsoft Azure VFP Switch Extension"},{"Id":"EA24CD6C-D17A-4348-9190-09F0D5BE83DD","IsEnabled":true,"Name":"Microsoft NDIS
捕获"}],"Flags":0,"Health":{"AddressNotificationMissedCount":0,"AddressNotificationSequenceNumber":0,"InterfaceNotificationMissedCount":0,"InterfaceNotificationSequenceNumber":0,"LastErrorCode":0,"LastUpdateTime":132062691024261116,"RouteNotificationMissedCount":0,"Rout
eNotificationSequenceNumber":0},"ID":"B4E14E41-5EE4-441A-9675-138F88C43DB0","IPv6":false,"LayeredOn":"1D68A2E3-C9B1-40DC-88BC-C215F750B048","MacPools":[{"EndMacAddress":"00-15-5D-4F-8F-FF","StartMacAddress":"00-15-5D-4F-80-00"}],"MaxConcurrentEndpoints":0,"Name":"nat","
NatName":"ICSBEDB5686-6B22-44B5-A3AF-385BD261F365","Policies":[],"Resources":{"AdditionalParams":{},"AllocationOrder":2,"Allocators":[{"AdapterNetCfgInstanceId":"{BEDB5686-6B22-44B5-A3AF-385BD261F365}","AdditionalParams":{},"AllocationOrder":0,"CompartmendId":0,"Connect
ed":true,"DevicelessNic":false,"EndpointNicGuid":"58D5547C-7040-4BD3-ABB6-E1EE878E6CAD","EndpointPortGuid":"AB26FE6E-B628-4E6B-AC8A-56824F0B44DF","Health":{"LastErrorCode":0,"LastUpdateTime":132062691026403111},"Hidden":false,"ID":"88AE1A7A-77BD-42DF-931B-F7F219C13F9A",
"InterfaceGuid":"BEDB5686-6B22-44B5-A3AF-385BD261F365","IsPolicy":false,"IsolationId":0,"MTU":1450,"MacAddress":"00-15-5D-4F-87-08","ManagementPort":true,"NicFriendlyName":"nat","PreferredPortFriendlyName":"Container NIC
88ae1a7a","State":3,"SwitchId":"AEBE7EB6-3486-43DF-BF4D-431CF2615513","Tag":"Host
Vnic","WaitForIpv6Interface":false,"nonPersistentPort":false},{"AdditionalParams":{},"AllocationOrder":1,"Dhcp":false,"Dns":false,"ExternalInterfaceConstraint":0,"Health":{"DHCPState":1,"DNSState":1,"ICSState":2,"LastErrorCode":0,"LastUpdateTime":132062691028748165},"IC
SFlags":0,"ID":"C015E1CB-3FDF-46A8-BCEF-3FE7AC53B831","IsPolicy":false,"Prefix":20,"PrivateInterfaceGUID":"BEDB5686-6B22-44B5-A3AF-385BD261F365","State":3,"SubnetIPAddress":"172.25.192.0","Tag":"ICS"}],"Health":{"LastErrorCode":0,"LastUpdateTime":132062691026403111},"ID
":"C9CAE6EF-217C-44D1-8942-56B09EB89577","PortOperationTime":0,"State":1,"SwitchOperationTime":0,"VfpOperationTime":0,"parentId":"630083EE-297A-445E-82F1-2B4950A1F129"},"State":1,"Subnets":[{"AdditionalParams":{},"AddressPrefix":"172.25.192.0/20","GatewayAddress":"172.2
5.192.1","Health":{"LastErrorCode":0,"LastUpdateTime":132062691026403111},"ID":"9472AD80-BCEE-440C-8ADB-7458C95532EA","Policies":[],"State":0}],"TotalEndpoints":0,"Type":"nat","Version":38654705666}],"Success":true}
Waiting for the Network to be created




修改 -ManagementIP 参数为 vEthernet

PS C:\k> .\start.ps1 -ManagementIP vEthernet  -NetworkMode overlay  -ClusterCIDR 172.20.0.0/16 -ServiceCIDR 10.68.0.0/16 -KubeDnsServiceIP 10.68.0.2 -LogDir F:\k8s\kubernetes\node\bin\log
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
PS C:\k>





.\start.ps1 -ManagementIP "vEthernet (以太网)"  -NetworkMode overlay  -ClusterCIDR 172.20.0.0/16 -ServiceCIDR 10.68.0.0/16 -KubeDnsServiceIP 10.68.0.2 -LogDir F:\k8s\kubernetes\node\bin\log

 .\start.ps1 -ManagementIP 10.1.36.50 -NetworkMode overlay  -ClusterCIDR 172.20.0.0/16 -ServiceCIDR 10.68.0.0/16 -KubeDnsServiceIP 10.68.0.2 -InterfaceName "vEthernet (以太网)" -LogDir F:\k8s\kubernetes\node\bin\log 





























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