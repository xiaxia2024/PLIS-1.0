# reasoner/reasoner.py
# 推理引擎（Vulnerability Reasoner）

import json
from datetime import datetime


class Reasoner:
    """
    Reasoner for PLIS-1.0
    输入:
        - parsed_json: parser 输出的结构化字典
        - rule_hits: rule_engine.apply_rules(...) 的输出列表
    输出:
        - machine_result: dict (可序列化为 JSON)
    """

    def __init__(self):
        pass

    # -------------------------------------------------------
    # 核心：根据规则命中生成推理路径
    # -------------------------------------------------------
    def generate_reasoning(self, parsed_json, rule_hits):
        reasoning_paths = []

        for hit in rule_hits:
            path = {
                "id": hit.get("id", ""),
                "name": hit.get("name", "Unnamed Rule"),
                "severity": hit.get("severity", "info"),
                "why": self._explain_why(hit),
                "evidence": hit.get("evidence", []),
                "confidence": self._calculate_confidence(hit),
            }
            reasoning_paths.append(path)

        return reasoning_paths

    # -------------------------------------------------------
    # WHY：推理解释
    # -------------------------------------------------------
    def _explain_why(self, hit):
        """
        根据 rule_engine.py 的输出解释 WHY
        """
        evid = hit.get("evidence", [])

        if not evid:
            return "No evidence found."

        # 简单解释合成
        why = " | ".join(
            [f"Matched by {e}" for e in evid]
        )

        return f"Rule triggered because: {why}"

    # -------------------------------------------------------
    # Confidence：简单可信度评分（后期可升级 AI）
    # -------------------------------------------------------
    def _calculate_confidence(self, hit):
        """
        简单信度逻辑：命中特征越多，可信度越高
        """
        e = hit.get("evidence", [])

        if len(e) == 1:
            return 0.6
        elif len(e) == 2:
            return 0.75
        elif len(e) >= 3:
            return 0.9
        return 0.5

    # -------------------------------------------------------
    # 对外入口：生成完整 JSON 输出
    # -------------------------------------------------------
    def build_machine_output(self, parsed_json, rule_hits):
        reasoning = self.generate_reasoning(parsed_json, rule_hits)

        machine = {
            "timestamp": datetime.utcnow().isoformat(),
            "targets": parsed_json.get("targets", parsed_json.get("ip", "")),
            "rules_triggered": len(rule_hits),
            "reasoning": reasoning,
        }

        return machine


# -------------------------------------------------------
# 便捷运行（你可选）
# -------------------------------------------------------
if __name__ == "__main__":
    sample_parsed = {"ports": ["80/http"], "services": ["Apache"]}
    sample_hits = [
        {
            "id": "SQLI-001",
            "name": "SQL Injection Detected",
            "severity": "high",
            "evidence": ["keyword: select", "regex: union.*select"],
        }
    ]

    r = Reasoner()
    out = r.build_machine_output(sample_parsed, sample_hits)
    print(json.dumps(out, indent=4))
