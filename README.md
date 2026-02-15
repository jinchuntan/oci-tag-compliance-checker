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

## Setup (Windows PowerShell)

```powershell
C:\Users\nigel\AppData\Local\Programs\Python\Python311\python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
notepad .env
python .\src\main.py
```
