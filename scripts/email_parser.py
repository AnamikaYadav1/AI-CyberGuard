import os
import hashlib
import email
from email import policy
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def extract_links_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    return links

def parse_eml(file_path):
    """Parse .eml file and return dict with headers, body, links, attachments info."""
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    headers = dict(msg.items())
    # get body (prefer html then plain)
    html = None
    text = None
    attachments = []
    for part in msg.walk():
        ctype = part.get_content_type()
        disp = part.get_content_disposition()
        if ctype == "text/html" and html is None:
            html = part.get_content()
        elif ctype == "text/plain" and text is None:
            text = part.get_content()
        elif disp == "attachment":
            fname = part.get_filename()
            payload = part.get_content()
            # save attachment metadata (not saving file here)
            attachments.append({"filename": fname, "size": len(payload) if payload else 0})

    links = []
    if html:
        links = extract_links_from_html(html)
    elif text:
        # rudimentary url extraction
        links = re.findall(r'(https?://[^\s]+)', text)

    return {
        "headers": headers,
        "text": text or "",
        "html": html or "",
        "links": links,
        "attachments": attachments
    }

def simple_phish_score(parsed):
    """Heuristic score — 0..1. Higher => likely phishing."""
    score = 0.0
    headers = parsed["headers"]
    from_addr = headers.get("From", "")
    # sender domain
    try:
        sender_domain = from_addr.split("@")[-1].strip().lower()
    except:
        sender_domain = ""
    # domain mismatch: if links point elsewhere
    for link in parsed["links"]:
        try:
            net = urlparse(link).netloc.lower()
            if net and sender_domain and sender_domain not in net:
                score += 0.25
        except:
            pass
    # attachments suspicious
    for att in parsed["attachments"]:
        fname = att.get("filename","").lower()
        if fname.endswith((".exe",".scr",".bat",".js",".vbs",".msi")):
            score += 0.35
    # urgent words in subject/body
    subj = headers.get("Subject","").lower()
    if any(w in subj for w in ["urgent","verify","update","password","bank","click"]):
        score += 0.2
    # clamp
    return min(score, 1.0)
