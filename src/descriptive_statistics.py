"""
Module: descriptive_statistics.py
Project: Customer Churn Analysis and Business Intelligence Dashboard
Description: Comprehensive statistical calculations including central tendency,
             dispersion, quartile distributions, categorical frequencies,
             and statistical hypothesis tests (Chi-Square & T-Tests).
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from scipy import stats


class DescriptiveStatisticsEngine:
    """
    Engine for calculating descriptive, bivariate, and inferential statistics
    for customer churn data without machine learning.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
        self.cat_cols = [
            "gender", "SeniorCitizenLabel", "Partner", "Dependents",
            "PhoneService", "MultipleLines", "InternetService",
            "OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies",
            "Contract", "PaperlessBilling", "PaymentMethod", "Churn"
        ]

    def get_numerical_summary(self) -> pd.DataFrame:
        """
        Calculates complete descriptive statistics for numerical columns:
        Mean, Median, Mode, Std, Variance, Min, Max, Q1, Q2, Q3, IQR,
        Skewness, and Kurtosis.
        """
        summary_records = []
        for col in self.num_cols:
            if col not in self.df.columns:
                continue
            series = self.df[col].dropna()
            
            # Mode calculation
            mode_series = series.mode()
            mode_val = mode_series.iloc[0] if not mode_series.empty else np.nan

            q1 = series.quantile(0.25)
            q2 = series.quantile(0.50)  # Median
            q3 = series.quantile(0.75)
            iqr = q3 - q1

            summary_records.append({
                "Metric": col,
                "Count": int(series.count()),
                "Mean": round(float(series.mean()), 2),
                "Median": round(float(series.median()), 2),
                "Mode": round(float(mode_val), 2),
                "Std Dev": round(float(series.std()), 2),
                "Variance": round(float(series.var()), 2),
                "Min": round(float(series.min()), 2),
                "Q1 (25%)": round(float(q1), 2),
                "Q2 (50%)": round(float(q2), 2),
                "Q3 (75%)": round(float(q3), 2),
                "Max": round(float(series.max()), 2),
                "IQR": round(float(iqr), 2),
                "Skewness": round(float(series.skew()), 3),
                "Kurtosis": round(float(series.kurtosis()), 3)
            })

        return pd.DataFrame(summary_records)

    def get_categorical_distribution(self, column: str) -> pd.DataFrame:
        """
        Calculates frequency, percentage share, and cumulative percentage for a categorical column.
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in dataframe.")

        counts = self.df[column].value_counts(dropna=False)
        percentages = (counts / len(self.df)) * 100
        cum_percentages = percentages.cumsum()

        dist_df = pd.DataFrame({
            "Category": counts.index.astype(str),
            "Frequency": counts.values,
            "Percentage (%)": percentages.round(2).values,
            "Cumulative (%)": cum_percentages.round(2).values
        })
        return dist_df

    def get_churn_breakdown_by_category(self, column: str) -> pd.DataFrame:
        """
        Computes bivariate cross-tabulation of Churn across categories of a column,
        including churn count, retained count, and specific churn rate %.
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found.")

        ct = pd.crosstab(self.df[column], self.df["Churn"], margins=False)
        if "Yes" not in ct.columns:
            ct["Yes"] = 0
        if "No" not in ct.columns:
            ct["No"] = 0

        ct["Total"] = ct["Yes"] + ct["No"]
        ct["Churn Rate (%)"] = (ct["Yes"] / ct["Total"] * 100).round(2)
        ct["Retention Rate (%)"] = (ct["No"] / ct["Total"] * 100).round(2)
        ct = ct.rename(columns={"Yes": "Churned Customers", "No": "Retained Customers"})
        ct = ct.reset_index().rename(columns={column: "Segment"})
        ct = ct.sort_values(by="Churn Rate (%)", ascending=False).reset_index(drop=True)
        return ct

    def get_numerical_stats_by_churn(self, num_col: str) -> pd.DataFrame:
        """
        Calculates descriptive statistics for a numerical column grouped by Churn status.
        """
        if num_col not in self.df.columns:
            raise ValueError(f"Column '{num_col}' not found.")

        grouped = self.df.groupby("Churn")[num_col]
        agg_df = grouped.agg(
            Count="count",
            Mean="mean",
            Median="median",
            Std="std",
            Min="min",
            Q1=lambda x: x.quantile(0.25),
            Q3=lambda x: x.quantile(0.75),
            Max="max"
        ).round(2).reset_index()

        agg_df["IQR"] = (agg_df["Q3"] - agg_df["Q1"]).round(2)
        return agg_df

    def perform_chi_square_tests(self) -> pd.DataFrame:
        """
        Runs Pearson's Chi-Square Test of Independence for all categorical variables
        against Churn. Computes Chi2 statistic, p-value, degrees of freedom, and Cramér's V
        effect size to quantify association strength.
        """
        results = []
        n = len(self.df)

        for col in self.cat_cols:
            if col == "Churn" or col not in self.df.columns:
                continue

            contingency = pd.crosstab(self.df[col], self.df["Churn"])
            chi2, p_val, dof, _ = stats.chi2_contingency(contingency)

            # Cramér's V calculation: sqrt(chi2 / (n * min(r-1, k-1)))
            min_dim = min(contingency.shape[0] - 1, contingency.shape[1] - 1)
            cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else 0.0

            significance = "Significant (p < 0.001)" if p_val < 0.001 else (
                "Significant (p < 0.05)" if p_val < 0.05 else "Not Significant"
            )

            # Association strength rating based on Cramér's V
            if cramers_v >= 0.35:
                strength = "Strong Association"
            elif cramers_v >= 0.20:
                strength = "Moderate Association"
            elif cramers_v >= 0.10:
                strength = "Weak Association"
            else:
                strength = "Negligible Association"

            results.append({
                "Feature": col,
                "Chi-Square Stat": round(float(chi2), 2),
                "p-value": f"{p_val:.2e}" if p_val < 0.001 else round(float(p_val), 4),
                "Degrees of Freedom": dof,
                "Cramer's V": round(float(cramers_v), 3),
                "Association Strength": strength,
                "Statistical Significance": significance
            })

        res_df = pd.DataFrame(results)
        return res_df.sort_values(by="Cramer's V", ascending=False).reset_index(drop=True)

    def perform_t_tests_on_numerical(self) -> pd.DataFrame:
        """
        Runs Welch's two-sample t-test (unequal variances) and Mann-Whitney U test
        for numerical metrics between Churned and Retained groups.
        """
        results = []
        churn_yes = self.df[self.df["Churn"] == "Yes"]
        churn_no = self.df[self.df["Churn"] == "No"]

        for col in self.num_cols:
            if col not in self.df.columns:
                continue

            grp_yes = churn_yes[col].dropna()
            grp_no = churn_no[col].dropna()

            t_stat, t_pval = stats.ttest_ind(grp_yes, grp_no, equal_var=False)
            u_stat, u_pval = stats.mannwhitneyu(grp_yes, grp_no, alternative="two-sided")

            # Cohen's d effect size
            n1, n2 = len(grp_yes), len(grp_no)
            s1, s2 = grp_yes.std(), grp_no.std()
            pooled_std = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
            cohens_d = (grp_yes.mean() - grp_no.mean()) / pooled_std if pooled_std != 0 else 0

            results.append({
                "Metric": col,
                "Churned Mean": round(float(grp_yes.mean()), 2),
                "Retained Mean": round(float(grp_no.mean()), 2),
                "Mean Difference": round(float(grp_yes.mean() - grp_no.mean()), 2),
                "Welch t-stat": round(float(t_stat), 2),
                "t-test p-value": f"{t_pval:.2e}" if t_pval < 0.001 else round(float(t_pval), 4),
                "Cohen's d": round(float(cohens_d), 3),
                "Mann-Whitney U p-val": f"{u_pval:.2e}" if u_pval < 0.001 else round(float(u_pval), 4),
                "Conclusion": "Statistically Significant Difference (p < 0.001)" if t_pval < 0.001 else "No Significant Difference"
            })

        return pd.DataFrame(results)


if __name__ == "__main__":
    import os
    from pathlib import Path
    base_dir = Path(__file__).resolve().parent.parent
    clean_path = os.path.join(base_dir, "data", "processed", "telco_churn_cleaned.csv")

    if os.path.exists(clean_path):
        data = pd.read_csv(clean_path)
        stats_engine = DescriptiveStatisticsEngine(data)
        print("=" * 70)
        print("NUMERICAL DESCRIPTIVE STATISTICS:")
        print("=" * 70)
        print(stats_engine.get_numerical_summary().to_string(index=False))

        print("\n" + "=" * 70)
        print("CHI-SQUARE TEST OF INDEPENDENCE (ASSOCIATION WITH CHURN):")
        print("=" * 70)
        print(stats_engine.perform_chi_square_tests().head(8).to_string(index=False))

        print("\n" + "=" * 70)
        print("WELCH'S TWO-SAMPLE T-TESTS (CHURNED VS RETAINED):")
        print("=" * 70)
        print(stats_engine.perform_t_tests_on_numerical().to_string(index=False))
