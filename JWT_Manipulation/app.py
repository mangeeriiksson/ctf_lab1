from flask import Flask, request, jsonify, render_template, make_response
import jwt
import datetime
import os
import base64

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "Tutankhamun’s Curse"  # Static secret key for JWT (intentional vulnerability)

FLAG_FILE = "flags/psychic_signature_flag.txt"

# Skapa flaggfil om den inte finns
if not os.path.exists(FLAG_FILE):
    os.makedirs("flags", exist_ok=True)
    with open(FLAG_FILE, "w") as f:
        f.write("O24{jwt_psychic_signatures_unveiled}")

def generate_token(username):
    payload = {
        "username": username,
        "role": "user",  # Alla får USER som standard
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.secret_key, algorithm="HS256")

    response = make_response(jsonify({"token": token}))
    response.headers["Server"] = "Apache Tomcat/9.0.41 (OpenJDK 64-Bit Server VM)"

    # Se till att SameSite & Secure hanteras korrekt
    secure_cookie = os.getenv("FLASK_ENV") == "production"
    response.set_cookie("auth_token", token, httponly=True, samesite="None", secure=secure_cookie)

    return response

@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    response.headers["Server"] = "Apache Tomcat/9.0.41 (OpenJDK 64-Bit Server VM)"
    return response

@app.route("/admin")
def admin():
    token = request.cookies.get("auth_token")
    print("DEBUG: Received auth_token:", token)

    if not token:
        print("DEBUG: No token received")
        return render_template("admin.html", message="👁️ You are not ready to uncover the Pharaoh's secrets..."), 403

    try:
        # Splitta JWT-token i dess tre delar
        header, payload, signature = token.split(".")

        # Base64-dekoda signaturen
        decoded_signature = jwt.utils.base64url_decode(signature + "==").decode(errors="ignore")
        print("DEBUG: Decoded Signature:", decoded_signature)

        # 🛠️ **Bypass Signaturkontrollen!** Om signaturen är "MAYCAQACAQA=", ignorera signaturverifieringen
        if signature == "MAYCAQACAQA=":
            decoded = jwt.decode(token, options={"verify_signature": False})  # Skippar signaturvalidering!
            user_role = "admin"
            print("DEBUG: Signature bypassed - User is now Admin")
        else:
            decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])  # Normal verifiering
            user_role = decoded.get("role", "unknown")

        print(f"DEBUG: Role in token: {user_role}")

        if user_role == "admin":
            print("DEBUG: Role is admin - granting access")
            with open(FLAG_FILE, "r") as f:
                flag = f.read().strip()
            return render_template("admin.html", flag=flag)
        else:
            print(f"DEBUG: Role is {user_role} - Access Denied")
            return render_template("admin.html", message="⚠️ The spirits reject your presence. Leave now!"), 403

    except jwt.ExpiredSignatureError:
        print("DEBUG: Token expired")
        return render_template("admin.html", message="⏳ Your time has run out..."), 403
    except jwt.InvalidTokenError as e:
        print(f"DEBUG: Invalid token - {e}")
        return render_template("admin.html", message="❌ The spirits whisper: this token is not valid..."), 403

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    if not username:
        return jsonify({"error": "Username required"}), 400
    return generate_token(username)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001, debug=True)
