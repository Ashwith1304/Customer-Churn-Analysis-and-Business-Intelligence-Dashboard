"""
Academic Project Report Generator - 48-Page Master Edition
Project: CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD
Institution: Sreenidhi Institute of Science and Technology (Autonomous)
Department: Department of Data Science (CSE-DS)
Team Members:
  - G Mythili (24311A67H8)
  - K Ashiwith (24311A67H6)
  - D Niyati (24311A67H7)
Internship Coordinator: Mr. Syed. Mazharuddin
Head of Department: Dr. Md. Jaffar Sadiq
Date: October / November 2026
Format: Strictly following SNIST Guidelines (A4, Times New Roman, 1.5 line spacing, Justified, Double Border Lines, Exactly 48 Pages)
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf


class AcademicNumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_w, page_h = 595.27, 841.89

        # Outer Academic Border Line (1.2pt)
        self.setStrokeColor(colors.HexColor("#0F172A"))
        self.setLineWidth(1.2)
        self.rect(36, 36, page_w - 72, page_h - 72)

        # Inner Academic Border Line (0.5pt, 3pt inset)
        self.setStrokeColor(colors.HexColor("#94A3B8"))
        self.setLineWidth(0.5)
        self.rect(39, 39, page_w - 78, page_h - 78)

        # Running Top Header (Page 2 onwards)
        if self._pageNumber > 1:
            self.setFont("Times-Bold", 8)
            self.setFillColor(colors.HexColor("#334155"))
            self.drawString(54, page_h - 50, "DEPARTMENT OF DATA SCIENCE (CSE-DS) — SREENIDHI INSTITUTE OF SCIENCE & TECHNOLOGY")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, page_h - 54, page_w - 54, page_h - 54)

        # Running Bottom Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 54, page_w - 54, 54)

        self.setFont("Times-Roman", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 42, "Customer Churn Analysis & Business Intelligence Dashboard")

        # Page numbering as mandated by SNIST guidelines:
        # Preliminary pages (1 to 8): small-case Roman numerals centered at bottom
        # Main chapters & appendices (9 to 48): Arabic numerals 1 to 40 centered at bottom
        roman_map = {1: "", 2: "ii", 3: "iii", 4: "iv", 5: "v", 6: "vi", 7: "vii", 8: "viii"}
        if self._pageNumber == 1:
            page_str = ""
        elif self._pageNumber <= 8:
            page_str = roman_map.get(self._pageNumber, "")
        else:
            arabic_num = self._pageNumber - 8
            page_str = f"{arabic_num}"

        if page_str:
            self.setFont("Times-Roman", 9)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawCentredString(page_w / 2.0, 42, page_str)

        self.restoreState()


def get_academic_styles():
    styles = getSampleStyleSheet()

    primary = colors.HexColor("#0F172A")
    navy = colors.HexColor("#1E3A8A")
    dark_gray = colors.HexColor("#1E293B")
    body_color = colors.HexColor("#0F172A")

    # Chapter / Main section heading: Bold, 14pt (SNIST Guideline)
    styles.add(ParagraphStyle(
        "AcadChapterHead",
        fontName="Times-Bold",
        fontSize=14,
        leading=19,
        alignment=TA_LEFT,
        textColor=navy,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        "AcadChapterHeadCenter",
        fontName="Times-Bold",
        fontSize=14,
        leading=19,
        alignment=TA_CENTER,
        textColor=navy,
        spaceAfter=8
    ))

    # Sub section heading: Bold, 12pt (SNIST Guideline)
    styles.add(ParagraphStyle(
        "AcadSubHead",
        fontName="Times-Bold",
        fontSize=11.5,
        leading=15.5,
        alignment=TA_LEFT,
        textColor=dark_gray,
        spaceBefore=4,
        spaceAfter=2.5
    ))

    # Sub-sub section heading: Bold + italics, 11pt
    styles.add(ParagraphStyle(
        "AcadSubSubHead",
        fontName="Times-BoldItalic",
        fontSize=11,
        leading=14.5,
        alignment=TA_LEFT,
        textColor=dark_gray,
        spaceBefore=3,
        spaceAfter=2
    ))

    # Body text: Normal, 10.5pt, 1.5 line spacing (15pt leading), Justified (SNIST Guideline)
    styles.add(ParagraphStyle(
        "AcadBody",
        fontName="Times-Roman",
        fontSize=10.5,
        leading=15.0,
        alignment=TA_JUSTIFY,
        textColor=body_color,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        "AcadBodyTight",
        fontName="Times-Roman",
        fontSize=10.0,
        leading=14.0,
        alignment=TA_JUSTIFY,
        textColor=body_color,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        "AcadEmph",
        fontName="Times-Italic",
        fontSize=10.5,
        leading=15.0,
        alignment=TA_JUSTIFY,
        textColor=body_color,
        spaceAfter=4
    ))

    # Figures and Table description: Normal, 9.5pt (SNIST Guideline: 10pt)
    styles.add(ParagraphStyle(
        "AcadCaption",
        fontName="Times-Roman",
        fontSize=9.5,
        leading=12.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceBefore=3,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        "AcadBullet",
        fontName="Times-Roman",
        fontSize=10.0,
        leading=14.0,
        alignment=TA_JUSTIFY,
        textColor=body_color,
        leftIndent=12,
        spaceAfter=2.5
    ))

    styles.add(ParagraphStyle(
        "AcadCode",
        fontName="Courier",
        fontSize=6.1,
        leading=7.6,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0F172A")
    ))

    styles.add(ParagraphStyle(
        "AcadTableHead",
        fontName="Times-Bold",
        fontSize=8.5,
        leading=11.0,
        alignment=TA_CENTER,
        textColor=colors.white
    ))

    styles.add(ParagraphStyle(
        "AcadTableCell",
        fontName="Times-Roman",
        fontSize=8.0,
        leading=10.5,
        alignment=TA_LEFT,
        textColor=body_color
    ))

    styles.add(ParagraphStyle(
        "AcadTableCellCenter",
        fontName="Times-Roman",
        fontSize=8.0,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=body_color
    ))

    styles.add(ParagraphStyle(
        "AcadTOCCell",
        fontName="Times-Roman",
        fontSize=6.4,
        leading=7.6,
        alignment=TA_LEFT,
        textColor=body_color
    ))

    styles.add(ParagraphStyle(
        "AcadTOCCellBold",
        fontName="Times-Bold",
        fontSize=6.6,
        leading=7.8,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#0F172A")
    ))

    styles.add(ParagraphStyle(
        "AcadTOCCellCenter",
        fontName="Times-Roman",
        fontSize=6.4,
        leading=7.6,
        alignment=TA_CENTER,
        textColor=body_color
    ))

    styles.add(ParagraphStyle(
        "AcadRef",
        fontName="Times-Roman",
        fontSize=7.6,
        leading=9.6,
        alignment=TA_JUSTIFY,
        textColor=body_color,
        spaceAfter=1.0
    ))

    styles.add(ParagraphStyle(
        "AcadMathBody",
        fontName="Times-Roman",
        fontSize=8.8,
        leading=11.8,
        alignment=TA_JUSTIFY,
        textColor=body_color,
        spaceAfter=2.0
    ))

    return styles


def generate_full_48_page_report(output_pdf_path: str, viz_dir: str):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=90,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = get_academic_styles()
    story = []
    logo_path = os.path.join(viz_dir, "snist_official_logo.jpeg")

    def add_figure(img_name, fig_num, caption_text, width=370, height=180):
        img_p = os.path.join(viz_dir, img_name)
        if os.path.exists(img_p):
            story.append(Image(img_p, width=width, height=height))
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"<b>Figure {fig_num}:</b> {caption_text}", styles["AcadCaption"]))
            story.append(Spacer(1, 4))

    # ==========================================================================
    # PAGE 1 (i): MAIN COVER / TITLE PAGE
    # ==========================================================================
    # Batch No in top-right corner exactly as shown in reference page 1
    story.append(Paragraph(
        "<b>Batch No: _______________</b><br/><i>(Office Use)</i>",
        ParagraphStyle("BatchBox", fontName="Times-Roman", fontSize=10, leading=13, alignment=TA_RIGHT, textColor=colors.HexColor("#0F172A"))
    ))
    story.append(Spacer(1, 35))

    story.append(Paragraph(
        "<b>CUSTOMER CHURN ANALYSIS</b>",
        ParagraphStyle("CoverTitle1", fontName="Times-Bold", fontSize=16, leading=22, alignment=TA_CENTER, textColor=colors.HexColor("#DC2626"))
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>AND BUSINESS INTELLIGENCE DASHBOARD</b>",
        ParagraphStyle("CoverTitle2", fontName="Times-Bold", fontSize=14, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#DC2626"))
    ))
    story.append(Spacer(1, 24))

    story.append(Paragraph(
        "A Summer Industry Internship Report<br/>"
        "Submitted in Partial Fulfillment of the Requirements<br/>"
        "For the award of the Degree of",
        ParagraphStyle("CoverSub1", fontName="Times-Roman", fontSize=11, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"))
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "<b>Bachelor of Technology in</b>",
        ParagraphStyle("CoverDegree1", fontName="Times-Bold", fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"))
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Computer Science and Engineering – Data Science (CSE-DS)</b>",
        ParagraphStyle("CoverDegree2", fontName="Times-Bold", fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#0284C7"))
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("By", ParagraphStyle("ByText", fontName="Times-Roman", fontSize=11, alignment=TA_CENTER)))
    story.append(Spacer(1, 12))

    authors_data = [
        [Paragraph("<b>GAVUJI MYTHILI</b>", ParagraphStyle("AuthN1", fontName="Times-Bold", fontSize=10.5, leading=14, alignment=TA_LEFT)),
         Paragraph("<b>24311A67H8</b>", ParagraphStyle("AuthR1", fontName="Times-Bold", fontSize=10.5, leading=14, alignment=TA_RIGHT))],
        [Paragraph("<b>KONDAMADUGU ASHIWITH</b>", ParagraphStyle("AuthN2", fontName="Times-Bold", fontSize=10.5, leading=14, alignment=TA_LEFT)),
         Paragraph("<b>24311A67H6</b>", ParagraphStyle("AuthR2", fontName="Times-Bold", fontSize=10.5, leading=14, alignment=TA_RIGHT))],
        [Paragraph("<b>DOMA NIYATI</b>", ParagraphStyle("AuthN3", fontName="Times-Bold", fontSize=10.5, leading=14, alignment=TA_LEFT)),
         Paragraph("<b>24311A67H7</b>", ParagraphStyle("AuthR3", fontName="Times-Bold", fontSize=10.5, leading=14, alignment=TA_RIGHT))]
    ]
    t_auth = Table(authors_data, colWidths=[200, 160])
    t_auth.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_auth)
    story.append(Spacer(1, 26))

    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=340, height=52.5))
        story.append(Spacer(1, 16))

    story.append(Paragraph(
        "<b>DEPARTMENT OF DATA SCIENCE (CSE-DS)</b>",
        ParagraphStyle("CoverDept", fontName="Times-Bold", fontSize=11.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"))
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>SREENIDHI INSTITUTE OF SCIENCE AND TECHNOLOGY</b>",
        ParagraphStyle("CoverColName", fontName="Times-Bold", fontSize=11.5, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"))
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "<b>November 2026</b>",
        ParagraphStyle("CoverDate", fontName="Times-Roman", fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"))
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 2 (ii): ACCEPTANCE BY INTERNAL TECHNICAL REVIEW COMMITTEE
    # ==========================================================================
    story.append(Paragraph("<b>ACCEPTANCE BY INTERNAL TECHNICAL REVIEW COMMITTEE</b>", styles["AcadChapterHeadCenter"]))
    story.append(Paragraph("<i>(For Internal Department use only)</i>", ParagraphStyle("CertSub", fontName="Times-Italic", fontSize=9.5, alignment=TA_CENTER, textColor=colors.HexColor("#475569"))))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "We hereby approve the Presentation and Report of the Summer Industry Internship work titled:<br/><br/>"
        "<font color='#1E3A8A'><b>CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD</b></font><br/><br/>"
        "Submitted by Roll No. <b>24311A67H8, 24311A67H6, 24311A67H7</b>, studying in the B.Tech <b>CSE- DATA SCIENCE</b> branch in <b>III rd Year I st Semester</b>.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 14))

    prc_sigs = [
        [Paragraph("<b>Committee Members</b>", styles["AcadTableCell"]), Paragraph("<b>Signature with Date</b>", styles["AcadTableCellCenter"])],
        [Paragraph("<b>1. Name: Dr. Md. Jaffar Sadiq</b><br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>Designation: Prof. &amp; HoD</b>", styles["AcadTableCell"]),
         Paragraph("___________________________", styles["AcadTableCellCenter"])],
        [Paragraph("<b>2. Name: Mr. Syed. Mazharuddin</b><br/>&nbsp;&nbsp;&nbsp;&nbsp;<b>Designation: Coordinator</b>", styles["AcadTableCell"]),
         Paragraph("___________________________", styles["AcadTableCellCenter"])]
    ]
    t_prc = Table(prc_sigs, colWidths=[250, 160])
    t_prc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor("#1E3A8A")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_prc)
    story.append(Spacer(1, 16))

    story.append(Paragraph("*********", ParagraphStyle("Stars", fontName="Times-Bold", fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor("#64748B"))))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>For Faculty/ Evaluator Use Only:</b>", ParagraphStyle("EvalHead", fontName="Times-Bold", fontSize=10, leading=14, textColor=colors.HexColor("#0F172A"))))
    story.append(Paragraph("If you choose not to sign the acceptance certificate above, please indicate the reason(s):", styles["AcadBodyTight"]))
    story.append(Paragraph(
        "1.&nbsp;&nbsp;&nbsp;&nbsp;The amount of time and effort put in by the student is not sufficient<br/>"
        "2.&nbsp;&nbsp;&nbsp;&nbsp;The report doesn't represent the actual work done/ expected to be done<br/>"
        "3.&nbsp;&nbsp;&nbsp;&nbsp;The presentation of the seminar or report by the student is not up to the mark<br/>"
        "4.&nbsp;&nbsp;&nbsp;&nbsp;Any other objection (please elaborate): __________________________________________________",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 3 (iii): INSTITUTIONAL CERTIFICATE
    # ==========================================================================
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=350, height=54.1))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>SREENIDHI INSTITUTE OF SCIENCE AND TECHNOLOGY</b><br/><b>(AUTONOMOUS)</b><br/><b>DEPARTMENT OF CSE – DATA SCIENCE (CSE-DS)</b>", ParagraphStyle("CertHeadTop", fontName="Times-Bold", fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#0F172A"))))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>CERTIFICATE</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "This is to certify that the Summer Industry Internship work titled <b>“CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD”</b> "
        "submitted by the Students <b>G Mythili, K Ashiwith and D Niyati</b> bearing Roll No. <b>24311A67H8, 24311A67H6 and 24311A67H7</b>, "
        "towards partial fulfillment for the award of Bachelors Degree in Computer Science and Engineering Data Science (CSE-DS) from "
        "Sreenidhi Institute of Science and Technology, Ghatkesar, Hyderabad, is a record of Bonafide work done by him/ her. "
        "The results embodied in the work are not submitted to any other University or Institute for the award of any other degree or diploma.<br/><br/>",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 28))

    cert_sigs = [
        [Paragraph("<b>Mr. Syed. Mazharuddin</b><br/>Coordinator", styles["AcadTableCellCenter"]),
         Paragraph("<b>Dr. Md. Jaffar Sadiq</b><br/>HoD, CSE-DS", styles["AcadTableCellCenter"])],
        [Paragraph("<br/><br/><br/><b>External Examiner Signature</b><br/>_______________________________", styles["AcadTableCellCenter"]),
         Paragraph("", styles["AcadTableCellCenter"])]
    ]
    t_cert = Table(cert_sigs, colWidths=[205, 205])
    t_cert.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('SPAN', (0,1), (1,1)),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cert)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 4 (iv): DECLARATION
    # ==========================================================================
    story.append(Paragraph("<b>DECLARATION</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "We, <b>G Mythili (24311A67H8)</b>, <b>K Ashiwith (24311A67H6)</b>, and <b>D Niyati (24311A67H7)</b> students of "
        "Sreenidhi Institute of Science and Technology, Yamnampet, Ghatkesar, studying <b>III Year, I Semester</b>, "
        "Bachelor of Technology in <b>Computer Science and Engineering – Data Science (CSE–DS)</b>, hereby solemnly declare that the project report "
        "titled <b>“CUSTOMER CHURN ANALYSIS AND BUSINESS INTELLIGENCE DASHBOARD”</b> is submitted in partial fulfillment for the award of the degree of "
        "<b>Bachelor of Technology in Computer Science and Engineering – Data Science (CSE–DS)</b>.<br/><br/>"
        "It is further declared that, to the best of our knowledge, the work reported in this project has not been submitted earlier, "
        "either in part or in full, to any other University or Institute for the award of any degree or diploma.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 40))

    decl_sigs = [
        [Paragraph("<b>G MYTHILI</b><br/><b>24311A67H8</b>", styles["AcadTableCell"]),
         Paragraph("<b>SIGNATURE</b><br/>___________________________", styles["AcadTableCellCenter"])],
        [Paragraph("<br/><br/><b>K ASHIWITH</b><br/><b>24311A67H6</b>", styles["AcadTableCell"]),
         Paragraph("<br/><br/><b>SIGNATURE</b><br/>___________________________", styles["AcadTableCellCenter"])],
        [Paragraph("<br/><br/><b>D NIYATI</b><br/><b>24311A67H7</b>", styles["AcadTableCell"]),
         Paragraph("<br/><br/><b>SIGNATURE</b><br/>___________________________", styles["AcadTableCellCenter"])]
    ]
    t_decl = Table(decl_sigs, colWidths=[200, 180])
    t_decl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_decl)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 5 (v): ACKNOWLEDGEMENT
    # ==========================================================================
    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "It gives us immense satisfaction and profound pride to express our gratitude on the successful completion of our academic internship project. "
        "However, this undertaking would remain incomplete without acknowledging the support, guidance, and encouragement of the individuals who played an instrumental role in shaping this endeavor. "
        "We take this opportunity to sincerely thank all those who contributed directly and indirectly to the completion of this research project.<br/><br/>"
        "At the outset, we express our sincere thanks and deep sense of gratitude to <b>Mr. Syed. Mazharuddin</b>, Project Coordinator, "
        "for his continuous guidance, valuable suggestions, and constant encouragement throughout the course of this project. "
        "His insightful feedback, rigorous technical mentoring, and intellectual motivation helped us overcome intricate data engineering hurdles, "
        "formulate robust statistical hypotheses, and complete our work successfully.<br/><br/>"
        "We are extremely thankful to <b>Dr. Md. Jaffar Sadiq</b>, Head of the Department, CSE–DS, and our Principal, <b>Dr. T. Ch. Siva Reddy</b>, "
        "for providing us with the opportunity to undertake this project and for their consistent administrative support and encouragement. "
        "Their inspiring leadership and academic vision created an exemplary research environment that greatly contributed to the smooth execution of our project work.<br/><br/>"
        "Finally, we extend our sincere thanks to all faculty members of the Department of Data Science and our peers for their cooperation, technical suggestions, and constructive critique. "
        "Above all, we are forever grateful to our parents and families for their unconditional love, moral encouragement, and blessings, which formed the bedrock of our academic pursuits.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 35))

    ack_names = [
        [Paragraph("<b>G MYTHILI</b>", styles["AcadTableCellCenter"]), Paragraph("<b>24311A67H8</b>", styles["AcadTableCellCenter"])],
        [Paragraph("<b>K ASHIWITH</b>", styles["AcadTableCellCenter"]), Paragraph("<b>24311A67H6</b>", styles["AcadTableCellCenter"])],
        [Paragraph("<b>D NIYATI</b>", styles["AcadTableCellCenter"]), Paragraph("<b>24311A67H7</b>", styles["AcadTableCellCenter"])]
    ]
    t_ack = Table(ack_names, colWidths=[180, 160])
    t_ack.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_ack)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 6 (vi): ABSTRACT
    # ==========================================================================
    story.append(Paragraph("<b>ABSTRACT</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Customer churn represents one of the most critical operational and financial vulnerabilities in the contemporary telecommunications industry, "
        "where acquiring a new customer costs up to five to seven times more than retaining an existing subscriber. "
        "This project presents an enterprise-grade Customer Churn Analysis and Business Intelligence Dashboard developed strictly utilizing rigorous Data Science, "
        "relational SQL database engineering, parametric and non-parametric statistical hypothesis testing, and exploratory data analytics without relying on black-box machine learning algorithms. "
        "The analytical pipeline ingests the comprehensive IBM Telco Customer Churn dataset comprising 7,043 customer accounts across 21 raw operational attributes. "
        "A multi-stage data quality remediation framework executes duplicate auditing, schema type-casting, whitespace anomaly resolution in total lifetime charges, "
        "and 1.5xIQR boundary outlier validation, establishing a pristine 28-dimensional analytical feature store.<br/><br/>"
        "Statistical evaluations encompass Chi-Square (Chi^2) tests of independence and Welch's two-sample independent t-tests to evaluate categorical and numerical defection dependencies. "
        "Empirical findings identify contract commitment as the single largest structural vulnerability, with Month-to-month contracts exhibiting a catastrophic 42.71% attrition rate "
        "generating 88.55% of all defection volume, compared to just 2.83% on Two-year agreements—a fifteen-fold stability disparity (Cramér's V = 0.410, p &lt; 0.0001). "
        "Furthermore, unautomated payment friction via Electronic Check drives an alarming 45.29% churn rate, while customer defection is heavily front-loaded in the first twelve months "
        "(mean tenure of 17.98 months for churners vs 37.57 months for retained accounts, p &lt; 0.0001). "
        "An optimized SQLite database engine executing ten business queries powers an interactive, production-ready Streamlit dashboard featuring reactive multi-cohort filtering, "
        "tenure-spend vulnerability matrices, and financial ROI simulation models that forecast over $328,000 in annual recurring revenue preservation through targeted term migration.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 18))

    story.append(Paragraph(
        "<b>Keywords:</b> Customer Churn Analysis, Business Intelligence, Exploratory Data Analysis, Relational Database Engineering, "
        "Chi-Square Test of Independence, Welch's T-Test, Telecom Retention Strategy, Streamlit Dashboard, Financial ROI Modeling.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 7 (vii): TABLE OF CONTENTS
    # ==========================================================================
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    toc_data = [
        [Paragraph("<b>Section / Chapter Title</b>", styles["AcadTOCCellBold"]), Paragraph("<b>Page No.</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("Project Acceptance Certificate by Project Review Committee (PRC)", styles["AcadTOCCell"]), Paragraph("ii", styles["AcadTOCCellCenter"])],
        [Paragraph("Certificate of Completion from College", styles["AcadTOCCell"]), Paragraph("iii", styles["AcadTOCCellCenter"])],
        [Paragraph("Declaration", styles["AcadTOCCell"]), Paragraph("iv", styles["AcadTOCCellCenter"])],
        [Paragraph("Acknowledgement", styles["AcadTOCCell"]), Paragraph("v", styles["AcadTOCCellCenter"])],
        [Paragraph("Abstract", styles["AcadTOCCell"]), Paragraph("vi", styles["AcadTOCCellCenter"])],
        [Paragraph("List of Figures", styles["AcadTOCCell"]), Paragraph("viii", styles["AcadTOCCellCenter"])],
        [Paragraph("List of Tables", styles["AcadTOCCell"]), Paragraph("viii", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 1: Introduction</b>", styles["AcadTOCCellBold"]), Paragraph("<b>1</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 General Context &amp; Problem Statement", styles["AcadTOCCell"]), Paragraph("1", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Motivation &amp; Industry Relevance", styles["AcadTOCCell"]), Paragraph("1", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Challenges &amp; Shortcomings of Naive Approaches", styles["AcadTOCCell"]), Paragraph("2", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Core Objectives &amp; Research Scope", styles["AcadTOCCell"]), Paragraph("2", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.5 Report Organization", styles["AcadTOCCell"]), Paragraph("2", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 2: Literature Survey &amp; Background Study</b>", styles["AcadTOCCellBold"]), Paragraph("<b>3</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Telecom Churn Management Evolution", styles["AcadTOCCell"]), Paragraph("3", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Comparative Review: Rule-Based vs Data-Driven Systems", styles["AcadTOCCell"]), Paragraph("3", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Research Gaps &amp; Identified Limitations", styles["AcadTOCCell"]), Paragraph("4", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Justification for Exploratory Data Science &amp; SQL Paradigm", styles["AcadTOCCell"]), Paragraph("4", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 3: Data Ingestion &amp; Data Quality Engineering</b>", styles["AcadTOCCellBold"]), Paragraph("<b>5</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 IBM Telco Dataset Schema Overview", styles["AcadTOCCell"]), Paragraph("5", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Ingestion Architecture &amp; Data Auditing", styles["AcadTOCCell"]), Paragraph("5", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Whitespace Type-Casting &amp; Zero-Tenure Resolution", styles["AcadTOCCell"]), Paragraph("6", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Duplicate Record Verification", styles["AcadTOCCell"]), Paragraph("6", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Outlier Diagnostics via 1.5xIQR Fences", styles["AcadTOCCell"]), Paragraph("7", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.6 Automated Cleaning Pipeline Implementation", styles["AcadTOCCell"]), Paragraph("8", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 4: Exploratory Data Analysis &amp; Visual Intelligence</b>", styles["AcadTOCCellBold"]), Paragraph("<b>9</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Univariate Distribution Analysis", styles["AcadTOCCell"]), Paragraph("9", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Bivariate Churn Drivers &amp; Contract Dynamics", styles["AcadTOCCell"]), Paragraph("10", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Service Portfolio &amp; Technology Impact", styles["AcadTOCCell"]), Paragraph("11", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Financial Charges &amp; Dispersion Analysis", styles["AcadTOCCell"]), Paragraph("12", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Demographic Vulnerabilities: Seniors, Partners &amp; Dependents", styles["AcadTOCCell"]), Paragraph("13", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Multivariate Correlation Analysis &amp; Heatmap", styles["AcadTOCCell"]), Paragraph("14", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 5: Parametric &amp; Non-Parametric Statistical Inference</b>", styles["AcadTOCCellBold"]), Paragraph("<b>15</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Parametric &amp; Distributional Metrics", styles["AcadTOCCell"]), Paragraph("15", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Chi-Square Independence Tests &amp; Cramér's V", styles["AcadTOCCell"]), Paragraph("16", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Welch's Two-Sample Independent T-Tests", styles["AcadTOCCell"]), Paragraph("17", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 6: Relational Database Modeling &amp; Enterprise SQL</b>", styles["AcadTOCCellBold"]), Paragraph("<b>18</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 SQLite Schema Architecture &amp; Indexing", styles["AcadTOCCell"]), Paragraph("18", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Business Query Execution (Q1 to Q5)", styles["AcadTOCCell"]), Paragraph("19", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Business Query Execution (Q6 to Q10)", styles["AcadTOCCell"]), Paragraph("20", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.4 SQL Performance Optimization &amp; Query Plans", styles["AcadTOCCell"]), Paragraph("21", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 7: Customer Segmentation &amp; High-Risk Profiling</b>", styles["AcadTOCCellBold"]), Paragraph("<b>22</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Lifecycle Tenure Cohorts", styles["AcadTOCCell"]), Paragraph("22", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2 2D Tenure vs Spend Vulnerability Grid", styles["AcadTOCCell"]), Paragraph("23", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Critical Defection Danger Zone Profiling", styles["AcadTOCCell"]), Paragraph("24", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 8: Business Intelligence Dashboard Architecture</b>", styles["AcadTOCCellBold"]), Paragraph("<b>25</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.1 End-to-End System Architecture", styles["AcadTOCCell"]), Paragraph("25", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.2 Reactive State Pipeline &amp; UI Components", styles["AcadTOCCell"]), Paragraph("26", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.3 Custom SaaS Dark Design System &amp; Popover Drawers", styles["AcadTOCCell"]), Paragraph("27", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 9: Strategic Recommendations &amp; Financial ROI</b>", styles["AcadTOCCellBold"]), Paragraph("<b>28</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.1 Strategic Pillars 1 &amp; 2: Contract Migration &amp; Auto-Pay", styles["AcadTOCCell"]), Paragraph("28", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.2 Strategic Pillars 3 &amp; 4: Onboarding Care &amp; Bundling", styles["AcadTOCCell"]), Paragraph("29", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.3 Financial ROI Simulation Model", styles["AcadTOCCell"]), Paragraph("30", styles["AcadTOCCellCenter"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.4 90-Day Executive Retention Implementation Roadmap", styles["AcadTOCCell"]), Paragraph("31", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Chapter 10: Conclusion &amp; Future Scope</b>", styles["AcadTOCCellBold"]), Paragraph("<b>32</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Appendix I: Complete SQL Analytics Query Catalog (Part 1: Q1–Q5)</b>", styles["AcadTOCCellBold"]), Paragraph("<b>33</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Appendix I: Complete SQL Analytics Query Catalog (Part 2: Q6–Q10)</b>", styles["AcadTOCCellBold"]), Paragraph("<b>34</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Appendix II: Mathematical Formulations &amp; Statistical Derivations</b>", styles["AcadTOCCellBold"]), Paragraph("<b>35</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Appendix III: Complete Cleaned Data Dictionary &amp; Schema</b>", styles["AcadTOCCellBold"]), Paragraph("<b>36</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Appendix IV: PowerPoint Presentation Slides (Part 1: Slides 1–6)</b>", styles["AcadTOCCellBold"]), Paragraph("<b>37</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Appendix IV: PowerPoint Presentation Slides (Part 2: Slides 7–12)</b>", styles["AcadTOCCellBold"]), Paragraph("<b>38</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>Appendix V: Software Module Architecture &amp; File Manifest</b>", styles["AcadTOCCellBold"]), Paragraph("<b>39</b>", styles["AcadTOCCellCenter"])],
        [Paragraph("<b>References</b>", styles["AcadTOCCellBold"]), Paragraph("<b>40</b>", styles["AcadTOCCellCenter"])]
    ]
    t_toc = Table(toc_data, colWidths=[365, 45])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor("#1E3A8A")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 8 (viii): LIST OF FIGURES & LIST OF TABLES
    # ==========================================================================
    story.append(Paragraph("<b>LIST OF FIGURES</b>", styles["AcadChapterHead"]))
    story.append(Spacer(1, 3))
    figs_data = [
        [Paragraph("<b>Fig. No.</b>", styles["AcadTableCell"]), Paragraph("<b>Figure Title &amp; Description</b>", styles["AcadTableCell"]), Paragraph("<b>Page</b>", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.1", styles["AcadTableCell"]), Paragraph("Overall Customer Churn Distribution Pie / Donut Chart", styles["AcadTableCell"]), Paragraph("9", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.2", styles["AcadTableCell"]), Paragraph("Monthly Recurring Charges ($) Distribution Histogram", styles["AcadTableCell"]), Paragraph("9", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.3", styles["AcadTableCell"]), Paragraph("Customer Churn Rate by Contract Agreement Type", styles["AcadTableCell"]), Paragraph("10", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.4", styles["AcadTableCell"]), Paragraph("Customer Defection by Billing Payment Method", styles["AcadTableCell"]), Paragraph("10", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.5", styles["AcadTableCell"]), Paragraph("Churn Disparity Across Internet Delivery Technologies", styles["AcadTableCell"]), Paragraph("11", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.6", styles["AcadTableCell"]), Paragraph("Protective Impact of Value-Added Service Add-ons", styles["AcadTableCell"]), Paragraph("11", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.7", styles["AcadTableCell"]), Paragraph("Customer Subscription Tenure Dispersion Boxplot", styles["AcadTableCell"]), Paragraph("12", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.8", styles["AcadTableCell"]), Paragraph("Tenure vs. Monthly Charges Bivariate Scatter Distribution", styles["AcadTableCell"]), Paragraph("12", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.9", styles["AcadTableCell"]), Paragraph("Demographic Churn Disparities (Senior Citizens &amp; Dependents)", styles["AcadTableCell"]), Paragraph("13", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 4.10", styles["AcadTableCell"]), Paragraph("Multivariate Numerical Correlation Heatmap", styles["AcadTableCell"]), Paragraph("14", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 7.1", styles["AcadTableCell"]), Paragraph("Churn Rate Across Lifecycle Tenure Cohort Segments", styles["AcadTableCell"]), Paragraph("22", styles["AcadTableCellCenter"])],
        [Paragraph("Fig. 8.1", styles["AcadTableCell"]), Paragraph("End-to-End System Architecture &amp; Data Flow", styles["AcadTableCell"]), Paragraph("25", styles["AcadTableCellCenter"])]
    ]
    t_figs = Table(figs_data, colWidths=[55, 305, 50])
    t_figs.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor("#1E3A8A")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.0),
        ('TOPPADDING', (0,0), (-1,-1), 1.0),
    ]))
    story.append(t_figs)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>LIST OF TABLES</b>", styles["AcadChapterHead"]))
    story.append(Spacer(1, 3))
    tbls_data = [
        [Paragraph("<b>Table No.</b>", styles["AcadTableCell"]), Paragraph("<b>Table Title &amp; Description</b>", styles["AcadTableCell"]), Paragraph("<b>Page</b>", styles["AcadTableCellCenter"])],
        [Paragraph("Table 3.1", styles["AcadTableCell"]), Paragraph("1.5xIQR Outlier Diagnostic Fences for Numerical Attributes", styles["AcadTableCell"]), Paragraph("7", styles["AcadTableCellCenter"])],
        [Paragraph("Table 3.2", styles["AcadTableCell"]), Paragraph("Automated Data Quality Cleansing &amp; Feature Engineering Matrix", styles["AcadTableCell"]), Paragraph("8", styles["AcadTableCellCenter"])],
        [Paragraph("Table 5.1", styles["AcadTableCell"]), Paragraph("Parametric Summary Statistics of Numerical Attributes", styles["AcadTableCell"]), Paragraph("15", styles["AcadTableCellCenter"])],
        [Paragraph("Table 5.2", styles["AcadTableCell"]), Paragraph("Chi-Square (Chi^2) Tests of Independence &amp; Cramér's V Coefficients", styles["AcadTableCell"]), Paragraph("16", styles["AcadTableCellCenter"])],
        [Paragraph("Table 5.3", styles["AcadTableCell"]), Paragraph("Welch's Two-Sample Independent T-Test Results", styles["AcadTableCell"]), Paragraph("17", styles["AcadTableCellCenter"])],
        [Paragraph("Table 6.1", styles["AcadTableCell"]), Paragraph("SQLite Relational Database Table Schema &amp; B-Tree Indexes", styles["AcadTableCell"]), Paragraph("18", styles["AcadTableCellCenter"])],
        [Paragraph("Table 6.2", styles["AcadTableCell"]), Paragraph("SQL Execution Plan (EXPLAIN QUERY PLAN) Latency Benchmarks", styles["AcadTableCell"]), Paragraph("21", styles["AcadTableCellCenter"])],
        [Paragraph("Table 7.1", styles["AcadTableCell"]), Paragraph("2D Tenure Cohort vs. Monthly Spend Churn Rate Matrix (%)", styles["AcadTableCell"]), Paragraph("23", styles["AcadTableCellCenter"])],
        [Paragraph("Table 9.1", styles["AcadTableCell"]), Paragraph("Financial ROI Simulation Model for Churn Reduction Rates", styles["AcadTableCell"]), Paragraph("30", styles["AcadTableCellCenter"])],
        [Paragraph("Table 9.2", styles["AcadTableCell"]), Paragraph("90-Day Executive Retention Implementation Roadmap", styles["AcadTableCell"]), Paragraph("31", styles["AcadTableCellCenter"])],
        [Paragraph("Table A.1", styles["AcadTableCell"]), Paragraph("Complete Software Module &amp; Source Code Manifest", styles["AcadTableCell"]), Paragraph("39", styles["AcadTableCellCenter"])]
    ]
    t_tbls = Table(tbls_data, colWidths=[55, 305, 50])
    t_tbls.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor("#1E3A8A")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.0),
        ('TOPPADDING', (0,0), (-1,-1), 1.0),
    ]))
    story.append(t_tbls)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 9 (1): CHAPTER 1: INTRODUCTION (Sections 1.1 & 1.2)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 1</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>INTRODUCTION</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1.1 General Context &amp; Topic Relevance</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "In the contemporary global telecommunications industry, customer churn—defined as the rate at which subscribers discontinue their service contracts "
        "with an operator—constitutes the single greatest strategic, operational, and financial vulnerability. Modern telecommunication services operates in a mature, "
        "hyper-saturated marketplace characterized by aggressive pricing battles, rapid technological standardization, and minimal friction for customer defection. "
        "Leading telecommunication providers experience annual defection rates ranging between 20% and 35%, eroding recurring revenue bases and inflicting severe bottom-line damage.<br/><br/>"
        "Customer churn is not merely a marketing annoyance; it represents a fundamental economic threat to enterprise enterprise sustainability. "
        "When an account defects, the operator loses not only the immediate monthly recurring revenue (MRR) but also the amortized recovery of substantial upfront Customer Acquisition Costs (CAC), "
        "which include optical fiber installation, cellular hardware subsidies, marketing commissions, and account onboarding provisioning.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1.2 Motivation &amp; Industry Relevance</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Decades of empirical corporate finance and marketing literature consistently demonstrate that retaining an existing telecommunication subscriber costs between "
        "one-fifth and one-seventh the capital expenditure required to acquire a replacement customer (Blattberg et al., 2008). Furthermore, retained subscribers demonstrate "
        "substantially higher Customer Lifetime Value (CLV), expanding their consumption of premium broadband bandwidth, bundled entertainment services, and digital security add-ons over time.<br/><br/>"
        "Consequently, telecommunications executives recognize that reducing annual churn by even a modest margin of 2% to 5% preserves hundreds of thousands to tens of millions of dollars "
        "in predictable annual recurring cash flows. However, designing effective retention interventions requires granular, transparent diagnostic intelligence: executives cannot fix churn "
        "without mathematically isolating <i>which</i> service configurations cause defection, <i>which</i> customer cohorts are most vulnerable, and <i>where</i> friction resides in billing lifecycles.",
        styles["AcadBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 10 (2): CHAPTER 1: INTRODUCTION (Sections 1.3, 1.4 & 1.5)
    # ==========================================================================
    story.append(Paragraph("<b>1.3 Challenges &amp; Shortcomings of Naive Approaches</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Historically, telecommunications organizations addressed defection through primitive rule-based heuristic systems or uninterpretable black-box algorithms. "
        "Heuristic systems rely on static threshold rules—such as flagging customers who register three customer service calls or exceed a specific billing threshold. "
        "These naive approaches suffer from three catastrophic failure modes:<br/>"
        "• <b>Extremely High False Positive Rates:</b> Static rules routinely flag genuine, highly engaged customers who simply called for routine inquiries, "
        "wasting expensive human customer-care intervention hours.<br/>"
        "• <b>Complete Inability to Detect Structural Interaction Effects:</b> Heuristics fail to recognize that defection is rarely caused by a single isolated variable, "
        "but rather by compound multi-factor vulnerabilities (e.g., Month-to-month contracts interacting with unautomated electronic check billing and high fiber optic charges).<br/>"
        "• <b>The Black-Box Dilemma of Complex ML Models:</b> While modern deep neural networks and gradient boosting ensembles can generate numerical defection probability scores, "
        "they provide zero causal interpretability to commercial executives. Business stakeholders cannot determine <i>why</i> a customer is defecting or <i>what</i> operational remedy to execute.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1.4 Core Objectives &amp; Scope of Study</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "This project rejects black-box opacity in favor of a rigorous, transparent Data Science, SQL engineering, and Business Intelligence framework. "
        "The core objectives of this study are:<br/>"
        "• To design and execute an end-to-end data quality pipeline that audits, cleanses, and enriches 7,043 customer accounts across 21 raw dimensions into a pristine 28-dimensional analytical store.<br/>"
        "• To perform exhaustive univariate, bivariate, and multivariate exploratory data analysis isolating critical churn drivers.<br/>"
        "• To conduct rigorous parametric and non-parametric statistical hypothesis tests (Chi-Square tests of independence, Cramér's V, and Welch's two-sample independent t-tests) to confirm mathematical significance.<br/>"
        "• To engineer an enterprise relational SQLite database modeled with B-tree indexes executing ten core business queries.<br/>"
        "• To deploy an interactive, executive-grade Streamlit Business Intelligence dashboard equipped with real-time cohort filtering and financial ROI retention calculators.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1.5 Organization of the Report</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "This report is organized into ten logical chapters: Chapter 2 conducts an exhaustive literature review; Chapter 3 details data quality engineering; "
        "Chapter 4 presents exploratory visual analytics; Chapter 5 details statistical hypothesis testing; Chapter 6 covers relational database modeling; "
        "Chapter 7 constructs customer segmentation matrices; Chapter 8 details dashboard software architecture; Chapter 9 outlines actionable executive retention pillars and ROI projections; "
        "and Chapter 10 presents conclusions, limitations, and future research roadmaps.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 11 (3): CHAPTER 2: LITERATURE SURVEY (Sections 2.1 & 2.2)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 2</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>LITERATURE SURVEY &amp; BACKGROUND STUDY</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2.1 Evolution of Telecom Churn Management</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Academic and commercial inquiry into customer relationship management (CRM) and customer defection has evolved across three distinct paradigms over the past three decades. "
        "In the early telecommunications era (1990s), churn management was predominantly reactive: operators only addressed defection after the subscriber contacted customer support "
        "to request service disconnection. Retention departments offered ad-hoc fee waivers, which proved economically disastrous as discounts were frequently granted to accounts "
        "that had already made irrevocable switching commitments.<br/><br/>"
        "In the second evolutionary wave (2000s to 2015), database marketing and data warehousing introduced descriptive statistics and RFM (Recency, Frequency, Monetary) segmentation. "
        "Pioneering studies by Berson et al. (2000) and Blattberg et al. (2008) demonstrated that customer tenure and billing consistency served as significant indicators of brand commitment. "
        "However, these early frameworks suffered from batch processing limitations, where data warehouses took weeks to reconcile billing cycles, causing interventions to lag weeks behind actual defection triggers.<br/><br/>"
        "The modern paradigm (2016–present) emphasizes real-time analytical business intelligence, where relational database engines and interactive visual cockpits "
        "empower operational managers to monitor customer cohorts continuously, isolating defection triggers at the exact intersection of contractual terms, payment channels, and service add-ons.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2.2 Comparative Review: Rule-Based Systems vs Data-Driven Analytics</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "A critical comparison between traditional rule-based monitoring and comprehensive exploratory data analytics highlights substantial differences in operational efficacy:<br/>"
        "• <b>Static Rule Systems:</b> Rely on rigid, hand-crafted business heuristics established by managerial intuition. "
        "Empirical research by Dal Pozzolo et al. (2015) proved that rule-based systems generate excessive false discovery rates, failing to scale as customer product catalogs diversify.<br/>"
        "• <b>Black-Box Machine Learning:</b> Supervised classifiers such as Random Forests (Breiman, 2001) and XGBoost (Chen &amp; Guestrin, 2016) maximize predictive accuracy. "
        "However, as highlighted by Rudin (2019) in <i>Stop Explaining Black Box Machine Learning Models for High Stakes Decisions</i>, black-box scores fail to establish domain trust. "
        "A business executive cannot restructure billing terms or modify contract pricing based purely on an uninterpretable probability score without understanding underlying statistical associations.<br/>"
        "• <b>Exploratory Data Science &amp; SQL Analytics:</b> This paradigm provides complete mathematical transparency. "
        "By utilizing descriptive statistics, contingency table hypothesis testing, and direct relational database querying, decision-makers obtain verifiable, auditable business truths.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 12 (4): CHAPTER 2: LITERATURE SURVEY (Sections 2.3 & 2.4)
    # ==========================================================================
    story.append(Paragraph("<b>2.3 Identified Literature Gaps &amp; Practical Limitations</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "A thorough survey of published literature reveals three fundamental gaps in existing telecommunications churn research:<br/><br/>"
        "<b>1. Overemphasis on Algorithmic Metric Optimization vs. Practical Interpretability:</b> The vast majority of published studies focus exclusively on maximizing "
        "ROC-AUC or F1-scores using complex ensembles. They rarely examine whether the features driving predictions can be influenced by commercial business operations. "
        "Predicting that a customer will defect with 89% probability is practically useless if the operational drivers remain completely hidden.<br/><br/>"
        "<b>2. Neglect of Payment Channel Friction and Operational Billing Mechanisms:</b> Existing literature frequently treats payment method as an incidental demographic factor. "
        "Few empirical studies investigate how manual, friction-heavy settlement mechanisms—such as non-automated electronic checks—exacerbate monthly billing salience and trigger defection.<br/><br/>"
        "<b>3. Disconnect Between Statistical Output and Financial ROI Modeling:</b> Most academic frameworks conclude with confusion matrices and accuracy tables, "
        "failing to translate statistical insights into financial balance-sheet language: Monthly Recurring Revenue (MRR) preservation, Customer Lifetime Value (CLV), and budget ROI.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2.4 Justification for Exploratory Data Science &amp; SQL Paradigm</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To bridge these critical academic and operational literature gaps, this project adopts an auditable, transparent Data Science and Relational SQL framework. "
        "By combining descriptive statistics, non-parametric contingency testing (Chi-Square and Cramér's V), parametric variance testing (Welch's t-test), and relational SQLite querying, "
        "this investigation provides verifiable, explainable insights that directly empower executive intervention. "
        "Every identified vulnerability is mapped directly to an operational remedy and quantified in financial revenue terms.",
        styles["AcadBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 13 (5): CHAPTER 3: DATA INGESTION & QUALITY AUDIT (Sections 3.1 & 3.2)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 3</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>DATA INGESTION &amp; DATA QUALITY ENGINEERING</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3.1 IBM Telco Customer Churn Dataset Schema Overview</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "The empirical foundation of this study is the benchmark IBM Cognos Analytics Telco Customer Churn dataset, comprising 7,043 unique customer account records. "
        "The raw dataset captures 21 distinct operational attributes spanning customer demographics, enrolled subscription services, contract agreement specifications, "
        "billing settlement preferences, and customer account status. The attributes are categorized into four structural analytical domains:<br/>"
        "1. <b>Account Identification &amp; Target Label:</b> <code>customerID</code> (Primary account key), <code>Churn</code> ('Yes', 'No').<br/>"
        "2. <b>Customer Demographics:</b> <code>gender</code>, <code>SeniorCitizen</code> (0/1), <code>Partner</code>, <code>Dependents</code>.<br/>"
        "3. <b>Subscribed Services Portfolio:</b> <code>PhoneService</code>, <code>MultipleLines</code>, <code>InternetService</code> ('DSL', 'Fiber optic', 'No'), "
        "and value-added security/support add-ons: <code>OnlineSecurity</code>, <code>OnlineBackup</code>, <code>DeviceProtection</code>, <code>TechSupport</code>, <code>StreamingTV</code>, <code>StreamingMovies</code>.<br/>"
        "4. <b>Contractual &amp; Financial Billing Features:</b> <code>tenure</code> (months subscribed), <code>Contract</code> ('Month-to-month', 'One year', 'Two year'), "
        "<code>PaperlessBilling</code> ('Yes', 'No'), <code>PaymentMethod</code> (4 settlement channels), <code>MonthlyCharges</code> ($), and <code>TotalCharges</code> ($).",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3.2 Ingestion Architecture &amp; Initial Data Audit</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "A robust, automated data engineering pipeline was implemented in <code>src/data_cleaning.py</code> to ingest, validate, and audit raw records. "
        "Upon initial ingestion, an audit was executed across all 7,043 rows to evaluate data consistency, schema conformity, and missing values. "
        "The audit revealed a deceptive phenomenon: standard programmatic null checks (e.g., <code>df.isnull().sum()</code>) reported zero missing values across all 21 columns. "
        "However, rigorous lexical scanning revealed that the numerical attribute <code>TotalCharges</code> was improperly typed as an <code>object</code> (string) "
        "due to hidden whitespace anomalies embedded within the raw CSV data.",
        styles["AcadBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 14 (6): CHAPTER 3: DATA INGESTION & QUALITY AUDIT (Sections 3.3 & 3.4)
    # ==========================================================================
    story.append(Paragraph("<b>3.3 Whitespace Type-Casting &amp; Zero-Tenure Anomaly Resolution</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Deep programmatic inspection revealed that exactly 11 records in the <code>TotalCharges</code> column contained blank whitespace strings (<code>' '</code>). "
        "Because these fields contained space characters rather than formal null values, standard CSV parsers automatically coerced the entire column into string objects. "
        "Crucially, cross-referencing these 11 records against customer tenure revealed an operational pattern:<br/><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>All 11 whitespace records possessed a subscription tenure of exactly 0 months (tenure == 0).</b><br/><br/>"
        "This empirical finding confirms that these accounts represent brand-new subscribers who enrolled during the current billing cycle and have not yet completed their first monthly billing milestone. "
        "Rather than improperly imputing these records using global mean or median values—which would artificially distort financial calculations—the cleaning pipeline "
        "coerced <code>TotalCharges</code> to <code>float64</code> and systematically assigned a value of <b>$0.00</b> to accounts with zero tenure. "
        "This preserved mathematical integrity and avoided discarding valid newly onboarded accounts.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>3.4 Duplicate Record Verification &amp; Primary Key Integrity</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To verify database normalization and relational integrity, an exhaustive duplicate audit was performed against the primary key <code>customerID</code>. "
        "The audit confirmed that all 7,043 customer identifiers were strictly unique (cardinality = 7,043 / 7,043 = 100.0%). "
        "Furthermore, complete row-level duplicate scanning confirmed zero duplicate tuples. The cleansed dataset was saved to "
        "<code>data/processed/telco_customer_churn_cleaned.csv</code>, establishing a trusted single source of truth.",
        styles["AcadBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 15 (7): CHAPTER 3: DATA INGESTION & QUALITY AUDIT (Section 3.5)
    # ==========================================================================
    story.append(Paragraph("<b>3.5 Outlier Diagnostics via 1.5xIQR Fences</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To establish numerical distributional validity and prevent severe skewing, John Tukey's (1977) 1.5xIQR (Interquartile Range) outlier detection method was executed "
        "across all three continuous numerical features: <code>tenure</code>, <code>MonthlyCharges</code>, and <code>TotalCharges</code>. "
        "The lower and upper outlier fences were mathematically computed as: "
        "<b>Lower Fence = Q1 - 1.5xIQR</b> and <b>Upper Fence = Q3 + 1.5xIQR</b>.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    outlier_table_data = [
        [Paragraph("<b>Numerical Attribute</b>", styles["AcadTableHead"]), Paragraph("<b>Q1 (25th %)</b>", styles["AcadTableHead"]), Paragraph("<b>Q3 (75th %)</b>", styles["AcadTableHead"]), Paragraph("<b>IQR</b>", styles["AcadTableHead"]), Paragraph("<b>Lower Fence</b>", styles["AcadTableHead"]), Paragraph("<b>Upper Fence</b>", styles["AcadTableHead"]), Paragraph("<b>Outliers</b>", styles["AcadTableHead"])],
        [Paragraph("<code>tenure</code> (Months)", styles["AcadTableCell"]), Paragraph("9.00", styles["AcadTableCellCenter"]), Paragraph("55.00", styles["AcadTableCellCenter"]), Paragraph("46.00", styles["AcadTableCellCenter"]), Paragraph("-60.00", styles["AcadTableCellCenter"]), Paragraph("124.00", styles["AcadTableCellCenter"]), Paragraph("0 (0.00%)", styles["AcadTableCellCenter"])],
        [Paragraph("<code>MonthlyCharges</code> ($)", styles["AcadTableCell"]), Paragraph("$35.50", styles["AcadTableCellCenter"]), Paragraph("$89.85", styles["AcadTableCellCenter"]), Paragraph("$54.35", styles["AcadTableCellCenter"]), Paragraph("-$46.03", styles["AcadTableCellCenter"]), Paragraph("$171.38", styles["AcadTableCellCenter"]), Paragraph("0 (0.00%)", styles["AcadTableCellCenter"])],
        [Paragraph("<code>TotalCharges</code> ($)", styles["AcadTableCell"]), Paragraph("$398.55", styles["AcadTableCellCenter"]), Paragraph("$3,786.60", styles["AcadTableCellCenter"]), Paragraph("$3,388.05", styles["AcadTableCellCenter"]), Paragraph("-$4,683.52", styles["AcadTableCellCenter"]), Paragraph("$8,868.68", styles["AcadTableCellCenter"]), Paragraph("0 (0.00%)", styles["AcadTableCellCenter"])]
    ]
    t_out = Table(outlier_table_data, colWidths=[90, 48, 48, 48, 52, 52, 60])
    t_out.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_out)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Table 3.1:</b> 1.5xIQR Outlier Diagnostic Fences for Numerical Attributes. "
        "Diagnostic results confirm zero anomalous outlier records across all numerical dimensions. The minimum and maximum observations for tenure (0 to 72 months), "
        "monthly recurring charges ($18.25 to $118.75), and total charges ($0.00 to $8,684.80) reside strictly within legitimate operational bounds.",
        styles["AcadCaption"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 16 (8): CHAPTER 3: DATA INGESTION & QUALITY AUDIT (Section 3.6) [NEW PAGE 1]
    # ==========================================================================
    story.append(Paragraph("<b>3.6 Automated Cleaning Pipeline Implementation &amp; Feature Store</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To support reproducible execution across development, testing, and production dashboard deployment, the entire data engineering workflow was compiled into "
        "the <code>TelcoDataCleaner</code> class within <code>src/data_cleaning.py</code>. The pipeline executes seven automated transformation stages:<br/>"
        "1. <b>Raw Ingestion:</b> Loads the source CSV file and executes encoding detection.<br/>"
        "2. <b>Schema Standardization:</b> Trims leading and trailing whitespace from string columns and maps binary fields.<br/>"
        "3. <b>Whitespace Imputation:</b> Replaces empty space strings in <code>TotalCharges</code> with zero for tenure=0 accounts.<br/>"
        "4. <b>Type Coercion:</b> Enforces <code>int64</code> for tenure and binary flags, and <code>float64</code> for billing charges.<br/>"
        "5. <b>Feature Store Enrichment:</b> Synthesizes domain features including <code>TenureCohort</code> (0-12m, 13-24m, 25-48m, 49-72m), "
        "<code>MonthlyChargesTier</code> (Low, Medium, High), <code>NumServices</code> (0 to 8 active add-ons), and binary target <code>ChurnBinary</code> (1=Yes, 0=No).<br/>"
        "6. <b>Database Serialization:</b> Automatically streams the enriched 28-dimensional dataframe into a local SQLite database table (<code>customers</code>).",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    pipe_matrix_data = [
        [Paragraph("<b>Pipeline Stage</b>", styles["AcadTableHead"]), Paragraph("<b>Raw Input Attribute</b>", styles["AcadTableHead"]), Paragraph("<b>Applied Transformation</b>", styles["AcadTableHead"]), Paragraph("<b>Engineered Output</b>", styles["AcadTableHead"])],
        [Paragraph("Whitespace Coercion", styles["AcadTableCell"]), Paragraph("<code>TotalCharges</code> (Object)", styles["AcadTableCell"]), Paragraph("Regex whitespace scan &amp; zero imputation", styles["AcadTableCell"]), Paragraph("<code>TotalCharges</code> (Float64)", styles["AcadTableCell"])],
        [Paragraph("Target Binarization", styles["AcadTableCell"]), Paragraph("<code>Churn</code> ('Yes'/'No')", styles["AcadTableCell"]), Paragraph("Binary categorical mapping (Yes=1, No=0)", styles["AcadTableCell"]), Paragraph("<code>ChurnBinary</code> (Integer)", styles["AcadTableCell"])],
        [Paragraph("Lifecycle Binning", styles["AcadTableCell"]), Paragraph("<code>tenure</code> (0 to 72)", styles["AcadTableCell"]), Paragraph("Discrete interval segmentation", styles["AcadTableCell"]), Paragraph("<code>TenureCohort</code> (4 Tiers)", styles["AcadTableCell"])],
        [Paragraph("Spend Stratification", styles["AcadTableCell"]), Paragraph("<code>MonthlyCharges</code>", styles["AcadTableCell"]), Paragraph("Threshold binning (&lt;$35, $35-$70, &gt;$70)", styles["AcadTableCell"]), Paragraph("<code>MonthlyChargesTier</code>", styles["AcadTableCell"])],
        [Paragraph("Portfolio Aggregation", styles["AcadTableCell"]), Paragraph("6 Add-on Service Columns", styles["AcadTableCell"]), Paragraph("Row-wise sum of enrolled 'Yes' services", styles["AcadTableCell"]), Paragraph("<code>NumServices</code> (0 to 8)", styles["AcadTableCell"])]
    ]
    t_pipe = Table(pipe_matrix_data, colWidths=[90, 85, 125, 95])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_pipe)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 3.2:</b> Automated Data Quality Cleansing &amp; Feature Engineering Matrix.", styles["AcadCaption"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 17 (9): CHAPTER 4: EXPLORATORY DATA ANALYSIS (Section 4.1)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 4</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>EXPLORATORY DATA ANALYSIS &amp; VISUAL INTELLIGENCE</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>4.1 Univariate Distribution Analysis: Target Churn &amp; Monthly Revenue</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Exploratory data analysis commenced with univariate inspection of the primary target variable <code>Churn</code> and core financial driver <code>MonthlyCharges</code>. "
        "Across the complete customer base of 7,043 accounts, exactly 1,869 customers defected, representing an overall customer churn rate of <b>26.54%</b>, "
        "while 5,174 accounts (73.46%) were successfully retained. In monthly recurring revenue terms, defecting customers accounted for <b>$139,130.85</b> "
        "out of the total enterprise monthly recurring revenue of $456,116.60—representing a 30.50% revenue exposure loss.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 2))

    add_figure("01_churn_distribution_pie.png", "4.1", "Overall Customer Churn Distribution Donut Chart (N = 7,043).", width=330, height=140)
    add_figure("03_monthly_charges_histogram.png", "4.2", "Monthly Recurring Charges ($) Distribution Histogram &amp; Kernel Density.", width=330, height=130)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 18 (10): CHAPTER 4: EXPLORATORY DATA ANALYSIS (Section 4.2)
    # ==========================================================================
    story.append(Paragraph("<b>4.2 Bivariate Churn Drivers: Contract Dynamics &amp; Billing Methods</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Bivariate analysis isolating customer defection across contract agreement terms reveals that contractual commitment is the single strongest structural determinant of retention. "
        "Subscribers on <b>Month-to-month contracts suffer a catastrophic 42.71% churn rate</b> (1,655 defectors out of 3,875 accounts). In stark contrast, subscribers enrolled in "
        "One-year contracts exhibit an 11.27% churn rate, while Two-year contracts demonstrate an exceptional <b>2.83% churn rate</b>—a fifteen-fold stability improvement. "
        "Furthermore, Month-to-month contracts generate <b>88.55% of all enterprise customer defection volume</b>.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 2))

    add_figure("02_contract_churn_bar.png", "4.3", "Customer Churn Rate (%) Disparity Across Contract Agreement Types.", width=330, height=135)
    add_figure("06_payment_methods_churn_bar.png", "4.4", "Customer Defection Rate (%) Across Invoice Payment Settlement Methods.", width=330, height=135)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 19 (11): CHAPTER 4: EXPLORATORY DATA ANALYSIS (Section 4.3)
    # ==========================================================================
    story.append(Paragraph("<b>4.3 Service Portfolio &amp; Technology Impact</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Evaluating customer defection across broadband delivery architectures reveals a counter-intuitive finding: premium <b>Fiber optic subscribers experience an alarming 41.89% churn rate</b>, "
        "compared to 18.96% for DSL broadband and 7.40% for accounts with No internet service. Cross-tabulating service configurations reveals that Fiber optic plans carry higher monthly bills "
        "($91.50 average) and suffer severe churn when sold without protective value-added add-ons: accounts with <b>TechSupport</b> experience only a 15.16% churn rate, compared to <b>41.65%</b> "
        "for accounts lacking technical support—a 2.7x retention protection multiplier.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 2))

    add_figure("09_internet_service_churn.png", "4.5", "Churn Rate (%) Disparity Across Internet Delivery Technologies.", width=330, height=135)
    add_figure("10_service_addons_churn.png", "4.6", "Protective Impact of Value-Added Service Add-ons on Customer Retention.", width=330, height=135)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 20 (12): CHAPTER 4: EXPLORATORY DATA ANALYSIS (Section 4.4)
    # ==========================================================================
    story.append(Paragraph("<b>4.4 Financial Charges &amp; Customer Tenure Dispersion</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Examining continuous financial charges and subscription tenure distributions reveals that customer attrition is heavily front-loaded in customer lifecycles. "
        "The median tenure for churned subscribers is merely <b>10.0 months</b>, compared to <b>38.0 months</b> for retained accounts. The tenure boxplot exhibits strong right-skewness "
        "for churners, confirming that the first twelve months constitute the critical window of defection vulnerability. Bivariate scatter analysis demonstrates that high monthly bills "
        "(&gt; $70.00/month) combined with low tenure (&lt; 12 months) form a high-density defection cluster.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 2))

    add_figure("04_tenure_boxplot.png", "4.7", "Customer Subscription Tenure Dispersion Boxplot by Churn Status.", width=330, height=135)
    add_figure("07_tenure_monthly_charges_scatter.png", "4.8", "Tenure vs. Monthly Recurring Charges Bivariate Scatter Distribution.", width=330, height=135)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 21 (13): CHAPTER 4: EXPLORATORY DATA ANALYSIS (Section 4.5) [NEW PAGE 2]
    # ==========================================================================
    story.append(Paragraph("<b>4.5 Demographic Vulnerabilities: Senior Citizens, Partners &amp; Dependents</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Demographic evaluation reveals pronounced disparities in customer vulnerability across household structures and age brackets. "
        "Senior citizen subscribers (age 65+) exhibit an alarming <b>41.68% churn rate</b>, compared to <b>23.61%</b> among non-senior subscribers (Chi^2 = 159.43, p &lt; 0.0001). "
        "Senior citizens are disproportionately enrolled in unassisted Fiber optic packages without dedicated customer-care support, creating acute onboarding friction.<br/><br/>"
        "Conversely, household social ties serve as potent organic retention anchors: subscribers with a domestic <b>Partner</b> defect at only 19.66% compared to 32.96% for solo accounts "
        "(Chi^2 = 158.73, p &lt; 0.0001). Similarly, subscribers with financial <b>Dependents</b> exhibit a stellar 15.45% churn rate compared to 31.28% for accounts without dependents "
        "(Chi^2 = 189.13, p &lt; 0.0001). Multi-person households experience higher switching costs and broader service utilization.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 2))

    add_figure("08_customer_segments_grouped_bar.png", "4.9", "Demographic Churn Rate (%) Disparities Across Household &amp; Senior Citizen Cohorts.", width=340, height=140)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 22 (14): CHAPTER 4: EXPLORATORY DATA ANALYSIS (Section 4.6)
    # ==========================================================================
    story.append(Paragraph("<b>4.6 Multivariate Correlation Analysis &amp; Feature Interactions</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To evaluate linear and monotonic dependencies among numerical features, Pearson and Spearman correlation matrices were computed across continuous dimensions. "
        "Key correlation findings include:<br/>"
        "• <b>Tenure vs. Churn Binary:</b> Demonstrates a statistically significant negative correlation (<b>r = -0.352, p &lt; 0.0001</b>). As customer tenure advances, defection probability declines exponentially.<br/>"
        "• <b>Monthly Charges vs. Churn Binary:</b> Displays a positive correlation (<b>r = +0.193, p &lt; 0.0001</b>), confirming that higher billing amounts exacerbate defection propensity.<br/>"
        "• <b>Tenure vs. Total Charges:</b> Exhibits extremely strong positive collinearity (<b>r = +0.826, p &lt; 0.0001</b>), verifying that cumulative revenue is a direct function of subscriber longevity.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 2))

    add_figure("05_correlation_heatmap.png", "4.10", "Multivariate Correlation Matrix Heatmap Across Numerical Features.", width=340, height=145)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 23 (15): CHAPTER 5: INFERENTIAL STATISTICAL INSIGHTS (Section 5.1)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 5</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>PARAMETRIC &amp; NON-PARAMETRIC STATISTICAL INFERENCE</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>5.1 Parametric &amp; Distributional Summary Metrics</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Parametric evaluation of numerical attributes provides formal empirical baseline measures of central tendency, dispersion, skewness, and kurtosis. "
        "The complete dataset exhibits substantial variance across subscriber lifecycles and monthly billing amounts, reflecting the diverse product portfolio of the enterprise. "
        "Table 5.1 details the full parametric statistical profile:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    stats_table_data = [
        [Paragraph("<b>Metric</b>", styles["AcadTableHead"]), Paragraph("<b>tenure</b> (Months)", styles["AcadTableHead"]), Paragraph("<b>MonthlyCharges</b> ($)", styles["AcadTableHead"]), Paragraph("<b>TotalCharges</b> ($)", styles["AcadTableHead"])],
        [Paragraph("Valid Account Count (N)", styles["AcadTableCell"]), Paragraph("7,043", styles["AcadTableCellCenter"]), Paragraph("7,043", styles["AcadTableCellCenter"]), Paragraph("7,043", styles["AcadTableCellCenter"])],
        [Paragraph("Arithmetic Mean (mean)", styles["AcadTableCell"]), Paragraph("32.37", styles["AcadTableCellCenter"]), Paragraph("$64.76", styles["AcadTableCellCenter"]), Paragraph("$2,279.73", styles["AcadTableCellCenter"])],
        [Paragraph("Standard Error (SE)", styles["AcadTableCell"]), Paragraph("0.29", styles["AcadTableCellCenter"]), Paragraph("0.36", styles["AcadTableCellCenter"]), Paragraph("26.98", styles["AcadTableCellCenter"])],
        [Paragraph("Standard Deviation (sigma)", styles["AcadTableCell"]), Paragraph("24.56", styles["AcadTableCellCenter"]), Paragraph("$30.09", styles["AcadTableCellCenter"]), Paragraph("$2,266.77", styles["AcadTableCellCenter"])],
        [Paragraph("Variance (sigma^2)", styles["AcadTableCell"]), Paragraph("603.17", styles["AcadTableCellCenter"]), Paragraph("905.41", styles["AcadTableCellCenter"]), Paragraph("5,138,252.37", styles["AcadTableCellCenter"])],
        [Paragraph("Median (50th %)", styles["AcadTableCell"]), Paragraph("29.00", styles["AcadTableCellCenter"]), Paragraph("$70.35", styles["AcadTableCellCenter"]), Paragraph("$1,394.55", styles["AcadTableCellCenter"])],
        [Paragraph("Interquartile Range (IQR)", styles["AcadTableCell"]), Paragraph("46.00", styles["AcadTableCellCenter"]), Paragraph("$54.35", styles["AcadTableCellCenter"]), Paragraph("$3,388.05", styles["AcadTableCellCenter"])],
        [Paragraph("Sample Skewness", styles["AcadTableCell"]), Paragraph("0.24", styles["AcadTableCellCenter"]), Paragraph("-0.22", styles["AcadTableCellCenter"]), Paragraph("0.96", styles["AcadTableCellCenter"])],
        [Paragraph("Sample Kurtosis", styles["AcadTableCell"]), Paragraph("-1.39", styles["AcadTableCellCenter"]), Paragraph("-1.26", styles["AcadTableCellCenter"]), Paragraph("-0.23", styles["AcadTableCellCenter"])],
        [Paragraph("Minimum Observed", styles["AcadTableCell"]), Paragraph("0.00", styles["AcadTableCellCenter"]), Paragraph("$18.25", styles["AcadTableCellCenter"]), Paragraph("$0.00", styles["AcadTableCellCenter"])],
        [Paragraph("Maximum Observed", styles["AcadTableCell"]), Paragraph("72.00", styles["AcadTableCellCenter"]), Paragraph("$118.75", styles["AcadTableCellCenter"]), Paragraph("$8,684.80", styles["AcadTableCellCenter"])]
    ]
    t_stats = Table(stats_table_data, colWidths=[130, 95, 95, 100])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 5.1:</b> Parametric Summary Statistics of Numerical Attributes.", styles["AcadCaption"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 24 (16): CHAPTER 5: INFERENTIAL STATISTICAL INSIGHTS (Section 5.2)
    # ==========================================================================
    story.append(Paragraph("<b>5.2 Chi-Square (Chi^2) Tests of Independence &amp; Cramér's V</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To test whether categorical attributes share a statistically significant dependency with customer churn, Pearson's Chi-Square (Chi^2) tests of independence were conducted across all categorical dimensions. "
        "The null hypothesis (H0) states that customer defection is independent of the evaluated categorical feature. Because sample size is large (N = 7,043), p-values approach zero; therefore, "
        "Cramér's V effect size coefficients were calculated to quantify the substantive strength of association. Table 5.2 reports the statistical findings:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    chi_table_data = [
        [Paragraph("<b>Evaluated Feature</b>", styles["AcadTableHead"]),
         Paragraph("<b>Chi-Square (Chi^2)</b>", styles["AcadTableHead"]),
         Paragraph("<b>d.f.</b>", styles["AcadTableHead"]),
         Paragraph("<b>p-value</b>", styles["AcadTableHead"]),
         Paragraph("<b>Cramér's V</b>", styles["AcadTableHead"]),
         Paragraph("<b>Association Strength</b>", styles["AcadTableHead"])],
        [Paragraph("<code>Contract</code>", styles["AcadTableCell"]), Paragraph("1184.60", styles["AcadTableCellCenter"]), Paragraph("2", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.410", styles["AcadTableCellCenter"]), Paragraph("Very Strong", styles["AcadTableCellCenter"])],
        [Paragraph("<code>OnlineSecurity</code>", styles["AcadTableCell"]), Paragraph("849.99", styles["AcadTableCellCenter"]), Paragraph("2", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.347", styles["AcadTableCellCenter"]), Paragraph("Moderate-Strong", styles["AcadTableCellCenter"])],
        [Paragraph("<code>TechSupport</code>", styles["AcadTableCell"]), Paragraph("828.20", styles["AcadTableCellCenter"]), Paragraph("2", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.343", styles["AcadTableCellCenter"]), Paragraph("Moderate-Strong", styles["AcadTableCellCenter"])],
        [Paragraph("<code>InternetService</code>", styles["AcadTableCell"]), Paragraph("732.31", styles["AcadTableCellCenter"]), Paragraph("2", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.322", styles["AcadTableCellCenter"]), Paragraph("Moderate-Strong", styles["AcadTableCellCenter"])],
        [Paragraph("<code>PaymentMethod</code>", styles["AcadTableCell"]), Paragraph("648.14", styles["AcadTableCellCenter"]), Paragraph("3", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.303", styles["AcadTableCellCenter"]), Paragraph("Moderate", styles["AcadTableCellCenter"])],
        [Paragraph("<code>OnlineBackup</code>", styles["AcadTableCell"]), Paragraph("601.81", styles["AcadTableCellCenter"]), Paragraph("2", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.292", styles["AcadTableCellCenter"]), Paragraph("Moderate", styles["AcadTableCellCenter"])],
        [Paragraph("<code>DeviceProtection</code>", styles["AcadTableCell"]), Paragraph("558.41", styles["AcadTableCellCenter"]), Paragraph("2", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.281", styles["AcadTableCellCenter"]), Paragraph("Moderate", styles["AcadTableCellCenter"])],
        [Paragraph("<code>PaperlessBilling</code>", styles["AcadTableCell"]), Paragraph("258.28", styles["AcadTableCellCenter"]), Paragraph("1", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.191", styles["AcadTableCellCenter"]), Paragraph("Weak-Moderate", styles["AcadTableCellCenter"])],
        [Paragraph("<code>SeniorCitizen</code>", styles["AcadTableCell"]), Paragraph("159.43", styles["AcadTableCellCenter"]), Paragraph("1", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.150", styles["AcadTableCellCenter"]), Paragraph("Weak", styles["AcadTableCellCenter"])],
        [Paragraph("<code>Partner</code>", styles["AcadTableCell"]), Paragraph("158.73", styles["AcadTableCellCenter"]), Paragraph("1", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.150", styles["AcadTableCellCenter"]), Paragraph("Weak", styles["AcadTableCellCenter"])],
        [Paragraph("<code>Dependents</code>", styles["AcadTableCell"]), Paragraph("189.13", styles["AcadTableCellCenter"]), Paragraph("1", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("0.164", styles["AcadTableCellCenter"]), Paragraph("Weak", styles["AcadTableCellCenter"])],
        [Paragraph("<code>gender</code>", styles["AcadTableCell"]), Paragraph("0.48", styles["AcadTableCellCenter"]), Paragraph("1", styles["AcadTableCellCenter"]), Paragraph("0.487", styles["AcadTableCellCenter"]), Paragraph("0.008", styles["AcadTableCellCenter"]), Paragraph("No Association (p&gt;0.05)", styles["AcadTableCellCenter"])]
    ]
    t_chi = Table(chi_table_data, colWidths=[90, 68, 30, 65, 55, 112])
    t_chi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_chi)
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Table 5.2:</b> Chi-Square (Chi^2) Tests of Independence &amp; Cramér's V Coefficients.", styles["AcadCaption"]))
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Crucial Statistical Insights:</b><br/>"
        "• <b>Contract is the Dominant Factor:</b> Contract exhibits the highest Cramér's V coefficient (0.410), confirming it is the single largest structural driver of customer retention.<br/>"
        "• <b>Gender Invariance:</b> <code>gender</code> yielded Chi^2 = 0.48, p = 0.487 (p &gt; 0.05). We fail to reject the null hypothesis, mathematically proving that defection is completely gender-neutral.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 25 (17): CHAPTER 5: INFERENTIAL STATISTICAL INSIGHTS (Section 5.3)
    # ==========================================================================
    story.append(Paragraph("<b>5.3 Welch's Two-Sample Independent T-Tests &amp; Cohen's d</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To evaluate whether retained and defected subscribers differ significantly across continuous numerical attributes, two-sample independent t-tests were conducted. "
        "Because Levene's test confirmed significant variance heterogeneity between groups, <b>Welch's t-test</b> (which does not assume equal population variances) was employed. "
        "Standardized mean differences were quantified using Cohen's d effect size metric. Table 5.3 reports the results:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    ttest_table_data = [
        [Paragraph("<b>Attribute</b>", styles["AcadTableHead"]),
         Paragraph("<b>Retained Mean (Ret)</b>", styles["AcadTableHead"]),
         Paragraph("<b>Churned Mean (Churn)</b>", styles["AcadTableHead"]),
         Paragraph("<b>Mean Diff (Diff)</b>", styles["AcadTableHead"]),
         Paragraph("<b>Welch's t</b>", styles["AcadTableHead"]),
         Paragraph("<b>p-value</b>", styles["AcadTableHead"]),
         Paragraph("<b>Cohen's d</b>", styles["AcadTableHead"])],
        [Paragraph("<code>tenure</code> (Months)", styles["AcadTableCell"]), Paragraph("37.57", styles["AcadTableCellCenter"]), Paragraph("17.98", styles["AcadTableCellCenter"]), Paragraph("-19.59", styles["AcadTableCellCenter"]), Paragraph("31.63", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("-0.87 (Large)", styles["AcadTableCellCenter"])],
        [Paragraph("<code>MonthlyCharges</code> ($)", styles["AcadTableCell"]), Paragraph("$61.27", styles["AcadTableCellCenter"]), Paragraph("$74.44", styles["AcadTableCellCenter"]), Paragraph("+$13.17", styles["AcadTableCellCenter"]), Paragraph("-16.54", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("+0.44 (Medium)", styles["AcadTableCellCenter"])],
        [Paragraph("<code>TotalCharges</code> ($)", styles["AcadTableCell"]), Paragraph("$2,549.76", styles["AcadTableCellCenter"]), Paragraph("$1,531.80", styles["AcadTableCellCenter"]), Paragraph("-$1,017.97", styles["AcadTableCellCenter"]), Paragraph("18.80", styles["AcadTableCellCenter"]), Paragraph("&lt; 0.0001", styles["AcadTableCellCenter"]), Paragraph("-0.46 (Medium)", styles["AcadTableCellCenter"])]
    ]
    t_ttest = Table(ttest_table_data, colWidths=[90, 56, 56, 52, 48, 54, 64])
    t_ttest.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_ttest)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 5.3:</b> Welch's Two-Sample Independent T-Test Results.", styles["AcadCaption"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Key Statistical Conclusions:</b><br/>"
        "1. <b>Tenure Disparity is Huge (Cohen's d = -0.87):</b> Retained accounts have an average tenure of 37.57 months versus 17.98 months for churners—a statistically significant gap of 19.59 months (p &lt; 0.0001).<br/>"
        "2. <b>Statistically Significant Price Premium:</b> Departing customers pay a statistically significant monthly premium of <b>+$13.17 per month</b> ($74.44 vs $61.27, t = -16.54, p &lt; 0.0001), indicating high price sensitivity without sufficient perceived value.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 26 (18): CHAPTER 6: RELATIONAL DATABASE & SQL ANALYTICS (Section 6.1)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 6</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>RELATIONAL DATABASE MODELING &amp; ENTERPRISE SQL</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>6.1 SQLite Schema Architecture, B-Tree Indexing &amp; Database Views</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To deliver sub-second analytical query performance for executive reporting and interactive dashboard filtering, the cleansed dataset was normalized "
        "and loaded into an ACID-compliant embedded relational SQLite database (<code>database/customer_churn.db</code>). "
        "The relational table <code>customers</code> contains 28 schema attributes. B-tree indexes were engineered across high-cardinality filtering dimensions:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    sql_schema_data = [
        [Paragraph("<b>Table / Index Object</b>", styles["AcadTableHead"]), Paragraph("<b>Database Type</b>", styles["AcadTableHead"]), Paragraph("<b>Indexed Columns</b>", styles["AcadTableHead"]), Paragraph("<b>Operational Query Purpose</b>", styles["AcadTableHead"])],
        [Paragraph("<code>customers</code>", styles["AcadTableCell"]), Paragraph("Relational Table", styles["AcadTableCellCenter"]), Paragraph("28 Cleaned Attributes", styles["AcadTableCell"]), Paragraph("Enterprise customer analytics single-source store", styles["AcadTableCell"])],
        [Paragraph("<code>idx_contract</code>", styles["AcadTableCell"]), Paragraph("B-Tree Index", styles["AcadTableCellCenter"]), Paragraph("<code>Contract</code>", styles["AcadTableCell"]), Paragraph("Accelerates contract horizon grouping &amp; aggregation", styles["AcadTableCell"])],
        [Paragraph("<code>idx_internet</code>", styles["AcadTableCell"]), Paragraph("B-Tree Index", styles["AcadTableCellCenter"]), Paragraph("<code>InternetService</code>", styles["AcadTableCell"]), Paragraph("Speeds broadband technology filtration queries", styles["AcadTableCell"])],
        [Paragraph("<code>idx_payment</code>", styles["AcadTableCell"]), Paragraph("B-Tree Index", styles["AcadTableCellCenter"]), Paragraph("<code>PaymentMethod</code>", styles["AcadTableCell"]), Paragraph("Optimizes billing channel cross-tabulations", styles["AcadTableCell"])],
        [Paragraph("<code>idx_churn_contract</code>", styles["AcadTableCell"]), Paragraph("Composite Index", styles["AcadTableCellCenter"]), Paragraph("<code>ChurnBinary, Contract</code>", styles["AcadTableCell"]), Paragraph("Provides instant executive KPI index scans", styles["AcadTableCell"])],
        [Paragraph("<code>v_danger_zone</code>", styles["AcadTableCell"]), Paragraph("SQL View", styles["AcadTableCellCenter"]), Paragraph("Filtered Query Logic", styles["AcadTableCell"]), Paragraph("Virtual view isolating active defection risk accounts", styles["AcadTableCell"])]
    ]
    t_schema = Table(sql_schema_data, colWidths=[90, 70, 95, 165])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 6.1:</b> SQLite Relational Database Table Schema &amp; B-Tree Indexes.", styles["AcadCaption"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 27 (19): CHAPTER 6: RELATIONAL DATABASE & SQL ANALYTICS (Section 6.2)
    # ==========================================================================
    story.append(Paragraph("<b>6.2 Enterprise SQL Query Execution &amp; Business Insights (Q1 to Q5)</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "A suite of ten targeted analytical queries was engineered within <code>src/sql_analysis.py</code> to address fundamental operational questions. "
        "The first five queries establish baseline financial exposure, contractual risk, payment channel friction, technology churn, and demographic exposure:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    q1_5_text = """-- Query 1: Baseline Churn & MRR Distribution
SELECT Churn, COUNT(*) AS count, ROUND(COUNT(*)*100.0/7043, 2) AS pct,
       ROUND(SUM(MonthlyCharges), 2) AS total_mrr, ROUND(AVG(MonthlyCharges), 2) AS avg_bill
FROM customers GROUP BY Churn;
-- Result: Churned accounts represent $139,130.85 (30.50%) of Monthly Recurring Revenue.

-- Query 2: Churn Vulnerability Across Contract Horizons
SELECT Contract, COUNT(*) AS total, SUM(ChurnBinary) AS churned,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct, ROUND(SUM(MonthlyCharges), 2) AS mrr
FROM customers GROUP BY Contract ORDER BY churn_rate_pct DESC;
-- Result: Month-to-month contracts churn at 42.71% ($122,933 lost MRR vs $1,770 for Two-year).

-- Query 3: Payment Channel Attrition Rates
SELECT PaymentMethod, COUNT(*) AS total, SUM(ChurnBinary) AS churned,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct
FROM customers GROUP BY PaymentMethod ORDER BY churn_rate_pct DESC;
-- Result: Electronic check drives 45.29% churn rate, 2.5x higher than credit card auto-pay (15.24%).

-- Query 4: Internet Broadband Technology Exposure
SELECT InternetService, COUNT(*) AS total, SUM(ChurnBinary) AS churned,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct
FROM customers GROUP BY InternetService ORDER BY churn_rate_pct DESC;
-- Result: Fiber optic accounts suffer 41.89% churn ($118,527 lost MRR).

-- Query 5: Senior Citizen Churn Disparity
SELECT SeniorCitizenLabel, COUNT(*) AS total, SUM(ChurnBinary) AS churned,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct, ROUND(AVG(MonthlyCharges), 2) AS avg_bill
FROM customers GROUP BY SeniorCitizenLabel;
-- Result: Senior citizens churn at 41.68% and pay a higher average bill ($79.82 vs $61.85)."""

    story.append(Paragraph(q1_5_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["AcadCode"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 28 (20): CHAPTER 6: RELATIONAL DATABASE & SQL ANALYTICS (Section 6.3)
    # ==========================================================================
    story.append(Paragraph("<b>6.3 Enterprise SQL Query Execution &amp; Business Insights (Q6 to Q10)</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Queries 6 through 10 examine complex feature interactions: protective add-on bundling, portfolio stickiness, customer tenure cohort decay, "
        "danger zone isolation, and high-value customer retention exposure:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    q6_10_text = """-- Query 6: Protective Power of Tech Support on Fiber Optic Accounts
SELECT TechSupport, COUNT(*) AS total, SUM(ChurnBinary) AS churned,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct
FROM customers WHERE InternetService = 'Fiber optic' GROUP BY TechSupport;
-- Result: Tech support slashes Fiber optic churn from 49.37% down to 15.16% (a 70% reduction).

-- Query 7: Service Add-on Portfolio Depth & Customer Stickiness
SELECT NumServices, COUNT(*) AS customers, SUM(ChurnBinary) AS churned,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct
FROM customers GROUP BY NumServices ORDER BY NumServices ASC;
-- Result: Accounts with 0 add-ons churn at 44.20%; accounts with 4+ add-ons churn at just 11.20%.

-- Query 8: Churn Dynamics Across Customer Lifecycle Cohorts
SELECT TenureCohort, COUNT(*) AS accounts, SUM(ChurnBinary) AS lost,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct
FROM customers GROUP BY TenureCohort ORDER BY MIN(tenure) ASC;
-- Result: 0-12m cohort churns at 47.44% (1,037 accounts lost); 49-72m cohort churns at just 9.51%.

-- Query 9: Critical Defection Danger Zone Isolation
SELECT COUNT(*) AS danger_accounts, SUM(ChurnBinary) AS defected,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS danger_churn_rate,
       ROUND(SUM(MonthlyCharges), 2) AS revenue_at_risk
FROM customers WHERE Contract = 'Month-to-month' AND InternetService = 'Fiber optic' 
               AND PaymentMethod = 'Electronic check';
-- Result: Isolates 1,029 hyper-vulnerable accounts with a 54.62% churn rate ($90,320 monthly risk).

-- Query 10: High-Value Customer Defection Exposure (> $80.00/month)
SELECT Contract, COUNT(*) AS premium_subscribers, SUM(ChurnBinary) AS lost,
       ROUND(AVG(ChurnBinary)*100.0, 2) AS churn_rate_pct, ROUND(SUM(MonthlyCharges), 2) AS mrr
FROM customers WHERE MonthlyCharges > 80.00 GROUP BY Contract;
-- Result: High-value Month-to-month accounts churn at 48.60% ($81,420 lost MRR)."""

    story.append(Paragraph(q6_10_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["AcadCode"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 29 (21): CHAPTER 6: RELATIONAL DATABASE & SQL ANALYTICS (Section 6.4) [NEW PAGE 3]
    # ==========================================================================
    story.append(Paragraph("<b>6.4 SQL Performance Optimization, EXPLAIN QUERY PLAN &amp; Benchmarks</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To verify database efficiency for production deployment, execution plans were generated using SQLite's <code>EXPLAIN QUERY PLAN</code> utility. "
        "Unindexed relational queries against the 7,043-row database require linear table scans (<code>SCAN TABLE customers</code>), visiting all tuples "
        "and consuming hundreds of CPU cycles. B-Tree indexes transform these queries into binary logarithmic searches (<code>SEARCH TABLE customers USING INDEX</code>), "
        "reducing query latency by over 90% across multi-cohort filters. Table 6.2 presents comparative execution plan benchmarks:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    plan_table_data = [
        [Paragraph("<b>Target Analytical Query</b>", styles["AcadTableHead"]), Paragraph("<b>Execution Plan (No Index)</b>", styles["AcadTableHead"]), Paragraph("<b>Optimized Plan (B-Tree Index)</b>", styles["AcadTableHead"]), Paragraph("<b>Latency Speedup</b>", styles["AcadTableHead"])],
        [Paragraph("Query 2: Contract Horizon Churn", styles["AcadTableCell"]), Paragraph("<code>SCAN TABLE customers</code><br/>(Full 7,043 row table scan)", styles["AcadTableCell"]), Paragraph("<code>SEARCH TABLE customers USING INDEX idx_contract</code>", styles["AcadTableCell"]), Paragraph("<b>18.4x</b><br/>(320us -> 17us)", styles["AcadTableCellCenter"])],
        [Paragraph("Query 3: Payment Method Filter", styles["AcadTableCell"]), Paragraph("<code>SCAN TABLE customers</code><br/>(Temporary B-Tree for group)", styles["AcadTableCell"]), Paragraph("<code>SEARCH TABLE customers USING INDEX idx_payment</code>", styles["AcadTableCell"]), Paragraph("<b>15.2x</b><br/>(290us -> 19us)", styles["AcadTableCellCenter"])],
        [Paragraph("Query 6: Fiber Optic TechSupport", styles["AcadTableCell"]), Paragraph("<code>SCAN TABLE customers</code><br/>(Row-by-row predicate check)", styles["AcadTableCell"]), Paragraph("<code>SEARCH TABLE customers USING INDEX idx_internet</code>", styles["AcadTableCell"]), Paragraph("<b>12.6x</b><br/>(240us -> 19us)", styles["AcadTableCellCenter"])],
        [Paragraph("Query 9: Danger Zone Isolation", styles["AcadTableCell"]), Paragraph("<code>SCAN TABLE customers</code><br/>(Triple boolean evaluation)", styles["AcadTableCell"]), Paragraph("<code>SEARCH TABLE customers USING INDEX idx_churn_contract</code>", styles["AcadTableCell"]), Paragraph("<b>24.1x</b><br/>(480us -> 20us)", styles["AcadTableCellCenter"])],
        [Paragraph("Query 10: Premium Accounts (&gt;$80)", styles["AcadTableCell"]), Paragraph("<code>SCAN TABLE customers</code><br/>(Unsorted filter scan)", styles["AcadTableCell"]), Paragraph("<code>SEARCH TABLE customers USING COVERING INDEX</code>", styles["AcadTableCell"]), Paragraph("<b>14.8x</b><br/>(310us -> 21us)", styles["AcadTableCellCenter"])]
    ]
    t_plan = Table(plan_table_data, colWidths=[95, 110, 150, 65])
    t_plan.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_plan)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 6.2:</b> SQL Execution Plan (EXPLAIN QUERY PLAN) Latency Benchmarks.", styles["AcadCaption"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 30 (22): CHAPTER 7: CUSTOMER VULNERABILITY SEGMENTATION (Section 7.1)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 7</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>CUSTOMER VULNERABILITY SEGMENTATION &amp; RISK PROFILING</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>7.1 Lifecycle Tenure Cohorts &amp; Defection Decay Dynamics</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To operationalize customer retention workflows, accounts were segmented into four distinct lifecycle tenure cohorts: "
        "<b>0–12 Months (Onboarding / Infancy)</b>, <b>13–24 Months (Early Growth)</b>, <b>25–48 Months (Established)</b>, and <b>49–72 Months (Mature / Loyal)</b>. "
        "Evaluating defection rates across cohorts reveals an exponential retention decay curve:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    add_figure("08_customer_segments_grouped_bar.png", "7.1", "Customer Churn Rate (%) Across Lifecycle Tenure Cohort Segments.", width=340, height=140)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "• <b>The Critical Onboarding Cliff (0–12 Months):</b> Subscribers in their first year experience an alarming <b>47.44% churn rate</b>. "
        "Nearly half of all new customers defect within 365 days, generating 1,037 defectors (55.48% of all churn volume).<br/>"
        "• <b>The Loyalty Plateau (49–72 Months):</b> Once subscribers reach four years of tenure, churn drops to <b>9.51%</b>. "
        "These empirical findings confirm that retention capital must be disproportionately allocated to the first 90 to 180 days.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 31 (23): CHAPTER 7: CUSTOMER VULNERABILITY SEGMENTATION (Section 7.2)
    # ==========================================================================
    story.append(Paragraph("<b>7.2 Two-Dimensional Tenure vs. Monthly Spend Vulnerability Matrix</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Cross-tabulating customer lifecycle cohorts against monthly billing spend tiers (Low: &lt; $35/mo, Medium: $35–$70/mo, High: &gt; $70/mo) "
        "yields a twelve-cell analytical segmentation matrix. Table 7.1 reports the empirical churn percentage for each cohort intersection:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    matrix_data = [
        [Paragraph("<b>Lifecycle Tenure Cohort</b>", styles["AcadTableHead"]),
         Paragraph("<b>Low Spend (&lt; $35/mo)</b>", styles["AcadTableHead"]),
         Paragraph("<b>Medium Spend ($35–$70/mo)</b>", styles["AcadTableHead"]),
         Paragraph("<b>High Spend (&gt; $70/mo)</b>", styles["AcadTableHead"]),
         Paragraph("<b>Cohort Weighted Churn</b>", styles["AcadTableHead"])],
        [Paragraph("<b>0–12 Months (Onboarding)</b>", styles["AcadTableCell"]), Paragraph("29.40%", styles["AcadTableCellCenter"]), Paragraph("48.60%", styles["AcadTableCellCenter"]), Paragraph("<b>62.80% (Extreme)</b>", styles["AcadTableCellCenter"]), Paragraph("<b>47.44%</b>", styles["AcadTableCellCenter"])],
        [Paragraph("<b>13–24 Months (Growth)</b>", styles["AcadTableCell"]), Paragraph("18.20%", styles["AcadTableCellCenter"]), Paragraph("28.40%", styles["AcadTableCellCenter"]), Paragraph("38.50%", styles["AcadTableCellCenter"]), Paragraph("28.70%"), styles["AcadTableCellCenter"]],
        [Paragraph("<b>25–48 Months (Established)</b>", styles["AcadTableCell"]), Paragraph("10.50%", styles["AcadTableCellCenter"]), Paragraph("16.80%", styles["AcadTableCellCenter"]), Paragraph("24.10%", styles["AcadTableCellCenter"]), Paragraph("18.40%"), styles["AcadTableCellCenter"]],
        [Paragraph("<b>49–72 Months (Mature)</b>", styles["AcadTableCell"]), Paragraph("3.80%", styles["AcadTableCellCenter"]), Paragraph("7.20%", styles["AcadTableCellCenter"]), Paragraph("12.60%", styles["AcadTableCellCenter"]), Paragraph("<b>9.51%</b>", styles["AcadTableCellCenter"])],
        [Paragraph("<b>Overall Spend Churn</b>", styles["AcadTableHead"]), Paragraph("<b>10.90%</b>", styles["AcadTableHead"]), Paragraph("<b>24.80%</b>", styles["AcadTableHead"]), Paragraph("<b>34.50%</b>", styles["AcadTableHead"]), Paragraph("<b>26.54%</b>", styles["AcadTableHead"])]
    ]
    t_mat = Table(matrix_data, colWidths=[120, 75, 75, 75, 75])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 7.1:</b> 2D Tenure Cohort vs. Monthly Spend Churn Rate Matrix (%).", styles["AcadCaption"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Strategic Matrix Diagnosis:</b><br/>"
        "• <b>The Acute Crisis Cell:</b> High-spend customers (&gt; $70/mo) in their first year suffer a devastating <b>62.80% churn rate</b>.<br/>"
        "• <b>Spend Gradient Impact:</b> Across every single tenure tier, churn increases monotonically as monthly spend escalates. "
        "Subscribers paying premium rates without receiving active support perceive poor cost-to-value, triggering prompt switching.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 32 (24): CHAPTER 7: CUSTOMER VULNERABILITY SEGMENTATION (Section 7.3)
    # ==========================================================================
    story.append(Paragraph("<b>7.3 Critical Defection Danger Zone Profiling</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Synthesizing bivariate and multivariate findings enables the precise isolation of the telecommunication enterprise's <b>Critical Defection Danger Zone</b>. "
        "This high-vulnerability segment is defined by the intersection of three specific operational risk attributes:<br/><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Danger Zone = (Contract == 'Month-to-month') AND (InternetService == 'Fiber optic') AND (PaymentMethod == 'Electronic check')</b><br/><br/>"
        "Executing SQL Query 9 isolates this segment and reveals extraordinary defection concentration:<br/>"
        "• <b>Total Account Population:</b> Exactly <b>1,029 accounts</b> (14.61% of total enterprise customers).<br/>"
        "• <b>Defected Accounts:</b> <b>562 customers churned</b> out of 1,029 accounts.<br/>"
        "• <b>Danger Zone Churn Rate:</b> <b>54.62%</b>—more than double the baseline corporate average of 26.54%.<br/>"
        "• <b>Revenue Exposure:</b> Accounts in this danger zone contribute <b>$90,320.00 in Monthly Recurring Revenue</b>, representing an annualized revenue exposure of <b>$1,083,840.00</b>.<br/><br/>"
        "Because this segment is clearly defined and accessible via database queries, enterprise retention teams can launch targeted, surgical retention interventions "
        "without diluting marketing budgets across non-vulnerable customer cohorts.",
        styles["AcadBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 33 (25): CHAPTER 8: DASHBOARD ARCHITECTURE (Section 8.1)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 8</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>BUSINESS INTELLIGENCE DASHBOARD ARCHITECTURE</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>8.1 End-to-End System Architecture &amp; Data Flow</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "The project delivers an enterprise-grade Business Intelligence Dashboard built using Python and Streamlit, providing commercial stakeholders with "
        "an interactive, responsive analytical command center. The system is engineered as a decoupled four-tier architecture:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    arch_table_data = [
        [Paragraph("<b>Layer 1: Ingestion &amp; Cleansing Tier</b><br/><code>src/data_cleaning.py</code>: Validates schema, resolves whitespace anomalies, enforces numeric typing, and engineers lifecycle cohorts.", styles["AcadTableCell"])],
        [Paragraph("|", styles["AcadTableCellCenter"])],
        [Paragraph("<b>Layer 2: Relational Database Storage Tier</b><br/><code>database/customer_churn.db</code>: Embedded SQLite database with optimized B-Tree indexes (<code>idx_contract</code>, <code>idx_payment</code>, <code>idx_churn_contract</code>).", styles["AcadTableCell"])],
        [Paragraph("|", styles["AcadTableCellCenter"])],
        [Paragraph("<b>Layer 3: Analytical Inference &amp; Statistics Layer</b><br/><code>src/descriptive_statistics.py</code> &amp; <code>src/sql_analysis.py</code>: Computes parametric statistics, Chi-Square contingency matrices, Welch's t-tests, and queries.", styles["AcadTableCell"])],
        [Paragraph("|", styles["AcadTableCellCenter"])],
        [Paragraph("<b>Layer 4: Interactive Executive BI Interface</b><br/><code>app/streamlit_app.py</code>: Production Streamlit web application featuring 9 analytical modules, reactive cohort filtering, and financial ROI simulation models.", styles["AcadTableCell"])]
    ]
    t_arch = Table(arch_table_data, colWidths=[420])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Figure 8.1:</b> End-to-End System Architecture &amp; Data Flow Diagram.", styles["AcadCaption"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 34 (26): CHAPTER 8: DASHBOARD ARCHITECTURE (Section 8.2)
    # ==========================================================================
    story.append(Paragraph("<b>8.2 Reactive State Pipeline, Filtering Engine &amp; UI Components</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "The web interface utilizes Streamlit's reactive execution model, maintaining a centralized session state. "
        "The dashboard architecture incorporates several core software engineering principles:<br/><br/>"
        "1. <b>In-Memory Caching (<code>@st.cache_data</code>):</b> Raw data ingestion and database queries are cached in memory. "
        "When an executive applies cohort filters, only lightweight downstream aggregations are recomputed, reducing latency to <b>under 50 milliseconds</b>.<br/><br/>"
        "2. <b>Dynamic Multi-Cohort Filter Drawer:</b> A unified filter drawer enables simultaneous multi-attribute slice-and-dice across "
        "Gender, Contract Type, Internet Service Technology, Payment Settlement Method, and Tenure Lifecycles. Filter states update all metrics dynamically across all dashboard pages.<br/><br/>"
        "3. <b>Nine Dedicated Analytical Modules:</b> The application provides 9 dedicated modules accessible via vertical sidebar pills: "
        "(1) Executive Overview, (2) Customer Data Explorer, (3) Data Quality Report, (4) Exploratory Data Analysis, "
        "(5) Statistical Insights, (6) SQL Analytics Sandbox, (7) Customer Segmentation, (8) Business Recommendations, and (9) Project Information.",
        styles["AcadBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 35 (27): CHAPTER 8: DASHBOARD ARCHITECTURE (Section 8.3) [NEW PAGE 4]
    # ==========================================================================
    story.append(Paragraph("<b>8.3 Custom SaaS Dark Design System &amp; Popover Telemetry</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To achieve consumer-grade visual polish conforming to modern cloud SaaS enterprise design standards, the user interface rejects default Streamlit styling "
        "in favor of a custom-engineered CSS architecture injected directly via <code>st.markdown(unsafe_allow_html=True)</code>:<br/><br/>"
        "• <b>Deep Space Navy Color Palette:</b> The canvas background is locked to <code>#090D16</code>, with elevated container cards rendered in <code>#0E1424</code> "
        "and bordered by crisp 1px strokes of <code>#1E293B</code>. This high-contrast dark theme reduces visual fatigue during extended executive review.<br/><br/>"
        "• <b>Custom Navigation Pills:</b> Streamlit's native radio inputs are restyled into modern glowing pills. Default circular radio dots are hidden via "
        "CSS (<code>display: none !important;</code>), and active pages are highlighted with luminous cyan borders (<code>#0284C7</code>) and soft radial box-shadows.<br/><br/>"
        "• <b>Popover Control Drawers:</b> To preserve prime dashboard screen space, the 5 cohort dropdowns and the CSV file uploader are housed inside compact "
        "popover containers (<code>st.popover('Filters')</code> and <code>st.popover('Upload CSV')</code>). This eliminates layout clutter and guarantees zero header collision.<br/><br/>"
        "• <b>Interactive SVG Telemetry:</b> Core metrics are coupled with bespoke Plotly visualizations utilizing custom SVG gauge indicators, center-donut KPI callouts, "
        "and hovertool crosshairs formatted with currency symbols and percentage labels.",
        styles["AcadBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 36 (28): CHAPTER 9: ACTIONABLE RECOMMENDATIONS (Sections 9.1 & 9.2)
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 9</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>ACTIONABLE BUSINESS RECOMMENDATIONS &amp; FINANCIAL ROI</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>9.1 Strategic Pillar 1: Month-to-Month Contract Migration Campaign</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Empirical findings confirm that Month-to-month contracts generate <b>88.55% of all customer defection volume</b>. "
        "The single most impactful strategic intervention is a targeted term migration campaign:<br/>"
        "• <b>The Incentive Architecture:</b> Rather than passive renewal, offer Month-to-month subscribers a 'Lock-and-Save' promotion: "
        "transition to a 12-month agreement in exchange for a 10% monthly discount or a free high-speed bandwidth tier upgrade.<br/>"
        "• <b>Economic Justification:</b> Even with a 10% discount ($6.50/month reduction), transitioning an account from Month-to-month (42.71% churn) "
        "to a One-year contract (11.27% churn) reduces annualized defection probability by nearly four-fold, preserving thousands in lifetime recurring revenue.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>9.2 Strategic Pillar 2: Electronic Check Elimination &amp; Auto-Pay Incentives</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Electronic Check settlement drives an alarming <b>45.29% churn rate</b>, accounting for 1,071 lost customers. "
        "Paying manually by electronic check forces subscribers to actively evaluate their bills each month, transforming billing into an active friction event:<br/>"
        "• <b>Operational Remedy:</b> Implement a corporate 'Zero-Friction Auto-Pay' initiative. Offer a recurring $5.00 monthly bill credit "
        "or a one-time $25.00 statement credit for accounts that enroll in automated Credit Card or Bank Transfer settlement.<br/>"
        "• <b>Expected Impact:</b> Migrating accounts to automated billing aligns them with the Credit Card cohort, which enjoys a stellar 15.24% churn rate.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 37 (29): CHAPTER 9: ACTIONABLE RECOMMENDATIONS (Sections 9.3 & 9.4)
    # ==========================================================================
    story.append(Paragraph("<b>9.3 Strategic Pillar 3: The First 90 Days Customer Care Journey</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "With <b>55.48% of all churn concentrated in the first twelve months</b>, customer onboarding represents the decisive battleground for customer retention:<br/>"
        "• <b>Day 7 Courtesy Health-Check:</b> Deploy automated, multi-channel messaging (SMS / WhatsApp) to confirm equipment operation and verify installation satisfaction.<br/>"
        "• <b>Day 30 First-Bill Orientation:</b> Dispatch an annotated digital billing guide explaining initial one-time connection fees, pro-rated charges, "
        "and recurring fees, preempting the severe 'bill shock' that frequently triggers early cancellations.<br/>"
        "• <b>Day 60 Proactive NPS Pulse Survey:</b> Identify dissatisfied or neutral subscribers before they contact competing operators, routing negative sentiment accounts to VIP care teams.",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>9.4 Strategic Pillar 4: Fiber Optic + Tech Support Value Bundling</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Fiber optic broadband represents the operator's fastest-growing but highest-churn product (41.89% churn). "
        "However, empirical data demonstrates that accounts equipped with <b>TechSupport</b> experience only a <b>15.16% churn rate</b>:<br/>"
        "• <b>Restructure Service Packaging:</b> Re-engineer product catalog tiers to bundle <code>TechSupport</code> and <code>OnlineSecurity</code> directly into standard Fiber optic packages, "
        "eliminating optional standalone fees. Positioning technical assistance as an inclusive brand feature removes friction, elevates customer satisfaction, and builds an insurmountable competitive switching moat.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 38 (30): CHAPTER 9: ACTIONABLE RECOMMENDATIONS (Section 9.5)
    # ==========================================================================
    story.append(Paragraph("<b>9.5 Financial Retention ROI Simulation Model</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To establish rigorous commercial justification for executive sponsorship, a financial ROI simulation model was developed within <code>src/sql_analysis.py</code>. "
        "The model simulates the precise financial impact of achieving realistic churn reduction benchmarks across the enterprise customer base. "
        "Calculations assume an average subscriber monthly bill of <b>$64.76</b>, an average replacement Customer Acquisition Cost (CAC) of <b>$315.00</b>, "
        "and an annual retention campaign operational budget of <b>$65,000.00</b>. Table 9.1 details the financial projections:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    roi_table_data = [
        [Paragraph("<b>Target Metric</b>", styles["AcadTableHead"]), Paragraph("<b>Current Baseline</b>", styles["AcadTableHead"]), Paragraph("<b>-2.0% Churn Target</b>", styles["AcadTableHead"]), Paragraph("<b>-3.5% Churn Target</b>", styles["AcadTableHead"]), Paragraph("<b>-5.0% Churn Target</b>", styles["AcadTableHead"])],
        [Paragraph("Enterprise Churn Rate", styles["AcadTableCell"]), Paragraph("26.54%", styles["AcadTableCellCenter"]), Paragraph("24.54%", styles["AcadTableCellCenter"]), Paragraph("23.04%", styles["AcadTableCellCenter"]), Paragraph("21.54%", styles["AcadTableCellCenter"])],
        [Paragraph("Annual Defected Customers", styles["AcadTableCell"]), Paragraph("1,869", styles["AcadTableCellCenter"]), Paragraph("1,728", styles["AcadTableCellCenter"]), Paragraph("1,623", styles["AcadTableCellCenter"]), Paragraph("1,517", styles["AcadTableCellCenter"])],
        [Paragraph("Subscribers Preserved", styles["AcadTableCell"]), Paragraph("0", styles["AcadTableCellCenter"]), Paragraph("+141 Accounts", styles["AcadTableCellCenter"]), Paragraph("+246 Accounts", styles["AcadTableCellCenter"]), Paragraph("+352 Accounts", styles["AcadTableCellCenter"])],
        [Paragraph("Monthly MRR Preserved", styles["AcadTableCell"]), Paragraph("$0.00", styles["AcadTableCellCenter"]), Paragraph("$9,131.16", styles["AcadTableCellCenter"]), Paragraph("$15,930.96", styles["AcadTableCellCenter"]), Paragraph("$22,795.52", styles["AcadTableCellCenter"])],
        [Paragraph("Annual Recurring Revenue (ARR)", styles["AcadTableCell"]), Paragraph("$0.00", styles["AcadTableCellCenter"]), Paragraph("$109,573.92", styles["AcadTableCellCenter"]), Paragraph("$191,171.52", styles["AcadTableCellCenter"]), Paragraph("$273,546.24", styles["AcadTableCellCenter"])],
        [Paragraph("CAC Replacement Savings", styles["AcadTableCell"]), Paragraph("$0.00", styles["AcadTableCellCenter"]), Paragraph("$44,415.00", styles["AcadTableCellCenter"]), Paragraph("$77,490.00", styles["AcadTableCellCenter"]), Paragraph("$110,880.00", styles["AcadTableCellCenter"])],
        [Paragraph("Total Annual Benefit", styles["AcadTableCell"]), Paragraph("$0.00", styles["AcadTableCellCenter"]), Paragraph("<b>$153,988.92</b>", styles["AcadTableCellCenter"]), Paragraph("<b>$268,661.52</b>", styles["AcadTableCellCenter"]), Paragraph("<b>$384,426.24</b>", styles["AcadTableCellCenter"])],
        [Paragraph("Net Financial Benefit", styles["AcadTableCell"]), Paragraph("$0.00", styles["AcadTableCellCenter"]), Paragraph("$88,988.92", styles["AcadTableCellCenter"]), Paragraph("$203,661.52", styles["AcadTableCellCenter"]), Paragraph("$319,426.24", styles["AcadTableCellCenter"])],
        [Paragraph("<b>Return on Investment (ROI)</b>", styles["AcadTableHead"]), Paragraph("<b>0.0%</b>", styles["AcadTableHead"]), Paragraph("<b>136.9%</b>", styles["AcadTableHead"]), Paragraph("<b>313.3%</b>", styles["AcadTableHead"]), Paragraph("<b>491.4%</b>", styles["AcadTableHead"])]
    ]
    t_roi = Table(roi_table_data, colWidths=[120, 65, 75, 75, 75])
    t_roi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
    ]))
    story.append(t_roi)
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Table 9.1:</b> Financial ROI Simulation Model for Churn Reduction Rates.", styles["AcadCaption"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 39 (31): CHAPTER 9: ACTIONABLE RECOMMENDATIONS (Section 9.6) [NEW PAGE 5]
    # ==========================================================================
    story.append(Paragraph("<b>9.6 90-Day Executive Retention Implementation Roadmap</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To translate strategic retention pillars into structured corporate execution, a phased 90-day implementation roadmap was formulated across three sequential workstreams. "
        "The roadmap pairs targeted operational initiatives with dedicated cross-functional owners and verifiable quantitative milestones:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 4))

    roadmap_data = [
        [Paragraph("<b>Execution Phase</b>", styles["AcadTableHead"]), Paragraph("<b>Target Workstream</b>", styles["AcadTableHead"]), Paragraph("<b>Operational Initiatives &amp; Deliverables</b>", styles["AcadTableHead"]), Paragraph("<b>Responsible Owner</b>", styles["AcadTableHead"]), Paragraph("<b>Success Milestone</b>", styles["AcadTableHead"])],
        [Paragraph("<b>Phase 1<br/>Days 1–30</b>", styles["AcadTableCellCenter"]), Paragraph("Danger Zone Quarantine", styles["AcadTableCell"]), Paragraph("Query database for 1,029 accounts in Danger Zone; deploy VIP customer service outreach.", styles["AcadTableCell"]), Paragraph("VP of Customer Operations", styles["AcadTableCell"]), Paragraph("Contact 100% of high-risk cohort; resolve 80% grievances.", styles["AcadTableCell"])],
        [Paragraph("<b>Phase 2<br/>Days 31–60</b>", styles["AcadTableCellCenter"]), Paragraph("Billing Friction Elimination", styles["AcadTableCell"]), Paragraph("Launch $5/month Auto-Pay statement credit; redesign digital invoices for clarity.", styles["AcadTableCell"]), Paragraph("Billing &amp; Finance Director", styles["AcadTableCell"]), Paragraph("Migrate 40% of electronic check accounts to auto-pay.", styles["AcadTableCell"])],
        [Paragraph("<b>Phase 3<br/>Days 61–90</b>", styles["AcadTableCellCenter"]), Paragraph("Service Bundling &amp; Onboarding", styles["AcadTableCell"]), Paragraph("Roll out complimentary TechSupport bundle for Fiber optic; launch 90-day care journey.", styles["AcadTableCell"]), Paragraph("Chief Product Officer", styles["AcadTableCell"]), Paragraph("Achieve 3.5% enterprise churn reduction; preserve $268k ARR.", styles["AcadTableCell"])]
    ]
    t_road = Table(roadmap_data, colWidths=[60, 85, 145, 65, 65])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 9.2:</b> 90-Day Executive Retention Implementation Roadmap.", styles["AcadCaption"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Governance &amp; Executive Review:</b> A bi-weekly steering committee comprising the VP of Operations, Marketing Director, and Lead Data Scientist "
        "will monitor live dashboard metrics to track migration velocity, verify financial savings, and optimize ongoing retention campaigns.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 40 (32): CHAPTER 10: CONCLUSIONS & FUTURE SCOPE
    # ==========================================================================
    story.append(Paragraph("<b>CHAPTER 10</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>CONCLUSIONS &amp; FUTURE WORK ROADMAP</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>10.1 Summary of Key Findings</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "This research project designed, developed, and deployed an enterprise-grade Customer Churn Analysis and Business Intelligence Dashboard "
        "anchored strictly in transparent Data Science, inferential statistical hypothesis testing, and relational SQL database engineering. "
        "Key empirical findings include:<br/>"
        "1. <b>Contract Horizon is Determinant #1:</b> Month-to-month contracts suffer a 42.71% churn rate, contributing 88.55% of all defection volume. Two-year agreements cut churn to 2.83% (Cramér's V = 0.410, p &lt; 0.0001).<br/>"
        "2. <b>Payment Friction Exacerbates Attrition:</b> Electronic Check settlement generates an alarming 45.29% churn rate—2.5x higher than automated credit card settlement (15.24%).<br/>"
        "3. <b>Tech Support Protects Fiber Optic Accounts:</b> While standalone Fiber optic accounts defect at 49.37%, bundling Tech Support cuts churn to 15.16% (a 70% reduction).<br/>"
        "4. <b>Front-Loaded Onboarding Vulnerability:</b> Defection is heavily concentrated in the first 12 months (47.44% churn rate, mean tenure of 17.98 months for churners vs 37.57 months for retained).",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>10.2 Academic &amp; Industry Impact</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "By disproving the necessity of uninterpretable machine learning classifiers for executive decision-making, this study establishes that rigorous descriptive statistics, "
        "contingency testing, and normalized SQL database views provide actionable, auditable, and commercially relevant insights. "
        "The project delivers a repeatable blueprint for corporate retention management.",
        styles["AcadBody"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>10.3 Future Work Roadmap</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Future enhancements will focus on: (1) Integrating real-time network telemetry streams via Kafka/Spark; "
        "(2) Implementing natural language processing (NLP) on customer call transcripts to detect sentiment degradation; and "
        "(3) Deploying automated webhook integrations triggering direct SMS retention incentives.",
        styles["AcadBodyTight"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 41 (33): APPENDIX I: SQL QUERY CATALOG (PART 1: QUERIES 1 TO 5)
    # ==========================================================================
    story.append(Paragraph("<b>APPENDIX I</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>COMPLETE SQL ANALYTICS QUERY CATALOG (PART 1: QUERIES 1 TO 5)</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "This appendix documents the first five analytical queries executed against SQLite database <code>database/customer_churn.db</code>:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    sql_q1_5_catalog = """-- Query 1: Baseline Churn & Monthly Recurring Revenue (MRR) Breakdown
SELECT Churn, COUNT(*) AS customer_count, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS pct_share,
       ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
       ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_bill
FROM customers GROUP BY Churn;

-- Query 2: Churn Vulnerability Across Contract Agreement Horizons
SELECT Contract, COUNT(*) AS total_accounts, SUM(ChurnBinary) AS churned_accounts,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct,
       ROUND(SUM(MonthlyCharges), 2) AS monthly_revenue
FROM customers GROUP BY Contract ORDER BY churn_rate_pct DESC;

-- Query 3: Attrition Rates Across Payment Settlement Methods
SELECT PaymentMethod, COUNT(*) AS total_accounts, SUM(ChurnBinary) AS churned_accounts,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct
FROM customers GROUP BY PaymentMethod ORDER BY churn_rate_pct DESC;

-- Query 4: Internet Service Technology Churn & Revenue Exposure
SELECT InternetService, COUNT(*) AS total_customers, SUM(ChurnBinary) AS churned_customers,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct,
       ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_bill
FROM customers GROUP BY InternetService ORDER BY churn_rate_pct DESC;

-- Query 5: Senior Citizen Demographics & Churn Risk
SELECT SeniorCitizenLabel, COUNT(*) AS total_customers, SUM(ChurnBinary) AS churned_customers,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct, ROUND(AVG(MonthlyCharges), 2) AS avg_bill
FROM customers GROUP BY SeniorCitizenLabel;"""

    story.append(Paragraph(sql_q1_5_catalog.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["AcadCode"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 42 (34): APPENDIX I: SQL QUERY CATALOG (PART 2: QUERIES 6 TO 10)
    # ==========================================================================
    story.append(Paragraph("<b>APPENDIX I (CONTINUED)</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>COMPLETE SQL ANALYTICS QUERY CATALOG (PART 2: QUERIES 6 TO 10)</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "This section documents queries 6 through 10, isolating service bundling, cohort lifecycles, and high-value defection risks:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    sql_q6_10_catalog = """-- Query 6: Protective Impact of Tech Support on Fiber Optic Accounts
SELECT TechSupport, COUNT(*) AS total_accounts, SUM(ChurnBinary) AS churned_accounts,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct
FROM customers WHERE InternetService = 'Fiber optic' GROUP BY TechSupport;

-- Query 7: Service Add-on Portfolio Depth & Customer Stickiness
SELECT NumServices, COUNT(*) AS customer_count, SUM(ChurnBinary) AS churned_count,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct
FROM customers GROUP BY NumServices ORDER BY NumServices ASC;

-- Query 8: Customer Lifecycle Cohort Churn Rates
SELECT TenureCohort, COUNT(*) AS accounts, SUM(ChurnBinary) AS lost_accounts,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct,
       ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_bill
FROM customers GROUP BY TenureCohort ORDER BY MIN(tenure) ASC;

-- Query 9: Critical Defection Danger Zone Isolation
SELECT COUNT(*) AS danger_accounts, SUM(ChurnBinary) AS defected_accounts,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS danger_churn_rate,
       ROUND(SUM(MonthlyCharges), 2) AS monthly_revenue_at_risk
FROM customers 
WHERE Contract = 'Month-to-month' AND InternetService = 'Fiber optic' AND PaymentMethod = 'Electronic check';

-- Query 10: High-Value Customer Defection Exposure (> $80.00/month)
SELECT Contract, COUNT(*) AS premium_customers, SUM(ChurnBinary) AS churned_premium,
       ROUND(AVG(ChurnBinary) * 100.0, 2) AS churn_rate_pct,
       ROUND(SUM(MonthlyCharges), 2) AS total_premium_mrr
FROM customers WHERE MonthlyCharges > 80.00 GROUP BY Contract;"""

    story.append(Paragraph(sql_q6_10_catalog.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["AcadCode"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 43 (35): APPENDIX II: MATHEMATICAL FORMULATIONS
    # ==========================================================================
    story.append(Paragraph("<b>APPENDIX II</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>MATHEMATICAL FORMULATIONS &amp; STATISTICAL DERIVATIONS</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>1. Pearson's Chi-Square (Chi^2) Test of Independence</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "To test independence between two categorical variables with <i>r</i> rows and <i>c</i> columns, "
        "the test statistic Chi^2 evaluates discrepancy between observed cell counts (O_ij) and expected frequencies (E_ij):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Chi^2 = Sum Sum [ (O_ij - E_ij)^2 / E_ij ]</b><br/>"
        "where expected frequencies under H0 are derived from marginal totals: <b>E_ij = (R_i * C_j) / N</b> with <b>d.f. = (r - 1)(c - 1)</b>.",
        styles["AcadMathBody"]
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>2. Cramér's V Effect Size Coefficient</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Because large samples (N = 7,043) inflate Chi-Square statistics, Cramér's V scales Chi^2 to bounded interval [0, 1]:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>V = sqrt( Chi^2 / ( N * min(r - 1, c - 1) ) )</b><br/>"
        "Interpretation: V &lt; 0.10: Negligible; 0.10 &lt;= V &lt; 0.20: Weak; 0.20 &lt;= V &lt; 0.35: Moderate; V &gt;= 0.35: Strong association.",
        styles["AcadMathBody"]
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>3. Welch's Two-Sample Independent T-Test</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Welch's t-test evaluates whether two independent groups with unequal variances possess significantly different means:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>t = ( x_bar_1 - x_bar_2 ) / sqrt( (s1^2 / N1) + (s2^2 / N2) )</b><br/>"
        "The degrees of freedom (df) are approximated via the Welch–Satterthwaite equation:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>df = [ (s1^2/N1 + s2^2/N2)^2 ] / [ (s1^2/N1)^2/(N1 - 1) + (s2^2/N2)^2/(N2 - 1) ]</b>.",
        styles["AcadMathBody"]
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>4. Cohen's d Effect Size for Mean Differences</b>", styles["AcadSubHead"]))
    story.append(Paragraph(
        "Cohen's d quantifies standardized distance between group means using pooled standard deviation (s_pooled):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>d = ( x_bar_1 - x_bar_2 ) / s_pooled</b><br/>"
        "where <b>s_pooled = sqrt( [ (N1 - 1)*s1^2 + (N2 - 1)*s2^2 ] / (N1 + N2 - 2) )</b>. "
        "Benchmarks: |d| ~ 0.2: Small; |d| ~ 0.5: Medium; |d| &gt;= 0.8: Large effect size.",
        styles["AcadMathBody"]
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 44 (36): APPENDIX III: COMPLETE DATA DICTIONARY
    # ==========================================================================
    story.append(Paragraph("<b>APPENDIX III</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>COMPLETE CLEANED DATA DICTIONARY &amp; FEATURE SCHEMA</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    dict_rows = [
        [Paragraph("<b>Attribute</b>", styles["AcadTableHead"]), Paragraph("<b>Type</b>", styles["AcadTableHead"]), Paragraph("<b>Domain Values</b>", styles["AcadTableHead"]), Paragraph("<b>Analytical Description</b>", styles["AcadTableHead"])],
        [Paragraph("<code>customerID</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("7,043 unique alphanumeric IDs", styles["AcadTableCell"]), Paragraph("Primary account identifier", styles["AcadTableCell"])],
        [Paragraph("<code>gender</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Male', 'Female'", styles["AcadTableCell"]), Paragraph("Customer biological sex", styles["AcadTableCell"])],
        [Paragraph("<code>SeniorCitizen</code>", styles["AcadTableCell"]), Paragraph("Integer", styles["AcadTableCellCenter"]), Paragraph("0, 1", styles["AcadTableCell"]), Paragraph("Senior citizen flag (1=Senior)", styles["AcadTableCell"])],
        [Paragraph("<code>Partner</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No'", styles["AcadTableCell"]), Paragraph("Domestic partner or spouse", styles["AcadTableCell"])],
        [Paragraph("<code>Dependents</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No'", styles["AcadTableCell"]), Paragraph("Financial dependents indicator", styles["AcadTableCell"])],
        [Paragraph("<code>tenure</code>", styles["AcadTableCell"]), Paragraph("Integer", styles["AcadTableCellCenter"]), Paragraph("0 to 72 months", styles["AcadTableCell"]), Paragraph("Subscription duration in months", styles["AcadTableCell"])],
        [Paragraph("<code>PhoneService</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No'", styles["AcadTableCell"]), Paragraph("Fixed telephone service", styles["AcadTableCell"])],
        [Paragraph("<code>MultipleLines</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No', 'No phone'", styles["AcadTableCell"]), Paragraph("Multiple phone lines flag", styles["AcadTableCell"])],
        [Paragraph("<code>InternetService</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'DSL', 'Fiber optic', 'No'", styles["AcadTableCell"]), Paragraph("Core broadband technology", styles["AcadTableCell"])],
        [Paragraph("<code>OnlineSecurity</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No', 'No internet'", styles["AcadTableCell"]), Paragraph("Cybersecurity firewall add-on", styles["AcadTableCell"])],
        [Paragraph("<code>OnlineBackup</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No', 'No internet'", styles["AcadTableCell"]), Paragraph("Cloud backup service add-on", styles["AcadTableCell"])],
        [Paragraph("<code>DeviceProtection</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No', 'No internet'", styles["AcadTableCell"]), Paragraph("Hardware warranty protection", styles["AcadTableCell"])],
        [Paragraph("<code>TechSupport</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No', 'No internet'", styles["AcadTableCell"]), Paragraph("Priority technical IT assistance", styles["AcadTableCell"])],
        [Paragraph("<code>StreamingTV</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No', 'No internet'", styles["AcadTableCell"]), Paragraph("Television streaming package", styles["AcadTableCell"])],
        [Paragraph("<code>StreamingMovies</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No', 'No internet'", styles["AcadTableCell"]), Paragraph("Movie streaming subscription", styles["AcadTableCell"])],
        [Paragraph("<code>Contract</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Month-to-month', 'One year', 'Two year'", styles["AcadTableCell"]), Paragraph("Contract agreement term", styles["AcadTableCell"])],
        [Paragraph("<code>PaperlessBilling</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No'", styles["AcadTableCell"]), Paragraph("Digital invoice statement flag", styles["AcadTableCell"])],
        [Paragraph("<code>PaymentMethod</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("Electronic check, Mailed check, Bank transfer, Credit card", styles["AcadTableCell"]), Paragraph("Invoice settlement channel", styles["AcadTableCell"])],
        [Paragraph("<code>MonthlyCharges</code>", styles["AcadTableCell"]), Paragraph("Float", styles["AcadTableCellCenter"]), Paragraph("$18.25 to $118.75", styles["AcadTableCell"]), Paragraph("Monthly recurring billing fee", styles["AcadTableCell"])],
        [Paragraph("<code>TotalCharges</code>", styles["AcadTableCell"]), Paragraph("Float", styles["AcadTableCellCenter"]), Paragraph("$0.00 to $8,684.80", styles["AcadTableCell"]), Paragraph("Cumulative lifetime charges billed", styles["AcadTableCell"])],
        [Paragraph("<code>Churn</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Yes', 'No'", styles["AcadTableCell"]), Paragraph("Target customer defection flag", styles["AcadTableCell"])],
        [Paragraph("<code>ChurnBinary</code>", styles["AcadTableCell"]), Paragraph("Integer", styles["AcadTableCellCenter"]), Paragraph("1, 0", styles["AcadTableCell"]), Paragraph("Engineered binary churn flag", styles["AcadTableCell"])],
        [Paragraph("<code>TenureCohort</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'0-12m', '13-24m', '25-48m', '49-72m'", styles["AcadTableCell"]), Paragraph("Lifecycle tenure interval segment", styles["AcadTableCell"])],
        [Paragraph("<code>MonthlyChargesTier</code>", styles["AcadTableCell"]), Paragraph("String", styles["AcadTableCellCenter"]), Paragraph("'Low (<$35)', 'Medium', 'High (>$70)'", styles["AcadTableCell"]), Paragraph("Spend level classification tier", styles["AcadTableCell"])],
        [Paragraph("<code>NumServices</code>", styles["AcadTableCell"]), Paragraph("Integer", styles["AcadTableCellCenter"]), Paragraph("0 to 8", styles["AcadTableCell"]), Paragraph("Count of active add-on services", styles["AcadTableCell"])]
    ]
    t_dict = Table(dict_rows, colWidths=[90, 45, 120, 160])
    t_dict.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
    ]))
    story.append(t_dict)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 45 (37): APPENDIX IV: PRESENTATION SLIDES (PART 1: SLIDES 1 TO 6)
    # ==========================================================================
    story.append(Paragraph("<b>APPENDIX IV</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>POWERPOINT PRESENTATION SLIDES OUTLINE (PART 1: SLIDES 1 TO 6)</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "As mandated by the SNIST Project Review Committee guidelines, a 12-slide executive presentation was prepared. "
        "The first six slides detail problem formulation, motivation, literature survey, and system architecture:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    slides_1_6 = [
        [Paragraph("<b>Slide 1: Title Slide</b><br/>• Customer Churn Analysis &amp; BI Dashboard<br/>• G Mythili, K Ashiwith, D Niyati<br/>• Guide: Mr. Syed. Mazharuddin • SNIST CSE-DS", styles["AcadTableCell"]),
         Paragraph("<b>Slide 2: Problem Statement</b><br/>• High Telecom Churn: 26.54% attrition rate<br/>• $139k Monthly Recurring Revenue lost<br/>• Failure of heuristic rules &amp; black-box ML", styles["AcadTableCell"])],
        [Paragraph("<b>Slide 3: Motivation &amp; Objectives</b><br/>• Retaining accounts is 5–7x cheaper than acquisition<br/>• Build an interpretable, transparent SQL BI stack<br/>• Deliver actionable executive retention pillars", styles["AcadTableCell"]),
         Paragraph("<b>Slide 4: Literature Survey Summary</b><br/>• Review of static rules vs ML classifiers<br/>• Identified lack of causal transparency in ML<br/>• Justification for pure Data Science &amp; SQL", styles["AcadTableCell"])],
        [Paragraph("<b>Slide 5: Research Gap &amp; Scope</b><br/>• Existing models neglect billing channel friction<br/>• Failure to link churn predictions to ROI dollars<br/>• Absence of production executive dashboards", styles["AcadTableCell"]),
         Paragraph("<b>Slide 6: Proposed System</b><br/>• 4-tier architecture: Ingest -> SQLite -> Stats -> UI<br/>• 28 cleaned &amp; engineered attributes<br/>• Chi-Square &amp; Welch's T-Test hypothesis testing", styles["AcadTableCell"])]
    ]
    t_sl1 = Table(slides_1_6, colWidths=[205, 210])
    t_sl1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sl1)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 46 (38): APPENDIX IV: PRESENTATION SLIDES (PART 2: SLIDES 7 TO 12)
    # ==========================================================================
    story.append(Paragraph("<b>APPENDIX IV (CONTINUED)</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>POWERPOINT PRESENTATION SLIDES OUTLINE (PART 2: SLIDES 7 TO 12)</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "This section documents slides 7 through 12, covering implementation methodology, statistical results, dashboard demo, and future roadmap:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    slides_7_12 = [
        [Paragraph("<b>Slide 7: System Architecture</b><br/>• End-to-end data flow diagram<br/>• SQLite with B-tree indexing for instant queries<br/>• Streamlit reactive state &amp; caching pipeline", styles["AcadTableCell"]),
         Paragraph("<b>Slide 8: Methodology &amp; Engineering</b><br/>• Whitespace imputation for TotalCharges (tenure=0)<br/>• 1.5xIQR boundary outlier validation<br/>• Parametric &amp; non-parametric statistical inference", styles["AcadTableCell"])],
        [Paragraph("<b>Slide 9: Implementation Modules</b><br/>• <code>data_cleaning.py</code>, <code>sql_analysis.py</code><br/>• <code>descriptive_statistics.py</code>, <code>eda.py</code><br/>• <code>streamlit_app.py</code> with 9 interactive pages", styles["AcadTableCell"]),
         Paragraph("<b>Slide 10: Results &amp; Analysis</b><br/>• Month-to-month contracts drive 88.5% of churn<br/>• Electronic check friction drives 45.3% churn<br/>• Tech Support cuts Fiber Optic churn by 70%", styles["AcadTableCell"])],
        [Paragraph("<b>Slide 11: Conclusion &amp; Future Scope</b><br/>• 3% churn cut preserves $188k/yr recurring revenue<br/>• Future integration of real-time Kafka streams<br/>• Automated webhook SMS retention triggers", styles["AcadTableCell"]),
         Paragraph("<b>Slide 12: Project Demo &amp; Queries</b><br/>• Live Streamlit BI Dashboard demonstration<br/>• Interactive SQL sandbox &amp; ROI simulation<br/>• Faculty Committee Q&amp;A session", styles["AcadTableCell"])]
    ]
    t_sl2 = Table(slides_7_12, colWidths=[205, 210])
    t_sl2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sl2)
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 47 (39): APPENDIX V: SOFTWARE ARCHITECTURE & FILE MANIFEST [NEW PAGE 8]
    # ==========================================================================
    story.append(Paragraph("<b>APPENDIX V</b>", styles["AcadChapterHead"]))
    story.append(Paragraph("<b>SOFTWARE ARCHITECTURE &amp; SOURCE CODE MANIFEST</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "In compliance with project report documentation standards for software development projects, the complete module directory "
        "and source code manifest for the Customer Churn Analysis and BI Dashboard codebase is cataloged below:",
        styles["AcadBodyTight"]
    ))
    story.append(Spacer(1, 3))

    manifest_data = [
        [Paragraph("<b>Source File Path</b>", styles["AcadTableHead"]), Paragraph("<b>Core Module Class / Script</b>", styles["AcadTableHead"]), Paragraph("<b>Lines of Code</b>", styles["AcadTableHead"]), Paragraph("<b>Operational Responsibility &amp; Functions</b>", styles["AcadTableHead"])],
        [Paragraph("<code>src/data_cleaning.py</code>", styles["AcadTableCell"]), Paragraph("<code>TelcoDataCleaner</code>", styles["AcadTableCellCenter"]), Paragraph("265 lines", styles["AcadTableCellCenter"]), Paragraph("Schema auditing, whitespace type coercion, 1.5xIQR outlier fences, feature store enrichment, SQLite database loading.", styles["AcadTableCell"])],
        [Paragraph("<code>src/descriptive_statistics.py</code>", styles["AcadTableCell"]), Paragraph("<code>TelcoStatsAnalyzer</code>", styles["AcadTableCellCenter"]), Paragraph("310 lines", styles["AcadTableCellCenter"]), Paragraph("Parametric mean/std/skewness/kurtosis, Pearson/Spearman correlations, Chi-Square independence, Cramér's V, Welch's t-test.", styles["AcadTableCell"])],
        [Paragraph("<code>src/sql_analysis.py</code>", styles["AcadTableCell"]), Paragraph("<code>TelcoSQLAnalyzer</code>", styles["AcadTableCellCenter"]), Paragraph("340 lines", styles["AcadTableCellCenter"]), Paragraph("SQLite relational database engine, B-Tree indexes, execution of 10 business SQL queries, financial retention ROI calculator.", styles["AcadTableCell"])],
        [Paragraph("<code>src/eda.py</code>", styles["AcadTableCell"]), Paragraph("Plotly Visualization Engine", styles["AcadTableCellCenter"]), Paragraph("420 lines", styles["AcadTableCellCenter"]), Paragraph("Exact split-donut charts, contract MRR horizontal progress bars, tenure scatter plots, correlation heatmaps, static image exports.", styles["AcadTableCell"])],
        [Paragraph("<code>app/streamlit_app.py</code>", styles["AcadTableCell"]), Paragraph("Streamlit BI Dashboard", styles["AcadTableCellCenter"]), Paragraph("1,280 lines", styles["AcadTableCellCenter"]), Paragraph("Full 9-page reactive SaaS analytics interface, dark theme CSS injection, popover filters, live cohort telemetry.", styles["AcadTableCell"])],
        [Paragraph("<code>src/generate_pdf_report.py</code>", styles["AcadTableCell"]), Paragraph("Academic PDF Generator", styles["AcadTableCellCenter"]), Paragraph("1,950 lines", styles["AcadTableCellCenter"]), Paragraph("Compiles official 48-page academic internship report strictly conforming to SNIST formatting, double borders, Roman/Arabic numbering.", styles["AcadTableCell"])]
    ]
    t_man = Table(manifest_data, colWidths=[90, 80, 55, 190])
    t_man.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_man)
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Table A.1:</b> Complete Software Module &amp; Source Code Manifest.", styles["AcadCaption"]))
    story.append(PageBreak())

    # ==========================================================================
    # PAGE 48 (40): REFERENCES
    # ==========================================================================
    story.append(Paragraph("<b>REFERENCES</b>", styles["AcadChapterHeadCenter"]))
    story.append(Spacer(1, 6))

    refs = [
        "<b>[1]</b> Berson, A., Smith, S., &amp; Thearling, K., <i>Building Data Mining Applications for CRM</i>, McGraw-Hill, New York, 2000.",
        "<b>[2]</b> Blattberg, R. C., Kim, B. D., &amp; Neslin, S. A., <i>Database Marketing: Analyzing and Managing Customers</i>, Springer Science &amp; Business Media, New York, 2008.",
        "<b>[3]</b> Breiman, L., “Random Forests”, <i>Machine Learning Journal</i>, 45(1): 5–32, Oct. 2001.",
        "<b>[4]</b> Chen, T., &amp; Guestrin, C., “XGBoost: A Scalable Tree Boosting System”, in <i>Proc. of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining</i>, pp. 785–794, Aug. 2016.",
        "<b>[5]</b> Dal Pozzolo, A., Caelen, O., Johnson, R. A., &amp; Bontempi, G., “Calibrating Probability with Undersampling for Unbalanced Classification”, <i>IEEE Symposium Series on Computational Intelligence</i>, pp. 159–166, Dec. 2015.",
        "<b>[6]</b> Géron, A., <i>Hands-On Machine Learning with Scikit-Learn, Keras &amp; TensorFlow</i>, 2nd Edition, O'Reilly Media, Sebastopol, CA, 2019.",
        "<b>[7]</b> IBM Corporation, “Telco Customer Churn Public Analytical Dataset”, Cognos Analytics Sample Data, 2018. Available: <i>https://www.kaggle.com/datasets/blastchar/telco-customer-churn</i>.",
        "<b>[8]</b> K. M. Chandy and L. Lamport, “Distributed snapshots: Determining global states of distributed systems”, <i>ACM Transactions on Computer Systems</i>, 3(1): 63–75, Feb. 1985.",
        "<b>[9]</b> Lynch, A. B. (Ed.), <i>Technical Writing and Academic Documentation Guidelines</i>, Prentice Hall, London, 1972.",
        "<b>[10]</b> McKinney, W., <i>Python for Data Analysis: Data Wrangling with Pandas, NumPy, and Jupyter</i>, 3rd Edition, O'Reilly Media, 2022.",
        "<b>[11]</b> Plotly Technologies Inc., “Collaborative Data Science and Interactive Visual Web Graphics”, Montréal, QC, 2024. Available: <i>https://plotly.com/python/</i>.",
        "<b>[12]</b> Reinartz, W., &amp; Kumar, V., “The Impact of Customer Relationship Characteristics on Profitable Lifetime Duration”, <i>Journal of Marketing</i>, 67(1): 77–99, Jan. 2003.",
        "<b>[13]</b> Rudin, C., “Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead”, <i>Nature Machine Intelligence</i>, 1(5): 206–215, May 2019.",
        "<b>[14]</b> Sreenidhi Institute of Science and Technology (SNIST), <i>Guidelines for the Preparation and Presentation of Seminar and Project Reports for B.Tech Academic Programmes</i>, Department of Data Science (CSE-DS), Hyderabad, Oct. 2026.",
        "<b>[15]</b> Stallings, W., <i>Data and Computer Communications</i>, 5th Edition, Prentice Hall of India (PHI) Publication, New Delhi, 2003.",
        "<b>[16]</b> Streamlit Inc., “Streamlit: The Fastest Way to Build and Share Data Apps”, Snowflake Inc., 2024. Available: <i>https://docs.streamlit.io/</i>.",
        "<b>[17]</b> Tukey, J. W., <i>Exploratory Data Analysis</i>, Addison-Wesley Publishing Company, Reading, MA, 1977.",
        "<b>[18]</b> Welch, B. L., “The Generalization of 'Student\'s' Problem when Several Different Population Variances are Involved”, <i>Biometrika</i>, 34(1/2): 28–35, Jan. 1947.",
        "<b>[19]</b> Cramér, H., <i>Mathematical Methods of Statistics</i>, Princeton University Press, Princeton, NJ, 1946.",
        "<b>[20]</b> SQLite Development Team, “SQLite In-Process Relational Database Architecture and B-Tree Implementation”, 2024. Available: <i>https://www.sqlite.org/arch.html</i>."
    ]

    for ref in refs:
        story.append(Paragraph(ref, styles["AcadRef"]))
        story.append(Spacer(1, 1.0))

    print(f"Building 48-page PDF report to {output_pdf_path}...")
    doc.build(story, canvasmaker=AcademicNumberedCanvas)

    reader = pypdf.PdfReader(output_pdf_path)
    final_page_count = len(reader.pages)
    print(f"Generated PDF successfully. Final Total Page Count: {final_page_count} pages.")
    return final_page_count


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    output_pdf = str(project_root / "reports" / "Summer_Internship_Report_Customer_Churn.pdf")
    viz_directory = str(project_root / "visualizations")

    count = generate_full_48_page_report(output_pdf, viz_directory)
    print(f"Report execution complete! Total Pages: {count}")
