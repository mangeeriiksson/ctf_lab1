import random
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "AncientPharaohsSecret"

users = {}  
generated_2fa = {}  

CORRECT_PASSWORD = "𓂀𓏏𓆣𓊪"
FLAG = "O24{PHARAOHS_2FA_BROKEN}"

# 🔥 STARTSIDAN
@app.route("/")
def index():
    return render_template("index.html")

# 🔥 Registrering – Genererar 2FA direkt efter registrering
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            return render_template("register.html", error="Username already exists!")

        users[username] = password  
        session["user"] = username
        generated_2fa[username] = str(random.randint(100000, 999999))  
        session["2fa_verified"] = False  
        return redirect(url_for("verify_2fa"))

    return render_template("register.html")

# 🔥 Inloggning – Efter inloggning får användaren sin 2FA-kod
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            session["2fa_verified"] = False
            return redirect(url_for("verify_2fa"))

        return render_template("login.html", error="Invalid username or password!")

    return render_template("login.html")

# 🔥 2FA-verifiering – Exploaterbar via Burp
@app.route("/verify_2fa", methods=["GET", "POST"])
def verify_2fa():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]

    if request.method == "POST":
        user_2fa = request.form.get("2fa")
        verified = request.form.get("verified")  

        if user_2fa == generated_2fa.get(username, "") or verified == "true":  
            session["2fa_verified"] = True
            return redirect(url_for("game"))

        return render_template("verify_2fa.html", fake_2fa=generated_2fa[username], error="Incorrect 2FA code!")

    return render_template("verify_2fa.html", fake_2fa=generated_2fa.get(username, "No Code Found"))

# 🔥 Spelsidan
@app.route("/game")
def game():
    if "user" not in session:
        return redirect(url_for("login"))  

    if not session.get("2fa_verified", False):
        return redirect(url_for("verify_2fa"))  

    return render_template("game.html")

# 🔥 Flagghantering – Nu krävs både lösenord och 2FA!
@app.route("/get_flag", methods=["POST"])
def get_flag():
    if "user" not in session or not session.get("2fa_verified", False):
        return jsonify({"error": "Unauthorized access!"}), 403

    data = request.json
    password = data.get("password", "").strip()
    twofa = data.get("twofa", "").strip()  

    if password == CORRECT_PASSWORD:
        if twofa == generated_2fa.get(session["user"], "") or twofa == "":  
            return jsonify({"flag": FLAG, "message": "The vault opens, revealing an ancient secret..."})

        return jsonify({"error": "The Pharaoh’s seal remains locked!"}), 403

    return jsonify({"error": "The Pharaoh rejects you!"}), 403

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
