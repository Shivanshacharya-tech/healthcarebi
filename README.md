# VitalFlow: Hospital ED Operations & Capacity Intelligence

[![SQL Server](https://img.shields.io/badge/Database-MS%20SQL%20Server-red?logo=microsoftsqlserver)](https://www.microsoft.com/en-us/sql-server)
[![AWS S3](https://img.shields.io/badge/Cloud-AWS%20S3-orange?logo=amazon-aws)](https://aws.amazon.com/s3/)
[![Power BI](https://img.shields.io/badge/BI-Power%20BI%20Desktop-yellow?logo=powerbi)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Pipeline-Python%203.13-blue?logo=python)](https://python.org)

An enterprise-grade Healthcare Operations Intelligence platform engineered to diagnose emergency department (ED) crowding, patient flow bottlenecks, Left-Without-Being-Seen (LWBS) rates, and inpatient bed occupancy across a 450-bed tertiary hospital network.

---

## 🏗️ Architecture & Data Pipeline

```
┌─────────────────────────────────┐
│   Data Generation & Simulation  │
│  (Python 3.13 / Stat Models)    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│       Cloud Staging Layer       │
│         AWS S3 Data Lake        │
│  (s3://vitalflow-healthcare/raw)│
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│      Relational Data Warehouse  │
│         MS SQL Server           │
│   • Star Schema (Kimball)       │
│   • Non-Clustered Indexes       │
│   • Analytical Views & Stored   │
│     Procedures                  │
└────────────────┬────────────────┘
                 │ DirectQuery / Import
                 ▼
┌─────────────────────────────────┐
│      Executive Power BI Suite   │
│   • 3-Page Storyboard           │
│   • Custom DAX (90th Pct, LOS)  │
│   • What-If Staffing Simulator  │
└─────────────────────────────────┘
```

---

## 📊 Star Schema Data Model

The data warehouse implements a high-performance **Kimball Star Schema**:

```
                       ┌──────────────────────┐
                       │       Dim_Date       │
                       │  (DateKey, Weekend,  │
                       │      Holidays)       │
                       └──────────┬───────────┘
                                  │ 1
                                  │
                                  │ N
                       ┌──────────┴───────────┐
     ┌─────────────────┤  Fact_ED_Encounters  ├─────────────────┐
     │ 1               │  (23,700+ Visits,    │               1 │
     │                 │   Wait, LOS, LWBS)   │                 │
┌────┴────────────┐    └──────────┬───────────┘    ┌────────────┴───┐
│  Dim_Patients   │               │ 1              │ Dim_Physicians │
│ (Age, Gender,   │               │                │ (Specialty,    │
│  Insurance)     │               │ N              │  Shift)        │
└────┬────────────┘    ┌──────────┴───────────┐    └────────────────┘
     │ 1               │ Fact_Inpatient_Stays │
     │                 │ (7,800+ Admissions,  │
     │                 │  Readmissions, Cost) │
     │                 └──────────┬───────────┘
     │                            │ N
     │                            │ 1
     └────────────────────────────┼─────────────────────────────┐
                                  │                             │
                       ┌──────────┴───────────┐                 │
                       │   Dim_Departments    │─────────────────┘
                       │ (Wards, BedCapacity, │
                       │  Staffing Ratios)    │
                       └──────────────────────┘
```

---

## 📈 Key Clinical & Operational Metrics

| Metric | Benchmark Target | Hospital Actual | Status | Business Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **LWBS Rate (%)** | `< 2.0%` | **3.8%** | 🚨 Critical Breach | Patients in triage leaving before physician consult; severe clinical risk & lost billing. |
| **Median Door-to-Doctor** | `< 30 mins` | **46.5 mins** | ⚠️ Delayed | Stretched staffing between 14:00 and 20:00 causes triage queuing. |
| **Median Boarding Time** | `< 120 mins` | **198 mins (~3.3 hrs)** | 🚨 Bottleneck | Admitted patients stranded in ED corridors waiting for inpatient beds to turn over. |
| **Inpatient Bed Occupancy**| `< 85.0%` | **89.4%** | ⚠️ Overcrowded | Exceeds safe threshold; triggers ambulance diversion and surgical delays. |
| **30-Day Readmission Rate**| `< 12.0%` | **14.2%** | ⚠️ CMS Penalty Risk | Driven predominantly by congestive heart failure and elderly Medicaid/Medicare cohorts. |

---

## 🖥️ 3-Page Power BI Dashboard Layout

### Page 1: Executive Operations Overview
* **KPI Header Cards:** Total ED Arrivals, Median Wait Time, LWBS %, Bed Occupancy %, Average ED Length of Stay.
* **Volume Heatmap:** Matrix visual cross-filtering **Day of Week** vs. **Hour of Day** to pinpoint peak arrival windows (Sunday/Monday 14:00–21:00).
* **Acuity Breakdown (ESI 1–5):** Donut and bar charts showing the proportion of emergent vs. low-acuity walk-ins.

### Page 2: Patient Flow Bottlenecks & Triage Diagnostics
* **Process Funnel:** Stage-by-stage dwell time: `Arrival -> Triage -> Physician Exam -> Disposition -> Bed Placement`.
* **The "LWBS Cliff" Scatterplot:** Correlation between wait time (minutes) and patient departure probability (spiking drastically after 90 minutes for ESI 4 & 5).
* **Physician Efficiency Matrix:** Comparison of patients treated per hour and door-to-eval times by specialty and shift.

### Page 3: Inpatient Capacity & What-If Staffing Simulator
* **Ward Occupancy Gauges:** Live bed utilization gauges for ICU, Cardiology, Med-Surg, and Pediatrics against operational caps.
* **Boarding Hours by Ward:** Breakdown showing Med-Surg and Cardiology as the primary drivers of ED gridlock.
* **Interactive What-If Parameter:** Slider adjusting fast-track triage capacity to simulate:
  * Reduction in LWBS Rate from 3.8% down to 1.9%.
  * Projected annual revenue preservation of **~$420,000**.

---

## 🚀 Quickstart & Setup Guide

### 1. Generate Raw Data
```bash
python scripts/generate_data.py
```

### 2. (Optional) Stage to AWS S3
Ensure AWS CLI is configured with credentials (`aws configure`), then execute:
```bash
python scripts/upload_to_aws_s3.py <your-bucket-name> <region>
```

### 3. Deploy MS SQL Server Database
1. Open **SQL Server Management Studio (SSMS)** or Azure Data Studio.
2. Execute `sql/01_create_database_and_tables.sql` to instantiate the schema and indexes.
3. Execute `sql/02_bulk_load_data.sql` to ingest the CSV files.
4. Execute `sql/03_analytical_views_and_kpis.sql` to compile analytical views and stored procedures.

### 4. Connect Power BI
1. Open Power BI Desktop $\to$ **Get Data** $\to$ **SQL Server Database**.
2. Server: `localhost` (or your SQL Server instance) | Database: `VitalFlow_Healthcare_DW`.
3. Select Import or DirectQuery.
4. Verify relationships match the Star Schema diagram above.
5. Create a new measure table `_Measures` and copy the formulas from `powerbi/dax_measures.md`.
