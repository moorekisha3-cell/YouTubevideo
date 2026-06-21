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

# ── Audio URLs (Tasha ElevenLabs voice) ──────────────────────────────────────
VIDEO1_AUDIO = [
    BASE + "hf_20260621_044059_8b9c7064-8b21-4946-9832-55aa16fa1cc3.mp3",  # Hook
    BASE + "hf_20260621_044105_0f4f6916-e024-47f0-bb97-9e7e0d16a58f.mp3",  # What Are Dividends
    BASE + "hf_20260621_044110_b221940d-8e9b-4d0d-8b99-3cd9149a4c01.mp3",  # How Much Do You Need
    BASE + "hf_20260621_044117_d6751f2c-e0ee-45ea-ab63-c04ec07abad5.mp3",  # Dividend ETFs
    BASE + "hf_20260621_044119_79872945-f410-4e3e-bdc4-9acc5b2979b5.mp3",  # Blue-Chip Stocks
    BASE + "hf_20260621_044123_aa05981c-4792-4d79-b45e-461787a3c266.mp3",  # REITs
    BASE + "hf_20260621_044130_fa025da4-636f-4c7a-b039-b9597e78aa8e.mp3",  # Sample Portfolio
    BASE + "hf_20260621_044133_102e329f-e332-467b-b323-8d8c432dddec.mp3",  # Risk Disclaimer
    BASE + "hf_20260621_044137_3f25b5f4-f065-47f2-8f46-29d86f251935.mp3",  # Encouragement
    BASE + "hf_20260621_044139_2694b2dd-f0cd-44e1-974c-7a991be6bb56.mp3",  # CTA Outro
]

VIDEO2_AUDIO = [
    BASE + "hf_20260621_044142_fd858ccc-975f-471f-8e64-6e3367039361.mp3",  # Hook
    BASE + "hf_20260621_044146_675ebead-7dd8-485e-9732-f7da1cb4738a.mp3",  # Mistake 1
    BASE + "hf_20260621_044149_5f4e4422-ecb6-44a5-8953-866f250d338f.mp3",  # Mistake 2
    BASE + "hf_20260621_044154_d7a7ff3c-5c96-459d-a575-bd67e67cbf00.mp3",  # Mistake 3
    BASE + "hf_20260621_044156_7be3e704-5684-4326-acb4-e7c69b68b476.mp3",  # Mistake 4
    BASE + "hf_20260621_044159_ae5878ab-88e3-49cc-88df-f8de2c369faa.mp3",  # Mistake 5
    BASE + "hf_20260621_044202_81dfb692-05a9-41fd-90ae-e4b46f1fe643.mp3",  # What To Do
    BASE + "hf_20260621_044205_ec0853f6-d336-4c67-b5e8-d9d4ceb81111.mp3",  # Outro CTA
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

# ── Video 3: The 4% Rule ──────────────────────────────────────────────────────
VIDEO3_SCENES = [
    BASE + "hf_20260621_050238_b189e5e6-6d4f-4958-9e41-e77ef34e5f7e.mp4",   # Hook
    BASE + "hf_20260621_050240_efca38a5-5eb0-4227-ac51-4967be4319c3.mp4",   # What Is 4% Rule
    BASE + "hf_20260621_050241_5848aae0-745f-4607-8b3d-e5b6d09e9483.mp4",   # Trinity Study
    BASE + "hf_20260621_050242_ec3d52b4-9a4f-47e2-bb72-472660175b8b.mp4",   # Calculate Your Number
    BASE + "hf_20260621_050244_31a40a0e-8bc6-4834-8572-2da5f51d1536.mp4",   # Does It Still Work
    BASE + "hf_20260621_050245_cb6d7770-b253-43cb-a216-e3568e14d48e.mp4",   # Sequence of Returns
    BASE + "hf_20260621_050247_16abdabf-0d52-47b0-b359-100b7f0f0773.mp4",   # Adjusting Withdrawals
    BASE + "hf_20260621_050248_b80816ff-a674-47a4-8549-397888737003.mp4",   # CTA
]

VIDEO3_AUDIO = [
    BASE + "hf_20260621_050303_b7bbd606-2fe4-455d-86d7-ef32aa20464e.mp3",   # Hook
    BASE + "hf_20260621_050308_15933828-2655-4703-a7fb-e73fd4e9f0a1.mp3",   # What Is 4% Rule
    BASE + "hf_20260621_050311_b36be98a-f0eb-4323-aec0-88a31950d994.mp3",   # Trinity Study
    BASE + "hf_20260621_050317_780e942f-d972-4c0a-9d62-b8bda5a3c788.mp3",   # Calculate Your Number
    BASE + "hf_20260621_050322_d6359e0b-ae91-4dfd-b196-4f034475a892.mp3",   # Does It Still Work
    BASE + "hf_20260621_050327_c3efbe77-cc9f-491f-a229-f13adbcd90e1.mp3",   # Sequence of Returns
    BASE + "hf_20260621_050331_92b5ae8b-b311-40ea-a431-3ee277b62cd9.mp3",   # Adjusting Withdrawals
    BASE + "hf_20260621_050336_e808cf1f-f385-48db-858e-27d48a4baea0.mp3",   # CTA
]

VIDEO3_META = {
    "title": "How to Never Run Out of Money in Retirement — The 4% Rule Explained",
    "description": """💡 What if there was a simple rule — backed by decades of research — that tells you exactly how much you can safely spend in retirement without ever running out of money?

It's called the 4% Rule. And in this video, I break it down in plain English so you can plan your retirement with confidence.

✅ What the 4% Rule is and where it comes from (the Trinity Study)
✅ How to calculate YOUR retirement savings target using the 25x Rule
✅ Does the 4% Rule still work in today's market?
✅ The hidden danger: Sequence of Returns Risk
✅ How to stay flexible with dynamic withdrawals

📌 CHAPTERS:
0:00 – Introduction & Hook
0:50 – What Is the 4% Rule?
2:00 – Where It Comes From (Trinity Study)
3:15 – How to Calculate Your Number (25x Rule)
4:30 – Does It Still Work Today?
5:45 – Sequence of Returns Risk
6:45 – Adjusting Your Withdrawal Rate
7:45 – Encouragement & Call to Action

⚠️ This video is for educational purposes only and is not personalized financial advice. Always consult a qualified financial advisor before making retirement decisions.

🔔 Subscribe to Economics 1144 for plain-English financial education every week!
👍 If this helped you, please LIKE this video!

#RetirementPlanning #4PercentRule #RetirementIncome #PersonalFinance #HowMuchToRetire #FinancialFreedom #TrinityStudy #RetirementSavings #Economics1144""",
    "tags": [],
    "categoryId": "27",
}

VIDEO3_THUMBNAIL = BASE + "hf_20260621_050424_f6069307-e868-4ce5-9524-3bb4bcbc0475.png"

# ── Video 4: Roth IRA vs Traditional IRA ─────────────────────────────────────
VIDEO4_SCENES = [
    BASE + "hf_20260621_051706_911f52cd-2be9-4385-8dac-82802781bec0.mp4",   # Hook
    BASE + "hf_20260621_051340_fdfff17b-9a49-410f-a137-7b763e6a7f33.mp4",   # Traditional IRA
    BASE + "hf_20260621_051343_e1a3dec4-7cee-4358-8415-647a9a36bb4d.mp4",   # Roth IRA
    BASE + "hf_20260621_051344_e5ebe1a4-7369-4ef8-aebd-b30585de92ac.mp4",   # Income Limits
    BASE + "hf_20260621_051707_36d1fc86-df60-4288-87ce-c6e0638f1502.mp4",   # Tax Now or Later
    BASE + "hf_20260621_051346_19935e08-e42f-46e2-9dd7-8ef72efbabca.mp4",   # Withdrawal Rules
    BASE + "hf_20260621_051709_f6cf09d4-69ac-44bf-b24a-ae40c81137fb.mp4",   # Which One
    BASE + "hf_20260621_051710_7a9bca0e-a040-4354-9cc7-973ce0418d77.mp4",   # CTA
]

VIDEO4_AUDIO = [
    BASE + "hf_20260621_050340_2697a8e7-f34c-4916-be30-c7279ffc5c12.mp3",   # Hook
    BASE + "hf_20260621_050345_ca7178d9-f279-4fff-bfec-96dcfca287da.mp3",   # Traditional IRA
    BASE + "hf_20260621_050349_8a15ec11-90a1-476f-b1f3-5e1f9aecaa00.mp3",   # Roth IRA
    BASE + "hf_20260621_050354_0c032e9f-2db7-4470-aa52-c33e212c9c3e.mp3",   # Income Limits
    BASE + "hf_20260621_050400_306e9f8d-e490-44b6-9c27-478b262b13a4.mp3",   # Tax Now or Later
    BASE + "hf_20260621_050404_859b943c-c19b-4668-811a-31e9286bb90a.mp3",   # Withdrawal Rules
    BASE + "hf_20260621_050409_e77ba58b-9f4a-44ed-8044-544c956feced.mp3",   # Which One
    BASE + "hf_20260621_050413_e5d3dd69-f4fa-43f8-8c7c-a6bcc2bceab0.mp3",   # CTA
]

VIDEO4_META = {
    "title": "Roth IRA vs Traditional IRA — Which One Is Right for You?",
    "description": """🤔 Roth IRA or Traditional IRA — which should you choose? Getting this wrong could cost you tens of thousands of dollars in taxes over your lifetime. But once you understand the key difference, the answer becomes crystal clear.

In this video, I break down both accounts in plain English so you can make a confident, informed decision.

✅ How the Traditional IRA works (tax deduction now, taxes later)
✅ How the Roth IRA works (pay taxes now, tax-FREE withdrawals forever)
✅ 2024 income limits and eligibility rules
✅ The key question: tax now or tax later?
✅ Withdrawal rules, flexibility, and Required Minimum Distributions
✅ A simple framework to decide which one is right for YOU

📌 CHAPTERS:
0:00 – Introduction & Hook
0:50 – What Is a Traditional IRA?
2:15 – What Is a Roth IRA?
3:30 – Income Limits & Eligibility
4:30 – The Key Question: Tax Now or Later?
5:45 – Withdrawal Rules & Flexibility
6:45 – Which One Is Right for You?
7:45 – Encouragement & Call to Action

⚠️ This video is for educational purposes only. Consult a fee-only financial advisor or CPA for personalized advice based on your situation.

🔔 Subscribe to Economics 1144 for plain-English financial education every week!
👍 If this helped you, please LIKE this video!

#RothIRA #TraditionalIRA #IRA #RetirementPlanning #PersonalFinance #TaxStrategy #RetirementSavings #Economics1144 #RothVsTraditional""",
    "tags": [],
    "categoryId": "27",
}

VIDEO4_THUMBNAIL = BASE + "hf_20260621_050425_3a47fa14-f4ed-481a-975c-f0ebba77ba87.png"

# ── Video 5: The Ladybird Deed ────────────────────────────────────────────────
VIDEO5_SCENES = [
    BASE + "hf_20260621_054512_834a39c3-813c-4af1-a718-28e8e9d4c2c4.mp4",   # Hook
    BASE + "hf_20260621_054514_80bcbe8e-363e-44d9-ae02-a61524d0c653.mp4",   # What Is a Ladybird Deed
    BASE + "hf_20260621_054515_7a08ee37-df98-4e4c-a8d0-03b3537e9a88.mp4",   # How It Works
    BASE + "hf_20260621_054517_a950996a-e666-4784-a42d-520e6fd30f2c.mp4",   # Medicaid Advantage
    BASE + "hf_20260621_054518_a32196a0-e330-44ac-8e9f-143b73e63d64.mp4",   # Tax Benefits
    BASE + "hf_20260621_054520_40f1ddd3-a853-4ddf-91ac-95b687af32f1.mp4",   # Which States
    BASE + "hf_20260621_054521_88f8bb32-3d12-4231-9de2-ff5f74289ef6.mp4",   # What to Watch Out For
    BASE + "hf_20260621_054522_cfc8bbfe-bdbb-4c84-a30d-95ee5c5d1449.mp4",   # CTA
]

VIDEO5_AUDIO = [
    BASE + "hf_20260621_054531_907ac342-1003-4aeb-aae9-25ad72089f4e.mp3",   # Hook
    BASE + "hf_20260621_054536_dd5b0170-3f9a-4446-9774-eef920d565b2.mp3",   # What Is a Ladybird Deed
    BASE + "hf_20260621_054541_fc479576-55eb-42a0-a96e-682ed412c555.mp3",   # How It Works
    BASE + "hf_20260621_054546_78884f1f-dd73-4ad3-8bc9-49e9497b8afc.mp3",   # Medicaid Advantage
    BASE + "hf_20260621_054551_7586e9e0-4bbc-4a4c-8f72-c4db41fc7e64.mp3",   # Tax Benefits
    BASE + "hf_20260621_054555_1ba96ebf-5218-4732-86da-9365533f0cba.mp3",   # Which States
    BASE + "hf_20260621_054600_15a5f194-cc58-469e-a1ba-5fa08b2bacb6.mp3",   # What to Watch Out For
    BASE + "hf_20260621_054604_bccf5d83-bbe3-482e-a5e9-cb56c79df954.mp3",   # CTA
]

VIDEO5_META = {
    "title": "The Ladybird Deed — The Smartest Way to Pass Your Home to Your Family",
    "description": """🏡 What if you could pass your home directly to your children — without a will, without probate, and without losing your Medicaid benefits? It's called the Ladybird Deed, and it's one of the most powerful estate planning tools most people have never heard of.

In this video I break down everything you need to know in plain English:

✅ What a Ladybird Deed (Enhanced Life Estate Deed) actually is
✅ How it works step by step — and why it beats a regular will
✅ How it protects your home from Medicaid Estate Recovery
✅ The stepped-up tax basis benefit that saves your heirs thousands
✅ Which 5 states recognize it: FL, MI, TX, VT, WV
✅ The 4 things to watch out for before you sign one

📌 CHAPTERS:
0:00 – Introduction & Hook
0:50 – What Is a Ladybird Deed?
2:15 – How It Works (Step by Step)
3:30 – The Medicaid Advantage
4:45 – Tax Benefits (Stepped-Up Basis)
5:45 – Which States Allow It?
6:45 – What to Watch Out For
7:45 – Encouragement & Call to Action

⚠️ This video is for educational purposes only and is not personalized legal or financial advice. Always consult a licensed estate planning attorney in your state.

🔔 Subscribe to Economics 1144 for plain-English financial and legal education every week!
👍 If this helped you, please LIKE this video!

#LadybirdDeed #EstatePlanning #Probate #Medicaid #HomeOwnership #PersonalFinance #Economics1144 #EnhancedLifeEstateDeed #FloridaEstatePlanning #AvoidProbate""",
    "tags": [],
    "categoryId": "27",
}

VIDEO5_THUMBNAIL = BASE + "hf_20260621_054616_0bb67d91-42eb-401f-aaaf-43c18c86eb3b.png"

# ── Video 6: Ladybird Deed vs Quitclaim Deed ─────────────────────────────────
VIDEO6_SCENES = [
    BASE + "hf_20260621_054929_1f0fe2eb-e62c-4b3c-9c6c-84bbe6754dba.mp4",   # Hook
    BASE + "hf_20260621_054930_4b236766-533a-4351-92de-0d3a66d06cea.mp4",   # What Is a Quitclaim Deed
    BASE + "hf_20260621_054931_d3c2d988-ca74-4f32-9bc5-10ffc752b9d6.mp4",   # Problems with Quitclaim
    BASE + "hf_20260621_054933_25ae8bdd-ee79-42c9-a144-5d7ff55ff749.mp4",   # What Is a Ladybird Deed
    BASE + "hf_20260621_054934_b9a42065-add3-41d5-9c93-ab574d5b4b85.mp4",   # Side-by-Side Comparison
    BASE + "hf_20260621_054935_2e103ff8-2dbe-46c3-86f1-6d92491f7ac7.mp4",   # When Quitclaim Is OK
    BASE + "hf_20260621_125601_004468be-d0d9-47f5-96c2-a5c169a91935.mp4",     # Which One to Choose
    BASE + "hf_20260621_125602_a7e29c97-0d97-4f14-bc43-859d8c69d3ca.mp4",     # CTA
]

VIDEO6_AUDIO = [
    BASE + "hf_20260621_054952_839bf70a-9811-4ac3-8ba3-e6c8386ba779.mp3",   # Hook
    BASE + "hf_20260621_054957_2451f15c-8e3d-40b9-88e4-d5c60fc595d5.mp3",   # What Is a Quitclaim Deed
    BASE + "hf_20260621_055003_086a83a5-6f81-4396-9108-e0534ddc8357.mp3",   # Problems with Quitclaim
    BASE + "hf_20260621_055011_71fe97a8-86f5-47f8-bc7b-474c97c79295.mp3",   # What Is a Ladybird Deed
    BASE + "hf_20260621_055013_996fcf2a-f688-4818-b846-1b214ba28a21.mp3",   # Side-by-Side Comparison
    BASE + "hf_20260621_055017_a273041a-5675-4a94-8df1-0ef8c1863144.mp3",   # When Quitclaim Is OK
    BASE + "hf_20260621_055022_f4359c42-7417-4de5-b7b3-2b7f0c442699.mp3",   # Which One to Choose
    BASE + "hf_20260621_055026_4656c1c4-6e7c-48cf-b4a0-8d63abd62d12.mp3",   # CTA
]

VIDEO6_META = {
    "title": "Ladybird Deed vs Quitclaim Deed — Which One Actually Protects Your Home?",
    "description": """⚠️ Thinking about transferring your home to your children? Choosing between a Ladybird Deed and a Quitclaim Deed could be the difference between protecting your family's future — or accidentally triggering a Medicaid penalty, a massive tax bill, or losing control of your own home.

In this video I break down the full comparison in plain English so you know exactly which one to use and why.

✅ What a Quitclaim Deed actually is — and the 3 costly mistakes it causes
✅ How the Ladybird Deed solves every one of those problems
✅ Side-by-side comparison: Control, Probate, Medicaid, Taxes
✅ When a Quitclaim Deed IS actually the right tool
✅ A simple framework to decide which one you need

📌 CHAPTERS:
0:00 – Introduction & Hook
0:50 – What Is a Quitclaim Deed?
2:15 – The 3 Problems with Using a Quitclaim Deed for Estate Planning
3:30 – What Is a Ladybird Deed?
4:45 – Side-by-Side Comparison (Control, Probate, Medicaid, Taxes)
5:45 – When a Quitclaim Deed IS Appropriate
6:30 – Which One Is Right for You?
7:30 – Encouragement & Call to Action

⚠️ This video is for educational purposes only. Consult a licensed estate planning or real estate attorney in your state before signing any deed.

🔔 Subscribe to Economics 1144 for plain-English financial and legal education every week!
👍 If this helped you, please LIKE this video!

#LadybirdDeed #QuitclaimDeed #EstatePlanning #Probate #Medicaid #HomeOwnership #PersonalFinance #Economics1144 #AvoidProbate #EstatePlanningTips""",
    "tags": [],
    "categoryId": "27",
}

VIDEO6_THUMBNAIL = BASE + "hf_20260621_055033_45b1b4c3-c381-4d1f-904f-0ee11ecd7181.png"


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


def download_audio(audio_urls, folder):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    paths = []
    for i, url in enumerate(audio_urls):
        if "PENDING" in url:
            print(f"  ⚠️  Audio {i+1} not ready yet")
            return None
        dest = folder / f"audio_{i+1:02d}.mp3"
        if dest.exists() and dest.stat().st_size > 10_000:
            print(f"  ✓ Audio {i+1} already downloaded")
        else:
            print(f"  ↓ Downloading audio {i+1}...")
            r = requests.get(url, stream=True, timeout=60)
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(65536):
                    f.write(chunk)
            print(f"    {dest.stat().st_size // 1024}KB")
        paths.append(str(dest))
    return paths


def merge_scenes_with_audio(scene_paths, audio_paths, work_dir):
    Path(work_dir).mkdir(exist_ok=True)
    merged = []
    for i, (video, audio) in enumerate(zip(scene_paths, audio_paths)):
        out = str(Path(work_dir) / f"merged_{i+1:02d}.mp4")
        cmd = ["ffmpeg", "-y",
               "-stream_loop", "-1", "-i", video,
               "-i", audio,
               "-shortest", "-map", "0:v", "-map", "1:a",
               "-c:v", "copy", "-c:a", "aac", out]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ffmpeg merge error scene {i+1}:", result.stderr[-300:])
            raise RuntimeError("ffmpeg merge failed")
        print(f"  ✓ Scene {i+1} merged ({Path(out).stat().st_size // 1024}KB)")
        merged.append(out)
    return merged


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
    try:
        from PIL import Image
        import io
        thumb_path = Path(__file__).parent / "thumbnail.jpg"
        r = requests.get(thumbnail_url, timeout=30)
        img = Image.open(io.BytesIO(r.content))
        img = img.convert("RGB")
        img.thumbnail((1280, 720))
        img.save(thumb_path, "JPEG", quality=85)
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
        ).execute()
        print(f"  ✓ Thumbnail set")
    except Exception as e:
        print(f"  ⚠️  Thumbnail skipped ({e}) — upload manually in YouTube Studio")


def main():
    work_dir = Path(__file__).parent
    youtube = get_youtube_service()

    # ── VIDEO 3: The 4% Rule ──────────────────────────────────────────────────
    print("\n=== VIDEO 3: How to Never Run Out of Money — The 4% Rule ===")
    v3_scenes = download_scenes(VIDEO3_SCENES, work_dir / "video3_scenes")
    v3_audio  = download_audio(VIDEO3_AUDIO,  work_dir / "video3_audio")
    if v3_scenes and v3_audio:
        merged3 = merge_scenes_with_audio(v3_scenes, v3_audio, work_dir / "video3_merged")
        v3_out = str(work_dir / "video3_final.mp4")
        concatenate(merged3, v3_out)
        v3_id = upload_video(youtube, v3_out, VIDEO3_META)
        set_thumbnail(youtube, v3_id, VIDEO3_THUMBNAIL)

    # ── VIDEO 4: Roth IRA vs Traditional IRA ─────────────────────────────────
    print("\n=== VIDEO 4: Roth IRA vs Traditional IRA ===")
    v4_scenes = download_scenes(VIDEO4_SCENES, work_dir / "video4_scenes")
    v4_audio  = download_audio(VIDEO4_AUDIO,  work_dir / "video4_audio")
    if v4_scenes and v4_audio:
        merged4 = merge_scenes_with_audio(v4_scenes, v4_audio, work_dir / "video4_merged")
        v4_out = str(work_dir / "video4_final.mp4")
        concatenate(merged4, v4_out)
        v4_id = upload_video(youtube, v4_out, VIDEO4_META)
        set_thumbnail(youtube, v4_id, VIDEO4_THUMBNAIL)

    # ── VIDEO 5: The Ladybird Deed ────────────────────────────────────────────
    print("\n=== VIDEO 5: The Ladybird Deed ===")
    v5_scenes = download_scenes(VIDEO5_SCENES, work_dir / "video5_scenes")
    v5_audio  = download_audio(VIDEO5_AUDIO,  work_dir / "video5_audio")
    if v5_scenes and v5_audio:
        merged5 = merge_scenes_with_audio(v5_scenes, v5_audio, work_dir / "video5_merged")
        v5_out = str(work_dir / "video5_final.mp4")
        concatenate(merged5, v5_out)
        v5_id = upload_video(youtube, v5_out, VIDEO5_META)
        set_thumbnail(youtube, v5_id, VIDEO5_THUMBNAIL)

    # ── VIDEO 6: Ladybird Deed vs Quitclaim Deed ──────────────────────────────
    print("\n=== VIDEO 6: Ladybird Deed vs Quitclaim Deed ===")
    v6_scenes = download_scenes(VIDEO6_SCENES, work_dir / "video6_scenes")
    v6_audio  = download_audio(VIDEO6_AUDIO,  work_dir / "video6_audio")
    if v6_scenes and v6_audio:
        merged6 = merge_scenes_with_audio(v6_scenes, v6_audio, work_dir / "video6_merged")
        v6_out = str(work_dir / "video6_final.mp4")
        concatenate(merged6, v6_out)
        v6_id = upload_video(youtube, v6_out, VIDEO6_META)
        set_thumbnail(youtube, v6_id, VIDEO6_THUMBNAIL)

    print("\n✅ All done!")


if __name__ == "__main__":
    main()
