import re
from schema.web_enum_schema import create_endpoint, create_web_enum_result


class DirsearchParser:
    def __init__(self, raw_log: str, base_url: str = "http://unknown"):
        self.raw = raw_log
        self.base_url = base_url

    def parse(self):
        endpoints = []

        # 示例：
        # [200] /admin/ - 3456B
        pattern = re.compile(
            r"\[(?P<status>\d+)\]\s+(?P<path>/\S+)(?:\s+-\s+(?P<size>\d+)B)?"
        )

        for line in self.raw.splitlines():
            m = pattern.search(line)
            if not m:
                continue

            status = int(m.group("status"))
            size = int(m.group("size")) if m.group("size") else None

            tags = []
            confidence = 0.6

            if status == 200:
                tags.append("accessible")
                confidence = 0.9
            elif status == 403:
                tags.append("forbidden")
                confidence = 0.7

            endpoints.append(
                create_endpoint(
                    path=m.group("path"),
                    base_url=self.base_url,
                    status=status,
                    length=size,
                    redirect=False,
                    tags=tags,
                    confidence=confidence,
                    source_tool="dirsearch"
                )
            )

        return create_web_enum_result(
            target=self.base_url,
            source="dirsearch",
            endpoints=endpoints
        )
