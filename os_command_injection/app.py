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
    hint = None
    flag = None  # Nu hanteras flaggan separat igen

    if request.method == "POST":
        command = request.form.get("command", "").strip()

        # Tillåtna kommandon och matchningslogik
        allowed_commands = ["ls", "ls -R", "ls flags"]
        if command.startswith("cat") and "flags/sacred_command.txt" in command:
            allowed_commands.append(command)

        cmd_parts = shlex.split(command)

        if cmd_parts and command in allowed_commands:
            try:
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()

                # Visa flaggan endast vid rätt kommando och på rätt plats
                if "cat" in command and "flags/sacred_command.txt" in command:
                    with open(FLAG_FILE, "r") as f:
                        flag = f.read().strip()
            except Exception as e:
                result = f"Error executing command: {e}"
        else:
            result = "⚠️ Forbidden command! The gods do not approve of this magic."
    
    # Dynamisk hint baserat på spelarens framsteg
    if request.args.get("hint"):
        hinted_commands = request.args.get("hinted_commands", "")
        
        if "ls" in hinted_commands:
            hint = "You have discovered the sacred chamber... But how will you find what’s inside? Try 'ls flags/'"
        elif "ls flags" in hinted_commands:
            hint = "You see the sacred text... But only those who *speak its name* may reveal its secrets. Try 'cat flags/sacred_command.txt'"
        else:
            hint = "The sacred knowledge lies within the hidden chambers... Try exploring with 'ls'."

    return render_template("temple_anubis.html", result=result, hint=hint, flag=flag)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
