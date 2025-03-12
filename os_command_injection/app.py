from flask import Flask, request, render_template, send_from_directory
import subprocess
import os
import shlex

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "indiana_jones_secret"

FLAG_FILE = "/root/true_flag.txt"
FAKE_FLAGS = {
    "/var/www/html/lost_scroll.txt": "O24{you_thought_this_was_real}",
    "/root/ancient_curse.txt": "O24{almost_there_but_not}" 
}

# Skapa den riktiga flaggan
os.makedirs(os.path.dirname(FLAG_FILE), exist_ok=True)
if not os.path.exists(FLAG_FILE):
    with open(FLAG_FILE, "w") as f:
        f.write("O24{command_of_the_pharaoh}")

# Skapa falska flaggor
for path, content in FAKE_FLAGS.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)

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
        allowed_commands = [
            "ls", "ls -R", "ls /var/www/html", "ls /root", "ls flags",
            "pwd", "whoami", "id"
        ]

        # Om användaren försöker läsa flaggan eller falska flaggor
        if command.startswith("cat") and any(flag in command for flag in FAKE_FLAGS.keys()) or command == f"cat {FLAG_FILE}":
            allowed_commands.append(command)

        cmd_parts = shlex.split(command)

        if cmd_parts and command in allowed_commands:
            try:
                # Om spelaren skriver exakt rätt kommando, visa endast flaggan
                if command == f"cat {FLAG_FILE}":
                    with open(FLAG_FILE, "r") as f:
                        result = f.read().strip()
                elif command == "ls /root":
                    result = "ancient_curse.txt"  # Visar endast falska flaggan i /root
                elif command in FAKE_FLAGS.keys():
                    result = FAKE_FLAGS[command]
                else:
                    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
            except Exception as e:
                result = f"Error executing command: {e}"
        else:
            result = "⚠️ Forbidden command! The gods do not approve of this magic."

    return render_template("temple_anubis.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
