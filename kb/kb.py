# kb/kb.py
import json
import os
from datetime import datetime


class KnowledgeBase:
    """
    PLIS Knowledge Base
    - 存储自动学习到的漏洞特征（signatures）
    - 为 RuleEngine 提供动态规则素材
    """

    def __init__(self, kb_path="kb/signatures.json"):
        self.kb_path = kb_path
        self.data = {
            "updated_at": None,
            "signatures": []
        }
        self._load()

    # --------------------------------------------------
    # 加载 KB
    # --------------------------------------------------
    def _load(self):
        if os.path.exists(self.kb_path):
            try:
                with open(self.kb_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                pass

    # --------------------------------------------------
    # 保存 KB
    # --------------------------------------------------
    def _save(self):
        self.data["updated_at"] = datetime.utcnow().isoformat() + "Z"
        os.makedirs(os.path.dirname(self.kb_path), exist_ok=True)

        with open(self.kb_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    # --------------------------------------------------
    # 核心接口：新增 signature
    # --------------------------------------------------
    def add_signature(self, signature):
        """
        signature: str
        """
        if not signature:
            return False

        signature = signature.strip().lower()

        if signature in self.data["signatures"]:
            return False

        self.data["signatures"].append(signature)
        self._save()
        return True

    # --------------------------------------------------
    # 提供给 RuleEngine 的接口
    # --------------------------------------------------
    def get_signatures(self):
        return self.data.get("signatures", [])
