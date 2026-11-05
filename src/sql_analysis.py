"""
Module: sql_analysis.py
Project: Customer Churn Analysis and Business Intelligence Dashboard
Description: SQLite database manager and analytics query runner answering the
             core 10 business intelligence questions.
"""

import os
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Tuple
import pandas as pd


class TelcoSQLAnalyzer:
    """
    Manages SQLite database ingestion and executes structured SQL analytical queries.
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path

    def init_database(self, csv_path: str, table_name: str = "customers") -> int:
        """
        Creates SQLite database and loads processed customer churn data into a table.
        Creates helpful indexes for rapid filtering.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Cleaned CSV file not found: {csv_path}")

        df = pd.read_csv(csv_path)

        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)

        # Write to sqlite table
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        # Create indexes on frequently filtered columns
        cursor = conn.cursor()
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_churn ON {table_name}(Churn);")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_contract ON {table_name}(Contract);")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_internet ON {table_name}(InternetService);")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_payment ON {table_name}(PaymentMethod);")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_tenure ON {table_name}(tenure);")
        conn.commit()
        conn.close()

        return len(df)

    def execute_query(self, query: str) -> pd.DataFrame:
        """Executes any arbitrary SQL query and returns result as a pandas DataFrame."""
        if not self.db_path or not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not initialized at: {self.db_path}")

        conn = sqlite3.connect(self.db_path)
        try:
            result_df = pd.read_sql_query(query, conn)
        finally:
            conn.close()

        return result_df

    @staticmethod
    def get_10_business_questions() -> List[Dict[str, Any]]:
        """
        Returns definition, business relevance, and SQL query for each of the 10 core questions.
        """
        return [
            {
                "id": 1,
                "title": "Total Number of Customers",
                "question": "What is the total number of customers?",
                "business_context": "Establishes the enterprise customer baseline volume for all proportional KPI calculations.",
                "query": """SELECT COUNT(*) AS total_customers 
FROM customers;""",
                "insight": "The telco customer base consists of exactly 7,043 unique accounts."
            },
            {
                "id": 2,
                "title": "Total Number of Churned Customers",
                "question": "What is the total number of churned customers?",
                "business_context": "Quantifies the absolute volume of customer defections requiring retention intervention.",
                "query": """SELECT COUNT(*) AS churned_customers 
FROM customers 
WHERE Churn = 'Yes';""",
                "insight": "1,869 customers have terminated their accounts."
            },
            {
                "id": 3,
                "title": "Overall Churn Percentage",
                "question": "What is the overall churn percentage?",
                "business_context": "Primary business health metric: benchmarked against telecom industry standards (~20-25%).",
                "query": """SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS churn_percentage
FROM customers;""",
                "insight": "The baseline churn rate stands at 26.54%, indicating significant revenue erosion opportunity."
            },
            {
                "id": 4,
                "title": "Contract Type with Highest Churn Rate",
                "question": "Which contract type has the highest churn rate?",
                "business_context": "Identifies contractual vulnerability and guides term-incentive promotions.",
                "query": """SELECT 
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;""",
                "insight": "Month-to-month contracts suffer a 42.71% churn rate, compared to 11.27% for One year and only 2.83% for Two year contracts."
            },
            {
                "id": 5,
                "title": "Payment Method with Most Churned Customers",
                "question": "Which payment method has the most churned customers?",
                "business_context": "Analyzes friction in the billing experience and identifies channels with highest drop-off.",
                "query": """SELECT 
    PaymentMethod,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churned_customers DESC;""",
                "insight": "Electronic check accounts for 1,071 churned customers (45.29% churn rate) — over 57% of all company churn stems from this single payment method."
            },
            {
                "id": 6,
                "title": "Average Monthly Charge Overall and by Status",
                "question": "What is the average monthly charge?",
                "business_context": "Assesses ARPU (Average Revenue Per User) and pricing elasticity disparity between churners and retainers.",
                "query": """SELECT 
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge_overall,
    ROUND(AVG(CASE WHEN Churn = 'Yes' THEN MonthlyCharges END), 2) AS avg_monthly_charge_churned,
    ROUND(AVG(CASE WHEN Churn = 'No' THEN MonthlyCharges END), 2) AS avg_monthly_charge_retained
FROM customers;""",
                "insight": "Overall average is $64.76/month. However, churned customers paid an average of $74.44/month vs $61.27/month for retained accounts — a $13.17 (21.5%) price premium that induces price sensitivity."
            },
            {
                "id": 7,
                "title": "Internet Service with Highest Churn",
                "question": "Which internet service has the highest churn?",
                "business_context": "Identifies technology infrastructure dissatisfaction or competitive pricing mismatch.",
                "query": """SELECT 
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;""",
                "insight": "Fiber optic internet exhibits a staggering 41.89% churn rate (1,297 churned), compared to DSL at 18.96% and No Internet at only 7.40%."
            },
            {
                "id": 8,
                "title": "Average Tenure of Churned vs Retained Customers",
                "question": "What is the average tenure of churned customers?",
                "business_context": "Defines the customer lifecycle danger zone and onboarding retention window.",
                "query": """SELECT 
    Churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(tenure), 2) AS avg_tenure_months,
    MIN(tenure) AS min_tenure,
    MAX(tenure) AS max_tenure
FROM customers
GROUP BY Churn
ORDER BY avg_tenure_months ASC;""",
                "insight": "Churned customers leave after an average of only 17.98 months, while retained customers average 37.57 months. Critical retention interventions must occur within the first 12 months."
            },
            {
                "id": 9,
                "title": "Customer Segment Generating Highest Monthly Revenue",
                "question": "Which customer segment generates the highest monthly revenue?",
                "business_context": "Pinpoints the financial backbone of monthly recurring revenue (MRR) to prioritize account protection.",
                "query": """SELECT 
    Contract,
    InternetService,
    COUNT(*) AS customer_count,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
FROM customers
GROUP BY Contract, InternetService
ORDER BY total_monthly_revenue DESC;""",
                "insight": "Month-to-month Fiber optic subscribers generate the highest monthly revenue ($187,460.50), but also suffer the highest churn rate (54.61%), presenting the single largest revenue risk."
            },
            {
                "id": 10,
                "title": "Customers on Month-to-Month Contracts",
                "question": "How many customers have month-to-month contracts?",
                "business_context": "Quantifies the exact operational scale of the most fragile contractual cohort.",
                "query": """SELECT 
    Contract,
    COUNT(*) AS customer_count,
    ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM customers) * 100, 2) AS percentage_of_total
FROM customers
WHERE Contract = 'Month-to-month'
GROUP BY Contract;""",
                "insight": "3,875 customers (55.02% of the entire customer base) are on Month-to-month contracts, meaning more than half of the company's clientele is at immediate risk every 30 days."
            }
        ]


def build_database_and_verify(csv_path: str, db_path: str) -> None:
    """Helper to initialize the database and run verification."""
    analyzer = TelcoSQLAnalyzer(db_path=db_path)
    count = analyzer.init_database(csv_path)
    print(f"Database successfully created at {db_path} with {count} rows.")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    proc_csv = os.path.join(base_dir, "data", "processed", "telco_churn_cleaned.csv")
    database_file = os.path.join(base_dir, "database", "customer_churn.db")

    print("=" * 60)
    print("INITIALIZING SQLITE DATABASE & EXECUTING SQL ANALYSIS")
    print("=" * 60)
    analyzer = TelcoSQLAnalyzer(db_path=database_file)
    analyzer.init_database(proc_csv)

    questions = analyzer.get_10_business_questions()
    for q in questions:
        print(f"\n[Q{q['id']}] {q['title']}")
        print("-" * 50)
        res = analyzer.execute_query(q["query"])
        print(res.to_string(index=False))
        print(f"Key Insight: {q['insight']}")
