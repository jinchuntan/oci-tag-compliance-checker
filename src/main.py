import os
from pathlib import Path

import oci
from dotenv import load_dotenv

from oci_helpers import get_config_and_signer, ensure_bucket, upload_file
from resources import get_instances, get_vcns_and_subnets
from compliance import parse_required_keys, evaluate
from report import ts_utc, write_json, write_md


def require(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise SystemExit(f"ERROR: Missing env var: {name}")
    return v


def main():
    load_dotenv()

    compartment_id = require("OCI_COMPARTMENT_OCID")
    bucket_name = require("OCI_BUCKET_NAME")
    prefix = os.getenv("OCI_OBJECT_PREFIX", "tag-compliance")
    required_keys = parse_required_keys(require("REQUIRED_TAG_KEYS"))

    config, signer = get_config_and_signer()

    os_client = oci.object_storage.ObjectStorageClient(config, signer=signer)
    namespace = os_client.get_namespace().data

    resources = []
    resources += get_instances(config, signer, compartment_id)
    resources += get_vcns_and_subnets(config, signer, compartment_id)

    summary, findings = evaluate(resources, required_keys)

    stamp = ts_utc()
    reports_dir = Path("reports")
    json_path = reports_dir / f"tag_compliance_{stamp}.json"
    md_path = reports_dir / f"tag_compliance_{stamp}.md"

    write_json({"summary": summary, "findings": findings}, json_path)
    write_md(summary, findings, md_path)

    status = ensure_bucket(os_client, namespace, compartment_id, bucket_name)
    upload_file(os_client, namespace, bucket_name, f"{prefix}/{json_path.name}", str(json_path))
    upload_file(os_client, namespace, bucket_name, f"{prefix}/{md_path.name}", str(md_path))

    print("Compliance check complete.")
    print(f"Bucket: {bucket_name} ({status})")
    print(f"Total resources: {summary['total_resources']}")
    print(f"Non-compliant: {summary['non_compliant']}")
    print(f"Uploaded: {prefix}/{json_path.name}")
    print(f"Uploaded: {prefix}/{md_path.name}")


if __name__ == "__main__":
    main()
