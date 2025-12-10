import re
import json

class NmapParser:
    def __init__(self, text):
        self.text = text
        self.data = {
            "ports": [],
            "services": [],
            "hostname": None,
            "domain": None,
            "os": None,
            "keywords": []
        }

    # 主函数
    def parse(self):
        self.parse_ports()
        self.parse_host_info()
        self.extract_keywords()
        return self.data

    # ============================
    # 1. 解析端口 + 服务 + 版本
    # ============================
    def parse_ports(self):
        """
        匹配格式：
        53/tcp   open  domain        Simple DNS Plus
        88/tcp   open  kerberos-sec  Microsoft Windows Kerberos
        """
        pattern = re.compile(
            r"(\d+)/(tcp|udp)\s+open\s+([\w\-\?]+)\s*(.*)"
        )

        matches = pattern.findall(self.text)

        for port, proto, service, version in matches:
            self.data["ports"].append(f"{port}/{service}")
            if version:
                self.data["services"].append(version.strip())

    # ============================
    # 2. 解析主机信息（域名、OS、主机名）
    # ============================
    def parse_host_info(self):
        # DNS Domain
        domain_match = re.search(r"DNS_Domain_Name:\s+([^\s]+)", self.text)
        if domain_match:
            self.data["domain"] = domain_match.group(1).strip()

        # Hostname
        host_match = re.search(r"DNS_Computer_Name:\s+([^\s]+)", self.text)
        if host_match:
            self.data["hostname"] = host_match.group(1).strip()

        # Windows OS Info
        os_match = re.search(r"OS:\s+Windows", self.text)
        if os_match:
            self.data["os"] = "Windows"

    # ============================
    # 3. 自动聚合关键词（自动进化基础）
    # ============================
    def extract_keywords(self):
        keywords = []

        word_bank = [
            "kerberos", "ldap", "smb", "rpc", "rdp",
            "active directory", "windows", "terminal services"
        ]

        for w in word_bank:
            if w.lower() in self.text.lower():
                keywords.append(w)

        self.data["keywords"] = keywords


# ====== 调试代码（可删） ======

if __name__ == "__main__":
    #base = os.path.dirname(os.path.abspath(__file__))   # 当前文件所在路径
    #log_path = os.path.join(base, "..", "demo.log")     # 读取上一级目录的 demo.log

    #with open(log_path, "r") as f:
    #    raw = f.read()
    
    with open("demo.log", "r") as f: #在kali直接运行namp_parser.py 执行demo.log
        raw = f.read()

    parser = NmapParser(raw)
    result = parser.parse()

    print(json.dumps(result, indent=4))
