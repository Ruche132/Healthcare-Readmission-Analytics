# Healthcare Readmission Risk & Cost Analysis

## Project Overview

Hospital readmissions are a major challenge for healthcare systems because they increase treatment costs and may indicate gaps in patient care. In this project, I analyzed 120,000 hospital admission records to identify clinical, socioeconomic, financial, and hospital-related factors associated with 30-day readmissions.

The project combines Python, SQLite, and Power BI to perform data cleaning, exploratory data analysis, SQL-based analysis, and interactive dashboard development.

---

## Objectives

* Calculate overall 30-day and 7-day readmission rates
* Identify patient characteristics associated with higher readmission risk
* Analyze the impact of comorbidities, Charlson Comorbidity Index (CCI), and previous admissions
* Study the relationship between hospitalization factors and readmission outcomes
* Evaluate financial burden and treatment costs associated with readmissions
* Build an interactive Power BI dashboard for stakeholder reporting

---

## Tools Used

* Python

  * Pandas
  * Matplotlib
* SQLite
* Power BI

---

## Dataset

The dataset contains approximately 120,000 hospital admissions and includes:

* Admissions information
* Patient demographics
* Diagnosis records
* Billing information
* Hospital information

Files used:

* admissions.csv
* patients.csv
* diagnoses.csv
* billing.csv
* hospitals.csv

---

## Project Workflow

### 1. Data Preparation

* Loaded data from multiple CSV files
* Checked missing values and duplicate records
* Standardized date columns
* Merged datasets into a master analytical table

### 2. Exploratory Data Analysis (Python)

Analyzed:

* Age vs Readmission
* Comorbidity Count vs Readmission
* Previous Admissions vs Readmission
* Length of Stay vs Readmission
* Charlson Comorbidity Index vs Readmission
* Diagnosis Category vs Readmission
* Ward Type vs Readmission
* Insurance Type and BPL Status
* Out-of-Pocket Expenses vs Readmission
* Cost Impact of Readmissions

### 3. SQL Analysis (SQLite)

Performed SQL-based analysis for:

* Readmission Rate Calculation
* Age Group Analysis
* Comorbidity Analysis
* Length of Stay Analysis
* Charlson Index Analysis
* Ward Type Analysis
* Financial Impact Analysis
* Out-of-Pocket Cost Analysis

### 4. Power BI Dashboard

Created a multi-page interactive dashboard to visualize:

* Executive Summary
* Patient History & Hospitalization Factors
* Socioeconomic & Financial Impact
* Hospital & Diagnosis Insights

---

## Key Findings

* Patients with higher Charlson Comorbidity Index scores showed higher readmission rates.
* Readmitted patients had significantly higher average treatment costs.
* Previous admissions were strongly associated with future readmission risk.
* Longer hospital stays generally showed higher readmission percentages.
* Higher out-of-pocket expenses were associated with increased readmission rates.

---

## Power BI Dashboard

### Executive Overview

![Dashboard Page 1](Dashboard_Page1.png)

### Patient History & Hospitalization Factors

![Dashboard Page 2](Dashboard_Page2.png)

### Socioeconomic & Financial Impact

![Dashboard Page 3](Dashboard_Page3.png)

### Hospital & Diagnosis Insights

![Dashboard Page 4](Dashboard_Page4.png)

---

## Python Visualizations

### Charlson Comorbidity Index vs Readmission

![CCI Analysis](CciVsReadmission.png)

### Age vs Readmission

![Age](AgeVsReadmission.png)

### Length of Stay vs Readmission

![Length of Stay](LOSVsReadmission.png)

### Diagnosis Category vs Readmission

![Diagnosis Category](DiagnosisVsReadmission.png)


###  Comorbidity vs Readmission


![Comorbidity](ComorbidityVsReadmission.png)




---



