"""
Deterministic seed generator for the TPRM demo database (stdlib only).

Emits:
  seed_data/vendors.csv, contracts.csv, data_access.csv, incidents.csv,
  sla_breaches.csv, prior_assessments.csv, spend.csv
  seed_data.sql   (batched INSERTs; run AFTER schema.sql)

Two "spotlight" vendors have hand-set facts so they line up with the sample
questionnaires in ../samples:
  V1003  Acme Analytics     -> Restricted data + PII, high value, a prior
                               breach + SLA misses  (questionnaire has gaps)
  V1007  Northwind Logistics-> Internal data, no PII, clean history
                               (questionnaire is clean)
The remaining vendors are generated to give the DB a realistic body so the
list/lookup tools behave like production.
"""
import csv, os, random, datetime as dt

SEED = 42
TODAY = dt.date(2026, 11, 1)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data")
os.makedirs(OUT, exist_ok=True)
random.seed(SEED)

INDUSTRIES = ["SaaS", "Cloud Infrastructure", "Payments", "Logistics",
              "Marketing", "HR Services", "Analytics", "Managed IT"]
COUNTRIES  = ["United States", "United Kingdom", "Germany", "Ireland",
              "Canada", "India", "Australia"]
TIERS      = ["Public", "Internal", "Confidential", "Restricted"]
CRIT       = ["Low", "Medium", "High"]
SERVICES   = ["Cloud hosting", "Email delivery", "Payroll processing",
              "Freight & logistics", "Web analytics", "CRM platform",
              "Endpoint management", "Data enrichment"]

# ---------------------------------------------------------------- vendors
vendors, data_access = [], []
spotlight = {
    1003: dict(name="Acme Analytics", industry="Analytics", country="United States",
               crit="High", status="Prospective", first="2026-08-14",
               tier="Restricted", pii=1, residency="US",
               systems="Customer data warehouse; production analytics pipeline"),
    1007: dict(name="Northwind Logistics", industry="Logistics", country="Germany",
               crit="Medium", status="Prospective", first="2026-09-02",
               tier="Internal", pii=0, residency="EU",
               systems="Shipment tracking API; carrier scheduling portal"),
}

names_pool = ["Contoso Cloud", "Fabrikam Payments", "Globex HR", "Initech Managed IT",
              "Umbrella Marketing", "Soylent SaaS", "Stark Hosting", "Wayne Data",
              "Wonka Logistics", "Cyberdyne Analytics", "Hooli Infrastructure",
              "Vehement Email", "Massive Dynamic CRM"]

all_ids = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010,
           1011, 1012, 1013, 1014, 1015]
np = iter(names_pool)
for vid in all_ids:
    if vid in spotlight:
        s = spotlight[vid]
        vendors.append([vid, s["name"], s["industry"], s["country"], s["crit"],
                        s["status"], s["first"]])
        data_access.append([vid, s["tier"], s["pii"], s["residency"], s["systems"]])
    else:
        name = next(np)
        tier = random.choice(TIERS)
        vendors.append([vid, name, random.choice(INDUSTRIES), random.choice(COUNTRIES),
                        random.choice(CRIT), random.choice(["Active", "Prospective"]),
                        (TODAY - dt.timedelta(days=random.randint(120, 1400))).isoformat()])
        data_access.append([vid, tier, 1 if tier in ("Confidential", "Restricted") and random.random() < 0.7 else 0,
                            random.choice(["US", "EU", "UK", "Global"]),
                            random.choice(SERVICES) + "; " + random.choice(SERVICES)])

# -------------------------------------------------------------- contracts
contracts = []
cid = 5000
value_hint = {1003: 480000, 1007: 120000}
for vid in all_ids:
    cid += 1
    base = value_hint.get(vid, random.choice([45000, 80000, 150000, 240000, 360000]))
    start = TODAY - dt.timedelta(days=random.randint(30, 900))
    contracts.append([cid, vid, f"{base:.2f}", start.isoformat(),
                      (start + dt.timedelta(days=365)).isoformat(),
                      "Active" if vid not in spotlight else "Pending",
                      random.choice(SERVICES)])

# --------------------------------------------------------------- incidents
incidents = []
iid = 7000
# spotlight: Acme has a real breach history; Northwind has none.
iid += 1
incidents.append([iid, 1003, "2026-03-19", "High", "DataBreach",
                  "Exposed S3 bucket containing customer export files; 14k records accessible for ~2 days.",
                  "2026-03-27"])
iid += 1
incidents.append([iid, 1003, "2025-11-05", "Medium", "Compliance",
                  "Subprocessor added without prior notification, contrary to DPA terms.", "2025-12-01"])
for vid in all_ids:
    if vid in (1003, 1007):
        continue
    for _ in range(random.randint(0, 2)):
        iid += 1
        d = TODAY - dt.timedelta(days=random.randint(60, 900))
        sev = random.choice(["Low", "Low", "Medium", "High"])
        cat = random.choice(["Outage", "Outage", "Compliance", "Other"])
        incidents.append([iid, vid, d.isoformat(), sev, cat,
                          f"{cat} event affecting service availability.",
                          (d + dt.timedelta(days=random.randint(1, 20))).isoformat()])

# ------------------------------------------------------------- sla breaches
sla = []
bid = 8000
for (vid, d, t, tgt, act, pen) in [
    (1003, "2026-04-02", "Availability",   "99.9%", "99.2%", 5000.00),
    (1003, "2026-06-11", "ResolutionTime", "4h",    "19h",   2500.00),
]:
    bid += 1
    sla.append([bid, vid, d, t, tgt, act, f"{pen:.2f}"])
for vid in all_ids:
    if vid in (1003, 1007):
        continue
    for _ in range(random.randint(0, 2)):
        bid += 1
        d = TODAY - dt.timedelta(days=random.randint(60, 800))
        sla.append([bid, vid, d.isoformat(), random.choice(["Availability", "ResponseTime", "ResolutionTime"]),
                    "99.9%", "99.5%", f"{random.choice([0, 500, 1000, 2500]):.2f}"])

# -------------------------------------------------------- prior assessments
prior = []
aid = 9000
aid += 1
prior.append([aid, 1003, "2025-09-30", "High", "High", "ApproveWithConditions"])
aid += 1
prior.append([aid, 1007, "2025-10-15", "Medium", "Low", "Approve"])
for vid in all_ids:
    if vid in (1003, 1007):
        continue
    if random.random() < 0.6:
        aid += 1
        ir = random.choice(["Low", "Medium", "High"])
        prior.append([aid, vid, (TODAY - dt.timedelta(days=random.randint(200, 700))).isoformat(),
                      ir, random.choice(["Low", "Medium", "High"]),
                      random.choice(["Approve", "ApproveWithConditions"])])

# ------------------------------------------------------------------- spend
spend = []
for vid in all_ids:
    base = value_hint.get(vid, random.choice([45000, 80000, 150000, 240000, 360000]))
    for yr in (2024, 2025, 2026):
        factor = {2024: 0.82, 2025: 0.93, 2026: 1.0}[yr] * random.uniform(0.95, 1.08)
        spend.append([vid, yr, f"{base * factor:.2f}"])

# ------------------------------------------------------------------- write CSVs
def dump(fn, header, rows):
    with open(os.path.join(OUT, fn), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

dump("vendors.csv", ["VendorId", "VendorName", "Industry", "Country", "Criticality", "OnboardingStatus", "FirstEngagedDate"], vendors)
dump("contracts.csv", ["ContractId", "VendorId", "AnnualValueUSD", "StartDate", "EndDate", "Status", "ServiceDescription"], contracts)
dump("data_access.csv", ["VendorId", "DataClassificationTier", "ProcessesPII", "DataResidency", "SystemsAccessed"], data_access)
dump("incidents.csv", ["IncidentId", "VendorId", "IncidentDate", "Severity", "Category", "Description", "ResolvedDate"], incidents)
dump("sla_breaches.csv", ["BreachId", "VendorId", "BreachDate", "SLAType", "TargetValue", "ActualValue", "PenaltyAppliedUSD"], sla)
dump("prior_assessments.csv", ["AssessmentId", "VendorId", "AssessmentDate", "InherentRisk", "ResidualRisk", "Recommendation"], prior)
dump("spend.csv", ["VendorId", "Year", "SpendUSD"], spend)

# ------------------------------------------------------------------- write SQL
def q(v):
    if v is None or v == "":
        return "NULL"
    s = str(v)
    # numeric?
    try:
        float(s)
        if s.replace(".", "", 1).lstrip("-").isdigit():
            return s
    except ValueError:
        pass
    return "N'" + s.replace("'", "''") + "'"

def insert_block(table, cols, rows, f):
    if not rows:
        return
    f.write(f"\n/* {table} */\n")
    for i in range(0, len(rows), 100):
        chunk = rows[i:i + 100]
        f.write(f"INSERT INTO dbo.{table} ({', '.join(cols)}) VALUES\n")
        f.write(",\n".join("(" + ", ".join(q(c) for c in r) + ")" for r in chunk))
        f.write(";\n")

sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data.sql")
with open(sql_path, "w", encoding="utf-8") as f:
    f.write("/* TPRM seed data. Run AFTER schema.sql. */\nSET NOCOUNT ON;\n")
    insert_block("Vendors", ["VendorId", "VendorName", "Industry", "Country", "Criticality", "OnboardingStatus", "FirstEngagedDate"], vendors, f)
    insert_block("Contracts", ["ContractId", "VendorId", "AnnualValueUSD", "StartDate", "EndDate", "Status", "ServiceDescription"], contracts, f)
    insert_block("DataAccess", ["VendorId", "DataClassificationTier", "ProcessesPII", "DataResidency", "SystemsAccessed"], data_access, f)
    insert_block("Incidents", ["IncidentId", "VendorId", "IncidentDate", "Severity", "Category", "Description", "ResolvedDate"], incidents, f)
    insert_block("SLABreaches", ["BreachId", "VendorId", "BreachDate", "SLAType", "TargetValue", "ActualValue", "PenaltyAppliedUSD"], sla, f)
    insert_block("PriorAssessments", ["AssessmentId", "VendorId", "AssessmentDate", "InherentRisk", "ResidualRisk", "Recommendation"], prior, f)
    insert_block("Spend", ["VendorId", "[Year]", "SpendUSD"], spend, f)

print(f"vendors={len(vendors)} contracts={len(contracts)} incidents={len(incidents)} "
      f"sla={len(sla)} prior={len(prior)} spend={len(spend)}")
print("wrote", sql_path)
