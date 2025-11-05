import requests
from collections import Counter
from datetime import datetime, timedelta
import os

# ======= CONFIGURE VIA ENV VARIABLES =======
BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
# ==========================================

if not BOT_TOKEN or not CHANNEL_ID:
    print("Error: Environment variables not set!")
    exit()

# Weekly time range
now = datetime.utcnow()
week_ago = now - timedelta(days=7)
oldest = int(week_ago.timestamp())
latest = int(now.timestamp())

# Fetch messages
url = "https://slack.com/api/conversations.history"
headers = {"Authorization": f"Bearer {BOT_TOKEN}"}
params = {"channel": CHANNEL_ID, "oldest": oldest, "latest": latest, "limit": 1000}

response = requests.get(url, headers=headers, params=params)
data = response.json()

if not data.get("ok"):
    print("Error fetching messages:", data)
    exit()

# Count messages per user
user_counts = Counter()
for msg in data.get("messages", []):
    user = msg.get("user")
    if user:
        user_counts[user] += 1

# Format report
report = f"Weekly report for channel {CHANNEL_ID}:\n"
for user, count in user_counts.items():
    report += f"<@{user}>: {count} messages\n"

print(report)

# Post report to Slack
post_url = "https://slack.com/api/chat.postMessage"
post_data = {"channel": CHANNEL_ID, "text": report}
post_response = requests.post(post_url, headers=headers, json=post_data)
