# renderer/output_renderer.py
# 输出模块：将 Reasoner 的 machine_output 转换为
# JSON（机器可读）和 Markdown（人类可读）

import json
from datetime import datetime

class OutputRenderer:
    """
    Output Renderer for PLIS-1.0
    输入:
        machine_output = reasoner.build_machine_output(...)
    输出:
        - JSON
        - Markdown
    """

    def __init__(self):
        pass

    # -------------------------------------------------------
    # JSON 输出（原样返回）
    # -------------------------------------------------------
    def to_json(self, machine_output, pretty=True):
        if pretty:
            return json.dumps(machine_output, indent=4, ensure_ascii=False)
        return json.dumps(machine_output)

    # -------------------------------------------------------
    # Markdown 输出（OSCP 风格 write-up）
    # -------------------------------------------------------
    def to_markdown(self, machine_output):
        md = []
        md.append(f"# 🛡️ PLIS Vulnerability Analysis Report")
        md.append(f"**Generated**: {machine_output.get('timestamp')} UTC\n")

        target = machine_output.get("targets", "Unknown Target")
        md.append(f"## 🎯 Target")
        md.append(f"- `{target}`\n")

        rule_count = machine_output.get("rules_triggered", 0)
        md.append(f"## 📌 Overview")
        md.append(f"- Number of rules triggered: **{rule_count}**\n")

        md.append("## 🔍 Vulnerability Details\n")

        for r in machine_output.get("reasoning", []):
            md.append(f"### {r.get('name')} ({r.get('severity')})")
            md.append(f"**Rule ID:** `{r.get('id')}`")
            md.append(f"**Confidence:** `{r.get('confidence')}`\n")
            md.append(f"#### 🧠 Why")
            md.append(f"{r.get('why')}\n")

            md.append(f"#### 🔬 Evidence")
            for e in r.get("evidence", []):
                md.append(f"- {e}")
            md.append("\n---\n")

        return "\n".join(md)


# -------------------------------------------------------
# 可选的 Debug 运行
# -------------------------------------------------------
if __name__ == "__main__":
    sample_machine = {
        "timestamp": datetime.utcnow().isoformat(),
        "targets": "10.10.10.10",
        "rules_triggered": 1,
        "reasoning": [
            {
                "id": "SQLI-001",
                "name": "SQL Injection",
                "severity": "high",
                "why": "Rule triggered because: keyword: select | regex: union.*select",
                "evidence": ["keyword: select", "regex: union.*select"],
                "confidence": 0.90
            }
        ]
    }

    renderer = OutputRenderer()
    print(renderer.to_markdown(sample_machine))
