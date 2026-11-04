/* =====================================================================
   Third-Party Risk Management (TPRM) — Azure SQL schema
   Load order:  1) schema.sql   2) seed_data.sql
   The agent never touches these tables directly. A read-only MCP layer
   exposes a few parameterized tools that query the vw* views below.
   ===================================================================== */

IF OBJECT_ID('dbo.vwSpendHistory','V')     IS NOT NULL DROP VIEW dbo.vwSpendHistory;
IF OBJECT_ID('dbo.vwPriorAssessments','V') IS NOT NULL DROP VIEW dbo.vwPriorAssessments;
IF OBJECT_ID('dbo.vwSLABreaches','V')      IS NOT NULL DROP VIEW dbo.vwSLABreaches;
IF OBJECT_ID('dbo.vwIncidentHistory','V')  IS NOT NULL DROP VIEW dbo.vwIncidentHistory;
IF OBJECT_ID('dbo.vwVendorProfile','V')    IS NOT NULL DROP VIEW dbo.vwVendorProfile;

IF OBJECT_ID('dbo.Spend','U')            IS NOT NULL DROP TABLE dbo.Spend;
IF OBJECT_ID('dbo.PriorAssessments','U') IS NOT NULL DROP TABLE dbo.PriorAssessments;
IF OBJECT_ID('dbo.SLABreaches','U')      IS NOT NULL DROP TABLE dbo.SLABreaches;
IF OBJECT_ID('dbo.Incidents','U')        IS NOT NULL DROP TABLE dbo.Incidents;
IF OBJECT_ID('dbo.DataAccess','U')       IS NOT NULL DROP TABLE dbo.DataAccess;
IF OBJECT_ID('dbo.Contracts','U')        IS NOT NULL DROP TABLE dbo.Contracts;
IF OBJECT_ID('dbo.Vendors','U')          IS NOT NULL DROP TABLE dbo.Vendors;
GO

CREATE TABLE dbo.Vendors (
    VendorId         INT           NOT NULL PRIMARY KEY,
    VendorName       NVARCHAR(200) NOT NULL,
    Industry         NVARCHAR(100) NOT NULL,
    Country          NVARCHAR(100) NOT NULL,
    Criticality      NVARCHAR(10)  NOT NULL,   -- Low | Medium | High
    OnboardingStatus NVARCHAR(30)  NOT NULL,   -- Prospective | Active | Offboarded
    FirstEngagedDate DATE          NOT NULL
);
GO

CREATE TABLE dbo.Contracts (
    ContractId         INT            NOT NULL PRIMARY KEY,
    VendorId           INT            NOT NULL REFERENCES dbo.Vendors(VendorId),
    AnnualValueUSD     DECIMAL(12,2)  NOT NULL,
    StartDate          DATE           NOT NULL,
    EndDate            DATE           NOT NULL,
    Status             NVARCHAR(20)   NOT NULL,  -- Active | Expired | Pending
    ServiceDescription NVARCHAR(300)  NOT NULL
);
GO

CREATE TABLE dbo.DataAccess (
    VendorId               INT          NOT NULL PRIMARY KEY REFERENCES dbo.Vendors(VendorId),
    DataClassificationTier NVARCHAR(20) NOT NULL,  -- Public | Internal | Confidential | Restricted
    ProcessesPII           BIT          NOT NULL,
    DataResidency          NVARCHAR(50) NOT NULL,  -- US | EU | UK | Global
    SystemsAccessed        NVARCHAR(300) NOT NULL
);
GO

CREATE TABLE dbo.Incidents (
    IncidentId   INT           NOT NULL PRIMARY KEY,
    VendorId     INT           NOT NULL REFERENCES dbo.Vendors(VendorId),
    IncidentDate DATE          NOT NULL,
    Severity     NVARCHAR(10)  NOT NULL,   -- Low | Medium | High | Critical
    Category     NVARCHAR(30)  NOT NULL,   -- DataBreach | Outage | Compliance | Other
    Description  NVARCHAR(400) NOT NULL,
    ResolvedDate DATE          NULL
);
GO

CREATE TABLE dbo.SLABreaches (
    BreachId          INT           NOT NULL PRIMARY KEY,
    VendorId          INT           NOT NULL REFERENCES dbo.Vendors(VendorId),
    BreachDate        DATE          NOT NULL,
    SLAType           NVARCHAR(30)  NOT NULL,   -- Availability | ResponseTime | ResolutionTime
    TargetValue       NVARCHAR(30)  NOT NULL,
    ActualValue       NVARCHAR(30)  NOT NULL,
    PenaltyAppliedUSD DECIMAL(10,2) NOT NULL
);
GO

CREATE TABLE dbo.PriorAssessments (
    AssessmentId   INT          NOT NULL PRIMARY KEY,
    VendorId       INT          NOT NULL REFERENCES dbo.Vendors(VendorId),
    AssessmentDate DATE         NOT NULL,
    InherentRisk   NVARCHAR(10) NOT NULL,   -- Low | Medium | High | Critical
    ResidualRisk   NVARCHAR(10) NOT NULL,   -- Low | Medium | High | Critical
    Recommendation NVARCHAR(40) NOT NULL    -- Approve | ApproveWithConditions | Reject
);
GO

CREATE TABLE dbo.Spend (
    VendorId INT           NOT NULL REFERENCES dbo.Vendors(VendorId),
    [Year]   INT           NOT NULL,
    SpendUSD DECIMAL(12,2) NOT NULL,
    CONSTRAINT PK_Spend PRIMARY KEY (VendorId, [Year])
);
GO

CREATE INDEX IX_Incidents_Vendor  ON dbo.Incidents(VendorId, IncidentDate);
CREATE INDEX IX_SLABreaches_Vendor ON dbo.SLABreaches(VendorId, BreachDate);
GO

/* ---------- Read-only views the MCP tools are allowed to query ---------- */

CREATE VIEW dbo.vwVendorProfile AS
SELECT  v.VendorId, v.VendorName, v.Industry, v.Country, v.Criticality,
        v.OnboardingStatus, v.FirstEngagedDate,
        d.DataClassificationTier, d.ProcessesPII, d.DataResidency, d.SystemsAccessed,
        c.ContractId, c.AnnualValueUSD, c.StartDate AS ContractStart,
        c.EndDate AS ContractEnd, c.Status AS ContractStatus, c.ServiceDescription
FROM        dbo.Vendors v
LEFT JOIN   dbo.DataAccess d ON d.VendorId = v.VendorId
OUTER APPLY (SELECT TOP 1 * FROM dbo.Contracts cc
             WHERE cc.VendorId = v.VendorId
             ORDER BY CASE WHEN cc.Status='Active' THEN 0 ELSE 1 END, cc.EndDate DESC) c;
GO

CREATE VIEW dbo.vwIncidentHistory AS
SELECT IncidentId, VendorId, IncidentDate, Severity, Category, Description, ResolvedDate
FROM   dbo.Incidents;
GO

CREATE VIEW dbo.vwSLABreaches AS
SELECT BreachId, VendorId, BreachDate, SLAType, TargetValue, ActualValue, PenaltyAppliedUSD
FROM   dbo.SLABreaches;
GO

CREATE VIEW dbo.vwPriorAssessments AS
SELECT AssessmentId, VendorId, AssessmentDate, InherentRisk, ResidualRisk, Recommendation
FROM   dbo.PriorAssessments;
GO

CREATE VIEW dbo.vwSpendHistory AS
SELECT VendorId, [Year], SpendUSD
FROM   dbo.Spend;
GO
