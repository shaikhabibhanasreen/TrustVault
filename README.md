# TrustVault — Secure Document Sharing Platform

TrustVault is a Django-based web application designed to provide controlled document sharing, user permissions, and an audit trail of important document-related activities.

The application allows users to upload documents, access documents they own or have permission to view, share documents with other users, and revoke access when necessary. Audit logs record important events to support accountability and traceability.

## Features

* **User Authentication:** Login and registration.
* **Role-Based Access:** User roles help control access to application features.
* **Document Upload:** Upload supported document formats.
* **Document Listing:** View documents owned by the logged-in user or shared with them.
* **Document Search:** Search accessible documents by title, description, or category.
* **Document Sharing:** Grant document permissions to other users.
* **Access Revocation:** Remove previously granted permissions.
* **Access Control:** Prevent unauthorized users from accessing protected documents.
* **Audit Logging:** Record activities such as uploads, views, permission changes, and denied access attempts.
* **Audit Chain Verification:** Verify the integrity of the audit log hash chain.
* **Dashboard:** View document information and recent activity.
* **Automated Tests:** Test document visibility and search behavior.

## Technology Stack

* Python
* Django
* SQLite
* HTML
* CSS
* Django Authentication
* Django Automated Testing

## Project Structure

```text
TrustVault/
├── accounts/       # User accounts and authentication
├── audit/          # Audit logs and hash-chain verification
├── config/         # Django project configuration
├── documents/      # Document management and permissions
├── manage.py
├── db.sqlite3
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd TrustVault
```

Replace the placeholder with your actual repository URL.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the project's required packages. If you have a `requirements.txt` file, run:

```powershell
pip install -r requirements.txt
```

If the file does not exist yet, create it as described in the next phase.

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Create an administrator account

```powershell
python manage.py createsuperuser
```

Follow the prompts to configure the account.

### 6. Start the development server

```powershell
python manage.py runserver
```

Open the local development server at:

`http://127.0.0.1:8000/`

Use the application's configured URLs to access registration, login, the document list, and the dashboard.

## Running Tests

Run the automated tests with:

```powershell
python manage.py test
```

The current test suite contains four document search and visibility tests. All four passed in the latest test run.

## Audit Chain Verification

Open the Django shell:

```powershell
python manage.py shell
```

Then execute:

```python
from audit.services import verify_audit_chain
verify_audit_chain()
```

A successful verification currently returns:

```text
(True, 'Audit chain is valid.')
```

Exit the shell with:

```python
exit()
```

## Security Notes

TrustVault implements authentication, document permission checks, access-revocation functionality, and audit logging.

The audit hash chain provides a mechanism for detecting changes to the linked audit entries. However, a valid chain alone does not prove that the application is fully secure or that an attacker cannot modify the entire chain. Production deployment requires additional security review, secure secret management, HTTPS, appropriate file-storage controls, and further testing.

## Future Improvements

* Expand automated tests for authentication, sharing, editing, and access revocation.
* Add stronger file validation and malware scanning.
* Improve audit-log protection and verification.
* Add secure production deployment configuration.
* Improve the dashboard with additional analytics.
* Add API documentation if the API endpoints are exposed.

## Project Status

The core document management, permission, search, dashboard, and audit functionality has been implemented. The current automated test suite passes all four tests, and audit-chain verification has succeeded in the latest check.
