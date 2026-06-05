# BrightPath Office Supplies - Productivity Baseline Notes

**Document ID:** BP-NOTE-PBN-009  
**Version:** 1.0  
**Effective Date:** December 20, 2024  
**Last Reviewed:** January 14, 2025  
**Document Owner:** Operations Manager & Lead Data Analyst  
**Applies To:** Operations Team, Executive Board, CX Analysts  

---

## 1. Purpose & Objectives
This document establishes the historical manual operational baseline for BrightPath Office Supplies' customer support operations prior to the full implementation of the **Responsible RAG Monitor and AI Support Assistant**. 

These statistics serve as the control dataset for statistical process control, business intelligence dashboards, and ROI evaluations. Later evaluations will compare AI-assisted performance against these historical baselines to measure efficiency gains, error rate reductions, and escalation behaviors.

---

## 2. Current Manual Workflow Description
Historically, our 6-person human support team handled all customer interactions manually.

[Inbound Support Request (Email/Web/Phone)]
                                  │
                                  ▼
                  [Manual Triage & CRM Tagging]
                                  │
                                  ▼
                    [Manual Knowledge Lookup]
                (Sifting through local PDF guides)
                                  │
                                  ▼
                     [Manual Response Draft]
                                  │
                                  ▼
                    [Direct Customer Delivery]

This process was slow, highly prone to individual agent interpretation, and suffered from inconsistent policy application across team members.

---

## 3. Average Historical Support Volumes & SLAs (Manual Era)
The following metrics represent the baseline averages calculated over the 12-month period spanning **November 1, 2023, to October 31, 2024**:

* **Average Weekly Inbound Tickets:** 850 tickets (all channels combined).
  * *Email:* 550 tickets/week
  * *Web Chat:* 180 chats/week
  * *Telephone:* 120 calls/week
* **First Response Time (FRT) Average:**
  * *Email:* 6.4 business hours.
  * *Web Chat (Human):* 4.2 minutes.
* **Resolution Time (RT) Average:**
  * *Standard Ticket:* 18.2 business hours.
  * *Complex Refund Ticket:* 42.5 business hours.

---

## 4. Quality, Escalation, and Error Baselines
Manual evaluation of 10% of closed tickets through periodic QA reviews revealed the following historical rates:

* **Manual Error Rate (Incorrect Policy Application):** **6.8%** of tickets. (Examples: issuing refunds without warehouse verification, quoting incorrect B2B return windows).
* **Escalation Rate (First-line to Supervisor):** **14.5%** of all inbound cases.
* **Customer Satisfaction Score (CSAT Baseline):** **72.0%** (Percentage of customers rating their interaction as "Satisfied" or "Highly Satisfied").
* **Average Operational Cost per Ticket:** **€8.50** (Calculated based on human labor, software licensing, and operational overheads).

---

## 5. Expected AI-Assisted Workflow (The Target State)
Following deployment of the "BrightPath AI Assistant" and the "Responsible RAG Monitor", the pipeline will transform:

[Inbound Web/Chat Request] ──► [AI RAG Retrieval] ──► [Responsible RAG Monitor Evaluation]
│
┌─────────────────────┴─────────────────────┐
▼ (Checks Pass) ▼ (Checks Fail)
[Instant AI Response] [Route to Human Tier-2/3]

Under this new workflow, we expect:
* AI handling of at least **60% of routine inquiries** (L1 level) without human intervention.
* Response times for automated channels to drop below **30 seconds**.
* Human team members focusing their time on L2, L3, and L4 escalated tickets.

---

## 6. Suggested Productivity Metrics for Ongoing Evaluation
To accurately track system performance, the monitoring software must calculate and display:

1. **Deflection Rate:** Percentage of chats resolved entirely by the AI assistant without human routing.
2. **Faithfulness / Hallucination Rate:** Frequency of LLM-as-Judge flagging an output as "unsupported by source documents."
3. **Escalation Precision:** Percentage of escalated tickets that actually met the Escalation Matrix criteria.
4. **SLA Breach Rate:** Percentage of tickets exceeding our first response or resolution targets.

---

## 7. Synthetic Baseline Data Table (Weekly Performance History)
This table represents synthetic historical data (pre-AI) for validation and model calibration.

| Week ID | Year | Total Inbound | Deflected (AI) | Escalated to Sup. | SLA Breaches | CSAT (%) | Avg Response (Hrs) | Incorrect Policy (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **W-40** | 2024 | 820 | 0 | 118 | 41 | 71.5 | 6.8 | 6.5 |
| **W-41** | 2024 | 845 | 0 | 126 | 38 | 73.0 | 6.2 | 7.0 |
| **W-42** | 2024 | 890 | 0 | 135 | 55 | 69.8 | 7.5 | 8.2 |
| **W-43** | 2024 | 810 | 0 | 110 | 29 | 74.2 | 5.9 | 5.8 |
| **W-44** | 2024 | 865 | 0 | 122 | 48 | 72.1 | 6.9 | 6.9 |
| **W-45** | 2024 | 910 | 0 | 141 | 62 | 68.4 | 8.1 | 7.5 |
| **W-46** | 2024 | 830 | 0 | 115 | 32 | 73.5 | 6.0 | 6.1 |
| **W-47** | 2024 | 875 | 0 | 130 | 50 | 71.9 | 7.1 | 7.0 |

---

## 8. Version Control & History
* **v1.0 (Dec 2024):** First compiled baseline dataset. Created by Lead Data Analyst, approved by Operations Manager.
