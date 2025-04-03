from flask import Flask, request, render_template, make_response, jsonify, redirect, url_for
import jwt
import os
import base64
import datetime
import subprocess
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from waitress import serve

app = Flask(__name__, template_folder="templates", static_folder="static")

FLAG_FILE = "flags/psychic_signature_flag.txt"
PRIVATE_KEY_FILE = "ec_private.pem"
PUBLIC_KEY_FILE = "ec_public.pem"

# Generera ECDSA-nycklar om de inte finns
if not os.path.exists(PRIVATE_KEY_FILE) or not os.path.exists(PUBLIC_KEY_FILE):
    print("[+] Generating ECDSA keypair for ES256...")
    subprocess.run(["openssl", "ecparam", "-name", "prime256v1", "-genkey", "-noout", "-out", PRIVATE_KEY_FILE], check=True)
    subprocess.run(["openssl", "ec", "-in", PRIVATE_KEY_FILE, "-pubout", "-out", PUBLIC_KEY_FILE], check=True)

# Läs in nycklar
with open(PRIVATE_KEY_FILE, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_FILE, "r") as f:
    PUBLIC_KEY = f.read()

# Skapa flaggfil om den inte finns
if not os.path.exists(FLAG_FILE):
    os.makedirs("flags", exist_ok=True)
    with open(FLAG_FILE, "w") as f:
        f.write("O24{jwt_psychic_signatures_unveiled}")

@app.after_request
def remove_server_header(response):
    response.headers.pop("Server", None)
    return response

def generate_token(username, role="user"):
    # Skapa en ogiltig token med rollen som "user"
    payload = {
        "username": username,
        "role": role,  # Ursprunglig roll är user
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="ES256")
    
    # Skicka tillbaka ogiltig token så att användaren kan manipulera den
    return render_template("login.html", message=f"✅ Token generated for {username}. You can decode and modify it.", token=token)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # Skapa ogiltig token när användarnamn skickas
    username = request.form.get("username")
    if not username:
        return render_template("login.html", message="⚠️ Please enter a name!")

    return generate_token(username)

@app.route("/admin")
def admin():
    # Hämta token från cookies
    token = request.cookies.get("auth_token")

    # Om token inte finns, visa meddelande och neka åtkomst
    if not token:
        return render_template("admin.html", message="👁️ You are not ready to uncover the Pharaoh's secrets..."), 403

    try:
        # Här försöker vi dekoda tokenen och kolla om den har blivit modifierad till admin
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["ES256"])

        # Om användaren är admin, ge tillgång till flaggan
        if decoded.get("role") == "admin":
            with open(FLAG_FILE, "r") as f:
                flag = f.read().strip()
            return render_template("admin.html", flag=flag)

        return render_template("admin.html", message="⚠️ The spirits reject your presence. Leave now!"), 403

    except jwt.ExpiredSignatureError:
        return render_template("admin.html", message="⏳ Your time has run out..."), 403
    except jwt.InvalidTokenError as e:
        return render_template("admin.html", message=f"❌ The spirits whisper: this token is not valid... ({e})"), 403

@app.route("/debug/decode", methods=["POST"])
def debug_decode():
    data = request.get_json()
    token = data.get("token", "")
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return jsonify({"error": "Malformed token"}), 400
        header_b64, payload_b64, signature_b64 = parts
        sig_bytes = base64.urlsafe_b64decode(signature_b64 + '==')
        r, s = decode_dss_signature(sig_bytes)
        return jsonify({"r": r, "s": s})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=6001)
