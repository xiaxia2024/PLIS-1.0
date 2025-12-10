import os
import yaml
import re
import json


class RuleEngine:
    def __init__(self, rule_folder="rules"):
        self.rule_folder = rule_folder
        self.rules = self.load_all_rules()

    # -------------------------------------------------------
    # 载入所有 YAML 规则
    # -------------------------------------------------------
    def load_all_rules(self):
        rules = []

        for file in os.listdir(self.rule_folder):
            if file.endswith(".yaml") or file.endswith(".yml"):
                with open(os.path.join(self.rule_folder, file), "r") as f:
                    data = yaml.safe_load(f)

                    # 兼容单规则与多规则 YAML 格式
                    if isinstance(data, dict) and "rules" in data:
                        rules.extend(data["rules"])
                    else:
                        rules.append(data)

        return rules

    # -------------------------------------------------------
    # 规则判断
    # -------------------------------------------------------
    def apply_rules(self, parsed_json):
        """
        parsed_json: 来自 parser 的结构化数据
        """
        results = []
        text_raw = json.dumps(parsed_json).lower()

        for rule in self.rules:
            rule_id = rule.get("id", rule.get("name", "Unknown"))
            name = rule.get("name", "Unnamed Rule")
            severity = rule.get("severity", "info")
            patterns = rule.get("patterns", [])
            regex_patterns = rule.get("regex", [])
            hints = rule.get("hints", [])
            evidence = []

            # -----------------------
            # 1. 关键字匹配
            # -----------------------
            for p in patterns:
                if p.lower() in text_raw:
                    evidence.append(f"keyword: {p}")

            # -----------------------
            # 2. 正则匹配
            # -----------------------
            for pattern in regex_patterns:
                try:
                    if re.search(pattern, text_raw):
                        evidence.append(f"regex: {pattern}")
                except re.error:
                    continue

            # -----------------------
            # 3. hints（轻量特征命中）
            # -----------------------
            for h in hints:
                if h.lower() in text_raw:
                    evidence.append(f"hint: {h}")

            # -----------------------
            # 如果 evidence 为空 → 规则未命中
            # -----------------------
            if not evidence:
                continue

            # -----------------------
            # 命中规则
            # -----------------------
            results.append({
                "id": rule_id,
                "name": name,
                "severity": severity,
                "evidence": evidence,
            })

        return results

    # -------------------------------------------------------
    # 自动扩展（未来版本）——从新样本自动生成新规则
    # -------------------------------------------------------
    def evolve_rules(self, new_patterns, rule_name="AutoLearnedPattern"):
        """
        未来可用：将新发现的模式写入 KB 或规则库
        """
        auto_rule = {
            "id": f"auto_{rule_name}",
            "name": rule_name,
            "severity": "low",
            "patterns": new_patterns,
            "description": "Automatically learned rule",
        }

        # 写入 auto_rules.yaml
        out_path = os.path.join(self.rule_folder, "auto_rules.yaml")
        with open(out_path, "a") as f:
            yaml.dump({"rules": [auto_rule]}, f)

        return auto_rule
