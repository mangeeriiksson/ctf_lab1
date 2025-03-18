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
                result = f"Deserialized object: {deserialized_object}"
        
        except Exception as e:
            result = f"Error processing the offering: {e}"
    
    if request.args.get("hint"):
        hint = "Some objects hold great power... Try creating a special object in Python and serializing it."
    
    return render_template("canopic_jar.html", result=result, hint=hint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6004, debug=True)
