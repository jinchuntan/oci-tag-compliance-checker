def parse_required_keys(raw: str):
    return [k.strip() for k in raw.split(",") if k.strip()]


def evaluate(resources, required_keys):
    findings = []
    compliant = 0

    for r in resources:
        tags = r.get("tags", {}) or {}
        missing = [k for k in required_keys if not str(tags.get(k, "")).strip()]

        if missing:
            findings.append({
                "type": r["type"],
                "name": r["name"],
                "ocid": r["ocid"],
                "missing_tags": missing,
            })
        else:
            compliant += 1

    summary = {
        "total_resources": len(resources),
        "compliant": compliant,
        "non_compliant": len(findings),
        "required_keys": required_keys,
    }
    return summary, findings
