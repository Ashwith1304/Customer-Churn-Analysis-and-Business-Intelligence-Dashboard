"""
Customer Churn Analysis and Business Intelligence Dashboard
A Data Analytics and Business Intelligence Project
Institution: Sreenidhi Institute of Science and Technology (Autonomous)
Department of Data Science (CSE-DS)
Team Members:
  - G Mythili (24311A67H8)
  - K Ashiwith (24311A67H6)
  - D Niyati (24311A67H7)
"""

import os
import sys
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Setup import path
current_dir = Path(__file__).resolve().parent
if (current_dir / "src").exists():
    parent_dir = current_dir
else:
    parent_dir = current_dir.parent

if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.data_cleaning import TelcoDataCleaner
from src.descriptive_statistics import DescriptiveStatisticsEngine
from src.sql_analysis import TelcoSQLAnalyzer
from src.eda import (
    create_exact_churn_donut,
    create_exact_contract_bars,
    create_exact_revenue_trend,
    create_exact_tenure_bars,
    create_exact_payment_bars,
    create_plotly_churn_donut,
    create_plotly_retention_gauge,
    create_plotly_revenue_spline,
    create_plotly_contract_churn,
    create_plotly_monthly_charges_dist,
    create_plotly_tenure_box,
    create_plotly_payment_method,
    create_plotly_scatter_tenure_charges,
    create_plotly_heatmap,
    TEXT_COLOR,
    TEXT_MUTED,
    CYAN_PRIMARY,
    BLUE_ACCENT,
    ROSE_CHURN,
    EMERALD_RETAIN
)

# ==============================================================================
# STREAMLIT CONFIGURATION & CUSTOM DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="Customer Churn Analysis and BI Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_UI_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #E2E8F0;
    }

    /* Deep Navy Dark Theme */
    .stApp {
        background-color: #080E1A;
        background-image: 
            radial-gradient(at 20% 15%, rgba(0, 132, 255, 0.08) 0px, transparent 55%),
            radial-gradient(at 80% 85%, rgba(139, 92, 246, 0.06) 0px, transparent 55%);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1540px;
    }

    /* Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #080E1A !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.4rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }

    /* Sidebar Brand Box */
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 18px;
        margin-bottom: 16px;
        border-bottom: 1px solid #1E293B;
    }
    .brand-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0084FF, #00C6FF);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0, 132, 255, 0.35);
    }
    .brand-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
        letter-spacing: -0.01em;
    }
    .brand-sub {
        font-size: 0.72rem;
        color: #38BDF8;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* Hide Streamlit Radio Dots */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: transparent;
        padding: 9px 12px;
        border-radius: 9px;
        margin: 0;
        cursor: pointer;
        transition: all 0.18s ease-in-out;
        display: flex;
        align-items: center;
        border: 1px solid transparent;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(30, 41, 59, 0.5);
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label p {
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        color: #94A3B8 !important;
        margin: 0 !important;
        white-space: nowrap;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover p {
        color: #F8FAFC !important;
    }
    /* Active Glowing Blue Navigation Pill */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: #0084FF !important;
        box-shadow: 0 4px 14px rgba(0, 132, 255, 0.45) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Sidebar Footer Artwork */
    .sidebar-footer-artwork {
        margin-top: 24px;
        padding: 16px 12px;
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(13, 21, 39, 0.8) 0%, rgba(8, 14, 26, 0.95) 100%);
        border: 1px solid #1E293B;
        text-align: center;
    }

    /* Top Bar Header */
    .top-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
        padding-bottom: 12px;
        border-bottom: 1px solid #1E293B;
    }
    .top-header-titles h1 {
        font-size: 1.55rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.2;
    }
    .top-header-titles p {
        font-size: 0.82rem;
        color: #94A3B8;
        margin: 3px 0 0 0;
        font-weight: 500;
    }
    .dataset-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #1E293B;
        color: #CBD5E1;
        font-size: 0.76rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
    }

    /* Horizontal Filter Bar */
    .filter-bar-wrapper {
        background: #0D1527;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 18px;
    }
    .filter-label-col {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.90rem;
        font-weight: 700;
        color: #FFFFFF;
        padding-top: 28px;
    }

    /* 6 KPI Cards Grid */
    .kpi-grid-saas {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 12px;
        margin-bottom: 18px;
    }
    .kpi-card {
        background: #0D1527;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px 14px 14px 14px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #334155;
    }
    .kpi-icon-bubble {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
    }
    .kpi-card-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94A3B8;
        letter-spacing: 0.01em;
        margin-bottom: 4px;
    }
    .kpi-card-value {
        font-size: 1.48rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    /* Card Containers */
    .card-panel {
        background: #0D1527;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .card-panel-header {
        font-size: 0.94rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Key Insights Card (Executive 6th Tile) */
    .insights-card-box {
        background: #0D1527;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 18px 20px;
        height: 370px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .insights-title-row {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.98rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 18px;
    }
    .insights-body-list {
        display: flex;
        flex-direction: column;
        gap: 13px;
    }
    .insight-bullet-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 0.83rem;
        line-height: 1.45;
        color: #CBD5E1;
    }
    .insight-check {
        color: #10B981;
        font-weight: 800;
        font-size: 0.95rem;
        line-height: 1.2;
    }

    /* Project Team Cards */
    .team-grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-top: 14px;
        margin-bottom: 24px;
    }
    .team-member-card {
        background: #0D1527;
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 24px 20px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .team-member-card:hover {
        transform: translateY(-3px);
        border-color: #0084FF;
    }
    .team-avatar-circle {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0084FF, #38BDF8);
        color: #FFFFFF;
        font-size: 1.15rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
        box-shadow: 0 4px 14px rgba(0, 132, 255, 0.35);
    }
    .team-member-name {
        font-size: 1.10rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .team-member-roll {
        display: inline-block;
        background: rgba(0, 132, 255, 0.12);
        border: 1px solid rgba(0, 132, 255, 0.3);
        color: #38BDF8;
        font-size: 0.80rem;
        font-weight: 700;
        padding: 3px 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        letter-spacing: 0.04em;
    }
    .team-dept-info {
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.35;
    }

    /* Streamlit Widget Styling */
    .stSelectbox label {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #121A2D !important;
        border-color: #1E293B !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        color: #FFFFFF !important;
    }
    .stButton > button {
        background-color: #0084FF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        padding: 6px 14px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #0070D8 !important;
        box-shadow: 0 4px 12px rgba(0, 132, 255, 0.4) !important;
    }
</style>
"""

st.markdown(CUSTOM_UI_CSS, unsafe_allow_html=True)


# ==============================================================================
# DATA ACCESS & CACHING PIPELINE
# ==============================================================================
@st.cache_data(show_spinner=False)
def get_dataset(custom_file=None):
    """Loads, caches, and returns both raw and processed datasets cleanly."""
    raw_path = parent_dir / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    proc_path = parent_dir / "data" / "processed" / "telco_churn_cleaned.csv"

    if custom_file is not None:
        raw_df = pd.read_csv(custom_file)
        cleaner = TelcoDataCleaner()
        cleaner.audit_report["initial_shape"] = raw_df.shape
        cleaner.audit_report["initial_columns"] = raw_df.columns.tolist()
        df_nodup, _ = cleaner.check_duplicates(raw_df)
        df_typed = cleaner.handle_data_types_and_missing(df_nodup)
        cleaner.detect_outliers_iqr(df_typed)
        df_final = cleaner.enrich_features(df_typed)
        return raw_df, df_final, cleaner.audit_report

    if proc_path.exists():
        proc_df = pd.read_csv(proc_path)
        raw_df = pd.read_csv(raw_path) if raw_path.exists() else proc_df
        cleaner = TelcoDataCleaner()
        cleaner.audit_report["initial_shape"] = raw_df.shape
        cleaner.audit_report["duplicates_found"] = 0
        cleaner.audit_report["blank_total_charges_count"] = 11
        cleaner.detect_outliers_iqr(proc_df)
        return raw_df, proc_df, cleaner.audit_report

    if raw_path.exists():
        cleaner = TelcoDataCleaner(str(raw_path))
        df_final, audit = cleaner.clean_pipeline(output_filepath=str(proc_path))
        raw_df = pd.read_csv(raw_path)
        return raw_df, df_final, audit

    return None, None, None


# Ensure SQLite database is connected
db_file = parent_dir / "database" / "customer_churn.db"
if not db_file.exists():
    sql_analyzer = TelcoSQLAnalyzer(str(db_file))
    sql_analyzer.init_database(str(parent_dir / "data" / "processed" / "telco_churn_cleaned.csv"))


# ==============================================================================
# SIDEBAR: BRAND, NAVIGATION & VISUAL ARTWORK
# ==============================================================================
# Brand Header (Exact match to target design)
st.sidebar.markdown("""
<div class="sidebar-brand-box">
    <div class="brand-avatar">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
    </div>
    <div>
        <div class="brand-title">Customer Churn</div>
        <div class="brand-sub">Business Intelligence</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation Menu (All 9 pages strictly matching specification)
PAGE_OPTIONS = [
    "🏠  Executive Overview",
    "📁  Customer Data Explorer",
    "🛡️  Data Quality Report",
    "📊  Exploratory Data Analysis",
    "📈  Statistical Insights",
    "💾  SQL Analytics",
    "👥  Customer Segmentation",
    "💡  Business Recommendations",
    "ℹ️  Project Information"
]

selected_page = st.sidebar.radio(
    "Navigation Menu",
    PAGE_OPTIONS,
    index=0,
    label_visibility="collapsed"
)

# Sidebar Bottom Visual Artwork (Matching Image 2 illuminated 3D artwork)
st.sidebar.markdown("""
<div class="sidebar-footer-artwork">
    <svg width="180" height="95" viewBox="0 0 200 100" fill="none">
        <defs>
            <linearGradient id="glowGrad" x1="0%" y1="100%" x2="0%" y2="0%">
                <stop offset="0%" stop-color="#0084FF" stop-opacity="0.1"/>
                <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.9"/>
            </linearGradient>
            <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#00E5FF"/>
                <stop offset="100%" stop-color="#0084FF"/>
            </linearGradient>
        </defs>
        <!-- Curved bottom wave -->
        <path d="M10 85 C 50 65, 150 95, 190 75" stroke="#1E3A8A" stroke-width="2.5" fill="none"/>
        <path d="M15 88 C 60 70, 140 98, 185 78" stroke="#0084FF" stroke-width="1.2" opacity="0.6" fill="none"/>
        <!-- 3D Bar Columns -->
        <rect x="55" y="62" width="14" height="26" rx="2" fill="url(#barGrad)"/>
        <rect x="75" y="48" width="14" height="40" rx="2" fill="url(#barGrad)"/>
        <rect x="95" y="32" width="14" height="56" rx="2" fill="url(#barGrad)"/>
        <rect x="115" y="44" width="14" height="44" rx="2" fill="url(#barGrad)"/>
        <rect x="135" y="58" width="14" height="30" rx="2" fill="url(#barGrad)"/>
        <!-- Floating circular avatar badge -->
        <circle cx="102" cy="22" r="14" fill="#0D1527" stroke="#0084FF" stroke-width="1.8"/>
        <path d="M96 28 C96 25, 108 25, 108 28" stroke="#38BDF8" stroke-width="1.5" stroke-linecap="round"/>
        <circle cx="102" cy="20" r="3.5" fill="#38BDF8"/>
    </svg>
    <div style="font-size:0.70rem;color:#64748B;font-weight:600;margin-top:4px;">
        CSE-DS • Sreenidhi Institute
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# TOP BAR: HEADER, DATA UPLOAD/DOWNLOAD & HORIZONTAL FILTER BAR
# ==============================================================================
# Quick Top Data Action Expander
with st.expander("📂 **Data Management (Upload Custom CSV / Download Dataset)**", expanded=False):
    col_up1, col_up2 = st.columns([1.2, 0.8])
    with col_up1:
        uploaded_custom = st.file_uploader(
            "Upload Custom Telco CSV File (Full analytics update automatically)",
            type=["csv"],
            help="Upload any alternative Telco Customer Churn CSV dataset."
        )
    with col_up2:
        raw_csv_path = parent_dir / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
        if raw_csv_path.exists():
            with open(raw_csv_path, "rb") as f:
                r_bytes = f.read()
            st.download_button(
                label="📥 Download Kaggle CSV Dataset",
                data=r_bytes,
                file_name="WA_Fn-UseC_-Telco-Customer-Churn.csv",
                mime="text/csv",
                use_container_width=True
            )
        st.markdown(
            """<a href="https://www.kaggle.com/datasets/blastchar/telco-customer-churn" target="_blank" style="text-decoration:none;">
            <div style="background:#121A2D;border:1px solid #1E293B;border-radius:8px;padding:6px;text-align:center;font-size:0.75rem;color:#38BDF8;font-weight:600;margin-top:6px;">
            🌐 Kaggle Dataset Source (BlastChar)
            </div></a>""",
            unsafe_allow_html=True
        )

raw_df, full_df, audit_report = get_dataset(uploaded_custom)

if full_df is None:
    st.error("Dataset not detected. Please upload the Telco Customer Churn CSV file above.")
    st.stop()

# Top Header Row (Matching Image 2)
st.markdown("""
<div class="top-header-row">
    <div class="top-header-titles">
        <h1>Customer Churn Analysis and Business Intelligence Dashboard</h1>
        <p>A Data Analytics and Business Intelligence Project</p>
    </div>
    <div class="dataset-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        <span>IBM Telco Customer Churn Dataset</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Horizontal Filter Bar (Clean top bar matching reference design)
st.markdown('<div class="filter-bar-wrapper">', unsafe_allow_html=True)
col_f_title, col_f1, col_f2, col_f3, col_f4, col_f5, col_f_btn = st.columns([0.7, 1.2, 1.3, 1.3, 1.5, 1.2, 1.1])

with col_f_title:
    st.markdown("""
    <div class="filter-label-col">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0084FF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
        </svg>
        <span>Filters</span>
    </div>
    """, unsafe_allow_html=True)

with col_f1:
    sel_gender = st.selectbox("Gender", ["All"] + sorted(full_df["gender"].unique().tolist()), key="f_gender")

with col_f2:
    sel_contract = st.selectbox("Contract Type", ["All"] + sorted(full_df["Contract"].unique().tolist()), key="f_contract")

with col_f3:
    sel_internet = st.selectbox("Internet Service", ["All"] + sorted(full_df["InternetService"].unique().tolist()), key="f_internet")

with col_f4:
    sel_pay = st.selectbox("Payment Method", ["All"] + sorted(full_df["PaymentMethod"].unique().tolist()), key="f_pay")

with col_f5:
    sel_tenure = st.selectbox("Tenure Range", ["All", "0-6 Months", "7-12 Months", "13-24 Months", "25-36 Months", "37-48 Months", "49-60 Months", "61-72 Months"], key="f_tenure")

with col_f_btn:
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.session_state["f_gender"] = "All"
        st.session_state["f_contract"] = "All"
        st.session_state["f_internet"] = "All"
        st.session_state["f_pay"] = "All"
        st.session_state["f_tenure"] = "All"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Apply Filters
filtered_df = full_df.copy()
if sel_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == sel_gender]
if sel_contract != "All":
    filtered_df = filtered_df[filtered_df["Contract"] == sel_contract]
if sel_internet != "All":
    filtered_df = filtered_df[filtered_df["InternetService"] == sel_internet]
if sel_pay != "All":
    filtered_df = filtered_df[filtered_df["PaymentMethod"] == sel_pay]
if sel_tenure != "All":
    tenure_map = {
        "0-6 Months": (0, 6),
        "7-12 Months": (7, 12),
        "13-24 Months": (13, 24),
        "25-36 Months": (25, 36),
        "37-48 Months": (37, 48),
        "49-60 Months": (49, 60),
        "61-72 Months": (61, 72)
    }
    t_min, t_max = tenure_map[sel_tenure]
    filtered_df = filtered_df[(filtered_df["tenure"] >= t_min) & (filtered_df["tenure"] <= t_max)]


# ==============================================================================
# 6 EXECUTIVE KPI CARDS (Matching Image 2)
# ==============================================================================
def render_6_kpi_cards(df: pd.DataFrame):
    """Renders 6 executive KPI cards in 1 row matching Image 2 exactly."""
    total = len(df)
    if total == 0:
        st.warning("No customer records match the selected filter combination. Please reset or broaden your filters.")
        return

    churned = int(df["ChurnBinary"].sum())
    active = total - churned
    rate = (churned / total) * 100
    avg_bill = df["MonthlyCharges"].mean()
    total_mrr = df["MonthlyCharges"].sum()

    kpi_html = f"""
    <div class="kpi-grid-saas">
        <div class="kpi-card">
            <div class="kpi-icon-bubble" style="background:rgba(0, 132, 255, 0.15);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0084FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div class="kpi-card-label">Total Customers</div>
            <div class="kpi-card-value">{total:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-bubble" style="background:rgba(16, 185, 129, 0.15);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div class="kpi-card-label">Active Customers</div>
            <div class="kpi-card-value">{active:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-bubble" style="background:rgba(255, 77, 109, 0.15);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF4D6D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div class="kpi-card-label">Churned Customers</div>
            <div class="kpi-card-value">{churned:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-bubble" style="background:rgba(0, 180, 216, 0.15);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00B4D8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
            </div>
            <div class="kpi-card-label">Churn Rate</div>
            <div class="kpi-card-value">{rate:.2f}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-bubble" style="background:rgba(56, 189, 248, 0.15);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                    <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>
            </div>
            <div class="kpi-card-label">Avg. Monthly Charges</div>
            <div class="kpi-card-value">${avg_bill:.2f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon-bubble" style="background:rgba(245, 158, 11, 0.15);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="9"></circle>
                    <path d="M14.5 9h-4a1.5 1.5 0 0 0 0 3h3a1.5 1.5 0 0 1 0 3h-4"></path>
                    <line x1="12" y1="7" x2="12" y2="9"></line>
                    <line x1="12" y1="15" x2="12" y2="17"></line>
                </svg>
            </div>
            <div class="kpi-card-label">Total Monthly Revenue</div>
            <div class="kpi-card-value">${total_mrr:,.2f}</div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)


render_6_kpi_cards(filtered_df)


# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW (Exact Visual Match to Image 2)
# ==============================================================================
if "Executive Overview" in selected_page:
    # 6 Visual Cards in 2 Rows of 3 Columns
    # Row 1
    col_r1_1, col_r1_2, col_r1_3 = st.columns(3)
    with col_r1_1:
        st.plotly_chart(create_exact_churn_donut(filtered_df), use_container_width=True)
    with col_r1_2:
        st.plotly_chart(create_exact_contract_bars(filtered_df), use_container_width=True)
    with col_r1_3:
        st.plotly_chart(create_exact_revenue_trend(filtered_df), use_container_width=True)

    # Row 2
    col_r2_1, col_r2_2, col_r2_3 = st.columns(3)
    with col_r2_1:
        st.plotly_chart(create_exact_tenure_bars(filtered_df), use_container_width=True)
    with col_r2_2:
        st.plotly_chart(create_exact_payment_bars(filtered_df), use_container_width=True)
    with col_r2_3:
        # Key Insights Card with green checkmarks exactly like Image 2
        st.markdown("""
        <div class="insights-card-box">
            <div class="insights-title-row">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00E5FF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
                </svg>
                <span>Key Insights</span>
            </div>
            <div class="insights-body-list">
                <div class="insight-bullet-item">
                    <span class="insight-check">✓</span>
                    <span>Overall churn rate is <b>26.54%</b> (1,869 out of 7,043 customers).</span>
                </div>
                <div class="insight-bullet-item">
                    <span class="insight-check">✓</span>
                    <span><b>Month-to-month contracts</b> have the highest churn rate (<b>42.71%</b>).</span>
                </div>
                <div class="insight-bullet-item">
                    <span class="insight-check">✓</span>
                    <span><b>Electronic check users</b> are more likely to churn (<b>45.29%</b>).</span>
                </div>
                <div class="insight-bullet-item">
                    <span class="insight-check">✓</span>
                    <span>Customers with <b>longer tenure</b> show significantly lower churn.</span>
                </div>
                <div class="insight-bullet-item">
                    <span class="insight-check">✓</span>
                    <span>Average monthly charge is <b>$64.76</b>, with a total revenue of <b>$456,116.75</b>.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 2: CUSTOMER DATA EXPLORER
# ==============================================================================
elif "Customer Data Explorer" in selected_page:
    tab_explore, tab_dict, tab_export = st.tabs(["Searchable Records", "Feature Data Dictionary", "Download Center"])

    with tab_explore:
        search_kw = st.text_input("🔍 Search by Customer ID, Contract, or Payment Method:", "")
        display_tbl = filtered_df.copy()
        if search_kw:
            mask = display_tbl.astype(str).apply(lambda row: row.str.contains(search_kw, case=False).any(), axis=1)
            display_tbl = display_tbl[mask]

        st.caption(f"Showing **{len(display_tbl):,}** matching customer accounts")
        st.dataframe(display_tbl.head(200), use_container_width=True, height=450)

    with tab_dict:
        dict_records = [
            {"Attribute": "customerID", "Type": "Categorical (ID)", "Description": "Unique alphanumeric customer identifier."},
            {"Attribute": "gender", "Type": "Categorical", "Description": "Customer biological sex ('Male' or 'Female')."},
            {"Attribute": "SeniorCitizen", "Type": "Binary Flag", "Description": "Senior citizen status indicator (1 = Yes, 0 = No)."},
            {"Attribute": "Partner", "Type": "Categorical", "Description": "Whether customer has a domestic partner or spouse."},
            {"Attribute": "Dependents", "Type": "Categorical", "Description": "Whether customer has financial dependents or children."},
            {"Attribute": "tenure", "Type": "Integer (Months)", "Description": "Customer subscription lifetime (0 to 72 months)."},
            {"Attribute": "PhoneService", "Type": "Categorical", "Description": "Fixed landline telephone service subscription."},
            {"Attribute": "MultipleLines", "Type": "Categorical", "Description": "Multiple telephone line subscription status."},
            {"Attribute": "InternetService", "Type": "Categorical", "Description": "Technology delivery: DSL, Fiber optic, or None."},
            {"Attribute": "OnlineSecurity", "Type": "Categorical", "Description": "Cybersecurity firewall protection add-on."},
            {"Attribute": "OnlineBackup", "Type": "Categorical", "Description": "Cloud data backup and recovery subscription."},
            {"Attribute": "DeviceProtection", "Type": "Categorical", "Description": "Hardware equipment replacement warranty."},
            {"Attribute": "TechSupport", "Type": "Categorical", "Description": "Priority IT and technical assistance subscription."},
            {"Attribute": "StreamingTV", "Type": "Categorical", "Description": "Television streaming service package."},
            {"Attribute": "StreamingMovies", "Type": "Categorical", "Description": "Movie streaming subscription package."},
            {"Attribute": "Contract", "Type": "Categorical", "Description": "Agreement term: Month-to-month, One year, Two year."},
            {"Attribute": "PaperlessBilling", "Type": "Categorical", "Description": "Digital statement delivery ('Yes' or 'No')."},
            {"Attribute": "PaymentMethod", "Type": "Categorical", "Description": "Billing method: Electronic check, Mailed check, Bank transfer, Credit card."},
            {"Attribute": "MonthlyCharges", "Type": "Continuous ($)", "Description": "Monthly bill amount billed to account."},
            {"Attribute": "TotalCharges", "Type": "Continuous ($)", "Description": "Cumulative charges billed over tenure lifetime."},
            {"Attribute": "Churn", "Type": "Target Flag", "Description": "Customer defection indicator ('Yes' or 'No')."},
            {"Attribute": "ChurnBinary", "Type": "Engineered Flag", "Description": "Numeric indicator (1 = Churned, 0 = Retained)."},
            {"Attribute": "TenureCohort", "Type": "Engineered Segment", "Description": "Lifecycle: 0-12m (New), 13-24m, 25-48m, 49-72m (Loyal)."},
            {"Attribute": "MonthlyChargesTier", "Type": "Engineered Segment", "Description": "Spend tier: Low (<$35), Medium ($35-$70), High (>$70)."},
            {"Attribute": "NumServices", "Type": "Engineered Count", "Description": "Count of subscribed value-added products (0 to 8)."}
        ]
        st.dataframe(pd.DataFrame(dict_records), use_container_width=True, height=450)

    with tab_export:
        c_ex1, c_ex2 = st.columns(2)
        with c_ex1:
            st.markdown("#### **Download Filtered & Enriched Dataset**")
            st.caption("Exports currently filtered records with all 28 enriched dimensions.")
            csv_exp = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv_exp,
                file_name="telco_churn_filtered_export.csv",
                mime="text/csv",
                use_container_width=True
            )
        with c_ex2:
            st.markdown("#### **Original Raw Kaggle Dataset**")
            st.caption("Direct copy of the 7,043 record Kaggle Telco dataset.")
            raw_csv_path = parent_dir / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
            if raw_csv_path.exists():
                with open(raw_csv_path, "rb") as f:
                    r_bytes = f.read()
                st.download_button(
                    label="📥 Download Kaggle CSV",
                    data=r_bytes,
                    file_name="WA_Fn-UseC_-Telco-Customer-Churn.csv",
                    mime="text/csv",
                    use_container_width=True
                )


# ==============================================================================
# PAGE 3: DATA QUALITY REPORT
# ==============================================================================
elif "Data Quality Report" in selected_page:
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    with col_q1:
        st.metric("Total Raw Accounts", f"{raw_df.shape[0]:,}")
    with col_q2:
        st.metric("Duplicate Rows Found", f"{audit_report.get('duplicates_found', 0)}")
    with col_q3:
        st.metric("Blank TotalCharges Fixed", f"{audit_report.get('blank_total_charges_count', 11)} accounts")
    with col_q4:
        st.metric("Final Feature Dimensions", f"{full_df.shape[1]} columns")

    st.markdown("<hr style='border-color:#1E293B;margin:16px 0;'>", unsafe_allow_html=True)

    c_audit1, c_audit2 = st.columns(2)
    with c_audit1:
        st.markdown("### 🔬 **Data Quality Remediation Actions**")
        st.markdown("""
        1. **Duplicate Verification:** Checked all 7,043 rows across all 21 raw columns. Exactly 0 duplicates detected.
        2. **Whitespace Type-Casting (`TotalCharges`):**
           - Raw data had 11 whitespace strings (`" "`) which forced Pandas to infer an `object` data type.
           - Every single one of these 11 cases corresponds to a new customer with `tenure == 0` (no billing cycle has elapsed).
           - Converted column to `float64` and imputed `$0.0` for new accounts, preserving 100% of customer accounts.
        3. **Categorical Normalization:** Stripped whitespace and mapped `SeniorCitizen` integer flag to `SeniorCitizenLabel`.
        4. **Feature Engineering:** Added `ChurnBinary`, `TenureCohort`, `MonthlyChargesTier`, and `NumServices`.
        """)
    with c_audit2:
        st.markdown("### 📦 **Outlier Diagnostics (1.5 × IQR Rule)**")
        outliers = audit_report.get("outlier_analysis", {})
        out_table = []
        for k, v in outliers.items():
            out_table.append({
                "Attribute": k,
                "Q1 (25%)": v["Q1"],
                "Q3 (75%)": v["Q3"],
                "IQR": v["IQR"],
                "Lower Bound": v["lower_bound"],
                "Upper Bound": v["upper_bound"],
                "Outlier Count": v["outlier_count"],
                "Outlier %": f"{v['outlier_percentage']}%"
            })
        st.dataframe(pd.DataFrame(out_table), use_container_width=True)
        st.info("💡 **Diagnostic Finding:** Zero statistical outliers exist under standard 1.5×IQR boundary rules. Numerical ranges accurately reflect genuine customer subscription lifecycles.")


# ==============================================================================
# PAGE 4: EXPLORATORY DATA ANALYSIS
# ==============================================================================
elif "Exploratory Data Analysis" in selected_page:
    tab_u, tab_b, tab_m = st.tabs(["Univariate Distributions", "Bivariate Churn Drivers", "Multivariate Interactions"])

    with tab_u:
        feat = st.selectbox("Select Attribute to Inspect:", ["tenure", "MonthlyCharges", "TotalCharges", "Contract", "InternetService", "PaymentMethod", "gender", "SeniorCitizenLabel"], index=0)
        c1, c2 = st.columns(2)
        if feat in ["tenure", "MonthlyCharges", "TotalCharges"]:
            with c1:
                st.plotly_chart(create_plotly_monthly_charges_dist(filtered_df) if feat=="MonthlyCharges" else px.histogram(filtered_df, x=feat, nbins=35, marginal="box", color_discrete_sequence=[CYAN_PRIMARY], title=f"<b>Distribution of {feat}</b>").update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)), use_container_width=True)
            with c2:
                s = filtered_df[feat]
                stats_df = pd.DataFrame({
                    "Statistic": ["Mean", "Median", "Mode", "Std Dev", "Min", "25%", "50%", "75%", "Max", "Skewness"],
                    "Value": [round(s.mean(), 2), round(s.median(), 2), round(s.mode().iloc[0], 2), round(s.std(), 2), round(s.min(), 2), round(s.quantile(0.25), 2), round(s.quantile(0.50), 2), round(s.quantile(0.75), 2), round(s.max(), 2), round(s.skew(), 3)]
                })
                st.dataframe(stats_df, use_container_width=True, height=350)
        else:
            with c1:
                cnt = filtered_df[feat].value_counts().reset_index()
                cnt.columns = [feat, "Count"]
                fig_c = px.bar(cnt, x=feat, y="Count", text="Count", color=feat, color_discrete_sequence=px.colors.qualitative.Prism, title=f"<b>Frequency Distribution: {feat}</b>")
                fig_c.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR), showlegend=False)
                st.plotly_chart(fig_c, use_container_width=True)
            with c2:
                engine = DescriptiveStatisticsEngine(filtered_df)
                st.dataframe(engine.get_categorical_distribution(feat), use_container_width=True)

    with tab_b:
        b_feat = st.selectbox("Select Attribute vs Churn:", ["Contract", "InternetService", "PaymentMethod", "gender", "SeniorCitizenLabel", "TechSupport", "OnlineSecurity"], index=0)
        c1, c2 = st.columns(2)
        engine = DescriptiveStatisticsEngine(filtered_df)
        b_df = engine.get_churn_breakdown_by_category(b_feat)
        with c1:
            st.dataframe(b_df, use_container_width=True)
        with c2:
            fig_b = px.bar(b_df, x="Segment", y="Churn Rate (%)", text="Churn Rate (%)", color="Churn Rate (%)", color_continuous_scale="Reds", title=f"<b>Churn Rate by {b_feat}</b>")
            fig_b.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_b, use_container_width=True)

        st.markdown("<hr style='border-color:#1E293B;margin:16px 0;'>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.plotly_chart(create_plotly_scatter_tenure_charges(filtered_df), use_container_width=True)
        with c4:
            st.plotly_chart(create_plotly_tenure_box(filtered_df), use_container_width=True)

    with tab_m:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(create_plotly_heatmap(filtered_df), use_container_width=True)
        with c2:
            pivot_c = filtered_df.pivot_table(index="Contract", columns="PaymentMethod", values="ChurnBinary", aggfunc=lambda x: round(np.mean(x) * 100, 1))
            fig_p = px.imshow(pivot_c, text_auto=True, color_continuous_scale="Reds", title="<b>Churn Rate (%) by Contract & Payment Method</b>")
            fig_p.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_p, use_container_width=True)


# ==============================================================================
# PAGE 5: STATISTICAL INSIGHTS
# ==============================================================================
elif "Statistical Insights" in selected_page:
    engine = DescriptiveStatisticsEngine(filtered_df)
    tab_s1, tab_s2, tab_s3 = st.tabs(["Summary Statistics", "Chi-Square Independence Tests", "Welch's Two-Sample T-Tests"])

    with tab_s1:
        st.markdown("### 📊 **Numerical Summary Statistics**")
        st.dataframe(engine.get_numerical_summary(), use_container_width=True)

        st.markdown("### 📋 **Metrics by Customer Churn Status**")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### **Tenure (Months) by Churn Status**")
            st.dataframe(engine.get_numerical_stats_by_churn("tenure"), use_container_width=True)
        with c2:
            st.markdown("##### **Monthly Charges ($) by Churn Status**")
            st.dataframe(engine.get_numerical_stats_by_churn("MonthlyCharges"), use_container_width=True)

    with tab_s2:
        st.markdown(r"### 🧪 **Chi-Square ($\chi^2$) Test of Independence & Cramér's V**")
        st.caption("Quantifies categorical attribute association strength with customer churn.")
        chi_df = engine.perform_chi_square_tests()
        st.dataframe(chi_df, use_container_width=True)

        fig_chi = px.bar(chi_df, x="Feature", y="Cramer's V", text="Cramer's V", color="Cramer's V", color_continuous_scale="Blues", title="<b>Feature Association Strength with Customer Churn (Cramér's V)</b>")
        fig_chi.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_chi, use_container_width=True)

    with tab_s3:
        st.markdown("### 🔬 **Welch's Two-Sample Independent T-Tests**")
        st.caption("Evaluates whether mean differences between Churned and Retained accounts are statistically significant.")
        t_df = engine.perform_t_tests_on_numerical()
        st.dataframe(t_df, use_container_width=True)

        st.markdown("""
        <div class="card-panel">
            <b style="color:#38BDF8;">Plain-Language Business Statistical Interpretation:</b>
            <ul style="margin-top:8px;font-size:0.86rem;color:#CBD5E1;">
                <li><b>Association vs. Causation:</b> Statistical tests show strong <i>association</i> (e.g. Month-to-month contracts have Cramér's V = 0.410, p < 10^-250), meaning contract structure is a massive indicator of defection risk. However, it does not mean contract length inherently causes defection; rather, it reflects low switching barriers.</li>
                <li><b>Tenure Disparity:</b> Churned customers defect after an average of 17.98 months (median 10 months) vs 37.57 months for retained accounts (p < 10^-200, large effect size). Defection is heavily front-loaded in the first 12 months.</li>
                <li><b>Price Sensitivity:</b> Churned accounts were billed $13.18 more per month ($74.44 vs $61.27, p < 10^-70), confirming that higher recurring bills elevate customer elasticity.</li>
                <li><b>Gender Neutrality:</b> Gender has no statistical association with churn (p = 0.487). Retention strategies should focus entirely on pricing, billing channels, and contractual agreements.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 6: SQL ANALYTICS
# ==============================================================================
elif "SQL Analytics" in selected_page:
    analyzer = TelcoSQLAnalyzer(str(db_file))
    questions = analyzer.get_10_business_questions()

    tab_q, tab_custom = st.tabs(["🏢 10 Core Business Questions", "⚡ Interactive SQL Sandbox"])

    with tab_q:
        q_titles = [f"Q{q['id']}: {q['title']}" for q in questions]
        sel_idx = st.selectbox("Select Business Question:", range(len(q_titles)), format_func=lambda i: q_titles[i])
        item = questions[sel_idx]

        st.markdown(f"### **{item['title']}**")
        st.caption(f"**Business Question:** {item['question']}")

        c1, c2 = st.columns([1.1, 0.9])
        with c1:
            st.markdown("##### **Executed SQL Query:**")
            st.code(item["query"], language="sql")
            res_df = analyzer.execute_query(item["query"])
            st.markdown("##### **Query Result Table:**")
            st.dataframe(res_df, use_container_width=True)

        with c2:
            st.markdown("##### **Business Interpretation:**")
            st.info(f"💡 {item['insight']}")

            if len(res_df) > 1 and len(res_df.columns) >= 2:
                n_col = res_df.select_dtypes(include=[np.number]).columns[-1]
                c_col = res_df.columns[0]
                fig_q = px.bar(res_df, x=c_col, y=n_col, text=n_col, color=n_col, color_continuous_scale="Teal", title=f"<b>{item['title']} Visual Breakdown</b>")
                fig_q.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
                st.plotly_chart(fig_q, use_container_width=True)

    with tab_custom:
        st.markdown("### 💻 **Interactive SQL Query Console**")
        st.caption("Execute custom live queries against the `customers` SQLite database table:")
        default_q = "SELECT Contract, PaymentMethod, COUNT(*) AS customer_count, ROUND(AVG(MonthlyCharges), 2) AS avg_charge\nFROM customers\nGROUP BY Contract, PaymentMethod\nORDER BY customer_count DESC\nLIMIT 10;"
        query_text = st.text_area("Write SQL:", value=default_q, height=120)

        if st.button("🚀 Run SQL Query", use_container_width=True):
            if any(w in query_text.upper() for w in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]):
                st.error("Read-only access: Only SELECT queries are permitted.")
            else:
                try:
                    q_res = analyzer.execute_query(query_text)
                    st.success(f"Query returned {len(q_res):,} rows successfully!")
                    st.dataframe(q_res, use_container_width=True)
                except Exception as ex:
                    st.error(f"SQL Execution Error: {str(ex)}")


# ==============================================================================
# PAGE 7: CUSTOMER SEGMENTATION
# ==============================================================================
elif "Customer Segmentation" in selected_page:
    tab_c1, tab_c2, tab_c3 = st.tabs(["Lifecycle Tenure Cohorts", "2D Vulnerability Grid", "High-Risk Account Explorer"])

    with tab_c1:
        c1, c2 = st.columns(2)
        with c1:
            seg_df = filtered_df.groupby("TenureCohort", observed=False)["ChurnBinary"].agg(
                Total="count",
                Churned="sum",
                ChurnRate=lambda x: round(x.mean() * 100, 2)
            ).reset_index()
            seg_df["TotalMRR"] = filtered_df.groupby("TenureCohort", observed=False)["MonthlyCharges"].sum().values.round(2)
            seg_df.columns = ["Lifecycle Cohort", "Total Accounts", "Churned Accounts", "Churn Rate (%)", "Total MRR ($)"]
            st.dataframe(seg_df, use_container_width=True)
        with c2:
            fig_seg = px.bar(seg_df, x="Lifecycle Cohort", y="Churn Rate (%)", text="Churn Rate (%)", color="Churn Rate (%)", color_continuous_scale="Reds", title="<b>Churn Rate by Customer Lifecycle Stage</b>")
            fig_seg.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_seg, use_container_width=True)

    with tab_c2:
        st.markdown("### 🗺️ **Tenure Cohort vs. Monthly Spend Matrix**")
        grid = filtered_df.pivot_table(index="TenureCohort", columns="MonthlyChargesTier", values="ChurnBinary", aggfunc=lambda x: round(np.mean(x) * 100, 1), observed=False)
        fig_g = px.imshow(grid, text_auto=True, color_continuous_scale="Reds", title="<b>Defection Rate (%) by Cohort & Spend Tier</b>")
        fig_g.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_g, use_container_width=True)
        st.warning("⚠️ **Highest Risk Cell:** New Customers (0-12m) paying High Monthly Charges (>$70) exhibit over **60% churn**, presenting the primary revenue loss danger.")

    with tab_c3:
        st.markdown("### 🔍 **Critical Defection Danger Zone Accounts**")
        st.caption("Accounts matching: **Month-to-month + Fiber Optic + Electronic Check**")
        danger = filtered_df[(filtered_df["Contract"] == "Month-to-month") & (filtered_df["InternetService"] == "Fiber optic") & (filtered_df["PaymentMethod"] == "Electronic check")]
        d1, d2, d3 = st.columns(3)
        with d1:
            st.metric("Danger Accounts", f"{len(danger):,}")
        with d2:
            d_rate = (danger["ChurnBinary"].sum() / len(danger) * 100) if len(danger) > 0 else 0
            st.metric("Danger Churn Rate", f"{d_rate:.1f}%")
        with d3:
            st.metric("Monthly Revenue at Risk", f"${danger['MonthlyCharges'].sum():,.2f}")
        st.dataframe(danger[["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn", "NumServices", "TechSupport"]].head(50), use_container_width=True)


# ==============================================================================
# PAGE 8: BUSINESS RECOMMENDATIONS
# ==============================================================================
elif "Business Recommendations" in selected_page:
    tab_rec, tab_calc = st.tabs(["Strategic Retention Pillars", "Customer Retention ROI Calculator"])

    with tab_rec:
        st.markdown("""
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px;">
            <div class="card-panel">
                <div class="card-panel-header" style="color:#38BDF8;">1. Annual Contract Term Transition</div>
                <div style="font-size:0.86rem;line-height:1.6;color:#CBD5E1;">
                    <b style="color:#FFFFFF;">Observed Finding:</b> Month-to-month contracts experience catastrophic 42.71% churn vs 11.27% for 1-year and 2.83% for 2-year.<br>
                    <b style="color:#FFFFFF;">Supporting Statistic:</b> Month-to-month accounts generate 88.55% of all defection (1,655 out of 1,869 churned accounts).<br>
                    <b style="color:#FFFFFF;">Business Impact:</b> Uncommitted customers create high revenue volatility and churn costs.<br>
                    <b style="color:#FFFFFF;">Suggested Action:</b> Offer a $10/month statement credit or line speed upgrade at Month 3 in exchange for an annual contract commitment.
                </div>
            </div>
            <div class="card-panel">
                <div class="card-panel-header" style="color:#38BDF8;">2. Auto-Pay Billing Optimization</div>
                <div style="font-size:0.86rem;line-height:1.6;color:#CBD5E1;">
                    <b style="color:#FFFFFF;">Observed Finding:</b> Electronic check users churn at 45.29%, nearly 3x higher than automated credit cards (15.24%) and bank transfers (16.71%).<br>
                    <b style="color:#FFFFFF;">Supporting Statistic:</b> Over 57.3% of all churned accounts (1,071 customers) use Electronic Check.<br>
                    <b style="color:#FFFFFF;">Business Impact:</b> Manual billing prompts monthly conscious scrutiny of the bill and elevated payment friction.<br>
                    <b style="color:#FFFFFF;">Suggested Action:</b> Introduce a $5/month recurring bill discount for enrolling in Credit Card or Bank Auto-Pay.
                </div>
            </div>
            <div class="card-panel">
                <div class="card-panel-header" style="color:#38BDF8;">3. The First 90 Days Care Journey</div>
                <div style="font-size:0.86rem;line-height:1.6;color:#CBD5E1;">
                    <b style="color:#FFFFFF;">Observed Finding:</b> Over 55.5% of all defection occurs in the first 12 months; churned customers defect at an average of 17.98 months (median 10 months).<br>
                    <b style="color:#FFFFFF;">Supporting Statistic:</b> 0-12m cohort churns at 47.44%, while 49-72m cohort churns at only 9.38%.<br>
                    <b style="color:#FFFFFF;">Business Impact:</b> Acquisition spend is squandered before customer accounts reach profitability.<br>
                    <b style="color:#FFFFFF;">Suggested Action:</b> Implement an onboarding sequence: Day 7 connection check, Day 30 bill review, and Day 60 speed optimization check.
                </div>
            </div>
            <div class="card-panel">
                <div class="card-panel-header" style="color:#38BDF8;">4. Fiber Optic Support Bundling</div>
                <div style="font-size:0.86rem;line-height:1.6;color:#CBD5E1;">
                    <b style="color:#FFFFFF;">Observed Finding:</b> Fiber Optic churns at 41.89% ($91.50/mo bill), but churn plummets to 11.84% when accounts include both Tech Support and Online Security.<br>
                    <b style="color:#FFFFFF;">Supporting Statistic:</b> Accounts with Tech Support churn at 15.17% vs 41.64% for accounts without support.<br>
                    <b style="color:#FFFFFF;">Business Impact:</b> Protects high-ARPU subscriptions from defecting due to unresolved technical friction.<br>
                    <b style="color:#FFFFFF;">Suggested Action:</b> Bundle complimentary Tech Support and Online Security directly into all high-speed Fiber Optic tiers.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_calc:
        st.markdown("### 🧮 **Customer Retention Financial ROI Calculator**")
        st.caption("Model the financial payoff of reducing customer churn across the monitored customer base:")

        target_pt = st.slider("Target Churn Reduction (Percentage Points):", min_value=0.5, max_value=10.0, value=3.0, step=0.5)

        base_t = len(full_df)
        base_c = int(full_df["ChurnBinary"].sum())
        base_r = (base_c / base_t) * 100
        new_r = max(0.0, base_r - target_pt)

        saved_accts = int(round(base_t * (target_pt / 100)))
        avg_churn_bill = full_df[full_df["Churn"] == "Yes"]["MonthlyCharges"].mean()

        m_saved = saved_accts * avg_churn_bill
        y_saved = m_saved * 12

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("Accounts Saved", f"{saved_accts:,}")
        with r2:
            st.metric("New Churn Rate", f"{new_r:.2f}%", f"-{target_pt:.1f}%")
        with r3:
            st.metric("Monthly Revenue Preserved", f"${m_saved:,.2f}")
        with r4:
            st.metric("Annual Revenue Protected", f"${y_saved:,.2f}")

        # Projections Line Chart
        steps = np.linspace(1, 10, 10)
        proj_y = [int(round(base_t * (p / 100))) * avg_churn_bill * 12 for p in steps]
        proj_df = pd.DataFrame({"Churn Reduction": [f"{p:.1f}%" for p in steps], "Annual Revenue Protected ($)": proj_y})
        fig_roi = px.line(proj_df, x="Churn Reduction", y="Annual Revenue Protected ($)", markers=True, color_discrete_sequence=[EMERALD_RETAIN], title="<b>Projected Annual Revenue Protected by Churn Reduction Rate</b>")
        fig_roi.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR))
        st.plotly_chart(fig_roi, use_container_width=True)


# ==============================================================================
# PAGE 9: PROJECT INFORMATION & TEAM MEMBERS
# ==============================================================================
elif "Project Information" in selected_page:
    st.markdown("### 🎓 **Project Team Members**")
    st.caption("Undergraduate Summer Industry Internship Project • Department of Data Science (CSE-DS)")

    # 3 Individual Cards for Team Members matching prompt specifications
    st.markdown("""
    <div class="team-grid-container">
        <div class="team-member-card">
            <div class="team-avatar-circle">GM</div>
            <div class="team-member-name">G Mythili</div>
            <div class="team-member-roll">Roll No: 24311A67H8</div>
            <div class="team-dept-info">
                <b>B.Tech CSE - Data Science</b><br>
                Sreenidhi Institute of Science & Technology
            </div>
        </div>
        <div class="team-member-card">
            <div class="team-avatar-circle">KA</div>
            <div class="team-member-name">K Ashiwith</div>
            <div class="team-member-roll">Roll No: 24311A67H6</div>
            <div class="team-dept-info">
                <b>B.Tech CSE - Data Science</b><br>
                Sreenidhi Institute of Science & Technology
            </div>
        </div>
        <div class="team-member-card">
            <div class="team-avatar-circle">DN</div>
            <div class="team-member-name">D Niyati</div>
            <div class="team-member-roll">Roll No: 24311A67H7</div>
            <div class="team-dept-info">
                <b>B.Tech CSE - Data Science</b><br>
                Sreenidhi Institute of Science & Technology
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Download Academic Internship PDF Report
    pdf_report_path = parent_dir / "reports" / "Summer_Internship_Report_Customer_Churn.pdf"
    if pdf_report_path.exists():
        with open(pdf_report_path, "rb") as f_pdf:
            pdf_bytes = f_pdf.read()
        st.download_button(
            label="📄 Download Institutional Academic Internship PDF Report (28 Pages)",
            data=pdf_bytes,
            file_name="Summer_Internship_Report_Customer_Churn.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown("<hr style='border-color:#1E293B;margin:20px 0;'>", unsafe_allow_html=True)

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("""
        #### **Project Summary & Scope**
        - **Project Title:** Customer Churn Analysis and Business Intelligence Dashboard
        - **Institution:** Sreenidhi Institute of Science and Technology (Autonomous), Hyderabad
        - **Department:** Department of Data Science (CSE-DS)
        - **Academic Period:** III Year I Semester — November 2026
        - **Project Coordinator:** Mr. P. V. K. Sandeep
        - **Head of Department:** Dr. Md. Jaffar Sadiq
        - **Dataset:** IBM Telco Customer Churn (7,043 Customer Records, 28 Analytical Attributes)
        
        #### **Technology Architecture**
        - **Language & Runtime:** Python 3.14 (Windows 64-bit)
        - **Data Processing:** Pandas, NumPy, SciPy (`scipy.stats`)
        - **Data Visualizations:** Plotly Express & Graph Objects, Matplotlib, Seaborn
        - **Relational Storage:** SQLite (`database/customer_churn.db`) with B-tree indexing
        - **Web Application Framework:** Streamlit Enterprise BI Architecture
        """)
    with col_info2:
        st.markdown("""
        #### **Module Breakdown**
        - `src/data_cleaning.py`: Type casting, whitespace resolution, duplicate audit, and IQR outlier boundaries.
        - `src/descriptive_statistics.py`: Parametric stats, Chi-Square independence tests, and Welch's two-sample t-tests.
        - `src/eda.py`: Publication-ready 300 DPI static figures and responsive Plotly visual generators.
        - `src/sql_analysis.py`: Relational database manager and 10 executive business SQL queries.
        - `src/generate_pdf_report.py`: Institutional academic internship PDF generator matching college format.
        - `app/streamlit_app.py`: Commercial-grade 9-page interactive analytics platform.
        - `reports/business_insights.md`: Full executive report and retention ROI projections.
        
        #### **Kaggle Dataset Source**
        - Available publicly on Kaggle: [IBM Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
        """)
