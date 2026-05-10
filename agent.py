import os
import requests
from datetime import date, timedelta
from email.message import EmailMessage
import smtplib

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -------------------------
# CONFIG
# -------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------
# PUBMED QUERY
# -------------------------

QUERY = """
(
  sleep[Title/Abstract]
  OR circadian[Title/Abstract]
  OR "circadian rhythm"[Title/Abstract]
  OR chronotype[Title/Abstract]
  OR melatonin[Title/Abstract]
  OR insomnia[Title/Abstract]
  OR "sleep deprivation"[Title/Abstract]
  OR "REM sleep"[Title/Abstract]
  OR "slow wave sleep"[Title/Abstract]
  OR "shift work"[Title/Abstract]
  OR suprachiasmatic[Title/Abstract]
)
AND
(
  "Nature"[Journal]
  OR "Science"[Journal]
  OR "Cell"[Journal]
  OR "Nature Neuroscience"[Journal]
  OR "Neuron"[Journal]
  OR "PNAS"[Journal]
  OR "Sleep"[Journal]
  OR "Journal of Biological Rhythms"[Journal]
  OR "Sleep Medicine Reviews"[Journal]
)
"""

PUBMED_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# -------------------------
# FUNCTIONS
# -------------------------

def search_pubmed(days_back=3, max_results=25):
    today = date.today()
    start = today - timedelta(days=days_back)

    params = {
        "db": "pubmed",
        "term": QUERY,
        "retmode": "xml",
        "retmax": max_results,
        "datetype": "pdat",
        "mindate": start.strftime("%Y/%m/%d"),
        "maxdate": today.strftime("%Y/%m/%d"),
    }

    r = requests.get(PUBMED_SEARCH, params=params)
    r.raise_for_status()

    return r.text


def fetch_pubmed(pmids_xml):
    return pmids_xml  # simplified (LLM will parse from XML)


def summarize_with_openai(pubmed_xml):
    prompt = f"""
You are a neuroscience research assistant.

Summarize these PubMed results on sleep and circadian rhythm research.

For each paper include:
- Title
- Journal/date
- One-sentence finding
- Why it matters
- Limitations

Be concise and avoid hype.

TEXT:
{pubmed_xml[:20000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content


def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        print(body)
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


def main():
    print("Searching PubMed...")

    xml = search_pubmed()
    print("Found results")

    summary = summarize_with_openai(xml)

    subject = f"Sleep & Circadian Brief — {date.today().isoformat()}"
    send_email(subject, summary)


if __name__ == "__main__":
    main()
