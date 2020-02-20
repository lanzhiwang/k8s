# Kubernetes 101 – Networking

 One of the reasons that I’m so interested in docker and it’s associated technologies is because of the new networking paradigm it brings along with it. Kubernetes has a unique (and pretty awesome) way of dealing with these networking challenges but it can be hard to understand at first glance. My goal in this post is to walk you through deploying a couple of Kubernetes constructs and analyze what Kubernetes is doing at the network layer to make it happen. That being said, let’s start with the basics of deploying a pod. We’ll be using the lab we created in the [first post](https://www.dasblinkenlichten.com/kubernetes-101-the-build/) and some of the config file examples we created in the [second post](https://www.dasblinkenlichten.com/kubernetes-101-the-constructs/).

*Note: I should point out here again that this lab is built with bare metal hardware. The network model in this type of lab is likely slightly different that what you’d see with a cloud provider. However, the mechanics behind what Kubernetes is doing from a network perspective should be identical.* 

So just to level set, here is what our lab looks like…

 

[![image](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/03/image_thumb12.png?zoom=2&resize=625%2C485)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/03/image12.png)
We touched on the topic of pod IP addressing before, but let’s provide some background so that we’re all on the same page. The Kubernetes network model dictates that the containers off each Kubernetes node should be routable. Recall that the default docker network mode provides a docker0 bridge with IP address in the 172.17.0.0/16 range. Each container will get an IP out of this subnet and use the docker0 bridge IP (172.17.42.1) as it’s default gateway. The catch is that the network doesn’t need to know about 172.17.0.0/16 or how to get to it since the docker host does a IP masquerade (or hide NAT) behind it’s real NIC’s IP address for any traffic sourced from a container. That is, the network would see any container traffic as coming from the docker nodes physical IP address.

*Note: When I use the work ‘network’ in this post I’m almost always referring to the physical network that connects the hosts together.* 

While this makes sense from an ease of use perspective, it’s not really ideal. That model requires all sorts of port mapping and in general sort of limits the ability of the docker host. In the Kubernetes model, the docker0 bridge on each host is routable on the network. That is, when a pod get’s deployed, a host outside of the cluster can access that pod directly rather than through a port mapping on the physical host. With that being said, you can view the Kubernetes nodes as routers from a network perspective. If we changed our lab diagram to a network diagram it might look more like this…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/10/image_thumb.png?zoom=2&resize=625%2C400)](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/10/image.png)
The multilayer switch (MLS) has two layer 3 segments hanging off of it. One supporting the 10.20.30.0/24 network and the other supporting the 192.168.10.0 /24 network. In addition, it has routes on it that tell it how to get to each of the subnets that hang off of the routers (Kubernetes nodes). This also means that containers generated on any node will use the node (docker0 bridge IP) as their default gateway, and the node in turn uses the MLS as it’s default gateway. I’m sort of beating the crap out of this concept but it’s important. Network guys LIKE layer 3 to the edge.

So now let’s move onto some examples and see what Kubernetes does on the networking side of things during different circumstances…

**Deploying a pod
**We did this in the last post, but let’s do it again and pay closer attention to what happens. Let’s take our pod example from the last post and use it again…

```
id: "webpod"
kind: "Pod"
apiVersion: "v1beta1"
desiredState:
  manifest:
    version: "v1beta1"
    id: "webpod"
    containers:
      - name: "webpod80"
        image: "jonlangemak/docker:web_container_80"
        cpu: 100
        ports:
          - containerPort: 80
            hostPort: 80
      - name: "webpod8080"
        image: "jonlangemak/docker:web_container_8080"
        cpu: 100
        ports:
          - containerPort: 8080
            hostPort: 8080
labels:
  name: "web"
```

Let’s also assume we’re working with a blank slate on the master. I’ve cleaned up any of the replication controllers, pods, and other services that we had used in the previous post…

[![image](https://i2.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb44.png?zoom=2&resize=625%2C111)](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image44.png)
So let’s go check out one of the nodes and see what it has running at this point. Let’s just pick kubminion1 for now…

[![image](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb45.png?zoom=2&resize=625%2C308)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image45.png)
So no containers running yet and I just want to point out the network configuration is as expected. We have a docker0 bridge interface and the minions local IP interface. Let’s head back to the master, deploy our pod from the config above, and see what happens…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb46.png?zoom=2&resize=625%2C111)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image46.png)
So a couple of interesting things happened already. Kubernetes has assigned a host of 10.20.30.62 (kubminion1) for this pod to run on. Notice that the pod also has an IP address assigned to it which happens to be within the docker0 bridge allocation for kubminion1. Let’s pop over to kubminion1 and see what’s going on…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb47.png?zoom=2&resize=625%2C76)](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image47.png)
Kubminion1 now has 3 containers running. Our pod specification only defines 2, so where does the third one come from? The third containers is running and image called ‘kubernetes/pause:go’. Notice how this is the container that has the ports mapped to it as well. So why is that? Let’s take a deeper look at the containers to see why. I’m going to use the docker ‘inspect’ command to look at some of the information of each container. Namely, I want to see what network mode each container is deployed in…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb48.png?zoom=2&resize=625%2C115)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image48.png)
Interesting, so if we check the ‘NetworkMode’ of each container we see an interesting configuration. The first container we inspected was running the ‘kubernetes/pause:go’ and has a default network mode. The second and third containers we inspected we’re running the ‘web_container_80’ and ‘web_container_8080’ images that we defined in our pods. Note that each of the pod containers has a non-default network config. Specifically, each pod container is using the [mapped container mode](https://www.dasblinkenlichten.com/docker-networking-101-mapped-container/) and specifying the target container as the one running the ‘Kubernetes/pause:go’ image.

So let’s think about this for a second, why would they do this? First off, all the containers in the pod need to share the same IP address. This makes mapped container mode almost a requirement. However, why don’t they just start the first pod container, and then link the second pod container to the first? I think the answer to that question comes in two pieces. First, linking a pod that has multiple containers could be a pain if you had more than 2. Second, you’re dependant on the first container you linked to. If container 2 is linked to container 1, and container 1 dies, then the network stack on container 2 dies as well. It’s easier (and smarter) to have a very basic container run and link all of the pod containers to it. This also simplifies port mapping as we only ever need to apply port mapping rules to the pause container.

So our pod network diagram looks like this…

[![image](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb49.png?zoom=2&resize=494%2C831)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image49.png)
So the real network destination for the pod IP traffic is the pause container. The diagram above is a little deceiving since it shows the pause container ‘forwarding’ the port 80 and port 8080 traffic to the relevant containers. The pause container doesn’t actually do this, it just works that way logically since the two web containers are listening on those ports and share the same network stack with the pause continuer. This is why all of the port mappings for the actual pod containers show up under the port mapping for the pause container. We can examine this with the ‘docker port’ command…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb50.png?zoom=2&resize=622%2C253)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image50.png)
So the pause container really just holds the network endpoint for the pod. It really doesn’t do anything else at all. So what about the node? Does it need to do anything to get the traffic to the pause container? Let’s check the iptables rules and see…

[![image](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb51.png?zoom=2&resize=625%2C222)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image51.png)
There are some rules here, but none of them apply to the pod we just defined. Like I mentioned in the last post, there are some default services Kubernetes provides by default which will be present on each Kubernetes node. That’s what we’re seeing in the above output. The key piece is that we don’t see any masquerade rules or any inbound port mappings for the pod 10.10.10.2.

**Deploying a service
**So now that we’ve seen how Kubernetes handles connecting it’s most basic building block, let’s talk about how it handles services. Like we talked about in our last post, services allow you to abstract services being hosted in pods. In addition, services allow you to scale services horizontally by providing a load balancing mechanism across pods hosting the same service. So let’s once again reset the lab by deleting the pod we just just created and make sure that kubmasta thinks the slate is clean…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb52.png?zoom=2&resize=625%2C112)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image52.png)Now, let’s take the service we defined in the last post and examine it one more time. Here is the configuration file for the service we had called ‘myfirstservice’…

```
  id: "webfrontend"
  kind: "Service"
  apiVersion: "v1beta1"
  port: 80
  containerPort: 80
  selector:
    name: "web"
  labels:
    name: "webservice"
```

To make things a little clearer to explain, I’m going to change the service definition slightly to this…

```
  id: "webfrontend"
  kind: "Service"
  apiVersion: "v1beta1"
  port: 80
  containerPort: 8080
  selector:
    name: "web8080"
  labels:
    name: "webservice"
```

Exact same deal, just changed the container port to be 8080. So let’s define this service in the Kubernetes cluster..

*Note: I dont think I mentioned this before but services should be built before pods that match the service selector are deployed. This ensures that the service related environmental variables exist in the containers.*

[![image](https://i2.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb53.png?zoom=2&resize=625%2C107)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image53.png)
The service creation worked as expected. If we check the available services we see that the cluster has given the service an IP address of 10.100.64.250. This IP address is allocated out of what Kubernetes refers to as the ‘Portal Network’. If you recall, when we built the API service on the kubmasta one of the flags we defined was the ‘PortalNet’…

```
[Unit]
Description=Kubernetes API Server
After=etcd.service
Wants=etcd.service
[Service]
ExecStart=/opt/kubernetes/kube-apiserver \
--address=0.0.0.0 \
--port=8080 \
--etcd_servers=http://127.0.0.1:4001 \
--portal_net=10.100.0.0/16 \
--logtostderr=true
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

This can really be any subnet so long as it doesn’t overlap with the docker0 or physical host subnets. The reason that it can be any subnet is that it’s never routed on the network. The portal net is only locally significant to each node and really just a means to get the traffic off the container and headed towards its default gateway (the docker0 bridge). So before we go any further, let’s again look at kubminion1 and see what’s changed since we defined the service. Let’s start by checking the netfilter rules…

*Note: I’m talking about the same service as above but the IP address is different. This is an unfortunate side effect of writing this blog over a few days and having to rebuild pieces of the lab in between. Above I refer to the service IP as 10.100.64.250 and below I refer to it as 10.100.87.105. Sorry for the confusion!*

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb54.png?zoom=2&resize=625%2C294)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image54.png)
So what do these rules do? The first line tells the host to match a TCP flow destined to 10.100.87.105 on port 80. If it sees a flow that matches that specification, it should redirect the traffic locally to port 39770. The second line tells the node to do the same thing but in a different manner since you’re covering traffic generated from the host rather than the container. The reason the rule isnt identical is because REDIRECT only works for traffic that’s traversing the host. Traffic that’s generated by the host needs to be tackled with a DNAT rule. Long story short, they accomplish the same thing just in different ways so that all traffic coming off the node headed to 10.100.87.105 on port 80 get redirected locally to the host on port 39770.

So we know that any traffic destined to the service IP and port will get redirected to the localhost on port 39770. But where does that get us? This is where the kubernetes-proxy service comes into play. The proxy service assigns a random port for a newly created service and creates a load balancing object within the service that listens on that particular port. In this case, the port happened to be 39770. If we would have been watching the logs of the kuberenetes-service on kubminion1 when we created the service, we would have seen log entries like this…

[![image](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb55.png?zoom=2&resize=625%2C29)](https://i2.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image55.png)
So now that the traffic destined to the service is being redirected to the proxy, we need something for it to load balance to. Let’s spin up one of the replication controllers from our last blog so we can see this in action. I’ll use this config for my replication controller…

```
id: web-controller-2
apiVersion: v1beta1
kind: ReplicationController
desiredState:
  replicas: 4
  replicaSelector:
    name: web8080
  podTemplate:
    desiredState:
      manifest:
        version: v1beta1
        id: webpod
        containers:
          - name: webpod
            image: jonlangemak/docker:web_container_8080
            ports:
              - containerPort: 8080
    labels:
      name: web8080
```

Let’s load this into the cluster and make sure that all of the pods start…

[![image](https://i2.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb56.png?zoom=2&resize=625%2C149)](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image56.png)
Looks good. So now that we have all the pods running, the service should select pods for load balancing that match the label of ‘web8080’. Since the replication controller selector matches all of the pods with the label of ‘web8080’, we should have 4 pods to load balance against. At this point, I’d argue that our lab looks like this…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb57.png?zoom=2&resize=625%2C733)](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image57.png)
While the Kubernetes proxy has been depicted as a sort of shim, it’s really just another service running on the node. The redirect rules we saw above are what make the Kubernetes proxy a shim for traffic destined to service IP addresses.

To see this in action, we’ll do a series of packet captures using tcpdump. To do this, we need to install tcpdump on kubminion1. Let’s install it with this command…

```
yum -y install tcpdump
```

Once installed, let’s open three SSH sessions to kubminion1. In the first window we’ll run the following tcpdump command…

```
tcpdump -nn -q -i ens18 port 8080
```

*Note: In this case we want to capture packets on the servers physical ethernet interface. In my case, it’s called ‘ens18’.*

In the second window we want to run another tcpdump, but we need to get some more info first. Namely, we want to get the virtual interface (veth) name for the container attached to the docker0 bridge. Running with the assumption that you only have the webpod container running on this host you can do a simple ‘ifconfig’ and you should only have one ‘Veth’ interface…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb58.png?zoom=2&resize=625%2C619)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image58.png)
Copy this interface name and insert it into the tcpdump command for your second window…

```
tcpdump -nn -q -i veth12370a6 host 10.100.87.105
```

Run both the commands and stack the windows up so you can see both at the same time…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb59.png?zoom=2&resize=625%2C433)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image59.png)
So once you have both captures running let’s turn our attention to the third window. Let’s use our ‘docker exec’ command to attach into the ‘web_container_8080’ container (do a ‘docker ps’ to get the container name first)…

docker exec -it e130a52dfae6 /bin/bash

Once inside the running container, let’s try and access the service with curl…

```
curl 10.100.87.105
```

After my first curl to the service IP address, I had this in my capture windows…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb60.png?zoom=2&resize=625%2C554)](https://i2.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image60.png)
So what does this tell us? Let’s draw this out in our diagram showing the top capture (traffic off the servers physical NIC) in red and the bottom capture (traffic off the docker0 bridge) in blue…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb61.png?zoom=2&resize=625%2C733)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image61.png)
*Note: I make a point to draw the line around the ‘kubernetes proxy’ on kubminion3. I did this because the kubernetes proxy on kubminion3 is NOT required for this flow to work. Put another way, the proxy service that intercepts the service request talks directly to the pod it load balances to.*

So if we look at the bottom window first, we see the traffic from the container point of view. The container attempts to open a TCP socket to 10.100.87.105 on port 80. We see return traffic from the service IP address of 10.100.87.105. From the container’s point of view, it’s entire communication is with the service. If we look at our second capture (top window) we can see what actually hit the wire. We see a TCP session sourced from the nodes physical IP address (10.20.30.62) and destined to the pod hosted on kubminion3 (10.10.30.4). To summarize, the Kubernetes proxy service is acting as a full proxy maintaining two distinct TCP connections. The first from container to proxy, and the second from proxy to the load balanced destination.

If we cleared our captures and ran the curl again we should see the traffic load balanced to another node…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb62.png?zoom=2&resize=536%2C517)](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image62.png)
In this case, the Kubernetes proxy decided to load balance the traffic to the pod running on kubminion2 (10.10.20.4). Our diagram for this flow would look like…

[![image](https://i0.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image_thumb63.png?zoom=2&resize=625%2C733)](https://i1.wp.com/www.dasblinkenlichten.com/wp-content/uploads/2015/02/image63.png)
I think you get the point without me showing you the other two possible outcomes for load balancing our test service. The important part to understand about services is that they allow you to easily and quickly scale pod deployed services. One could see how this can be a powerful feature when coupled with pods deployed with a replication controller.

But while services handle an important aspect of a Kubernetes cluster, they’re only relevant for pods accessing services living in other pods. Recall, the portal IP space isn’t accessible from the network, it’s only locally significant to the host. So how do things outside the cluster consume applications deployed in the cluster? We’ll cover that in our next post.

[来源](https://www.dasblinkenlichten.com/kubernetes-101-networking/)