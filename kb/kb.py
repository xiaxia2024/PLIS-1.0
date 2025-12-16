import json
import os
from datetime import datetime


class KnowledgeBase:
    def __init__(self, kb_path="kb/patterns.json"):
        self.kb_path = kb_path
        self.patterns = self.load()

    def load(self):
        if not os.path.exists(self.kb_path):
            return []
        with open(self.kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        with open(self.kb_path, "w", encoding="utf-8") as f:
            json.dump(self.patterns, f, indent=2)

    # -------------------------------------------------
    # 自动学习：从 endpoints 中提炼“候选模式”
    # -------------------------------------------------
    def learn_from_web_enum(self, parsed_json):
        if parsed_json.get("scan_type") != "web_enum":
            return

        for ep in parsed_json.get("endpoints", []):
            path = ep.get("path")
            status = ep.get("status")

            if not path or status not in (200, 401, 403):
                continue

            self._add_or_update_pattern(
                pattern=path,
                context="web_enum",
                severity="medium",
                confidence=ep.get("confidence", 0.5)
            )

        self.save()

    def _add_or_update_pattern(self, pattern, context, severity, confidence):
        now = datetime.utcnow().isoformat() + "Z"

        for p in self.patterns:
            if p["pattern"] == pattern and p["context"] == context:
                p["evidence_count"] += 1
                p["last_seen"] = now
                p["confidence"] = min(0.95, p["confidence"] + 0.05)
                return

        self.patterns.append({
            "id": f"auto_{context}_{pattern.strip('/').replace('/', '_')}",
            "pattern_type": "path",
            "pattern": pattern,
            "context": context,
            "severity": severity,
            "confidence": confidence,
            "evidence_count": 1,
            "source": "auto-learn",
            "first_seen": now,
            "last_seen": now,
            "enabled": True
        })
