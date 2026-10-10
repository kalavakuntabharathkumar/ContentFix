from pathlib import Path
from bs4 import BeautifulSoup
import re

def audit_html(path: Path, site_root: Path) -> list[dict]:
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    issues = []
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    if not title:
        issues.append(("missing_title", "Page title is missing"))
    desc = soup.find("meta", attrs={"name": "description"})
    if not desc or not desc.get("content", "").strip():
        issues.append(("missing_description", "Meta description is missing"))
    for img in soup.find_all("img"):
        if not img.get("alt", "").strip():
            issues.append(("missing_alt", f"Image is missing alt text: {img.get('src', 'unknown')}"))
    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        target = (path.parent / href.split("#")[0]).resolve()
        try:
            target.relative_to(site_root.resolve())
        except ValueError:
            issues.append(("unsafe_link", f"Link escapes site root: {href}"))
            continue
        if href and not target.exists():
            issues.append(("broken_link", f"Local target not found: {href}"))
    if re.search(r"\s{3,}", soup.get_text(" ", strip=True)):
        issues.append(("formatting", "Excessive whitespace in page text"))
    return [{"page": path.name, "issue_type": kind, "detail": detail} for kind, detail in issues]
