from flask import Flask, request, render_template, send_from_directory
import subprocess
import os
import shlex

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "indiana_jones_secret"

FLAGS_DIR = "flags"
FLAG_FILE = os.path.join(FLAGS_DIR, "sacred_command.txt")

# Skapa flaggfilen om den inte finns
os.makedirs(FLAGS_DIR, exist_ok=True)
if not os.path.exists(FLAG_FILE):
    with open(FLAG_FILE, "w") as f:
        f.write("O24{command_of_the_pharaoh}")

# Fix för statiska filer
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route("/")
def index():
    return render_template("temple_anubis.html")

@app.route("/temple", methods=["GET", "POST"])
def temple_of_anubis():
    result = None

    if request.method == "POST":
        command = request.form.get("command", "").strip()

        # Tillåtna kommandon
        allowed_commands = ["ls", "ls -R", "ls flags"]
        
        # Om användaren försöker läsa flaggan, inkludera det i tillåtna kommandon
        if command.startswith("cat") and "flags/sacred_command.txt" in command:
            allowed_commands.append(command)

        cmd_parts = shlex.split(command)

        if cmd_parts and command in allowed_commands:
            try:
                # Om spelaren skriver exakt rätt kommando, visa endast flaggan
                if command == f"cat {FLAG_FILE}":
                    with open(FLAG_FILE, "r") as f:
                        result = f.read().strip()  # Visar endast flaggan, ingen extra text
                else:
                    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
            except Exception as e:
                result = f"Error executing command: {e}"
        else:
            result = "⚠️ Forbidden command! The gods do not approve of this magic."

    return render_template("temple_anubis.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
