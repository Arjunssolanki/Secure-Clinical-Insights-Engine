# Secure-Clinical-Insights-Engine

An enterprise-ready, secure infrastructure pipeline deployed on **AWS (Asia Pacific - Mumbai region)** hosting an **Ubuntu EC2** instance integrated with a tuned **PostgreSQL database engine** extended with **pgvector** for hybrid semantic AI Electronic Health Record (EHR) workloads.

---

## 🛠️ Infrastructure Setup Summary

### 1. Compute & Storage (AWS EC2)

- **Instance Type:** `t2.micro` (1 vCPU, 1 GiB RAM) [AWS Free Tier compliant].
- **Storage:** 20GB General Purpose SSD (`gp3`) root volume.
- **Elastic IP:** Static public IPv4 address (`3.7.80.38`) for network persistence across server reboots.

### 2. Network Firewall (Security Groups)

- **`clinical-FDE-Database`** custom security group tied to the VPC.
- **Inbound Rules:** SSH (Port 22) locked down to your local IP; HTTP (Port 80) opened globally (`0.0.0.0/0`).

---

## 💻 Local Workspace Configuration (Windows Client)

Executed from `PS D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine`.

1. **Private Key Privilege Isolation:** Windows inheritance permissions are stripped from `clinical.pem` to grant exclusive read/write access to the active user account via `icacls.exe`.
2. **Isolated Workspace:** Python virtual environment (`clinicenv`) created and activated on the D drive.
3. **Core Framework Ingestion:** Dependencies installed via `requirements.txt`, including `sentence-transformers`, `tqdm`, `torch`, and `nemoguardrails`.

---

## 🔌 Remote Connection & Database Management

- **EC2 Connection:** `ssh -i clinical.pem ubuntu@3.7.80.38` (supports `-o ServerAliveInterval=60` for keep-alive heartbeats).
- **PostgreSQL Service:** Case-sensitive system service commands target `postgresql` (e.g., `sudo systemctl status postgresql@14-main`).
- **Superuser Access:** Log in via `sudo -i -u postgres psql`.
- **Database & Role Setup:** Initializes the `ehr_db` database and configures the `fde_admin` administrative user with secure parameters.

---

## 🐍 Architectural Python File Manifest & Core Logic

1. **`src/config.py`:** Centralized environment variables manager using `python-dotenv` to build PostgreSQL connection URIs securely.
2. **`src/database/connection.py`:** `SQLAlchemy` connection pool manager targeting AWS with `pool_pre_ping=True` and transactional session handlers (`get_db`).
3. **`scripts/01_ingest_baseline_data.py`:** Parses `MIMIC_IV_Trasncript.csv` and `schema.sql`, cleans `NaN` values, and streams tabular data to AWS.
4. **`scripts/02_verify_ingestion.py`:** Executes low-overhead `COUNT(*)` telemetry checks and samples records via `pandas`.
5. **`scripts/03_apply_vector_schema.py`:** Adds a `vector(768)` `clinical_embedding` column via defensive `ALTER TABLE` DDL statements.
6. **`scripts/04_generate_embeddings.py`:** Computes embeddings via `NeuML/bioclinical-modernbert-base-embeddings` and PyTorch, updating AWS records in bulk.
7. **`src/pii_redaction/presidio_service.py`:** Microsoft Presidio-based redactor utilizing custom regex and deny-lists to scrub PII/PHI prior to LLM calls.
8. **`src/guardrails/`:** NVIDIA NeMo Guardrails configuration (`config.yml` and `rails.co`) enforcing medical compliance and refusal boundaries.
