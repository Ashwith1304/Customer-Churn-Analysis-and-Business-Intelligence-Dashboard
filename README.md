# Customer Churn Analysis and Business Intelligence Dashboard

An end-to-end Data Science, Statistical Analytics, and Business Intelligence project exploring customer retention, churn drivers, and revenue optimization in the telecommunications sector.

---

## 1. Project Title

**Customer Churn Analysis and Business Intelligence Dashboard**

---

## 2. Project Team

| Student Name | Roll Number |
| :--- | :--- |
| G Mythili | 24311A67H8 |
| K Ashiwith | 24311A67H6 |
| D Niyati | 24311A67H7 |

**Institution:** Sreenidhi Institute of Science and Technology (Autonomous), Yamnampet, Ghatkesar, Hyderabad  
**Department:** Department of Data Science (CSE-DS)  
**Academic Year:** III Year, I Semester — November 2026  

---

## 3. Project Overview

Customer churn is one of the biggest challenges subscription businesses face. In the telecommunications industry, retaining existing subscribers is significantly more cost-effective than acquiring new ones.

This project delivers an interactive Business Intelligence application and empirical data analysis of telecom customer churn. The project focuses on data cleaning, exploratory data analysis (EDA), descriptive and inferential statistics, relational SQL querying via SQLite, and an interactive multi-page dashboard built with Streamlit and Plotly.

---

## 3. Problem Statement

A telecom service provider is seeing customer attrition that erodes monthly recurring revenue (MRR). Management needs clear, reliable answers to key questions:

- Why are customers leaving the service?
- Which contract terms and payment methods experience the highest churn?
- How do monthly charges and customer tenure relate to customer churn?
- Which value-added services protect customers from leaving?
- What practical, data-backed actions can the company take to improve retention?

---

## 4. Project Objectives

- Clean and validate raw customer records, resolving missing values and verifying outlier thresholds.
- Perform descriptive statistics (mean, median, mode, standard deviation, quartiles, IQR, skewness, and kurtosis).
- Conduct bivariate and multivariate exploratory data analysis across demographic, contractual, and service features.
- Run statistical hypothesis tests: Pearson's Chi-Square Test of Independence ($\chi^2$) with Cramér's V effect size, and Welch's two-sample independent t-tests.
- Load cleaned data into an SQLite database (`customer_churn.db`) and write SQL queries to answer 10 core business questions.
- Build an interactive, multi-page Streamlit dashboard with responsive KPI metrics, dynamic global filters, an interactive SQL sandbox, and a customer retention ROI calculator.

---

## 5. Dataset Information

The project analyzes the **IBM Telco Customer Churn Dataset** ([Kaggle BlastChar](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)), containing **7,043 customer accounts** across **21 attributes**:

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `customerID` | Object / String | Unique alphanumeric customer account identifier |
| `gender` | Categorical | Customer gender ('Male', 'Female') |
| `SeniorCitizen` | Integer (0/1) | Whether the customer is a senior citizen |
| `Partner` | Categorical | Whether the customer has a partner ('Yes', 'No') |
| `Dependents` | Categorical | Whether the customer has dependents ('Yes', 'No') |
| `tenure` | Integer (Months) | Number of months the customer has stayed with the company |
| `PhoneService` | Categorical | Fixed telephone landline subscription ('Yes', 'No') |
| `MultipleLines` | Categorical | Whether customer has multiple phone lines |
| `InternetService` | Categorical | Technology delivery ('DSL', 'Fiber optic', 'No') |
| `OnlineSecurity` | Categorical | Cybersecurity firewall protection add-on ('Yes', 'No') |
| `OnlineBackup` | Categorical | Cloud data backup service add-on ('Yes', 'No') |
| `DeviceProtection` | Categorical | Equipment replacement warranty add-on ('Yes', 'No') |
| `TechSupport` | Categorical | Dedicated technical support subscription ('Yes', 'No') |
| `StreamingTV` | Categorical | Digital TV streaming package ('Yes', 'No') |
| `StreamingMovies` | Categorical | Digital movie streaming package ('Yes', 'No') |
| `Contract` | Categorical | Agreement term ('Month-to-month', 'One year', 'Two year') |
| `PaperlessBilling` | Categorical | Digital email billing statements ('Yes', 'No') |
| `PaymentMethod` | Categorical | Billing method (Electronic check, Mailed check, Bank transfer, Credit card) |
| `MonthlyCharges` | Float64 ($) | Recurring monthly bill amount |
| `TotalCharges` | Object -> Float64 ($) | Cumulative charges billed across customer lifetime |
| `Churn` | Categorical (Target) | Whether customer left during the observation period ('Yes', 'No') |

### Downloading and Uploading the Dataset

1. **Automatic Download in Dashboard:** The dashboard includes an instant download button for the raw Kaggle dataset directly in the sidebar.
2. **Kaggle Link:** The dataset can also be downloaded directly from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).
3. **Custom CSV Upload:** If you have an updated or alternative dataset, you can upload it using the file uploader in the dashboard sidebar.

---

## 6. Technology Stack

- **Python 3.10+ / 3.14:** Core data processing, analytics, and application logic.
- **Pandas:** Data loading, cleaning, grouping, and feature engineering.
- **NumPy:** Mathematical calculations and array operations.
- **SciPy (`scipy.stats`):** Chi-Square tests of independence, Cramér's V, and Welch's two-sample t-tests.
- **Plotly Express & Graph Objects:** Interactive, responsive charts with tooltips and custom themes.
- **Matplotlib & Seaborn:** Publication-ready 300 DPI static chart generation.
- **SQLite 3:** Relational database storage with b-tree indexing for query execution.
- **Streamlit:** Modern web application framework with reactive state management.

---

## 7. Project Directory Structure

```text
customer-churn-analysis/
│
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv    # Original raw dataset from Kaggle
│   └── processed/
│       └── telco_churn_cleaned.csv                # Cleaned, audited, and enriched dataset
│
├── notebooks/
│   └── exploratory_analysis.ipynb                 # Jupyter Notebook with step-by-step EDA
│
├── src/
│   ├── data_cleaning.py                           # Data cleaning, type conversion, and outlier checks
│   ├── descriptive_statistics.py                  # Descriptive stats, Chi-Square, and Welch's t-tests
│   ├── eda.py                                     # Matplotlib/Seaborn static & Plotly interactive visuals
│   └── sql_analysis.py                            # SQLite database manager & 10 core business queries
│
├── database/
│   └── customer_churn.db                          # Relational SQLite database
│
├── visualizations/                                # 10 high-resolution static charts (300 DPI)
│   ├── 01_churn_distribution_pie.png
│   ├── 02_contract_churn_bar.png
│   ├── 03_monthly_charges_histogram.png
│   ├── 04_tenure_boxplot.png
│   ├── 05_correlation_heatmap.png
│   ├── 06_payment_methods_churn_bar.png
│   ├── 07_tenure_monthly_charges_scatter.png
│   ├── 08_customer_segments_grouped_bar.png
│   ├── 09_internet_service_churn.png
│   └── 10_service_addons_churn.png
│
├── app/
│   └── streamlit_app.py                           # 9-page Streamlit Business Intelligence application
│
├── reports/
│   └── business_insights.md                       # Detailed analytical report and findings
│
├── requirements.txt                               # Project dependencies
├── README.md                                      # Project documentation
└── .gitignore                                     # Python gitignore file
```

---

## 8. Data Cleaning and Preprocessing

The cleaning pipeline in `src/data_cleaning.py` performs the following steps:

1. **Duplicate Check:** Verified that all 7,043 records are unique (0 duplicates found).
2. **Whitespace Value Resolution:** Handled 11 blank space strings (`" "`) in `TotalCharges`. All 11 records correspond to new customers where `tenure == 0`. Converted the column to `float64` and imputed `$0.0` for accounts with zero completed billing cycles, preserving 100% of rows without dropping data.
3. **Categorical Normalization:** Trimmed leading and trailing whitespace across all text columns. Mapped `SeniorCitizen` (0/1) to `SeniorCitizenLabel` ('Yes'/'No') for clearer reporting.
4. **Outlier Detection:** Evaluated continuous metrics (`tenure`, `MonthlyCharges`, `TotalCharges`) using the $1.5 \times \text{IQR}$ rule:
   - `tenure`: Range [0, 72] months, 0 outliers.
   - `MonthlyCharges`: Range [\$18.25, \$118.75], 0 outliers.
   - `TotalCharges`: Range [\$0.0, \$8,684.80], 0 outliers.
5. **Feature Engineering:**
   - `ChurnBinary`: Binary integer flag (1 for Churned, 0 for Retained).
   - `TenureCohort`: Binned categories (`0-12m`, `13-24m`, `25-48m`, `49-72m`).
   - `MonthlyChargesTier`: Spend tiers (`Low <$35`, `Medium $35-$70`, `High >$70`).
   - `NumServices`: Total count of subscribed add-on features (0 to 8).

Cleaned records are saved in `data/processed/telco_churn_cleaned.csv` (7,043 rows × 28 columns).

---

## 9. Exploratory Data Analysis

Implemented across `src/eda.py` and `notebooks/exploratory_analysis.ipynb`:

- **Univariate Analysis:**
  - Churn distribution: 5,174 retained accounts (73.46%) vs 1,869 churned accounts (26.54%).
  - Tenure distribution: Bimodal shape with high peaks at 1 month (new trials) and 72 months (loyal base).
  - Monthly charges: Peak at ~\$20 (basic phone service), followed by a broad distribution between \$70 and \$100 (broadband bundles).
- **Bivariate Analysis:**
  - Churn by Contract: Month-to-month contracts experience a 42.71% churn rate, compared to 11.27% for 1-year and 2.83% for 2-year.
  - Churn by Payment Method: Electronic check churn is 45.29% vs ~15-16% for automated credit cards and bank transfers.
  - Tenure vs Churn: Median tenure of churned customers is only 10 months vs 38 months for retained accounts.
- **Multivariate Analysis:**
  - Correlation heatmap examining linear relationships between tenure, charges, and defection.
  - Interaction cross-tabulations examining churn rate across contract types and payment channels simultaneously.

---

## 10. Statistical Analysis

Implemented in `src/descriptive_statistics.py`:

### Summary Statistics Table

| Metric | Mean | Median | Mode | Std Dev | Min | Q1 | Q2 | Q3 | Max | IQR | Skewness | Kurtosis |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **tenure** | 32.37 | 29.00 | 1.00 | 24.56 | 0.00 | 9.00 | 29.00 | 55.00 | 72.00 | 46.00 | +0.240 | -1.387 |
| **MonthlyCharges** | 64.76 | 70.35 | 20.05 | 30.09 | 18.25 | 35.50 | 70.35 | 89.85 | 118.75 | 54.35 | -0.221 | -1.257 |
| **TotalCharges** | 2279.73 | 1394.55 | 0.00 | 2266.79 | 0.00 | 398.55 | 1394.55 | 3786.60 | 8684.80 | 3388.05 | +0.963 | -0.229 |

### Chi-Square ($\chi^2$) Test of Independence & Cramér's V

Evaluates whether categorical attributes are statistically associated with customer churn:

| Feature | $\chi^2$ Stat | p-value | df | Cramér's V | Association Strength | Conclusion |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Contract** | 1184.60 | $< 10^{-250}$ | 2 | **0.410** | Strong Association | Significant ($p < 0.001$) |
| **OnlineSecurity** | 850.00 | $< 10^{-180}$ | 2 | 0.347 | Moderate Association | Significant ($p < 0.001$) |
| **TechSupport** | 828.20 | $< 10^{-180}$ | 2 | 0.343 | Moderate Association | Significant ($p < 0.001$) |
| **InternetService** | 732.31 | $< 10^{-150}$ | 2 | 0.322 | Moderate Association | Significant ($p < 0.001$) |
| **PaymentMethod** | 648.14 | $< 10^{-140}$ | 3 | 0.303 | Moderate Association | Significant ($p < 0.001$) |
| **gender** | 0.48 | 0.487 | 1 | 0.008 | Negligible Association | **Not Significant** ($p = 0.487$) |

### Welch's Two-Sample Independent T-Tests

Tests whether mean differences between churned and retained customers are statistically significant:

- **Tenure:** Churned customers stay an average of 17.98 months vs 37.57 months for retained customers (difference of -19.59 months, $t = -34.82$, $p < 10^{-200}$, Cohen's $d = -0.852$ — large effect size).
- **Monthly Charges:** Churned customers paid an average of \$74.44/month vs \$61.27/month for retained accounts (difference of +\$13.18/month, $t = +18.41$, $p < 10^{-70}$ — significant price premium).

---

## 11. SQL Business Analysis

Cleaned records are stored in an SQLite database (`database/customer_churn.db`) under table `customers`. The `src/sql_analysis.py` module answers the 10 core business questions:

```sql
-- Total Customers
SELECT COUNT(*) AS total_customers FROM customers; -- 7,043

-- Total Churned Customers
SELECT COUNT(*) AS churned_customers FROM customers WHERE Churn = 'Yes'; -- 1,869

-- Overall Churn Percentage
SELECT ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS churn_pct 
FROM customers; -- 26.54%

-- Highest Churn Contract
SELECT Contract, COUNT(*) AS total, SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
       ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS rate
FROM customers GROUP BY Contract ORDER BY rate DESC;

-- Most Churned Payment Method
SELECT PaymentMethod, COUNT(*) AS total, SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned
FROM customers GROUP BY PaymentMethod ORDER BY churned DESC;

-- Average Monthly Charges
SELECT ROUND(AVG(MonthlyCharges), 2) AS avg_overall,
       ROUND(AVG(CASE WHEN Churn = 'Yes' THEN MonthlyCharges END), 2) AS avg_churned,
       ROUND(AVG(CASE WHEN Churn = 'No' THEN MonthlyCharges END), 2) AS avg_retained
FROM customers;

-- Internet Service Highest Churn
SELECT InternetService, ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS rate
FROM customers GROUP BY InternetService ORDER BY rate DESC;

-- Average Tenure of Churned vs Retained
SELECT Churn, ROUND(AVG(tenure), 2) AS avg_tenure FROM customers GROUP BY Churn;

-- Top Monthly Revenue Segment
SELECT Contract, InternetService, ROUND(SUM(MonthlyCharges), 2) AS total_mrr
FROM customers GROUP BY Contract, InternetService ORDER BY total_mrr DESC;

-- Month-to-Month Contract Volume
SELECT Contract, COUNT(*) AS total, ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM customers) * 100, 2) AS pct
FROM customers WHERE Contract = 'Month-to-month' GROUP BY Contract;
```

---

## 12. Dashboard Features

The application (`app/streamlit_app.py`) includes 9 dedicated pages:

1. **Executive Overview:** 6 KPI cards with inline SVG sparklines, retention health gauge, revenue dynamics spline chart, contract and payment charts, and key empirical observations.
2. **Customer Data Explorer:** Filterable and searchable customer table, feature dictionary, and one-click CSV download.
3. **Data Quality Report:** Step-by-step remediation summary, whitespace resolution report, and IQR outlier boundaries.
4. **Exploratory Data Analysis:** Dedicated tabs for univariate distributions, bivariate churn cross-tabulations, and multivariate correlation matrices.
5. **Statistical Insights:** Parametric summary table, Chi-Square independence tests with Cramér's V ranking, Welch's t-tests, and plain-language statistical interpretations.
6. **SQL Analytics:** View queries and results for all 10 business questions + live custom SQL sandbox.
7. **Customer Segmentation:** Tenure cohort lifecycle breakdown, 2D vulnerability grid (Tenure × Spend Tier), and danger zone customer explorer.
8. **Business Recommendations:** 4-part framework recommendations and an interactive customer retention ROI financial calculator.
9. **Project Information:** Technical specifications, architecture overview, and Kaggle dataset citation.

---

## 13. Key Business Questions

1. **What is the overall churn rate?**  
   26.54% (1,869 out of 7,043 customers).
2. **Which contract type is most vulnerable?**  
   Month-to-month contracts experience a 42.71% churn rate and account for 88.55% of all defected customers.
3. **Which payment method causes the most churn?**  
   Electronic check (45.29% churn rate), accounting for over 57.3% of all churned accounts.
4. **When do customers leave?**  
   Over 55.5% of all defection happens in the first 12 months. Churned customers have a median tenure of only 10 months.
5. **How does pricing affect churn?**  
   Churned customers paid an average of \$74.44/month vs \$61.27/month for retained accounts (a \$13.18/month premium).
6. **Do support services reduce churn?**  
   Yes. Customers with Tech Support churn at 15.17% vs 41.64% for customers without support.

---

## 14. Business Recommendations

Each recommendation follows a structured four-part framework:

1. **Annual Contract Term Transition:**
   - *Observed Finding:* Month-to-month accounts churn at 42.71% vs 2.83% for two-year contracts.
   - *Supporting Statistic:* Month-to-month contracts represent 88.55% of all churn in the company.
   - *Business Impact:* High defection volume creates severe recurring revenue volatility.
   - *Suggested Action:* Offer a \$10/month statement credit or speed upgrade at Month 3 in exchange for an annual contract commitment.
2. **Auto-Pay Billing Optimization:**
   - *Observed Finding:* Electronic check accounts churn at 45.29%, nearly 3x higher than automated credit cards (15.24%).
   - *Supporting Statistic:* Over 57.3% of all churned customers use Electronic Check.
   - *Business Impact:* Manual payments cause monthly friction and conscious value re-evaluation.
   - *Suggested Action:* Provide a \$5/month recurring bill discount for enrolling in Credit Card or Bank Auto-Pay.
3. **The First 90 Days Onboarding Journey:**
   - *Observed Finding:* 55.5% of all defection occurs in the first 12 months (median churn tenure is 10 months).
   - *Supporting Statistic:* The 0-12m cohort churns at 47.44%, while the 49-72m cohort churns at only 9.38%.
   - *Business Impact:* Customer acquisition cost (CAC) is lost before accounts reach profitability.
   - *Suggested Action:* Implement a proactive onboarding journey: Day 7 connection check, Day 30 bill walkthrough, and Day 60 speed optimization check.
4. **Fiber Optic Support Bundling:**
   - *Observed Finding:* Fiber optic churns at 41.89% (\$91.50/month average bill), but churn drops to 11.84% when accounts include both Tech Support and Online Security.
   - *Supporting Statistic:* Accounts with Tech Support churn at 15.17% vs 41.64% without support.
   - *Business Impact:* High-revenue customers defect when experiencing unaddressed technical issues.
   - *Suggested Action:* Bundle complimentary Tech Support and Online Security directly into Fiber Optic subscription tiers.

---

## 15. Installation Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14 Windows 64-bit)
- Windows PowerShell or Command Prompt

### Step 1: Navigate to Project Directory
```powershell
cd "c:\Users\KONDAMADUGU ASHWITH\Downloads\intern\customer-churn-analysis"
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 16. How to Run the Project

Execute the data pipeline and launch the dashboard using Windows PowerShell:

```powershell
# 1. Clean raw data and generate processed CSV
python src/data_cleaning.py

# 2. Run descriptive statistics and hypothesis tests
python src/descriptive_statistics.py

# 3. Initialize SQLite database and execute 10 business queries
python src/sql_analysis.py

# 4. Generate high-resolution static charts in visualizations/
python src/eda.py

# 5. Launch the Streamlit Business Intelligence Dashboard
python -m streamlit run app/streamlit_app.py
```

Once running, open your web browser at:  
👉 **`http://localhost:8501`**

---

## 17. Screenshots

The dashboard interface includes:

- **Executive KPI Cards:** Total Customers (`7,043`), Active Customers (`5,174`), Churned Customers (`1,869`), Churn Rate (`26.54%`), ARPU (`$64.76`), and Total MRR (`$456,117`) with inline SVG sparklines.
- **Revenue Dynamics Area Chart:** Smooth spline chart displaying monthly revenue dynamics across customer tenure cohorts.
- **Contract & Payment Visualizations:** Grouped bar charts showing churn and retention across agreements and billing channels.
- **Interactive SQL Console:** Live SQL query editor and result tables executed against SQLite.
- **Retention ROI Simulator:** Interactive slider projecting preserved accounts, monthly revenue saved, and annual revenue protected.

---

## 18. Future Enhancements

- **Automated Cohort Retention Tracking:** Track customer cohorts over time to calculate quarterly cohort survival rates.
- **Customer Lifetime Value (CLV) Modeling:** Incorporate historical tenure distribution to calculate customer lifetime value across segments.
- **Automated Email Reports:** Export executive summary PDF reports for weekly management briefings.
- **Expanded Database Connectors:** Support direct connections to PostgreSQL and Snowflake for enterprise data pipelines.

---

## 19. Conclusion

This project demonstrates how rigorous exploratory data analysis, descriptive statistics, hypothesis testing, and relational SQL queries provide clear, actionable business insights without the complexity of black-box models.

By identifying the primary drivers of defection — month-to-month contracts, manual electronic check payments, first-year onboarding vulnerability, and unsupported fiber optic pricing — telecom leadership can take concrete, data-backed actions to protect over **\$300,000 to \$500,000 in annual recurring revenue**.
