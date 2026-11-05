# Customer Churn Analysis & Business Intelligence Report

**Project Title:** CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD  
**Discipline:** Pure Data Science, Exploratory Data Analysis & Business Intelligence  
**Dataset:** IBM Telco Customer Churn (7,043 customer accounts)  
**Methodology:** Parametric/Non-Parametric Descriptive Statistics, Contingency Analysis, Chi-Square Hypothesis Testing, Welch's Two-Sample T-Tests, and SQL Relational Modeling.  

### Project Team
| Student Name | Roll Number |
| :--- | :--- |
| G Mythili | 24311A67H8 |
| K Ashiwith | 24311A67H6 |
| D Niyati | 24311A67H7 |

**Institution:** Sreenidhi Institute of Science and Technology (Autonomous), Yamnampet, Ghatkesar, Hyderabad  
**Department:** Department of Data Science (CSE-DS)  
**Academic Year:** III Year, I Semester — November 2026  

---

## Executive Summary

This investigation analyzed 7,043 telecommunications accounts to understand customer defection patterns, quantify financial risk, and develop data-driven retention strategies without the opacity of black-box predictive models.

The baseline company metrics reveal an **overall customer churn rate of 26.54%** (1,869 churned accounts), eroding approximately **\$139,130 in monthly recurring revenue (MRR)** or **\$1.67 Million annually**. 

Statistical hypothesis testing demonstrates that churn is not random, nor is it driven by demographic traits like gender ($p = 0.487$). Rather, it is concentrated within specific contractual arrangements, payment channels, service technologies, and the initial 12 months of the customer journey.

---

## 1. Key Business Findings & Statistical Evidence

### 1.1 Contract Agreement: The Dominant Churn Factor
- **Chi-Square Statistic:** $\chi^2 = 1184.60$, $p = 5.86 \times 10^{-258}$
- **Effect Size (Cramér's V):** $0.410$ (Strongest association in entire dataset)
- **Month-to-month contracts:**
  - Total Customers: **3,875** (55.02% of customer base)
  - Churned Customers: **1,655**
  - **Churn Rate: 42.71%**
  - Month-to-month customers account for **88.55% of all churn in the entire company**.
- **One-year contracts:**
  - Total Customers: **1,473** (20.91% of base)
  - Churned Customers: **166**
  - **Churn Rate: 11.27%** (73.6% risk reduction vs. month-to-month)
- **Two-year contracts:**
  - Total Customers: **1,695** (24.07% of base)
  - Churned Customers: **48**
  - **Churn Rate: 2.83%** (93.4% risk reduction vs. month-to-month)

> **Key Takeaway:** Short-term agreements eliminate switching friction. Encouraging customers to commit to 1- or 2-year terms is the single most potent lever for reducing churn.

---

### 1.2 Payment Channel Friction: The Electronic Check Anomaly
- **Chi-Square Statistic:** $\chi^2 = 648.14$, $p = 3.68 \times 10^{-140}$
- **Effect Size (Cramér's V):** $0.303$ (Moderate-to-Strong)
- **Electronic Check:**
  - Total Customers: **2,365** (33.58% of base)
  - Churned Customers: **1,071**
  - **Churn Rate: 45.29%**
  - Represents **57.30% of all churned customers**.
- **Mailed Check:**
  - Total Customers: 1,612 | Churned: 308 | **Churn Rate: 19.11%**
- **Bank Transfer (Automatic):**
  - Total Customers: 1,544 | Churned: 258 | **Churn Rate: 16.71%**
- **Credit Card (Automatic):**
  - Total Customers: 1,522 | Churned: 232 | **Churn Rate: 15.24%**

> **Key Takeaway:** Customers utilizing manual Electronic Check payment have nearly **3x higher churn** than automated payment users. Manual payment prompts monthly conscious scrutiny of the bill, while automated methods create frictionless continuity.

---

### 1.3 Internet Technology & Price Sensitivity: The Fiber Optic Paradox
- **Fiber Optic Internet:**
  - Total Customers: **3,096** (43.96% of base)
  - Churned Customers: **1,297**
  - **Churn Rate: 41.89%**
  - Accounts for **69.39% of company churn**.
  - Average Monthly Charge: **\$91.50**
- **DSL Internet:**
  - Total Customers: 2,421 | Churned: 459 | **Churn Rate: 18.96%** | Avg Monthly Charge: **\$58.10**
- **No Internet Service (Phone Only):**
  - Total Customers: 1,526 | Churned: 113 | **Churn Rate: 7.40%** | Avg Monthly Charge: **\$21.08**

> **Key Takeaway:** Fiber optic customers are the highest monthly spenders, but churn at more than double the rate of DSL customers. The steep monthly bill (\$91.50 vs \$58.10) combined with service interruptions or inadequate tech support creates high churn vulnerability.

---

### 1.4 Tenure Cliff: The First 12 Months Danger Zone
- **Welch's Two-Sample T-Test on Tenure:**
  - Churned Customers Mean Tenure: **17.98 months** (Median: **10.00 months**)
  - Retained Customers Mean Tenure: **37.57 months** (Median: **38.00 months**)
  - Difference: **-19.59 months** ($t = -34.82$, $p = 1.20 \times 10^{-232}$, Cohen's $d = -0.852$)
- **Tenure Cohort Breakdown:**
  - **0-12 Months (New):** 2,186 customers | 1,037 churned | **47.44% Churn Rate** (55.48% of total churn occurs here)
  - **13-24 Months (Developing):** 1,024 customers | 294 churned | **28.71% Churn Rate**
  - **25-48 Months (Established):** 1,594 customers | 328 churned | **20.58% Churn Rate**
  - **49-72 Months (Loyal):** 2,239 customers | 210 churned | **9.38% Churn Rate**

> **Key Takeaway:** The defection hazard is front-loaded. A customer who survives the first 12 months is over 50% less likely to churn, and by year four, churn drops below 10%.

---

### 1.5 The Protective Power of Support & Security Services
- **Online Security:**
  - Without Security: Churn Rate = **41.77%**
  - With Security: Churn Rate = **14.61%** (65.0% risk reduction)
- **Tech Support:**
  - Without Tech Support: Churn Rate = **41.64%**
  - With Tech Support: Churn Rate = **15.17%** (63.6% risk reduction)
- **Full Support Bundle (Both Security + Tech Support):**
  - Customers with both features have a churn rate of just **11.84%**.

> **Key Takeaway:** Support and security add-ons act as a "retention anchor." When customers rely on the telco to protect their devices and resolve technical problems, switching costs multiply.

---

### 1.6 Demographic and Household Insights
- **Senior Citizens:**
  - Senior Citizens experience a **41.68% churn rate** vs **23.61% for non-seniors** ($\chi^2 = 159.44$, $p = 1.51 \times 10^{-36}$).
- **Partners & Dependents:**
  - Customers living alone churn at **32.96%**, compared to **19.66%** for customers with partners.
  - Customers without dependents churn at **31.28%**, compared to **15.45%** for families with dependents.
- **Gender Neutrality:**
  - Male Churn Rate: **26.16%** | Female Churn Rate: **26.92%**
  - $\chi^2 = 0.484$, $p = 0.487$ (Not statistically significant; gender does not influence customer churn).

---

## 2. Risk Matrix & Customer Segmentation

| Customer Segment Profile | Total Base | Churn Rate | Monthly Revenue | Risk Rating | Primary Vulnerability |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Month-to-month + Fiber Optic + Electronic Check** | 1,128 | **64.89%** | \$97,410 | 🔴 Critical | High cost, zero term commitment, manual friction |
| **New Customer (<12m) + No Tech Support** | 1,489 | **52.25%** | \$94,220 | 🔴 Critical | Early friction, unresolved technical onboarding |
| **Senior Citizens on Month-to-month** | 807 | **54.65%** | \$65,480 | 🟠 High | Budget pressure, complex service issues |
| **Month-to-month DSL Users** | 1,223 | **32.22%** | \$61,418 | 🟡 Moderate | Lower price cushions the churn hazard |
| **1-Year Contract Subscribers (Any Tech)** | 1,473 | **11.27%** | \$95,817 | 🟢 Low | Committed relationship, contractual friction |
| **2-Year Contract + Auto-Pay + Support** | 1,215 | **2.22%** | \$86,300 | 🟢 Minimal | Maximum stickiness, brand loyalists |

---

## 3. Data-Driven Strategic Recommendations

### Strategy 1: Contract Term Conversion Program
- **Tactic:** Launch an automated campaign targeting Month-to-month customers in months 3, 6, and 9 offering an annual contract incentive (e.g., "Lock in your rate with a \$10/month loyalty discount and free speed upgrade for 12 months").
- **Expected Impact:** Converting 20% of month-to-month customers (775 accounts) to 1-year agreements would reduce churners by approximately 244 customers, preserving **\$18,170 in MRR (\$218,000 annually)**.

### Strategy 2: Auto-Pay Migration & Billing Optimization
- **Tactic:** Offer a \$5 monthly recurring statement credit to all customers migrating from Electronic Check or Mailed Check to automatic Bank Transfer or Credit Card.
- **Expected Impact:** Transitioning 30% of Electronic Check users (710 accounts) to automated billing eliminates monthly decision friction, cutting segment churn from 45.3% to ~16.0% and saving approximately 208 accounts (**\$15,480 MRR**).

### Strategy 3: The "First 90 Days" Onboarding & Concierge Support
- **Tactic:** Establish a proactive customer success sequence for all new sign-ups:
  - Day 7: Automated connection diagnostic & satisfaction SMS.
  - Day 30: First bill walkthrough to eliminate billing surprises.
  - Day 60: Free 30-day trial of Online Security and Tech Support.
- **Expected Impact:** Reducing the first-year churn hazard from 47.4% to 35.0% preserves 272 customer accounts.

### Strategy 4: Fiber Optic Experience & Support Bundling
- **Tactic:** Bundle Online Security and Tech Support into the standard Fiber Optic tier at no additional standalone charge. Fiber optic customers pay \$91.50/month; including \$10 of perceived support value prevents defection of high-margin accounts.
- **Expected Impact:** Brings Fiber optic churn rate down from 41.9% closer to the DSL benchmark (19.0%), protecting the single highest MRR segment in the company.

### Strategy 5: Senior Citizen Friendly Care Package
- **Tactic:** Deploy dedicated phone-first customer support and simplified fixed-price senior plans to resolve technical hurdles without online ticket friction.

---

## 4. Retention Financial ROI Model

| Retention Target | Accounts Retained | Monthly Revenue Saved | Annual Revenue Protected |
| :--- | :---: | :---: | :---: |
| **Conservative (2% Churn Reduction)** | 141 | \$10,490 | **\$125,880** |
| **Moderate (5% Churn Reduction)** | 352 | \$26,200 | **\$314,400** |
| **Aggressive (8% Churn Reduction)** | 563 | \$41,910 | **\$502,920** |

*Calculations based on average churned customer monthly charge of \$74.44.*

---

## 5. Conclusion

This purely analytical, statistical, and business intelligence evaluation demonstrates that churn in the Telco business is systematic and predictable through business rules. 

By eliminating payment friction, incentivizing annual commitments, bundling security and technical support into high-speed fiber tiers, and fortifying the first 12 months of customer onboarding, the organization can substantially boost customer lifetime value (LTV) and protect over **\$300,000 to \$500,000 in annual recurring revenue**.
