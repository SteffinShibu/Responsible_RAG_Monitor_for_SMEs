# BrightPath Office Supplies - Internal Employee AI Use Guidelines

**Document ID:** BP-POL-AIU-006  
**Version:** 1.2  
**Effective Date:** November 15, 2024  
**Last Reviewed:** January 10, 2025  
**Document Owner:** IT Director & HR Lead  
**Applies To:** All BrightPath Employees, Interns, and Contractors  

---

## 1. Purpose & Scope
This document sets forth the authorized, prohibited, and conditional use cases of Artificial Intelligence (AI) and Machine Learning (ML) tools by BrightPath Office Supplies employees. These guidelines are designed to maximize workplace productivity and innovation while protecting the company's intellectual property, maintaining compliance with the EU AI Act and GDPR, and avoiding reputation damage from inaccurate or biased AI outputs.

---

## 2. Approved AI Use Cases
Employees are encouraged to utilize BrightPath’s *approved enterprise-tier AI solutions* (e.g., our internal secured instance of the BrightPath AI Copilot) for the following business activities:

1. **Drafting General Communications:** Writing outlines, initial drafts of marketing copy, internal newsletters, or non-confidential customer announcements.
2. **Coding Assistance:** Generating boilerplate software code, writing SQL queries for inventory reporting, or debugging internal scripts (provided no real database connection strings or IP is exposed).
3. **Data Analysis Assistance:** Summarizing generic, anonymous operational statistics or parsing public supply-chain market reports.
4. **Learning and Research:** Asking for explanations of technical concepts, logistics formulas, or translating general documentation into other European languages.

---

## 3. Prohibited AI Use Cases
To prevent legal, security, and compliance failures, the following practices are strictly prohibited:

* **No Automated Decision Making:** Employees must not use AI tools to automatically evaluate, accept, or reject job applications, employee performance ratings, or candidate resumes. Human-in-the-loop review is mandatory for all HR actions.
* **No Direct Output Copying for Customer Responses:** Support agents must never copy and paste AI-generated answers directly to customers without reviewing, editing, and verifying the contents against current official documentation (e.g., this SME Document Pack).
* **No Uploading of Proprietary Code or IP:** Employees must not input any proprietary code from our ERP system, webshop backend, or internal databases into third-party, consumer-grade AI models (such as public versions of ChatGPT or Gemini).
* **No Uploading of Sensitive or Personal Data (GDPR Violations):** It is a disciplinary offense to paste customer names, telephone numbers, emails, addresses, or purchase histories into any external AI platform.

---

## 4. Prompting & Verification Rules
To minimize the risk of AI "hallucinations" (the generation of false or incorrect facts), employees must adhere to the following workflow when generating work products with AI support:

[Define AI Task] ──► [Input Structured Prompt] ──► [Inspect AI Output]
│
▼
{Verify Facts?}
│
┌──────────────────────────────────────────────────┴──────────────────────────────────────────────────┐
▼ (Fact Confirmed) ▼ (Fact Unverified)
[Manual Human Edit / Check Policy Documents] [Delete AI Claim]
│ │
▼ ▼
[Finalize Document Approval] [Rewrite Query / Source Manually]

### 4.1 Verification Checklist before Publishing
Before sending any email, document, or report containing AI-assisted content to an external party (customer, vendor, or regulatory agency), the author must verify:
* **The "Zero-Hallucination" Check:** Every claim of fact, date, price, or policy threshold corresponds exactly with published BrightPath operational standards.
* **Tone Alignment:** The language is humble, polite, and aligned with our **Customer Support Policy (BP-POL-CSP-001, Section 6)**.
* **No Hidden Placeholders:** The document contains no residual LLM artifacts (e.g., *"As an AI, I cannot..."* or *"[Insert Name Here]"*).

---

## 5. Handling Confidential Corporate Information
"Confidential Information" refers to any data that is not explicitly published on the BrightPath website or in public press releases. This includes, but is not limited to:
* Vendor price agreements and volume discount schedules.
* Financial margins, transaction volumes, and warehouse capacity reports.
* Corporate partnership negotiations and strategic expansion plans.

*Rule:* Confidential Information must only be processed using BrightPath's internal, secured AI environment (the **BrightPath Enterprise AI Workspace**). It must never be exposed to public web scrapers or external machine-learning training data.

---

## 6. Accountability Statement
The use of AI does not relieve an employee of their professional responsibilities. 

* **The "Human Owner" Rule:** If an employee publishes a report, issues a customer refund, or schedules a delivery based on AI recommendations that turn out to be false or non-compliant, the employee—not the AI—is held accountable for the error.
* **Disciplinary Actions:** Violations of these guidelines (such as uploading customer lists to public AI models or automating HR recruitment) will be subject to HR investigation, written warnings, and potentially contract termination for gross misconduct.

---

## 7. Version Control & History
* **v1.0 (Nov 2023):** Initial internal release following pilot tests of generative AI tools.
* **v1.2 (Nov 2024):** Enhanced rules on human-in-the-loop verification, aligning with the EU AI Act classification of HR tools as "high risk." Added strict data protection warnings.