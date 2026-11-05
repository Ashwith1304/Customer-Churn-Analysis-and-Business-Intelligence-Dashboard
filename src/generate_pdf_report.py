"""
Academic Summer Internship Report Generator
Project: CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD
Institution: Sreenidhi Institute of Science and Technology (Autonomous)
Department: Department of Data Science (CSE-DS)
Team Members:
  - G Mythili (24311A67H8)
  - K Ashiwith (24311A67H6)
  - D Niyati (24311A67H7)
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with page numbers (Page X of Y)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        # Skip headers/footers on preliminary pages (first 6 pages)
        if self._pageNumber <= 6:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Top Header
        self.drawString(54, 750, "DEPARTMENT OF DATA SCIENCE (CSE-DS) — SREENIDHI INSTITUTE OF SCIENCE & TECHNOLOGY")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 744, 558, 744)

        # Running Bottom Footer
        self.line(54, 48, 558, 48)
        self.setFont("Helvetica", 8)
        self.drawString(54, 36, "Customer Churn Analysis & Business Intelligence Dashboard")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.restoreState()


def build_pdf_report(output_pdf_path: str, viz_dir: str):
    """Constructs the comprehensive 40+ page academic internship report."""
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Palette
    primary_color = colors.HexColor("#0F172A")
    secondary_color = colors.HexColor("#1E3A8A")
    accent_blue = colors.HexColor("#0284C7")
    dark_gray = colors.HexColor("#334155")
    light_bg = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    # Typography Styles
    style_cover_dept = ParagraphStyle(
        "CoverDept",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=1, # Center
        textColor=secondary_color
    )
    style_cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=26,
        alignment=1,
        textColor=primary_color
    )
    style_cover_sub = ParagraphStyle(
        "CoverSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=dark_gray
    )
    style_cover_author = ParagraphStyle(
        "CoverAuthor",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=primary_color
    )
    style_h1 = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=secondary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    style_h3 = ParagraphStyle(
        "Heading3_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=accent_blue,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=dark_gray,
        spaceAfter=8
    )
    style_body_bold = ParagraphStyle(
        "Body_Bold",
        parent=style_body,
        fontName="Helvetica-Bold",
        textColor=primary_color
    )
    style_callout = ParagraphStyle(
        "Callout_Text",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )
    style_code = ParagraphStyle(
        "Code_Block",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )
    style_table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=dark_gray
    )
    style_table_head = ParagraphStyle(
        "TableHead",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Paragraph("Batch No: Office Use", ParagraphStyle("Batch", fontName="Helvetica", fontSize=9, alignment=0, textColor=dark_gray)))
    story.append(Spacer(1, 40))
    story.append(Paragraph("CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD", style_cover_title))
    story.append(Spacer(1, 8))
    story.append(Paragraph("A Data Analytics and Business Intelligence Project", style_cover_sub))
    story.append(Spacer(1, 28))
    story.append(Paragraph("A Summer Industry Internship Report<br/>Submitted in Partial Fulfillment of the Requirements<br/>For the award of the Degree of", style_cover_sub))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Bachelor of Technology in<br/><b>Computer Science and Engineering – Data Science (CSE-DS)</b>", style_cover_dept))
    story.append(Spacer(1, 28))
    story.append(Paragraph("By", style_cover_sub))
    story.append(Spacer(1, 10))

    team_cover_table = [
        [Paragraph("<b>G MYTHILI</b>", style_cover_author), Paragraph("<b>24311A67H8</b>", style_cover_author)],
        [Paragraph("<b>K ASHIWITH</b>", style_cover_author), Paragraph("<b>24311A67H6</b>", style_cover_author)],
        [Paragraph("<b>D NIYATI</b>", style_cover_author), Paragraph("<b>24311A67H7</b>", style_cover_author)],
    ]
    t_cov = Table(team_cover_table, colWidths=[200, 160], hAlign="CENTER")
    t_cov.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_cov)
    story.append(Spacer(1, 45))

    story.append(Paragraph("DEPARTMENT OF DATA SCIENCE (CSE-DS)<br/><b>SREENIDHI INSTITUTE OF SCIENCE AND TECHNOLOGY</b><br/>(An Autonomous Institution, Approved by AICTE, Accredited by NAAC with 'A+' Grade)<br/>Yamnampet, Ghatkesar, Hyderabad - 501301", style_cover_dept))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>November 2026</b>", style_cover_dept))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ACCEPTANCE BY INTERNAL TECHNICAL REVIEW COMMITTEE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("ACCEPTANCE BY INTERNAL TECHNICAL REVIEW COMMITTEE", style_cover_dept))
    story.append(Paragraph("(For Internal Department use only)", style_cover_sub))
    story.append(Spacer(1, 25))
    story.append(Paragraph(
        "We hereby approve the Presentation and Report of the Summer Industry Internship work titled:",
        style_body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD</b>", style_h2))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Submitted by Roll No. <b>24311A67H8, 24311A67H6, 24311A67H7</b>, studying in the <b>B.Tech CSE - DATA SCIENCE</b> branch in III Year I Semester.",
        style_body
    ))
    story.append(Spacer(1, 40))

    reviewers_table = [
        [Paragraph("<b>Internal Review Committee Members:</b>", style_body_bold), ""],
        [Paragraph("<br/><br/>1. Signature: _______________________<br/>Name: <b>Mr. P. V. K. Sandeep</b><br/>Project Coordinator, CSE-DS", style_body),
         Paragraph("<br/><br/>2. Signature: _______________________<br/>Name: <b>Dr. Md. Jaffar Sadiq</b><br/>Head of Department, CSE-DS", style_body)],
        [Paragraph("<br/><br/><br/>3. Signature: _______________________<br/>Internal Examiner", style_body),
         Paragraph("<br/><br/><br/>4. Signature: _______________________<br/>Date: ________________________", style_body)]
    ]
    t_rev = Table(reviewers_table, colWidths=[240, 240])
    t_rev.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(t_rev)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CERTIFICATE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("SREENIDHI INSTITUTE OF SCIENCE AND TECHNOLOGY", style_cover_dept))
    story.append(Paragraph("(AUTONOMOUS)", style_cover_sub))
    story.append(Paragraph("DEPARTMENT OF CSE – DATA SCIENCE (CSE-DS)", style_cover_dept))
    story.append(Spacer(1, 15))
    story.append(Paragraph("CERTIFICATE", style_h1))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "This is to certify that the Summer Industry Internship work titled <b>'CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD'</b> "
        "submitted by the students <b>G Mythili</b>, <b>K Ashiwith</b>, and <b>D Niyati</b> bearing Roll No. <b>24311A67H8, 24311A67H6</b> and <b>24311A67H7</b>, "
        "towards partial fulfillment for the award of Bachelor's Degree in Computer Science and Engineering – Data Science (CSE-DS) from Sreenidhi Institute of Science and Technology, "
        "Ghatkesar, Hyderabad, is a record of Bonafide work carried out by them under supervision. The results embodied in this work have not been submitted to any other University or Institute for the award of any other degree or diploma.",
        style_body
    ))
    story.append(Spacer(1, 60))

    cert_signatures = [
        [Paragraph("<b>Mr. P. V. K. Sandeep</b><br/>Project Coordinator<br/>Department of CSE-DS", style_body),
         Paragraph("<b>Dr. Md. Jaffar Sadiq</b><br/>Head of Department<br/>Department of CSE-DS", style_body)],
        [Paragraph("<br/><br/><br/><br/><b>External Examiner Signature</b>", style_body),
         Paragraph("<br/><br/><br/><br/><b>Principal</b><br/>Dr. T. Ch. Siva Reddy", style_body)]
    ]
    t_cert = Table(cert_signatures, colWidths=[240, 240])
    t_cert.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(t_cert)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DECLARATION
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("DECLARATION", style_h1))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "We, <b>G Mythili</b> (24311A67H8), <b>K Ashiwith</b> (24311A67H6), and <b>D Niyati</b> (24311A67H7), students of Sreenidhi Institute of Science and Technology, "
        "Yamnampet, Ghatkesar, studying III Year, I Semester, Bachelor of Technology in Computer Science and Engineering – Data Science (CSE-DS), hereby solemnly declare that the project report titled "
        "<b>'CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD'</b> is submitted in partial fulfillment for the award of the degree of Bachelor of Technology in Computer Science and Engineering – Data Science (CSE-DS).",
        style_body
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "It is further declared that, to the best of our knowledge, the work reported in this project has not been submitted earlier, either in part or in full, to any other University or Institute for the award of any degree or diploma.",
        style_body
    ))
    story.append(Spacer(1, 45))

    dec_table = [
        [Paragraph("<b>G MYTHILI</b><br/>24311A67H8", style_body_bold), Paragraph("SIGNATURE: _______________________", style_body)],
        [Paragraph("<br/><br/><b>K ASHIWITH</b><br/>24311A67H6", style_body_bold), Paragraph("<br/><br/>SIGNATURE: _______________________", style_body)],
        [Paragraph("<br/><br/><b>D NIYATI</b><br/>24311A67H7", style_body_bold), Paragraph("<br/><br/>SIGNATURE: _______________________", style_body)],
    ]
    t_dec = Table(dec_table, colWidths=[240, 240])
    story.append(t_dec)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("ACKNOWLEDGEMENT", style_h1))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "It gives us immense satisfaction to express our gratitude on the successful completion of our project. "
        "However, this project would remain incomplete without the support, guidance, and encouragement of the people who have played a significant role in shaping this work. "
        "We take this opportunity to sincerely thank all those who contributed directly or indirectly to the completion of this project.",
        style_body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "At the outset, we express our sincere thanks and deep sense of gratitude to <b>Mr. P. V. K. Sandeep</b>, Project Coordinator, for his continuous guidance, valuable suggestions, "
        "and constant encouragement throughout the course of this project. His insightful feedback, technical support, and motivation helped us overcome various challenges and complete our work successfully.",
        style_body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "We are extremely thankful to <b>Dr. Md. Jaffar Sadiq</b>, Head of the Department, CSE-DS, for providing us with the opportunity to undertake this project and for his consistent support and encouragement. "
        "His inspiring leadership and expert guidance created a positive academic environment that greatly contributed to the smooth execution of our project work.",
        style_body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "We also thank our Principal, <b>Dr. T. Ch. Siva Reddy</b>, for permitting us to pursue this internship project and for his continuous institutional support.",
        style_body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Finally, we extend our sincere thanks to all the faculty members of the Department of Data Science and our peers for their cooperation, suggestions, and support during this project work. "
        "Above all, we are grateful to our parents for their continuous encouragement and blessings, which played a crucial role in the successful completion of this project.",
        style_body
    ))
    story.append(Spacer(1, 35))

    ack_names = [
        [Paragraph("<b>G MYTHILI</b>", style_body_bold), Paragraph("24311A67H8", style_body)],
        [Paragraph("<b>K ASHIWITH</b>", style_body_bold), Paragraph("24311A67H6", style_body)],
        [Paragraph("<b>D NIYATI</b>", style_body_bold), Paragraph("24311A67H7", style_body)],
    ]
    t_ack = Table(ack_names, colWidths=[200, 200])
    story.append(t_ack)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ABSTRACT
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD", style_cover_dept))
    story.append(Paragraph("A Data Analytics and Business Intelligence Project", style_cover_sub))
    story.append(Spacer(1, 8))
    story.append(Paragraph("G MYTHILI (24311A67H8), K ASHIWITH (24311A67H6), D NIYATI (24311A67H7)", style_body_bold))
    story.append(Spacer(1, 15))
    story.append(Paragraph("ABSTRACT", style_h1))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Customer churn is a critical operational vulnerability in subscription-based telecommunication enterprises, directly degrading monthly recurring revenue (MRR) and inflating customer acquisition expenses. "
        "While modern literature frequently approaches retention through complex black-box Machine Learning algorithms, such models often conceal transparent operational drivers, present compliance hurdles, and create brittle dependencies. "
        "In contrast, this project establishes a rigorous, purely analytical Business Intelligence (BI) framework utilizing empirical Exploratory Data Analysis (EDA), parametric and non-parametric descriptive statistics, inferential hypothesis testing, relational SQL modeling, and an executive multi-page web platform.",
        style_body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Analyzing 7,043 customer accounts from the industry-standard IBM Telco Customer Churn dataset, the investigation identified an overall churn rate of <b>26.54% (1,869 accounts)</b>, eroding over <b>$139,130 in monthly revenue ($1.67 Million annualized)</b>. "
        "Data quality auditing handled 11 whitespace records in cumulative billing without discarding customer history, and validated outlier absence via 1.5×IQR boundaries across continuous dimensions. "
        "Inferential statistical tests definitively isolated contract agreements (Pearson Chi-Square statistic = 1,184.60, p < 10^-250, Cramér's V = 0.410) and payment methods (Chi-Square = 648.14, p < 10^-140, Cramér's V = 0.303) as the primary drivers of defection. "
        "Month-to-month contracts demonstrated a 42.71% churn rate, comprising 88.55% of all churned accounts, while electronic check payment methods exhibited a 45.29% churn rate. "
        "Welch's independent two-sample t-test confirmed that churned customers possess significantly lower tenure (17.98 months vs 37.57 months, t = -34.82, p < 10^-200) and pay a statistically significant price premium of $13.18/month ($74.44 vs $61.27, t = +18.41, p < 10^-70).",
        style_body
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "An SQLite database engine was constructed to execute 10 executive business queries, powering a commercial-grade Business Intelligence application built with Streamlit and Plotly. "
        "The resulting platform features dynamic multi-attribute global filtering, live SQL sandbox querying, cohort vulnerability grids, and an interactive financial ROI simulator. "
        "Targeted strategic interventions—including annual contract upgrade credits, auto-pay discounts, structured 90-day onboarding, and fiber optic support bundling—demonstrate potential to safeguard between $300,000 and $500,000 in protected annual recurring revenue.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: TABLE OF CONTENTS
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("CONTENTS", style_h1))
    story.append(Spacer(1, 12))

    toc_data = [
        [Paragraph("<b>1. INTRODUCTION</b>", style_body_bold), Paragraph("<b>1</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background and Telecommunications Industry Context", style_body), Paragraph("1", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 The Strategic Significance of Customer Retention", style_body), Paragraph("2", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Pure Data Science & Business Intelligence vs. Machine Learning", style_body), Paragraph("3", style_body)],
        [Paragraph("<b>2. PROBLEM STATEMENT & OBJECTIVES</b>", style_body_bold), Paragraph("<b>4</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Problem Definition & Revenue Vulnerability", style_body), Paragraph("4", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Core Business Questions", style_body), Paragraph("5", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Project Objectives & Performance Scope", style_body), Paragraph("6", style_body)],
        [Paragraph("<b>3. DATASET DESCRIPTION & ARCHITECTURE</b>", style_body_bold), Paragraph("<b>7</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Dataset Attribution & Characteristics", style_body), Paragraph("7", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Comprehensive Feature Data Dictionary", style_body), Paragraph("8", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 End-to-End System Architecture", style_body), Paragraph("10", style_body)],
        [Paragraph("<b>4. DATA CLEANING & AUDITING PIPELINE</b>", style_body_bold), Paragraph("<b>11</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Ingestion and Structural Integrity Verification", style_body), Paragraph("11", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Whitespace Resolution in TotalCharges", style_body), Paragraph("12", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Statistical Outlier Diagnostics (1.5 × IQR Rule)", style_body), Paragraph("13", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Feature Engineering and Cohort Categorization", style_body), Paragraph("14", style_body)],
        [Paragraph("<b>5. EXPLORATORY DATA ANALYSIS (EDA)</b>", style_body_bold), Paragraph("<b>15</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Univariate Distribution Analysis", style_body), Paragraph("15", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Bivariate Churn Cross-Tabulations", style_body), Paragraph("18", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Multivariate Interactions & Correlation Matrix", style_body), Paragraph("22", style_body)],
        [Paragraph("<b>6. INFERENTIAL STATISTICAL ANALYSIS & HYPOTHESIS TESTING</b>", style_body_bold), Paragraph("<b>24</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Parametric & Non-Parametric Summary Statistics", style_body), Paragraph("24", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Pearson Chi-Square Tests of Independence & Cramér's V", style_body), Paragraph("25", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Welch's Two-Sample Independent T-Tests", style_body), Paragraph("27", style_body)],
        [Paragraph("<b>7. RELATIONAL SQL BUSINESS ANALYSIS</b>", style_body_bold), Paragraph("<b>29</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Relational Schema & SQLite Storage Architecture", style_body), Paragraph("29", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Ten Executive SQL Business Queries & Results", style_body), Paragraph("30", style_body)],
        [Paragraph("<b>8. BUSINESS INTELLIGENCE DASHBOARD IMPLEMENTATION</b>", style_body_bold), Paragraph("<b>35</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.1 User Interface Architecture & SaaS Design System", style_body), Paragraph("35", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.2 Reactive Global Filter Engine & Component Layout", style_body), Paragraph("36", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.3 Multi-Page Module Specifications", style_body), Paragraph("37", style_body)],
        [Paragraph("<b>9. STRATEGIC BUSINESS RECOMMENDATIONS & FINANCIAL ROI</b>", style_body_bold), Paragraph("<b>39</b>", style_body_bold)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.1 Four-Pillar Retention Framework", style_body), Paragraph("39", style_body)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.2 Financial ROI Modeling & Revenue Safeguards", style_body), Paragraph("41", style_body)],
        [Paragraph("<b>10. CONCLUSION & FUTURE SCOPE</b>", style_body_bold), Paragraph("<b>42</b>", style_body_bold)],
        [Paragraph("<b>REFERENCES</b>", style_body_bold), Paragraph("<b>44</b>", style_body_bold)],
        [Paragraph("<b>APPENDIX: SOURCE CODE LISTINGS & SETUP</b>", style_body_bold), Paragraph("<b>45</b>", style_body_bold)],
    ]
    t_toc = Table(toc_data, colWidths=[430, 50])
    t_toc.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("1. INTRODUCTION", style_h1))
    story.append(Paragraph("1.1 Background and Telecommunications Industry Context", style_h2))
    story.append(Paragraph(
        "In the modern subscription economy, particularly within the telecommunications sector, subscriber attrition—commonly known as customer churn—represents one of the most substantial impediments to sustained profitability and market capitalization. "
        "Telecommunications infrastructure providers operate in highly saturated and intensely competitive markets characterized by high fixed capital expenditures in fiber-optic deployment, cellular towers, and spectrum licenses. "
        "In this capital-intensive environment, acquiring a new customer is estimated by telecommunication industry benchmarks to cost between five and twenty-five times more than retaining an existing subscriber.",
        style_body
    ))
    story.append(Paragraph(
        "When an account defects, the provider not only loses immediate monthly recurring revenue (MRR), but also forfeits the long-term customer lifetime value (CLV) and incurs substantial unrecoverable customer acquisition costs (CAC) associated with marketing, installation, customer premises equipment (CPE), and onboarding subsidies.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.2 The Strategic Significance of Customer Retention", style_h2))
    story.append(Paragraph(
        "Research in customer loyalty economics shows that even modest improvements in customer retention deliver disproportionately large expansions in net profitability. "
        "A classical five percent increase in customer retention can boost corporate profits by 25% to 95%, because long-tenure customers typically generate higher average revenue per user (ARPU), require lower servicing costs, demonstrate greater willingness to adopt bundled premium services, and serve as organic brand advocates. "
        "Consequently, telecommunication executives require transparent, empirical visibility into customer defection patterns to implement targeted interventions before accounts cancel.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.3 Pure Data Science & Business Intelligence vs. Machine Learning", style_h2))
    story.append(Paragraph(
        "In recent years, enterprise data teams have frequently deployed complex Machine Learning (ML) classifiers—such as Gradient Boosted Trees, Random Forests, and Deep Neural Networks—to forecast churn probabilities. "
        "While predictive models possess statistical utility, they frequently suffer from critical operational limitations in business leadership contexts:",
        style_body
    ))

    ml_vs_bi = [
        [Paragraph("<b>Evaluation Dimension</b>", style_table_head), Paragraph("<b>Predictive Machine Learning</b>", style_table_head), Paragraph("<b>Pure Data Science & BI (This Project)</b>", style_table_head)],
        [Paragraph("<b>Model Transparency</b>", style_table_cell), Paragraph("Opaque 'black-box' feature interactions; hard to justify to executives.", style_table_cell), Paragraph("Fully explainable empirical distributions, hypothesis tests, and SQL queries.", style_table_cell)],
        [Paragraph("<b>Causality & Actionability</b>", style_table_cell), Paragraph("Scores risk scores without clear operational remediations.", style_table_cell), Paragraph("Directly identifies policy friction (e.g., electronic check fees, contract terms).", style_table_cell)],
        [Paragraph("<b>Computational Overhead</b>", style_table_cell), Paragraph("Requires model retraining, concept drift monitoring, GPU/cloud dependencies.", style_table_cell), Paragraph("Lightweight, instantaneous query execution on indexed relational tables.", style_table_cell)],
        [Paragraph("<b>Executive Trust</b>", style_table_cell), Paragraph("Statistical hallucinations or overfitting risks erode executive confidence.", style_table_cell), Paragraph("100% verifiable audited data grounded in classical inferential mathematics.", style_table_cell)],
    ]
    t_comp = Table(ml_vs_bi, colWidths=[120, 180, 204])
    t_comp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [light_bg, colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "By focusing strictly on rigorous exploratory data analysis, parametric and non-parametric descriptive statistics, hypothesis testing (Chi-Square & Welch's t-tests), and relational SQL analytics, this project equips decision-makers with completely explainable and actionable retention strategies.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: PROBLEM STATEMENT & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("2. PROBLEM STATEMENT & OBJECTIVES", style_h1))
    story.append(Paragraph("2.1 Problem Definition & Revenue Vulnerability", style_h2))
    story.append(Paragraph(
        "A mid-sized telecommunications service provider is observing customer attrition across its primary service lines (Fixed Landline, DSL Broadband, and Fiber Optic Internet). "
        "Management has observed that customer churn is eroding monthly recurring revenue (MRR) at an unsustainable rate, yet leadership lacks quantitative clarity regarding which customer cohorts are defecting, when defection occurs during the subscriber lifecycle, and what commercial policies are accelerating customer loss.",
        style_body
    ))
    story.append(Paragraph(
        "Without transparent analytics, retention marketing budgets are distributed uniformly across all customer segments rather than concentrated on the specific contractual arrangements and billing channels where revenue is hemorrhaging.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 Core Business Questions", style_h2))
    story.append(Paragraph("To address this operational challenge, the analysis must definitively answer 10 executive business questions:", style_body))

    questions = [
        "1. What is the total size of the customer base and how many accounts are actively monitored?",
        "2. What is the absolute number of churned customers and what is the overall corporate churn rate?",
        "3. How does customer churn distribute across different contractual commitments (Month-to-month, One year, Two year)?",
        "4. Which billing and payment method exhibits the highest volume and proportion of customer defection?",
        "5. What is the average monthly charge (ARPU) across retained versus churned subscriber cohorts?",
        "6. Which broadband delivery technology (DSL vs. Fiber Optic vs. No Internet) experiences the most severe defection rate?",
        "7. What is the average subscription tenure of churned accounts relative to retained customers?",
        "8. Which multi-attribute customer segment generates the largest monthly recurring revenue (MRR)?",
        "9. What volume and percentage of subscribers are enrolled in month-to-month commitments?",
        "10. What concrete, data-backed interventions can enterprise leadership execute to protect monthly revenue?"
    ]
    for q in questions:
        story.append(Paragraph(f"<b>• {q}</b>", style_body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.3 Project Objectives & Performance Scope", style_h2))
    story.append(Paragraph(
        "The primary objectives of this investigation include:",
        style_body
    ))
    story.append(Paragraph("<b>1. Data Ingestion & Auditing:</b> Ingest the 7,043-record IBM Telco customer dataset, audit structural integrity, resolve whitespace values, detect outliers via 1.5×IQR rules, and engineer analytical cohorts.", style_body))
    story.append(Paragraph("<b>2. Descriptive & Inferential Statistics:</b> Compute parametric and non-parametric central tendencies and dispersions; conduct Pearson Chi-Square tests of independence and Welch's two-sample independent t-tests.", style_body))
    story.append(Paragraph("<b>3. Relational SQL Modeling:</b> Design a relational SQLite schema, insert sanitized customer records, create performance b-tree indices, and formulate optimized SQL queries to address all core business questions.", style_body))
    story.append(Paragraph("<b>4. Interactive Business Intelligence Dashboard:</b> Develop a 9-page commercial-grade web dashboard utilizing Streamlit and Plotly, providing multi-variable global filtering, live SQL sandbox querying, and financial ROI simulation.", style_body))
    story.append(Paragraph("<b>5. Strategic Policy Formulation:</b> Synthesize analytical findings into a concrete Four-Pillar Retention Framework with quantifiable financial projections.", style_body))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 3: DATASET DESCRIPTION & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("3. DATASET DESCRIPTION & ARCHITECTURE", style_h1))
    story.append(Paragraph("3.1 Dataset Attribution & Characteristics", style_h2))
    story.append(Paragraph(
        "The project evaluates the industry-benchmark <b>IBM Telco Customer Churn Dataset</b>, curated and distributed by BlastChar via Kaggle. "
        "The dataset represents <b>7,043 unique telecommunication customer accounts</b> in California, capturing customer demographic attributes, account subscription parameters, value-added service bundles, payment channels, and churn outcomes over an observed quarterly billing window.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Comprehensive Feature Data Dictionary", style_h2))
    story.append(Paragraph("The dataset comprises 21 raw columns and 4 engineered analytical dimensions as detailed below:", style_body))

    data_dict = [
        [Paragraph("<b>Attribute</b>", style_table_head), Paragraph("<b>Data Type</b>", style_table_head), Paragraph("<b>Domain Values</b>", style_table_head), Paragraph("<b>Description</b>", style_table_head)],
        [Paragraph("customerID", style_code), Paragraph("String", style_table_cell), Paragraph("Alphanumeric string", style_table_cell), Paragraph("Unique customer account identifier.", style_table_cell)],
        [Paragraph("gender", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Female, Male", style_table_cell), Paragraph("Customer biological sex.", style_table_cell)],
        [Paragraph("SeniorCitizen", style_code), Paragraph("Binary Flag", style_table_cell), Paragraph("0, 1", style_table_cell), Paragraph("Customer senior citizen demographic flag.", style_table_cell)],
        [Paragraph("Partner", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No", style_table_cell), Paragraph("Indicates whether customer has a domestic partner.", style_table_cell)],
        [Paragraph("Dependents", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No", style_table_cell), Paragraph("Indicates whether customer supports dependents.", style_table_cell)],
        [Paragraph("tenure", style_code), Paragraph("Integer", style_table_cell), Paragraph("0 to 72 months", style_table_cell), Paragraph("Number of months subscriber has remained with company.", style_table_cell)],
        [Paragraph("PhoneService", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No", style_table_cell), Paragraph("Fixed landline voice telephone subscription.", style_table_cell)],
        [Paragraph("MultipleLines", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No, No phone service", style_table_cell), Paragraph("Customer has multiple telephone lines.", style_table_cell)],
        [Paragraph("InternetService", style_code), Paragraph("Categorical", style_table_cell), Paragraph("DSL, Fiber optic, No", style_table_cell), Paragraph("Broadband internet technology delivery type.", style_table_cell)],
        [Paragraph("OnlineSecurity", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No, No internet service", style_table_cell), Paragraph("Cybersecurity firewall protection add-on.", style_table_cell)],
        [Paragraph("OnlineBackup", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No, No internet service", style_table_cell), Paragraph("Cloud data storage backup subscription.", style_table_cell)],
        [Paragraph("DeviceProtection", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No, No internet service", style_table_cell), Paragraph("Hardware replacement warranty add-on.", style_table_cell)],
        [Paragraph("TechSupport", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No, No internet service", style_table_cell), Paragraph("Priority technical assistance subscription.", style_table_cell)],
        [Paragraph("StreamingTV", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No, No internet service", style_table_cell), Paragraph("Digital television programming package.", style_table_cell)],
        [Paragraph("StreamingMovies", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No, No internet service", style_table_cell), Paragraph("Digital movie on-demand subscription.", style_table_cell)],
        [Paragraph("Contract", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Month-to-month, One year, Two year", style_table_cell), Paragraph("Billing contract commitment duration.", style_table_cell)],
        [Paragraph("PaperlessBilling", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Yes, No", style_table_cell), Paragraph("Digital invoice delivery indicator.", style_table_cell)],
        [Paragraph("PaymentMethod", style_code), Paragraph("Categorical", style_table_cell), Paragraph("Electronic check, Mailed check, Bank transfer, Credit card", style_table_cell), Paragraph("Billing remittance channel.", style_table_cell)],
        [Paragraph("MonthlyCharges", style_code), Paragraph("Float64 ($)", style_table_cell), Paragraph("$18.25 to $118.75", style_table_cell), Paragraph("Recurring monthly subscription charge.", style_table_cell)],
        [Paragraph("TotalCharges", style_code), Paragraph("Float64 ($)", style_table_cell), Paragraph("$0.00 to $8684.80", style_table_cell), Paragraph("Cumulative charges billed across account lifetime.", style_table_cell)],
        [Paragraph("Churn", style_code), Paragraph("Target Flag", style_table_cell), Paragraph("Yes, No", style_table_cell), Paragraph("Indicates whether customer defected during period.", style_table_cell)],
        [Paragraph("ChurnBinary", style_code), Paragraph("Engineered Flag", style_table_cell), Paragraph("0, 1", style_table_cell), Paragraph("Numerical representation: 1 = Churned, 0 = Retained.", style_table_cell)],
        [Paragraph("TenureCohort", style_code), Paragraph("Engineered Cohort", style_table_cell), Paragraph("0-12m, 13-24m, 25-48m, 49-72m", style_table_cell), Paragraph("Customer lifecycle stage grouping.", style_table_cell)],
        [Paragraph("MonthlyChargesTier", style_code), Paragraph("Engineered Tier", style_table_cell), Paragraph("Low (<$35), Medium ($35-$70), High (>$70)", style_table_cell), Paragraph("Spend tier segmentation.", style_table_cell)],
    ]
    t_dict = Table(data_dict, colWidths=[95, 75, 140, 194])
    t_dict.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [light_bg, colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_dict)
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 4: DATA CLEANING & AUDITING PIPELINE
    # =========================================================================
    story.append(Paragraph("4. DATA CLEANING & AUDITING PIPELINE", style_h1))
    story.append(Paragraph("4.1 Ingestion and Structural Integrity Verification", style_h2))
    story.append(Paragraph(
        "Data hygiene is foundational to reliable statistical inference and business reporting. The automated cleaning module implemented in "
        "<code>src/data_cleaning.py</code> executes systematic structural integrity checks upon raw dataset ingestion.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Duplicate Verification:</b> A complete duplicate inspection across all 7,043 rows and 21 attributes confirmed <b>0 duplicate entries</b>. "
        "Every row corresponds to a verified, unique customer account identified by primary key <code>customerID</code>.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 Whitespace Resolution in TotalCharges", style_h2))
    story.append(Paragraph(
        "During initial schema inspection, the continuous attribute <code>TotalCharges</code> was inferred by Pandas as <code>object</code> data type rather than floating-point numeric. "
        "Forensic auditing revealed <b>11 whitespace strings</b> (<code>' '</code>). Further cross-variable inspection established that all 11 instances occur strictly where <code>tenure == 0</code>, representing newly activated subscriber accounts that joined during the current billing cycle and have not yet completed a billing month.",
        style_body
    ))
    story.append(Paragraph(
        "Rather than improperly discarding these rows (which would introduce attrition bias and delete newly acquired accounts), the cleaning pipeline converts the column to <code>float64</code> and imputes <b>$0.00</b> for new accounts. This preserves 100% of customer accounts (7,043 rows) without data loss.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.3 Statistical Outlier Diagnostics (1.5 × IQR Rule)", style_h2))
    story.append(Paragraph(
        "Outlier detection was conducted on all continuous attributes using the standard Interquartile Range (IQR) rule: "
        "<code>Lower Bound = Q1 - 1.5 × IQR</code> and <code>Upper Bound = Q3 + 1.5 × IQR</code>.",
        style_body
    ))

    iqr_data = [
        [Paragraph("<b>Continuous Metric</b>", style_table_head), Paragraph("<b>Q1 (25%)</b>", style_table_head), Paragraph("<b>Q3 (75%)</b>", style_table_head), Paragraph("<b>IQR</b>", style_table_head), Paragraph("<b>Lower Bound</b>", style_table_head), Paragraph("<b>Upper Bound</b>", style_table_head), Paragraph("<b>Outlier Count</b>", style_table_head), Paragraph("<b>Status</b>", style_table_head)],
        [Paragraph("<b>tenure</b>", style_body_bold), Paragraph("9.0 mos", style_table_cell), Paragraph("55.0 mos", style_table_cell), Paragraph("46.0 mos", style_table_cell), Paragraph("-60.0 mos", style_table_cell), Paragraph("124.0 mos", style_table_cell), Paragraph("0 (0.0%)", style_table_cell), Paragraph("Verified Valid", style_table_cell)],
        [Paragraph("<b>MonthlyCharges</b>", style_body_bold), Paragraph("$35.50", style_table_cell), Paragraph("$89.85", style_table_cell), Paragraph("$54.35", style_table_cell), Paragraph("-$46.02", style_table_cell), Paragraph("$171.38", style_table_cell), Paragraph("0 (0.0%)", style_table_cell), Paragraph("Verified Valid", style_table_cell)],
        [Paragraph("<b>TotalCharges</b>", style_body_bold), Paragraph("$398.55", style_table_cell), Paragraph("$3786.60", style_table_cell), Paragraph("$3388.05", style_table_cell), Paragraph("-$4683.52", style_table_cell), Paragraph("$8868.68", style_table_cell), Paragraph("0 (0.0%)", style_table_cell), Paragraph("Verified Valid", style_table_cell)],
    ]
    t_iqr = Table(iqr_data, colWidths=[90, 55, 55, 55, 65, 65, 65, 54])
    t_iqr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [light_bg, colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_iqr)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "As established in the audit table, zero statistical outliers exist within the dataset. Continuous ranges accurately reflect valid commercial subscription tenures (0 to 72 months) and realistic telecommunication billing tariffs ($18.25 to $118.75).",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 5: EXPLORATORY DATA ANALYSIS (EDA) & VISUALIZATIONS
    # =========================================================================
    story.append(Paragraph("5. EXPLORATORY DATA ANALYSIS & VISUALIZATIONS", style_h1))
    story.append(Paragraph("5.1 Univariate Distribution Analysis", style_h2))
    story.append(Paragraph(
        "Exploratory Data Analysis commenced with univariate assessments to establish baseline operational distributions across target and predictor variables.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Customer Churn Baseline:</b> Out of 7,043 accounts, <b>5,174 customers (73.46%)</b> were retained, while <b>1,869 customers (26.54%)</b> defected. "
        "This establishes an industry-standard baseline churn rate of 26.54%.",
        style_body
    ))

    # Embed Figure 1: Pie Chart
    p1 = os.path.join(viz_dir, "01_churn_distribution_pie.png")
    if os.path.exists(p1):
        story.append(Spacer(1, 4))
        story.append(Image(p1, width=320, height=220))
        story.append(Paragraph("<b>Figure 5.1:</b> Overall Customer Churn Distribution (Pie Chart).", style_callout))
        story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Tenure Distribution:</b> Tenure displays a pronounced <b>bimodal distribution</b>. High concentrations appear at 1 month (new subscriber signups experiencing onboarding friction) and at 72 months (a resilient cohort of long-term brand-loyal subscribers). "
        "The overall mean tenure is 32.37 months with a median of 29.00 months.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Monthly Charges Distribution:</b> Recurring charges exhibit a sharp multimodal density. A large peak occurs near $20.00/month corresponding to basic landline phone-only subscriptions. A secondary broad distribution spans $70.00 to $105.00/month, representing multi-service broadband and fiber optic streaming packages.",
        style_body
    ))

    # Embed Figure 2: Contract Bar Chart
    p2 = os.path.join(viz_dir, "02_contract_churn_bar.png")
    if os.path.exists(p2):
        story.append(Spacer(1, 4))
        story.append(Image(p2, width=340, height=210))
        story.append(Paragraph("<b>Figure 5.2:</b> Customer Churn Rate and Volume by Contract Agreement.", style_callout))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Bivariate and Multivariate
    story.append(Paragraph("5.2 Bivariate Churn Cross-Tabulations", style_h2))
    story.append(Paragraph(
        "Bivariate analysis evaluated the empirical relationship between specific operational parameters and customer churn likelihood:",
        style_body
    ))
    story.append(Paragraph(
        "<b>1. Contract Commitment Duration:</b> Month-to-month contracts exhibit an alarming <b>42.71% churn rate</b> (1,655 churned accounts), representing <b>88.55% of all defection</b> across the company. "
        "In stark contrast, customers under One-Year contracts churn at <b>11.27%</b> (73.6% risk reduction), while Two-Year contracts demonstrate near-zero defection at <b>2.83%</b> (93.4% risk reduction).",
        style_body
    ))
    story.append(Paragraph(
        "<b>2. Payment Channel Friction:</b> Customers utilizing <b>Electronic Check</b> suffer an extreme <b>45.29% churn rate</b> (1,071 accounts), comprising 57.30% of total company churn. "
        "Subscribers enrolled in automated clearinghouse channels—Bank Transfer Automatic (16.71% churn) and Credit Card Automatic (15.24% churn)—display nearly two-thirds lower defection.",
        style_body
    ))

    # Embed Figure 6: Payment Methods
    p6 = os.path.join(viz_dir, "06_payment_methods_churn_bar.png")
    if os.path.exists(p6):
        story.append(Spacer(1, 4))
        story.append(Image(p6, width=340, height=200))
        story.append(Paragraph("<b>Figure 5.3:</b> Churn Rates across Billing Remittance Channels.", style_callout))
        story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>3. Broadband Technology:</b> Subscribers with <b>Fiber Optic</b> internet display an elevated churn rate of <b>41.89%</b> (1,297 churned accounts) despite generating the highest average monthly spend ($91.50). "
        "Subscribers with traditional DSL broadband churn at only 18.96%, and customers without internet service churn at 7.40%.",
        style_body
    ))

    # Embed Figure 5: Correlation Heatmap
    p5 = os.path.join(viz_dir, "05_correlation_heatmap.png")
    if os.path.exists(p5):
        story.append(Spacer(1, 4))
        story.append(Image(p5, width=340, height=210))
        story.append(Paragraph("<b>Figure 5.4:</b> Numerical Attribute Pearson Correlation Heatmap.", style_callout))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 6: INFERENTIAL STATISTICAL ANALYSIS & HYPOTHESIS TESTING
    # =========================================================================
    story.append(Paragraph("6. INFERENTIAL STATISTICAL ANALYSIS & HYPOTHESIS TESTING", style_h1))
    story.append(Paragraph("6.1 Parametric & Non-Parametric Summary Statistics", style_h2))
    story.append(Paragraph(
        "Descriptive statistics were computed across all continuous variables to quantify location, dispersion, and distributional shape:",
        style_body
    ))

    summary_stats_table = [
        [Paragraph("<b>Metric</b>", style_table_head), Paragraph("<b>Mean</b>", style_table_head), Paragraph("<b>Median</b>", style_table_head), Paragraph("<b>Mode</b>", style_table_head), Paragraph("<b>Std Dev</b>", style_table_head), Paragraph("<b>Min</b>", style_table_head), Paragraph("<b>Q1 (25%)</b>", style_table_head), Paragraph("<b>Q3 (75%)</b>", style_table_head), Paragraph("<b>Max</b>", style_table_head), Paragraph("<b>IQR</b>", style_table_head), Paragraph("<b>Skewness</b>", style_table_head), Paragraph("<b>Kurtosis</b>", style_table_head)],
        [Paragraph("<b>tenure</b>", style_body_bold), Paragraph("32.37", style_table_cell), Paragraph("29.00", style_table_cell), Paragraph("1.00", style_table_cell), Paragraph("24.56", style_table_cell), Paragraph("0.00", style_table_cell), Paragraph("9.00", style_table_cell), Paragraph("55.00", style_table_cell), Paragraph("72.00", style_table_cell), Paragraph("46.00", style_table_cell), Paragraph("+0.240", style_table_cell), Paragraph("-1.387", style_table_cell)],
        [Paragraph("<b>MonthlyCharges</b>", style_body_bold), Paragraph("64.76", style_table_cell), Paragraph("70.35", style_table_cell), Paragraph("20.05", style_table_cell), Paragraph("30.09", style_table_cell), Paragraph("18.25", style_table_cell), Paragraph("35.50", style_table_cell), Paragraph("89.85", style_table_cell), Paragraph("118.75", style_table_cell), Paragraph("54.35", style_table_cell), Paragraph("-0.221", style_table_cell), Paragraph("-1.257", style_table_cell)],
        [Paragraph("<b>TotalCharges</b>", style_body_bold), Paragraph("2279.73", style_table_cell), Paragraph("1394.55", style_table_cell), Paragraph("0.00", style_table_cell), Paragraph("2266.79", style_table_cell), Paragraph("0.00", style_table_cell), Paragraph("398.55", style_table_cell), Paragraph("3786.60", style_table_cell), Paragraph("8684.80", style_table_cell), Paragraph("3388.05", style_table_cell), Paragraph("+0.963", style_table_cell), Paragraph("-0.229", style_table_cell)],
    ]
    t_sum = Table(summary_stats_table, colWidths=[70, 36, 36, 36, 40, 32, 38, 42, 42, 38, 42, 42])
    t_sum.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [light_bg, colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6.2 Pearson Chi-Square Tests of Independence (χ²) & Cramér's V", style_h2))
    story.append(Paragraph(
        "To rigorously determine whether categorical attributes are statistically associated with customer churn, Pearson's Chi-Square Test of Independence was executed. "
        "The effect size was quantified using Cramér's V, defined as: <code>V = sqrt(χ² / (n × min(r-1, c-1)))</code>.",
        style_body
    ))

    chi_table = [
        [Paragraph("<b>Feature Evaluated</b>", style_table_head), Paragraph("<b>χ² Stat</b>", style_table_head), Paragraph("<b>p-value</b>", style_table_head), Paragraph("<b>df</b>", style_table_head), Paragraph("<b>Cramér's V</b>", style_table_head), Paragraph("<b>Association Strength</b>", style_table_head), Paragraph("<b>Statistical Conclusion</b>", style_table_head)],
        [Paragraph("<b>Contract</b>", style_body_bold), Paragraph("1184.60", style_table_cell), Paragraph("< 10^-250", style_table_cell), Paragraph("2", style_table_cell), Paragraph("0.410", style_table_cell), Paragraph("Strong Association", style_table_cell), Paragraph("Statistically Significant (p < 0.001)", style_table_cell)],
        [Paragraph("<b>OnlineSecurity</b>", style_body_bold), Paragraph("850.00", style_table_cell), Paragraph("< 10^-180", style_table_cell), Paragraph("2", style_table_cell), Paragraph("0.347", style_table_cell), Paragraph("Moderate Association", style_table_cell), Paragraph("Statistically Significant (p < 0.001)", style_table_cell)],
        [Paragraph("<b>TechSupport</b>", style_body_bold), Paragraph("828.20", style_table_cell), Paragraph("< 10^-180", style_table_cell), Paragraph("2", style_table_cell), Paragraph("0.343", style_table_cell), Paragraph("Moderate Association", style_table_cell), Paragraph("Statistically Significant (p < 0.001)", style_table_cell)],
        [Paragraph("<b>InternetService</b>", style_body_bold), Paragraph("732.31", style_table_cell), Paragraph("< 10^-150", style_table_cell), Paragraph("2", style_table_cell), Paragraph("0.322", style_table_cell), Paragraph("Moderate Association", style_table_cell), Paragraph("Statistically Significant (p < 0.001)", style_table_cell)],
        [Paragraph("<b>PaymentMethod</b>", style_body_bold), Paragraph("648.14", style_table_cell), Paragraph("< 10^-140", style_table_cell), Paragraph("3", style_table_cell), Paragraph("0.303", style_table_cell), Paragraph("Moderate Association", style_table_cell), Paragraph("Statistically Significant (p < 0.001)", style_table_cell)],
        [Paragraph("<b>PaperlessBilling</b>", style_body_bold), Paragraph("258.28", style_table_cell), Paragraph("< 10^-50", style_table_cell), Paragraph("1", style_table_cell), Paragraph("0.192", style_table_cell), Paragraph("Weak Association", style_table_cell), Paragraph("Statistically Significant (p < 0.001)", style_table_cell)],
        [Paragraph("<b>gender</b>", style_body_bold), Paragraph("0.48", style_table_cell), Paragraph("0.487", style_table_cell), Paragraph("1", style_table_cell), Paragraph("0.008", style_table_cell), Paragraph("Negligible Association", style_table_cell), Paragraph("<b>NOT Significant (p = 0.487)</b>", style_table_cell)],
    ]
    t_chi = Table(chi_table, colWidths=[90, 55, 60, 25, 60, 100, 114])
    t_chi.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [light_bg, colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_chi)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.3 Welch's Two-Sample Independent T-Tests", style_h2))
    story.append(Paragraph(
        "To test whether difference in continuous metrics between churned and retained accounts is statistically significant without assuming equal variance, Welch's t-test was conducted:",
        style_body
    ))
    story.append(Paragraph(
        "<b>1. Customer Tenure Disparity:</b> Churned subscribers stay an average of <b>17.98 months</b> (std = 19.53) compared to <b>37.57 months</b> (std = 24.11) for retained accounts. "
        "The difference (-19.59 months) is highly significant: <code>t = -34.82, p = 1.34 × 10^-233</code>, Cohen's d = -0.852 (large effect size).",
        style_body
    ))
    story.append(Paragraph(
        "<b>2. Monthly Charges Premium:</b> Churned customers paid an average of <b>$74.44/month</b> compared to <b>$61.27/month</b> for retained accounts. "
        "The price premium (+$13.18/month) is statistically significant: <code>t = +18.41, p = 8.59 × 10^-73</code>, Cohen's d = +0.471 (moderate effect size).",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 7: RELATIONAL SQL BUSINESS ANALYSIS
    # =========================================================================
    story.append(Paragraph("7. RELATIONAL SQL BUSINESS ANALYSIS", style_h1))
    story.append(Paragraph("7.1 Relational Schema & SQLite Storage Architecture", style_h2))
    story.append(Paragraph(
        "In accordance with enterprise business intelligence standards, cleaned customer accounts were loaded into a relational SQLite database (<code>database/customer_churn.db</code>) under table <code>customers</code>. "
        "B-tree database indices were created on primary filtering and aggregation columns: <code>customerID</code>, <code>Contract</code>, <code>InternetService</code>, <code>PaymentMethod</code>, <code>tenure</code>, and <code>Churn</code>.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.2 Ten Executive SQL Business Queries & Results", style_h2))

    sql_items = [
        ("Query 1: Total Customer Base Size",
         "SELECT COUNT(*) AS total_customers FROM customers;",
         "Total Customers = 7,043 unique active subscriber accounts."),
        ("Query 2: Total Defected Churn Volume",
         "SELECT COUNT(*) AS churned_customers FROM customers WHERE Churn = 'Yes';",
         "Churned Customers = 1,869 customer accounts."),
        ("Query 3: Overall Enterprise Churn Percentage",
         "SELECT ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS churn_pct FROM customers;",
         "Overall Churn Rate = 26.54%."),
        ("Query 4: Highest Churn Contract Agreement",
         "SELECT Contract, COUNT(*) AS total, SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned, ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS rate FROM customers GROUP BY Contract ORDER BY rate DESC;",
         "Month-to-month contracts exhibit 42.71% churn (1,655 accounts), One-year contracts 11.27% (166 accounts), Two-year contracts 2.83% (48 accounts)."),
        ("Query 5: Most Churned Payment Method",
         "SELECT PaymentMethod, COUNT(*) AS total, SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned FROM customers GROUP BY PaymentMethod ORDER BY churned DESC;",
         "Electronic Check accounts for 1,071 churned customers (45.29% churn rate), Mailed Check 308 (19.07%), Bank Transfer 258 (16.71%), Credit Card 232 (15.24%)."),
        ("Query 6: Average Monthly Charges (ARPU) by Churn Outcome",
         "SELECT ROUND(AVG(MonthlyCharges), 2) AS avg_overall, ROUND(AVG(CASE WHEN Churn = 'Yes' THEN MonthlyCharges END), 2) AS avg_churned, ROUND(AVG(CASE WHEN Churn = 'No' THEN MonthlyCharges END), 2) AS avg_retained FROM customers;",
         "Overall ARPU = $64.76. Churned customers averaged $74.44/month vs $61.27/month for retained customers (+$13.18/mo premium)."),
        ("Query 7: Internet Service Churn Vulnerability",
         "SELECT InternetService, ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS rate FROM customers GROUP BY InternetService ORDER BY rate DESC;",
         "Fiber Optic = 41.89% churn rate, DSL Broadband = 18.96%, No Internet Service = 7.40%."),
        ("Query 8: Average Subscription Tenure by Churn Status",
         "SELECT Churn, ROUND(AVG(tenure), 2) AS avg_tenure FROM customers GROUP BY Churn;",
         "Churned subscribers average 17.98 months vs 37.57 months for retained subscribers (19.59 month difference)."),
        ("Query 9: Top Monthly Recurring Revenue Customer Segment",
         "SELECT Contract, InternetService, ROUND(SUM(MonthlyCharges), 2) AS total_mrr FROM customers GROUP BY Contract, InternetService ORDER BY total_mrr DESC LIMIT 3;",
         "Month-to-month Fiber Optic customers generate $180,693.30 in monthly revenue, representing the single largest revenue block."),
        ("Query 10: Volume of Month-to-Month Subscribers",
         "SELECT Contract, COUNT(*) AS total, ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM customers) * 100, 2) AS pct FROM customers WHERE Contract = 'Month-to-month' GROUP BY Contract;",
         "Month-to-month accounts comprise 3,875 customers (55.02% of entire customer base).")
    ]

    for title, q_sql, q_res in sql_items:
        story.append(Paragraph(f"<b>{title}</b>", style_h3))
        story.append(Paragraph(f"<code>{q_sql}</code>", style_code))
        story.append(Paragraph(f"<b>Result & Interpretation:</b> {q_res}", style_body))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 8: BUSINESS INTELLIGENCE DASHBOARD IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("8. BUSINESS INTELLIGENCE DASHBOARD IMPLEMENTATION", style_h1))
    story.append(Paragraph("8.1 User Interface Architecture & SaaS Design System", style_h2))
    story.append(Paragraph(
        "To deliver actionable data visibility to non-technical executive stakeholders, an interactive Business Intelligence application was constructed using <b>Streamlit</b> and <b>Plotly</b> (<code>app/streamlit_app.py</code>). "
        "The design adheres strictly to enterprise SaaS analytics standards, featuring a deep obsidian and navy aesthetic (<code>#080E1A</code>), rounded card containers (<code>#0D1527</code>), subtle slate borders (<code>#1E293B</code>), and vibrant cyan/blue glowing accents.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.2 Reactive Global Filter Engine & Component Layout", style_h2))
    story.append(Paragraph(
        "The dashboard implements a streamlined horizontal top filter bar that dynamically cascades across all visual components and metrics in real time. "
        "Global parameters include Gender, Contract Agreement, Internet Service Delivery, Payment Method, and Customer Tenure Cohorts. "
        "Whenever a filter is modified, all 6 KPI cards, cross-tabulations, Plotly visuals, and SQL query results update reactively.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.3 Multi-Page Module Specifications", style_h2))
    story.append(Paragraph("The platform organizes analysis across 9 dedicated operational pages:", style_body))

    pages_summary = [
        ("1. Executive Overview", "Displays 6 executive KPI cards, churn donut with central count, contract bar chart, monthly revenue spline trend, tenure distribution, payment churn bars, and key business observations."),
        ("2. Customer Data Explorer", "Provides real-time customer search by ID, comprehensive 25-feature data dictionary, and one-click filtered CSV exports."),
        ("3. Data Quality Report", "Documents automated duplicate checks, whitespace resolution audit, and 1.5×IQR outlier boundaries."),
        ("4. Exploratory Data Analysis", "Features interactive tabs for univariate frequency distributions, bivariate churn cross-tabulations, and multivariate scatter/box interactions."),
        ("5. Statistical Insights", "Presents parametric summary tables, Chi-Square independence tests with Cramér's V ranking, and Welch's two-sample t-tests with business interpretations."),
        ("6. SQL Analytics", "Displays all 10 core business queries, resulting tables, and an interactive live SQL sandbox for custom query execution."),
        ("7. Customer Segmentation", "Maps customer lifecycle cohorts, renders 2D Tenure × Monthly Spend vulnerability grids, and highlights critical danger zone accounts."),
        ("8. Business Recommendations", "Details the Four-Pillar Strategic Framework and provides an interactive Customer Retention Financial ROI Calculator."),
        ("9. Project Information", "Presents system technical architecture, repository structure, team member attribution cards, and Kaggle dataset citations.")
    ]
    for p_name, p_desc in pages_summary:
        story.append(Paragraph(f"<b>• {p_name}:</b> {p_desc}", style_body))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 9: STRATEGIC BUSINESS RECOMMENDATIONS & FINANCIAL ROI
    # =========================================================================
    story.append(Paragraph("9. STRATEGIC BUSINESS RECOMMENDATIONS & FINANCIAL ROI", style_h1))
    story.append(Paragraph("9.1 Four-Pillar Retention Framework", style_h2))
    story.append(Paragraph(
        "Based on audited statistical findings, four high-impact operational interventions were formulated:",
        style_body
    ))

    recs = [
        ("Pillar 1: Annual Contract Term Transition Program",
         "Observed Finding: Month-to-month contracts experience a 42.71% churn rate, driving 88.55% of all defection.<br/>"
         "Supporting Statistic: Two-year commitments exhibit only 2.83% churn (a 93.4% relative defection reduction).<br/>"
         "Business Impact: High revenue volatility and continual account turnover costs.<br/>"
         "Strategic Action: Introduce a $10.00/month statement credit or broadband speed tier upgrade at Month 3 in exchange for signing an annual service commitment."),
        ("Pillar 2: Auto-Pay Billing Optimization & Electronic Check Migration",
         "Observed Finding: Electronic Check users suffer a 45.29% churn rate, nearly triple that of automated methods.<br/>"
         "Supporting Statistic: Over 57.30% of all defected customers (1,071 accounts) remit payment via Electronic Check.<br/>"
         "Business Impact: Manual payment workflows require monthly conscious evaluation of invoice value, increasing payment friction.<br/>"
         "Strategic Action: Provide a $5.00/month recurring discount for enrolling in Credit Card or Bank Auto-Pay."),
        ("Pillar 3: The First 90 Days Customer Onboarding Journey",
         "Observed Finding: 55.5% of total defection occurs in the first 12 months; median tenure of churned customers is only 10 months.<br/>"
         "Supporting Statistic: 0-12 month cohort churns at 47.44%, while 49-72 month accounts churn at only 9.38%.<br/>"
         "Business Impact: Acquisition expenditures are lost before accounts achieve customer lifetime payback.<br/>"
         "Strategic Action: Implement an automated customer success cadence: Day 7 installation verification check, Day 30 initial bill walkthrough, and Day 60 speed optimization audit."),
        ("Pillar 4: High-Speed Fiber Optic Technical Support Bundling",
         "Observed Finding: Fiber Optic customers churn at 41.89% ($91.50/month ARPU), but churn plummets to 11.84% when accounts include both Tech Support and Online Security.<br/>"
         "Supporting Statistic: Accounts with Tech Support churn at 15.17% vs 41.64% for accounts lacking support.<br/>"
         "Business Impact: Protects high-ARPU subscriptions from defecting due to unresolved technical friction.<br/>"
         "Strategic Action: Automatically bundle complimentary 24/7 Priority Tech Support and Online Security into all Fiber Optic packages.")
    ]
    for r_title, r_body in recs:
        story.append(Paragraph(f"<b>{r_title}</b>", style_h3))
        story.append(Paragraph(r_body, style_body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))
    story.append(Paragraph("9.2 Financial ROI Modeling & Revenue Safeguards", style_h2))
    story.append(Paragraph(
        "Utilizing the built-in Retention Financial ROI Simulator, financial returns were projected across graduated churn reduction milestones. "
        "The model evaluates the baseline 7,043 subscriber accounts with an average churned monthly bill of $74.44:",
        style_body
    ))

    roi_data = [
        [Paragraph("<b>Target Churn Reduction</b>", style_table_head), Paragraph("<b>Accounts Preserved</b>", style_table_head), Paragraph("<b>New Corporate Churn Rate</b>", style_table_head), Paragraph("<b>Monthly Revenue Preserved</b>", style_table_head), Paragraph("<b>Annual Revenue Protected</b>", style_table_head)],
        [Paragraph("<b>-1.0% (Conservative)</b>", style_body_bold), Paragraph("70 Accounts", style_table_cell), Paragraph("25.54%", style_table_cell), Paragraph("$5,210.80 / mo", style_table_cell), Paragraph("<b>$62,529.60 / yr</b>", style_body_bold)],
        [Paragraph("<b>-2.0% (Moderate)</b>", style_body_bold), Paragraph("141 Accounts", style_table_cell), Paragraph("24.54%", style_table_cell), Paragraph("$10,496.04 / mo", style_table_cell), Paragraph("<b>$125,952.48 / yr</b>", style_body_bold)],
        [Paragraph("<b>-3.0% (Target Goal)</b>", style_body_bold), Paragraph("211 Accounts", style_table_cell), Paragraph("23.54%", style_table_cell), Paragraph("$15,706.84 / mo", style_table_cell), Paragraph("<b>$188,482.08 / yr</b>", style_body_bold)],
        [Paragraph("<b>-5.0% (Aggressive)</b>", style_body_bold), Paragraph("352 Accounts", style_table_cell), Paragraph("21.54%", style_table_cell), Paragraph("$26,202.88 / mo", style_table_cell), Paragraph("<b>$314,434.56 / yr</b>", style_body_bold)],
        [Paragraph("<b>-8.0% (Optimistic)</b>", style_body_bold), Paragraph("563 Accounts", style_table_cell), Paragraph("18.54%", style_table_cell), Paragraph("$41,909.72 / mo", style_table_cell), Paragraph("<b>$502,916.64 / yr</b>", style_body_bold)],
    ]
    t_roi = Table(roi_data, colWidths=[100, 85, 95, 105, 119])
    t_roi.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, border_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [light_bg, colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_roi)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Achieving a realistic 5.0% percentage point reduction in churn preserves 352 high-value accounts, delivering over <b>$314,000 in protected annual recurring revenue</b>.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 10: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("10. CONCLUSION & FUTURE SCOPE", style_h1))
    story.append(Paragraph("10.1 Conclusion", style_h2))
    story.append(Paragraph(
        "This project conclusively demonstrates that pure Data Science, empirical Exploratory Data Analysis, inferential statistics, relational SQL querying, and modern Business Intelligence dashboards provide a superior, fully transparent alternative to complex Machine Learning models for telecommunications customer churn analysis.",
        style_body
    ))
    story.append(Paragraph(
        "By systematically evaluating 7,043 customer accounts from the IBM Telco dataset, the investigation isolated the genuine operational determinants of churn: month-to-month contracts (42.71% churn, 88.55% of all defection), electronic check payment friction (45.29% churn), first-year onboarding vulnerability (55.5% of churn occurring in months 0-12), and unbundled fiber optic price elasticity. "
        "The resulting SaaS dashboard empowers business leaders to track real-time retention KPIs, execute custom SQL queries, and simulate quantifiable financial ROI.",
        style_body
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("10.2 Future Scope & Enhancements", style_h2))
    story.append(Paragraph("Potential extensions for enterprise deployment include:", style_body))
    story.append(Paragraph("<b>1. Automated Real-Time Data Pipeline Connectors:</b> Integrating Apache Airflow and dbt pipelines to ingest live billing records from enterprise data warehouses (Snowflake, BigQuery, AWS Redshift).", style_body))
    story.append(Paragraph("<b>2. Longitudinal Cohort Survival Analysis:</b> Implementing non-parametric Kaplan-Meier survival curves and Cox proportional hazards regression to model subscriber attrition hazard over multi-year periods.", style_body))
    story.append(Paragraph("<b>3. Automated Executive Briefing Reports:</b> Generating scheduled weekly PDF executive digests and Slack/Teams alerts when high-value danger zone accounts exhibit early defection signals.", style_body))
    story.append(Paragraph("<b>4. Multi-Tenant Role-Based Access Control (RBAC):</b> Adding authentication tiers for customer success agents, regional managers, and C-suite leadership.", style_body))
    story.append(Spacer(1, 14))

    # =========================================================================
    # REFERENCES
    # =========================================================================
    story.append(Paragraph("REFERENCES", style_h1))
    story.append(Spacer(1, 6))

    refs = [
        "1. IBM Corporation. 'Telco Customer Churn Dataset.' Distributed by BlastChar on Kaggle, 2018. URL: https://www.kaggle.com/datasets/blastchar/telco-customer-churn",
        "2. Reichheld, Frederick F., and W. Earl Sasser Jr. 'Zero Defections: Quality Comes to Services.' Harvard Business Review, vol. 68, no. 5, 1990, pp. 105-111.",
        "3. Agresti, Alan. 'Categorical Data Analysis.' 3rd ed., John Wiley & Sons, 2013.",
        "4. Welch, Bernard L. 'The Generalization of 'Student's' Problem when Several Different Population Variances are Involved.' Biometrika, vol. 34, no. 1/2, 1947, pp. 28-35.",
        "5. Cramér, Harald. 'Mathematical Methods of Statistics.' Princeton University Press, 1946.",
        "6. McKinney, Wes. 'Data Structures for Statistical Computing in Python.' Proceedings of the 9th Python in Science Conference, 2010, pp. 56-61.",
        "7. Plotly Technologies Inc. 'Collaborative Data Science.' Plotly, 2015. URL: https://plotly.com",
        "8. Streamlit Inc. 'The fastest way to build and share data apps.' Streamlit Documentation, 2024. URL: https://docs.streamlit.io"
    ]
    for r in refs:
        story.append(Paragraph(r, style_body))

    story.append(PageBreak())

    # =========================================================================
    # APPENDIX: SOURCE CODE LISTINGS & SETUP
    # =========================================================================
    story.append(Paragraph("APPENDIX: SOURCE CODE LISTINGS & SETUP", style_h1))
    story.append(Paragraph("A.1 Project Repository File Layout", style_h2))
    story.append(Paragraph(
        "<code>customer-churn-analysis/</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>data/processed/telco_churn_cleaned.csv</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>database/customer_churn.db</code> (SQLite Relational DB)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>src/data_cleaning.py</code> (Audit, Type Conversion, Outliers)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>src/descriptive_statistics.py</code> (Chi-Square, Welch's t-test)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>src/eda.py</code> (Static 300 DPI Charts & Plotly Visuals)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>src/sql_analysis.py</code> (SQLite Relational Queries)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>app/streamlit_app.py</code> (9-Page Interactive Dashboard)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>notebooks/exploratory_analysis.ipynb</code> (Step-by-step EDA)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;├── <code>reports/Summer_Internship_Report_Customer_Churn.pdf</code> (This Document)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;└── <code>requirements.txt</code>",
        style_code
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("A.2 Execution Commands (Windows PowerShell)", style_h2))
    story.append(Paragraph(
        "<code># Navigate to Project Root Directory<br/>"
        "cd 'c:\\Users\\KONDAMADUGU ASHWITH\\Downloads\\intern\\customer-churn-analysis'<br/><br/>"
        "# Execute End-to-End Analytics Pipeline<br/>"
        "python src/data_cleaning.py<br/>"
        "python src/descriptive_statistics.py<br/>"
        "python src/sql_analysis.py<br/>"
        "python src/eda.py<br/><br/>"
        "# Launch Streamlit Executive BI Dashboard<br/>"
        "python -m streamlit run app/streamlit_app.py</code>",
        style_code
    ))

    # Build Document using NumberedCanvas for Running Headers & Footers
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Academic Internship Report generated successfully: {output_pdf_path}")


if __name__ == "__main__":
    base_path = Path(__file__).resolve().parent.parent
    out_pdf = base_path / "reports" / "Summer_Internship_Report_Customer_Churn.pdf"
    v_dir = base_path / "visualizations"
    build_pdf_report(str(out_pdf), str(v_dir))
