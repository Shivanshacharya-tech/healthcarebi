-- =========================================================================
-- VitalFlow Healthcare BI - MS SQL Server Analytical Views & Procedures
-- Database: VitalFlow_Healthcare_DW
-- Purpose: Pre-calculated views for Power BI DirectQuery / Import reporting
-- =========================================================================

USE VitalFlow_Healthcare_DW;
GO

-- 1. Executive Operations Daily Summary View
CREATE OR ALTER VIEW dbo.vw_ED_Executive_Daily AS
SELECT 
    d.FullDate,
    d.[Year],
    d.MonthName,
    d.DayOfWeekName,
    d.IsWeekend,
    d.IsHoliday,
    COUNT(f.EncounterID) AS TotalArrivals,
    SUM(CASE WHEN f.IsLWBS = 1 THEN 1 ELSE 0 END) AS TotalLWBS,
    ROUND(CAST(SUM(CASE WHEN f.IsLWBS = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(f.EncounterID) * 100, 2) AS LWBSRatePct,
    SUM(CASE WHEN f.IsAdmitted = 1 THEN 1 ELSE 0 END) AS TotalAdmitted,
    ROUND(CAST(SUM(CASE WHEN f.IsAdmitted = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(f.EncounterID) * 100, 2) AS AdmissionRatePct,
    ROUND(AVG(CAST(f.WaitTimeMinutes AS FLOAT)), 1) AS AvgWaitTimeMinutes,
    ROUND(AVG(CAST(f.EDLOSMinutes AS FLOAT)), 1) AS AvgEDLOSMinutes,
    ROUND(AVG(CASE WHEN f.IsAdmitted = 1 THEN CAST(f.BoardingTimeMinutes AS FLOAT) ELSE NULL END), 1) AS AvgBoardingMinutes,
    SUM(f.EDCostUSD) AS TotalEDRevenueUSD
FROM dbo.Fact_ED_Encounters f
JOIN dbo.Dim_Date d ON f.ArrivalDateKey = d.DateKey
GROUP BY 
    d.FullDate, d.[Year], d.MonthName, d.DayOfWeekName, d.IsWeekend, d.IsHoliday;
GO

-- 2. Hourly Arrival & Wait Time Heatmap Matrix View
CREATE OR ALTER VIEW dbo.vw_Hourly_Arrival_Heatmap AS
SELECT 
    d.DayOfWeekNum,
    d.DayOfWeekName,
    f.ArrivalHour,
    COUNT(f.EncounterID) AS TotalArrivals,
    ROUND(AVG(CAST(f.WaitTimeMinutes AS FLOAT)), 1) AS AvgWaitTimeMinutes,
    ROUND(CAST(SUM(CASE WHEN f.IsLWBS = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(f.EncounterID) * 100, 2) AS LWBSRatePct
FROM dbo.Fact_ED_Encounters f
JOIN dbo.Dim_Date d ON f.ArrivalDateKey = d.DateKey
GROUP BY 
    d.DayOfWeekNum, d.DayOfWeekName, f.ArrivalHour;
GO

-- 3. Inpatient Capacity, Occupancy & 30-Day Readmission View
CREATE OR ALTER VIEW dbo.vw_Inpatient_Capacity_Metrics AS
SELECT 
    dept.DepartmentID,
    dept.DepartmentName,
    dept.DepartmentType,
    dept.BedCapacity,
    dept.FloorNumber,
    COUNT(s.StayID) AS TotalAdmissions,
    ROUND(AVG(s.InpatientLOSDays), 2) AS AvgInpatientLOSDays,
    SUM(CASE WHEN s.Is30DayReadmission = 1 THEN 1 ELSE 0 END) AS Total30DayReadmissions,
    ROUND(CAST(SUM(CASE WHEN s.Is30DayReadmission = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(s.StayID) * 100, 2) AS ReadmissionRatePct,
    SUM(s.TotalInpatientCostUSD) AS TotalWardRevenueUSD,
    ROUND(AVG(s.TotalInpatientCostUSD), 2) AS AvgCostPerStayUSD
FROM dbo.Fact_Inpatient_Stays s
JOIN dbo.Dim_Departments dept ON s.DepartmentID = dept.DepartmentID
GROUP BY 
    dept.DepartmentID, dept.DepartmentName, dept.DepartmentType, dept.BedCapacity, dept.FloorNumber;
GO

-- 4. Stored Procedure: Physician Productivity & Clinical Triage Evaluation
CREATE OR ALTER PROCEDURE dbo.usp_Get_Physician_Performance_Summary
    @StartDate DATE = '2024-01-01',
    @EndDate DATE = '2024-12-31'
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        p.PhysicianID,
        p.PhysicianName,
        p.Specialty,
        p.PrimaryShift,
        COUNT(f.EncounterID) AS TotalPatientsTreated,
        ROUND(AVG(CAST(f.WaitTimeMinutes AS FLOAT)), 1) AS AvgDoorToDoctorMins,
        ROUND(AVG(CAST(f.EDLOSMinutes AS FLOAT)), 1) AS AvgEDLengthOfStayMins,
        SUM(CASE WHEN f.IsAdmitted = 1 THEN 1 ELSE 0 END) AS PatientsAdmitted,
        ROUND(CAST(SUM(CASE WHEN f.IsAdmitted = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(f.EncounterID) * 100, 1) AS AdmissionPct
    FROM dbo.Fact_ED_Encounters f
    JOIN dbo.Dim_Physicians p ON f.PhysicianID = p.PhysicianID
    JOIN dbo.Dim_Date d ON f.ArrivalDateKey = d.DateKey
    WHERE d.FullDate BETWEEN @StartDate AND @EndDate
      AND f.IsLWBS = 0 -- Exclude LWBS since physician was never assigned
    GROUP BY 
        p.PhysicianID, p.PhysicianName, p.Specialty, p.PrimaryShift
    ORDER BY 
        TotalPatientsTreated DESC;
END;
GO

PRINT 'VitalFlow Analytical Views & Stored Procedures Created Successfully!';
GO
