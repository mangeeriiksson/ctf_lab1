from flask import Flask, request, render_template
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "indiana_jones_secret"

BASE_DIR = "/var/www/html"  # Spelaren kan navigera härifrån
FAKE_FLAGS_DIR = "/var/www/html/flags"
SECURE_FLAG_PATH = "/root/flags/true_flag.txt"

# Skapa falska flaggor
FAKE_FLAGS = {
    "/var/www/html/flags/fake_scroll.txt": "O24{this_is_not_the_real_flag}",
    "/var/www/html/flags/cursed_tablet.txt": "O24{so_close_but_not_it}"
}
for path, content in FAKE_FLAGS.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/papyrus", methods=["GET", "POST"])
def papyrus():
    requested_file = request.form.get("file", "") if request.method == "POST" else request.args.get("file", "")

    if not requested_file:
        return render_template("papyrus.html", file_list=None, flag=None)

    # Path traversal från BASE_DIR
    file_path = os.path.abspath(os.path.join(BASE_DIR, requested_file))

    # 🔍 Logga sökvägen som spelaren försöker nå
    print(f"🔍 Requested path: {file_path}")

    # Om det är en katalog, lista innehållet
    if os.path.isdir(file_path):
        try:
            files = os.listdir(file_path)
            file_list = "<br>".join(files)  # Ingen länkning, endast text
            hint = f"📂 Contents:<br>{file_list}"
            return render_template("papyrus.html", hint=hint, file_list=files, flag=None)

        except PermissionError:
            return render_template("papyrus.html", hint="🚫 You don't have permission to access this directory.", file_list=None, flag=None)
        except Exception as e:
            return render_template("papyrus.html", hint=f"❌ Error listing directory: {e}", file_list=None, flag=None)

    try:
        # Om spelaren försöker läsa en falsk flagga
        if file_path in FAKE_FLAGS.keys():
            return render_template("papyrus.html", content=FAKE_FLAGS[file_path], flag=None)
        
        # Om spelaren skriver in rätt path till den riktiga flaggan
        if file_path == SECURE_FLAG_PATH:
            with open(SECURE_FLAG_PATH, "r") as f:
                flag = f.read().strip()
            return render_template("papyrus.html", content=flag, flag=flag)

        # Läs andra filer
        with open(file_path, "r") as f:
            content = f.read().strip()
        return render_template("papyrus.html", content=content, flag=None)

    except FileNotFoundError:
        return render_template("papyrus.html", hint="📜 The file is missing...", flag=None)
    except IsADirectoryError:
        return render_template("papyrus.html", hint="📂 This is a directory. Try listing its contents.", flag=None)
    except PermissionError:
        return render_template("papyrus.html", hint="🚫 You don't have permission to access this file.", flag=None)
    except Exception as e:
        return render_template("papyrus.html", hint=f"❌ Error: {e}", flag=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
