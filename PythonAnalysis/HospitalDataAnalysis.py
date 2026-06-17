"""
Healthcare Readmission Risk & Cost Analysis

Objective:
Analyze hospital admissions data to identify
clinical, socioeconomic, and hospital-level
factors associated with 30-day readmissions.

Tools:
- Python (Pandas, Matplotlib)
- SQLite
- Power BI

Dataset Size:
120,000 hospital admissions
"""


import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# create/connect database file
conn = sqlite3.connect("hospital_readmission.db")
cursor = conn.cursor()

# Read all CSV files
admissions = pd.read_csv("admissions.csv")
billing = pd.read_csv("billing.csv")
diagnoses = pd.read_csv("diagnoses.csv")
hospitals = pd.read_csv("hospitals.csv")
patients = pd.read_csv("patients.csv")

tables = {
    "Admissions": admissions,
    "Billing": billing,
    "Diagnoses": diagnoses,
    "Hospitals": hospitals,
    "Patients": patients
}

for name, df in tables.items():
    print("\n" + "="*60)
    print(f"{name.upper()} TABLE")
    print("="*60)

    print("\nShape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nDuplicates:", df.duplicated().sum())


patients['insurance_type'] = patients['insurance_type'].fillna("Unknown")

admissions['admit_date'] = pd.to_datetime(admissions['admit_date'])
admissions['discharge_date'] = pd.to_datetime(admissions['discharge_date'])

readmission_df = (
    admissions
    .merge(patients, on='patient_id', how='left')
    .merge(billing, on='admission_id', how='left')
    .merge(hospitals, on='hospital_id', how='left')
)

def readmission_rate(df, group_col):
    return (
        df.groupby(group_col)['readmitted_30d']
        .mean()
        .mul(100)
        .round(2)
        .reset_index(name='readmission_rate')
        .sort_values('readmission_rate', ascending=False)
    )

def plot_bar(df, x, y, title):
    df.plot(x=x, y=y, kind='bar', figsize=(8,5), legend=False)
    plt.title(title)
    plt.ylabel("Readmission Rate (%)")
    plt.xlabel(x)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

readmission_rate_30d = readmission_df['readmitted_30d'].mean() * 100
print(f"Overall 30-Day Readmission Rate: {readmission_rate_30d:.2f}%")

readmission_rate_7d = readmission_df['readmitted_7d'].mean() * 100
print(f"Overall 7-Day Readmission Rate: {readmission_rate_7d:.2f}%")


readmission_df['age_group'] = pd.cut(
    readmission_df['age'],
    bins=[0,18,35,50,65,120],
    labels=['0-18','19-35','36-50','51-65','65+']
)

age_analysis = readmission_rate(readmission_df, 'age_group')
print(age_analysis)

plot_bar(age_analysis, 'age_group', 'readmission_rate', 'Age vs Readmission')

gender_analysis = readmission_rate(readmission_df, 'gender')
print(gender_analysis)
print(readmission_df['gender'].value_counts())

comorbidity_analysis = readmission_rate(readmission_df, 'comorbidity_count')
print(comorbidity_analysis)

print(readmission_df['comorbidity_count'].value_counts())

plot_bar(comorbidity_analysis, 'comorbidity_count', 'readmission_rate', 'Comorbidity vs Readmission')


prev_adm_analysis = readmission_rate(readmission_df, 'prev_admissions')
print(prev_adm_analysis)

print(readmission_df['prev_admissions'].value_counts())

plot_bar(prev_adm_analysis, 'prev_admissions', 'readmission_rate', 'Previous Admissions vs Readmission')


insurance_analysis = readmission_rate(readmission_df, 'insurance_type')
print(insurance_analysis)

print(readmission_df['insurance_type'].value_counts())


print(pd.crosstab(
    readmission_df['insurance_type'],
    readmission_df['bpl_card']
))

print(pd.crosstab(
    readmission_df['insurance_type'],
    readmission_df['bpl_card'],
    normalize='index'
).round(3) * 100)

bpl_analysis = readmission_rate(readmission_df, 'bpl_card')
print(bpl_analysis)

primary_diag = diagnoses[diagnoses['diag_rank'] == 1]

diag_readmission = readmission_df.merge(
    primary_diag[['admission_id', 'diag_category']],
    on='admission_id',
    how='left'
)

diag_analysis = readmission_rate(diag_readmission, 'diag_category')

print(diag_analysis)

plot_bar(diag_analysis, 'diag_category', 'readmission_rate', 'Diagnosis vs Readmission')

readmission_df['los_group'] = pd.cut(
    readmission_df['los_days'],
    bins=[0, 3, 7, 14, 100],
    labels=['1-3 Days', '4-7 Days', '8-14 Days', '15+ Days']
)

los_analysis = readmission_rate(readmission_df, 'los_group')

print(los_analysis)

plot_bar(los_analysis, 'los_group', 'readmission_rate', 'LOS vs Readmission')

readmission_df['charlson_group'] = pd.cut(
    readmission_df['charlson_index'],
    bins=[-1, 1, 3, 5, 100],
    labels=['Low (0-1)','Moderate (2-3)','High (4-5)','Very High (6+)']
)

charlson_analysis = readmission_rate(readmission_df, 'charlson_group')

print(charlson_analysis)

plot_bar(charlson_analysis, 'charlson_group', 'readmission_rate', 'Charlson Index vs Readmission')


state_analysis = readmission_rate(readmission_df, 'state_y')
print(state_analysis)

teaching_analysis = readmission_rate(readmission_df, 'teaching')
print(teaching_analysis)

tier_analysis = readmission_rate(readmission_df, 'tier')
print(tier_analysis)


print(readmission_df.groupby('readmitted_30d')['total_cost_inr'].mean().round(2))

cost_analysis = readmission_rate(readmission_df, 'cost_category')
print(cost_analysis)

cost_compare = readmission_df.groupby('readmitted_30d')['total_cost_inr'].mean()

extra_cost = cost_compare[1] - cost_compare[0]
print(extra_cost)


print(readmission_df['out_of_pocket_inr'].describe())

readmission_df['oop_group'] = pd.cut(
    readmission_df['out_of_pocket_inr'],
    bins=[-1, 0, 10000, 50000, readmission_df['out_of_pocket_inr'].max()],
    labels=['₹0','₹1-10K','₹10K-50K','₹50K+']
)

oop_analysis = readmission_rate(readmission_df, 'oop_group')

print(oop_analysis)

plot_bar(oop_analysis, 'oop_group', 'readmission_rate', 'Out-of-Pocket vs Readmission')

#Load Data to SQLlite

admissions.to_sql("admissions", conn, if_exists="replace", index=False)
patients.to_sql("patients", conn, if_exists="replace", index=False)
billing.to_sql("billing", conn, if_exists="replace", index=False)
hospitals.to_sql("hospitals", conn, if_exists="replace", index=False)
diagnoses.to_sql("diagnoses", conn, if_exists="replace", index=False)

print("All tables created in SQLite!")

##Overall 30-day readmission rate
query = """
SELECT 
    ROUND(AVG(readmitted_30d) * 100, 2) AS readmission_rate_30d
FROM admissions;
"""

result = pd.read_sql(query, conn)
print(result)

#Age analysis 
query = """
SELECT
    CASE
        WHEN p.age BETWEEN 0 AND 18 THEN '0-18'
        WHEN p.age BETWEEN 19 AND 35 THEN '19-35'
        WHEN p.age BETWEEN 36 AND 50 THEN '36-50'
        WHEN p.age BETWEEN 51 AND 65 THEN '51-65'
        ELSE '65+'
    END AS age_group,

    ROUND(AVG(a.readmitted_30d) * 100, 2) AS readmission_rate

FROM admissions a
JOIN patients p
ON a.patient_id = p.patient_id

GROUP BY age_group
ORDER BY readmission_rate DESC;
"""

age_df = pd.read_sql(query, conn)
print(age_df)

#ComorbidityAnalysis 
query = """
SELECT
    p.comorbidity_count,
    ROUND(AVG(a.readmitted_30d) * 100, 2) AS readmission_rate

FROM admissions a
JOIN patients p
ON a.patient_id = p.patient_id

GROUP BY p.comorbidity_count
ORDER BY p.comorbidity_count;
"""

comorb_df = pd.read_sql(query, conn)
print(comorb_df)


#LOSAnalysis 
query = """
SELECT
    CASE
        WHEN los_days BETWEEN 1 AND 3 THEN '1-3 Days'
        WHEN los_days BETWEEN 4 AND 7 THEN '4-7 Days'
        WHEN los_days BETWEEN 8 AND 14 THEN '8-14 Days'
        ELSE '15+ Days'
    END AS los_group,

    ROUND(AVG(readmitted_30d) * 100, 2) AS readmission_rate

FROM admissions
GROUP BY los_group
ORDER BY readmission_rate;
"""

los_df = pd.read_sql(query, conn)
print(los_df)


#FinancialImpact
query = """
SELECT
    a.readmitted_30d,
    ROUND(AVG(b.total_cost_inr), 2) AS avg_cost
FROM admissions a
JOIN billing b
ON a.admission_id = b.admission_id
GROUP BY a.readmitted_30d;
"""

cost_df = pd.read_sql(query, conn)
print(cost_df)

#OutofPocketImpact
query = """
SELECT
    CASE
        WHEN out_of_pocket_inr = 0 THEN '₹0'
        WHEN out_of_pocket_inr BETWEEN 1 AND 10000 THEN '₹1-10K'
        WHEN out_of_pocket_inr BETWEEN 10001 AND 50000 THEN '₹10K-50K'
        ELSE '₹50K+'
    END AS oop_group,

    ROUND(AVG(readmitted_30d) * 100, 2) AS readmission_rate

FROM billing b
JOIN admissions a
ON a.admission_id = b.admission_id
GROUP BY oop_group;
"""

oop_df = pd.read_sql(query, conn)
print(oop_df)


#cciVsReadmission
query = """
SELECT
    CASE
        WHEN charlson_index BETWEEN 0 AND 1 THEN 'Low (0-1)'
        WHEN charlson_index BETWEEN 2 AND 3 THEN 'Moderate (2-3)'
        WHEN charlson_index BETWEEN 4 AND 5 THEN 'High (4-5)'
        ELSE 'Very High (6+)'
    END AS charlson_group,

    ROUND(AVG(readmitted_30d) * 100, 2) AS readmission_rate

FROM admissions
GROUP BY charlson_group
ORDER BY readmission_rate;
"""

cci_df = pd.read_sql(query, conn)
print(cci_df)

#WardType
query = """
SELECT
    ward_type,
    ROUND(AVG(readmitted_30d) * 100, 2) AS readmission_rate
FROM admissions
GROUP BY ward_type
ORDER BY readmission_rate DESC;
"""
Ward_Type = pd.read_sql(query, conn)
print(Ward_Type)

