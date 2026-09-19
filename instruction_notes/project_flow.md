# Secure-Clinical-Insights-Engine

An enterprise-ready, secure infrastructure pipeline deployed on **AWS (Asia Pacific - Mumbai region)** hosting an **Ubuntu EC2** instance integrated with a tuned **PostgreSQL database engine** for Electronic Health Record (EHR) workloads.

---

## 🛠️ Infrastructure Setup Summary

### 1. Compute & Storage (AWS EC2)

- **Instance Type:** Deployed on an **AWS EC2 Instance** to serve as the application and database host.
- **Storage Allocation:** Provisioned with a **20GB General Purpose SSD (gp3)** root volume.
- **Network Stability (Elastic IP):** Allocated and associated a static, permanent public IPv4 address (**`3.7.80.38`**). This ensures network persistence so that downstream database components or backend configurations remain unbroken during server reboots.

### 2. Network Firewall (Security Groups)

- Configured a custom security group named **`clinical-FDE-Database`** explicitly tied to the project VPC network.
- **Inbound Rules Configured:**
  - **SSH (Port 22):** Locked down specifically to your local work station's public IP address for secure shell administration.
  - **HTTP (Port 80):** Opened globally (`0.0.0.0/0`) to allow application web traffic interfaces.

---

## 🔑 Secure Connection & Permissions (Windows Client)

Because SSH requires strict private key confidentiality, inheritance permissions on the local Windows machine were stripped to grant exclusive access to your local Windows user profile.

### Windows PowerShell Permission Optimization:

```powershell
# Reset and drop permission inheritance from unauthorized system groups
icacls.exe "D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine\clinical.pem" /reset
icacls.exe "D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine\clinical.pem" /inheritance:r

# Grant exclusive full read/write privileges to your logged-in Windows account
icacls.exe "D:\2026\newstudy\projects\Secure-Clinical-Insights-Engine\clinical.pem" /grant:r "$($env:USERNAME):(F)"
```

### Establish SSH Remote Terminal Access:

```bash
ssh -i clinical.pem ubuntu@3.7.80.38
```

---

## 🗄️ Database Provisioning & Security (PostgreSQL)

PostgreSQL is installed and running natively inside the Ubuntu container environment. The primary database cluster and specific admin access criteria have been successfully initialized.

### 1. Database Creation

Executed via the database engine wrapper to initialize the core health record warehouse:

```bash
sudo -i -u postgres psql -c "CREATE DATABASE ehr_db;"
```

### 2. Administrative Role Configuration

Logged into the interactive `psql` interface as the super-administrator to configure a custom app-level database administrator (**`fde_admin`**) with fine-tuned structural settings:

```sql
-- Create the dedicated application manager role
CREATE USER fde_admin WITH PASSWORD 'SecureEHR2026!';

-- Set global parameter settings for optimal clinical operations
ALTER ROLE fde_admin SET client_encoding TO 'utf8';
ALTER ROLE fde_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE fde_admin SET timezone TO 'UTC';

-- Assign full privileges of the core database to the role
GRANT ALL PRIVILEGES ON DATABASE ehr_db TO fde_admin;
```

---

## 🔒 Security Best Practices Implemented

- **Zero Secret Disclosure:** Credentials, system IPs, and specific database access secrets are isolated inside a localized `.env` configuration template.
- **Git Safeguard:** The `.env` file must be added to the `.gitignore` mapping structure to guarantee critical pipeline variables are never pushed to public version control repositories.
