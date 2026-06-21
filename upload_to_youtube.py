#!/usr/bin/env python3
"""
Economics 101 — YouTube Upload Script
Run this on your local machine to download scenes, assemble, and upload both videos.

Requirements:
  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib requests
  brew install ffmpeg   (Mac)  OR  sudo apt install ffmpeg  (Linux/WSL)

Usage:
  python3 upload_to_youtube.py
"""

import os, json, subprocess, requests, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ── Credentials (loaded from credentials.json — keep that file private!) ─────
_cred_path = Path(__file__).parent / "credentials.json"
with open(_cred_path) as _f:
    _creds = json.load(_f)
CLIENT_ID     = _creds["client_id"]
CLIENT_SECRET = _creds["client_secret"]
REFRESH_TOKEN = _creds["refresh_token"]

# ── Scene URLs ────────────────────────────────────────────────────────────────
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3E9CD98A05vyrIMdmQDzXZVh719/"

VIDEO1_SCENES = [
    BASE + "hf_20260620_041123_26d3aa6c-ee67-4a2f-88c3-76a883f0a1b6.mp4",   # Hook
    BASE + "hf_20260620_041124_5e81d7a7-2778-441c-a537-bd0d521fc50c.mp4",   # Dividends
    BASE + "hf_20260620_041125_2266af9d-2e8b-426a-bf29-1df56b57276b.mp4",   # How Much
    BASE + "hf_20260620_041126_d035817a-bb4b-4e9c-9702-5e17c03baab8.mp4",   # ETFs
    BASE + "hf_20260620_041127_feeeda4d-4938-46dc-aabf-ba58b7b97cb7.mp4",   # Blue-Chip
    BASE + "hf_20260620_041128_bde26485-8386-4114-a48d-be7ebd4a90c5.mp4",   # REITs
    BASE + "hf_20260620_041129_40866303-b5bf-4795-bc4d-198a891830fb.mp4",   # Portfolio
    BASE + "hf_20260620_041130_9b48f92a-1dfa-46de-b131-cca115018487.mp4",   # Encouragement
    BASE + "hf_20260620_061213_ee62a735-de45-4f21-9c44-8896627309ac.mp4",   # Risk Disclaimer
    BASE + "hf_20260620_061215_a7272826-0a6e-4735-a238-7f4e87bacd15.mp4",   # CTA Outro
]

VIDEO2_SCENES = [
    BASE + "hf_20260620_042138_3113b297-626b-431a-bfc3-c31b4c1ceec2.mp4",   # Hook
    BASE + "hf_20260620_042209_1726874a-04b4-4003-a61c-7d2b59b23f9a.mp4",   # Mistake 1
    BASE + "hf_20260620_042144_e5abf6fe-936b-4851-900f-a26df194224e.mp4",   # Mistake 2
    BASE + "hf_20260620_042146_b18398f2-948d-44cc-942c-ddd0d69c374d.mp4",   # Mistake 3
    BASE + "hf_20260620_042148_b1c3dac4-7f2a-44cc-81e4-a2bedff2b6f1.mp4",   # Mistake 4
    BASE + "hf_20260620_042150_16ab2ba9-8b9a-4cf2-ae4b-fe835a4eb21b.mp4",   # Mistake 5
    BASE + "hf_20260620_042153_dc3bc08f-16b5-403f-bf97-37a92e5d431d.mp4",   # What To Do
    BASE + "hf_20260620_042212_caffd49c-9f76-485a-babc-9a3405f86602.mp4",   # CTA Outro
]

# ── SEO Metadata ──────────────────────────────────────────────────────────────
VIDEO1_META = {
    "title": "How to Build $1,000 a Month in Dividend Income (Step by Step)",
    "description": """💰 Want your money to pay YOU every month — even in retirement? In this video, I'll show you exactly how to build $1,000 a month in dividend income using a simple, proven strategy anyone can follow.

Whether you're 52 or 68, it is NOT too late to start. Here's what we cover:

✅ What dividends are and how they work
✅ How much you actually need invested (4%, 5%, and 6% yield scenarios)
✅ The 3 best types of investments for dividend income: ETFs, Blue-Chip Stocks, and REITs
✅ A sample portfolio allocation to target $1,000/month
✅ The risks you need to know before you invest

📌 CHAPTERS:
0:00 – Introduction & Hook
0:45 – What Are Dividends?
2:15 – How Much Do You Need Invested?
3:45 – Dividend ETFs (Pillar 1)
4:40 – Blue-Chip Stocks (Pillar 2)
5:20 – REITs (Pillar 3)
6:00 – Sample Portfolio Allocation
7:15 – Risks to Understand
8:00 – Encouragement & Next Steps
9:00 – Call to Action

⚠️ This video is for educational purposes only and is not personalized financial advice. Always consult a qualified financial advisor before making investment decisions.

🔔 Subscribe to Economics 1144 for plain-English financial education every week!
👍 If this helped you, please LIKE this video!

#DividendInvesting #PassiveIncome #RetirementIncome #DividendStocks #PersonalFinance #Economics101 #FinancialFreedom #Investing #REITs #DividendETF""",
    "tags": [],
    "categoryId": "27",  # Education
}

VIDEO2_META = {
    "title": "5 Social Security Mistakes That Could Cost You $100,000",
    "description": """⚠️ Most Americans are leaving over $100,000 on the table when it comes to Social Security — and they don't even know it.

In this video, I'll walk you through the 5 most common Social Security mistakes and exactly how to avoid them so you collect every dollar you've earned.

If you're 55 or older and haven't claimed yet — this could be one of the most important videos you watch this year.

🔴 THE 5 MISTAKES:
❌ Mistake #1 – Claiming Social Security too early (age 62 vs. 70)
❌ Mistake #2 – Not coordinating with your spouse (spousal benefit strategy)
❌ Mistake #3 – Ignoring the earnings test while still working
❌ Mistake #4 – Forgetting that Social Security benefits can be TAXED
❌ Mistake #5 – Never checking your SSA earnings record for errors

📌 CHAPTERS:
0:00 – Introduction & Hook
0:45 – Mistake #1: Claiming Too Early
2:15 – Mistake #2: Not Coordinating with Your Spouse
3:30 – Mistake #3: The Earnings Test
4:45 – Mistake #4: Taxes on Your Benefits
6:00 – Mistake #5: Check Your Earnings Record
7:15 – What to Do Right Now (5-Step Recap)
8:15 – Call to Action

📋 ACTION STEPS:
1. Know your full retirement age before you claim
2. Coordinate Social Security timing with your spouse
3. Understand the earnings test if you're still working
4. Do tax planning before you claim
5. Go to ssa.gov and check your earnings record today

⚠️ This video is for educational purposes only. For personalized advice, consult a Social Security specialist or licensed financial advisor.

🔔 Subscribe to Economics 1144 for clear, plain-English retirement and personal finance content every week!
👍 Hit LIKE if this video helped you!

#SocialSecurity #RetirementPlanning #SocialSecurityMistakes #SocialSecurityBenefits #RetirementIncome #PersonalFinance #Economics101 #WhenToClaimSocialSecurity #SpousalBenefit #SSA""",
    "tags": [],
    "categoryId": "27",
}

# ── Thumbnail URLs ────────────────────────────────────────────────────────────
VIDEO1_THUMBNAIL = "https://d8j0ntlcm91z4.cloudfront.net/user_3E9CD98A05vyrIMdmQDzXZVh719/hf_20260620_044506_43e8a6fe-0f39-47b2-852c-c9ef96b86e7a.png"
VIDEO2_THUMBNAIL = "https://d8j0ntlcm91z4.cloudfront.net/user_3E9CD98A05vyrIMdmQDzXZVh719/hf_20260620_044505_6bfabf61-5fbd-49c0-9ff1-8fc96d84e6df.png"


def download_scenes(scenes, folder):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    paths = []
    for i, url in enumerate(scenes):
        if url.startswith("SCENE_"):
            print(f"  ⚠️  Scene {i+1} URL not yet available — check Higgsfield for job completion")
            return None
        dest = folder / f"scene_{i+1:02d}.mp4"
        if dest.exists() and dest.stat().st_size > 100_000:
            print(f"  ✓ Scene {i+1} already downloaded")
        else:
            print(f"  ↓ Downloading scene {i+1}...")
            r = requests.get(url, stream=True, timeout=60)
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(65536):
                    f.write(chunk)
            print(f"    {dest.stat().st_size // 1024}KB")
        paths.append(str(dest))
    return paths


def concatenate(scene_paths, output_path):
    concat_file = Path(output_path).parent / "concat_list.txt"
    with open(concat_file, "w") as f:
        for p in scene_paths:
            f.write(f"file '{p}'\n")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
           "-c", "copy", output_path]
    print(f"  Running ffmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ffmpeg error:", result.stderr[-500:])
        raise RuntimeError("ffmpeg failed")
    size_mb = Path(output_path).stat().st_size / 1_048_576
    print(f"  ✓ Assembled: {output_path} ({size_mb:.1f} MB)")


def get_youtube_service():
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube"]
    )
    return build("youtube", "v3", credentials=creds)


def upload_video(youtube, video_path, meta):
    print(f"  Uploading: {meta['title']}")
    body = {
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": meta["categoryId"],
        },
        "status": {"privacyStatus": "public"},
    }
    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True, chunksize=5*1024*1024)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    {int(status.progress() * 100)}% uploaded...")
    video_id = response["id"]
    print(f"  ✓ Uploaded! https://youtu.be/{video_id}")
    return video_id


def set_thumbnail(youtube, video_id, thumbnail_url):
    thumb_path = Path(__file__).parent / "thumbnail.jpg"
    r = requests.get(thumbnail_url, timeout=30)
    with open(thumb_path, "wb") as f:
        f.write(r.content)
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumb_path, mimetype="image/jpeg")
    ).execute()
    print(f"  ✓ Thumbnail set")


def main():
    work_dir = Path(__file__).parent
    youtube = get_youtube_service()

    # ── VIDEO 2: Social Security (all 8 scenes ready) ──────────────────────
    print("\n=== VIDEO 2: Social Security Mistakes ===")
    v2_paths = download_scenes(VIDEO2_SCENES, work_dir / "video2_scenes")
    if v2_paths:
        v2_out = str(work_dir / "video2_final.mp4")
        concatenate(v2_paths, v2_out)
        v2_id = upload_video(youtube, v2_out, VIDEO2_META)
        set_thumbnail(youtube, v2_id, VIDEO2_THUMBNAIL)

    # ── VIDEO 1: Dividend Income ───────────────────────────────────────────
    # NOTE: Update SCENE_9_RISK_URL and SCENE_10_CTA_URL in VIDEO1_SCENES above
    # with the completed URLs from Higgsfield jobs:
    #   ee62a735-de45-4f21-9c44-8896627309ac  (Risk Disclaimer)
    #   a7272826-0a6e-4735-a238-7f4e87bacd15  (CTA Outro)
    print("\n=== VIDEO 1: Dividend Income ===")
    v1_paths = download_scenes(VIDEO1_SCENES, work_dir / "video1_scenes")
    if v1_paths:
        v1_out = str(work_dir / "video1_final.mp4")
        concatenate(v1_paths, v1_out)
        v1_id = upload_video(youtube, v1_out, VIDEO1_META)
        set_thumbnail(youtube, v1_id, VIDEO1_THUMBNAIL)

    print("\n✅ All done!")


if __name__ == "__main__":
    main()
