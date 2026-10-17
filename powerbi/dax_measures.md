# VitalFlow Healthcare BI - Complete Power BI DAX Reference Guide

This document contains production-ready DAX measures organized by category. Create a dedicated **`_Measures`** table in Power BI to house these calculations.

---

## 1. Core Operational Volume Measures

### Total Arrivals
```dax
Total Arrivals = 
COUNTROWS(Fact_ED_Encounters)
```

### Total Admitted Patients
```dax
Total Admitted = 
CALCULATE(
    COUNTROWS(Fact_ED_Encounters),
    Fact_ED_Encounters[IsAdmitted] = 1
)
```

### Total LWBS (Left Without Being Seen)
```dax
Total LWBS = 
CALCULATE(
    COUNTROWS(Fact_ED_Encounters),
    Fact_ED_Encounters[IsLWBS] = 1
)
```

### Total Inpatient Stays
```dax
Total Inpatient Stays = 
COUNTROWS(Fact_Inpatient_Stays)
```

---

## 2. Operational Rates & Conversion Ratios

### LWBS Rate (%)
*Benchmark: High-performing hospitals aim for `< 2.0%`.*
```dax
LWBS Rate % = 
DIVIDE(
    [Total LWBS],
    [Total Arrivals],
    0
)
```
*(Format as: `0.0%`)*

### Admission Rate (%)
```dax
Admission Rate % = 
DIVIDE(
    [Total Admitted],
    [Total Arrivals],
    0
)
```
*(Format as: `0.0%`)*

### 30-Day Readmission Rate (%)
*CMS Hospital Readmissions Reduction Program metric.*
```dax
30-Day Readmission Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(Fact_Inpatient_Stays), Fact_Inpatient_Stays[Is30DayReadmission] = 1),
    [Total Inpatient Stays],
    0
)
```
*(Format as: `0.0%`)*

---

## 3. Clinical Wait Time & Flow Metrics (The Bottlenecks)

### Median Door-to-Doctor Wait Time (Minutes)
*Median is clinically preferred over mean because high-wait outliers skew averages.*
```dax
Median Wait Time (Min) = 
MEDIAN(Fact_ED_Encounters[WaitTimeMinutes])
```

### 90th Percentile Wait Time (Minutes)
*Measures peak queuing delay experience for the most delayed 10% of patients.*
```dax
90th Percentile Wait Time (Min) = 
PERCENTILE.INC(Fact_ED_Encounters[WaitTimeMinutes], 0.90)
```

### Average ED Length of Stay (Hours)
```dax
Avg ED LOS (Hours) = 
DIVIDE(
    AVERAGE(Fact_ED_Encounters[EDLOSMinutes]),
    60,
    0
)
```
*(Format as: `0.0 hrs`)*

### Median Boarding Time (Hours)
*Duration admitted patients spend stranded in ED hallways waiting for an open inpatient bed.*
```dax
Median Boarding Time (Hours) = 
CALCULATE(
    DIVIDE(MEDIAN(Fact_ED_Encounters[BoardingTimeMinutes]), 60, 0),
    Fact_ED_Encounters[IsAdmitted] = 1
)
```

### Average Inpatient Length of Stay (Days)
```dax
Avg Inpatient LOS (Days) = 
AVERAGE(Fact_Inpatient_Stays[InpatientLOSDays])
```

---

## 4. Bed Capacity & Hospital Occupancy Modeling

### Bed Occupancy Rate (%)
*Calculates inpatient bed utilization against total operational licensed beds (450 total hospital capacity).*
```dax
Bed Occupancy Rate % = 
VAR TotalOccupiedBedDays = SUM(Fact_Inpatient_Stays[InpatientLOSDays])
VAR TotalAvailableBedDays = SUM(Dim_Departments[BedCapacity]) * DISTINCTCOUNT(Dim_Date[DateKey])
RETURN
DIVIDE(TotalOccupiedBedDays, TotalAvailableBedDays, 0)
```

---

## 5. Time Intelligence & Growth (MoM / YoY)

### Prior Month Arrivals
```dax
Prior Month Arrivals = 
CALCULATE(
    [Total Arrivals],
    DATEADD(Dim_Date[FullDate], -1, MONTH)
)
```

### Month-over-Month (MoM) Arrival Growth %
```dax
Arrivals MoM Growth % = 
DIVIDE(
    [Total Arrivals] - [Prior Month Arrivals],
    [Prior Month Arrivals],
    0
)
```
*(Format as: `+0.0%;-0.0%;0.0%`)*

---

## 6. Dynamic KPI Conditional Color Coding

### LWBS Status Color (Hex)
*Green for under 2%, Amber for 2% - 3%, Red for > 3%*
```dax
LWBS Status Color = 
SWITCH(
    TRUE(),
    [LWBS Rate %] <= 0.02, "#107C41",  -- Dark Green
    [LWBS Rate %] <= 0.035, "#D83B01", -- Amber / Orange
    "#A80000"                           -- Dark Red
)
```

### Boarding Alert Indicator
```dax
Boarding Time Alert = 
IF(
    [Median Boarding Time (Hours)] > 4.0,
    "🚨 CRITICAL BOARDING DELAY (> 4 hrs)",
    "✓ Operational SLA Compliant (< 4 hrs)"
)
```

---

## 7. What-If Scenario Modeling (Simulating Bed & Staff Expansion)

To build the interactive What-If slider in Power BI:
1. Go to **Modeling** tab $\to$ **New Parameter** $\to$ **Numeric Range**.
2. Name: `Target Triage Wait Reduction %`, Min: `0%`, Max: `50%`, Increment: `5%`.
3. Create the simulated impact measure:

```dax
Simulated LWBS Rate % = 
VAR ReductionFactor = 1 - ('Target Triage Wait Reduction %'[Target Triage Wait Reduction % Value] / 100)
RETURN
[LWBS Rate %] * ReductionFactor
```

```dax
Estimated Annual Revenue Saved = 
VAR PreventedLWBSPatients = [Total LWBS] * ('Target Triage Wait Reduction %'[Target Triage Wait Reduction % Value] / 100)
VAR AvgPatientBilling = 850
RETURN
PreventedLWBSPatients * AvgPatientBilling
```
