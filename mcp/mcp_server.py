"""
MCP server for the TPRM database (read-only). Implements the six tools in
tool_contract.md and nothing else. SQL touches the dbo.vw* views only; there is
no write surface.

Transport is selected by env:
  MCP_TRANSPORT = "http"  -> streamable-HTTP on MCP_HOST:MCP_PORT at /mcp  (container)
  MCP_TRANSPORT = "stdio" -> stdio (local dev; default)

Env:
  TPRM_SQL_CONNECTION  ODBC connection string for the read-only login (Uid=tprm_ro).
"""
import os
import pyodbc
from mcp.server.fastmcp import FastMCP

CONN = os.environ["TPRM_SQL_CONNECTION"]
ROW_CAP = 500

mcp = FastMCP(
    "tprm-db",
    host=os.environ.get("MCP_HOST", "0.0.0.0"),
    port=int(os.environ.get("MCP_PORT", "8000")),
)


def _rows(sql: str, *params):
    """Run a parameterized SELECT with a statement timeout; return list[dict]."""
    cx = pyodbc.connect(CONN, readonly=True, timeout=15)
    try:
        cx.timeout = 15
        cur = cx.cursor()
        cur.execute(sql, params)
        cols = [c[0] for c in cur.description]
        out = []
        for r in cur.fetchmany(ROW_CAP):
            d = {}
            for k, v in zip(cols, r):
                d[k] = v.isoformat() if hasattr(v, "isoformat") else (float(v) if hasattr(v, "quantize") else v)
            out.append(d)
        return out
    finally:
        cx.close()


@mcp.tool()
def list_vendors(name_like: str) -> list:
    """Resolve a vendor name (substring) to VendorId(s)."""
    return _rows(
        "SELECT TOP 25 VendorId, VendorName, Industry, Country "
        "FROM dbo.vwVendorProfile WHERE VendorName LIKE '%' + ? + '%' ORDER BY VendorName",
        name_like)


@mcp.tool()
def get_vendor_profile(vendor_id: int) -> list:
    """Identity, criticality, data tier, PII flag, residency, current contract."""
    return _rows("SELECT * FROM dbo.vwVendorProfile WHERE VendorId = ?", vendor_id)


@mcp.tool()
def get_incident_history(vendor_id: int, since: str = None) -> list:
    """Security/compliance incidents for a vendor since a date (default 36 months)."""
    if since is None:
        return _rows(
            "SELECT TOP 500 IncidentId, IncidentDate, Severity, Category, Description, ResolvedDate "
            "FROM dbo.vwIncidentHistory WHERE VendorId = ? "
            "AND IncidentDate >= DATEADD(month,-36,CAST(GETDATE() AS date)) ORDER BY IncidentDate DESC",
            vendor_id)
    return _rows(
        "SELECT TOP 500 IncidentId, IncidentDate, Severity, Category, Description, ResolvedDate "
        "FROM dbo.vwIncidentHistory WHERE VendorId = ? AND IncidentDate >= ? ORDER BY IncidentDate DESC",
        vendor_id, since)


@mcp.tool()
def get_sla_breaches(vendor_id: int, window_months: int = 24) -> list:
    """SLA breaches for a vendor within the trailing window (default 24 months)."""
    return _rows(
        "SELECT TOP 500 BreachId, BreachDate, SLAType, TargetValue, ActualValue, PenaltyAppliedUSD "
        "FROM dbo.vwSLABreaches WHERE VendorId = ? "
        "AND BreachDate >= DATEADD(month,-?,CAST(GETDATE() AS date)) ORDER BY BreachDate DESC",
        vendor_id, window_months)


@mcp.tool()
def get_prior_assessments(vendor_id: int) -> list:
    """Previous risk assessments (inherent/residual rating + recommendation)."""
    return _rows(
        "SELECT AssessmentId, AssessmentDate, InherentRisk, ResidualRisk, Recommendation "
        "FROM dbo.vwPriorAssessments WHERE VendorId = ? ORDER BY AssessmentDate DESC",
        vendor_id)


@mcp.tool()
def get_spend_history(vendor_id: int) -> list:
    """Annual spend with the vendor."""
    return _rows(
        "SELECT [Year], SpendUSD FROM dbo.vwSpendHistory WHERE VendorId = ? ORDER BY [Year]",
        vendor_id)


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio").lower()
    if transport == "http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
