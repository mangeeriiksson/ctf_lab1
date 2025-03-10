from flask import Flask, request, render_template, make_response

import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "pharaohs_secret_key"

FLAGS_DIR = "flags"
FLAG_FILE = os.path.join(FLAGS_DIR, "pharaohs_seal.txt")

# Skapa flaggan om den saknas
os.makedirs(FLAGS_DIR, exist_ok=True)
if not os.path.exists(FLAG_FILE):
    with open(FLAG_FILE, "w") as f:
        f.write("O24{duat_barriers_fall_as_the_false_pharaoh_rises}")

# 🔐 Broken Access Control - Admin Panel
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    role = request.cookies.get("role", "user")
    hint = request.args.get("hint")  # Kollar om spelaren begär en hint

    if role == "admin":
        with open(FLAG_FILE, "r") as f:
            flag = f.read().strip()
        return render_template("admin.html", flag=flag)

    response = make_response(render_template("admin.html", flag=None, hint=hint))
    response.set_cookie("role", "user")  # Sätter standardroll
    return response
