# 🛡️ Machine Learning Intrusion Detection System (IDS)

A student-friendly, practical-ready Web Application demonstrating how Supervised Machine Learning (**Random Forest Classifier**) detects whether incoming network connection activity is **NORMAL** or an **INTRUSION / ATTACK** using the benchmark **NSL-KDD** dataset.

---

## 📋 Table of Contents
1. [Problem Statement](#-problem-statement)
2. [Project Objective](#-project-objective)
3. [Technologies Used](#-technologies-used)
4. [Dataset Description](#-dataset-description)
5. [Machine Learning Algorithm](#-machine-learning-algorithm)
6. [System Architecture](#-system-architecture)
7. [Installation & Setup](#-installation--setup)
8. [How to Train the Model](#-how-to-train-the-model)
9. [How to Start the Flask Application](#-how-to-start-the-flask-application)
10. [How to Use the Website](#-how-to-use-the-website)
11. [Expected Output & Sample Demonstration](#-expected-output--sample-demonstration)
12. [Model Evaluation & Real Metrics](#-model-evaluation--real-metrics)
13. [Limitations](#-limitations)
14. [Future Improvements](#-future-improvements)
15. [🎓 How to Explain This Project in Viva (Practical Q&A)](#-how-to-explain-this-project-in-viva-practical-qa)

---

## 📌 Problem Statement
Traditional cybersecurity perimeter defenses rely heavily on **signature-based Intrusion Detection Systems (IDS)** (such as static firewall rules and known attack hash matching). While effective against older, cataloged threats, signature-based tools struggle against zero-day vulnerabilities, polymorphic attack variants, and sudden traffic anomalies. There is an urgent academic and industrial need for **Machine Learning based anomaly detection** capable of learning general statistical traits of legitimate network traffic vs. malicious behavior.

---

## 🎯 Project Objective
1. Build an end-to-end Machine Learning pipeline trained on the benchmark **NSL-KDD** dataset.
2. Formulate the problem as a **Binary Classification** task (`NORMAL` vs. `INTRUSION`).
3. Develop a lightweight, responsive **Flask web application** with a modern cybersecurity dark theme.
4. Provide both **1-Click Realistic Traffic Presets** and **Manual Feature Input** for effortless demonstration in college practicals and vivas.
5. Display live prediction results, classification probability/confidence score, threat risk level, and academic disclaimers.
6. Provide transparent, live model metrics (Accuracy, Precision, Recall, F1-Score, and Visual Confusion Matrix) computed directly from the trained model.

---

## 💻 Technologies Used
- **Backend & Web Server:** Python 3, Flask
- **Machine Learning & Data Processing:** Scikit-Learn, Pandas, NumPy, Joblib
- **Frontend & UI:** HTML5, CSS3, JavaScript (Fetch API), Bootstrap 5, Bootstrap Icons
- **Data Visualization:** Chart.js

---

## 📊 Dataset Description
This project utilizes the **NSL-KDD** benchmark dataset, provided by the Canadian Institute for Cybersecurity (University of New Brunswick). NSL-KDD is the standard academic dataset created to rectify statistical deficiencies and redundant records found in the legacy KDD Cup 99 dataset.

- **Raw NSL-KDD Records:** 41 traffic features + connection label + difficulty score.
- **Student-Friendly Selected Feature Subset (13 Key Features):**
  1. `protocol_type`: Protocol suite (`tcp`, `udp`, `icmp`).
  2. `service`: Destination service (`http`, `private`, `smtp`, `ftp_data`, `telnet`, etc.).
  3. `flag`: TCP handshake status (`SF` = Normal, `S0` = SYN flood no reply, `REJ` = Rejected, etc.).
  4. `duration`: Length of connection in seconds.
  5. `src_bytes`: Bytes sent from client/source to destination.
  6. `dst_bytes`: Bytes sent from server/destination back to client.
  7. `logged_in`: 1 if authenticated login succeeded, 0 otherwise.
  8. `count`: Connections to the same destination host in past 2 seconds.
  9. `srv_count`: Connections to the same port/service in past 2 seconds.
  10. `same_srv_rate`: % of connections to the same service.
  11. `diff_srv_rate`: % of connections to different services (port scan indicator).
  12. `dst_host_srv_count`: Connections to the same service on the destination host.
  13. `dst_host_same_srv_rate`: % of connections to the same service on the destination host.
- **Target Mapping:**
  - `normal` &rarr; `NORMAL` (Class 0, Low Risk)
  - All attack categories (`neptune`, `smurf`, `portsweep`, `satan`, etc.) &rarr; `INTRUSION` (Class 1, High Risk)

---

## 🌲 Machine Learning Algorithm
The system uses the **Random Forest Classifier** (`sklearn.ensemble.RandomForestClassifier`):
- **Ensemble Technique:** Bootstrap Aggregating (Bagging).
- **Estimators:** 100 decision trees (`n_estimators=100`).
- **Maximum Depth:** `max_depth=15` (to guard against overfitting while capturing non-linear interactions).
- **Random State:** `random_state=42` (ensures 100% reproducible training results).
- **Preprocessing:**
  - `OneHotEncoder(handle_unknown='ignore')` for categorical attributes (`protocol_type`, `service`, `flag`).
  - `StandardScaler()` for continuous numerical metrics.
  - Bundled using Scikit-Learn `ColumnTransformer`.

---

## 🏗️ System Architecture

```
[ NSL-KDD Dataset: data/KDDTrain+.txt ]
                    │
                    ▼
           [ train_model.py ]
   ├── Data Cleaning & Binary Labeling
   ├── OneHotEncoder + StandardScaler
   ├── 80/20 Stratified Train/Test Split
   ├── Random Forest Classifier (100 Trees)
   └── Model Evaluation (Accuracy, Precision, Recall, F1, CM)
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
[ model/intrusion_model.pkl ] [ results/model_metrics.json ]
[ model/preprocessor.pkl   ]
          │                   │
          └─────────┬─────────┘
                    ▼
             [ Flask Backend: app.py ]
             ├── predict.py (Inference Engine)
             ├── /api/predict (REST Endpoint)
             └── /api/model-performance
                    │
                    ▼
         [ Web Frontend: Bootstrap 5 + JS ]
         ├── Dashboard (/): Stats & Chart.js
         ├── Detect (/detect): Presets & Form
         ├── Performance (/performance): Confusion Matrix
         └── About (/about): Academic Viva Notes
```

---

## 🚀 Installation & Setup

### Step 1: Open Terminal / PowerShell
Navigate to the project directory:
```bash
cd intrusion-detection-system
```

### Step 2: Create and Activate Virtual Environment (Optional but Recommended)
**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ How to Train the Model
To execute the complete data cleaning, feature engineering, training, and evaluation pipeline:
```bash
python train_model.py
```

**What happens automatically:**
1. Verifies if `data/KDDTrain+.txt` exists; if missing, automatically downloads it from the official GitHub mirror.
2. Preprocesses categorical and numeric features.
3. Fits the Random Forest Classifier on 40,000 training records.
4. Evaluates performance on 10,000 held-out test records.
5. Saves serialized artifacts to `model/intrusion_model.pkl` and `model/preprocessor.pkl`.
6. Saves evaluation metrics to `results/model_metrics.json`.

---

## 🌐 How to Start the Flask Application
Once the model is trained, start the local web server:
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🖥️ How to Use the Website

1. **Dashboard (`/`):**
   - View primary model metadata (Random Forest, Binary Mode, NSL-KDD, ~99.8% Accuracy).
   - Inspect live prediction counters (Total, Normal, Intrusion) updated in real-time.
   - Analyze Session Distribution Donut Chart and Top Feature Importance Bar Chart.
2. **Detect Intrusion (`/detect`):**
   - **Mode B (Recommended for Viva):** Click **[Normal Traffic Example]** or **[Attack Traffic Example]** to auto-populate realistic network packet features.
   - **Mode A (Manual Tuning):** Adjust protocol, service, flags, bytes, or connection counts manually.
   - Click **[PREDICT ACTIVITY]** to run immediate machine learning inference.
3. **Model Performance (`/performance`):**
   - Review genuine Scikit-Learn evaluation statistics: Accuracy, Precision, Recall, and F1-Score.
   - Inspect the interactive **Visual Confusion Matrix** (TN, FP, FN, TP) and per-class Classification Report.
4. **About System (`/about`):**
   - Read system concepts, architectural flow, and comprehensive answers to 14 viva questions.

---

## 🧪 Expected Output & Sample Demonstration

During your practical examination, demonstrate the following step-by-step flow:

### Test Case 1: Normal Web Traffic
1. Go to the **Detect Intrusion** page.
2. Click the green button: **[Normal Traffic Example]**.
   - Populates: `protocol: tcp`, `service: http`, `flag: SF`, `src_bytes: 232`, `dst_bytes: 8153`, `count: 5`, `same_srv_rate: 1.0`.
3. Click **[PREDICT ACTIVITY]**.
4. **Result Displayed:**
   - **Status:** `NORMAL ACTIVITY` (Green Badge)
   - **Confidence:** `~92.3%`
   - **Risk Level:** `LOW`
   - **Explanation:** *"Based on the supplied network traffic features, the trained Random Forest model classified this activity as NORMAL with 92.34% confidence..."*

### Test Case 2: DoS SYN Flood Attack (Neptune)
1. On the same page, click the red button: **[Attack Traffic Example]**.
   - Populates: `protocol: tcp`, `service: private`, `flag: S0` (SYN sent, no ack), `src_bytes: 0`, `dst_bytes: 0`, `count: 123` (abnormal burst), `same_srv_rate: 0.05`.
2. Click **[PREDICT ACTIVITY]**.
3. **Result Displayed:**
   - **Status:** `INTRUSION DETECTED` (Crimson Red Badge)
   - **Confidence:** `100.0%`
   - **Risk Level:** `HIGH`
   - **Explanation:** *"Based on the supplied network traffic features, the trained Random Forest model classified this activity as an INTRUSION with 100.0% confidence..."*

---

## 📈 Model Evaluation & Real Metrics

The metrics below were generated directly from the trained Random Forest on 10,000 held-out test samples:

| Metric | Score | Formula / Meaning |
| :--- | :--- | :--- |
| **Accuracy** | **99.77%** | \(\frac{TP + TN}{TP + TN + FP + FN}\) |
| **Precision** | **99.77%** | \(\frac{TP}{TP + FP}\) (Measures false alarm rate) |
| **Recall (Sensitivity)** | **99.77%** | \(\frac{TP}{TP + FN}\) (Measures missed attack rate) |
| **F1-Score** | **99.77%** | Harmonic mean of Precision and Recall |

### Actual Confusion Matrix (10,000 Test Records)
- **True Negatives (TN):** `5,308` (Normal traffic accurately identified as Normal)
- **False Positives (FP):** `3` (Normal falsely flagged as attack - Type I Error)
- **False Negatives (FN):** `20` (Attacks missed - Type II Error)
- **True Positives (TP):** `4,669` (Intrusions accurately detected)

---

## ⚠️ Limitations
1. **Academic Scope:** Designed as an educational demonstration, not a production firewall or inline packet-dropper.
2. **Tabular Feature Dependency:** Expects pre-extracted statistical connection features rather than raw hex PCAP packet streams.
3. **Zero-Day Generalization:** While Random Forest generalizes well across statistical variations, novel zero-day exploits differing completely from NSL-KDD attack distributions may evade detection.

---

## 🔮 Future Improvements
1. **Multi-Class Classification:** Expand prediction beyond binary to categorize specific attack families (DoS, Probe, R2L, U2R).
2. **Live PCAP Sniffing:** Integrate Python `scapy` to capture real Ethernet/Wi-Fi packets from network cards and extract features dynamically.
3. **Deep Learning Comparison:** Compare Random Forest against 1D-CNNs and LSTM networks on sequential network flow data.

---

## 🎓 How to Explain This Project in Viva (Practical Q&A)

Here are student-friendly answers to the most common questions examiners ask during a viva:

### 1. What is an Intrusion Detection System (IDS)?
> *"An Intrusion Detection System is a security tool that continuously monitors network traffic for suspicious activities, unauthorized access attempts, or policy violations. Upon detecting an anomaly or attack, it raises an alert for administrators."*

### 2. What is an intrusion in cybersecurity?
> *"An intrusion is any unauthorized, malicious action that attempts to compromise the Confidentiality, Integrity, or Availability (the CIA Triad) of a system or network—such as a Denial of Service attack or an unauthorized login."*

### 3. Why did you use Machine Learning instead of traditional rules?
> *"Traditional IDS tools rely on rigid signatures or hardcoded rules. If an attacker slightly modifies their payload, signature-based IDS fails. Machine Learning learns underlying statistical relationships across multiple network attributes, allowing it to detect new or slightly mutated attacks without human-written rules."*

### 4. Why did you choose the Random Forest algorithm?
> *"Random Forest is an ensemble of multiple decision trees that uses bagging (bootstrap aggregation). It is ideal for tabular network data because:
> 1. It handles both categorical and numerical features effortlessly.
> 2. It avoids overfitting by averaging predictions across 100 decorrelated trees.
> 3. It gives high accuracy (>99%) with fast inference and provides feature importance scores."*

### 5. What is the NSL-KDD dataset?
> *"NSL-KDD is the benchmark academic dataset released by the Canadian Institute for Cybersecurity to improve the legacy KDD Cup 99 dataset. It removes redundant records and provides a balanced distribution so that machine learning models are not biased toward frequent samples."*

### 6. What are features in Machine Learning?
> *"Features are individual measurable variables extracted from each connection record. In our project, features include the protocol used (TCP/UDP), connection flags (SF, S0), duration, source/destination bytes transferred, and connection frequency counts in a 2-second window."*

### 7. What is Binary Classification?
> *"Binary classification is a supervised learning task where every sample is categorized into one of two mutually exclusive classes. Here, the two classes are NORMAL (legitimate network traffic) and INTRUSION (malicious attack traffic)."*

### 8. What is the difference between Training and Testing data?
> *"Training data (80% in our project) is used by the algorithm to learn patterns and construct decision trees. Testing data (20%) is strictly held-out data never seen during training, used to evaluate how well the model generalizes to new traffic."*

### 9. What is Overfitting and how did you prevent it?
> *"Overfitting happens when a model memorizes noise and specific peculiarities of the training data, causing poor performance on real-world test data. We prevented overfitting by using Random Forest (which averages 100 trees), limiting tree depth (`max_depth=15`), and applying stratified train/test splitting."*

### 10. What is Accuracy?
> *"Accuracy is the ratio of correct predictions to total predictions: \((TP + TN) / Total\). Our model achieves 99.77% accuracy on 10,000 unseen test packets."*

### 11. What are Precision, Recall, and F1-Score? Why are they needed?
> *- **Precision:** Out of all packets flagged as attacks, how many were truly attacks? High precision means minimal false alarms.*
> *- **Recall:** Out of all actual attacks that took place, how many did our system catch? High recall means few missed attacks.*
> *- **F1-Score:** The harmonic mean of precision and recall. It ensures balanced performance, especially when attack and normal samples have different class frequencies.*

### 12. What is a Confusion Matrix?
> *"A Confusion Matrix is a 2x2 table comparing actual labels against predicted labels:
> - **True Negative (TN):** Normal traffic correctly classified as Normal.
> - **False Positive (FP):** Normal traffic falsely flagged as Attack (False Alarm).
> - **False Negative (FN):** Attack traffic missed and classified as Normal (Dangerous error).
> - **True Positive (TP):** Attack traffic correctly caught by the model."*

### 13. How does the Flask backend communicate with the Machine Learning model?
> *"The trained Random Forest and preprocessing pipeline are saved as binary `.pkl` files using `joblib`. When a user submits features on the website, Flask receives the JSON payload, loads the preprocessor to encode and scale the features, passes the array to `model.predict()` and `model.predict_proba()`, and sends the output (prediction, confidence %, risk level) back to the browser as JSON."*

### 14. What are the roles of One-Hot Encoding and Feature Scaling?
> *- **One-Hot Encoding:** Converts non-numeric categories like protocol (`tcp`, `udp`, `icmp`) into binary indicator columns (0 or 1) so mathematical algorithms can compute with them.*
> *- **Feature Scaling (StandardScaler):** Normalizes continuous values (like source bytes from 0 to 100,000 vs rate percentages from 0 to 1) to mean 0 and unit variance, preventing large values from dominating the tree splits.*

---

## 👨‍💻 Project Directory Structure
```
intrusion-detection-system/
├── app.py                     # Flask application routes and API endpoints
├── train_model.py             # Complete ML training & evaluation script
├── predict.py                 # Core inference engine with input validation
├── test_app.py                # Automated test suite (10 unit/integration tests)
├── generate_project_pdf.py    # ReportLab script generating the PDF guide
├── Intrusion_Detection_System_Practical_Guide.pdf # Academic PDF Guide for Practicals
├── requirements.txt           # Python library dependencies
├── README.md                  # Complete documentation and viva guide
│
├── data/
│   ├── KDDTrain+.txt          # NSL-KDD training dataset
│   └── KDDTest+.txt           # NSL-KDD testing dataset
│
├── model/
│   ├── intrusion_model.pkl    # Serialized Random Forest model
│   └── preprocessor.pkl       # Serialized ColumnTransformer preprocessor
│
├── results/
│   └── model_metrics.json     # Real evaluated performance metrics
│
├── templates/
│   ├── base.html              # Layout, navbar, footer, CDNs
│   ├── index.html             # Dashboard with charts & live counters
│   ├── detect.html            # Detection form (Mode A manual + Mode B presets)
│   ├── performance.html       # Confusion matrix & classification report
│   └── about.html             # Conceptual guide & 14 viva questions
│
└── static/
    ├── css/
    │   └── style.css          # Modern dark-theme cybersecurity styles
    └── js/
        └── script.js          # Preset loader, AJAX inference, Chart.js
```

---

*Academic Practical Project — Intrusion Detection System using Machine Learning.*
