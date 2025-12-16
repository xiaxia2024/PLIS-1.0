import json
import os
import sys
from datetime import datetime

# --------------------------
# 导入组件
# --------------------------
from parse.nmap_parser import NmapParser
from engine.rule_engine import RuleEngine
from engine.reasoner import Reasoner
from renderer.output_renderer import OutputRenderer
from kb.kb import KnowledgeBase
from parse.gobuster_parser import GobusterParser
from parse.dirsearch_parser import DirsearchParser


# ============================================================
# 自动选择合适 parser（未来支持 gobuster/httpx/nikto…）
# ============================================================
def auto_select_parser(log_text):
    """
    根据特征自动选择 parser
    """

    # Nmap 的典型特征：
    if "Nmap scan report" in log_text or "/tcp" in log_text:
        return "nmap"
    # Gobuster 的典型特征：
    if "Gobuster" in log_text or "(Status:" in log_text: 
        return "gobuster"
    # dirsearch 的典型特征：
    if "[200]" in log_text and "dirsearch" in log_text.lower():
        return "dirsearch"

    return "unknown"


# ============================================================
# 主引擎
# ============================================================
class Engine:
    def __init__(self, log_path, rules_dir="rules"):
        self.log_path = log_path
        self.rules_dir = rules_dir

        self.result = {}
        self.kb = KnowledgeBase()

        self.parser = None
        self.parsed_json = None
        self.rule_hits = None
        self.reasoning_output = None
        self.final_output = None

    # --------------------------
    # 运行 PLIS 全流程
    # --------------------------
    def run(self):

        # --------------------------------------------
        # Step 1. 读取 log 文件
        # --------------------------------------------
        if not os.path.exists(self.log_path):
            raise FileNotFoundError(f"Log file not found: {self.log_path}")

        with open(self.log_path, "r", encoding="utf-8") as f:
            raw_log = f.read()

        # --------------------------------------------
        # Step 2. 自动选择 parser
        # --------------------------------------------
        parser_type = auto_select_parser(raw_log)

        if parser_type == "nmap":
            self.parser = NmapParser(raw_log)

        elif parser_type == "gobuster":
            self.parser = GobusterParser(raw_log)
        elif parser_tyep == "dirsearch":
            self.parser = DirsearchParser(raw_log)

        else:
            raise ValueError("未知日志类型，无法解析“）

        # --------------------------------------------
        # Step 3. parser 输出结构化 JSON
        # --------------------------------------------
        self.parsed_json = self.parser.parse()

        # --------------------------------------------
        # Step 4. Rule Engine 匹配漏洞
        # --------------------------------------------
        rule_engine = RuleEngine(self.rules_dir)
        self.rule_hits = rule_engine.apply_rules(self.parsed_json)

        # --------------------------------------------
        # Step 5. Reasoner 推理 WHY
        # --------------------------------------------
        reasoner = Reasoner()
        self.reasoning_output = reasoner.build_machine_output(
            parsed_json=self.parsed_json,
            rule_engine = RuleEngine(rules_dir="rules"),
            rule_hits = rule_engine.apply_rules(parsed_json),

            target=self.parsed_json.get("target", "unknown")
        )

        # --------------------------------------------
        # Step 5.6. 自动学习阶段(new add)
        # --------------------------------------------
        self.auto_learn(self.parsed_json, self.rule_hits)

        # --------------------------------------------
        # Step 6. Renderer 输出
        # --------------------------------------------
        renderer = OutputRenderer()

        json_out = renderer.to_json(self.reasoning_output, pretty=True)
        md_out = renderer.to_markdown(self.reasoning_output)

        # 保存输出
        with open("machine.json", "w", encoding="utf-8") as f:
            f.write(json_out)

        with open("report.md", "w", encoding="utf-8") as f:
            f.write(md_out)

        return {
            "parsed": self.parsed_json,
            "rule_hits": self.rule_hits,
            "reasoning": self.reasoning_output
        }

    def auto_learn(self, parsed_json, rule_hits):
        keywords = []

        for host in parsed_json.get("hosts", []):
            for port in host.get("ports", []):
                service = port.get("service")
                if service:
                    keywords.append(service.lower())

                banner = port.get("banner")
                if banner:
                    keywords.append(banner[:50].lower())

        for key in parsed_json.keys():
            keywords.append(key.lower())

        keywords = set(keywords)

        for kw in keywords:
            self.kb.add_signature(kw)


# ============================================================
# CLI 入口
# ============================================================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("用法: python3 engine.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]

    engine = Engine(log_file)
    engine.run()
