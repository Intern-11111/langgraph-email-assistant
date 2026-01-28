# TeamD1 – Real‑Time Gmail Email Assistant

This document describes the programs in TeamD1 and how they work together to deliver a real‑time, human‑in‑the‑loop email review workflow.

## Overview
- Real‑time Gmail watch triggers on new inbox messages via Google Pub/Sub.
- A Flask webhook processes push events, fetches email data, classifies it, and queues dangerous items for human review.
- A dashboard displays pending emails (subject, sender, full body) for approve/delete.

## Architecture & Data Flow
1. Gmail Watch
   - [gmail_watch.py](gmail_watch.py) registers a Gmail watch on a Pub/Sub topic (`projects/$PROJECT_ID/topics/$PUBSUB_TOPIC`).
2. Pub/Sub Push → Webhook
   - Google Pub/Sub delivers push events to the Flask endpoint `/gmail-webhook` handled by [app.py](app.py).
3. Fetch & Classify
   - [email_fetcher.py](email_fetcher.py) retrieves `snippet`, `subject`, `sender`, `body`.
   - [classifier.py](classifier.py) classifies: `dangerous` (phishing), `spam` (promotions), or `safe`.
4. Actions
   - [action_engine.py](action_engine.py) routes by class:
     - `dangerous`: queue for review with full body, archive from inbox
     - `spam`: archive
     - `safe`: no action
   - Queued items are stored via [review_queue.py](review_queue.py) in [data/pending_reviews.json](../data/pending_reviews.json).
5. Human Review
   - [templates/dashboard.html](templates/dashboard.html) renders the review queue.
   - Approvals are saved to [reports/approved_actions.json](../reports/approved_actions.json).

## Components
- Web App: [app.py](app.py)
  - Routes: `/gmail-webhook`, `/dashboard`, `/dashboard/approve`, `/dashboard/delete`, `/health`, `/`.
  - Uses `render_template()` to serve the dashboard.
- Gmail API:
  - Auth: [gmail_auth.py](gmail_auth.py) (uses `client_secret_*.json` and `token.json`).
  - Watch: [gmail_watch.py](gmail_watch.py).
  - History fetcher: [gmail_listener.py](gmail_listener.py).
- Processing:
  - Classifier: [classifier.py](classifier.py) – keyword heuristics.
  - Actions: [action_engine.py](action_engine.py) – archive & queue logic.
  - Review queue: [review_queue.py](review_queue.py) – JSON persistence.
- UI:
  - Template: [templates/dashboard.html](templates/dashboard.html) – shows subject, sender, full body; auto‑refreshes every 10s.

## Setup
### Requirements
- Python 3.11
- Google Cloud project with Pub/Sub enabled
- Gmail API enabled and OAuth client secret JSON
- Environment variables:
  - `PROJECT_ID` – GCP project ID
  - `PUBSUB_TOPIC` – Pub/Sub topic name (without `projects/.../topics/` prefix)
  - `FLASK_PORT` (optional, default 5000)

### Credentials
- Place `client_secret_*.json` in the [TeamD1](.) folder.
- First run will create/update `token.json` after OAuth login.

### Install deps (if needed)
The repository includes a venv under `ai/`. Activate it or install requirements:

```bash
# Option A: Use existing venv
./ai/Scripts/Activate.ps1

# Option B: Create venv + install
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Real‑Time Operation
### 1) Run the Flask app
```bash
python TeamD1/app.py
```
Expose it publicly for Pub/Sub push (e.g., ngrok):
```bash
ngrok http 5000
```
Use the public HTTPS URL for the push subscription endpoint: `https://<your-public-url>/gmail-webhook`.

### 2) Start Gmail watch
```bash
python TeamD1/gmail_watch.py
```
This registers a watch on `INBOX`. Gmail sends events to your Pub/Sub topic, which pushes to the webhook.

### 3) Send a test email
- Dangerous (will appear on dashboard for review):
  - Subject: Urgent: Verify Your Bank Account
  - Body: "Please click here to verify; enter the OTP; do not share your password."
- Spam (will be archived):
  - Subject: Exclusive Offer: 70% Discount On Gadgets!
  - Body: "Use promo code FREE70; limited‑time deal and discount."

### 4) Review queue dashboard
- Visit: `http://127.0.0.1:5000/dashboard`
- Shows subject, sender, full body.
- Approve → moves to [../reports/approved_actions.json](../reports/approved_actions.json) and removes from [../data/pending_reviews.json](../data/pending_reviews.json).
- Delete → removes from pending reviews.

## Health & Diagnostics
- Health endpoint: `GET /health` uses Gmail API to verify connectivity.
- Logs: Flask console output and your terminal.

## Troubleshooting
- Pub/Sub push not reaching webhook:
  - Ensure the app is publicly reachable (HTTPS), not `127.0.0.1`.
  - Push subscription must point to `/gmail-webhook`.
- Gmail watch stops:
  - Re‑run [gmail_watch.py](gmail_watch.py); Gmail watches expire.
- Credentials errors:
  - Ensure `client_secret_*.json` is present; re‑authenticate to refresh `token.json`.
- No items on dashboard:
  - Only `dangerous` emails are queued. Try the phishing sample above.

## Notes on Storage & Security
- Pending reviews: [../data/pending_reviews.json](../data/pending_reviews.json)
- Approved actions: [../reports/approved_actions.json](../reports/approved_actions.json)
- Secrets & tokens are ignored via `.gitignore` (e.g., `TeamD1/token.json`, `TeamD1/client_secret_*.json`).

## Next Steps
- Add real‑time UI updates via Server‑Sent Events/WebSockets.
- Enhance classifier with ML model or rules.
- Persist storage using a database instead of JSON files.
