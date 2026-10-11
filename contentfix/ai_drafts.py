import json
from bs4 import BeautifulSoup

def draft_metadata(html: str, api_key: str | None = None) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    text = " ".join(soup.get_text(" ", strip=True).split())[:1800]
    if not api_key:
        return {
            "mode": "offline_fallback",
            "meta_description": (text[:150] or "Learn more about this page.") ,
            "alt_text": f"Image illustrating {title or 'the page content'}",
            "review_required": True
        }
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Draft concise accessible web metadata. Return JSON with meta_description and alt_text. Do not invent facts."},
                {"role": "user", "content": f"Page title: {title}\nVisible page text: {text}"}
            ]
        )
        data = json.loads(response.choices[0].message.content)
        return {"mode": "openai", **data, "review_required": True}
    except Exception as exc:
        return {"mode": "error", "message": str(exc), "review_required": True}
