from pathlib import Path
import os
import streamlit as st
import pandas as pd
from contentfix.audit import audit_html
from contentfix.db import connect, sync_issues, fetch_requests, update_status
from contentfix.exports import export_excel

ROOT = Path(__file__).parent
SITE = ROOT / "sample_site"
DB = ROOT / "data" / "contentfix.db"

st.set_page_config(page_title="ContentFix", layout="wide")
st.title("ContentFix")
st.caption("Content audit · remediation tracking · metadata migration")
conn = connect(DB)

if st.button("Run audit on sample site", type="primary"):
    pages = sorted(SITE.glob("*.html"))
    issues = [issue for page in pages for issue in audit_html(page, SITE)]
    sync_issues(conn, issues)
    st.session_state["last_audit"] = issues
    st.success(f"Audited {len(pages)} local HTML pages and found {len(issues)} issue instances.")

rows = fetch_requests(conn)
df = pd.DataFrame(rows, columns=["id", "page", "issue_type", "detail", "status", "created_at"])
c1, c2, c3 = st.columns(3)
c1.metric("Tracked requests", len(df))
c2.metric("Open", int((df.status == "open").sum()) if not df.empty else 0)
c3.metric("Resolved", int((df.status == "resolved").sum()) if not df.empty else 0)

st.subheader("Issue register")
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
    selected = st.number_input("Request ID", min_value=1, step=1)
    status = st.selectbox("New status", ["open", "in_progress", "resolved"])
    if st.button("Update request"):
        update_status(conn, int(selected), status)
        st.rerun()
    st.download_button("Download Excel issue register", export_excel(df), "contentfix_audit.xlsx")
else:
    st.info("Run the audit to populate the issue register.")

st.subheader("GenAI metadata drafts")
st.write("Draft copy for a selected page. Review every suggestion before publishing.")
page_names = sorted(p.name for p in SITE.glob("*.html"))
selected_page = st.selectbox("Page", page_names)
if st.button("Draft metadata"):
    from contentfix.ai_drafts import draft_metadata
    html = (SITE / selected_page).read_text(encoding="utf-8")
    result = draft_metadata(html, os.getenv("OPENAI_API_KEY"))
    st.json(result)
