from flask import Flask, send_file, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download")
def download_file():
    return send_file("static/secrets.enc", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6005, debug=True)
