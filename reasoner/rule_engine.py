import os
import yaml
import re
import json
#from kb.kb import KnowledgeBase

class RuleEngine:
    def __init__(self, rules_dir="rules"):
        self.rules_dir = rules_dir
        self.rules = self.load_all_rules()

    # -------------------------------------------------------
    # 递归载入 YAML 规则
    # -------------------------------------------------------
    def load_all_rules(self):
        loaded = []
        for root, dirs, files in os.walk(self.rules_dir):
            for file in files:
                if file.endswith(".yml") or file.endswith(".yaml"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or []

                        # 文件格式情况处理
                        if isinstance(data, dict) and "rules" in data:
                            loaded.extend(data["rules"])
                        elif isinstance(data, list):
                            loaded.extend(data)
                        elif isinstance(data, dict):
                            loaded.append(data)

        return loaded

    # -------------------------------------------------------
    # 稳健地 Flatten 文本
    # -------------------------------------------------------
    def flatten_text(self, obj):
        if isinstance(obj, dict):
            return " ".join(self.flatten_text(v) for v in obj.values())
        elif isinstance(obj, list):
            return " ".join(self.flatten_text(i) for i in obj)
        return str(obj)

    # -------------------------------------------------------
    # 简单关键字匹配
    # -------------------------------------------------------
    def match(self, text):
        matches = []
        txt = text.lower()

        for rule in self.rules:
            patterns = rule.get("patterns", [])
            if isinstance(patterns, str):
                patterns = [patterns]

            for p in patterns:
                if p.lower() in txt:
                    matches.append(rule)
                    break
        return matches

    # -------------------------------------------------------
    # 完整规则引擎
    # -------------------------------------------------------
    def apply_rules(self, parsed_json):
        results = []
        text_raw = self.flatten_text(parsed_json).lower()

        for rule in self.rules:
            rule_id = rule.get("id", rule.get("name", "Unknown"))
            name = rule.get("name", "Unnamed Rule")
            severity = rule.get("severity", "info")
            description = rule.get("description", "")
            evidence = []

            # patterns
            patterns = rule.get("patterns", [])
            if isinstance(patterns, str):
                patterns = [patterns]

            # regex
            regex_patterns = rule.get("regex", [])
            if isinstance(regex_patterns, str):
                regex_patterns = [regex_patterns]

            # hints
            hints = rule.get("hints", [])
            if isinstance(hints, str):
                hints = [hints]

            # match
            for p in patterns:
                if p.lower() in text_raw:
                    evidence.append(f"keyword: {p}")

            for r in regex_patterns:
                try:
                    if re.search(r, text_raw):
                        evidence.append(f"regex: {r}")
                except re.error:
                    continue

            for h in hints:
                if h.lower() in text_raw:
                    evidence.append(f"hint: {h}")

            if not evidence:
                continue

            results.append({
                "id": rule_id,
                "name": name,
                "severity": severity,
                "description": description,
                "evidence": evidence
            })

        return results
