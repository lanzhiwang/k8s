# alertmanager


```
$ sudo mkdir -p /var/lib/alertmanager /etc/alertmanager/template
$ sudo chown -R $(whoami):docker /var/lib/alertmanager /etc/alertmanager/template

$ vim /etc/alertmanager/config.yml
global:
  resolve_timeout: 5m
templates:
  - '/etc/alertmanager/template/*.tmpl'
route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 30s
  group_interval: 1m
  repeat_interval: 1m
  receiver: WebHook
inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster', 'service']
receivers:
  - name: 'WebHook'
    webhook_configs:
      - url: 'http://localhost:5001'

$ docker run -d -p 9003:9003 --name alertmanager








```