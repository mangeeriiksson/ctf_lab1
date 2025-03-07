from flask import Flask, request, render_template, session
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "indiana_jones_secret"

BASE_DIR = os.path.abspath(os.getcwd())
FLAGS_DIR = os.path.join(BASE_DIR, "flags")
STATIC_DIR = os.path.join(BASE_DIR, "static/papyrus")

@app.route("/papyrus", methods=["GET", "POST"])
def papyrus():
    requested_file = request.form.get("file", "") if request.method == "POST" else request.args.get("file", "")
    
    if not requested_file:
        return render_template("papyrus.html", hint="Seek the hidden scrolls...", file_list=None, flag=None)
    
    file_path = os.path.normpath(os.path.join(BASE_DIR, requested_file))
    
    if os.path.isdir(file_path):
        try:
            files = os.listdir(file_path)
            hint = "📂 These scrolls are part of the Pharaoh's archives..."
            if "scroll_hint.txt" in files:
                hint += " Perhaps reading 'scroll_hint.txt' will reveal the way?"
            return render_template("papyrus.html", hint=hint, file_list=files, flag=None)
        except Exception as e:
            return render_template("papyrus.html", hint=f"Error listing directory: {e}", file_list=None, flag=None)
    
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
        flag = None
        if "ancient_scroll.txt" in file_path:
            flag = "O24{ancient_path_unlocked_by_the_worthy}"
        return render_template("papyrus.html", content=content, flag=flag)
    except FileNotFoundError:
        return render_template("papyrus.html", hint="📜 The scroll is missing...", flag=None)
    except Exception as e:
        return render_template("papyrus.html", hint=f"Error: {e}", flag=None)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)