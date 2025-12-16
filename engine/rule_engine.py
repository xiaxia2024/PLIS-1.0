import os
import yaml
import json
import re
from kb.kb import KnowledgeBase


class RuleEngine:
    def __init__(self, rules_dir="rules", kb_path="kb/patterns.json"):
        self.rules_dir = rules_dir

        # 1. 人工编写的静态规则
        self.static_rules = self.load_all_rules()

        # 2. 知识库（自动学习）
        self.kb = KnowledgeBase(kb_path)

        # 3. 从 KB 生成的动态规则
        self.dynamic_rules = self.load_dynamic_rules()

    # ----------------------------------------
    # 加载 rules/ 下的 YAML 静态规则
    # ----------------------------------------
    def load_all_rules(self):
        rules = []

        for root, _, files in os.walk(self.rules_dir):
            for file in files:
                if file.endswith((".yml", ".yaml")):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, list):
                            rules.extend(data)
                        elif isinstance(data, dict):
                            rules.append(data)

        return rules

    # ----------------------------------------
    # 从 KB 中生成“动态规则”
    # ----------------------------------------
    def load_dynamic_rules(self):
        rules = []

        for p in self.kb.patterns:
            if not p.get("enabled", True):
                continue

            rules.append({
                "id": p["id"],
                "name": f"[AUTO] {p['pattern']}",
                "severity": p.get("severity", "low"),
                "patterns": [p["pattern"]],
                "confidence": p.get("confidence", 0.5),
                "source": "knowledge_base"
            })

        return rules

    # ----------------------------------------
    # 规则判定入口
    # ----------------------------------------
    def apply_rules(self, parsed_json):
        results = []
        text = json.dumps(parsed_json).lower()

        all_rules = self.static_rules + self.dynamic_rules

        for rule in all_rules:
            evidence = []

            for p in rule.get("patterns", []):
                if p.lower() in text:
                    evidence.append(p)

            if not evidence:
                continue

            results.append({
                "id": rule.get("id"),
                "name": rule.get("name"),
                "severity": rule.get("severity"),
                "confidence": rule.get("confidence", 0.5),
                "source": rule.get("source", "static"),
                "evidence": evidence
            })

        return results
