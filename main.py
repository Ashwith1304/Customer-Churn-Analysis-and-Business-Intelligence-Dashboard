"""
Customer Churn Analysis & Business Intelligence Dashboard
Enterprise Retention Analytics
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
    create_exact_split_donut,
    create_contract_mrr_bars,
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
    page_title="Customer Churn Analysis & Business Intelligence Dashboard",
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

    /* Deep Slate Navy Background matching Enterprise Dashboard */
    .stApp {
        background-color: #090D16 !important;
        background-image: 
            radial-gradient(at 15% 10%, rgba(0, 132, 255, 0.08) 0px, transparent 50%),
            radial-gradient(at 85% 90%, rgba(14, 165, 233, 0.05) 0px, transparent 50%) !important;
    }

    /* Transparent Streamlit Header */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Top clearance so Streamlit Cloud fixed top bar never overlaps dashboard content */
    .block-container {
        padding-top: 5.2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 1560px !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 5.8rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }

    /* Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B111E !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 3.2rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }

    /* Sidebar Brand Box */
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 12px;
        margin-bottom: 12px;
    }
    .brand-avatar-box {
        width: 38px;
        height: 38px;
        border-radius: 9px;
        background: linear-gradient(135deg, rgba(0, 132, 255, 0.25), rgba(0, 210, 255, 0.12));
        border: 1px solid rgba(0, 210, 255, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 16px rgba(0, 210, 255, 0.22);
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
        color: #64748B;
        font-weight: 500;
        margin-top: 2px;
    }

    /* Live Status Pill */
    .sidebar-status-pill {
        background: #111927;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 7px 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 18px;
    }
    .status-live {
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #FFFFFF;
    }
    .pulse-dot {
        width: 7px;
        height: 7px;
        background: #0084FF;
        border-radius: 50%;
        box-shadow: 0 0 8px #0084FF;
    }
    .status-count {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748B;
    }

    /* Sidebar Section Header */
    .sidebar-section-header {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 10px;
        padding-left: 4px;
    }

    /* Hide Streamlit Radio Dots & Indicators completely */
    div[data-testid="stRadio"] input[type="radio"],
    div[data-testid="stRadio"] input + div,
    div[data-testid="stRadio"] label > div:first-of-type,
    div[data-testid="stRadio"] [data-baseweb="radio"] input + div,
    div[data-testid="stRadio"] [data-baseweb="radio"] label > div:first-of-type,
    [data-baseweb="radio"] input + div,
    [data-baseweb="radio"] > div:first-of-type,
    [data-baseweb="radio"] label > div:first-of-type,
    div[data-testid="stRadio"] [data-testid="stRadioButton"],
    div[data-testid="stRadio"] label svg,
    div[data-testid="stRadio"] label [aria-hidden="true"],
    div[data-testid="stRadio"] label span[class*="Radio"],
    div[data-testid="stRadio"] label div[class*="Radio"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0 !important;
        border: none !important;
        pointer-events: none !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label,
    div[data-testid="stRadio"] [data-baseweb="radio"] {
        background: transparent;
        padding: 9px 12px;
        border-radius: 8px;
        margin: 0;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
        display: flex;
        align-items: center;
        border: 1px solid transparent;
        width: 100%;
        box-sizing: border-box;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    div[data-testid="stRadio"] [data-baseweb="radio"]:hover {
        background: rgba(30, 41, 59, 0.45);
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    div[data-testid="stRadio"] [data-baseweb="radio"] p,
    div[data-testid="stRadio"] [data-baseweb="radio"] span {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #94A3B8 !important;
        margin: 0 !important;
        white-space: nowrap;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover p,
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover span,
    div[data-testid="stRadio"] [data-baseweb="radio"]:hover p,
    div[data-testid="stRadio"] [data-baseweb="radio"]:hover span {
        color: #F8FAFC !important;
    }

    /* Active Selected Nav Item (Blue Pill matching Image) */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked),
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] div[role="radiogroup"] > label[aria-checked="true"],
    div[data-testid="stRadio"] label:has(input:checked),
    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked),
    div[data-testid="stRadio"] [data-checked="true"] {
        background: #0084FF !important;
        box-shadow: 0 4px 14px rgba(0, 132, 255, 0.35) !important;
        border-radius: 9px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p,
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) span,
    div[data-testid="stRadio"] label:has(input:checked) p,
    div[data-testid="stRadio"] label:has(input:checked) span,
    div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) p,
    div[data-testid="stRadio"] [data-baseweb="radio"]:has(input:checked) span,
    div[data-testid="stRadio"] [data-checked="true"] p,
    div[data-testid="stRadio"] [data-checked="true"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Sidebar Footer */
    .sidebar-team-footer {
        margin-top: 28px;
        padding-top: 14px;
        border-top: 1px solid #1E293B;
    }
    .footer-inst {
        font-size: 0.72rem;
        font-weight: 600;
        color: #94A3B8;
    }
    .footer-names {
        font-size: 0.68rem;
        color: #64748B;
        margin-top: 3px;
    }

    /* Top Breadcrumb */
    .top-breadcrumb {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.95rem;
        font-weight: 600;
        padding-top: 4px;
    }
    .bc-parent {
        color: #64748B;
    }
    .bc-active {
        color: #FFFFFF;
        font-weight: 700;
    }

    /* 6 KPI Cards Grid */
    .kpi-row-6 {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 12px;
        margin-top: 14px;
        margin-bottom: 20px;
    }
    @media (max-width: 1100px) {
        .kpi-row-6 { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 600px) {
        .kpi-row-6 { grid-template-columns: repeat(2, 1fr); }
    }
    .kpi-card-v2 {
        background: #111927;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px 16px 14px 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-card-v2:hover {
        transform: translateY(-2px);
        border-color: #334155;
    }
    .kpi-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .kpi-label-v2 {
        font-size: 0.76rem;
        font-weight: 600;
        color: #94A3B8;
    }
    .kpi-badge-icon {
        font-size: 0.88rem;
        font-weight: 800;
        line-height: 1;
    }
    .kpi-val-v2 {
        font-size: 1.55rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 6px;
    }
    .kpi-sub-v2 {
        font-size: 0.72rem;
        color: #64748B;
        font-weight: 500;
    }
    .text-cyan { color: #00D2FF !important; }
    .text-green { color: #10B981 !important; }
    .text-rose { color: #EF4444 !important; }
    .text-blue { color: #38BDF8 !important; }

    /* Card Panels */
    .card-panel {
        background: #111927;
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }

    /* Popover & Action Buttons */
    div[data-testid="stPopover"] > button,
    .stDownloadButton > button {
        background: #111927 !important;
        border: 1px solid #1E293B !important;
        border-radius: 8px !important;
        color: #E2E8F0 !important;
        font-size: 0.80rem !important;
        font-weight: 600 !important;
        padding: 6px 14px !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stPopover"] > button:hover,
    .stDownloadButton > button:hover {
        background: #182234 !important;
        border-color: #334155 !important;
        color: #FFFFFF !important;
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
        background: #111927;
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


# Initialize Session State for Filter Cohorts
if "f_gender" not in st.session_state:
    st.session_state["f_gender"] = "All"
if "f_contract" not in st.session_state:
    st.session_state["f_contract"] = "All"
if "f_internet" not in st.session_state:
    st.session_state["f_internet"] = "All"
if "f_pay" not in st.session_state:
    st.session_state["f_pay"] = "All"
if "f_tenure" not in st.session_state:
    st.session_state["f_tenure"] = "All"
if "custom_csv_upload" not in st.session_state:
    st.session_state["custom_csv_upload"] = None

# Initial Load
raw_df, full_df, audit_report = get_dataset(st.session_state["custom_csv_upload"])
if full_df is None:
    st.error("Dataset not detected. Please verify data files.")
    st.stop()


# ==============================================================================
# SIDEBAR: BRAND, NAVIGATION & VISUAL ARTWORK (Matching Image Exactly)
# ==============================================================================
# Brand Header
st.sidebar.markdown("""
<div class="sidebar-brand-box">
    <div class="brand-avatar-box">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00D2FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
    </div>
    <div>
        <div class="brand-title">Customer Churn BI</div>
        <div class="brand-sub">Enterprise Retention Analytics</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Live Status Pill
st.sidebar.markdown(f"""
<div class="sidebar-status-pill">
    <div class="status-live"><span class="pulse-dot"></span> IBM Telco Live</div>
    <div class="status-count">{len(full_df):,} rows</div>
</div>
""", unsafe_allow_html=True)

# Section Label
st.sidebar.markdown('<div class="sidebar-section-header">ANALYTICS MODULES</div>', unsafe_allow_html=True)

# Navigation Menu Options (Exact match to target image)
PAGE_OPTIONS = [
    "⊞  Executive Overview",
    "👤  Customer Data Explorer",
    "🛡️  Data Quality Report",
    "📊  Exploratory Data Analysis",
    "Σ  Statistical Analysis",
    "💾  SQL Business Analytics",
    "👥  Customer Segmentation",
    "💡  Business Recommendations",
    "ℹ️  About Project"
]

selected_page = st.sidebar.radio(
    "Navigation Menu",
    PAGE_OPTIONS,
    index=0,
    label_visibility="collapsed"
)

# Sidebar Footer
st.sidebar.markdown("""
<div class="sidebar-team-footer">
    <div class="footer-inst">SNIST · CSE Data Science</div>
    <div class="footer-names">G Mythili · K Ashiwith · D Niyati</div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# TOP BAR: BREADCRUMB & CONTROLS (Filters Popover, Upload, Export)
# ==============================================================================
# Clean active page name
clean_page_name = (
    selected_page
    .replace("⊞", "")
    .replace("👤", "")
    .replace("🛡️", "")
    .replace("📊", "")
    .replace("Σ", "")
    .replace("💾", "")
    .replace("👥", "")
    .replace("💡", "")
    .replace("ℹ️", "")
    .strip()
)

# Compute filtered dataframe
filtered_df = full_df.copy()
if st.session_state["f_gender"] != "All":
    filtered_df = filtered_df[filtered_df["gender"] == st.session_state["f_gender"]]
if st.session_state["f_contract"] != "All":
    filtered_df = filtered_df[filtered_df["Contract"] == st.session_state["f_contract"]]
if st.session_state["f_internet"] != "All":
    filtered_df = filtered_df[filtered_df["InternetService"] == st.session_state["f_internet"]]
if st.session_state["f_pay"] != "All":
    filtered_df = filtered_df[filtered_df["PaymentMethod"] == st.session_state["f_pay"]]
if st.session_state["f_tenure"] != "All":
    tenure_map = {
        "0-6 Months": (0, 6),
        "7-12 Months": (7, 12),
        "13-24 Months": (13, 24),
        "25-36 Months": (25, 36),
        "37-48 Months": (37, 48),
        "49-60 Months": (49, 60),
        "61-72 Months": (61, 72)
    }
    if st.session_state["f_tenure"] in tenure_map:
        t_min, t_max = tenure_map[st.session_state["f_tenure"]]
        filtered_df = filtered_df[(filtered_df["tenure"] >= t_min) & (filtered_df["tenure"] <= t_max)]

# Top Header Layout
col_hdr_left, col_hdr_right = st.columns([1.35, 1.05])
with col_hdr_left:
    st.markdown(f"""
    <div class="top-breadcrumb">
        <span class="bc-parent">Telco Retention BI &nbsp;›&nbsp;</span>
        <span class="bc-active">{clean_page_name}</span>
    </div>
    """, unsafe_allow_html=True)

with col_hdr_right:
    c_f, c_up, c_dl = st.columns([1.1, 0.95, 1.15])
    
    # 1. Filters Popover
    with c_f:
        filter_btn_label = f"🔍 Filters ({len(filtered_df):,}/{len(full_df):,})"
        with st.popover(filter_btn_label, use_container_width=True):
            st.markdown("##### **Filter Customer Cohorts**")
            f_g = st.selectbox("Gender", ["All"] + sorted(full_df["gender"].unique().tolist()), index=["All"] + sorted(full_df["gender"].unique().tolist()).index(st.session_state["f_gender"]) if st.session_state["f_gender"] in full_df["gender"].unique().tolist() else 0, key="pop_f_gender")
            f_c = st.selectbox("Contract Type", ["All"] + sorted(full_df["Contract"].unique().tolist()), index=["All"] + sorted(full_df["Contract"].unique().tolist()).index(st.session_state["f_contract"]) if st.session_state["f_contract"] in full_df["Contract"].unique().tolist() else 0, key="pop_f_contract")
            f_i = st.selectbox("Internet Service", ["All"] + sorted(full_df["InternetService"].unique().tolist()), index=["All"] + sorted(full_df["InternetService"].unique().tolist()).index(st.session_state["f_internet"]) if st.session_state["f_internet"] in full_df["InternetService"].unique().tolist() else 0, key="pop_f_internet")
            f_p = st.selectbox("Payment Method", ["All"] + sorted(full_df["PaymentMethod"].unique().tolist()), index=["All"] + sorted(full_df["PaymentMethod"].unique().tolist()).index(st.session_state["f_pay"]) if st.session_state["f_pay"] in full_df["PaymentMethod"].unique().tolist() else 0, key="pop_f_pay")
            tenure_opts = ["All", "0-6 Months", "7-12 Months", "13-24 Months", "25-36 Months", "37-48 Months", "49-60 Months", "61-72 Months"]
            f_t = st.selectbox("Tenure Range", tenure_opts, index=tenure_opts.index(st.session_state["f_tenure"]) if st.session_state["f_tenure"] in tenure_opts else 0, key="pop_f_tenure")
            
            c_apply, c_rst = st.columns(2)
            with c_apply:
                if st.button("Apply Filters", use_container_width=True):
                    st.session_state["f_gender"] = f_g
                    st.session_state["f_contract"] = f_c
                    st.session_state["f_internet"] = f_i
                    st.session_state["f_pay"] = f_p
                    st.session_state["f_tenure"] = f_t
                    st.rerun()
            with c_rst:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state["f_gender"] = "All"
                    st.session_state["f_contract"] = "All"
                    st.session_state["f_internet"] = "All"
                    st.session_state["f_pay"] = "All"
                    st.session_state["f_tenure"] = "All"
                    st.rerun()

    # 2. Upload Custom CSV Popover
    with c_up:
        with st.popover("📤 Upload CSV", use_container_width=True):
            st.markdown("##### **Upload Custom Telco Dataset**")
            st.caption("Upload any Telco Churn CSV file. All KPI cards, charts, and queries will recalculate automatically.")
            up_file = st.file_uploader("Choose CSV File", type=["csv"], key="pop_uploader_widget")
            if up_file is not None:
                st.session_state["custom_csv_upload"] = up_file
                st.success(f"✓ Active: `{up_file.name}`")
                if st.button("Load Dataset", use_container_width=True):
                    st.rerun()

    # 3. Export Clean CSV Button (Solid Blue)
    with c_dl:
        cleaned_path = parent_dir / "data" / "processed" / "telco_churn_cleaned.csv"
        if cleaned_path.exists():
            with open(cleaned_path, "rb") as f_cl:
                cl_bytes = f_cl.read()
        else:
            cl_bytes = full_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Clean CSV",
            data=cl_bytes,
            file_name="telco_churn_cleaned.csv",
            mime="text/csv",
            use_container_width=True
        )


# ==============================================================================
# 6 EXECUTIVE KPI CARDS (Matching Target Image Exactly)
# ==============================================================================
def render_6_kpi_cards(df: pd.DataFrame, total_dataset_len: int):
    """Renders 6 executive KPI cards in 1 row matching the SaaS design exactly."""
    total = len(df)
    if total == 0:
        st.warning("No customer records match the selected filter combination. Please reset filters.")
        return

    churned = int(df["ChurnBinary"].sum())
    active = total - churned
    rate = (churned / total * 100) if total > 0 else 0
    avg_bill = df["MonthlyCharges"].mean() if total > 0 else 0
    total_mrr = df["MonthlyCharges"].sum() if total > 0 else 0

    if total_mrr >= 1_000_000:
        mrr_str = f"${total_mrr/1_000_000:.2f}M"
    elif total_mrr >= 1_000:
        mrr_str = f"${total_mrr/1_000:.1f}k"
    else:
        mrr_str = f"${total_mrr:,.2f}"

    loyalty_share = (active / total * 100) if total > 0 else 0
    dataset_pct = (total / total_dataset_len * 100) if total_dataset_len > 0 else 100

    kpi_html = f"""
    <div class="kpi-row-6">
        <div class="kpi-card-v2">
            <div class="kpi-top">
                <span class="kpi-label-v2">Total Customers</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00D2FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
            </div>
            <div class="kpi-val-v2">{total:,}</div>
            <div class="kpi-sub-v2">{dataset_pct:.0f}% full dataset</div>
        </div>
        <div class="kpi-card-v2">
            <div class="kpi-top">
                <span class="kpi-label-v2">Active Retained</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="8.5" cy="7" r="4"></circle>
                    <polyline points="17 11 19 13 23 9"></polyline>
                </svg>
            </div>
            <div class="kpi-val-v2 text-green">{active:,}</div>
            <div class="kpi-sub-v2">{loyalty_share:.1f}% loyalty share</div>
        </div>
        <div class="kpi-card-v2">
            <div class="kpi-top">
                <span class="kpi-label-v2">Churned Customers</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="8.5" cy="7" r="4"></circle>
                    <line x1="18" y1="8" x2="23" y2="13"></line>
                    <line x1="23" y1="8" x2="18" y2="13"></line>
                </svg>
            </div>
            <div class="kpi-val-v2 text-rose">{churned:,}</div>
            <div class="kpi-sub-v2">Subscribers lost</div>
        </div>
        <div class="kpi-card-v2">
            <div class="kpi-top">
                <span class="kpi-label-v2">Churn Rate</span>
                <span class="kpi-badge-icon text-cyan">%</span>
            </div>
            <div class="kpi-val-v2 text-cyan">{rate:.2f}%</div>
            <div class="kpi-sub-v2">Industry avg ~21%</div>
        </div>
        <div class="kpi-card-v2">
            <div class="kpi-top">
                <span class="kpi-label-v2">Avg Monthly Charge</span>
                <span class="kpi-badge-icon text-blue">$</span>
            </div>
            <div class="kpi-val-v2">${avg_bill:.2f}</div>
            <div class="kpi-sub-v2">ARPU per account</div>
        </div>
        <div class="kpi-card-v2">
            <div class="kpi-top">
                <span class="kpi-label-v2">Monthly MRR</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00D2FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                    <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
            </div>
            <div class="kpi-val-v2">${mrr_str}</div>
            <div class="kpi-sub-v2">Recurring monthly</div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)


render_6_kpi_cards(filtered_df, len(full_df))


# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW (Pixel-Perfect Match to Target Image)
# ==============================================================================
if "Executive Overview" in selected_page:
    total = len(filtered_df)
    churned = int(filtered_df["ChurnBinary"].sum())
    active = total - churned
    rate = (churned / total * 100) if total > 0 else 0
    loyalty_share = (active / total * 100) if total > 0 else 0

    # Middle Row: 2 Large Cards (Customer Retention vs Attrition Split & Contract Commitment vs Churn Propensity)
    col_mid_left, col_mid_right = st.columns([0.9, 1.1])
    
    with col_mid_left:
        st.markdown(f"""
        <div class="card-panel" style="min-height:365px;">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;">
                <div>
                    <div style="font-size:0.96rem;font-weight:700;color:#FFFFFF;">Customer Retention vs Attrition Split</div>
                    <div style="font-size:0.75rem;color:#64748B;margin-top:2px;">Distribution of active vs cancelled accounts</div>
                </div>
                <div style="background:#1E293B;padding:3px 10px;border-radius:6px;font-size:0.72rem;font-weight:600;color:#94A3B8;">
                    N = {total:,}
                </div>
            </div>
        """, unsafe_allow_html=True)

        c_d1, c_d2 = st.columns([1.15, 0.85])
        with c_d1:
            st.plotly_chart(
                create_exact_split_donut(filtered_df),
                use_container_width=True,
                config={"displayModeBar": False}
            )
        with c_d2:
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;justify-content:center;height:220px;gap:20px;padding-left:6px;">
                <div>
                    <div style="display:flex;align-items:center;gap:8px;font-size:0.82rem;font-weight:600;color:#CBD5E1;">
                        <span style="width:8px;height:8px;border-radius:50%;background:#00D2FF;display:inline-block;"></span>
                        <span>Active Retained</span>
                    </div>
                    <div style="display:flex;align-items:baseline;gap:12px;margin-top:4px;padding-left:16px;">
                        <span style="font-size:1.15rem;font-weight:800;color:#FFFFFF;">{active:,}</span>
                        <span style="font-size:0.80rem;font-weight:600;color:#00D2FF;">{loyalty_share:.1f}%</span>
                    </div>
                </div>
                <div>
                    <div style="display:flex;align-items:center;gap:8px;font-size:0.82rem;font-weight:600;color:#CBD5E1;">
                        <span style="width:8px;height:8px;border-radius:50%;background:#0099DD;display:inline-block;"></span>
                        <span>Churned Accounts</span>
                    </div>
                    <div style="display:flex;align-items:baseline;gap:12px;margin-top:4px;padding-left:16px;">
                        <span style="font-size:1.15rem;font-weight:800;color:#FFFFFF;">{churned:,}</span>
                        <span style="font-size:0.80rem;font-weight:600;color:#EF4444;">{rate:.1f}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_mid_right:
        # Dynamic Contract Calculations
        m2m_df = filtered_df[filtered_df["Contract"] == "Month-to-month"]
        y1_df = filtered_df[filtered_df["Contract"] == "One year"]
        y2_df = filtered_df[filtered_df["Contract"] == "Two year"]

        tot_m2m = len(m2m_df)
        lost_m2m = int(m2m_df["ChurnBinary"].sum()) if tot_m2m > 0 else 0
        rate_m2m = (lost_m2m / tot_m2m * 100) if tot_m2m > 0 else 0

        tot_y1 = len(y1_df)
        lost_y1 = int(y1_df["ChurnBinary"].sum()) if tot_y1 > 0 else 0
        rate_y1 = (lost_y1 / tot_y1 * 100) if tot_y1 > 0 else 0

        tot_y2 = len(y2_df)
        lost_y2 = int(y2_df["ChurnBinary"].sum()) if tot_y2 > 0 else 0
        rate_y2 = (lost_y2 / tot_y2 * 100) if tot_y2 > 0 else 0

        stability_ratio = (rate_m2m / rate_y2) if rate_y2 > 0 else 15.0

        st.markdown(f"""
        <div class="card-panel" style="min-height:365px;">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:14px;">
                <div>
                    <div style="font-size:0.96rem;font-weight:700;color:#FFFFFF;">Contract Commitment vs Churn Propensity</div>
                    <div style="font-size:0.75rem;color:#64748B;margin-top:2px;">Comparison of attrition percentages across contract agreements</div>
                </div>
                <div style="color:#64748B;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                </div>
            </div>

            <!-- Month to month -->
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;font-size:0.80rem;font-weight:600;margin-bottom:6px;">
                    <span style="color:#CBD5E1;">Month-to-month</span>
                    <span><span style="color:#94A3B8;font-weight:500;">{lost_m2m:,} / {tot_m2m:,} lost</span> &nbsp; <b style="color:#EF4444;">{rate_m2m:.1f}%</b></span>
                </div>
                <div style="background:#1E293B;height:7px;border-radius:4px;overflow:hidden;width:100%;">
                    <div style="background:#EF4444;height:100%;width:{min(100, max(0, rate_m2m))}%;border-radius:4px;"></div>
                </div>
            </div>

            <!-- One year -->
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;font-size:0.80rem;font-weight:600;margin-bottom:6px;">
                    <span style="color:#CBD5E1;">One year</span>
                    <span><span style="color:#94A3B8;font-weight:500;">{lost_y1:,} / {tot_y1:,} lost</span> &nbsp; <b style="color:#F59E0B;">{rate_y1:.1f}%</b></span>
                </div>
                <div style="background:#1E293B;height:7px;border-radius:4px;overflow:hidden;width:100%;">
                    <div style="background:#F59E0B;height:100%;width:{min(100, max(0, rate_y1))}%;border-radius:4px;"></div>
                </div>
            </div>

            <!-- Two year -->
            <div style="margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;font-size:0.80rem;font-weight:600;margin-bottom:6px;">
                    <span style="color:#CBD5E1;">Two year</span>
                    <span><span style="color:#94A3B8;font-weight:500;">{lost_y2:,} / {tot_y2:,} lost</span> &nbsp; <b style="color:#10B981;">{rate_y2:.1f}%</b></span>
                </div>
                <div style="background:#1E293B;height:7px;border-radius:4px;overflow:hidden;width:100%;">
                    <div style="background:#10B981;height:100%;width:{min(100, max(0, rate_y2))}%;border-radius:4px;"></div>
                </div>
            </div>

            <!-- Strategic Vulnerability Callout Box -->
            <div style="background:rgba(0, 132, 255, 0.08);border:1px solid rgba(0, 132, 255, 0.22);border-radius:9px;padding:12px 14px;display:flex;align-items:flex-start;gap:10px;margin-top:16px;">
                <span style="color:#00D2FF;font-size:15px;line-height:1.2;">ⓘ</span>
                <div style="font-size:0.77rem;color:#CBD5E1;line-height:1.45;">
                    <b style="color:#FFFFFF;">Primary Strategic Vulnerability:</b> Month-to-month contracts suffer an attrition rate of <b style="color:#EF4444;">{rate_m2m:.1f}%</b>, compared to just <b style="color:#10B981;">{rate_y2:.1f}%</b> on two-year agreements—a <b style="color:#00D2FF;">{stability_ratio:.0f}x stability difference</b>.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Bottom Row: 3 Cards (Monthly MRR, Tenure Cohorts, Payment Method Attrition)
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        st.markdown("""
        <div class="card-panel" style="padding-bottom:6px;margin-bottom:8px;">
            <div style="font-size:0.92rem;font-weight:700;color:#FFFFFF;margin-bottom:2px;">Monthly MRR by Contract Type</div>
            <div style="font-size:0.74rem;color:#64748B;">Recurring revenue contribution across agreement horizons</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(create_contract_mrr_bars(filtered_df), use_container_width=True, config={"displayModeBar": False})

    with col_b2:
        st.markdown("""
        <div class="card-panel" style="padding-bottom:6px;margin-bottom:8px;">
            <div style="font-size:0.92rem;font-weight:700;color:#FFFFFF;margin-bottom:2px;">Tenure Cohorts (Months)</div>
            <div style="font-size:0.74rem;color:#64748B;">Customer distribution across lifecycle tenure tiers</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(create_exact_tenure_bars(filtered_df), use_container_width=True, config={"displayModeBar": False})

    with col_b3:
        st.markdown("""
        <div class="card-panel" style="padding-bottom:6px;margin-bottom:8px;">
            <div style="font-size:0.92rem;font-weight:700;color:#FFFFFF;margin-bottom:2px;">Payment Method Attrition</div>
            <div style="font-size:0.74rem;color:#64748B;">Defection rates across electronic and automated channels</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(create_exact_payment_bars(filtered_df), use_container_width=True, config={"displayModeBar": False})


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
# PAGE 5: STATISTICAL ANALYSIS
# ==============================================================================
elif "Statistical Analysis" in selected_page:
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
# PAGE 6: SQL BUSINESS ANALYTICS
# ==============================================================================
elif "SQL Business Analytics" in selected_page or "SQL Analytics" in selected_page:
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
                <div style="font-size:0.96rem;font-weight:700;color:#38BDF8;margin-bottom:8px;">1. Annual Contract Term Transition</div>
                <div style="font-size:0.86rem;line-height:1.6;color:#CBD5E1;">
                    <b style="color:#FFFFFF;">Observed Finding:</b> Month-to-month contracts experience catastrophic 42.71% churn vs 11.27% for 1-year and 2.83% for 2-year.<br>
                    <b style="color:#FFFFFF;">Supporting Statistic:</b> Month-to-month accounts generate 88.55% of all defection (1,655 out of 1,869 churned accounts).<br>
                    <b style="color:#FFFFFF;">Business Impact:</b> Uncommitted customers create high revenue volatility and churn costs.<br>
                    <b style="color:#FFFFFF;">Suggested Action:</b> Offer a $10/month statement credit or line speed upgrade at Month 3 in exchange for an annual contract commitment.
                </div>
            </div>
            <div class="card-panel">
                <div style="font-size:0.96rem;font-weight:700;color:#38BDF8;margin-bottom:8px;">2. Auto-Pay Billing Optimization</div>
                <div style="font-size:0.86rem;line-height:1.6;color:#CBD5E1;">
                    <b style="color:#FFFFFF;">Observed Finding:</b> Electronic check users churn at 45.29%, nearly 3x higher than automated credit cards (15.24%) and bank transfers (16.71%).<br>
                    <b style="color:#FFFFFF;">Supporting Statistic:</b> Over 57.3% of all churned accounts (1,071 customers) use Electronic Check.<br>
                    <b style="color:#FFFFFF;">Business Impact:</b> Manual billing prompts monthly conscious scrutiny of the bill and elevated payment friction.<br>
                    <b style="color:#FFFFFF;">Suggested Action:</b> Introduce a $5/month recurring bill discount for enrolling in Credit Card or Bank Auto-Pay.
                </div>
            </div>
            <div class="card-panel">
                <div style="font-size:0.96rem;font-weight:700;color:#38BDF8;margin-bottom:8px;">3. The First 90 Days Care Journey</div>
                <div style="font-size:0.86rem;line-height:1.6;color:#CBD5E1;">
                    <b style="color:#FFFFFF;">Observed Finding:</b> Over 55.5% of all defection occurs in the first 12 months; churned customers defect at an average of 17.98 months (median 10 months).<br>
                    <b style="color:#FFFFFF;">Supporting Statistic:</b> 0-12m cohort churns at 47.44%, while 49-72m cohort churns at only 9.38%.<br>
                    <b style="color:#FFFFFF;">Business Impact:</b> Acquisition spend is squandered before customer accounts reach profitability.<br>
                    <b style="color:#FFFFFF;">Suggested Action:</b> Implement an onboarding sequence: Day 7 connection check, Day 30 bill review, and Day 60 speed optimization check.
                </div>
            </div>
            <div class="card-panel">
                <div style="font-size:0.96rem;font-weight:700;color:#38BDF8;margin-bottom:8px;">4. Fiber Optic Support Bundling</div>
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
# PAGE 9: ABOUT PROJECT & TEAM MEMBERS
# ==============================================================================
elif "About Project" in selected_page or "Project Information" in selected_page:
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
        - **Project Title:** Customer Churn Analysis & Business Intelligence Dashboard
        - **Institution:** Sreenidhi Institute of Science and Technology (Autonomous), Hyderabad
        - **Department:** Department of Data Science (CSE-DS)
        - **Academic Period:** III Year I Semester — November 2026
        - **Internship Coordinator:** Mr. Syed. Mazharuddin
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
