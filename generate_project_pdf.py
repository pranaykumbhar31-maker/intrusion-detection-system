"""
=============================================================================
PDF Generator Script for Intrusion Detection System Practical & Project Guide
Uses ReportLab to create an academic, publication-quality PDF document.
=============================================================================
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(BASE_DIR, "Intrusion_Detection_System_Practical_Guide.pdf")

# Custom Canvas for Page Numbers and Running Header
class NumberedCanvas(canvas.Canvas):
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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Intrusion Detection System using Machine Learning — Practical & Project Guide")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, letter[0] - 54, 742)

        # Running Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, footer_text)
        self.drawString(54, 36, "Academic Demonstration Project • NSL-KDD Benchmark • Random Forest")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, letter[0] - 54, 48)

        self.restoreState()


def create_ids_guide_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    primary_color = colors.HexColor("#0f172a")     # Deep slate navy
    accent_blue = colors.HexColor("#0284c7")       # Professional cyber blue
    accent_green = colors.HexColor("#059669")      # Emerald green
    accent_red = colors.HexColor("#dc2626")        # Crimson red
    text_dark = colors.HexColor("#1e293b")         # Charcoal body text
    bg_light = colors.HexColor("#f8fafc")          # Off-white table / card background
    border_color = colors.HexColor("#e2e8f0")

    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=6
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceAfter=14
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=accent_blue,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        spaceAfter=5
    )

    style_body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=style_body,
        fontName='Helvetica-Bold'
    )

    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        spaceAfter=4,
        leftIndent=8,
        rightIndent=8
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1 # Center
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_dark
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=style_table_cell,
        alignment=1 # Center
    )

    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=style_table_cell,
        fontName='Helvetica-Bold'
    )

    style_viva_q = ParagraphStyle(
        'VivaQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    style_viva_a = ParagraphStyle(
        'VivaA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        spaceAfter=5,
        leftIndent=10
    )

    story = []

    # =========================================================================
    # HEADER BANNER
    # =========================================================================
    story.append(Paragraph("Machine Learning Intrusion Detection System (IDS)", style_title))
    story.append(Paragraph("Practical Demonstration Flow & Comprehensive Project Documentation", style_subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceBefore=0, spaceAfter=10))

    # Meta Info Table
    meta_data = [
        [
            Paragraph("<b>Topic:</b> Intrusion Detection using ML", style_table_cell),
            Paragraph("<b>Algorithm:</b> Random Forest Classifier", style_table_cell),
            Paragraph("<b>Dataset:</b> NSL-KDD Benchmark", style_table_cell)
        ],
        [
            Paragraph("<b>Classification:</b> Binary (Normal vs Attack)", style_table_cell),
            Paragraph("<b>Accuracy:</b> 99.77% on Test Data", style_table_cell),
            Paragraph("<b>Stack:</b> Python, Flask, Scikit-learn", style_table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 160, 174])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 1: SAMPLE DEMONSTRATION FLOW (FOR PRACTICAL EXAM)
    # =========================================================================
    story.append(Paragraph("1. Sample Demonstration Flow (For Your Practical / Viva)", style_h1))
    story.append(Paragraph(
        "Follow this exact step-by-step procedure during your practical evaluation to demonstrate the working system effortlessly to the examiner:",
        style_body
    ))

    demo_steps = [
        ("Step 1: Start System & Open Dashboard",
         "Run <code>python app.py</code> in terminal and navigate to <b>http://127.0.0.1:5000</b>. Show the Home Dashboard displaying model cards: Random Forest, NSL-KDD, Binary Classification, and the dynamically loaded <b>99.77% accuracy</b>. Point out the live traffic donut chart and top feature importance graph."),
        ("Step 2: Navigate to 'Detect Intrusion'",
         "Click <b>Detect Intrusion</b> on the top navigation bar. Point out the two demonstration modes: <b>Mode B (1-Click Traffic Presets)</b> for instant evaluation and <b>Mode A (Manual Feature Input)</b> with 13 network traffic features."),
        ("Step 3: Test Legitimate Network Traffic (NORMAL)",
         "Click the green button: <b>[Normal Traffic Example]</b>. The form instantly populates legitimate HTTP connection features (<code>protocol: tcp, service: http, flag: SF, src_bytes: 232, dst_bytes: 8153, count: 5</code>). Click <b>PREDICT ACTIVITY</b>.<br/>"
         "<b>Result Displayed:</b> Large Green Banner: <b>NORMAL ACTIVITY</b> | Confidence: <b>92.34%</b> | Risk: <b>LOW</b>. Explain the disclaimer confirming this is a machine learning statistical prediction."),
        ("Step 4: Test Malicious Attack Traffic (INTRUSION - DoS)",
         "Click the red button: <b>[Attack Traffic Example]</b>. The form auto-populates a classic Neptune SYN flood attack (<code>protocol: tcp, service: private, flag: S0 (unanswered SYN), count: 123 (high connection burst), src_bytes: 0</code>). Click <b>PREDICT ACTIVITY</b>.<br/>"
         "<b>Result Displayed:</b> Large Crimson Banner: <b>INTRUSION DETECTED</b> | Confidence: <b>100.0%</b> | Risk: <b>HIGH</b>. The explanation notes abnormal SYN flags and high connection bursts."),
        ("Step 5: Test Reconnaissance Attack (Port Sweep Probe)",
         "Click the yellow button: <b>[Port Scan Attack]</b>. Populates port scan recon traffic (<code>flag: REJ, diff_srv_rate: 1.0</code>). Click <b>PREDICT ACTIVITY</b> &rarr; Accurately flagged as <b>INTRUSION</b> (HIGH Risk)."),
        ("Step 6: Show Actual Model Performance & Confusion Matrix",
         "Navigate to <b>Model Performance</b>. Show the examiner the genuine 2x2 Confusion Matrix and Classification Report generated from the 10,000 held-out test records.")
    ]

    for title, desc in demo_steps:
        story.append(Paragraph(f"<b>&bull; {title}</b>", style_h2))
        story.append(Paragraph(desc, style_body))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: PROJECT OVERVIEW & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. Project Overview & System Architecture", style_h1))
    story.append(Paragraph(
        "<b>Problem Statement:</b> Traditional signature-based IDS fail against mutated and zero-day attacks. This project implements a machine learning anomaly detection system that identifies malicious network flows using statistical traffic features.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Machine Learning Pipeline:</b>",
        style_body
    ))

    pipeline_text = (
        "<b>Dataset (NSL-KDD)</b> &rarr; <b>Data Cleaning & Labeling</b> (normal = NORMAL, attacks = INTRUSION) &rarr; "
        "<b>Feature Selection</b> (13 connection & traffic features) &rarr; "
        "<b>Preprocessing</b> (OneHotEncoder + StandardScaler) &rarr; "
        "<b>80/20 Train/Test Split</b> &rarr; <b>Random Forest Classifier</b> (100 Trees) &rarr; "
        "<b>Evaluation</b> &rarr; <b>Model Serialization</b> (joblib) &rarr; "
        "<b>Flask REST API</b> &rarr; <b>Modern Web Interface</b>."
    )
    story.append(Paragraph(pipeline_text, style_code))
    story.append(Spacer(1, 4))

    # Selected Features Table
    story.append(Paragraph("<b>13 High-Impact Features Selected from NSL-KDD:</b>", style_body))
    feat_data = [
        [Paragraph("Category", style_table_header), Paragraph("Feature Name", style_table_header), Paragraph("Description & Cybersecurity Significance", style_table_header)],
        [Paragraph("Protocol & Flags", style_table_cell_bold), Paragraph("protocol_type, service, flag", style_table_cell), Paragraph("Protocol (TCP/UDP/ICMP), network service port, and TCP status flag (SF = normal handshake, S0 = SYN flood, REJ = rejected connection).", style_table_cell)],
        [Paragraph("Payload & Session", style_table_cell_bold), Paragraph("duration, src_bytes, dst_bytes, logged_in", style_table_cell), Paragraph("Duration in seconds, bytes transmitted each way, and authentication flag (1 = successfully logged in, 0 = guest/unauthenticated).", style_table_cell)],
        [Paragraph("Traffic Frequencies", style_table_cell_bold), Paragraph("count, srv_count", style_table_cell), Paragraph("Connections to same host or service in past 2-second window. Massive bursts indicate DoS attacks.", style_table_cell)],
        [Paragraph("Traffic Ratios", style_table_cell_bold), Paragraph("same_srv_rate, diff_srv_rate", style_table_cell), Paragraph("% connections to same vs different services. High diff_srv_rate strongly indicates port scanning / probing.", style_table_cell)],
        [Paragraph("Host-Based Stats", style_table_cell_bold), Paragraph("dst_host_srv_count, dst_host_same_srv_rate", style_table_cell), Paragraph("Destination host service connection density and uniformity over multiple sessions.", style_table_cell)]
    ]
    feat_table = Table(feat_data, colWidths=[100, 140, 264])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent_blue),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(feat_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: MODEL EVALUATION & REAL METRICS
    # =========================================================================
    story.append(Paragraph("3. Model Evaluation Results & Confusion Matrix", style_h1))
    story.append(Paragraph(
        "The Random Forest model was evaluated on <b>10,000 held-out test samples</b> from the NSL-KDD benchmark. All metrics below are genuine and dynamically recorded in <code>results/model_metrics.json</code>:",
        style_body
    ))

    # Metric Table
    metric_data = [
        [Paragraph("Metric", style_table_header), Paragraph("Score", style_table_header), Paragraph("Mathematical Formula", style_table_header), Paragraph("Cybersecurity Practical Meaning", style_table_header)],
        [Paragraph("Accuracy", style_table_cell_bold), Paragraph("<b>99.77%</b>", style_table_cell_center), Paragraph("(TP + TN) / Total", style_table_cell), Paragraph("Overall correct classifications across all test traffic.", style_table_cell)],
        [Paragraph("Precision", style_table_cell_bold), Paragraph("<b>99.77%</b>", style_table_cell_center), Paragraph("TP / (TP + FP)", style_table_cell), Paragraph("Minimizes false alarms (legitimate traffic mistakenly blocked).", style_table_cell)],
        [Paragraph("Recall", style_table_cell_bold), Paragraph("<b>99.77%</b>", style_table_cell_center), Paragraph("TP / (TP + FN)", style_table_cell), Paragraph("Critical: Minimizes missed attacks (intrusions slipping through).", style_table_cell)],
        [Paragraph("F1-Score", style_table_cell_bold), Paragraph("<b>99.77%</b>", style_table_cell_center), Paragraph("2 &times; (P &times; R) / (P + R)", style_table_cell), Paragraph("Harmonic balance between precision and recall.", style_table_cell)]
    ]
    m_table = Table(metric_data, colWidths=[70, 60, 114, 260])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 8))

    # Confusion Matrix Table
    story.append(Paragraph("<b>Actual Evaluated Confusion Matrix (10,000 Test Records):</b>", style_body))
    cm_data = [
        [Paragraph("", style_table_header), Paragraph("Predicted NORMAL", style_table_header), Paragraph("Predicted INTRUSION", style_table_header), Paragraph("Class Analysis", style_table_header)],
        [
            Paragraph("<b>Actual NORMAL</b>", style_table_cell_bold),
            Paragraph("<font color='#059669'><b>5,308 (TN)</b></font><br/>True Negatives", style_table_cell_center),
            Paragraph("<font color='#d97706'><b>3 (FP)</b></font><br/>False Alarms (Type I)", style_table_cell_center),
            Paragraph("Normal traffic correctly identified with 99.94% recall.", style_table_cell)
        ],
        [
            Paragraph("<b>Actual INTRUSION</b>", style_table_cell_bold),
            Paragraph("<font color='#dc2626'><b>20 (FN)</b></font><br/>Missed Attacks (Type II)", style_table_cell_center),
            Paragraph("<font color='#059669'><b>4,669 (TP)</b></font><br/>Accurate Detection", style_table_cell_center),
            Paragraph("4,669 attacks intercepted out of 4,689 total (99.57% detection rate).", style_table_cell)
        ]
    ]
    cm_table = Table(cm_data, colWidths=[110, 115, 115, 164])
    cm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent_blue),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(cm_table)
    story.append(Spacer(1, 8))

    # Feature Importance Summary
    story.append(Paragraph("<b>Top Features Influencing Random Forest Splits (Gini Importance):</b>", style_body))
    top_f_data = [
        [Paragraph("Rank", style_table_header), Paragraph("Feature Name", style_table_header), Paragraph("Weight", style_table_header), Paragraph("Why it's important in Cyber Detection", style_table_header)],
        [Paragraph("#1", style_table_cell_center), Paragraph("src_bytes", style_table_cell_bold), Paragraph("13.61%", style_table_cell_center), Paragraph("Payload size sent. Floods often send 0 bytes or anomalous fixed packet sizes.", style_table_cell)],
        [Paragraph("#2", style_table_cell_center), Paragraph("dst_bytes", style_table_cell_bold), Paragraph("12.89%", style_table_cell_center), Paragraph("Payload received. Benign sessions receive large data; DoS/probes receive almost none.", style_table_cell)],
        [Paragraph("#3", style_table_cell_center), Paragraph("flag_SF", style_table_cell_bold), Paragraph("8.87%", style_table_cell_center), Paragraph("Normal SYN-ACK handshake completion flag; absence indicates probe or flood.", style_table_cell)],
        [Paragraph("#4", style_table_cell_center), Paragraph("same_srv_rate", style_table_cell_bold), Paragraph("7.65%", style_table_cell_center), Paragraph("Density of connections targeted at a single service.", style_table_cell)],
        [Paragraph("#5", style_table_cell_center), Paragraph("diff_srv_rate", style_table_cell_bold), Paragraph("7.31%", style_table_cell_center), Paragraph("Scans and probes target multiple diverse ports/services consecutively.", style_table_cell)],
        [Paragraph("#6", style_table_cell_center), Paragraph("count", style_table_cell_bold), Paragraph("6.12%", style_table_cell_center), Paragraph("Rapid connection burst within 2 seconds; primary indicator of DoS attacks.", style_table_cell)]
    ]
    top_f_table = Table(top_f_data, colWidths=[40, 110, 60, 294])
    top_f_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(top_f_table)

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 4: HOW TO EXPLAIN IN VIVA (PRACTICAL Q&A)
    # =========================================================================
    story.append(Paragraph("4. How to Explain This Project in Viva (Practical Q&A)", style_h1))
    story.append(Paragraph(
        "Examiners frequently ask these foundational questions. Memorize these concise, high-scoring answers:",
        style_body
    ))

    viva_qa = [
        ("Q1: What is an Intrusion Detection System (IDS)?",
         "An IDS is a cybersecurity defense tool that continuously monitors network traffic or system logs for malicious activity, policy violations, or unauthorized access attempts. When detected, it raises an alert for administrators."),
        ("Q2: Why use Machine Learning instead of traditional signature-based rules (like Snort)?",
         "Traditional signature-based IDS only detects known attacks whose exact hashes or rules are stored in a database. If an attacker slightly modifies the payload (polymorphism or zero-day), signatures fail. Machine Learning learns generalized statistical patterns of legitimate vs. anomalous traffic, enabling it to detect new, unseen variants."),
        ("Q3: Why did you choose Random Forest Classifier?",
         "Random Forest is an ensemble of 100 decision trees using bagging (bootstrap aggregation). It was chosen because: (1) It handles mixed categorical and continuous tabular network data exceptionally well, (2) Averaging multiple trees prevents overfitting, (3) It achieves 99%+ accuracy without heavy hyperparameter tuning, and (4) It provides interpretable feature importances."),
        ("Q4: What is the NSL-KDD dataset?",
         "NSL-KDD was developed by the Canadian Institute for Cybersecurity (UNB) to solve critical flaws in the older KDD Cup 99 dataset. It eliminates millions of duplicate records that previously biased classifiers toward frequent packets, providing an unbiased benchmark for academic IDS."),
        ("Q5: What is the difference between Training and Testing data?",
         "Training data (80% in our project) is used by the algorithm to build decision rules and learn internal node split thresholds. Testing data (20%) is strictly held-out data never seen during training, used exclusively to evaluate generalization performance."),
        ("Q6: What is a Confusion Matrix and what is the most dangerous error in IDS?",
         "A Confusion Matrix is a 2x2 grid comparing actual labels against predictions (TN, FP, FN, TP). In cybersecurity, <b>False Negatives (FN)</b> are the most dangerous error because a missed attack penetrates the network, whereas False Positives (FP) merely cause an administrator to investigate a false alarm."),
        ("Q7: How does the Flask backend communicate with the Machine Learning model?",
         "The trained Random Forest model and preprocessor are saved as binary files (<code>.pkl</code>) using Joblib. When the web interface submits JSON features via HTTP POST, Flask routes it to <code>predict.py</code>, runs the preprocessor (One-Hot + Scaler), calls <code>model.predict()</code> and <code>model.predict_proba()</code>, and returns the result (label, probability, risk level, explanation) as JSON back to the browser."),
        ("Q8: What is Overfitting and how did you prevent it?",
         "Overfitting occurs when a model memorizes the training data and noise, failing on new data. We prevented overfitting by using an ensemble of 100 trees, constraining maximum tree depth (<code>max_depth=15</code>), and applying stratified train/test splitting.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(q, style_viva_q))
        story.append(Paragraph(a, style_viva_a))

    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 5: COMMANDS TO RUN
    # =========================================================================
    story.append(Paragraph("5. Setup & Execution Commands", style_h1))
    commands_text = (
        "<b>1. Navigate:</b> cd intrusion-detection-system<br/>"
        "<b>2. Install Dependencies:</b> pip install -r requirements.txt<br/>"
        "<b>3. Train Model:</b> python train_model.py<br/>"
        "<b>4. Start Web Application:</b> python app.py<br/>"
        "<b>5. Open Browser:</b> http://127.0.0.1:5000<br/>"
        "<b>6. Run Automated Tests:</b> python test_app.py"
    )
    story.append(Paragraph(commands_text, style_code))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated PDF: {filename} ({os.path.getsize(filename)} bytes)")

if __name__ == '__main__':
    create_ids_guide_pdf(OUTPUT_PDF)
