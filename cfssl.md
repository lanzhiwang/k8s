# cfssl



```

{
  "CN": "admin",  # 域名 k8s user
  "hosts": [],  # 表示哪些主机名(域名)或者IP可以使用此csr申请的证书，为空或者""表示所有的都可以使用
  "key": {  # 生成证书的算法
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",  #国家
      "ST": "hubeisheng",  # 省份
      "L": "wuhanshi",  # 城市
      "O": "system:masters",  # 公司名称 k8s group
      "OU": "System"  # 公司部门
    }
  ]
}
```

