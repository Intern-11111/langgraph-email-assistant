from flask import Flask, request, render_template, jsonify, redirect, url_for
import base64
import json
import logging
from googleapiclient.errors import HttpError

from config import PORT, REVIEW_DB

from email_fetcher import (
    fetch_email,
    fetch_email_subject,
    fetch_email_body,
    fetch_email_sender,
)

from classifier import classify_email_overall
from action_engine import process_email
from review_queue import load_reviews, save_reviewed_email

from gmail_listener import fetch_new_message_ids   # IMPORTANT

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/gmail-webhook", methods=["POST"])
def gmail_webhook():

    data_json = request.get_json(silent=True)

    # Accept verification pings
    if not data_json:
        logging.info("Empty Pub/Sub verification ping received")
        return "OK", 200

    logging.info("Pub/Sub push received: %s", data_json)

    history_id = None

    # Decode Pub/Sub payload
    if isinstance(data_json, dict) and "message" in data_json:
        try:
            pubsub_message = data_json["message"]

            raw = base64.b64decode(
                pubsub_message.get("data", "")
            ).decode("utf-8")

            payload = json.loads(raw) if raw else {}

            history_id = payload.get("historyId")

        except Exception as e:
            logging.exception("Failed to decode Pub/Sub message")
            return "OK", 200

    # If no historyId, safely exit
    if not history_id:
        logging.warning("No historyId found in push payload")
        return "OK", 200

    logging.info("📨 Gmail History Event Received: %s", history_id)

    try:
        # Fetch actual new Gmail message IDs
        message_ids = fetch_new_message_ids(history_id)

        message_ids = message_ids[-10:]  # Limit to last 10 messages

        logging.info("New messages detected: %s", message_ids)

        for msg_id in message_ids:

            snippet = fetch_email(msg_id)
            subject = fetch_email_subject(msg_id)
            body = fetch_email_body(msg_id)
            sender = fetch_email_sender(msg_id)

            label = classify_email_overall(
                snippet or "",
                subject or "",
                body or "",
                sender or ""
            )

            logging.info("Detected label=%s for message_id=%s", label, msg_id)

            # Send full body (fallback to snippet) along with subject/sender
            process_email(
                msg_id,
                label,
                body or snippet or "",
                subject=subject,
                sender=sender,
            )

        return jsonify({"status": "ok"}), 200

    except HttpError as e:
        logging.exception("Gmail API error")
        return jsonify({"error": "Gmail API error", "details": str(e)}), 502

    except Exception as e:
        logging.exception("Unhandled webhook error")
        return jsonify({"error": "Server error", "details": str(e)}), 500


# ============================
# HUMAN REVIEW DASHBOARD
# ============================

@app.route("/dashboard")
def dashboard():
    try:
        reviews = load_reviews()
    except Exception:
        reviews = []

    return render_template("dashboard.html", emails=reviews)


@app.route("/dashboard/approve", methods=["POST"])
def dashboard_approve():

    email_id = request.form.get("id")
    content = request.form.get("content", "")

    if not email_id:
        return redirect(url_for("dashboard"))

    save_reviewed_email({
        "id": email_id,
        "content": content,
        "status": "approved"
    })

    try:
        with open(REVIEW_DB, "r") as f:
            data = json.load(f)
    except Exception:
        data = []

    data = [item for item in data if str(item.get("id")) != str(email_id)]

    with open(REVIEW_DB, "w") as f:
        json.dump(data, f, indent=4)

    return redirect(url_for("dashboard"))


@app.route("/dashboard/delete", methods=["POST"])
def dashboard_delete():

    email_id = request.form.get("id")

    if not email_id:
        return redirect(url_for("dashboard"))

    try:
        with open(REVIEW_DB, "r") as f:
            data = json.load(f)
    except Exception:
        data = []

    data = [item for item in data if str(item.get("id")) != str(email_id)]

    with open(REVIEW_DB, "w") as f:
        json.dump(data, f, indent=4)

    return redirect(url_for("dashboard"))


# ============================
# HEALTH CHECK
# ============================

@app.route("/health", methods=["GET"])
def health():

    from gmail_auth import get_gmail_service

    try:
        service = get_gmail_service()
        service.users().messages().list(userId="me", maxResults=1).execute()

        return jsonify({"status": "ok"}), 200

    except HttpError as e:
        return jsonify({"status": "error", "details": str(e)}), 502

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


# ============================
# MAIN ENTRY
# ============================

if __name__ == "__main__":
    app.run(port=PORT)


