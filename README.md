# Secure-Clinical-Insights-Engine

An enterprise-ready, secure infrastructure pipeline deployed on **AWS (Asia Pacific - Mumbai region)** hosting an **Ubuntu EC2** instance integrated with a tuned **PostgreSQL database engine** extended with **pgvector** for hybrid semantic AI Electronic Health Record (EHR) workloads.

---

## 🛠️ Infrastructure Setup Summary

### 1. Compute & Storage (AWS EC2)

- **Instance Type Selection:** `t2.micro` (1 vCPU, 1 GiB RAM) [AWS Free Tier compliant].
- **Storage Allocation:** Provisioned with a **20GB General Purpose SSD (gp3)** root storage volume.
- **Network Stability (Elastic IP):** Allocated and associated a static, permanent public IPv4 address (**`3.7.80.38`**). This ensures network persistence so that downstream database components or backend configurations remain unbroken during server reboots.

### 2. Network Firewall (Security Groups)

- Configured a custom security group named **`clinical-FDE-Database`** explicitly tied to the project VPC network.
- **Inbound Rules Configured:**
  - **SSH (Port 22):** Locked down specifically to your local workstation's public IP address for secure shell administration.
  - **HTTP (Port 80):** Opened globally (`0.0.0.0/0`) to allow application web traffic interfaces.

---

## 💻 Local Workspace Configuration (Windows Client)

All local project management operations are executed from the native target folder path:  
`PS D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine>`

### 1. Private Key Privilege Isolation

Because SSH requires strict private key confidentiality, inheritance permissions on the local Windows host are stripped to grant exclusive access to your active user account:

```powershell
# Reset permissions and drop inheritance allocations from generic system groups
icacls.exe "D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine\clinical.pem" /reset
icacls.exe "D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine\clinical.pem" /inheritance:r

# Grant exclusive full read/write privileges strictly to your logged-in Windows account
icacls.exe "D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine\clinical.pem" /grant:r "$($env:USERNAME):(F)"
```

### 2. Isolated Workspace Environment Setup

Initialized an isolated execution runtime environment block directly inside the project root on the D drive (`clinicenv`) to bypass volume storage thresholds on the primary system boot drive (C:):

```powershell
# Create the local python virtual environment path natively
python -m venv clinicenv

# Activate the localized platform runtime environment shell workspace
clinicenv\Scripts\activate
```

### 3. Core Framework Package Ingestion

Deploy the operational clinical dependency framework stack natively inside the active environment shell utilizing the structural requirements manifest matrix:

```powershell
pip install -r requirements.txt
```

_(Additional AI processing requirements tracking libraries are synced via the localized terminal manager:)_

```powershell
pip install sentence-transformers tqdm torch
```

---

## 🔌 Remote Connection Operations Protocol

### 1. Connecting to the Ubuntu EC2 Instance

Establish a secure remote shell session from your local Windows terminal terminal prompt utilizing the isolated key string:

```bash
ssh -i clinical.pem ubuntu@3.7.80.38
```

_Note: To prevent server timeout connection drops during long administrative periods, execute utilizing the keep-alive heartbeat arguments string:_

```bash
ssh -o ServerAliveInterval=60 -i clinical.pem ubuntu@3.7.80.38
```

### 2. Managing the PostgreSQL Service (Case-Sensitive)

Linux system service control daemons are strictly **case-sensitive**. All administration utilities must target entirely lowercase strings (`postgresql`):

```bash
# Query the system logs for the explicit cluster manager instance
sudo systemctl status postgresql@14-main

# Restart the database instance engine to pull configuration changes
sudo systemctl restart postgresql@14-main
```

_Note: If a status tracking readout enters the `less` paging viewer terminal view (`lines 1-13`), press **`q`** on your keyboard to instantly return to your active Ubuntu shell._

### 3. Interactive PostgreSQL Superuser Shell Access

Log directly into the core interactive database wrapper interface as the system master administrator:

```bash
sudo -i -u postgres psql
```

_Note: Execute **`\q`** inside the database prompt (`postgres=#`) to drop out of the interactive layer and return to your standard Ubuntu shell environment._

---

## 🗄️ Database Provisioning & Security Architecture

### 1. Database Creation

Executed via the database engine wrapper to initialize the core health record warehouse target container:

```bash
sudo -i -u postgres psql -c "CREATE DATABASE ehr_db;"
```

### 2. Administrative Role Configuration

The following optimized configuration schema rules were executed one clean line at a time inside the interactive `psql` console to register our app-level administrator (`fde_admin`):

```sql
CREATE USER fde_admin WITH PASSWORD 'SecureEHR2026!';
ALTER ROLE fde_admin SET client_encoding TO 'utf8';
ALTER ROLE fde_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE fde_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ehr_db TO fde_admin;
```

---

## 🐍 Architectural Python File Manifest & Core Logic

### 1. Context Configuration Engine (`src/config.py`)

- **What it does:** Centralized environment variables manager for the local workstation application logic.
- **Core Logic:** Leverages `python-dotenv` to scan your hidden root `.env` profile. It pulls operational environment inputs (`DB_USER`, `DB_PASSWORD`, etc.) dynamically into Python system memory and synthesizes the standard PostgreSQL connection URI string string used by database engines. This setup isolates secrets out of raw code repositories.

### 2. Database Session Orchestrator (`src/database/connection.py`)

- **What it does:** Instantiates the core database connection engine pool and structural session manager.
- **Core Logic:** Uses `SQLAlchemy` to build a persistent computational communication pipeline targeting your AWS Elastic IP `3.7.80.38`. It implements advanced operational configurations like `pool_pre_ping=True` (which actively tests connection dropouts over long-distance Wi-Fi paths before running scripts) and serves an isolated transactional data handler block (`get_db`) to downstream ingestion code blocks.

### 3. Legacy Tabular Data Pipeline (`scripts/01_ingest_baseline_data.py`)

- **What it does:** Parses the raw historical health dataset and pushes it across the internet into AWS.
- **Core Logic:** Dynamically calculates relative local project directories to locate the `schema.sql` file and your raw medical CSV file (`MIMIC_IV_Trasncript.csv`). It maps cell parameters using `pandas`, runs structural transformations to turn invalid data cells (`NaN`) into clean database `NULL` data formats, and uses high-speed streaming blocks to write data into the remote server instance.
- **Execution:**
  ```powershell
  python scripts\01_ingest_baseline_data.py
  ```

### 4. Integrity Validation & Audit Telemetry (`scripts/02_verify_ingestion.py`)

- **What it does:** Connects across network firewalls to verify structural data volume and format correctness.
- **Core Logic:** Directly issues an optimized, low-overhead SQL `COUNT(*)` function query to retrieve total table capacities without causing instance memory bottlenecks. It filters records where medications are actively recorded (`WHERE drug IS NOT NULL`) and draws a small structural block sample directly into a clean `pandas` framework output data grid table on your local Windows command prompt.
- **Execution:**
  ```powershell
  python scripts\02_verify_ingestion.py
  ```

### 5. Automated Server Schema Upgrader (`scripts/03_apply_vector_schema.py`)

- **What it does:** Modifies your database structure to support AI vectors straight from your local client machine.
- **Core Logic:** Initiates a programmatic connection to your AWS database cluster using `SQLAlchemy`. It executes a clean `ALTER TABLE` DDL statement to inject a new structural storage field (`clinical_embedding`) configured as a specialized **`vector(768)`** data type. It queries internal database schemas (`information_schema.columns`) to confirm the configuration succeeded, utilizing a defensive `IF NOT EXISTS` check to prevent crashing or table structural disruption if executed multiple times.
- **Execution:**
  ```powershell
  python scripts\03_apply_vector_schema.py
  ```

### 6. BioClinical AI Embedding Generator (`scripts/04_generate_embeddings.py`)

- **What it does:** Reads unstructured clinical inputs, converts them into high-dimensional AI numbers, and commits them in bulk back to AWS.
- **Core Logic:** Downloads and runs the localized deep-learning transformer model NeuML/bioclinical-modernbert-base-embeddings. It iterates through your database records where vector records are blank, merges multi-column textual fragments (such as diagnoses, lab checks, and pharmaceutical codes) into structured clinical strings delimited by pipes (|), and executes parallel matrix embeddings calculations utilizing PyTorch. It then triggers optimized SQL bulk UPDATE statements to map the resulting 768-dimensional float arrays back to their target matching rows in AWS.
- **Execution:**
  ```powershell
  python scripts\04_generate_embeddings.py
  ```
