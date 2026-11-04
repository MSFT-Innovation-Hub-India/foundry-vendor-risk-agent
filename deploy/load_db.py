"""
Load schema + seed into Azure SQL (tprmdb) as the Entra admin, then create the
read-only login the MCP server uses. Auth is the caller's AAD token from az CLI
(no stored admin password). Writes deploy/deploy.env with the MCP connection
string (contains the generated tprm_ro password; keep it out of chat/logs).

Requires the SQL firewall to allow this client IP (see deploy notes).
"""
import json, os, pathlib, re, secrets, string, struct, subprocess
import pyodbc

SERVER = os.environ.get("TPRM_SQL_SERVER", "your-sql-server.database.windows.net")
DB = os.environ.get("TPRM_SQL_DB", "tprmdb")
KIT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = (KIT / "database" / "schema.sql").read_text(encoding="utf-8")
SEED = (KIT / "database" / "seed_data.sql").read_text(encoding="utf-8")
DEPLOY = KIT / "deploy"; DEPLOY.mkdir(exist_ok=True)
VIEWS = ["vwVendorProfile", "vwIncidentHistory", "vwSLABreaches",
         "vwPriorAssessments", "vwSpendHistory"]
SQL_COPT_SS_ACCESS_TOKEN = 1256


def token_struct():
    tok = os.environ.get("TPRM_AAD_TOKEN")
    if not tok:
        tok = json.loads(subprocess.check_output(
            "az account get-access-token --resource https://database.windows.net/ -o json",
            shell=True))["accessToken"]
    b = tok.encode("utf-16-le")
    return struct.pack(f"<I{len(b)}s", len(b), b)


def connect(db):
    cs = (f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{SERVER},1433;"
          f"Database={db};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;")
    return pyodbc.connect(cs, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct()},
                          autocommit=True)


def run_batches(cur, text):
    for batch in re.split(r'(?im)^\s*GO\s*$', text):
        if batch.strip():
            cur.execute(batch)


# 1. schema + seed
with connect(DB) as cx:
    cur = cx.cursor()
    run_batches(cur, SCHEMA)
    cur.execute(SEED)            # seed has no GO -> single batch
    cur.execute("SELECT COUNT(*) FROM dbo.Vendors"); nv = cur.fetchone()[0]
    cur.execute("SELECT DataClassificationTier, ProcessesPII FROM dbo.vwVendorProfile WHERE VendorId=1003")
    acme = cur.fetchone()
    print(f"schema+seed loaded: {nv} vendors; Acme(1003) tier={acme[0]} pii={acme[1]}")

# 2. read-only login. Password must be a literal in DDL; it must meet Azure
# complexity (3 of 4 categories) and must NOT contain the account name ("tprm").
# Symbol set excludes ; = { } ' so it is safe in both the DDL literal and the
# ODBC connection string.
def make_pwd():
    sym = "!#%^*-_+"
    while True:
        chars = [secrets.choice(string.ascii_uppercase), secrets.choice(string.ascii_lowercase),
                 secrets.choice(string.digits), secrets.choice(sym)]
        chars += [secrets.choice(string.ascii_letters + string.digits + sym) for _ in range(22)]
        secrets.SystemRandom().shuffle(chars)
        p = "".join(chars)
        if "tprm" not in p.lower():
            return p
pwd = make_pwd()
with connect("master") as cx:
    cur = cx.cursor()
    cur.execute("IF NOT EXISTS (SELECT 1 FROM sys.sql_logins WHERE name='tprm_ro') "
                f"CREATE LOGIN tprm_ro WITH PASSWORD='{pwd}';")
    cur.execute(f"ALTER LOGIN tprm_ro WITH PASSWORD='{pwd}';")
    print("login tprm_ro ready")

# 3. user + least-privilege grants (views only)
with connect(DB) as cx:
    cur = cx.cursor()
    cur.execute("IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name='tprm_ro') "
                "CREATE USER tprm_ro FOR LOGIN tprm_ro;")
    for v in VIEWS:
        cur.execute(f"GRANT SELECT ON dbo.{v} TO tprm_ro;")
    print(f"granted SELECT on {len(VIEWS)} views to tprm_ro")

# 4. write the MCP connection string (keep this file secret)
conn = (f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{SERVER},1433;Database={DB};"
        f"Uid=tprm_ro;Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
(DEPLOY / "deploy.env").write_text("TPRM_SQL_CONNECTION=" + conn + "\n", encoding="utf-8")
print("wrote deploy/deploy.env (contains tprm_ro password)")
