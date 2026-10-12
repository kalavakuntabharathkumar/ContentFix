from pathlib import Path
import pandas as pd
from contentfix.db import connect, fetch_requests

root = Path(__file__).resolve().parents[1]
conn = connect(root / "data" / "contentfix.db")
rows = fetch_requests(conn)
df = pd.DataFrame(rows, columns=["id", "page", "issue_type", "detail", "status", "created_at"])
out = root / "exports"
out.mkdir(exist_ok=True)
df.to_csv(out / "contentfix_issues.csv", index=False)
print(f"Exported {len(df)} rows to {out / 'contentfix_issues.csv'}")
