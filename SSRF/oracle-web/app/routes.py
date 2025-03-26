from flask import Blueprint, request, render_template
import requests
import random

bp = Blueprint("bp", __name__)

oracle_quotes = [
    "Only those who read between the protocols shall be enlightened.",
    "The gods hide behind status codes and timeouts.",
    "He who pings the void, risks awakening it.",
    "A forged request is a step toward forbidden knowledge.",
    "The scrolls speak... if you know where to look.",
    "Some scrolls are visible only at port 6008..."
]

@bp.route("/")
def index():
    debug = request.args.get("debug") == "1"
    return render_template("index.html", debug=debug)

@bp.route("/ask")
def ask():
    url = request.args.get("url")
    if not url:
        return "⛔ The Oracle requires a URL.", 400

    if "google.com" in url or "http" not in url:
        return (
            "🌪️ The Oracle cannot reach the outside realm. "
            "Only inner ports like 127.0.0.1:6008 may be consulted.",
            400
        )

    try:
        r = requests.get(url, timeout=3)
        quote = random.choice(oracle_quotes)

        # Visa en hint om 404
        if r.status_code == 404:
            hint = "📜 Nothing found there... but the scrolls hide well. Have you tried robots.txt?"
        else:
            hint = None

        return render_template("ask.html", response_text=r.text, quote=quote, hint=hint)

    except requests.exceptions.Timeout:
        return "🕒 The Oracle waited, but the realm did not respond in time...", 504

    except Exception as e:
        return f"⚠️ The Oracle failed to reach that realm. Error: {str(e)}", 500
