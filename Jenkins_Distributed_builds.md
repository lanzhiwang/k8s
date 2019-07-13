# Jenkins Distributed builds

[参考1](https://wiki.jenkins.io/display/JENKINS/Distributed+builds)
[参考2](https://hub.docker.com/u/jenkins)
[参考3](https://jenkins.io/zh/blog/2018/12/10/the-official-Docker-image/)

It is pretty common when starting with Jenkins to have a single server which runs the master and all builds, however Jenkins architecture is fundamentally "Master+Agent". The master is designed to do co-ordination and provide the GUI and API endpoints, and the Agents are designed to perform the work. The reason being that workloads are often best "farmed out" to distributed servers. This may be for scale, or to provide different tools, or build on different target platforms. Another common reason for remote agents is to enact deployments into secured environments (without the master having direct access).   从Jenkins开始拥有运行master和所有构建的单个服务器是很常见的，但Jenkins架构基本上是“Master + Agent”。 主服务器旨在协调并提供GUI和API端点，代理程序旨在执行工作。 原因是工作负载通常最好“分配”到分布式服务器。 这可能是为了扩展，或提供不同的工具，或构建在不同的目标平台上。 远程代理的另一个常见原因是将部署安装到安全环境中（主设备无法直接访问）。

Many people today use Jenkins in cloud environments, and there are plugins and extensions to support the various environments and clouds. These may involve Virtual Machines, Docker Containers, Kubernetes (for example see Jenkins-X), EC2, Azure, Google Cloud, VMWare and more. In these cases the agents are managed for you typically (and in many cases on demand, as needed), so you may not need to read the content of this document for those cases.   今天许多人在云环境中使用Jenkins，并且有插件和扩展来支持各种环境和云。 这些可能涉及虚拟机，Docker容器，Kubernetes（例如参见Jenkins-X），EC2，Azure，Google Cloud，VMWare等。 在这些情况下，代理通常会为您管理（并且在许多情况下根据需要按需管理），因此您可能不需要为这些情况阅读本文档的内容。

This document describes this distributed mode of Jenkins and some of the ways in which you can configure it, should you need to take control (or maybe you are curious)  本文档描述了Jenkins的这种分布式模式以及您可以配置它的一些方法，如果您需要控制（或者您很好奇）


Contents

* How does this work?  这是如何运作的？
	* Master to agent connections  掌握代理连接
	* Agent to master connections 代理来掌握连接
	* Choosing which agent pipelines and steps run on  选择运行哪些代理管道和步骤
* Different ways of starting agents  不同的启动代理方式
	* Have master launch agent via ssh  通过ssh拥有主启动代理
	* Have master launch agent on Windows  在Windows上拥有主启动代理
	* Write your own script to launch Jenkins agents  编写自己的脚本以启动Jenkins代理
	* Launch agent via "JNLP" from agent back to master in a browser  通过“JNLP”从代理启动代理程序返回到浏览器中的主代理程序
	* Launch agent headlessly from agent back to master on command line  在命令行上从代理无回复启动代理
	* Other Requirements  其他需求
* Node labels for agents  代理的节点标签
	* Defining labels  定义标签
	* Using labels  使用标签
* Example: Configuration on Unix  示例：在Unix上配置
* Scheduling strategy  调度策略
* Node monitoring  节点监控
* Offline status and retention strategy  脱机状态和保留策略
* Transition from master-only to master/agent  从master-only转换为master / agent
* Access an Internal CI Build Farm (Master + Agents) from the Public Internet  从公共Internet访问内部CI构建服务器场（主服务器+代理服务器）
* Running Multiple Agents on the Same Machine  在同一台计算机上运行多个代理
* Troubleshooting tips  故障排除提示
	* Windows agent service upgrades  Windows代理服务升级
* Other readings  其他读物

## How does this work?  这是如何运作的？

A "master" operating by itself is the basic installation of Jenkins and in this configuration the master handles all tasks for your build system. In most cases installing an agent doesn't change the behavior of the master. It will serve all HTTP requests, and it can still build projects on its own. Once you install a few agents you might find yourself removing the executors on the master in order to free up master resources (allowing it to concentrate resources on managing your build environment) but this is not a necessary step. If you start to use Jenkins a lot with just a master you will most likely find that you will run out of resources (memory, CPU, etc.). At this point you can either upgrade your master or you can setup agents to pick up the load. As mentioned above you might also need several different environments to test your builds. In this case using an agent to represent each of your required environments is almost a must.  操作本身的“主”是Jenkins的基本安装，在此配置中，master处理构建系统的所有任务。 在大多数情况下，安装代理程序不会更改主服务器的行为。 它将为所有HTTP请求提供服务，它仍然可以自己构建项目。 一旦安装了几个代理，您可能会发现自己正在删除主服务器上的执行程序以释放主资源（允许它集中资源来管理构建环境），但这不是必要的步骤。 如果你开始大量使用Jenkins只有一个主人，你很可能会发现你将耗尽资源（内存，CPU等）。 此时，您可以升级主服务器，也可以设置代理来获取负载。 如上所述，您可能还需要几种不同的环境来测试构建。 在这种情况下，使用代理来表示每个所需的环境几乎是必须的。

An agent is a computer that is set up to offload build projects from the master and once setup this distribution of tasks is fairly automatic. The exact delegation behavior depends on the configuration of each project; some projects may choose to "stick" to a particular machine for a build, while others may choose to roam freely between agents. For people accessing your Jenkins system via the integrated website (http://yourjenkinsmaster:8080), things work mostly transparently. You can still browse javadoc, see test results, download build results from a master, without ever noticing that builds were done by agents.  In other words, the master becomes a sort of "portal" to the entire build farm.  代理程序是设置为从主程序卸载构建项目的计算机，一旦设置此任务分配是相当自动的。 确切的委派行为取决于每个项目的配置; 一些项目可能会选择“粘贴”到特定的机器进行构建，而其他项目可能选择在代理之间自由漫游。 对于通过集成网站（http：// yourjenkinsmaster：8080）访问Jenkins系统的人来说，事情大多是透明的。 您仍然可以浏览javadoc，查看测试结果，从主服务器下载构建结果，而无需注意到构建是由代理完成的。 换句话说，主服务器成为整个构建服务器场的一种“门户”。

Since each agent runs a separate program called an "agent" there is no need to install the full Jenkins (package or compiled binaries) on an agent. There are various ways to start agents, but in the end the agent and Jenkins master need to establish a bi-directional communication link (for example a TCP/IP socket) in order to operate.  由于每个代理程序都运行一个名为“代理程序”的独立程序，因此无需在代理程序上安装完整的Jenkins（程序包或已编译的二进制文件）。 启动代理有多种方法，但最终代理和Jenkins主机需要建立双向通信链路（例如TCP / IP套接字）才能运行。

Follow the Step by step guide to set up master and agent machines on Windows to quickly start using distributed builds.  按照分步指南在Windows上设置主计算机和代理计算机，以快速开始使用分布式构建。

### Master to agent connections  掌握代理连接

The most popular ways agents are configured are via connections that are initiated from the master. This allows agents to be minimally configured and the control lives with the master. This does require that the master have network access (ingress) to the agent (typically this is via ssh). In some cases this is not desirable due to security network rules, in which case you can use Agent to master connections via "JNLP".  最常用的代理配置方式是通过主服务器启动的连接。 这样可以最大限度地配置代理，并使控件与主服务器一起使用。 这确实要求主服务器具有对代理的网络访问（入口）（通常这是通过ssh）。 在某些情况下，由于安全网络规则，这是不可取的，在这种情况下，您可以使用代理通过“JNLP”来控制连接。

### Agent to master connections 代理来掌握连接

In some cases the agent server will not be visible to the master, so the master can not initiate the agent process. You can use a different type of agent configuration in this case called "JNLP". This means that the master does not need network "ingress" to the agent (but the agent will need to be able to connect back to the master). Handy for if the agents are behind a firewall, or perhaps in some more secure environment to do trusted deploys (as an example). See the sections below to choose the type of agent that is most appropriate for your needs.   在某些情况下，代理服务器对主服务器不可见，因此主服务器无法启动代理进程。 在这种情况下，您可以使用不同类型的代理配置，称为“JNLP”。 这意味着主服务器不需要网络“进入”代理（但代理需要能够连接回主服务器）。 如果代理程序位于防火墙后面，或者可能在某些更安全的环境中进行可信部署（作为示例），则非常方便。 请参阅以下部分，以选择最适合您需求的代理类型。

### Choosing which agent pipelines and steps run on  选择运行哪些代理管道和步骤

As you will see below, agents can be labelled. This means different part of your build, or pipeline, can be allocated to run in specific agents (based on their label). This can be useful for tools, operating systems or perhaps for security purposes (it is possible to set quite detailed access rules of what can run where, based on agent configurations). A server that runs an agent is often referred to as a "Node" in Jenkins terminology.   正如您将在下面看到的，可以标记代理。 这意味着您的构建或管道的不同部分可以分配为在特定代理中运行（基于其标签）。 这对于工具，操作系统或可能出于安全目的非常有用（可以根据代理配置设置可以在哪里运行的非常详细的访问规则）。 运行代理的服务器通常在Jenkins术语中称为“节点”。

## Different ways of starting agents  不同的启动代理方式

Pick the right method depending on your environment and OS that master/agents run, or if you want the connection initiated from the master or from the agent end.  根据您的主机/代理运行的环境和操作系统，或者您希望从主服务器或代理程序端启动连接，选择正确的方法。

### Have master launch agent via ssh  通过ssh拥有主启动代理

Jenkins has a built-in SSH client implementation that it can use to talk to remote sshd and start an agent. This is the most convenient and preferred method for Unix agents, which normally has sshd out-of-the-box. Click Manage Jenkins, then Manage Nodes, then click "New Node." In this set up, you'll supply the connection information (the agent host name, user name, and ssh credential). Note that the agent will need the master's public ssh key copied to ~/.ssh/authorized_keys. (This is a decent howto if you need ssh help). Jenkins will do the rest of the work by itself, including copying the binary needed for an agent, and starting/stopping agents. If your project has external dependencies (like a special ~/.m2/settings.xml, or a special version of java), you'll need to set that up yourself, though.  The Slave Setup Plugin may be of help.  Jenkins有一个内置的SSH客户端实现，可用于与远程sshd通信并启动代理。 对于Unix代理来说，这是最方便和首选的方法，它通常具有开箱即用的sshd。 单击Manage Jenkins，然后单击Manage Nodes，然后单击“New Node”。 在此设置中，您将提供连接信息（代理主机名，用户名和ssh凭证）。 请注意，代理程序需要将master的公共ssh密钥复制到〜/ .ssh / authorized_keys。 （如果你需要ssh帮助，这是一个不错的方法）。 Jenkins将自己完成剩下的工作，包括复制代理所需的二进制文件，以及启动/停止代理。 如果您的项目具有外部依赖项（例如特殊的〜/ .m2 / settings.xml或特殊版本的java），您需要自己设置它。 Slave Setup Plugin可能会有所帮助。

This is the most convenient set up on Unix. However, if you are on Windows and you don't have ssh commands with cygwin for example, you can use a tool like PuTTY and PuTTYgen to generate your private and public pair of keys.  这是Unix上最方便的设置。 但是，如果您使用的是Windows并且没有使用cygwin的ssh命令，则可以使用PuTTY和PuTTYgen等工具生成私钥和公钥。

For connecting to Windows agents through cygwin sshd, see SSH agents and Cygwin for more details.  要通过cygwin sshd连接到Windows代理，请参阅SSH代理和Cygwin以获取更多详细信息。

### Have master launch agent on Windows  在Windows上拥有主启动代理

For Windows agents, Jenkins can use the remote management facility built into Windows 2000 or later (WMI+DCOM, to be more specific.) In this set up, you'll supply the username and the password of the user who has the administrative access to the system, and Jenkins will use that remotely create a Windows service and remotely start/stop them.  对于Windows代理，Jenkins可以使用Windows 2000或更高版本中内置的远程管理工具（WMI + DCOM，更具体一点。）在此设置中，您将提供具有管理访问权限的用户的用户名和密码。 到系统，Jenkins将使用它远程创建Windows服务并远程启动/停止它们。

This is the most convenient set up on Windows, but does not allow you to run programs that require display interaction (such as GUI tests).  这是Windows上最方便的设置，但不允许您运行需要显示交互的程序（例如GUI测试）。

Note : Unlike other Node's configuration type, the Node's name is very important as it is taken as the node's address where to create the service !  注意：与其他Node的配置类型不同，Node的名称非常重要，因为它被视为节点的地址来创建服务！

### Write your own script to launch Jenkins agents  编写自己的脚本以启动Jenkins代理

If the above turn-key solutions do not provide flexibility necessary, you can write your own script to start an agent. You place this script on the master, and tell Jenkins to run this script whenever it needs to connect to an agent.  如果上述交钥匙解决方案无法提供必要的灵活性，您可以编写自己的脚本来启动代理。 您将此脚本放在主服务器上，并告诉Jenkins在需要连接到代理时运行此脚本。

Typically, your script uses a remote program execution mechanism like SSH, or other similar means (on Windows, this could be done by the same protocols through cygwin or tools like psexec), but Jenkins doesn't really assume any specific method of connectivity.  通常，您的脚本使用远程程序执行机制，如SSH或其他类似方法（在Windows上，这可以通过cygwin通过相同的协议或像psexec这样的工具完成），但Jenkins并没有真正假设任何特定的连接方法。

What Jenkins expects from your script is that, in the end, it has to execute the agent program like java -jar agent.jar, on the right computer, and have its stdin/stdout connect to your script's stdin/stdout. For example, a script that does "ssh mynode java -jar ~/bin/agent.jar" would satisfy this.
(The point is that you let Jenkins run this command, as Jenkins uses this stdin/stdout as the communication channel to the agent. Because of this, running this manually from your shell will do you no good).  enkins对您的脚本的期望是，最终，它必须在右侧计算机上执行代理程序，如java -jar agent.jar，并将其stdin / stdout连接到您的脚本的stdin / stdout。 例如，执行“ssh mynode java -jar~ / bin / agent.jar”的脚本将满足此要求。
（关键是你让Jenkins运行这个命令，因为Jenkins使用这个stdin / stdout作为代理的通信通道。因此，从shell手动运行它对你没有好处）。

A copy of agent.jar can be downloaded from http://yourserver:port/jnlpJars/agent.jar . Many people write scripts in such a way that this 160K jar is downloaded during the running of said script, to ensure that a consistent version of agent.jar is always used. Such an approach eliminates the agent.jar updating issue discussed below. Note that the SSH Slaves plugin does this automatically, so agents configured using this plugin always use the correct agent.jar.  可以从http：// yourserver：port / jnlpJars / agent.jar下载agent.jar的副本。 许多人编写脚本的方式是在运行所述脚本期间下载这个160K jar，以确保始终使用一致版本的agent.jar。 这种方法消除了下面讨论的agent.jar更新问题。 请注意，SSH Slaves插件会自动执行此操作，因此使用此插件配置的代理始终使用正确的agent.jar。

Updating slave.jar

Technically speaking, in this set up you should update agent.jar every time you upgrade Jenkins to a new version. However, in practice agent.jar changes infrequently enough that it's also practical not to update until you see a fatal problem in start-up.  从技术上讲，在这个设置中，每次将Jenkins升级到新版本时都应该更新agent.jar。 但是，在实践中，agent.jar不经常更改，直到您在启动时看到致命问题时才更新。

Launching agents this way often requires an additional initial set up on agents (especially on Windows, where remote login mechanism is not available out of box), but the benefits of this approach is that when the connection goes bad, you can use Jenkins's web interface to re-establish the connection.  以这种方式启动代理通常需要在代理上进行额外的初始设置（特别是在Windows上，其中远程登录机制不可用），但这种方法的好处是当连接变坏时，可以使用Jenkins的Web界面 重新建立连接。

### Launch agent via "JNLP" from agent back to master in a browser  通过“JNLP”从代理启动代理程序返回到浏览器中的主代理程序

Another way of doing this is to start an agent through Java Web Start (JNLP).  另一种方法是通过Java Web Start（JNLP）启动代理。

It requires the server to be configured to appear in first place. So, before attempting to create the build agent, head into manage Jenkins->Global Security->TCP port for JNLP agents.  它要求将服务器配置为首先出现。 因此，在尝试创建构建代理之前，请先管理Jenkins-> Global Security-> TCP端口以获取JNLP代理。

In this approach, you'll interactively logon to the agent node, open a browser, and open the agent page. You'll be then presented with the JNLP launch icon. Upon clicking it, Java Web Start will kick in, and it launches an agent on the computer where the browser was running.  在此方法中，您将以交互方式登录到代理节点，打开浏览器并打开代理页面。 然后，您将看到JNLP启动图标。 单击它后，Java Web Start将启动，并在运行浏览器的计算机上启动代理。

This mode is convenient when the master cannot initiate a connection to agents, such as when it runs outside a firewall while the rest of the agents are in the firewall. OTOH, if the machine with an agent goes down, the master has no way of re-launching it on its own.  当主服务器无法启动与代理的连接时，例如当它在防火墙外部运行而其他代理位于防火墙中时，此模式很方便。 OTOH，如果带有代理的机器发生故障，主机无法自行重新启动它。

On Windows, you can do this manually once, then from the launched JNLP agent, you can install it as a Windows service so that you don't need to interactively start the agent from then on.  在Windows上，您可以手动执行一次，然后从启动的JNLP代理程序中将其安装为Windows服务，这样您就不需要从此开始以交互方式启动代理程序。

If you need display interaction (e.g. for GUI tests) on Windows and you have a dedicated (virtual) test machine, this is a suitable option. Create a jenkins user account, enable auto-login, and put a shortcut to the JNLP file in the Startup items (after having trusted the agent's certificate). This allows one to run tests as a restricted user as well.  如果您需要在Windows上进行显示交互（例如，用于GUI测试）并且您有专用（虚拟）测试机器，则这是一个合适的选项。 创建一个jenkins用户帐户，启用自动登录，并在启动项中放置JNLP文件的快捷方式（在信任代理的证书之后）。 这允许用户也可以作为受限用户运行测试。

Note: If the master is running behind a reverse proxy or similar, you might need to configure "Tunnel connection through" in the "Advanced" section of the JNLP start method on the agent configuration page to make JNLP work.  注意：如果主服务器在反向代理或类似代理之后运行，则可能需要在代理配置页面上的JNLP启动方法的“高级”部分中配置“通过隧道连接”以使JNLP正常工作。

### Launch agent headlessly from agent back to master on command line  在命令行上从代理无回复启动代理

This launch mode uses a mechanism very similar to JNLP as described above, except that it runs without using GUI, making it convenient for an execution as a daemon on Unix. To do this, configure this agent to be a JNLP agent, take agent.jar as discussed above, and then from the agent, run a command like this:  此启动模式使用与上述JNLP非常相似的机制，除了它在不使用GUI的情况下运行，从而便于在Unix上作为守护程序执行。 要执行此操作，请将此代理配置为JNLP代理，如上所述获取agent.jar，然后从代理运行如下命令：

```bash
$ java -jar agent.jar -jnlpUrl http://yourserver:port/computer/agent-name/slave-agent.jnlp
```

Make sure to replace "agent-name" with the name of your agent.  确保将“agent-name”替换为您的代理的名称。

### Other Requirements  其他需求

Also note that the agents are a kind of a cluster, and operating a cluster (especially a large one or heterogeneous one) is always a non-trivial task. For example, you need to make sure that all agents have JDKs, Ant, CVS, and/or any other tools you need for builds. You need to make sure that agents are up and running, etc. Jenkins is not a clustering middleware, and therefore it doesn't make this any easier.  Nevertheless, one can use a server provisioning tool and a configuration management software to facilitate both aspects.  还要注意，代理是一种集群，操作集群（尤其是大型集群或异构集群）始终是一项非常重要的任务。 例如，您需要确保所有代理都具有JDK，Ant，CVS和/或构建所需的任何其他工具。 您需要确保代理已启动并运行等.Jenkins不是集群中间件，因此它不会使这更容易。 然而，可以使用服务器供应工具和配置管理软件来促进这两个方面。

## Node labels for agents  代理的节点标签

Labels are tags one can give an agent which allows it to differentiate itself from other nodes in Jenkins.  标签是可以提供代理的标签，允许它将自己与Jenkins中的其他节点区分开来。

A few reasons why node labels are important:  节点标签重要的几个原因：

* Nodes might have certain tools associated with it. Labels could include different tools a given node supports.  节点可能具有与之关联的某些工具。 标签可以包括给定节点支持的不同工具。

* Nodes may be in a multi-operating system build environment (e.g. Windows, Mac, and Linux agents within one Jenkins build system). There can be a label for the operating system of the node.  节点可以在多操作系统构建环境中（例如，在一个Jenkins构建系统内的Windows，Mac和Linux代理）。 可以为节点的操作系统添加标签。

* Nodes may be in geographically different locations which can be the case for multi-datacenter deployments. Jenkins can have agents in different datacenters when inter-datacenter communication is strictly regulated with edge firewalls. In this case, you might have a label for the datacenter or cloudstack in which the agent resides.  节点可能位于地理位置不同的位置，这可能是多数据中心部署的情况。 当使用边缘防火墙严格控制数据中心间通信时，Jenkins可以在不同的数据中心拥有代理。 在这种情况下，您可能拥有代理所在的数据中心或cloudstack的标签。

### Defining labels  定义标签

Labels are defined in the settings of static agents and for agent clouds. They must be space separated words which define that agent. Sticking to standard ASCII characters is recommended. Here's a few label suggestions one can use for agent agents:  标签在静态代理和代理云的设置中定义。 它们必须是空格分隔的单词，用于定义代理。 建议坚持使用标准ASCII字符。 以下是可以用于代理商代理的一些标签建议：

* For toolchains: jdk, node_js, ruby, etc
* For operating systems: linux, windows, osx; or you can be more detailed like ubuntu16.04
* For geographic locations: us-east, japan, eu-central etc
* For platforms: docker, openstack, etc.

### Using labels  使用标签

Jobs and pipelines can be pinned to specific agents or groups of agents if multiple agents have similar sets of labels. In jobs, visit advanced settings and choose restrict where the job can run. In pipelines, you would restrict it with the node block. You can restrict jobs by specifying a single label or use a label expression. Here's two examples:  如果多个代理具有相似的标签集，则可以将作业和管道固定到特定代理或代理组。 在作业中，访问高级设置并选择限制作业可以运行的位置。 在管道中，您将使用节点块限制它。 您可以通过指定单个标签或使用标签表达式来限制作业。 这是两个例子：

* Single label: us-east
* Label expression: openstack && us-east && linux

The above label expression means that a given agent must have all of those labels.  上面的标签表达意味着给定的代理必须具有所有这些标签。

## Example: Configuration on Unix  示例：在Unix上配置

This section describes Kohsuke Kawaguchi's set up of Jenkins agents that he used to use inside Sun for his day job. His master Jenkins node ran on a SPARC Solaris box, and he had many SPARC Solaris agents, Opteron Linux agents, and a few Windows agents.  本节描述了Kohsuke Kawaguchi设立的Jenkins代理商，他曾经在Sun内部使用过他的日常工作。 他的主人Jenkins节点在SPARC Solaris机器上运行，他有许多SPARC Solaris代理，Opteron Linux代理和一些Windows代理。

* Each computer has an user called `jenkins` and a group called `jenkins`. All computers use the same UID and GID. (If you have access to NIS, this can be done more easily.) This is not a Jenkins requirement, but it makes the agent management easier.

* On each computer, `/var/jenkins` directory is set as the home directory of user `jenkins`. Again, this is not a hard requirement, but having the same directory layout makes things easier to maintain.  在每台计算机上，/ var / jenkins目录设置为用户jenkins的主目录。 同样，这不是一个硬性要求，但具有相同的目录布局使事情更容易维护。

* All machines run `sshd`. Windows agents run `cygwin sshd`.

* All machines have `/usr/sbin/ntpdate` installed, and synchronize clock regularly with the same NTP server.

* Master's `/var/jenkins` have all the build tools beneath it --- a few versions of Ant, Maven, and JDKs. JDKs are native programs, so I have JDK copies for all the architectures I need. The directory structure looks like this:  Master的/ var / jenkins拥有它下面的所有构建工具--- Ant，Maven和JDK的几个版本。 JDK是本机程序，所以我有所需的所有架构的JDK副本。 目录结构如下所示：

```
/var/jenkins
  +- .ssh
  +- bin
  |   +- agent  (more about this below)
  +- workspace (jenkins creates this file and store all data files inside)
  +- tools
      +- ant-1.5
      +- ant-1.6
      +- maven-1.0.2
      +- maven-2.0
      +- java-1.4 -> native/java-1.4 (symlink)
      +- java-1.5 -> native/java-1.5 (symlink)
      +- java-1.8 -> native/java-1.8 (symlink)
      +- native -> solaris-sparcv9 (symlink; different on each computer)
      +- solaris-sparcv9
      |   +- java-1.4
      |   +- java-1.5
      |   +- java-1.8
      +- linux-amd64
          +- java-1.4
          +- java-1.5
          +- java-1.8
```

* Master's `/var/jenkins/.ssh` has private/public key and `authorized_keys` so that a master can execute programs on agents through `ssh`, by using public key authentication.

* On master, I have a little shell script that uses rsync to synchronize master's /var/jenkins to agents (except /var/jenkins/workspace). I also use the script to replicate tools on all agents.  在master上，我有一个小shell脚本，它使用rsync将master的 /var/jenkins 同步到代理（/var/jenkins/workspace 除外）。 我还使用该脚本在所有代理上复制工具。

* `/var/jenkins/bin/launch-agent` is a shell script that Jenkins uses to execute jobs remotely. This shell script sets up `PATH` and a few other things before launching `agent.jar`. Below is a very simple example script.  /var/jenkins/bin/launch-agent 是Jenkins用于远程执行作业的shell脚本。 在启动agent.jar之前，此shell脚本会设置PATH和其他一些内容。 下面是一个非常简单的示例脚本。

```bash
#!/bin/bash
 
JAVA_HOME=/opt/SUN/jdk1.8.0_152
PATH=$PATH:$JAVA_HOME/bin
export PATH
java -jar /var/jenkins/bin/agent.jar
```

* Finally all computers have other standard build tools like svn and cvs installed and available in PATH.  最后，所有计算机都安装了其他标准构建工具，如svn和cvs，并在PATH中提供。

Note that in the more recent Jenkins packages, the default JENKINS_HOME (aka home directory for the 'jenkins' user on Linux machines, e.g. Red Hat, CentOS, Ubuntu) is set to /var/lib/jenkins.  请注意，在最近的Jenkins软件包中，默认的JENKINS_HOME（也就是Linux机器上'jenkins'用户的主目录，例如Red Hat，CentOS，Ubuntu）设置为 /var/lib/jenkins 。

## Scheduling strategy  调度策略

Some agents are faster, while others are slow. Some agents are closer (network wise) to a master, others are far away. So doing a good build distribution is a challenge. Currently, Jenkins employs the following strategy:  有些代理更快，而有些则慢。 有些代理商与主人更接近（网络明智），其他代理商则很远。 因此，进行良好的构建分发是一项挑战。 目前，Jenkins采用以下策略：

1. If a project is configured to stick to one computer, that's always honored.  如果项目配置为坚持一台计算机，那么它总是很受尊重。

2. Jenkins tries to build a project on the same computer that it was previously built.  Jenkins尝试在之前构建的同一台计算机上构建项目。

If you have interesting ideas (or better yet, implementations), please let me know.

## Node monitoring  节点监控

Jenkins has a notion of a “node monitor” which can check the status of an agent for various conditions, displaying the results and optionally marking the agent offline accordingly. Jenkins bundles several, checking disk space in the workspace; disk space in the temporary partition; swap space; clock skew (compared to the master); and response time.  Jenkins有一个“节点监视器”的概念，它可以检查代理的各种条件的状态，显示结果并可选地相应地标记代理。 Jenkins捆绑了几个，检查工作区中的磁盘空间; 临时分区中的磁盘空间; 交换空间; 时钟偏差（与主人相比）; 和响应时间。

Plugins can add other monitors.  插件可以添加其他监视器。

## Offline status and retention strategy  脱机状态和保留策略

Administrators can manually mark agents offline (with an optional published reason) or reconnect them.  管理员可以脱机手动标记代理（使用可选的已发布原因）或重新连接它们。

Groovy scripts such as Monitor and Restart Offline Slaves can perform batch operations like this. There is also a CLI command to reconnect.  诸如Monitor和Restart Offline Slaves之类的Groovy脚本可以执行这样的批处理操作。 还有一个CLI命令可以重新连接。

Then there is a background task which automatically reconnects agents that are thought to be back up. The behavior is configurable per agent (or per cloud, if using cloudy provisioning for agents) via a “retention strategy”, of which Jenkins bundles several (plugins can contribute others): always keep online if possible; drop offline when not in use; use a schedule; behave according to cloud’s notion of load.  然后有一个后台任务会自动重新连接被认为备份的代理。 可以通过“保留策略”为每个代理（或每个云，如果使用代理的多云配置）配置行为，其中Jenkins捆绑了几个（插件可以贡献其他人）：如果可能，始终保持在线; 不使用时脱机; 使用时间表; 根据云的负载概念表现。

## Transition from master-only to master/agent  从master-only转换为master / agent

Typically, you start with a master-only installation and then much later you add agents as your projects grow. When you enable the master/agent mode, Jenkins automatically configures all your existing projects to stick to the master node. This is a precaution to avoid disturbing existing projects, since most likely you won't be able to configure agents correctly without trial and error. After you configure agents successfully, you need to individually configure projects to let them roam freely. This is tedious, but it allows you to work on one project at a time.  通常，您从一个仅限主的安装开始，然后在项目增长时添加代理。 启用主/代理模式后，Jenkins会自动将所有现有项目配置为保留在主节点上。 这是一种避免干扰现有项目的预防措施，因为很可能您无法在没有反复试验的情况下正确配置代理。 成功配置代理后，需要单独配置项目以使其自由漫游。 这很乏味，但它允许您一次处理一个项目。

Projects that are newly created on master/agent-enabled Jenkins will be by default configured to roam freely.  默认情况下，在启用主/代理的Jenkins上新创建的项目将自由漫游。

## Access an Internal CI Build Farm (Master + Agents) from the Public Internet  从公共Internet访问内部CI构建服务器场（主服务器+代理服务器）

One might consider make the Jenkins master accessible on the public network (so that people can see it), while leaving the build agents within the firewall (typical reasons: cost and security) There are several ways to make it work:  有人可能会考虑让Jenkins master在公共网络上可访问（以便人们可以看到它），同时将构建代理留在防火墙内（典型的原因：成本和安全性）有几种方法可以使它工作：

* Equip the master node with a network interface that's exposed to the public Internet (simple to do, but not recommended in general)  为主节点配备暴露于公共Internet的网络接口（操作简单，但一般不推荐）

* Allow port-forwarding from the master to your agents within the firewall. The port-forwarding should be restricted so that only the master with its known IP can connect to agents. With this set up in the firewall, as far as Jenkins is concerned it's as if the firewall doesn't exist.  If multiple hops are involved, you may wish to investigate how to do ssh "jump host" transparently using the ProxyCommand construct.  In fact,  with a properly configured "jump host" setup, even the master doesn't need to expose itself to the public Internet at all - as long as the organization's firewall allows port 22 traffic.  允许从主服务器向防火墙内的代理进行端口转发。 应限制端口转发，以便只有具有已知IP的主服务器才能连接到代理。 在防火墙中进行此设置，就Jenkins而言，就好像防火墙不存在一样。 如果涉及多个跃点，您可能希望研究如何使用ProxyCommand构造透明地执行ssh“jump host”。 事实上，通过正确配置的“跳转主机”设置，即使主设备根本不需要将自己暴露给公共互联网 - 只要组织的防火墙允许端口22流量。

* Use JNLP agents and have agents connect to the master, not the other way around. In this case it's the agents that initiates the connection, so it works correctly with the NAT firewall.  使用JNLP代理并让代理连接到主服务器，而不是相反。 在这种情况下，它是启动连接的代理，因此它可以与NAT防火墙一起正常工作。

Note that in both cases, once the master is compromised, all your agents can be easily compromised (IOW, malicious master can execute arbitrary program on agents), so both set-up leaves much to be desired in terms of isolating security breach. Build Publisher Plugin provides another way of doing this, in more secure fashion.  请注意，在这两种情况下，一旦主服务器遭到入侵，您的所有代理都可能很容易受到攻击（IOW，恶意主服务器可以在代理上执行任意程序），因此在隔离安全漏洞方面，这两种设置都有很多不足之处。 Build Publisher Plugin以更安全的方式提供了另一种方法。

## Running Multiple Agents on the Same Machine  在同一台计算机上运行多个代理

Using a well established virtualization infrastructure such as Kernel-based Virtual Machine (KVM), it is quite easy to run multiple agent instances on a single physical node.  Such instances can be running various Linux, *BSD UNIX, Solaris, Windows.  For Windows, one can have them installed as separate Windows services so they can start up on system startup. While the correct use of executors largely obviates the need for multiple agent instances on the same machine, there are some unique use cases to consider:  使用完善的虚拟化基础架构（如基于内核的虚拟机（KVM）），在单个物理节点上运行多个代理程序实例非常容易。 这样的实例可以运行各种Linux，* BSD UNIX，Solaris，Windows。 对于Windows，可以将它们作为单独的Windows服务安装，以便它们可以在系统启动时启动。 虽然正确使用执行程序在很大程度上避免了在同一台机器上需要多个代理程序实例，但还是有一些独特的用例需要考虑：

* You want more configurability between the configured nodes. Say you have one node set to be used as much as possible, and the other node to be used only when needed.  您希望配置的节点之间具有更多可配置性。 假设您有一个节点设置尽可能使用，另一个节点仅在需要时使用。

* You may have multiple Jenkins master installations building different things, and so this configuration would allow you to have agents for more than one master on the same box. That's right, with Jenkins you really can serve two masters.  您可能有多个Jenkins主装置构建不同的东西，因此这种配置允许您在同一个盒子上拥有多个主服务器的代理。 没错，詹金斯你真的可以为两位大师服务。

* You may wish to leverage the easiness of starting/stopping/replacing virtual machines, perhaps in conjunction with Jenkins plugins such as the Libvirt Slaves Plugin.  您可能希望利用启动/停止/替换虚拟机的简便性，可能与Jenkins插件（如Libvirt Slaves Plugin）一起使用。

* You wish to maximize your hardware investment and utilization, at the same time minimizing operating cost (e.g. utility expenses for running idling agents).  您希望最大化您的硬件投资和利用率，同时最大限度地降低运营成本（例如运行空转代理的公用事业费用）。

Follow these steps to get multiple agents working on the same Windows box:  请按照以下步骤使多个代理在同一Windows框上工作：



* Troubleshooting tips  故障排除提示
	* Windows agent service upgrades  Windows代理服务升级
* Other readings  其他读物










