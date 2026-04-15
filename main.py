import os
import sys
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlparse

import requests
import resend


def fetch_top_stories(num_stories=30):
    yesterday = date.today() - timedelta(days=1)
    start_ts = int(datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=timezone.utc).timestamp())
    end_ts = start_ts + 86400

    resp = requests.get(
        "https://hn.algolia.com/api/v1/search",
        params={
            "tags": "story",
            "numericFilters": f"created_at_i>{start_ts},created_at_i<{end_ts},points>5",
            "hitsPerPage": num_stories,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["hits"]


def format_email(stories, date_str):
    subject = f"Hacker News Digest - {date_str}"

    rows = ""
    for i, story in enumerate(stories, 1):
        title = story.get("title", "Untitled")
        url = story.get("url") or f"https://news.ycombinator.com/item?id={story['objectID']}"
        points = story.get("points", 0)
        comments = story.get("num_comments", 0)
        hn_link = f"https://news.ycombinator.com/item?id={story['objectID']}"
        parsed = urlparse(url)
        display_url = f"{parsed.netloc}{parsed.path}".rstrip("/")

        rows += f"""
        <tr>
          <td style="padding:12px 16px;border-bottom:1px solid #eee;">
            <div style="font-size:15px;line-height:1.4;">
              <span style="color:#999;font-size:13px;">{i}.</span>
              <a href="{url}" style="color:#1a1a1a;text-decoration:none;font-weight:500;">{title}</a>
            </div>
            <div style="font-size:12px;color:#888;margin-top:4px;">
              {points} points &middot;
              <a href="{hn_link}" style="color:#888;text-decoration:none;">{comments} comments</a> &middot;
              <a href="{url}" style="color:#888;text-decoration:none;">{display_url[:60]}{"…" if len(display_url) > 60 else ""}</a>
            </div>
          </td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:600px;margin:20px auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
    <div style="background:#ff6600;padding:20px 24px;">
      <h1 style="margin:0;font-size:20px;color:#fff;">Hacker News Digest</h1>
      <p style="margin:4px 0 0;font-size:13px;color:rgba(255,255,255,0.85);">{date_str} &middot; Top {len(stories)} stories</p>
    </div>
    <table style="width:100%;border-collapse:collapse;">
      {rows}
    </table>
    <div style="padding:16px 24px;font-size:11px;color:#aaa;text-align:center;">
      Powered by Algolia HN Search API
    </div>
  </div>
</body>
</html>"""

    return subject, html


def send_email(subject, html_body):
    resend.api_key = os.environ["RESEND_API_KEY"]

    to_addresses = [addr.strip() for addr in os.environ["EMAIL_TO"].split(",")]

    resend.Emails.send({
        "from": os.environ["EMAIL_FROM"],
        "to": to_addresses,
        "subject": subject,
        "html": html_body,
    })


def main():
    stories = fetch_top_stories(num_stories=30)

    if not stories:
        print("No stories found for yesterday. Skipping email.")
        sys.exit(0)

    yesterday = date.today() - timedelta(days=1)
    date_str = yesterday.strftime("%B %-d, %Y")

    subject, html_body = format_email(stories, date_str)
    send_email(subject, html_body)

    print(f"Digest sent: {len(stories)} stories for {date_str}")


if __name__ == "__main__":
    main()
