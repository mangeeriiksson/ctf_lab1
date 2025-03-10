from flask import Flask, request, render_template, session
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "indiana_jones_secret"

BASE_DIR = "/var/www/html"
FALSE_FLAGS_DIR = os.path.join(BASE_DIR, "flags")  # 🎭 Här ligger falska flaggor
TRUE_FLAGS_DIR = "/root/flags"  # 🔥 Den riktiga flaggan finns här!

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/papyrus", methods=["GET", "POST"])
def papyrus():
    requested_file = request.form.get("file", "") if request.method == "POST" else request.args.get("file", "")

    if not requested_file:
        return render_template("papyrus.html", hint="Seek the hidden scrolls...", file_list=None, flag=None)

    file_path = os.path.normpath(os.path.join(BASE_DIR, requested_file))

    # 🎭 Om spelaren listar /flags först, de hittar endast falska flaggor
    if os.path.isdir(file_path):
        try:
            files = os.listdir(file_path)
            hint = "📂 These scrolls are part of the Pharaoh's archives..."
            if "fake_scroll_1.txt" in files:
                hint += " Perhaps reading 'fake_scroll_1.txt' will reveal the way?"
            return render_template("papyrus.html", hint=hint, file_list=files, flag=None)
        except Exception as e:
            return render_template("papyrus.html", hint=f"Error listing directory: {e}", file_list=None, flag=None)

    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
        
        flag = None

        # 🎭 Om spelaren läser en falsk flagga → Aktivera GUDARNAS VREDE!
        if "fake_scroll" in file_path:
            return render_template(
                "papyrus.html", 
                content="⚡ THE GODS ARE DISPLEASED! ⚡",
                hint="📜 A dark presence fills the air... You feel a powerful force rejecting your actions...",
                flag=None
            )

        # 🔥 Om spelaren hittar den riktiga flaggan i /root/flags
        if os.path.abspath(file_path) == os.path.join(TRUE_FLAGS_DIR, "ancient_scroll.txt"):
            flag = "O24{the_true_treasure_is_buried_deep}"

        return render_template("papyrus.html", content=content, flag=flag)

    except FileNotFoundError:
        return render_template("papyrus.html", hint="📜 The scroll is missing...", flag=None)
    except Exception as e:
        return render_template("papyrus.html", hint=f"Error: {e}", flag=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
