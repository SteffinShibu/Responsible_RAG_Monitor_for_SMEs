# BrightPath Office Supplies - Customer Complaint Handling SOP

**Document ID:** BP-SOP-CCH-008  
**Version:** 2.1  
**Effective Date:** October 15, 2024  
**Last Reviewed:** January 12, 2025  
**Document Owner:** Head of Customer Experience (CX)  
**Applies To:** Customer Support Agents, Support Supervisors, Quality Analysts  

---

## 1. Purpose & Scope
This Standard Operating Procedure (SOP) defines the operational workflow for receiving, classifying, investigating, resolving, and documenting formal customer complaints at BrightPath Office Supplies. Our objective is to turn negative customer experiences into opportunities for brand loyalty, whilst maintaining strict compliance with Dutch consumer rights and keeping financial payouts within approved budget boundaries.

This document should be read in conjunction with **BP-POL-CSP-001 (Customer Support Policy)**, **BP-POL-RRP-002 (Refund Policy)**, and **BP-MX-EM-005 (Escalation Matrix)**.

---

## 2. Complaint Categories & Severity Levels
Inbound complaints must be logged under one of four categories and assigned a severity level upon intake.

### 2.1 Category Classifications
* **Product Quality (PQ):** Defective items, damaged ergonomic furniture, non-functional electronics.
* **Service Quality (SQ):** Unhelpful support staff, incorrect information given by agent, billing issues.
* **Logistics & Delivery (LD):** Late arrival, missing items from order package, courier driver misconduct.
* **Data Privacy / Ethics (DPE):** GDPR queries, unsolicited marketing emails, complaints regarding AI interaction.

### 2.2 Severity Levels
[Inbound Complaint]
│
├─► Is there a threat of legal action, GDPR violation, or value > €500?
│ ├─► YES ──► Classify as LEVEL 3 (CRITICAL)
│ └─► NO
│
├─► Is there a significant delay, B2B contract issue, or value €150 - €500?
│ ├─► YES ──► Classify as LEVEL 2 (MAJOR)
│ └─► NO
│
└─► Standard minor issue, simple late order, or value < €150?
└─► Classify as LEVEL 1 (MINOR)

---

## 3. Mandatory Steps for Complaint Resolution

All formal complaints must go through the following five-step pipeline:

### Step 1: Intake & Triage
* **Action:** Capture customer details, Order ID, and specific complaint reasons.
* **AI Rule:** The AI Assistant must parse the text for keywords such as "formal complaint" (officiële klacht), "disappointed" (teleurgesteld), or "legal" (juridisch). The AI must acknowledge the complaint within **5 minutes** during business hours, and immediately transfer the case to a human agent if categorized as Level 2 or Level 3.

### Step 2: Investigation & Fact-Finding
* **Action:** Review CRM system notes, warehouse camera footage (if picking error is claimed), shipping logs from PostNL/DHL, and any photographs provided by the customer.
* **Timeline:** Level 1 investigations must be completed within **4 hours** of triage. Level 2 and 3 investigations must be completed within **2 business days**.

### Step 3: Resolution Formulation & Compensation Limits
When proposing a resolution, support agents must stay within strict compensation limits:

* **Level 1 (Minor):** 
  * Replacement of defective item (pre-approved) or refund.
  * Maximum voluntary goodwill voucher: **€10.00** (without supervisor sign-off).
* **Level 2 (Major):**
  * Full refund or credit note.
  * Maximum voluntary goodwill voucher: **€25.00** (requires Supervisor approval).
* **Level 3 (Critical):**
  * High-value refund.
  * Goodwill compensation up to **€50.00** or 10% discount on B2B contract (requires joint COO and Finance Director approval).

### Step 4: Customer Communication
* **Standard:** Use clear, empathetic, and professional language. 
* **Rule:** Never admit legal liability or breach of contract without approval from the Chief Operations Officer. Avoid phrases like *"This is entirely our fault, we have breached our contract"*—instead, use: *"We sincerely regret that this delivery did not meet our high standards, and we are committed to making this right."*

### Step 5: Archiving and Quality Review
* **Action:** Tag the ticket with the appropriate category (PQ, SQ, LD, DPE) and the suffix `-COMPLAINT`. Ensure all investigation documents and communications are attached to the customer record in the CRM system.
* **Retention:** Complaint records must be archived for a minimum of **3 years** to identify systemic operational failures.

---

## 4. Special Rules for AI-Related Complaints
If a customer submits a complaint specifically regarding their interaction with the AI Assistant (e.g., claiming the AI was rude, gave incorrect policy information, or hallucinated a refund promise):
1. **Immediate Quarantine:** The chat history must be immediately flagged with `#AI-COMPLAINT` and duplicated to the AI Governance Specialist.
2. **De-activation of Automated Responses:** For that specific customer's profile, the AI Assistant must be completely deactivated. All future touchpoints must bypass automated chat systems and route straight to human agents.
3. **Corrective Action:** The AI Governance Specialist must review the prompt log within **3 business days** to determine if prompt injection occurred, or if model parameters (e.g., temperature, system guidelines) require adjustment.

---

## 5. Version Control & History
* **v1.0 (Nov 2021):** Launch SOP.
* **v2.0 (Mar 2023):** Added compensation boundaries and strict supervisor approvals.
* **v2.1 (Oct 2024):** Added Section 4 regarding special protocols for AI-related complaints and automated system overrides.