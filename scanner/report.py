import json
import datetime as datetime



def generate_json(findings, target, path = "report.json"):
    data = {
        "target": target,
        "scanned_at":datetime.now.isoformat(),
        "total_findings": len(findings),
        "findings": findings,
    }
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False, indent=2)
    return path