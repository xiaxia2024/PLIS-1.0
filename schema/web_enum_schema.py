from datetime import datetime


def create_web_enum_result(
    target: str,
    source: str,
    endpoints: list,
    metadata: dict = None
):
    """
    统一 Web 枚举扫描结果 Schema
    Gobuster / Dirsearch / ffuf 都往这里灌
    """

    statuses = sorted(list({ep.get("status") for ep in endpoints if ep.get("status")}))
    
    return {
        "target": target,
        "source": source,
        "scan_type": "web_enum",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_endpoints": len(endpoints),
            "status_codes": statuses,
            "interesting": sum(
                1 for ep in endpoints
                if ep.get("status") in [200, 401, 403]
            )
        },
        "endpoints": endpoints,
        "metadata": metadata or {}
    }


def create_endpoint(
    path: str,
    base_url: str,
    status: int = None,
    length: int = None,
    method: str = "GET",
    content_type: str = None,
    redirect: bool = False,
    tags: list = None,
    confidence: float = 0.5,
    source_tool: str = None
):
    """
    单个 Web Endpoint 的统一表达
    """

    return {
        "path": path,
        "url": base_url.rstrip("/") + path,
        "method": method,
        "status": status,
        "length": length,
        "content_type": content_type,
        "redirect": redirect,
        "confidence": confidence,
        "source_tool": source_tool,
        "tags": tags or []
    }
