
---

# data_privacy_and_ai_usage_policy.md

```markdown
# BrightPath Office Supplies - Data Privacy and AI Usage Policy

**Document ID:** BP-POL-DPA-004  
**Version:** 2.0  
**Effective Date:** December 15, 2024  
**Last Reviewed:** January 18, 2025  
**Document Owner:** Chief Compliance Officer / DPO (Data Protection Officer)  
**Applies To:** All Employees, External Contractors, and Software Developers  

---

## 1. Purpose & Scope
This policy defines the principles and standards governing data privacy, personal data protection, and the acceptable deployment of Artificial Intelligence (AI) technologies at BrightPath Office Supplies. As a Dutch entity, BrightPath strictly complies with the **General Data Protection Regulation (GDPR)** (Algemene Verordening Gegevensbescherming - AVG) and national privacy laws.

This policy applies to all operations involving customer personal data (such as names, physical addresses, emails, and transaction histories), employee details, and any analytical or customer-facing AI models integrated into our IT infrastructure.

---

## 2. General Data Privacy Principles (GDPR Compliance)
BrightPath is committed to the fundamental tenets of data protection:

1. **Lawfulness, Fairness, and Transparency:** Customer data is collected only for specific, explicit, and legitimate purposes (e.g., order fulfillment, customer support).
2. **Data Minimization:** We only collect the minimum amount of personal data required to complete the transactions.
3. **Purpose Limitation:** Customer data collected for shipping must not be repurposed for unauthorized marketing profiles without explicit consent.
4. **Accuracy & Storage Limitation:** Personal data must be kept accurate and deleted or anonymized once the retention obligation expires (e.g., tax records must be held for 7 years under Dutch tax law (Belastingdienst); general chat logs are kept for 90 days).

---

## 3. Handling Personal and Sensitive Customer Data

### 3.1 Personal Data (PII)
Personal Identifiable Information (PII) includes:
* First and Last Names
* Physical Delivery Addresses
* Email Addresses
* Telephone Numbers
* Order Tracking Codes (when linked with a name)

### 3.2 Sensitive Data (Special Categories)
Under the GDPR, special categories of data (e.g., medical information, political opinions, race, or religious beliefs) are strictly prohibited from being collected, processed, or stored by BrightPath. 
* **The Citizen Service Number (Burgerservicenummer - BSN):** BrightPath does not require and must never request or store a customer's BSN.
* **Payment Card Industry (PCI) Data:** Full credit card numbers, CVVs, or bank account PINs must never be recorded in chat logs, customer notes, or emails. All payments are processed through our certified third-party provider (Mollie).

---

## 4. AI Tool Usage and System Boundaries
BrightPath deploys Large Language Models (LLMs) to optimize business efficiency, specifically through our "BrightPath AI Assistant."

### 4.1 What Employees CAN Paste into AI Tools
* Publicly available product brochures, catalogs, and technical specifications.
* Anonymized policy templates (e.g., general templates without company-specific confidential data or customer details).
* Code snippets that do not contain internal system credentials, database URIs, or API keys.

### 4.2 What Employees CANNOT Paste into AI Tools (Third-Party or Public)
Employees are strictly prohibited from entering the following into any public or non-enterprise-controlled AI tool (e.g., free versions of ChatGPT, Claude, Midjourney):
* **Customer Data:** No names, physical addresses, order histories, or specific support conversations.
* **Financial Information:** No invoice details, sales forecasts, or corporate balance sheets.
* **Intellectual Property:** No source code of BrightPath systems, proprietary workflow notes, or draft strategic business plans.
* **Employee Information:** No payroll files, performance evaluations, or resumes.

*Note on Internal Tools:* The "BrightPath AI Assistant" and "Responsible RAG Monitor" run on secured, enterprise-grade cloud instances with zero-data retention commitments for model retraining. Employees may use these internal interfaces in accordance with **BP-POL-AIU-006 (Internal Employee AI Use Guidelines)**.

---

## 5. Human Oversight & De-escalation Requirements
All AI interactions within our customer-facing portals must be supervised through administrative dashboards.

* **Audit Rights:** The Data Protection Officer reserves the right to audit AI conversation logs at any point.
* **Opt-Out Mechanism:** Any customer interacting with our AI assistant has the absolute right to demand a human agent. If the phrase "speak to a human" or its equivalent is recognized, the system must immediately hand over the connection to the human support queue, preserving the chat history for the human agent's review.

---

## 6. Audit Logging Expectations
To demonstrate compliance under the EU AI Act and GDPR Article 30:
1. **Activity Logs:** The system must record every prompt entered and every response generated, along with the timestamps, model metadata, and citation confidence scores.
2. **Review of Flagged Violations:** The "Responsible RAG Monitor" must automatically flag responses containing potential hallucinations, unauthorized policy commitments, or private information leaks.
3. **Log Retention:** Log records must be retained for exactly **180 days** before automated purging, unless active legal disputes require extended holds.

---

## 7. Operational Actions in Case of Data Breach
If an employee or system monitor detects that sensitive customer data (e.g., credit card information, physical address lists) has been accidentally pasted into an unauthorized AI model or leaked to the public:
1. Immediately notify the Data Protection Officer via `dpo@brightpathofficesupplies.nl` and log an ticket with `#DATA-BREACH`.
2. The DPO must assess the breach within **24 hours** to determine if a notification must be made to the Dutch Data Protection Authority (Autoriteit Persoonsgegevens - AP) within the statutory **72-hour window**.

---

## 8. Version Control & History
* **v1.0 (May 2018):** GDPR compliance framework launched.
* **v1.5 (Nov 2023):** Integrated initial AI usage instructions.
* **v2.0 (Dec 2024):** Complete overhaul to align with the EU AI Act guidelines, defining explicit boundaries for prompt injection mitigation, audit logs, and clear BSN/PCI restrictions.