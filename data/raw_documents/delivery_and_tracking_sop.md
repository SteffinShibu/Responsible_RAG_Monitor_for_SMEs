# BrightPath Office Supplies - Delivery and Tracking SOP

**Document ID:** BP-SOP-DTS-003  
**Version:** 1.5  
**Effective Date:** December 1, 2024  
**Last Reviewed:** January 15, 2025  
**Document Owner:** Logistics & Warehouse Manager  
**Applies To:** Logistics Team, Dispatch Clerks, Customer Support Agents  

---

## 1. Purpose & Scope
This Standard Operating Procedure (SOP) outlines the guidelines, timelines, carrier expectations, and recovery procedures for shipping and delivering products from BrightPath Office Supplies to retail (B2C) and corporate (B2B) customers. This document guides our customer service agents and automated AI tools on how to track orders, manage delayed shipments, handle lost packages, and address shipping disputes.

---

## 2. Fulfillment and Shipping Timelines
All orders are shipped from our central warehouse in **Almere, Netherlands**. We partner with PostNL, DHL Express, and DPD for domestic and continental European shipments.

### 2.1 Standard Shipping Times
* **Netherlands & Belgium:** 1 to 2 business days.
* **Germany & Luxembourg:** 2 to 4 business days.
* **Rest of the European Union:** 4 to 8 business days.
* **Cut-Off Time:** Orders placed before **16:00 CET** Monday through Friday are dispatched on the same business day. Orders placed after 16:00 CET, or during weekends and public holidays, are dispatched the following business day.

### 2.2 Express Shipping Times
* **Benelux Region:** Next business day (for orders placed before 15:00 CET).
* **Rest of EU:** 2 business days.

---

## 3. Order Tracking Procedures
Upon courier pick-up, the customer is automatically emailed a Tracking Link and a unique Carrier Tracking ID (e.g., PostNL: `3S...`, DHL: `JVGL...`, DPD: `05...`).

### 3.1 AI Tracking Retrieval Rules
When a customer queries the AI Assistant regarding shipment location, the AI must strictly verify the following before disclosing any detail:
1. **The customer must provide the order number (Format: `BP-[YYYY]-[5 Digits]`, e.g., `BP-2024-88492`).**
2. **The customer must provide the delivery zip code (Postcode) for verification.**
3. If the tracking status shows "Delivered," but the customer disputes this, the AI must not make any assumptions. It must immediately escalate the query to a human agent and cross-reference **Section 4.1 (Disputed Deliveries)**.

---

## 4. Problem Resolution & Courier Escalation

### 4.1 Disputed Deliveries ("Delivered" but Not Received)
If courier tracking shows a package as "Delivered" but the customer claims they do not have it:
1. **Self-Check Prompt:** Advise the customer to check with immediate neighbors, building reception desks, or nearby parcel delivery points (Afhaallocatie).
2. **GPS / Proof of Delivery (PoD) Review:** Human agents (not the AI Assistant) must log into the carrier's merchant portal to retrieve the GPS delivery coordinates and the signature image (if applicable).
3. **Formal Investigation (Onderzoek):** If the package cannot be located, a human agent must open a formal dispute file with the courier within **5 business days** of the marked delivery date.
   * *Courier resolution time:* PostNL and DHL typically require 3 to 10 business days to complete their internal investigation.
   * *Customer Relief:* While the investigation is pending, BrightPath cannot issue a refund. For B2B clients, a supervisor may authorize a replacement shipment if the customer signs a "Declaration of Non-Receipt" (Verklaring van niet-ontvangst).

### 4.2 Delayed Package Process
A package is officially classified as "Delayed" if it has not arrived within **3 business days** past the maximum estimated delivery window (e.g., 5 business days for Netherlands delivery).
* **Action:** Support agents must initiate a tracking check via the carrier's system.
* **Communication Template:** Use *Template A-1* (see Section 6) to keep the customer informed.
* **Goodwill Trigger:** If the delay is caused solely by our logistics partner, apply the compensation outlined in **BP-POL-RRP-002, Section 4**.

### 4.3 Lost Package Process
A package is officially declared "Lost" when:
* The courier service formally states in writing/portal that the package is lost, OR
* The shipment has been inactive with no tracking updates for more than **10 consecutive calendar days** within the Benelux, or **15 consecutive calendar days** for international EU shipments.
* **Action:** Upon declaring a package lost, BrightPath will initiate a priority replacement order or issue a full refund, according to the customer's preference.

---

## 5. Courier Escalation Contacts & SLA
For logistics-only inquiries, BrightPath team members (never customers) contact carrier help desks via our partner channels:
* **PostNL Partner Support:** +31 (0) 88 868 6868 (Quote contract account number: `NL-99201`)
* **DHL Express Business Helpdesk:** `nl.express.business@dhl.com`
* **DPD Business Desk:** +31 (0) 85 002 2222

---

## 6. Customer Communication Templates (Human Agent Only)

### Template A-1: Delayed Shipment Notice
```text
Subject: Update regarding your BrightPath Order [Order Number]

Dear [Customer Name],

We are contacting you regarding your order [Order Number], which was dispatched on [Dispatch Date] via [Courier Name].

Our tracking shows that your package has met with an unexpected delay in transit. We sincerely apologize for this inconvenience. We are currently working closely with [Courier Name] to expedite delivery.

You can monitor your shipment's latest movement here: [Tracking Link].

If your order does not arrive by [Date = Today + 3 business days], please contact us directly, and we will initiate an official investigation and arrange for a solution.

Kind regards,
[Agent Name]
BrightPath Office Supplies

---

## 7. Scenarios Mandating AI Assistant Escalation

The AI Assistant is structurally restricted from managing shipping issues autonomously. It must immediately escalate the interaction to a human agent when:
1. The tracking status is "Returned to Sender" (RTS): This indicates a delivery failure due to address errors, repeated missed attempts, or damage in transit.
2. The customer explicitly states "My tracking is stuck" or "No movement for 3 days."
3. The customer mentions "customs fees" or "VAT charges" for international deliveries. (BrightPath ships from within the EU Schengen zone; customers within the EU should never receive customs notices. This could indicate a scam or warehouse sorting error).

---

## 8. Version Control & History
* **v1.0 (May 2022):** Document created.
* **v1.4 (Jan 2024):** Updated to reflect updated PostNL integration rules.
* **v1.5 (Dec 2024):** Added explicit AI escalation instructions for "Returned to Sender" statuses and tracking dispute rules.