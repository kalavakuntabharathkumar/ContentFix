from io import BytesIO
import pandas as pd

def export_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Issue Register")
        summary = (df.groupby(["issue_type", "status"]).size()
                   .reset_index(name="count"))
        summary.to_excel(writer, index=False, sheet_name="Summary")
    return output.getvalue()
