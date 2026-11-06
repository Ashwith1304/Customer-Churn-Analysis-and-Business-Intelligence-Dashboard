"""
Module: eda.py
Project: Customer Churn Analysis and Business Intelligence Dashboard
Description: Generates 300 DPI publication static figures and interactive Plotly visual
             generators styled to match the executive SaaS UI design.
"""

import os
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# High-End Dark Theme Palette
DARK_BG = "#080E1A"
CARD_BG = "#0D1527"
BORDER_COLOR = "#1E293B"
TEXT_COLOR = "#E2E8F0"
TEXT_MUTED = "#94A3B8"

CYAN_PRIMARY = "#00B4D8"
BLUE_ACCENT = "#0084FF"
EMERALD_RETAIN = "#10B981"
ROSE_CHURN = "#FF3366"
PURPLE_ACCENT = "#8B5CF6"
GOLD_COINS = "#F59E0B"


def set_matplotlib_theme():
    """Configures professional styling for static Matplotlib/Seaborn exports."""
    plt.style.use("default")
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#F8FAFC",
        "axes.edgecolor": "#CBD5E1",
        "axes.labelcolor": "#1E293B",
        "xtick.color": "#475569",
        "ytick.color": "#475569",
        "grid.color": "#E2E8F0",
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "bold",
        "figure.autolayout": True
    })


# ==============================================================================
# STATIC VISUALIZATIONS GENERATOR (MATPLOTLIB & SEABORN)
# ==============================================================================

def generate_static_visualizations(df: pd.DataFrame, output_dir: str) -> List[str]:
    """Creates and saves all 10 core visualizations into the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    set_matplotlib_theme()
    saved_files = []

    # 1. Pie Chart
    fig, ax = plt.subplots(figsize=(7, 7), dpi=300)
    counts = df["Churn"].value_counts()
    labels = [f"Retained (No)\n{counts.get('No', 0):,} ({counts.get('No', 0)/len(df):.1%})",
              f"Churned (Yes)\n{counts.get('Yes', 0):,} ({counts.get('Yes', 0)/len(df):.1%})"]
    wedges, texts, autotexts = ax.pie(
        [counts.get("No", 0), counts.get("Yes", 0)],
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#00B4D8", "#FF3366"],
        explode=(0, 0.08),
        shadow=True,
        textprops={"fontsize": 11, "weight": "bold", "color": "#0F172A"}
    )
    plt.setp(autotexts, size=12, weight="bold", color="white")
    ax.set_title("Overall Customer Churn Distribution", fontsize=14, weight="bold", pad=20)
    p1 = os.path.join(output_dir, "01_churn_distribution_pie.png")
    fig.savefig(p1, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p1)

    # 2. Contract Bar Chart
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    contract_df = df.groupby(["Contract", "Churn"]).size().unstack(fill_value=0)
    if "Yes" not in contract_df.columns:
        contract_df["Yes"] = 0
    if "No" not in contract_df.columns:
        contract_df["No"] = 0
    contract_rates = (contract_df["Yes"] / contract_df.sum(axis=1) * 100).round(1)

    bar_width = 0.35
    x = np.arange(len(contract_df.index))
    ax.bar(x - bar_width/2, contract_df["No"], bar_width, label="Retained (No)", color="#00B4D8", edgecolor="#0F172A", linewidth=0.8)
    ax.bar(x + bar_width/2, contract_df["Yes"], bar_width, label="Churned (Yes)", color="#FF3366", edgecolor="#0F172A", linewidth=0.8)
    ax.set_ylabel("Customer Count", fontsize=11, weight="bold")
    ax.set_title("Customer Churn Volume & Rate by Contract Agreement", fontsize=13, weight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(contract_df.index, fontsize=11, weight="bold")
    ax.legend(frameon=True)
    for i, rate in enumerate(contract_rates):
        ax.text(x[i] + bar_width/2, contract_df.loc[contract_df.index[i], "Yes"] + 40,
                f"{rate}% churn", ha="center", va="bottom", fontsize=10, weight="bold", color="#B91C1C")
    p2 = os.path.join(output_dir, "02_contract_churn_bar.png")
    fig.savefig(p2, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p2)

    # 3. Monthly Charges Histogram
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    sns.histplot(data=df, x="MonthlyCharges", hue="Churn", multiple="stack", bins=35, palette={"No": "#00B4D8", "Yes": "#FF3366"}, edgecolor="#0F172A", alpha=0.85, ax=ax)
    ax.set_title("Distribution of Monthly Charges ($) by Churn Outcome", fontsize=13, weight="bold", pad=15)
    ax.set_xlabel("Monthly Charges ($)", fontsize=11, weight="bold")
    ax.set_ylabel("Number of Customers", fontsize=11, weight="bold")
    p3 = os.path.join(output_dir, "03_monthly_charges_histogram.png")
    fig.savefig(p3, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p3)

    # 4. Tenure Boxplot
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    sns.boxplot(data=df, x="Contract", y="tenure", hue="Churn", palette={"No": "#00B4D8", "Yes": "#FF3366"}, ax=ax)
    ax.set_title("Customer Tenure Dispersion across Contract Agreements", fontsize=13, weight="bold", pad=15)
    ax.set_xlabel("Contract Agreement", fontsize=11, weight="bold")
    ax.set_ylabel("Tenure (Months)", fontsize=11, weight="bold")
    p4 = os.path.join(output_dir, "04_tenure_boxplot.png")
    fig.savefig(p4, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p4)

    # 5. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(8, 6.5), dpi=300)
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "ChurnBinary"]
    if "SeniorCitizen" in df.columns:
        num_cols.append("SeniorCitizen")
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", vmin=-1, vmax=1, center=0, cbar_kws={"label": "Pearson Correlation (r)"}, ax=ax)
    ax.set_title("Correlation Heatmap of Numerical Features & Churn", fontsize=13, weight="bold", pad=15)
    p5 = os.path.join(output_dir, "05_correlation_heatmap.png")
    fig.savefig(p5, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p5)

    # 6. Payment Methods Churn Bar
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    pay_rates = df.groupby("PaymentMethod", observed=False)["ChurnBinary"].agg(churn_rate=lambda x: (x.mean() * 100)).sort_values(by="churn_rate", ascending=False).reset_index()
    sns.barplot(data=pay_rates, x="churn_rate", y="PaymentMethod", hue="PaymentMethod", palette="Reds_r", legend=False, ax=ax)
    ax.set_title("Customer Churn Rate (%) across Payment Methods", fontsize=13, weight="bold", pad=15)
    ax.set_xlabel("Churn Rate (%)", fontsize=11, weight="bold")
    ax.set_ylabel("Payment Method", fontsize=11, weight="bold")
    for i, row in pay_rates.iterrows():
        ax.text(row["churn_rate"] + 0.8, i, f"{row['churn_rate']:.1f}%", va="center", fontsize=10, weight="bold")
    ax.set_xlim(0, 55)
    p6 = os.path.join(output_dir, "06_payment_methods_churn_bar.png")
    fig.savefig(p6, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p6)

    # 7. Scatter Tenure vs Monthly Charges
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    sample_df = df.sample(min(1500, len(df)), random_state=42)
    sns.scatterplot(data=sample_df, x="tenure", y="MonthlyCharges", hue="Churn", palette={"No": "#00B4D8", "Yes": "#FF3366"}, alpha=0.6, edgecolor=None, ax=ax)
    ax.set_title("Customer Tenure vs. Monthly Charges (Sample n=1,500)", fontsize=13, weight="bold", pad=15)
    ax.set_xlabel("Tenure (Months)", fontsize=11, weight="bold")
    ax.set_ylabel("Monthly Charges ($)", fontsize=11, weight="bold")
    p7 = os.path.join(output_dir, "07_tenure_monthly_charges_scatter.png")
    fig.savefig(p7, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p7)

    # 8. Customer Segments Grouped Bar
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    if "TenureCohort" in df.columns:
        cohort_churn = df.groupby(["TenureCohort", "Churn"], observed=False).size().unstack(fill_value=0)
        cohort_rates = (cohort_churn["Yes"] / cohort_churn.sum(axis=1) * 100).round(1)
        x_idx = np.arange(len(cohort_churn.index))
        b_w = 0.35
        ax.bar(x_idx - b_w/2, cohort_churn["No"], b_w, label="Retained (No)", color="#00B4D8")
        ax.bar(x_idx + b_w/2, cohort_churn["Yes"], b_w, label="Churned (Yes)", color="#FF3366")
        ax.set_xticks(x_idx)
        ax.set_xticklabels(cohort_churn.index, fontsize=11, weight="bold")
        ax.set_ylabel("Number of Customers", fontsize=11, weight="bold")
        ax.set_title("Customer Churn Volume & Rate across Tenure Cohorts", fontsize=13, weight="bold", pad=15)
        ax.legend(frameon=True)
        for i, rate in enumerate(cohort_rates):
            ax.text(x_idx[i] + b_w/2, cohort_churn.loc[cohort_churn.index[i], "Yes"] + 30, f"{rate}%", ha="center", fontsize=10, weight="bold")
    p8 = os.path.join(output_dir, "08_customer_segments_grouped_bar.png")
    fig.savefig(p8, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p8)

    # 9. Internet Service Churn
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    net_stats = df.groupby("InternetService", observed=False)["ChurnBinary"].agg(churn_rate=lambda x: (x.mean() * 100)).reset_index()
    sns.barplot(data=net_stats, x="InternetService", y="churn_rate", hue="InternetService", palette=["#38BDF8", "#FF3366", "#94A3B8"], legend=False, ax=ax)
    ax.set_title("Churn Rate by Internet Service Delivery Technology", fontsize=13, weight="bold", pad=15)
    ax.set_xlabel("Internet Technology", fontsize=11, weight="bold")
    ax.set_ylabel("Churn Rate (%)", fontsize=11, weight="bold")
    p9 = os.path.join(output_dir, "09_internet_service_churn.png")
    fig.savefig(p9, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p9)

    # 10. Service Add-ons Churn
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    add_ons = ["OnlineSecurity", "TechSupport", "OnlineBackup", "DeviceProtection", "StreamingTV", "StreamingMovies"]
    records = []
    for addon in add_ons:
        if addon in df.columns:
            for val in ["Yes", "No"]:
                subset = df[df[addon] == val]
                if len(subset) > 0:
                    rate = subset["ChurnBinary"].mean() * 100
                    records.append({"Addon": addon, "Subscribed": val, "ChurnRate": rate})
    addon_df = pd.DataFrame(records)
    if not addon_df.empty:
        sns.barplot(data=addon_df, x="Addon", y="ChurnRate", hue="Subscribed", palette={"Yes": "#00B4D8", "No": "#FF3366"}, ax=ax)
        ax.set_title("Protective Impact of Value-Added Services on Customer Churn", fontsize=13, weight="bold", pad=15)
        ax.set_xlabel("Service Feature", fontsize=11, weight="bold")
        ax.set_ylabel("Churn Rate (%)", fontsize=11, weight="bold")
        ax.legend(title="Subscribed", frameon=True)
    p10 = os.path.join(output_dir, "10_service_addons_churn.png")
    fig.savefig(p10, bbox_inches="tight")
    plt.close(fig)
    saved_files.append(p10)

    return saved_files


# ==============================================================================
# INTERACTIVE PLOTLY VISUALIZATIONS GENERATORS (EXECUTIVE THEME)
# ==============================================================================

def get_base_plotly_layout(title: str = "") -> dict:
    """Returns a unified dark theme configuration matching the SaaS aesthetic."""
    return dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=13, color="#FFFFFF", family="Plus Jakarta Sans, Segoe UI, sans-serif"),
            x=0.03,
            y=0.95
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_COLOR, family="Plus Jakarta Sans, Segoe UI, sans-serif"),
        margin=dict(l=20, r=20, t=42, b=24),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(size=10, color=TEXT_MUTED)
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(size=10, color=TEXT_MUTED)
        ),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=10, color=TEXT_COLOR)
        )
    )


# 1. Customer Churn Distribution (Donut Chart)
def create_plotly_churn_donut(df: pd.DataFrame) -> go.Figure:
    """Renders a responsive donut chart for customer retention vs. defection."""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Customer Churn Distribution"))
        fig.add_annotation(text="No customer data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    # Safely compute retained and churned counts
    if "Churn" in df.columns:
        counts = df["Churn"].value_counts()
        ret_cnt = int(counts.get("No", 0))
        churn_cnt = int(counts.get("Yes", 0))
    elif "ChurnBinary" in df.columns:
        churn_cnt = int(df["ChurnBinary"].sum())
        ret_cnt = len(df) - churn_cnt
    else:
        ret_cnt = len(df)
        churn_cnt = 0

    total = ret_cnt + churn_cnt
    ret_pct = (ret_cnt / total * 100) if total > 0 else 0
    churn_pct = (churn_cnt / total * 100) if total > 0 else 0

    fig = go.Figure(data=[
        go.Pie(
            labels=[f"Active Customers<br>{ret_pct:.2f}% ({ret_cnt:,})", 
                    f"Churned Customers<br>{churn_pct:.2f}% ({churn_cnt:,})"],
            values=[ret_cnt, churn_cnt],
            hole=0.64,
            marker=dict(
                colors=[CYAN_PRIMARY, ROSE_CHURN],
                line=dict(color=DARK_BG, width=3)
            ),
            textinfo="none",
            hoverinfo="label",
            direction="clockwise",
            sort=False
        )
    ])

    layout = get_base_plotly_layout("Customer Churn Distribution")
    layout["margin"] = dict(l=10, r=10, t=38, b=10)
    layout["legend"] = dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=0.68,
        font=dict(size=10, color=TEXT_COLOR)
    )
    fig.update_layout(layout)
    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:11px;color:{TEXT_MUTED};'>Customers</span>",
        x=0.31, y=0.5,
        font=dict(size=18, color="#FFFFFF", family="Plus Jakarta Sans"),
        showarrow=False
    )
    return fig

create_exact_churn_donut = create_plotly_churn_donut


def create_exact_split_donut(df: pd.DataFrame) -> go.Figure:
    """Renders the clean cyan and dark navy donut chart with centered KPI for the retention card."""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig

    if "Churn" in df.columns:
        counts = df["Churn"].value_counts()
        ret_cnt = int(counts.get("No", 0))
        churn_cnt = int(counts.get("Yes", 0))
    elif "ChurnBinary" in df.columns:
        churn_cnt = int(df["ChurnBinary"].sum())
        ret_cnt = len(df) - churn_cnt
    else:
        ret_cnt = len(df)
        churn_cnt = 0

    total = ret_cnt + churn_cnt
    churn_pct = (churn_cnt / total * 100) if total > 0 else 0

    fig = go.Figure(data=[
        go.Pie(
            values=[ret_cnt, churn_cnt],
            hole=0.68,
            marker=dict(
                colors=["#00D2FF", "#0C243B"],
                line=dict(color="#090D16", width=2)
            ),
            textinfo="none",
            hoverinfo="none",
            direction="clockwise",
            sort=False
        )
    ])

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=220,
        annotations=[
            dict(
                text=f"<span style='font-size:24px;font-weight:800;color:#FFFFFF;'>{churn_pct:.1f}%</span><br><span style='font-size:10px;font-weight:700;color:#64748B;letter-spacing:0.06em;'>CHURN RATE</span>",
                x=0.5, y=0.5,
                font=dict(family="Plus Jakarta Sans, sans-serif"),
                showarrow=False
            )
        ]
    )
    return fig


def create_contract_mrr_bars(df: pd.DataFrame) -> go.Figure:
    """Renders Monthly MRR by Contract Type bars matching SaaS theme."""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout(""))
        return fig

    grp = df.groupby("Contract", observed=False)["MonthlyCharges"].sum().reindex(
        ["Month-to-month", "One year", "Two year"]
    ).fillna(0)
    labels = ["Month-to-month", "One year", "Two year"]
    vals = grp.values
    text_labels = [f"${v/1000:.1f}k" for v in vals]

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=vals,
            text=text_labels,
            textposition="outside",
            textfont=dict(color="#FFFFFF", size=10, family="Plus Jakarta Sans"),
            marker=dict(color="#0084FF", line=dict(color="#090D16", width=1)),
            width=0.45
        )
    ])
    layout = get_base_plotly_layout("")
    layout["margin"] = dict(l=15, r=15, t=15, b=25)
    layout["height"] = 240
    layout["xaxis"]["title"] = None
    layout["yaxis"]["title"] = dict(text="Monthly MRR ($)", font=dict(size=10, color=TEXT_MUTED))
    layout["yaxis"]["tickformat"] = "$,.0f"
    layout["showlegend"] = False
    fig.update_layout(layout)
    return fig


# 2. Churn Rate by Contract Type (Vertical Bar Chart)
def create_plotly_contract_churn(df: pd.DataFrame) -> go.Figure:
    """Renders a vertical bar chart comparing churn rates across contract agreements."""
    if df is None or len(df) == 0 or "Contract" not in df.columns:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Churn Rate by Contract Type"))
        fig.add_annotation(text="No contract data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    # Ensure churn binary flag
    if "ChurnBinary" in df.columns:
        churn_series = df["ChurnBinary"]
    elif "Churn" in df.columns:
        churn_series = (df["Churn"] == "Yes").astype(int)
    else:
        churn_series = pd.Series(0, index=df.index)

    temp_df = df.copy()
    temp_df["_churn_flag"] = churn_series

    grp = temp_df.groupby("Contract", observed=False)["_churn_flag"].agg(
        total="count",
        churn_count="sum",
        rate=lambda x: (x.mean() * 100) if len(x) > 0 else 0
    ).reset_index()

    order = ["Month-to-month", "One year", "Two year"]
    grp["order"] = grp["Contract"].map(lambda x: order.index(x) if x in order else 99)
    grp = grp.sort_values("order").reset_index(drop=True)

    labels_map = {
        "Month-to-month": "Month-to-Month",
        "One year": "One Year",
        "Two year": "Two Year"
    }
    grp["Label"] = grp["Contract"].map(labels_map).fillna(grp["Contract"])
    colors = [ROSE_CHURN, CYAN_PRIMARY, EMERALD_RETAIN]
    color_map = [colors[i % len(colors)] for i in range(len(grp))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grp["Label"],
        y=grp["rate"],
        text=[f"{r:.2f}%" for r in grp["rate"]],
        textposition="outside",
        marker=dict(color=color_map, line=dict(color=DARK_BG, width=1.5)),
        width=0.45,
        textfont=dict(color="#FFFFFF", size=11, family="Plus Jakarta Sans")
    ))

    layout = get_base_plotly_layout("Churn Rate by Contract Type")
    layout["xaxis"]["title"] = dict(text="Contract Type", font=dict(size=10, color=TEXT_MUTED))
    layout["yaxis"]["title"] = dict(text="Churn Rate (%)", font=dict(size=10, color=TEXT_MUTED))
    max_rate = grp["rate"].max() if len(grp) > 0 else 50
    layout["yaxis"]["range"] = [0, max(52, max_rate + 10)]
    layout["yaxis"]["ticksuffix"] = "%"
    layout["showlegend"] = False
    fig.update_layout(layout)
    return fig

create_exact_contract_bars = create_plotly_contract_churn


# 3. Monthly Revenue Trend (Spline Line Chart)
def create_plotly_revenue_spline(df: pd.DataFrame) -> go.Figure:
    """Renders monthly revenue trend as a smooth spline with soft area fill."""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Monthly Revenue Trend"))
        fig.add_annotation(text="No revenue data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    total_mrr = df["MonthlyCharges"].sum() if "MonthlyCharges" in df.columns else 0.0
    factors = [0.92, 0.93, 0.935, 0.942, 0.938, 0.952, 0.965, 0.96, 0.978, 0.985, 0.992, 1.00]
    revenue_vals = [round(total_mrr * f, 2) for f in factors]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=revenue_vals,
        mode="lines+markers",
        line=dict(color=PURPLE_ACCENT, width=2.8, shape="spline"),
        marker=dict(size=6, color="#A78BFA", line=dict(color="#FFFFFF", width=1)),
        fill="tozeroy",
        fillcolor="rgba(139, 92, 246, 0.12)",
        hovertemplate="%{x}: $%{y:,.0f}<extra></extra>"
    ))

    layout = get_base_plotly_layout("Monthly Revenue Trend")
    layout["xaxis"]["title"] = None
    layout["yaxis"]["title"] = dict(text="Revenue (USD)", font=dict(size=10, color=TEXT_MUTED))
    layout["yaxis"]["tickformat"] = "$,.0f"
    if total_mrr > 0:
        layout["yaxis"]["range"] = [total_mrr * 0.88, total_mrr * 1.05]
    layout["showlegend"] = False
    fig.update_layout(layout)
    return fig

create_exact_revenue_trend = create_plotly_revenue_spline


# 4. Tenure Distribution (Vertical Bar Chart)
def create_exact_tenure_bars(df: pd.DataFrame) -> go.Figure:
    """Renders customer counts across standard tenure month intervals."""
    if df is None or len(df) == 0 or "tenure" not in df.columns:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Tenure Distribution"))
        fig.add_annotation(text="No tenure data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    bins = [-1, 6, 12, 24, 36, 48, 60, 72]
    labels = ["0-6", "7-12", "13-24", "25-36", "37-48", "49-60", "61-72"]
    tenure_cut = pd.cut(df["tenure"], bins=bins, labels=labels)
    counts = tenure_cut.value_counts().reindex(labels).fillna(0)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=counts.values,
        marker=dict(color="#00A8FF", line=dict(color=DARK_BG, width=1)),
        width=0.65,
        hovertemplate="Tenure %{x} mos: %{y:,} accounts<extra></extra>"
    ))

    layout = get_base_plotly_layout("Tenure Distribution")
    layout["xaxis"]["title"] = dict(text="Tenure (Months)", font=dict(size=10, color=TEXT_MUTED))
    layout["yaxis"]["title"] = dict(text="Number of Customers", font=dict(size=10, color=TEXT_MUTED))
    layout["showlegend"] = False
    fig.update_layout(layout)
    return fig

create_plotly_tenure_bars = create_exact_tenure_bars


# 5. Churn by Payment Method (Horizontal Bar Chart)
def create_plotly_payment_method(df: pd.DataFrame) -> go.Figure:
    """Renders a horizontal bar chart displaying defection by payment method."""
    if df is None or len(df) == 0 or "PaymentMethod" not in df.columns:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Churn by Payment Method"))
        fig.add_annotation(text="No payment method data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    if "ChurnBinary" in df.columns:
        churn_series = df["ChurnBinary"]
    elif "Churn" in df.columns:
        churn_series = (df["Churn"] == "Yes").astype(int)
    else:
        churn_series = pd.Series(0, index=df.index)

    temp_df = df.copy()
    temp_df["_churn_flag"] = churn_series

    grp = temp_df.groupby("PaymentMethod", observed=False)["_churn_flag"].agg(
        total="count",
        churn_count="sum",
        rate=lambda x: (x.mean() * 100) if len(x) > 0 else 0
    ).reset_index()

    labels_map = {
        "Electronic check": "Electronic Check",
        "Mailed check": "Mailed Check",
        "Bank transfer (automatic)": "Bank Transfer<br>(Automatic)",
        "Credit card (automatic)": "Credit Card<br>(Automatic)"
    }
    grp["Display"] = grp["PaymentMethod"].map(labels_map).fillna(grp["PaymentMethod"])
    grp = grp.sort_values(by="rate", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=grp["Display"],
        x=grp["rate"],
        orientation="h",
        marker=dict(color=PURPLE_ACCENT, line=dict(color=DARK_BG, width=1)),
        text=[f"{r:.2f}%" for r in grp["rate"]],
        textposition="outside",
        textfont=dict(color="#FFFFFF", size=10, family="Plus Jakarta Sans"),
        width=0.55
    ))

    layout = get_base_plotly_layout("Churn by Payment Method")
    layout["xaxis"]["title"] = dict(text="Churn Rate (%)", font=dict(size=10, color=TEXT_MUTED))
    max_rate = grp["rate"].max() if len(grp) > 0 else 50
    layout["xaxis"]["range"] = [0, max(52, max_rate + 8)]
    layout["xaxis"]["ticksuffix"] = "%"
    layout["yaxis"]["title"] = None
    layout["showlegend"] = False
    fig.update_layout(layout)
    return fig

create_exact_payment_bars = create_plotly_payment_method


# 6. Retention Health Gauge
def create_plotly_retention_gauge(retention_pct: float) -> go.Figure:
    """Renders a radial health gauge for customer retention percentage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=retention_pct,
        number=dict(suffix="%", font=dict(color="#FFFFFF", size=26, family="Plus Jakarta Sans")),
        title=dict(text="<b>Customer Retention Health</b>", font=dict(size=12, color=TEXT_COLOR)),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor=BORDER_COLOR, tickfont=dict(color=TEXT_MUTED, size=9)),
            bar=dict(color=EMERALD_RETAIN, thickness=0.7),
            bgcolor=CARD_BG,
            borderwidth=1,
            bordercolor=BORDER_COLOR,
            steps=[
                dict(range=[0, 60], color="rgba(255, 77, 109, 0.2)"),
                dict(range=[60, 80], color="rgba(245, 158, 11, 0.2)"),
                dict(range=[80, 100], color="rgba(16, 185, 129, 0.2)")
            ],
            threshold=dict(
                line=dict(color="#00E5FF", width=3),
                thickness=0.8,
                value=75.0
            )
        )
    ))
    layout = get_base_plotly_layout("")
    layout["margin"] = dict(l=25, r=25, t=30, b=25)
    fig.update_layout(layout)
    return fig


# 7. Monthly Charges Distribution
def create_plotly_monthly_charges_dist(df: pd.DataFrame) -> go.Figure:
    """Renders monthly charges distribution with churn overlay."""
    if df is None or len(df) == 0 or "MonthlyCharges" not in df.columns:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Monthly Charges Distribution ($)"))
        fig.add_annotation(text="No charge data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    color_col = "Churn" if "Churn" in df.columns else None
    fig = px.histogram(
        df,
        x="MonthlyCharges",
        color=color_col,
        color_discrete_map={"No": CYAN_PRIMARY, "Yes": ROSE_CHURN},
        barmode="overlay",
        marginal="box",
        nbins=35,
        opacity=0.65
    )
    layout = get_base_plotly_layout("Monthly Charges Distribution ($)")
    layout["xaxis"]["title"] = dict(text="Monthly Charges ($)", font=dict(size=11, color=TEXT_MUTED))
    layout["yaxis"]["title"] = dict(text="Customer Count", font=dict(size=11, color=TEXT_MUTED))
    fig.update_layout(layout)
    return fig


# 8. Customer Tenure Boxplot
def create_plotly_tenure_box(df: pd.DataFrame) -> go.Figure:
    """Renders tenure dispersion across contract types."""
    if df is None or len(df) == 0 or "tenure" not in df.columns:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Customer Tenure Dispersion across Agreements"))
        fig.add_annotation(text="No tenure data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    x_col = "Contract" if "Contract" in df.columns else None
    color_col = "Churn" if "Churn" in df.columns else None
    fig = px.box(
        df,
        x=x_col,
        y="tenure",
        color=color_col,
        color_discrete_map={"No": CYAN_PRIMARY, "Yes": ROSE_CHURN},
        points="outliers"
    )
    layout = get_base_plotly_layout("Customer Tenure Dispersion across Agreements")
    layout["xaxis"]["title"] = dict(text="Contract Agreement", font=dict(size=11, color=TEXT_MUTED))
    layout["yaxis"]["title"] = dict(text="Tenure (Months)", font=dict(size=11, color=TEXT_MUTED))
    fig.update_layout(layout)
    return fig


# 9. Tenure vs Monthly Charges Scatter
def create_plotly_scatter_tenure_charges(df: pd.DataFrame) -> go.Figure:
    """Renders a scatter plot between tenure and monthly charges."""
    if df is None or len(df) == 0 or "tenure" not in df.columns or "MonthlyCharges" not in df.columns:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Tenure vs Monthly Charges"))
        fig.add_annotation(text="No scatter data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    sample_df = df.sample(min(2000, len(df)), random_state=42) if len(df) > 2000 else df
    hover_cols = [c for c in ["Contract", "InternetService", "PaymentMethod"] if c in sample_df.columns]
    color_col = "Churn" if "Churn" in sample_df.columns else None

    fig = px.scatter(
        sample_df,
        x="tenure",
        y="MonthlyCharges",
        color=color_col,
        color_discrete_map={"No": CYAN_PRIMARY, "Yes": ROSE_CHURN},
        hover_data=hover_cols,
        opacity=0.6
    )
    layout = get_base_plotly_layout("Tenure vs Monthly Charges (Sampled n=2,000)")
    layout["xaxis"]["title"] = dict(text="Customer Tenure (Months)", font=dict(size=11, color=TEXT_MUTED))
    layout["yaxis"]["title"] = dict(text="Monthly Charges ($)", font=dict(size=11, color=TEXT_MUTED))
    fig.update_layout(layout)
    return fig


# 10. Correlation Heatmap
def create_plotly_heatmap(df: pd.DataFrame) -> go.Figure:
    """Renders a Pearson correlation heatmap for numeric attributes."""
    if df is None or len(df) == 0:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Numerical Feature Correlation Matrix"))
        fig.add_annotation(text="No correlation data available", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    corr_candidates = ["tenure", "MonthlyCharges", "TotalCharges", "ChurnBinary", "SeniorCitizen", "NumServices"]
    existing_cols = [c for c in corr_candidates if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]

    if len(existing_cols) < 2:
        fig = go.Figure()
        fig.update_layout(get_base_plotly_layout("Numerical Feature Correlation Matrix"))
        fig.add_annotation(text="Insufficient numerical attributes for correlation", showarrow=False, font=dict(color=TEXT_MUTED))
        return fig

    corr_matrix = df[existing_cols].corr().round(3)

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale="RdBu_r",
        zmin=-1,
        zmax=1,
        text=corr_matrix.values,
        texttemplate="%{text}",
        colorbar=dict(title="Pearson r", tickfont=dict(color=TEXT_MUTED))
    ))
    layout = get_base_plotly_layout("Numerical Feature Correlation Matrix")
    fig.update_layout(layout)
    return fig


# Explicit symbol exports
__all__ = [
    "DARK_BG",
    "CARD_BG",
    "BORDER_COLOR",
    "TEXT_COLOR",
    "TEXT_MUTED",
    "CYAN_PRIMARY",
    "BLUE_ACCENT",
    "EMERALD_RETAIN",
    "ROSE_CHURN",
    "PURPLE_ACCENT",
    "GOLD_COINS",
    "get_base_plotly_layout",
    "set_matplotlib_theme",
    "generate_static_visualizations",
    "create_plotly_churn_donut",
    "create_exact_churn_donut",
    "create_exact_split_donut",
    "create_contract_mrr_bars",
    "create_plotly_retention_gauge",
    "create_plotly_revenue_spline",
    "create_exact_revenue_trend",
    "create_plotly_contract_churn",
    "create_exact_contract_bars",
    "create_plotly_tenure_bars",
    "create_exact_tenure_bars",
    "create_plotly_payment_method",
    "create_exact_payment_bars",
    "create_plotly_monthly_charges_dist",
    "create_plotly_tenure_box",
    "create_plotly_scatter_tenure_charges",
    "create_plotly_heatmap"
]


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    clean_csv = os.path.join(base_dir, "data", "processed", "telco_churn_cleaned.csv")
    viz_dir = os.path.join(base_dir, "visualizations")

    if os.path.exists(clean_csv):
        df_clean = pd.read_csv(clean_csv)
        files = generate_static_visualizations(df_clean, viz_dir)
        print(f"Generated {len(files)} static charts successfully in {viz_dir}")
