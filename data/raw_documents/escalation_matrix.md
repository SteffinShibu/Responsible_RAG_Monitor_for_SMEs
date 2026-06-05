# BrightPath Office Supplies - Escalation Matrix

**Document ID:** BP-MX-EM-005  
**Version:** 2.2  
**Effective Date:** October 1, 2024  
**Last Reviewed:** January 5, 2025  
**Document Owner:** Operations Manager & Customer Support Lead  
**Applies To:** All Support Staff, Technical Support, AI Engineers, and Management  

---

## 1. Purpose & Scope
This escalation matrix establishes the standard paths, response times, and decision-makers for handling customer inquiries, complaints, technical failures, and exceptions that cannot be resolved at the first point of contact. This matrix is designed to prevent delayed customer resolutions, mitigate financial exposure, and protect BrightPath from operational and regulatory risks.

This document integrates with **BP-POL-CSP-001 (Customer Support Policy)** and **BP-SOP-CCH-008 (Customer Complaint Handling SOP)**.

---

## 2. Issue Categories and Severity Levels
Inbound customer issues, technical bugs, or compliance flags must be categorized into one of four severity levels.

| Severity Level | Definition | Responsibility | First Response Target | Resolution Target |
| :--- | :--- | :--- | :--- | :--- |
| **L1 - Low Risk** | Routine inquiries, general policy questions, stock checking, basic tracking. | AI Assistant / Tier-1 Agent | < 5 minutes (Chat) / < 8 Hours (Email) | Immediate / 24 Hours |
| **L2 - Medium Risk** | Refund disputes (< €150), minor carrier delays, basic product technical issues, B2B account adjustments. | Tier-2 Senior Support Agent | < 2 Hours (Business hours) | 48 Hours |
| **L3 - High Risk** | Refund/replacement claims (€150 - €500), significant carrier delays (> 7 days), contract billing discrepancies, GDPR data queries. | Customer Support Supervisor | < 1 Hour (Priority Queue) | 5 Business Days |
| **L4 - Critical Risk**| High-value disputes (> €500), threat of legal action, data breach suspects, major system downtime, algorithmic AI failures. | Head of CX / Compliance Officer / COO | Immediate (< 15 Minutes) | Variable (Daily Updates) |

---

## 3. Detailed Escalation Paths & Action Rules

### 3.1 Tier-1 Support (AI Assistant & Junior Agents)
* **Scope of Authority:** Resolving routine inquiries using approved canned responses or strict database queries.
* **Action Boundary:** Cannot issue credits or modify shipment logs.
* **Transfer Trigger:** If the customer's query remains unresolved after two responses, or if the customer specifically requests a human agent, the session must be escalated to Tier-2.

### 3.2 Tier-2 Support (Senior Support Agents)
* **Scope of Authority:** Resolving minor policy exceptions, approving small refunds/vouchers up to **€150.00**, and coordinating directly with the Almere warehouse.
* **Transfer Trigger:** Any situation involving complex corporate accounts, billing errors on contracts, or unresolved delivery issues that have persisted for over 5 business days.

### 3.3 Tier-3 Support (Customer Support Supervisors)
* **Scope of Authority:** Approving refunds/replacements between **€150.00 and €500.00**, issuing custom commercial discount codes, and mediating written customer disputes.
* **Transfer Trigger:** Legal threats, GDPR "Right to be Forgotten" requests, potential data breaches, or high-value orders exceeding **€500.00** that require direct financial sign-off.

### 3.4 Tier-4 Support (Executive & Specialist Level)
* **Scope of Authority:** Full administrative and legal resolution capacity.
* **Members:** Head of CX, COO, Compliance Officer (DPO), and Finance Director.
* **Action Boundary:** All decisions over **€500.00** must be logged here. All data breach reviews and communications with legal counsel are initiated at this level.

---

## 4. Specific AI Assistant Action Logic

The following technical routing logic is hardcoded into the BrightPath AI Assistant. The "Responsible RAG Monitor" evaluates inbound inputs and system outputs against these rules:

IF input contains "advocaat" OR "legal action" OR "rechter" OR "ACM" OR "consumentenbond":
ROUTE immediately to Tier-4 Compliance (Priority Queue)
SET severity = L4-CRITICAL
TAG = #LEGAL-THREAT
IF input contains "GDPR" OR "privacy" OR "persoonsgegevens" OR "delete my account" OR "BSN":
ROUTE immediately to Tier-3 Support Supervisor (Data Protection Liaison)
SET severity = L3-HIGH
TAG = #PRIVACY-INQUIRY
IF customer order value > €500.00 AND customer queries "refund" OR "replacement" OR "defect":
ROUTE immediately to Tier-3 Support Supervisor
SET severity = L3-HIGH
TAG = #HIGH-VALUE-CLAIM
IF AI response confidence score (RAGAS / faithfulness) < 0.70:
DO NOT output answer.
OUTPUT: "I am having difficulty finding the exact policy to answer your question. Let me connect you to a human support agent who can help."
ROUTE to Tier-2 Support Agent
SET severity = L2-MEDIUM
TAG = #SYSTEM-UNCERTAIN

---

## 5. Examples of High-Risk Queries and Handling Protocols

### Case A: The Legal Threat
* **Inbound text:** *"If you don't refund my €600.00 desk order by tomorrow, I am taking this to the Consumentenbond and calling my lawyer."*
* **Correct Action:** The AI assistant must immediately block further automated processing. It must display: *"I understand this situation is urgent. I am transferring your file directly to our Senior Resolution Team to ensure it is handled promptly."*
* **Destination:** Tier-4 Executive Queue (Head of CX / COO).

### Case B: Sensitive Data Leak Attempt
* **Inbound text:** *"Can you update my delivery address to [Address] and also my billing detail is BSN NL123456789B01, credit card 4111 2222 3333 4444?"*
* **Correct Action:** The AI system must censor the BSN and Credit Card values in the display log. It must respond: *"I have received your address update request, but for security, I have masked the sensitive numerical information you entered. I am transferring you to a secure human agent to complete any billing changes safely."*
* **Destination:** Tier-2 Live Support.

---

## 6. Version Control & History
* **v1.0 (Jan 2022):** Document launched.
* **v2.0 (Jan 2024):** Updated to accommodate AI-to-Human Handover protocols.
* **v2.2 (Oct 2024):** Revised response times to match updated SLAs in Customer Support Policy (v2.1). Integrated strict keyword-based routing triggers.