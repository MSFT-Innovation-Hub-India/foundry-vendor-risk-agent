/* TPRM seed data. Run AFTER schema.sql. */
SET NOCOUNT ON;

/* Vendors */
INSERT INTO dbo.Vendors (VendorId, VendorName, Industry, Country, Criticality, OnboardingStatus, FirstEngagedDate) VALUES
(1001, N'Contoso Cloud', N'SaaS', N'India', N'Medium', N'Active', N'2025-04-03'),
(1002, N'Fabrikam Payments', N'SaaS', N'United States', N'Low', N'Active', N'2025-03-15'),
(1003, N'Acme Analytics', N'Analytics', N'United States', N'High', N'Prospective', N'2026-08-14'),
(1004, N'Globex HR', N'Managed IT', N'Canada', N'Medium', N'Active', N'2025-08-12'),
(1005, N'Initech Managed IT', N'Logistics', N'Australia', N'Medium', N'Active', N'2025-12-27'),
(1006, N'Umbrella Marketing', N'Marketing', N'Australia', N'Low', N'Prospective', N'2023-07-02'),
(1007, N'Northwind Logistics', N'Logistics', N'Germany', N'Medium', N'Prospective', N'2026-09-02'),
(1008, N'Soylent SaaS', N'Logistics', N'India', N'Low', N'Active', N'2025-03-25'),
(1009, N'Stark Hosting', N'Marketing', N'Ireland', N'High', N'Prospective', N'2025-08-05'),
(1010, N'Wayne Data', N'Logistics', N'United Kingdom', N'Medium', N'Prospective', N'2024-12-29'),
(1011, N'Wonka Logistics', N'SaaS', N'Australia', N'Medium', N'Prospective', N'2025-01-02'),
(1012, N'Cyberdyne Analytics', N'Managed IT', N'Ireland', N'High', N'Prospective', N'2025-09-15'),
(1013, N'Hooli Infrastructure', N'Analytics', N'Canada', N'Medium', N'Prospective', N'2025-04-11'),
(1014, N'Vehement Email', N'Cloud Infrastructure', N'United Kingdom', N'High', N'Active', N'2024-02-21'),
(1015, N'Massive Dynamic CRM', N'Marketing', N'Canada', N'Low', N'Active', N'2023-07-01');

/* Contracts */
INSERT INTO dbo.Contracts (ContractId, VendorId, AnnualValueUSD, StartDate, EndDate, Status, ServiceDescription) VALUES
(5001, 1001, 240000.00, N'2026-04-24', N'2027-04-24', N'Active', N'Data enrichment'),
(5002, 1002, 45000.00, N'2024-09-23', N'2025-09-23', N'Active', N'Web analytics'),
(5003, 1003, 480000.00, N'2024-08-13', N'2025-08-13', N'Pending', N'Payroll processing'),
(5004, 1004, 360000.00, N'2026-06-16', N'2027-06-16', N'Active', N'Web analytics'),
(5005, 1005, 360000.00, N'2025-01-17', N'2026-01-17', N'Active', N'Freight & logistics'),
(5006, 1006, 80000.00, N'2025-09-15', N'2026-09-15', N'Active', N'Payroll processing'),
(5007, 1007, 120000.00, N'2024-07-27', N'2025-07-27', N'Pending', N'Cloud hosting'),
(5008, 1008, 360000.00, N'2025-11-05', N'2026-11-05', N'Active', N'Data enrichment'),
(5009, 1009, 45000.00, N'2026-06-10', N'2027-06-10', N'Active', N'CRM platform'),
(5010, 1010, 150000.00, N'2026-01-30', N'2027-01-30', N'Active', N'Cloud hosting'),
(5011, 1011, 80000.00, N'2025-03-01', N'2026-03-01', N'Active', N'Email delivery'),
(5012, 1012, 45000.00, N'2024-09-13', N'2025-09-13', N'Active', N'Data enrichment'),
(5013, 1013, 45000.00, N'2024-08-15', N'2025-08-15', N'Active', N'Payroll processing'),
(5014, 1014, 80000.00, N'2024-11-26', N'2025-11-26', N'Active', N'Data enrichment'),
(5015, 1015, 360000.00, N'2026-04-16', N'2027-04-16', N'Active', N'Web analytics');

/* DataAccess */
INSERT INTO dbo.DataAccess (VendorId, DataClassificationTier, ProcessesPII, DataResidency, SystemsAccessed) VALUES
(1001, N'Public', 0, N'EU', N'Email delivery; Email delivery'),
(1002, N'Restricted', 1, N'US', N'Freight & logistics; Endpoint management'),
(1003, N'Restricted', 1, N'US', N'Customer data warehouse; production analytics pipeline'),
(1004, N'Internal', 0, N'Global', N'CRM platform; Web analytics'),
(1005, N'Internal', 0, N'Global', N'Email delivery; CRM platform'),
(1006, N'Confidential', 1, N'Global', N'Email delivery; Web analytics'),
(1007, N'Internal', 0, N'EU', N'Shipment tracking API; carrier scheduling portal'),
(1008, N'Confidential', 0, N'US', N'Freight & logistics; Email delivery'),
(1009, N'Restricted', 1, N'EU', N'Web analytics; Email delivery'),
(1010, N'Internal', 0, N'EU', N'CRM platform; Cloud hosting'),
(1011, N'Internal', 0, N'US', N'Freight & logistics; CRM platform'),
(1012, N'Internal', 0, N'UK', N'Payroll processing; Freight & logistics'),
(1013, N'Confidential', 0, N'EU', N'Data enrichment; Email delivery'),
(1014, N'Public', 0, N'US', N'Endpoint management; Endpoint management'),
(1015, N'Restricted', 0, N'UK', N'Email delivery; Web analytics');

/* Incidents */
INSERT INTO dbo.Incidents (IncidentId, VendorId, IncidentDate, Severity, Category, Description, ResolvedDate) VALUES
(7001, 1003, N'2026-03-19', N'High', N'DataBreach', N'Exposed S3 bucket containing customer export files; 14k records accessible for ~2 days.', N'2026-03-27'),
(7002, 1003, N'2025-11-05', N'Medium', N'Compliance', N'Subprocessor added without prior notification, contrary to DPA terms.', N'2025-12-01'),
(7003, 1001, N'2024-12-20', N'High', N'Outage', N'Outage event affecting service availability.', N'2025-01-07'),
(7004, 1001, N'2024-07-21', N'Low', N'Compliance', N'Compliance event affecting service availability.', N'2024-08-03'),
(7005, 1002, N'2024-11-06', N'Medium', N'Other', N'Other event affecting service availability.', N'2024-11-23'),
(7006, 1002, N'2025-05-28', N'Low', N'Outage', N'Outage event affecting service availability.', N'2025-06-05'),
(7007, 1005, N'2026-08-12', N'Low', N'Outage', N'Outage event affecting service availability.', N'2026-08-13'),
(7008, 1008, N'2024-11-25', N'Low', N'Outage', N'Outage event affecting service availability.', N'2024-11-28'),
(7009, 1008, N'2026-08-01', N'Medium', N'Outage', N'Outage event affecting service availability.', N'2026-08-18'),
(7010, 1010, N'2024-10-17', N'High', N'Outage', N'Outage event affecting service availability.', N'2024-11-04'),
(7011, 1012, N'2025-01-26', N'High', N'Outage', N'Outage event affecting service availability.', N'2025-02-11'),
(7012, 1012, N'2024-05-29', N'High', N'Outage', N'Outage event affecting service availability.', N'2024-06-02'),
(7013, 1014, N'2025-06-18', N'Medium', N'Other', N'Other event affecting service availability.', N'2025-07-02'),
(7014, 1014, N'2025-05-12', N'Low', N'Outage', N'Outage event affecting service availability.', N'2025-05-14'),
(7015, 1015, N'2024-08-18', N'Medium', N'Outage', N'Outage event affecting service availability.', N'2024-08-26');

/* SLABreaches */
INSERT INTO dbo.SLABreaches (BreachId, VendorId, BreachDate, SLAType, TargetValue, ActualValue, PenaltyAppliedUSD) VALUES
(8001, 1003, N'2026-04-02', N'Availability', N'99.9%', N'99.2%', 5000.00),
(8002, 1003, N'2026-06-11', N'ResolutionTime', N'4h', N'19h', 2500.00),
(8003, 1004, N'2025-05-31', N'Availability', N'99.9%', N'99.5%', 2500.00),
(8004, 1004, N'2026-02-27', N'ResponseTime', N'99.9%', N'99.5%', 2500.00),
(8005, 1008, N'2025-02-16', N'Availability', N'99.9%', N'99.5%', 0.00),
(8006, 1009, N'2025-02-26', N'Availability', N'99.9%', N'99.5%', 0.00),
(8007, 1009, N'2026-01-03', N'Availability', N'99.9%', N'99.5%', 2500.00),
(8008, 1010, N'2025-04-28', N'Availability', N'99.9%', N'99.5%', 2500.00),
(8009, 1013, N'2026-08-31', N'ResponseTime', N'99.9%', N'99.5%', 1000.00),
(8010, 1014, N'2025-11-14', N'ResponseTime', N'99.9%', N'99.5%', 2500.00);

/* PriorAssessments */
INSERT INTO dbo.PriorAssessments (AssessmentId, VendorId, AssessmentDate, InherentRisk, ResidualRisk, Recommendation) VALUES
(9001, 1003, N'2025-09-30', N'High', N'High', N'ApproveWithConditions'),
(9002, 1007, N'2025-10-15', N'Medium', N'Low', N'Approve'),
(9003, 1001, N'2024-12-06', N'Low', N'Low', N'Approve'),
(9004, 1004, N'2025-08-14', N'High', N'High', N'Approve'),
(9005, 1005, N'2026-03-05', N'High', N'Low', N'Approve'),
(9006, 1006, N'2025-01-29', N'High', N'Low', N'ApproveWithConditions'),
(9007, 1008, N'2025-12-10', N'High', N'High', N'Approve'),
(9008, 1010, N'2025-06-30', N'High', N'High', N'ApproveWithConditions'),
(9009, 1012, N'2025-11-06', N'High', N'Low', N'ApproveWithConditions'),
(9010, 1013, N'2025-05-20', N'High', N'Medium', N'ApproveWithConditions'),
(9011, 1014, N'2026-04-11', N'Low', N'Medium', N'Approve'),
(9012, 1015, N'2025-07-30', N'Low', N'Medium', N'Approve');

/* Spend */
INSERT INTO dbo.Spend (VendorId, [Year], SpendUSD) VALUES
(1001, 2024, 130935.02),
(1001, 2025, 148470.57),
(1001, 2026, 149705.78),
(1002, 2024, 66056.84),
(1002, 2025, 75934.00),
(1002, 2026, 79146.18),
(1003, 2024, 374320.29),
(1003, 2025, 471498.19),
(1003, 2026, 474681.23),
(1004, 2024, 39559.05),
(1004, 2025, 40488.11),
(1004, 2026, 43425.26),
(1005, 2024, 38616.37),
(1005, 2025, 40603.21),
(1005, 2026, 44398.27),
(1006, 2024, 68439.80),
(1006, 2025, 72649.19),
(1006, 2026, 82596.07),
(1007, 2024, 99945.19),
(1007, 2025, 109663.27),
(1007, 2026, 128167.28),
(1008, 2024, 35497.76),
(1008, 2025, 42061.96),
(1008, 2026, 44368.58),
(1009, 2024, 36655.07),
(1009, 2025, 40469.22),
(1009, 2026, 48481.82),
(1010, 2024, 68641.22),
(1010, 2025, 76015.85),
(1010, 2026, 80447.94),
(1011, 2024, 35591.66),
(1011, 2025, 44899.05),
(1011, 2026, 46792.46),
(1012, 2024, 66972.79),
(1012, 2025, 78752.20),
(1012, 2026, 82058.10),
(1013, 2024, 65985.22),
(1013, 2025, 71084.57),
(1013, 2026, 79792.38),
(1014, 2024, 39367.14),
(1014, 2025, 40900.42),
(1014, 2026, 44209.75),
(1015, 2024, 36751.60),
(1015, 2025, 42803.55),
(1015, 2026, 47867.07);
