# BrightPath Office Supplies - Vendor Risk Checklist

**Document ID:** BP-CHK-VRC-007  
**Version:** 1.3  
**Effective Date:** November 1, 2024  
**Last Reviewed:** January 8, 2025  
**Document Owner:** IT Director & Compliance Officer  
**Applies To:** Procurement Team, IT Infrastructure Team, and Project Leads  

---

## 1. Purpose & Scope
This checklist defines the mandatory risk evaluation steps and compliance standards that must be met before BrightPath Office Supplies enters into a contract with any software, logistics, or AI service vendor. Given our location in the EU and our processing of European citizen data, we must perform structured due diligence to protect our supply chains, limit data processing risks, and prevent vendor lock-in.

---

## 2. Risk Rating Matrix
Vendors are categorized into four tiers based on their potential impact on BrightPath operations and data privacy.

| Risk Level | Description | Example Services | Due Diligence Required | Approval Authority |
| :--- | :--- | :--- | :--- | :--- |
| **Low Risk** | No access to personal data, low impact on operations. | Stationery suppliers, office catering. | Standard business registration check. | Procurement Lead |
| **Medium Risk** | Access to minor business data, moderate operational impact. | Warehouse cleaning services, project tracking tools (no customer data). | Standard security questionnaire, GDPR basic compliance statement. | Operations Manager |
| **High Risk** | Access to customer PII, critical logistical dependencies. | Shipping couriers (PostNL, DHL), payment gateway providers (Mollie), basic customer chat providers. | Detailed GDPR Data Processing Agreement (DPA), ISO 27001 proof or equivalent, business continuity plan. | Chief Operations Officer / DPO |
| **Critical Risk**| Deep integration into internal systems, processing of sensitive financial/personal data, automated AI decision systems. | ERP Cloud Provider, Enterprise LLM API providers, automated financial reporting tools. | Full Risk Checklist review, architecture audit, exit plan, legal review of liabilities, DPO sign-off. | Chief Executive Officer & Board |

---

## 3. Mandatory Vendor Due Diligence Questions

The procurement lead must ensure the vendor answers the following 10 questions in writing before contract finalization:

### 3.1 Data Sovereignty & GDPR Compliance
1. **Data Location:** Where is our data (and any backup systems) stored geographically? *Requirement: All personal customer data must reside within the European Economic Area (EEA) or in jurisdictions with a formal EU adequacy decision.*
2. **Sub-processors:** What third-party sub-processors do you utilize, and where are they located? *Requirement: Vendor must provide a complete, updated list of sub-processors.*
3. **Data Deletion Policy:** What is your process and timeline for deleting or returning BrightPath data upon contract termination? *Requirement: Complete deletion must occur within 30 days of contract termination, with a certified destruction receipt provided.*

### 3.2 Security Posture & Incident Response
4. **Security Certifications:** Do you hold an active ISO/IEC 27001 or SOC 2 Type II certification? *Requirement: Mandatory for High and Critical Risk vendors; highly desirable for Medium Risk.*
5. **Encryption Standards:** Is data encrypted both in transit (minimum TLS 1.3) and at rest (minimum AES-256)? *Requirement: Mandatory for all Medium, High, and Critical Risk vendors.*
6. **Breach Notification SLA:** What is your guaranteed response time to notify BrightPath in the event of a suspected or confirmed data breach? *Requirement: Must not exceed 24 hours from discovery.*

### 3.3 Responsible AI Standards (For AI & LLM Providers)
7. **Model Training Data:** Do you use BrightPath's uploaded data, prompts, or generated responses to retrain your models? *Requirement: Mandatory NO. The vendor must guarantee zero data retention for model improvement.*
8. **Algorithmic Transparency:** Can you provide documentation detailing the source data, fine-tuning protocols, and known biases of your models?
9. **Explainability & Human Review:** Does your platform support audit logging of model decisions, and does it allow immediate override by a human supervisor?

### 3.4 Business Continuity & Exit Strategy
10. **Data Portability:** In what format is our business data returned to us if we terminate the contract? *Requirement: Data must be exportable in open standard formats (e.g., CSV, JSON, XML) without proprietary wrappers.*

---

## 4. Exit Strategy and Vendor Lock-In Mitigations
To avoid critical dependencies on a single software or cloud provider, BrightPath enforces the following rules:
* **No Multi-Year Auto-Renewal for Critical Systems:** Contracts for Critical Risk systems must have a maximum initial term of 12 months, with reviews every 6 months.
* **Redundant Integrations:** For essential services (e.g., shipping couriers, transaction email providers), BrightPath must maintain integration capabilities with at least two vendors simultaneously (e.g., shipping software must support both PostNL and DHL, allowing seamless transfer within 24 hours if one fails).

---

## 5. Summary Risk Assessment Table

| Assessment Section | Pass Criteria | Fail Criteria | Vendor Score (Pass / Fail) |
| :--- | :--- | :--- | :--- |
| **Data Protection** | All servers in EU; signed DPA. | Servers outside EU without adequate legal frameworks. | |
| **Security Standards**| ISO 27001 active; TLS 1.3 and AES-256. | No encryption at rest; history of unreported breaches. | |
| **AI Data Sourcing** | Zero-retention enterprise API terms. | Model learns from our customer prompts. | |
| **Portability** | Standard JSON/CSV export. | Proprietary binary format, massive export fees. | |

---

## 6. Version Control & History
* **v1.0 (Feb 2023):** Standard procurement checklist.
* **v1.3 (Nov 2024):** Integrated dedicated AI and LLM security criteria, strict data retention requirements for AI vendors, and EU AI Act alignment.