import re

class DirsearchParser:
    def __init__(self, raw_text):
        self.raw = raw_text

    def parse(self):
        results = {
            "scanner": "dirsearch",
            "paths": [],
            "interesting_paths": [],
            "parameters": [],
            "status_codes": {}
        }

        for line in self.raw.splitlines():
            # [200]  /admin/
            m = re.search(r"\[(\d{3})\]\s+(/[^\s]+)", line)
            if not m:
                continue

            status = int(m.group(1))
            path = m.group(2)

            entry = {
                "path": path,
                "status": status
            }

            results["paths"].append(entry)

            results["status_codes"].setdefault(str(status), 0)
            results["status_codes"][str(status)] += 1

            if any(k in path.lower() for k in [
                "admin", "upload", "backup", "login",
                "test", "dev", "api", "include"
            ]):
                results["interesting_paths"].append(entry)

            if "?" in path:
                results["parameters"].append(path)

        return results
