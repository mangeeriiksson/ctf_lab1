from flask import Flask, request, render_template
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "indiana_jones_secret"

BASE_DIR = "/"  # Gör att användaren kan navigera från root
FAKE_FLAGS_DIR = "/var/www/html/flags"
SECURE_FLAG_PATH = "/root/flags/true_flag.txt"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/papyrus", methods=["GET", "POST"])
def papyrus():
    requested_file = request.form.get("file", "") if request.method == "POST" else request.args.get("file", "")

    if not requested_file:
        return render_template("papyrus.html", file_list=None, flag=None)

    # Path traversal från root istället för /var/www/html
    file_path = os.path.abspath(os.path.join("/", requested_file))

    # 🔍 Logga sökvägen som spelaren försöker nå
    print(f"🔍 Requested path: {file_path}")

    # Om det är en katalog, lista innehållet
    if os.path.isdir(file_path):
        try:
            files = os.listdir(file_path)
            file_links = [f"<a href='/papyrus?file={requested_file}/{file}'>{file}</a>" for file in files]
            hint = f"📂 Contents:<br>{'<br>'.join(file_links)}"
            return render_template("papyrus.html", hint=hint, file_list=files, flag=None)

        except PermissionError:
            return render_template("papyrus.html", hint="🚫 You don't have permission to access this directory.", file_list=None, flag=None)

        except Exception as e:
            return render_template("papyrus.html", hint=f"❌ Error listing directory: {e}", file_list=None, flag=None)

    try:
        # Läs filens innehåll
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
