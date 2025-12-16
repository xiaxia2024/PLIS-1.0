import os
import json
import yaml

from kb.kb import KnowledgeBase


class RuleEngine:
    """
    RuleEngine = 静态规则（YAML） + 动态规则（来自 KB）
    """

    def __init__(self, rules_dir="rules", kb_path="kb/patterns.json"):
        self.rules_dir = rules_dir

        # 1️⃣ 加载人工编写的静态规则
        self.static_rules = self.load_static_rules()

        # 2️⃣ 加载知识库
        self.kb = KnowledgeBase(kb_path)

        # 3️⃣ 从 KB 生成动态规则
        self.dynamic_rules = self.load_dynamic_rules()

    # --------------------------------------------------
    # 加载 rules/ 目录下的 YAML 规则
    # --------------------------------------------------
    def load_static_rules(self):
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

    # --------------------------------------------------
    # ⭐ 关键：KB → 动态规则（你问的就是这里）
    # --------------------------------------------------
    def load_dynamic_rules(self):
        """
        将 KB 中学习到的 pattern 转换为 RuleEngine 可用的规则
        """
        rules = []

        for p in self.kb.patterns:
            # 允许人工关闭某些自动规则
            if not p.get("enabled", True):
                continue

            rules.append({
                "id": p.get("id"),
                "name": f"[AUTO] Pattern detected: {p.get('pattern')}",
                "severity": p.get("severity", "low"),
                "patterns": [p.get("pattern")],
                "confidence": p.get("confidence", 0.5),
                "source": "knowledge_base",
                "context": p.get("context", "unknown")
            })

        return rules

    # --------------------------------------------------
    # 规则匹配入口
    # --------------------------------------------------
    def apply_rules(self, parsed_json):
        """
        parsed_json: parser 输出的结构化 JSON
        """
        results = []
        text = json.dumps(parsed_json, ensure_ascii=False).lower()

        # 静态规则 + 动态规则一起参与判定
        all_rules = self.static_rules + self.dynamic_rules

        for rule in all_rules:
            evidence = []

            for pattern in rule.get("patterns", []):
                if pattern and pattern.lower() in text:
                    evidence.append(pattern)

            if not evidence:
                continue

            results.append({
                "id": rule.get("id"),
                "name": rule.get("name"),
                "severity": rule.get("severity"),
                "confidence": rule.get("confidence", 0.5),
                "source": rule.get("source", "static"),
                "context": rule.get("context"),
                "evidence": evidence
            })

        return results
