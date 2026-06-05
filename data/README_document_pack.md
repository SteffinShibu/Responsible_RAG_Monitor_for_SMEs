# BrightPath Office Supplies - Synthetic SME Document Pack

Welcome to the **BrightPath Office Supplies Synthetic SME Document Pack**. This asset contains 10 fully detailed, internally consistent, and realistic operational documents, alongside a comprehensive test dataset (`sample_test_questions.csv`). It has been designed specifically for evaluating Retrieval-Augmented Generation (RAG) pipelines, statistical process monitoring, LLM-as-judge frameworks, and responsible AI governance workflows in a realistic European Small-to-Medium Enterprise (SME) context.

---

## 1. Document Pack Structure
This repository contains the following synthetic artifacts:

1. **`customer_support_policy.md`**: Outlines support channels, SLAs, tone guidelines, and AI assistant boundaries.
2. **`refund_and_replacement_policy.md`**: Defines return windows (differentiating B2C and B2B), defective replacements, late delivery compensation, and high-value transaction limits (€500.00).
3. **`delivery_and_tracking_sop.md`**: Standard shipping timelines for the EU, tracking rules, lost package criteria, and courier interaction policies.
4. **`data_privacy_and_ai_usage_policy.md`**: GDPR-compliant rules regarding personal identifiable information (PII), Citizen Service Numbers (BSN), credit card data, and general AI boundaries.
5. **`escalation_matrix.md`**: Maps issue severity (L1 to L4) to support roles, establishing routing rules for high-risk topics (legal, GDPR, high-value).
6. **`internal_employee_ai_use_guidelines.md`**: Guidelines for employee use of generative AI tools, the human-in-the-loop verification pipeline, and proprietary information security.
7. **`vendor_risk_checklist.md`**: Procurement checklist evaluating software/AI vendors on data sovereignty, ISO 27001 compliance, and exit portability.
8. **`customer_complaint_handling_sop.md`**: Multi-step triage and investigation process for formal complaints, compensation limits, and procedures for handling AI-related customer complaints.
9. **`productivity_baseline_notes.md`**: Operational metrics and statistical baselines from the historical "manual support era" for performance analysis.
10. **`faq_knowledge_base.md`**: A 50-question master FAQ list (divided into customer and employee sections) providing immediate, source-cited reference data.
11. **`sample_test_questions.csv`**: A dataset containing 50 test cases categorized by difficulty, risk, and expected behavior, mapping directly back to policy elements.

---

## 2. Intended Use Cases

This synthetic document pack is optimized for testing and monitoring advanced RAG and LLM systems:

### A. RAG Retrieval & Context Matching
* **Multi-Document Reasoning:** Test if your RAG pipeline can retrieve details across multiple files. For instance, determining if a delayed custom shipment exceeding €500 requires dual sign-off involves checking `refund_and_replacement_policy.md` (high-value threshold), `delivery_and_tracking_sop.md` (delay classification), and `escalation_matrix.md` (routing).
* **Source Citations:** Test if your system correctly identifies source documents and sections (e.g., `[Source: BP-POL-RRP-002, Section 2.1]`).

### B. LLM-as-Judge Evaluation
* **Factuality & Hallucination Audits:** Inject incorrect assertions (e.g., claiming a B2B return has a 14-day window without restocking fees) and evaluate if an LLM-as-judge accurately identifies the hallucination.
* **Tone Compliance:** Ensure the LLM judge flags responses containing rude, overly casual, or non-empathetic wording.

### C. Responsible AI & Guardrail Verification
* **Sensitive Data Redaction:** Test if your system masks BSN numbers or payment card details entered by users during mock support conversations.
* **Escalation Triggers:** Verify if the system blocks automated answers and triggers handovers when detecting legal threats, GDPR complaints, or order values above the €500 threshold.
* **Out-of-Scope Mitigation:** Test if the AI correctly declines to answer when prompted to create custom discounts, promise refunds, or guarantee shipping dates.

---

## 3. Embedded Responsible AI Risks and Edge Cases

To make evaluations robust, the document pack contains deliberate "stress tests" and realistic operational constraints:

* **B2B vs. B2C Mismatch:** B2C clients have a 14-day withdrawal window with no fees. B2B clients have a 7-day window with a mandatory 15% restocking fee. Testing questions challenge the RAG system to correctly identify the customer class before answering.
* **High-Value Transaction Constraint:** Direct refund and replacement approvals are capped at €500.00. Any scenario involving numbers above this limit requires dual sign-off. RAG pipelines must recognize when they are unauthorized to proceed.
* **Courier Investigation Lag:** The policies state that refunds cannot be issued for packages marked "Delivered" until a courier investigation (which takes 3 to 10 days) is completed. RAG systems must not promise immediate refunds for tracking disputes.
* **Strict Privacy Overrides:** Direct keywords like "BSN", "GDPR", or "delete my account" are configured to trigger immediate handovers to human agents to prevent unauthorized data processing.

---

## 4. Limitations
* **Fictional Data:** All company names, phone numbers, email addresses, and policy thresholds are entirely fictional. Do not use this document pack as genuine legal or regulatory counsel.
* **Simplified Compliance:** While these documents incorporate real GDPR concepts, Dutch Civil Code references, and EU AI Act definitions, they are simplified to match a 45-person SME context and are not a complete substitute for professional legal audits.