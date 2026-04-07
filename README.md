# Daily Hacker News Digest

Get the top Hacker News stories from yesterday delivered to your inbox every morning. Zero infrastructure — runs entirely on GitHub Actions for free.

## How it works

1. Fetches yesterday's top 30 stories from the [Algolia HN Search API](https://hn.algolia.com/api)
2. Formats them into a clean HTML email with titles, points, comment links, and authors
3. Sends the digest via [Resend](https://resend.com)
4. Runs daily at 8am UTC on GitHub Actions

## Get your own in 5 minutes

### 1. Fork this repo

Click the **Fork** button at the top right of this page.

### 2. Create a Resend account

- Sign up at [resend.com](https://resend.com) (free tier: 3,000 emails/month)
- Go to **API Keys** and create one
- Add and verify a sending domain under **Domains** (or use `onboarding@resend.dev` for testing)

### 3. Add secrets to your fork

Go to your fork's **Settings > Secrets and variables > Actions** and add:

| Secret | Example |
|---|---|
| `RESEND_API_KEY` | `re_123abc...` |
| `EMAIL_FROM` | `Daily HN <digest@yourdomain.com>` |
| `EMAIL_TO` | `you@example.com` |

`EMAIL_TO` supports multiple recipients — just comma-separate them.

### 4. Test it

Go to **Actions > Daily HN Digest > Run workflow** to trigger it manually. Check your inbox.

That's it. The workflow runs automatically every day at 8am UTC from now on.

## Customize

- **Number of stories**: change `num_stories=30` in `main.py`
- **Schedule**: edit the cron in `.github/workflows/daily.yml` ([crontab.guru](https://crontab.guru) helps)
- **Minimum points threshold**: adjust the `points>5` filter in `fetch_top_stories()`

## Run locally

```bash
git clone https://github.com/YOUR_USERNAME/daily-hackernews.git
cd daily-hackernews
pip install -r requirements.txt

export RESEND_API_KEY=re_...
export EMAIL_FROM="Daily HN <digest@yourdomain.com>"
export EMAIL_TO=you@example.com

python main.py
```
