-- =========================================================================
-- VitalFlow Healthcare BI - MS SQL Server Bulk Data Ingestion
-- Note: Update the path variable below to your actual machine path if running via SSMS.
-- Default path: C:\Users\achar\.gemini\antigravity\scratch\vitalflow-healthcare-bi\data\raw\
-- =========================================================================

USE VitalFlow_Healthcare_DW;
GO

-- 1. Ingest Dim_Date
PRINT 'Loading Dim_Date...';
BULK INSERT dbo.Dim_Date
FROM 'C:\Users\achar\.gemini\antigravity\scratch\vitalflow-healthcare-bi\data\raw\dim_date.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

-- 2. Ingest Dim_Departments
PRINT 'Loading Dim_Departments...';
BULK INSERT dbo.Dim_Departments
FROM 'C:\Users\achar\.gemini\antigravity\scratch\vitalflow-healthcare-bi\data\raw\dim_departments.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

-- 3. Ingest Dim_Physicians
PRINT 'Loading Dim_Physicians...';
BULK INSERT dbo.Dim_Physicians
FROM 'C:\Users\achar\.gemini\antigravity\scratch\vitalflow-healthcare-bi\data\raw\dim_physicians.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

-- 4. Ingest Dim_Patients
PRINT 'Loading Dim_Patients...';
BULK INSERT dbo.Dim_Patients
FROM 'C:\Users\achar\.gemini\antigravity\scratch\vitalflow-healthcare-bi\data\raw\dim_patients.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

-- 5. Ingest Fact_ED_Encounters
PRINT 'Loading Fact_ED_Encounters...';
BULK INSERT dbo.Fact_ED_Encounters
FROM 'C:\Users\achar\.gemini\antigravity\scratch\vitalflow-healthcare-bi\data\raw\fact_ed_encounters.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

-- 6. Ingest Fact_Inpatient_Stays
PRINT 'Loading Fact_Inpatient_Stays...';
BULK INSERT dbo.Fact_Inpatient_Stays
FROM 'C:\Users\achar\.gemini\antigravity\scratch\vitalflow-healthcare-bi\data\raw\fact_inpatient_stays.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO

-- Verification Queries
SELECT 'Dim_Date' AS TableName, COUNT(*) AS TotalRows FROM dbo.Dim_Date
UNION ALL
SELECT 'Dim_Departments', COUNT(*) FROM dbo.Dim_Departments
UNION ALL
SELECT 'Dim_Physicians', COUNT(*) FROM dbo.Dim_Physicians
UNION ALL
SELECT 'Dim_Patients', COUNT(*) FROM dbo.Dim_Patients
UNION ALL
SELECT 'Fact_ED_Encounters', COUNT(*) FROM dbo.Fact_ED_Encounters
UNION ALL
SELECT 'Fact_Inpatient_Stays', COUNT(*) FROM dbo.Fact_Inpatient_Stays;
GO
