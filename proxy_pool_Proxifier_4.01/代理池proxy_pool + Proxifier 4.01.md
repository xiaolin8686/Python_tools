## 项目部署

软件包可通过网络下载

[下载地址](https://github.com/xiaolin8686/Python_tools/releases/download/V1.0.0/proxy_pool_toolkit.zip)

### Linux 配置

1.  防火墙关闭

```bash
systemctl stop firewalld // 关闭防火墙
systemctl disable firewalld // 禁用防火墙
```

2. 安装python3

```
yum install python3 python3-pip
```

3. 关闭selinux

```
vim /etc/selinux/config
# 修改SELINUX的值为disabled后重启系统
SELINUX=disabled
```

### Redis 安装

#### 源码部署	[参考文献](https://www.cnblogs.com/ztxd/articles/16718761.html)

1. 安装依赖

   ~~~bash
   gcc -v
   # 若没有安装，则使用下列命令进行安装
   yum install -y gcc
   ~~~

2. 下载 redis 安装包，并解压

   ~~~bash
   # 下载，我是在root下执行的下载，所以我的下载目录为：/root/redis-6.2.6，这里按照自己的实际情况调整
   wget https://download.redis.io/releases/redis-6.2.6.tar.gz
   # 解压
   tar -xzvf redis-6.2.6.tar.gz -C /usr/local/
   ~~~

3. 进入解压目录并编译

   ~~~bash
   # 进入解压目录
   cd /usr/local/redis-6.2.6
   # 编译
   make
   ~~~

4. 指定安装目录并进行安装

   ~~~bash
   # 指定安装目录为 /usr/local/redis
   make install PREFIX=/usr/local/redis
   ~~~

5. 复制配置文件进行启动

   ~~~bash
   cp /usr/local/redis-6.2.6/redis.conf /usr/local/redis/bin/
   
   # 修改配置文件
   cd /usr/local/redis/bin/
   vi redis.conf
   # 修改内容如下：
   # daemonize 的值从 no 修改成 yes
   # 如果想要设置指定IP连接redis，只需要修改redis.conf文件中bind配置项即可。如果不限IP，将127.0.0.1修改成0.0.0.0即可。
   bind 127.0.0.1 -::1
   
   # 设置密码
   requirepass 123456 //123456是设置的密码
   
   # 启动redis
   ./redis-server redis.conf
   ~~~



**Redis 启动/关闭 脚本**

* 启动脚本

  ~~~bash
  #!/bin/bash
  cd /usr/local/redis/bin/
  nohup ./redis-server redis.conf >/dev/null 2>&1 &
  ~~~

* 关闭脚本

  ~~~bash
  #!/bin/bash
  ps -ef | grep '/usr/local/redis/bin/redis-server' | grep -v grep | awk '{print $2}' | xargs kill -9
  ~~~

**一键部署脚本**

~~~bash
#!/bin/bash
yum install -y gcc

wget https://download.redis.io/releases/redis-6.2.6.tar.gz
tar -xzvf redis-6.2.6.tar.gz -C /usr/local/

cd /usr/local/redis-6.2.6
make

make install PREFIX=/usr/local/redis

cp /usr/local/redis-6.2.6/redis.conf /usr/local/redis/bin/

cat > /usr/local/redis/bin/install.sh <<q
#!/bin/bash
cd /usr/local/redis/bin/
nohup ./redis-server redis.conf >/dev/null 2>&1 &
q

cat > /usr/local/redis/bin/uninstall.sh <<q
#!/bin/bash
ps -ef | grep redis-server | grep -v grep | awk '{print \$2}' | xargs kill -9
q

chmod +x /usr/local/redis/bin/install.sh
chmod +x /usr/local/redis/bin/uninstall.sh
~~~



#### Docker部署 

docker 安装包可以在百度网盘上下载

1. 安装 docker 环境

   ~~~bash
   yum install -y yum-utils
   yum-config-manager \
       --add-repo \
       https://download.docker.com/linux/centos/docker-ce.repo
   yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   systemctl enable docker
   systemctl start docker
   ~~~

2. 更换 docker 源

   ~~~bash
   mkdir -p /etc/docker
   tee /etc/docker/daemon.json <<-'EOF'
   {
    "registry-mirrors": ["https://yytcclg8.mirror.aliyuncs.com"]
   }
   EOF
   systemctl daemon-reload
   systemctl restart docker
   ~~~

3. 设置 docker 代理

   ~~~bash
   # 该网站网络比较慢
   wget https://github.com/xiaolin8686/Linux_tools/releases/download/V1.0/proxy_docker
   chmod +x proxy_docker
   ./proxy_docker -i 192.168.162.1 -p 7890
   systemctl daemon-reload
   systemctl restart docker
   ~~~

4. 安装 redis

   ~~~bash
   docker pull redis
   ~~~

5. 启动 redis

   ~~~bash
   docker run -d --name redis -p 6379:6379 redis --requirepass "pwd"
   -p 端口
   -requirepass "密码"
   ~~~

6. docker 常规命令

   ~~~bash
   docker ps
   # 查看运行容器
   
   docker ps -a
   # 查看全部容器（包括非运行）
   
   docker images
   # 查看docker镜像
   
   docker stop/start/restart f07b3fa4305c
   # 停止/启动/重启 容器
   
   docker start $(docker ps -a | awk '{ print $1}' | tail -n +2)
   # 启动所有docker容器
   
   docker stop $(docker ps -a | awk '{ print $1}' | tail -n +2)
   # 关闭所有docker容器
   
   docker rm $(docker ps -a | awk '{ print $1}' | tail -n +2)
   # 删除所有容器
   
   docker rmi $(docker images | awk '{print $3}' |tail -n +2)
   # 删除所有镜像
   
   ~~~

   

**一键部署脚本**

~~~bash
#!/bin/bash
yum install -y yum-utils
yum-config-manager --add-repo   http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
systemctl enable docker
systemctl start docker
mkdir -p /etc/docker
tee /etc/docker/daemon.json <<-'EOF'
{
 "registry-mirrors": ["https://yytcclg8.mirror.aliyuncs.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker
wget https://github.com/xiaolin8686/Linux_tools/releases/download/V1.0/proxy_docker
chmod +x proxy_docker
./proxy_docker -i 192.168.162.1 -p 7890
systemctl daemon-reload
systemctl restart docker
docker pull redis
~~~

### Proxy_Pool 安装

1. 下载项目

   ~~~bash
   git clone https://github.com/jhao104/proxy_pool.git
   ~~~

   或直接去这个地址上下载 https://github.com/jhao104/proxy_pool

2. 解压项目，下载依赖    若是通过 git 抓取项目的，可跳过解压这一步骤

   ~~~bash
   tar -zxvf proxy_pool-2.4.1.tar.gz
   cd proxy_pool-2.4.1
   python3 -m pip install -r requirements.txt
   pip3 install --upgrade APScheduler
   pip3 install --upgrade Flask Jinja2
   ~~~

3. 设置配置

   ~~~bash
   vim setting.py
   
   # 修改配置信息
   DB_CONN = 'redis://:pwd@127.0.0.1:6379/0' #修改对应的配置信息
   ~~~

#### 项目启动脚本

* 开启脚本

  ~~~bash
  #!/usr/bin/env bash
  nohup python3 proxyPool.py server >/dev/null 2>&1 &
  nohup python3 proxyPool.py schedule >/dev/null 2>&1 &
  ~~~

* 关闭脚本

  ~~~bash
  #!/bin/bash
  ps -ef | grep proxyPool.py  | grep -v grep | awk '{print $2}' | xargs kill -9
  ~~~



**一键部署脚本**

~~~bash
tar -zxvf proxy_pool-2.4.1.tar.gz
cd proxy_pool-2.4.1
python3 -m pip install -r requirements.txt
pip3 install --upgrade APScheduler
pip3 install --upgrade Flask Jinja2

cat > install.sh <<q
#!/usr/bin/env bash
nohup python3 proxyPool.py server >/dev/null 2>&1 &
nohup python3 proxyPool.py schedule >/dev/null 2>&1 &
q

cat > uninstall.sh <<q
#!/bin/bash
ps -ef | grep proxyPool.py | grep -v grep | awk '{print \$2}' | xargs kill -9
q

chmod +x install.sh
chmod +x uninstall.sh
~~~

### 生成脚本

~~~python
# -*- coding:utf8 -*-
import redis
import json
from xml.etree import ElementTree

def RedisProxyGet():
    ConnectString = []
    # 更改配置文件
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password='pwd', decode_responses=True)
    use_proxy = redis.Redis(connection_pool=pool)
    key = use_proxy.hkeys('use_proxy')
    for temp in key:
        try:
            ConnectString.append(json.loads(use_proxy.hget('use_proxy',temp)))
        except json.JSONDecodeError: # JSON解析异常处理
            pass
    return ConnectString

def xmlOutputs(data):
    i = 101
    ProxyIDList = []
# ProxifierProfile根
    ProxifierProfile = ElementTree.Element("ProxifierProfile")
    ProxifierProfile.set("version", str(i))
    ProxifierProfile.set("platform", "Windows")
    ProxifierProfile.set("product_id", "0")
    ProxifierProfile.set("product_minver", "310")

# Options 节点
    Options = ElementTree.SubElement(ProxifierProfile, "Options")

    # Options.Resolve
    Resolve = ElementTree.SubElement(Options, "Resolve")
    # Options.Resolve.AutoModeDetection
    AutoModeDetection = ElementTree.SubElement(Resolve, "AutoModeDetection")
    AutoModeDetection.set("enabled", "false")

    # Options.Resolve.ViaProxy
    ViaProxy = ElementTree.SubElement(Resolve, "ViaProxy")
    ViaProxy.set("enabled", "false")

    # Options.Resolve.ViaProxy.TryLocalDnsFirst
    TryLocalDnsFirst = ElementTree.SubElement(ViaProxy, "TryLocalDnsFirst")
    TryLocalDnsFirst.set("enabled", "false")

    # Options.Resolve.ExclusionList
    ExclusionList = ElementTree.SubElement(Resolve, "ExclusionList")
    ExclusionList.text = "%ComputerName%; localhost; *.local"

    # Options.*
    Encryption = ElementTree.SubElement(Options, "Encryption")
    Encryption.set("mode", 'basic')
    Encryption = ElementTree.SubElement(Options, "HttpProxiesSupport")
    Encryption.set("enabled", 'true')
    Encryption = ElementTree.SubElement(Options, "HandleDirectConnections")
    Encryption.set("enabled", 'false')
    Encryption = ElementTree.SubElement(Options, "ConnectionLoopDetection")
    Encryption.set("enabled", 'true')
    Encryption = ElementTree.SubElement(Options, "ProcessServices")
    Encryption.set("enabled", 'false')
    Encryption = ElementTree.SubElement(Options, "ProcessOtherUsers")
    Encryption.set("enabled", 'false')

    # ProxyList
    ProxyList = ElementTree.SubElement(ProxifierProfile, "ProxyList")
    for temp in data:
        i += 1  # 从101开始增加
        # ProxyList.Proxy
        Proxy = ElementTree.SubElement(ProxyList, "Proxy")
        Proxy.set("id", str(i))

        if not temp['https']:
            Proxy.set("type", "HTTP")
        else:
            Proxy.set("type", "HTTPS")
            Proxy.text = str(i)
            ProxyIDList.append(i)

        # ProxyList.Proxy.Address
        Address = ElementTree.SubElement(Proxy, "Address")
        Address.text = temp['proxy'].split(":", 1)[0]

        # ProxyList.Proxy.Port
        Port = ElementTree.SubElement(Proxy, "Port")
        Port.text = temp['proxy'].split(":", 1)[1]

        # ProxyList.Proxy.Options
        Options = ElementTree.SubElement(Proxy, "Options")
        Options.text = "48"

    # RuleList
    ChainList = ElementTree.SubElement(ProxifierProfile, "ChainList")

    # RuleList.Chain
    Chain = ElementTree.SubElement(ChainList, "Chain")
    Chain.set("id", str(i))
    Chain.set("type", "simple")

    # RuleList.Chain.Name
    Name = ElementTree.SubElement(Chain, "Name")
    Name.text="AgentPool"

    # RuleList.Chain.Proxy
    for temp_id in ProxyIDList:
        Proxy = ElementTree.SubElement(Chain, "Proxy")
        Proxy.set("enabled", "true")
        Proxy.text=str(temp_id)
    # RuleList
    RuleList = ElementTree.SubElement(ProxifierProfile, "RuleList")

    # Rule
    Rule = ElementTree.SubElement(RuleList, "Rule")
    Rule.set("enabled", "true")
    Name = ElementTree.SubElement(Rule,"Name")
    Applications = ElementTree.SubElement(Rule,"Applications")
    Action = ElementTree.SubElement(Rule,"Action")

    Name.text="御剑后台扫描工具.exe [auto-created]"
    Applications.text="御剑后台扫描工具.exe"
    Action.set("type","Direct")

    # Rule
    Rule = ElementTree.SubElement(RuleList, "Rule")
    Rule.set("enabled", "true")
    Name = ElementTree.SubElement(Rule,"Name")
    Targets = ElementTree.SubElement(Rule,"Targets")
    Action = ElementTree.SubElement(Rule,"Action")

    Name.text="Localhost"
    Targets.text="localhost; 127.0.0.1; %ComputerName%"
    Action.set("type", "Direct")

    # Rule
    Rule = ElementTree.SubElement(RuleList, "Rule")
    Rule.set("enabled", "true")
    Name = ElementTree.SubElement(Rule, "Name")
    Action = ElementTree.SubElement(Rule, "Action")
    Name.text = "Default"
    Action.text = "102"
    Action.set("type", "Proxy")

    tree = ElementTree.ElementTree(ProxifierProfile)
    tree.write("ProxifierConf.ppx", encoding="UTF-8", xml_declaration=True)
if __name__ == '__main__':
    proxy_data = RedisProxyGet()
    xmlOutputs(proxy_data)
    print("ProxifierConf.ppx配置文件创建完成....")
~~~





































