from flask import Flask, request, render_template, session
import os
import pickle
import base64

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "indiana_jones_secret"

FLAGS_DIR = "flags"
FLAG_FILE = os.path.join(FLAGS_DIR, "soul_of_osiris.txt")

# Skapa flaggfilen om den inte finns
os.makedirs(FLAGS_DIR, exist_ok=True)
if not os.path.exists(FLAG_FILE):
    with open(FLAG_FILE, "w") as f:
        f.write("O24{spirit_of_osiris_unleashed}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/canopic_jar", methods=["GET", "POST"])
def canopic_jar():
    result = None
    hint = None

    if request.method == "POST":
        serialized_data = request.form.get("jar", "")
        try:
            decoded_data = base64.b64decode(serialized_data)
            deserialized_object = pickle.loads(decoded_data)

            # Om objektet innehåller "get_flag", visa flaggan istället för objektet
            if "get_flag" in str(deserialized_object):
                with open(FLAG_FILE, "r") as f:
                    result = f.read().strip()
            else:
                result = f"📜 The Jars Speak... {deserialized_object}"
        
        except Exception as e:
            result = f"⚠️ Error processing the offering: {e}"

    # 🔍 Hint-system
    if request.args.get("hint"):
        hint = """🏺 Deep within the crypts of Osiris, the scribes of old sealed their secrets inside objects of power. 
        Only those who can forge an artifact of their own shall gain the favor of the gods.

        The priests whisper of a forgotten art—binding knowledge within an offering. 
        One must inscribe the right symbols in the language of the mystics... then encode it in the sacred script before presenting it to the jar.

        Could it be that the answer lies within the very foundation of this world... 
        a construct shaped by those who call upon the power of 'pickle'?"""

    return render_template("canopic_jar.html", result=result, hint=hint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
