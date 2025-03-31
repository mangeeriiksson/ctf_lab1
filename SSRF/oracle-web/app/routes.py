from flask import Blueprint, request, render_template, Response
import requests
import random

bp = Blueprint("bp", __name__)

oracle_quotes = [
    "Only those who read between the protocols shall be enlightened.",
    "The gods hide behind status codes and timeouts.",
    "He who pings the void, risks awakening it.",
    "A forged request is a step toward forbidden knowledge.",
    "The scrolls speak... if you know where to look.",
    "Some scrolls are visible only at port 6008...",
]

# Start page
@bp.route("/")
def index():
    debug = request.args.get("debug") == "1"
    quote = random.choice(oracle_quotes)
    return render_template("index.html", debug=debug, quote=quote)

# SSRF endpoint
@bp.route("/ask")
def ask():
    url = request.args.get("url")
    if not url:
        return "⛔ The Oracle requires a URL.", 400

    # Basic filter to restrict outside URLs
    if "google.com" in url or "http" not in url:
        return (
            "🌪️ The Oracle cannot reach the outside realm. "
            "Only inner ports like 127.0.0.1:6008 may be consulted.",
            400
        )

    try:
        r = requests.get(url, timeout=3)
        quote = random.choice(oracle_quotes)

        hint = None
        if r.status_code == 404:
            hint = "📜 Nothing found there... but the scrolls hide well. Have you tried robots.txt?"

        return render_template("ask.html", response_text=r.text, quote=quote, hint=hint)

    except requests.exceptions.Timeout:
        return "🕒 The Oracle waited, but the realm did not respond in time...", 504

    except Exception as e:
        return f"⚠️ The Oracle failed to reach that realm. Error: {str(e)}", 500

# robots.txt for flavor + hint
@bp.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "# Only the seeker knows what lies within forbidden paths...",
        mimetype="text/plain"
    )

# Optional: visible folder (mystery)
@bp.route("/admin/")
def admin_index():
    return Response(
        "This chamber is no longer guarded.\n"
        "\nSome say old files were archived here… but most are lost to time.",
        mimetype="text/plain"
    )

@bp.route("/admin/flag/")
def flag_folder():
    return Response(
        "📁 One file survived.\n"
        "Its name? Forgotten by many... but not all.",
        mimetype="text/plain"
    )

@bp.route("/admin/flag/oracle-flag.txt")
def flag_file():
    content = (
        "📜 oracle-flag.txt\n"
        "------------------\n"
        "o24{Or4cle_gr4ts_flA6}"
    )
    headers = {
        "Content-Disposition": "inline; filename=oracle-flag.txt"
    }
    return Response(content, mimetype="text/plain", headers=headers)

# Hidden prophecy scroll (used by oracle.js)
@bp.route("/admin/scrolls/73/prophecy")
def secret_scroll():
    return Response(
        "The chosen path begins not in light, but in silence.\n"
        "Its gateway lies hidden behind port 6008, veiled in stone.",
        mimetype="text/plain"
    )
