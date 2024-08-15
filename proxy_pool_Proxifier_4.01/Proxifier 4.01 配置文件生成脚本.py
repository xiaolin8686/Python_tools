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