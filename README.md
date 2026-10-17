# OCI Tag Compliance Checker

A standalone Python tool using the OCI Python SDK to inventory core resources and evaluate tag compliance.

## What it checks

- Compute instances
- VCNs
- Subnets

It verifies required freeform tags (configurable via `.env`) and produces:

- JSON report (machine-readable)
- Markdown report (human-readable)

Both reports are uploaded to OCI Object Storage for evidence and review.

## Prerequisites

- Python 3.11 and access to an OCI tenancy.
- An OCI SDK configuration profile in `~/.oci/config` (on Windows, `%USERPROFILE%\.oci\config`). See the [OCI Python SDK configuration guide](https://docs.oracle.com/en-us/iaas/tools/python/latest/configuration.html).
- Permissions to read the target compute/network resources and Object Storage namespace, inspect the report bucket, and upload report objects. If the bucket does not exist, the tool also needs permission to create it.

## Setup (Windows PowerShell)

Run these commands from the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
python .\src\main.py
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` directly for the `python` commands above; changing the execution policy is not required.

## Setup (macOS / Linux)

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and fill in the required values before running:
python src/main.py
```

## Configuration

| Variable | Required | Purpose |
| --- | --- | --- |
| `OCI_COMPARTMENT_OCID` | Yes | Compartment containing the resources to check and any report bucket the tool creates. |
| `OCI_BUCKET_NAME` | Yes | Object Storage bucket for the generated reports. |
| `REQUIRED_TAG_KEYS` | Yes | Comma-separated freeform tag keys, such as `owner,environment,cost_center`. |
| `OCI_PROFILE` | No | Profile in the OCI SDK config file; defaults to `DEFAULT`. |
| `OCI_OBJECT_PREFIX` | No | Uploaded report prefix; defaults to `tag-compliance`. |

The template leaves the compartment and bucket blank so they must be supplied before the tool runs. Set the tag keys to match your own policy. Credentials and signing keys belong in your local OCI SDK configuration, not in the repository.

The tool reads resource tags but does not modify them. It saves JSON and Markdown files to `reports/`, creates a private Object Storage bucket if needed, and uploads both files. Running it therefore makes Object Storage writes; it is not a local-only dry run.

## Troubleshooting

- **Missing env var:** confirm `.env` exists at the repository root and the named value is non-empty.
- **Profile/configuration error:** check that `OCI_PROFILE` names a profile in `~/.oci/config` and that its signing-key path is valid.
- **Authorization or bucket error:** check the configured compartment, region, bucket name, and the permissions listed above. Local reports may already exist in `reports/` if an upload fails.

## Output
<img width="940" height="131" alt="image" src="https://github.com/user-attachments/assets/bced8ea5-ba06-4b57-9918-4f5c5445e5d4" />
<img width="940" height="449" alt="image" src="https://github.com/user-attachments/assets/2c27b6ca-9eea-448f-bf37-1d52a850a832" />


