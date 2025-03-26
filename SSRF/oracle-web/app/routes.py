from flask import Blueprint, request, render_template
import requests
import random

bp = Blueprint("bp", __name__)

oracle_quotes = [
    "Only those who read between the protocols shall be enlightened.",
    "The gods hide behind status codes and timeouts.",
    "He who pings the void, risks awakening it.",
    "A forged request is a step toward forbidden knowledge.",
    "The scrolls speak... if you know where to look."
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

    try:
        r = requests.get(url, timeout=3)
        quote = random.choice(oracle_quotes)
        return render_template("ask.html", response_text=r.text, quote=quote)
    except Exception as e:
        return f"⚠️ The Oracle failed to reach that realm. Error: {str(e)}", 500
