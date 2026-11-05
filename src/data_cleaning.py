"""
Module: data_cleaning.py
Project: Customer Churn Analysis and Business Intelligence Dashboard
Description: Robust pipeline for cleaning, auditing, validating, and enriching
             the IBM Telco Customer Churn dataset.
"""

import os
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


class TelcoDataCleaner:
    """
    Data Cleaning and Preprocessing pipeline for the Telco Customer Churn dataset.
    Performs data loading, duplicate checks, data type casting, missing value imputation,
    outlier detection via the IQR method, and business feature enrichment.
    """

    def __init__(self, raw_filepath: str = None):
        self.raw_filepath = raw_filepath
        self.audit_report: Dict[str, Any] = {}

    def load_data(self, filepath: str = None) -> pd.DataFrame:
        """Loads the raw Telco dataset from CSV."""
        path = filepath or self.raw_filepath
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"Raw data file not found at: {path}")
        
        df = pd.read_csv(path)
        self.audit_report["initial_shape"] = df.shape
        self.audit_report["initial_columns"] = df.columns.tolist()
        return df

    def check_duplicates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """Detects and removes duplicate records."""
        duplicate_count = int(df.duplicated().sum())
        self.audit_report["duplicates_found"] = duplicate_count
        if duplicate_count > 0:
            df = df.drop_duplicates().reset_index(drop=True)
        return df, duplicate_count

    def handle_data_types_and_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fixes incorrect data types, specifically TotalCharges which contains
        whitespace strings, converting them to numeric and imputing tenure=0 cases.
        """
        df = df.copy()

        # Identify missing values before processing
        initial_missing = df.isnull().sum().to_dict()
        self.audit_report["initial_null_counts"] = initial_missing

        # TotalCharges has whitespace strings for new customers (tenure = 0)
        blank_total_charges = int((df["TotalCharges"].astype(str).str.strip() == "").sum())
        self.audit_report["blank_total_charges_count"] = blank_total_charges

        # Convert TotalCharges to numeric, replacing blanks with NaN
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce")

        # For customers with tenure == 0, TotalCharges is legitimately 0.0 (no billed cycle yet)
        zero_tenure_mask = (df["tenure"] == 0) & (df["TotalCharges"].isnull())
        df.loc[zero_tenure_mask, "TotalCharges"] = 0.0

        # In case any remaining NaNs exist, fill with median
        remaining_nan = int(df["TotalCharges"].isnull().sum())
        if remaining_nan > 0:
            median_val = df["TotalCharges"].median()
            df["TotalCharges"] = df["TotalCharges"].fillna(median_val)
            self.audit_report["total_charges_median_imputed"] = remaining_nan

        # Ensure tenure is integer
        df["tenure"] = df["tenure"].astype(int)

        # Ensure MonthlyCharges is float
        df["MonthlyCharges"] = df["MonthlyCharges"].astype(float)

        # Standardize SeniorCitizen: create SeniorCitizenLabel for clear BI visualization
        df["SeniorCitizenLabel"] = df["SeniorCitizen"].map({1: "Yes", 0: "No"}).fillna("No")

        # Strip any extra whitespace from string categorical columns
        cat_cols = df.select_dtypes(include=["object", "string"]).columns
        for col in cat_cols:
            df[col] = df[col].astype(str).str.strip()

        self.audit_report["final_null_counts"] = df.isnull().sum().to_dict()
        return df

    def detect_outliers_iqr(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Checks for numerical outliers using the Interquartile Range (IQR) rule:
        [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
        """
        outlier_summary = {}
        num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]

        for col in num_cols:
            q1 = float(df[col].quantile(0.25))
            q3 = float(df[col].quantile(0.75))
            iqr = q3 - q1
            lower_bound = float(q1 - 1.5 * iqr)
            upper_bound = float(q3 + 1.5 * iqr)

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_count = int(len(outliers))

            outlier_summary[col] = {
                "Q1": round(q1, 2),
                "Q3": round(q3, 2),
                "IQR": round(iqr, 2),
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "outlier_count": outlier_count,
                "outlier_percentage": round((outlier_count / len(df)) * 100, 2)
            }

        self.audit_report["outlier_analysis"] = outlier_summary
        return outlier_summary

    def enrich_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds domain-specific categorical groupings for customer segmentation
        and business analytics.
        """
        df = df.copy()

        # 1. Churn Binary Indicator
        df["ChurnBinary"] = (df["Churn"].str.lower() == "yes").astype(int)

        # 2. Customer Tenure Cohort
        # 0-12 months: High-risk trial period
        # 13-24 months: Developing relationship
        # 25-48 months: Established accounts
        # 49-72 months: Brand loyalists
        bins_tenure = [-1, 12, 24, 48, 72]
        labels_tenure = ["0-12 Months (New)", "13-24 Months (Developing)", 
                         "25-48 Months (Established)", "49-72 Months (Loyal)"]
        df["TenureCohort"] = pd.cut(df["tenure"], bins=bins_tenure, labels=labels_tenure)

        # 3. Monthly Charges Spend Tier
        # Low: < $35 (Basic phone / economy)
        # Medium: $35 - $70 (Standard bundle)
        # High: > $70 (Premium bundle / fiber optic)
        bins_charges = [0, 35, 70, 150]
        labels_charges = ["Low (<$35)", "Medium ($35-$70)", "High (>$70)"]
        df["MonthlyChargesTier"] = pd.cut(df["MonthlyCharges"], bins=bins_charges, labels=labels_charges)

        # 4. Service Adoption Count
        # Evaluate how many value-added services customer has subscribed to
        services = [
            "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
            "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
        ]
        
        def count_services(row):
            count = 0
            for s in services:
                val = str(row.get(s, "")).strip().lower()
                if val == "yes":
                    count += 1
            return count

        df["NumServices"] = df.apply(count_services, axis=1)

        # 5. Service Bundle Category
        def classify_bundle(row):
            has_internet = str(row.get("InternetService", "")).lower() != "no"
            has_phone = str(row.get("PhoneService", "")).lower() == "yes"
            if has_internet and has_phone:
                return "Triple/Double Play (Both)"
            elif has_internet:
                return "Internet Only"
            elif has_phone:
                return "Phone Only"
            return "No Main Service"

        df["ServiceBundle"] = df.apply(classify_bundle, axis=1)

        # 6. Support & Security Package Flag
        has_sec = (df["OnlineSecurity"].str.lower() == "yes")
        has_sup = (df["TechSupport"].str.lower() == "yes")
        df["HasSecurityAndSupport"] = np.where(
            has_sec & has_sup, "Both Services",
            np.where(has_sec, "Security Only",
                     np.where(has_sup, "Tech Support Only", "Neither Service"))
        )

        return df

    def clean_pipeline(self, input_filepath: str = None, output_filepath: str = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Executes the full data cleaning, auditing, and feature enrichment pipeline.
        Saves processed data to output_filepath.
        """
        # Step 1: Load
        df_raw = self.load_data(input_filepath)

        # Step 2: Remove duplicates
        df_nodup, _ = self.check_duplicates(df_raw)

        # Step 3: Handle data types and missing values
        df_typed = self.handle_data_types_and_missing(df_nodup)

        # Step 4: Detect outliers
        self.detect_outliers_iqr(df_typed)

        # Step 5: Feature Enrichment
        df_enriched = self.enrich_features(df_typed)

        # Step 6: Validate consistency
        self.audit_report["final_shape"] = df_enriched.shape
        self.audit_report["final_columns"] = df_enriched.columns.tolist()
        self.audit_report["total_customers"] = int(len(df_enriched))
        self.audit_report["churn_rate_pct"] = round(float(df_enriched["ChurnBinary"].mean() * 100), 2)

        # Step 7: Save to processed destination
        if output_filepath:
            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
            df_enriched.to_csv(output_filepath, index=False)
            self.audit_report["saved_to"] = output_filepath

        return df_enriched, self.audit_report


def clean_and_save_data(raw_csv_path: str, processed_csv_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Convenience helper function to run the full cleaning pipeline."""
    cleaner = TelcoDataCleaner(raw_filepath=raw_csv_path)
    return cleaner.clean_pipeline(output_filepath=processed_csv_path)


if __name__ == "__main__":
    # Standard standalone run
    base_dir = Path(__file__).resolve().parent.parent
    raw_path = os.path.join(base_dir, "data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
    proc_path = os.path.join(base_dir, "data", "processed", "telco_churn_cleaned.csv")

    print("=" * 60)
    print("CUSTOMER CHURN DATA CLEANING PIPELINE")
    print("=" * 60)
    df_clean, audit = clean_and_save_data(raw_path, proc_path)
    print(f"Initial Shape: {audit['initial_shape']}")
    print(f"Duplicates Removed: {audit['duplicates_found']}")
    print(f"Blank TotalCharges Fixed: {audit['blank_total_charges_count']}")
    print(f"Final Shape: {audit['final_shape']}")
    print(f"Churn Rate: {audit['churn_rate_pct']}%")
    print(f"Processed file saved to: {audit['saved_to']}")
    print("\nOutlier Detection Summary (IQR Method):")
    for col, stats in audit["outlier_analysis"].items():
        print(f" - {col}: {stats['outlier_count']} outliers ({stats['outlier_percentage']}%) | Range: [{stats['lower_bound']}, {stats['upper_bound']}]")
    print("=" * 60)
