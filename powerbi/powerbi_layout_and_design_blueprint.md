# VitalFlow Healthcare BI - Complete Power BI Visual Layout Blueprint

This design blueprint provides the visual hierarchy, component positioning, visual types, and field mappings for your 3-page Power BI executive suite.

---

## 🎨 Global Report Settings & Canvas Setup
* **Canvas Size:** `16:9` widescreen (`1280 x 720 px`)
* **Page Background:** `#F4F6F9` (Light Healthcare Slate Gray)
* **Card & Container Background:** `#FFFFFF` (Pure White with 4px border radius and subtle drop shadow)
* **Theme:** Import [`powerbi/vitalflow_theme.json`](file:///C:/Users/achar/.gemini/antigravity/scratch/vitalflow-healthcare-bi/powerbi/vitalflow_theme.json) (**View tab -> Themes -> Browse for themes**).

---

## 📄 PAGE 1: Executive Operations Hub
*Target Audience: Chief Operating Officer (COO), Chief Medical Officer (CMO)*
*Objective: High-level volume tracking, SLA breach detection, and peak load identification.*

### Top Navigation & Slicer Bar (Y: 10px to 80px)
* **Report Title:** Text Box: `VitalFlow | Hospital Operations & Emergency Department Executive Suite` (Font: Segoe UI Bold, 16pt, `#0B2545`).
* **Slicers (Top Right):**
  1. `Date Range`: Between slider on `Dim_Date[FullDate]`.
  2. `Quarter`: Button group (`Q1`, `Q2`, `Q3`, `Q4`) on `Dim_Date[Quarter]`.
  3. `Day Type`: Dropdown filter on `Dim_Date[IsWeekend]` (All, Weekday, Weekend).

### Row 1: Executive KPI Cards (Y: 90px to 190px)
Place 5 uniform KPI Cards (Width: 230px, Height: 95px):
1. **Total ED Volume:** Measure `[Total Arrivals]` | Subtext: `[Arrivals MoM Growth %]`
2. **Median Wait Time:** Measure `[Median Wait Time (Min)]` | Target: `< 30 min` (Conditional font color: Green if $\le 30$, Red if $> 45$)
3. **90th Percentile Wait:** Measure `[90th Percentile Wait Time (Min)]` | Subtitle: `Peak Queuing Delay`
4. **LWBS Rate (%):** Measure `[LWBS Rate %]` | Target: `< 2.0%` (Conditional background color using `[LWBS Status Color]`)
5. **Bed Occupancy (%):** Measure `[Bed Occupancy Rate %]` | Target: `< 85.0%` (Amber alert threshold at $85\%$)

### Row 2: Operational Volume Diagnostics (Y: 205px to 450px)
* **Visual 1 (Left - 60% Width): Hourly Arrival & Wait Time Heatmap Matrix**
  * *Visual Type:* **Matrix Visual**
  * *Rows:* `Dim_Date[DayOfWeekName]` (sorted by `DayOfWeekNum`)
  * *Columns:* `Fact_ED_Encounters[ArrivalHour]` (0 to 23)
  * *Values:* `[Total Arrivals]`
  * *Conditional Formatting:* Background color gradient (Lowest value `#E0F2FE` Light Blue $\to$ Highest value `#0B2545` Deep Navy).
  * *Key Finding:* Highlights Sunday and Monday afternoon/evening spikes (14:00 to 21:00) requiring nursing shift reinforcement.
* **Visual 2 (Right - 40% Width): Triage Acuity Distribution (ESI 1 to 5)**
  * *Visual Type:* **Donut Chart**
  * *Legend:* `Fact_ED_Encounters[TriageAcuityESI]` (ESI 1: Resuscitation, ESI 2: Emergent, ESI 3: Urgent, ESI 4: Semi-Urgent, ESI 5: Non-Urgent)
  * *Values:* `[Total Arrivals]`
  * *Data Labels:* Category and % of Total.

### Row 3: Daily Trend & Departure Disposition (Y: 465px to 695px)
* **Visual 3 (Left - 65% Width): Daily Volume & 7-Day Rolling Average**
  * *Visual Type:* **Line and Clustered Column Chart**
  * *X-Axis:* `Dim_Date[FullDate]`
  * *Column Y-Axis:* `[Total Arrivals]` (Soft Blue `#B0C4DE`)
  * *Line Y-Axis:* 7-day moving average `[Total Arrivals 7D MA]` (Navy Blue `#0B2545`, stroke 3px).
* **Visual 4 (Right - 35% Width): Final Disposition Breakdown**
  * *Visual Type:* **100% Stacked Bar Chart**
  * *Y-Axis:* `Fact_ED_Encounters[TriageAcuityESI]`
  * *X-Axis:* `Fact_ED_Encounters[Disposition]` (Admitted, Discharged, LWBS, Transferred)
  * *Insight:* Demonstrates that ESI 1 & 2 convert almost entirely to inpatient admission, whereas ESI 4 & 5 represent walk-ins at risk of LWBS.

---

## 📄 PAGE 2: Clinical Flow & ED Bottlenecks
*Target Audience: Emergency Department Medical Director, Nurse Managers*
*Objective: Uncover process bottlenecks, door-to-eval delays, and the "LWBS Cliff".*

### Row 1: KPI Cards (Y: 90px to 190px)
1. **Average Door-to-Doctor:** Measure `[Avg Door to Doctor Mins]`
2. **Median Boarding Time:** Measure `[Median Boarding Time (Hours)]` | Benchmark: `< 2.0 hrs` (Actual: $3.3\text{ hrs}$)
3. **Average ED Length of Stay:** Measure `[Avg ED LOS (Hours)]` (Split by Admitted vs. Discharged)
4. **Estimated LWBS Billing Lost:** Measure `[Total LWBS] * 850` (Lost opportunity cost)

### Row 2: Patient Journey Funnel & The LWBS Cliff (Y: 205px to 450px)
* **Visual 1 (Left - 45% Width): Patient Dwell Time Funnel**
  * *Visual Type:* **Funnel Chart** or **Horizontal Clustered Bar**
  * *Stages:*
    1. Arrival $\to$ Triage Complete (Avg: 11 mins)
    2. Triage $\to$ Physician Exam (Avg: 35 mins)
    3. Physician Exam $\to$ Clinical Disposition (Avg: 145 mins)
    4. Disposition $\to$ Departure / Inpatient Bed (Avg: 198 mins for admitted)
  * *Finding:* Stage 4 (Boarding delay) is the single largest component of total patient stay.
* **Visual 2 (Right - 55% Width): The "LWBS Cliff" Scatterplot**
  * *Visual Type:* **Scatter Chart**
  * *X-Axis:* `Fact_ED_Encounters[WaitTimeMinutes]` (Binned in 15-minute intervals)
  * *Y-Axis:* `[LWBS Rate %]`
  * *Legend:* `Fact_ED_Encounters[TriageAcuityESI]`
  * *Insight:* Patients in ESI 4 and 5 tolerate waits up to 60 minutes with $<1\%$ LWBS. After 90 minutes, LWBS probability climbs exponentially to $>15\%$.

### Row 3: Staffing Shift Throughput & Physician Metrics (Y: 465px to 695px)
* **Visual 3 (Left - 50% Width): Physician Workload & Turnaround Time**
  * *Visual Type:* **Table / Matrix with Data Bars**
  * *Columns:* `Dim_Physicians[PhysicianName]`, `Dim_Physicians[Specialty]`, `Dim_Physicians[PrimaryShift]`, `[Total Patients Treated]`, `[Avg Door to Doctor Mins]`, `[Admission Rate %]`.
* **Visual 4 (Right - 50% Width): Shift Volume vs. Staffing Coverage**
  * *Visual Type:* **Clustered Column Chart**
  * *X-Axis:* `Dim_Physicians[PrimaryShift]` (Morning, Evening, Night)
  * *Y-Axis:* `[Total Arrivals]`, `[Median Wait Time (Min)]`
  * *Action Item:* Shift reallocation: Evening shift handles 52% of total volume with only 33% of physician staffing.

---

## 📄 PAGE 3: Inpatient Capacity & What-If Simulator
*Target Audience: VP of Nursing, Bed Management Committee, Hospital CFO*
*Objective: Track ward-level bed saturation, boarding hours, readmission risk, and model ROI.*

### Row 1: Bed Occupancy Gauges by Ward (Y: 90px to 230px)
Place 4 **Gauge Visuals** side-by-side:
1. **Intensive Care Unit (ICU):** Target: $80\%$, Max: $100\%$, Current: $88.5\%$ (Red Flag 🚨)
2. **Cardiology / Step-Down:** Target: $85\%$, Max: $100\%$, Current: $91.2\%$ (Red Flag 🚨)
3. **Medical-Surgical Ward:** Target: $85\%$, Max: $100\%$, Current: $86.8\%$ (Amber Flag ⚠️)
4. **Pediatric Unit:** Target: $80\%$, Max: $100\%$, Current: $58.0\%$ (Green Flag ✓)

### Row 2: Inpatient Length of Stay & 30-Day Readmissions (Y: 245px to 475px)
* **Visual 1 (Left - 50% Width): Average LOS (Days) vs. 30-Day Readmission Rate %**
  * *Visual Type:* **Scatter Chart** or **Bubble Chart**
  * *X-Axis:* `[Avg Inpatient LOS (Days)]`
  * *Y-Axis:* `[30-Day Readmission Rate %]`
  * *Size:* `[Total Inpatient Stays]`
  * *Details:* `Dim_Departments[DepartmentName]`
  * *Key Insight:* Cardiology and ICU patients exhibit the highest readmission rates ($18.9\%$ and $19.7\%$), driving up avoidable care costs.
* **Visual 2 (Right - 50% Width): Inpatient Ward Cost & Revenue Impact**
  * *Visual Type:* **Treemap**
  * *Group:* `Dim_Departments[DepartmentName]`
  * *Values:* `SUM(Fact_Inpatient_Stays[TotalInpatientCostUSD])`
  * *Color:* Readmission Rate %

### Row 3: Interactive What-If ROI Scenario Simulator (Y: 490px to 695px)
*Create a highlighted grey callout box titled: **"Executive Decision Support: Fast-Track Triage Investment Simulation"***
* **Interactive Control (Left - 30% Width):**
  * Slider connected to What-If parameter: `'Target Triage Wait Reduction %'` ($0\%$ to $50\%$).
* **Simulation Result KPI Cards (Center - 40% Width):**
  * Card 1: **Simulated LWBS Rate:** `[Simulated LWBS Rate %]` (Shows dynamic drop from 3.8% down to 1.9%).
  * Card 2: **Annual Revenue Preserved:** `[Estimated Annual Revenue Saved]` (Displays projected \$350K - \$500K saved).
* **Narrative Recommendation (Right - 30% Width):**
  * Text Card summarizing executive recommendation:
    > *"Deploying 1 dedicated Fast-Track Physician Assistant between 14:00 and 20:00 will reduce low-acuity triage delays by 35%, slashing LWBS departures by ~450 patients annually and recapturing approximately **\$382,500** in lost outpatient hospital revenue."*
