#!/usr/bin/env python3
"""
Economics 1144: upload the "Pay the Tax Now" Short to YouTube.
Run this on your local machine (it uses the same credentials.json as upload_to_youtube.py).

Requirements:
  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

Usage (from the repo root):
  python3 short/upload_short.py              # public
  python3 short/upload_short.py --private    # private, to check it in YouTube Studio first
"""

import json, sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parent.parent
VIDEO = Path(__file__).resolve().parent / "renders" / "pay-the-tax-now.mp4"

# ── Credentials (credentials.json in the repo root — keep that file private!) ──
with open(ROOT / "credentials.json") as _f:
    _creds = json.load(_f)

SHORT_META = {
    "title": "Roth vs Traditional IRA: Pay the Tax Now? #Shorts",
    "description": """Same savings, two accounts, but only one gets taxed later. 🤔

A Traditional IRA gives you the tax break now, then taxes every withdrawal as income. A Roth IRA is taxed going in, so qualified withdrawals after 59½ are tax-free.

✅ 2026 IRA limit: $7,500 a year (about $625 a month)
✅ Age 50 or older: $8,600

📺 Watch the full breakdown, Roth IRA vs Traditional IRA, on the Economics 1144 channel.

⚠️ This video is for educational purposes only. Consult a fee-only financial advisor or CPA for personalized advice based on your situation.

🔔 Subscribe to Economics 1144 for plain-English financial education every week!

#Shorts #RothIRA #TraditionalIRA #RetirementPlanning #PersonalFinance #Economics1144""",
    "tags": ["Roth IRA", "Traditional IRA", "IRA contribution limit 2026", "retirement planning",
             "personal finance", "Economics 1144", "Shorts"],
    "categoryId": "27",  # Education
}


def main():
    privacy = "private" if "--private" in sys.argv else "public"
    if not VIDEO.exists():
        sys.exit(f"Missing {VIDEO}. Pull the branch, or render it with: cd short && npm run render")

    youtube = build("youtube", "v3", credentials=Credentials(
        token=None,
        refresh_token=_creds["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=_creds["client_id"],
        client_secret=_creds["client_secret"],
        scopes=["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube"],
    ))

    print(f"  Uploading ({privacy}): {SHORT_META['title']}")
    body = {
        "snippet": {k: SHORT_META[k] for k in ("title", "description", "tags", "categoryId")},
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(str(VIDEO), mimetype="video/mp4", resumable=True, chunksize=5*1024*1024)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    {int(status.progress() * 100)}% uploaded...")
    print(f"  ✓ Uploaded! https://youtube.com/shorts/{response['id']}")


if __name__ == "__main__":
    main()
