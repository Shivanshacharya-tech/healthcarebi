"""
VitalFlow Healthcare BI - Synthetic Data Generator
Generates realistic, statistically calibrated hospital operational data:
- dim_patients.csv
- dim_departments.csv
- dim_physicians.csv
- dim_date.csv
- fact_ed_encounters.csv
- fact_inpatient_stays.csv
"""

import csv
import random
from datetime import datetime, timedelta
import math
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

START_DATE = datetime(2024, 1, 1, 0, 0, 0)
END_DATE = datetime(2024, 12, 31, 23, 59, 59)
TOTAL_DAYS = (END_DATE - START_DATE).days + 1

# -------------------------------------------------------------
# 1. DIM_DATE
# -------------------------------------------------------------
print("Generating dim_date.csv...")
date_records = []
current = START_DATE
holidays_2024 = {
    "2024-01-01": "New Year's Day",
    "2024-01-15": "MLK Day",
    "2024-05-27": "Memorial Day",
    "2024-07-04": "Independence Day",
    "2024-09-02": "Labor Day",
    "2024-11-28": "Thanksgiving",
    "2024-12-25": "Christmas Day"
}

while current <= END_DATE:
    d_str = current.strftime("%Y-%m-%d")
    is_weekend = 1 if current.weekday() in (5, 6) else 0
    is_holiday = 1 if d_str in holidays_2024 else 0
    date_records.append({
        "date_key": int(current.strftime("%Y%m%d")),
        "full_date": d_str,
        "year": current.year,
        "quarter": f"Q{(current.month - 1) // 3 + 1}",
        "month_num": current.month,
        "month_name": current.strftime("%B"),
        "month_short": current.strftime("%b"),
        "day": current.day,
        "day_of_week_num": current.isoweekday(),
        "day_of_week_name": current.strftime("%A"),
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "holiday_name": holidays_2024.get(d_str, "")
    })
    current += timedelta(days=1)

with open(os.path.join(OUTPUT_DIR, "dim_date.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=date_records[0].keys())
    writer.writeheader()
    writer.writerows(date_records)

# -------------------------------------------------------------
# 2. DIM_DEPARTMENTS
# -------------------------------------------------------------
print("Generating dim_departments.csv...")
departments = [
    {"department_id": "DEP-ED", "department_name": "Emergency Department", "department_type": "Emergency", "bed_capacity": 45, "nurse_to_patient_ratio": "1:3", "floor_number": 1},
    {"department_id": "DEP-ICU", "department_name": "Intensive Care Unit (ICU)", "department_type": "Critical Care", "bed_capacity": 30, "nurse_to_patient_ratio": "1:1", "floor_number": 2},
    {"department_id": "DEP-MEDSURG", "department_name": "Medical-Surgical Ward", "department_type": "Inpatient", "bed_capacity": 140, "nurse_to_patient_ratio": "1:5", "floor_number": 3},
    {"department_id": "DEP-CARD", "department_name": "Cardiology / CCU", "department_type": "Step-Down Care", "bed_capacity": 50, "nurse_to_patient_ratio": "1:3", "floor_number": 4},
    {"department_id": "DEP-PED", "department_name": "Pediatric Inpatient Unit", "department_type": "Inpatient", "bed_capacity": 40, "nurse_to_patient_ratio": "1:4", "floor_number": 2},
    {"department_id": "DEP-ORTHO", "department_name": "Orthopedics & Trauma Ward", "department_type": "Inpatient", "bed_capacity": 55, "nurse_to_patient_ratio": "1:4", "floor_number": 5},
    {"department_id": "DEP-ONC", "department_name": "Oncology & Palliative Care", "department_type": "Inpatient", "bed_capacity": 40, "nurse_to_patient_ratio": "1:4", "floor_number": 6}
]

with open(os.path.join(OUTPUT_DIR, "dim_departments.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=departments[0].keys())
    writer.writeheader()
    writer.writerows(departments)

# -------------------------------------------------------------
# 3. DIM_PHYSICIANS
# -------------------------------------------------------------
print("Generating dim_physicians.csv...")
physician_names = [
    ("Dr. Marcus Vance", "Emergency Medicine"),
    ("Dr. Sarah Chen", "Emergency Medicine"),
    ("Dr. Elena Rostova", "Emergency Medicine"),
    ("Dr. David Patel", "Emergency Medicine"),
    ("Dr. Emily Howard", "Emergency Medicine"),
    ("Dr. James Thorne", "Emergency Medicine"),
    ("Dr. Priya Sharma", "Critical Care / Trauma"),
    ("Dr. Alexander Wu", "Critical Care / Trauma"),
    ("Dr. Robert Gomez", "Cardiology"),
    ("Dr. Rachel Weiss", "Cardiology"),
    ("Dr. Anthony Rossi", "Internal Medicine"),
    ("Dr. Jennifer Brooks", "Internal Medicine"),
    ("Dr. Karen Mitchell", "Pediatrics"),
    ("Dr. Liam O'Connor", "Orthopedic Surgery")
]

physicians = []
for idx, (name, spec) in enumerate(physician_names, start=1):
    shift = "Morning (07:00-15:00)" if idx % 3 == 0 else ("Evening (15:00-23:00)" if idx % 3 == 1 else "Night (23:00-07:00)")
    physicians.append({
        "physician_id": f"DOC-{100 + idx}",
        "physician_name": name,
        "specialty": spec,
        "primary_shift": shift,
        "years_experience": random.randint(3, 25)
    })

with open(os.path.join(OUTPUT_DIR, "dim_physicians.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=physicians[0].keys())
    writer.writeheader()
    writer.writerows(physicians)

# -------------------------------------------------------------
# 4. DIM_PATIENTS
# -------------------------------------------------------------
print("Generating dim_patients.csv (8,000 patient master profiles)...")
FIRST_NAMES_M = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Daniel", "Matthew", "Anthony", "Donald", "Paul"]
FIRST_NAMES_F = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris"]

INSURANCE_TYPES = ["Medicare", "Medicaid", "Blue Cross Blue Shield", "UnitedHealthcare", "Aetna", "Uninsured / Self-Pay"]
INSURANCE_WEIGHTS = [0.35, 0.20, 0.22, 0.12, 0.06, 0.05]

patients = []
NUM_PATIENTS = 8000

for pid in range(1, NUM_PATIENTS + 1):
    gender = random.choice(["Male", "Female"])
    first_name = random.choice(FIRST_NAMES_M if gender == "Male" else FIRST_NAMES_F)
    last_name = random.choice(LAST_NAMES)
    
    # Age distribution leaning towards elderly for Medicare and pediatric spikes
    age_bracket = random.choices(["pediatric", "young_adult", "middle_age", "senior", "elderly"], weights=[0.12, 0.20, 0.23, 0.25, 0.20])[0]
    if age_bracket == "pediatric":
        age = random.randint(1, 17)
        age_group = "0-17"
    elif age_bracket == "young_adult":
        age = random.randint(18, 35)
        age_group = "18-35"
    elif age_bracket == "middle_age":
        age = random.randint(36, 50)
        age_group = "36-50"
    elif age_bracket == "senior":
        age = random.randint(51, 65)
        age_group = "51-65"
    else:
        age = random.randint(66, 92)
        age_group = "66+"

    # Insurance correlation
    if age >= 65:
        ins = "Medicare"
    elif age <= 17:
        ins = random.choice(["Medicaid", "Blue Cross Blue Shield", "UnitedHealthcare"])
    else:
        ins = random.choices(INSURANCE_TYPES, weights=INSURANCE_WEIGHTS)[0]

    zip_prefix = random.choices(["90001", "90012", "90024", "90035", "90048", "90210", "90802"], weights=[0.25, 0.20, 0.18, 0.15, 0.10, 0.07, 0.05])[0]
    
    patients.append({
        "patient_id": f"PAT-{pid:05d}",
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "age": age,
        "age_group": age_group,
        "insurance_provider": ins,
        "zip_code": zip_prefix,
        "is_high_risk": 1 if (age >= 65 and random.random() < 0.35) else 0
    })

with open(os.path.join(OUTPUT_DIR, "dim_patients.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=patients[0].keys())
    writer.writeheader()
    writer.writerows(patients)

# -------------------------------------------------------------
# 5. FACT_ED_ENCOUNTERS & FACT_INPATIENT_STAYS
# -------------------------------------------------------------
print("Generating fact_ed_encounters.csv and fact_inpatient_stays.csv (~22,000 visits)...")

COMPLAINTS_BY_ESI = {
    1: ["Cardiac Arrest", "Severe Respiratory Failure", "Multiple Trauma (MVA)", "Massive Hemorrhage", "Unresponsive / Coma"],
    2: ["Severe Chest Pain (STEMI)", "Acute Stroke Symptoms", "Severe Dyspnea / Asthma Attack", "Altered Mental Status", "Sepsis Alert", "Compound Fracture"],
    3: ["Moderate Abdominal Pain", "Suspected Fracture / Dislocation", "High Persistent Fever", "Kidney Stone Colic", "Severe Laceration", "Uncontrolled Vomiting"],
    4: ["Mild Asthma / Wheezing", "Simple Closed Fracture", "Skin Abscess / Cellulitis", "Urinary Tract Infection", "Sprain / Strain", "Minor Concussion"],
    5: ["Sore Throat / Cold Symptoms", "Medication Refill Request", "Suture Removal", "Mild Rash", "Earache", "Low Back Pain (Chronic)"]
}

# ESI distribution: ESI 1 (2%), ESI 2 (18%), ESI 3 (45%), ESI 4 (25%), ESI 5 (10%)
ESI_WEIGHTS = [0.02, 0.18, 0.45, 0.25, 0.10]

# Hourly arrival curve (peak 10:00 to 22:00, trough 03:00 to 06:00)
HOURLY_WEIGHTS = [
    0.02, 0.015, 0.012, 0.01, 0.01, 0.015,  # 00:00 - 05:59
    0.025, 0.035, 0.05, 0.065, 0.075, 0.08, # 06:00 - 11:59
    0.08, 0.075, 0.07, 0.07, 0.065, 0.06,   # 12:00 - 17:59
    0.06, 0.055, 0.045, 0.035, 0.03, 0.025  # 18:00 - 23:59
]

ed_encounters = []
inpatient_stays = []
encounter_counter = 1
admission_counter = 1

patient_lookup = {p["patient_id"]: p for p in patients}
patient_ids = list(patient_lookup.keys())
ed_physician_ids = [doc["physician_id"] for doc in physicians if "Emergency" in doc["specialty"] or "Trauma" in doc["specialty"]]

current_date = START_DATE
while current_date <= END_DATE:
    # Daily volume: weekends and Mondays have higher volume
    base_daily = 60
    if current_date.weekday() in (0, 6): # Monday or Sunday
        base_daily = 72
    elif current_date.weekday() in (4, 5): # Friday or Saturday
        base_daily = 66
    
    daily_count = int(random.gauss(base_daily, 6))

    for _ in range(daily_count):
        # Determine arrival time based on hourly weights
        arr_hour = random.choices(range(24), weights=HOURLY_WEIGHTS)[0]
        arr_minute = random.randint(0, 59)
        arr_second = random.randint(0, 59)
        arrival_dt = current_date.replace(hour=arr_hour, minute=arr_minute, second=arr_second)

        # Pick patient
        pat_id = random.choice(patient_ids)
        pat = patient_lookup[pat_id]

        # Pick ESI score (older patients shift slightly to more acute)
        if pat["age"] >= 65:
            esi = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.28, 0.45, 0.17, 0.05])[0]
        elif pat["age"] <= 17:
            esi = random.choices([1, 2, 3, 4, 5], weights=[0.01, 0.12, 0.42, 0.35, 0.10])[0]
        else:
            esi = random.choices([1, 2, 3, 4, 5], weights=ESI_WEIGHTS)[0]

        chief_complaint = random.choice(COMPLAINTS_BY_ESI[esi])
        physician_id = random.choice(ed_physician_ids)

        # Triage time: 4 to 20 minutes after arrival
        triage_mins = random.randint(4, 18)
        triage_dt = arrival_dt + timedelta(minutes=triage_mins)

        # Door-to-Doctor wait time based on ESI
        if esi == 1:
            wait_mins = random.randint(0, 3) # immediate
        elif esi == 2:
            wait_mins = random.randint(5, 25)
        elif esi == 3:
            wait_mins = random.randint(25, 95)
        elif esi == 4:
            wait_mins = random.randint(45, 140)
        else:
            wait_mins = random.randint(60, 200)

        # Left Without Being Seen (LWBS) probability
        # Increases drastically if wait time > 90 mins for low acuity (ESI 4 and 5)
        is_lwbs = False
        if esi in [4, 5] and wait_mins > 80:
            lwbs_chance = 0.25 if wait_mins > 120 else 0.12
            if random.random() < lwbs_chance:
                is_lwbs = True

        if is_lwbs:
            doctor_assigned_dt = ""
            disposition_dt = arrival_dt + timedelta(minutes=wait_mins)
            departure_dt = disposition_dt
            disposition = "LWBS (Left Without Being Seen)"
            ed_los_mins = wait_mins
            boarding_mins = 0
            ed_cost = 85.0
        else:
            doctor_assigned_dt = triage_dt + timedelta(minutes=max(1, wait_mins - triage_mins))
            
            # Clinical evaluation & treatment duration in ED
            if esi == 1:
                treatment_mins = random.randint(60, 180)
            elif esi == 2:
                treatment_mins = random.randint(90, 240)
            elif esi == 3:
                treatment_mins = random.randint(80, 210)
            elif esi == 4:
                treatment_mins = random.randint(45, 120)
            else:
                treatment_mins = random.randint(30, 90)

            disposition_dt = doctor_assigned_dt + timedelta(minutes=treatment_mins)

            # Determine Disposition
            # High acuity = high admission rate
            if esi == 1:
                disp_prob = [0.03, 0.90, 0.07] # Discharged, Admitted, Transferred
            elif esi == 2:
                disp_prob = [0.25, 0.70, 0.05]
            elif esi == 3:
                disp_prob = [0.65, 0.33, 0.02]
            elif esi == 4:
                disp_prob = [0.88, 0.11, 0.01]
            else:
                disp_prob = [0.97, 0.02, 0.01]

            disposition = random.choices(["Discharged Home", "Admitted to Inpatient", "Transferred to Specialist Facility"], weights=disp_prob)[0]

            # Boarding time for admitted patients
            if disposition == "Admitted to Inpatient":
                # Boarding delay waiting for inpatient bed (critical bottleneck metric)
                # 60 to 360 mins (1 to 6 hours), sometimes higher during peak
                boarding_mins = random.randint(75, 340)
                if arr_hour in [14, 15, 16, 17, 18, 19]: # afternoon bed gridlock
                    boarding_mins += random.randint(30, 90)
                departure_dt = disposition_dt + timedelta(minutes=boarding_mins)
            else:
                boarding_mins = 0
                departure_dt = disposition_dt + timedelta(minutes=random.randint(15, 45)) # discharge paperwork

            ed_los_mins = int((departure_dt - arrival_dt).total_seconds() / 60)
            base_cost = {1: 1850.0, 2: 1200.0, 3: 750.0, 4: 420.0, 5: 250.0}[esi]
            ed_cost = round(base_cost + random.uniform(50, 400), 2)

        enc_id = f"ENC-2024-{encounter_counter:06d}"
        encounter_counter += 1

        ed_encounters.append({
            "encounter_id": enc_id,
            "patient_id": pat_id,
            "physician_id": physician_id,
            "arrival_timestamp": arrival_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_date_key": int(arrival_dt.strftime("%Y%m%d")),
            "arrival_hour": arr_hour,
            "triage_timestamp": triage_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "doctor_assigned_timestamp": doctor_assigned_dt.strftime("%Y-%m-%d %H:%M:%S") if doctor_assigned_dt else "",
            "disposition_timestamp": disposition_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "departure_timestamp": departure_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "triage_acuity_esi": esi,
            "chief_complaint": chief_complaint,
            "disposition": disposition,
            "wait_time_minutes": wait_mins if not is_lwbs else "",
            "ed_los_minutes": ed_los_mins,
            "boarding_time_minutes": boarding_mins,
            "is_lwbs": 1 if is_lwbs else 0,
            "is_admitted": 1 if disposition == "Admitted to Inpatient" else 0,
            "ed_cost_usd": ed_cost
        })

        # If admitted, generate Inpatient Stay Record
        if disposition == "Admitted to Inpatient":
            stay_id = f"IP-2024-{admission_counter:05d}"
            admission_counter += 1
            bed_assigned_dt = departure_dt # leaves ED into inpatient bed

            # Select ward based on diagnosis/esi
            if esi == 1 or "Severe" in chief_complaint or "Cardiac" in chief_complaint:
                assigned_dept = random.choice(["DEP-ICU", "DEP-CARD"])
            elif pat["age"] <= 17:
                assigned_dept = "DEP-PED"
            elif "Trauma" in chief_complaint or "Fracture" in chief_complaint:
                assigned_dept = "DEP-ORTHO"
            elif "Chest Pain" in chief_complaint or "STEMI" in chief_complaint:
                assigned_dept = "DEP-CARD"
            else:
                assigned_dept = random.choices(["DEP-MEDSURG", "DEP-CARD", "DEP-ONC"], weights=[0.60, 0.25, 0.15])[0]

            # Inpatient Length of Stay (Days)
            if assigned_dept == "DEP-ICU":
                los_days = round(random.lognormvariate(1.2, 0.5), 1)
                daily_rate = 3800.0
            elif assigned_dept == "DEP-CARD":
                los_days = round(random.lognormvariate(1.1, 0.4), 1)
                daily_rate = 2600.0
            else:
                los_days = round(random.lognormvariate(0.9, 0.4), 1)
                daily_rate = 1800.0
            
            los_days = max(1.0, min(los_days, 28.0))
            discharge_inpatient_dt = bed_assigned_dt + timedelta(days=los_days)

            # Readmission within 30 days flag (10-18% typical benchmark)
            # Higher for elderly or cardiac/sepsis cases
            readmit_prob = 0.18 if (pat["age"] >= 65 or assigned_dept in ["DEP-ICU", "DEP-CARD"]) else 0.08
            is_readmitted = 1 if random.random() < readmit_prob else 0

            # Discharge disposition
            if assigned_dept == "DEP-ICU" and random.random() < 0.05:
                ip_disp = "Expired (Deceased)"
            elif pat["age"] >= 75 and random.random() < 0.25:
                ip_disp = "Skilled Nursing Facility (SNF)"
            elif random.random() < 0.12:
                ip_disp = "Home Health Care"
            else:
                ip_disp = "Routine Discharge Home"

            total_cost = round((los_days * daily_rate) + ed_cost + random.uniform(500, 3000), 2)

            inpatient_stays.append({
                "stay_id": stay_id,
                "encounter_id": enc_id,
                "patient_id": pat_id,
                "department_id": assigned_dept,
                "admit_timestamp": bed_assigned_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "admit_date_key": int(bed_assigned_dt.strftime("%Y%m%d")),
                "discharge_timestamp": discharge_inpatient_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "discharge_date_key": int(discharge_inpatient_dt.strftime("%Y%m%d")),
                "inpatient_los_days": los_days,
                "discharge_disposition": ip_disp,
                "is_30day_readmission": is_readmitted,
                "total_inpatient_cost_usd": total_cost
            })

    current_date += timedelta(days=1)

# Write ED Encounters
print(f"Writing {len(ed_encounters)} ED encounters...")
with open(os.path.join(OUTPUT_DIR, "fact_ed_encounters.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=ed_encounters[0].keys())
    writer.writeheader()
    writer.writerows(ed_encounters)

# Write Inpatient Stays
print(f"Writing {len(inpatient_stays)} Inpatient stays...")
with open(os.path.join(OUTPUT_DIR, "fact_inpatient_stays.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=inpatient_stays[0].keys())
    writer.writeheader()
    writer.writerows(inpatient_stays)

print(f"\n[SUCCESS] Generated all 6 relational datasets in: {OUTPUT_DIR}")
print(f"  - dim_date.csv ({len(date_records)} rows)")
print(f"  - dim_departments.csv ({len(departments)} rows)")
print(f"  - dim_physicians.csv ({len(physicians)} rows)")
print(f"  - dim_patients.csv ({len(patients)} rows)")
print(f"  - fact_ed_encounters.csv ({len(ed_encounters)} rows)")
print(f"  - fact_inpatient_stays.csv ({len(inpatient_stays)} rows)")
