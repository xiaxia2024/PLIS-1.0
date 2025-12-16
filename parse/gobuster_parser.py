import re
from schema.web_enum_schema import create_endpoint, create_web_enum_result


class GobusterParser:
    def __init__(self, raw_log: str, base_url: str = "http://unknown"):
        self.raw = raw_log
        self.base_url = base_url

    def parse(self):
        endpoints = []

        # Gobuster 行示例：
        # /admin (Status: 301) [Size: 0]
        pattern = re.compile(
            r"(?P<path>/\S+)\s+\(Status:\s+(?P<status>\d+)\)\s+\[Size:\s+(?P<size>\d+)\]"
        )

        for line in self.raw.splitlines():
            m = pattern.search(line)
            if not m:
                continue

            status = int(m.group("status"))
            size = int(m.group("size"))

            tags = []
            confidence = 0.5

            if status == 200:
                tags.append("accessible")
                confidence = 0.9
            elif status in (301, 302):
                tags.append("redirect")
                confidence = 0.6
            elif status == 403:
                tags.append("forbidden")
                confidence = 0.7

            endpoints.append(
                create_endpoint(
                    path=m.group("path"),
                    base_url=self.base_url,
                    status=status,
                    length=size,
                    redirect=status in (301, 302),
                    tags=tags,
                    confidence=confidence,
                    source_tool="gobuster"
                )
            )

        return create_web_enum_result(
            target=self.base_url,
            source="gobuster",
            endpoints=endpoints
        )
