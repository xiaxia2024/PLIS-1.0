import re

class GobusterParser:
    def __init__(self, raw_text):
        self.raw = raw_text

    def parse(self):
        results = {
            "scanner": "gobuster",
            "paths": [],
            "interesting_paths": [],
            "parameters": [],
            "status_codes": {}
        }

        for line in self.raw.splitlines():
            # /admin (Status: 301) [Size: 0]
            m = re.search(r"(/[\w\-/\.]+)\s+\(Status:\s*(\d+)\)", line)
            if not m:
                continue

            path = m.group(1)
            status = int(m.group(2))

            entry = {
                "path": path,
                "status": status
            }

            results["paths"].append(entry)

            # 统计状态码
            results["status_codes"].setdefault(str(status), 0)
            results["status_codes"][str(status)] += 1

            # 可疑路径规则（为 RuleEngine 准备）
            if any(k in path.lower() for k in [
                "admin", "upload", "backup", "test",
                "old", "dev", "api", "include"
            ]):
                results["interesting_paths"].append(entry)

            # 参数检测（LFI / SQLi / RFI）
            if "?" in path:
                results["parameters"].append(path)

        return results
