import json
from datetime import datetime
from pathlib import Path


def ts_utc():
    return datetime.utcnow().strftime("%Y-%m-%d_%H%M%S_UTC")


def write_json(payload, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_md(summary, findings, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# OCI Tag Compliance Report")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Total resources: {summary['total_resources']}")
    lines.append(f"- Compliant: {summary['compliant']}")
    lines.append(f"- Non-compliant: {summary['non_compliant']}")
    lines.append(f"- Required tags: {', '.join(summary['required_keys'])}")
    lines.append("")
    lines.append("## Non-compliant Resources")
    if not findings:
        lines.append("No non-compliant resources found.")
    else:
        lines.append("| Type | Name | Missing Tags |")
        lines.append("|---|---|---|")
        for f in findings:
            lines.append(f"| {f['type']} | {f['name']} | {', '.join(f['missing_tags'])} |")

    out_path.write_text("\n".join(lines), encoding="utf-8")
