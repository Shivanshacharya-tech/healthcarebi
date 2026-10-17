# Power Query (M) Scripts for MS SQL Server Connection

You can import all 6 tables from your local SQL Server instance using **Get Data -> SQL Server Database** with Server: `localhost` and Database: `VitalFlow_Healthcare_DW`.

Alternatively, in Power Query Editor, go to **Home -> New Source -> Blank Query -> Advanced Editor** and paste each snippet:

---

### 1. `Dim_Date`
```powerquery
let
    Source = Sql.Database("localhost", "VitalFlow_Healthcare_DW", [Query="SELECT * FROM dbo.Dim_Date"])
in
    Source
```

### 2. `Dim_Departments`
```powerquery
let
    Source = Sql.Database("localhost", "VitalFlow_Healthcare_DW", [Query="SELECT * FROM dbo.Dim_Departments"])
in
    Source
```

### 3. `Dim_Physicians`
```powerquery
let
    Source = Sql.Database("localhost", "VitalFlow_Healthcare_DW", [Query="SELECT * FROM dbo.Dim_Physicians"])
in
    Source
```

### 4. `Dim_Patients`
```powerquery
let
    Source = Sql.Database("localhost", "VitalFlow_Healthcare_DW", [Query="SELECT * FROM dbo.Dim_Patients"])
in
    Source
```

### 5. `Fact_ED_Encounters`
```powerquery
let
    Source = Sql.Database("localhost", "VitalFlow_Healthcare_DW", [Query="SELECT * FROM dbo.Fact_ED_Encounters"])
in
    Source
```

### 6. `Fact_Inpatient_Stays`
```powerquery
let
    Source = Sql.Database("localhost", "VitalFlow_Healthcare_DW", [Query="SELECT * FROM dbo.Fact_Inpatient_Stays"])
in
    Source
```

---

## Star Schema Relationship Configuration in Model View

Once imported, navigate to the **Model View** tab in Power BI Desktop and ensure the following $1:N$ single-direction relationships are active:

| From Table (Dimension) | Column | To Table (Fact) | Column | Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dim_Date** | `DateKey` | **Fact_ED_Encounters** | `ArrivalDateKey` | $1:*$ | Single |
| **Dim_Date** | `DateKey` | **Fact_Inpatient_Stays** | `AdmitDateKey` | $1:*$ | Single |
| **Dim_Patients** | `PatientID`| **Fact_ED_Encounters** | `PatientID` | $1:*$ | Single |
| **Dim_Patients** | `PatientID`| **Fact_Inpatient_Stays**| `PatientID` | $1:*$ | Single |
| **Dim_Physicians**| `PhysicianID`| **Fact_ED_Encounters**| `PhysicianID` | $1:*$ | Single |
| **Dim_Departments**| `DepartmentID`| **Fact_Inpatient_Stays**| `DepartmentID`| $1:*$ | Single |
| **Fact_ED_Encounters**| `EncounterID`| **Fact_Inpatient_Stays**| `EncounterID`| $1:1$ or $1:*$ | Single |
