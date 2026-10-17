-- =========================================================================
-- VitalFlow Healthcare BI - MS SQL Server Schema Setup
-- Database: VitalFlow_Healthcare_DW
-- Architecture: Star Schema (Kimball Methodology)
-- =========================================================================

-- 1. Create Database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'VitalFlow_Healthcare_DW')
BEGIN
    CREATE DATABASE VitalFlow_Healthcare_DW;
END
GO

USE VitalFlow_Healthcare_DW;
GO

-- 2. Drop existing foreign keys and tables if re-running
IF OBJECT_ID('dbo.Fact_Inpatient_Stays', 'U') IS NOT NULL DROP TABLE dbo.Fact_Inpatient_Stays;
IF OBJECT_ID('dbo.Fact_ED_Encounters', 'U') IS NOT NULL DROP TABLE dbo.Fact_ED_Encounters;
IF OBJECT_ID('dbo.Dim_Patients', 'U') IS NOT NULL DROP TABLE dbo.Dim_Patients;
IF OBJECT_ID('dbo.Dim_Physicians', 'U') IS NOT NULL DROP TABLE dbo.Dim_Physicians;
IF OBJECT_ID('dbo.Dim_Departments', 'U') IS NOT NULL DROP TABLE dbo.Dim_Departments;
IF OBJECT_ID('dbo.Dim_Date', 'U') IS NOT NULL DROP TABLE dbo.Dim_Date;
GO

-- =========================================================================
-- DIMENSION TABLES
-- =========================================================================

-- Dim_Date
CREATE TABLE dbo.Dim_Date (
    DateKey INT PRIMARY KEY,
    FullDate DATE NOT NULL,
    [Year] INT NOT NULL,
    [Quarter] VARCHAR(5) NOT NULL,
    MonthNum INT NOT NULL,
    MonthName VARCHAR(20) NOT NULL,
    MonthShort VARCHAR(5) NOT NULL,
    [Day] INT NOT NULL,
    DayOfWeekNum INT NOT NULL,
    DayOfWeekName VARCHAR(15) NOT NULL,
    IsWeekend BIT NOT NULL,
    IsHoliday BIT NOT NULL,
    HolidayName VARCHAR(50) NULL
);

-- Dim_Departments
CREATE TABLE dbo.Dim_Departments (
    DepartmentID VARCHAR(20) PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL,
    DepartmentType VARCHAR(50) NOT NULL,
    BedCapacity INT NOT NULL,
    NurseToPatientRatio VARCHAR(20) NOT NULL,
    FloorNumber INT NOT NULL
);

-- Dim_Physicians
CREATE TABLE dbo.Dim_Physicians (
    PhysicianID VARCHAR(20) PRIMARY KEY,
    PhysicianName VARCHAR(100) NOT NULL,
    Specialty VARCHAR(100) NOT NULL,
    PrimaryShift VARCHAR(50) NOT NULL,
    YearsExperience INT NOT NULL
);

-- Dim_Patients
CREATE TABLE dbo.Dim_Patients (
    PatientID VARCHAR(20) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Age INT NOT NULL,
    AgeGroup VARCHAR(20) NOT NULL,
    InsuranceProvider VARCHAR(50) NOT NULL,
    ZipCode VARCHAR(10) NOT NULL,
    IsHighRisk BIT NOT NULL
);

-- =========================================================================
-- FACT TABLES
-- =========================================================================

-- Fact_ED_Encounters
CREATE TABLE dbo.Fact_ED_Encounters (
    EncounterID VARCHAR(30) PRIMARY KEY,
    PatientID VARCHAR(20) NOT NULL,
    PhysicianID VARCHAR(20) NOT NULL,
    ArrivalTimestamp DATETIME2 NOT NULL,
    ArrivalDateKey INT NOT NULL,
    ArrivalHour INT NOT NULL,
    TriageTimestamp DATETIME2 NOT NULL,
    DoctorAssignedTimestamp DATETIME2 NULL,
    DispositionTimestamp DATETIME2 NOT NULL,
    DepartureTimestamp DATETIME2 NOT NULL,
    TriageAcuityESI INT NOT NULL CHECK (TriageAcuityESI BETWEEN 1 AND 5),
    ChiefComplaint VARCHAR(100) NOT NULL,
    Disposition VARCHAR(50) NOT NULL,
    WaitTimeMinutes INT NULL,
    EDLOSMinutes INT NOT NULL,
    BoardingTimeMinutes INT NOT NULL DEFAULT 0,
    IsLWBS BIT NOT NULL,
    IsAdmitted BIT NOT NULL,
    EDCostUSD DECIMAL(10, 2) NOT NULL,
    CONSTRAINT FK_ED_Patient FOREIGN KEY (PatientID) REFERENCES dbo.Dim_Patients(PatientID),
    CONSTRAINT FK_ED_Physician FOREIGN KEY (PhysicianID) REFERENCES dbo.Dim_Physicians(PhysicianID),
    CONSTRAINT FK_ED_Date FOREIGN KEY (ArrivalDateKey) REFERENCES dbo.Dim_Date(DateKey)
);

-- Fact_Inpatient_Stays
CREATE TABLE dbo.Fact_Inpatient_Stays (
    StayID VARCHAR(30) PRIMARY KEY,
    EncounterID VARCHAR(30) NOT NULL,
    PatientID VARCHAR(20) NOT NULL,
    DepartmentID VARCHAR(20) NOT NULL,
    AdmitTimestamp DATETIME2 NOT NULL,
    AdmitDateKey INT NOT NULL,
    DischargeTimestamp DATETIME2 NOT NULL,
    DischargeDateKey INT NOT NULL,
    InpatientLOSDays DECIMAL(5, 2) NOT NULL,
    DischargeDisposition VARCHAR(50) NOT NULL,
    Is30DayReadmission BIT NOT NULL,
    TotalInpatientCostUSD DECIMAL(12, 2) NOT NULL,
    CONSTRAINT FK_IP_Encounter FOREIGN KEY (EncounterID) REFERENCES dbo.Fact_ED_Encounters(EncounterID),
    CONSTRAINT FK_IP_Patient FOREIGN KEY (PatientID) REFERENCES dbo.Dim_Patients(PatientID),
    CONSTRAINT FK_IP_Department FOREIGN KEY (DepartmentID) REFERENCES dbo.Dim_Departments(DepartmentID),
    CONSTRAINT FK_IP_AdmitDate FOREIGN KEY (AdmitDateKey) REFERENCES dbo.Dim_Date(DateKey)
);

-- Indexes for high-performance Power BI DirectQuery & Analytical queries
CREATE NONCLUSTERED INDEX IX_ED_ArrivalDateKey ON dbo.Fact_ED_Encounters(ArrivalDateKey) INCLUDE (TriageAcuityESI, WaitTimeMinutes, IsLWBS, IsAdmitted);
CREATE NONCLUSTERED INDEX IX_ED_PatientID ON dbo.Fact_ED_Encounters(PatientID);
CREATE NONCLUSTERED INDEX IX_IP_DepartmentID ON dbo.Fact_Inpatient_Stays(DepartmentID) INCLUDE (InpatientLOSDays, Is30DayReadmission);
CREATE NONCLUSTERED INDEX IX_IP_AdmitDateKey ON dbo.Fact_Inpatient_Stays(AdmitDateKey);
GO

PRINT 'VitalFlow Healthcare DW Schema Created Successfully!';
GO
