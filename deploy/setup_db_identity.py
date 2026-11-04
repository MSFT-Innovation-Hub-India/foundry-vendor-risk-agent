"""
Grant the Container App's managed identity read-only access to tprmdb, and remove
the earlier password-based login. Run AFTER the Container App (system-assigned MI)
exists. Auth is the caller's Entra admin token (env TPRM_AAD_TOKEN or az CLI).

Env:
  MI_NAME  the Entra principal name of the managed identity = the Container App
           name for a system-assigned identity (e.g. "tprm-mcp").
"""
import json, os, struct, subprocess
import pyodbc

SERVER = os.environ.get("TPRM_SQL_SERVER", "your-sql-server.database.windows.net")
DB = os.environ.get("TPRM_SQL_DB", "tprmdb")
MI_NAME = os.environ["MI_NAME"]
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

if "]" in MI_NAME:
    raise SystemExit("unexpected character in MI_NAME")

with connect(DB) as cx:
    cur = cx.cursor()
    # remove the earlier password-based user, if present
    cur.execute("IF EXISTS (SELECT 1 FROM sys.database_principals WHERE name='tprm_ro') DROP USER tprm_ro;")
    # create the managed-identity user from Entra and grant read-only on the views
    cur.execute(f"IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name=N'{MI_NAME}') "
                f"CREATE USER [{MI_NAME}] FROM EXTERNAL PROVIDER;")
    for v in VIEWS:
        cur.execute(f"GRANT SELECT ON dbo.{v} TO [{MI_NAME}];")
    print(f"managed identity [{MI_NAME}] granted SELECT on {len(VIEWS)} views")

with connect("master") as cx:
    cur = cx.cursor()
    cur.execute("IF EXISTS (SELECT 1 FROM sys.sql_logins WHERE name='tprm_ro') DROP LOGIN tprm_ro;")
    print("dropped password login tprm_ro")
