```
它完成完整流程：
读取 .log 输入
调用 parser（例如 nmap_parser.py）
加载规则引擎（rules/ 下的 YAML）
执行漏洞判定
调用 reasoning engine 给出漏洞原因
输出最终结构化 JSON
可选：写入漏洞知识库（KB）
```

import json
import os
import yaml

# 导入你的 parser
from parse.nmap_parser import NmapParser


class RuleEngine:
    def __init__(self, rule_folder="rules"):
        self.rules = self.load_rules(rule_folder)

    def load_rules(self, folder):
        rules = []
        for file in os.listdir(folder):
            if file.endswith(".yaml"):
                with open(os.path.join(folder, file), "r") as f:
                    rules.append(yaml.safe_load(f))
        return rules

    def apply_rules(self, parsed_json):
        findings = []

        for rule in self.rules:
            rule_name = rule.get("name")
            match_keywords = rule.get("match_keywords", [])

            for kw in match_keywords:
                if kw.lower() in json.dumps(parsed_json).lower():
                    findings.append(rule_name)
                    break
        return findings


class Reasoner:
    def explain(self, rule_hits, parsed_json):
        explanations = []

        for hit in rule_hits:
            text = f"检测到规则: {hit} → 因为相关关键字出现在扫描数据中"
            explanations.append(text)

        return explanations


class Engine:
    def __init__(self, log_path):
        self.log_path = log_path
        self.result = {}

    def run(self):
        # 读取 log 文件
        with open(self.log_path, "r") as f:
            raw = f.read()

        # 1. 解析 Log → JSON
        parser = NmapParser(raw)
        parsed_json = parser.parse()

        # 2. 加载 Rule Engine
        rule_engine = RuleEngine()

        # 3. 规则匹配
        rule_hits = rule_engine.apply_rules(parsed_json)

        # 4. 推理解释
        reasoner = Reasoner()
        explanations = reasoner.explain(rule_hits, parsed_json)

        # 5. 整合结果
        self.result = {
            "parsed": parsed_json,
            "rule_hits": rule_hits,
            "reasoning": explanations
        }

        return self.result


if __name__ == "__main__":
    # 自动获取 demo.log 路径（PLIS/ 下）
    base = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base, "demo.log")

    engine = Engine(log_path)
    output = engine.run()

    print(json.dumps(output, indent=4))

