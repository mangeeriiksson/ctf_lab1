from flask import Blueprint, render_template, Response

bp = Blueprint("bp", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "# Only the seeker knows what lies within forbidden paths...",
        mimetype="text/plain"
    )

@bp.route("/admin/")
def admin():
    return Response(
        "This chamber is no longer guarded.\n"
        "\nSome say old files were archived here… but most are lost to time.",
        mimetype="text/plain"
    )

@bp.route("/admin/flag/")
def flag_folder():
    return Response(
        "📁 One file survived.\n"
        "Its name? Forgotten by many... but not all.",
        mimetype="text/plain"
    )

@bp.route("/admin/flag/oracle-flag.txt")
def flag_file():
    content = (
        "📜 oracle-flag.txt\n"
        "------------------\n"
        "o24{Or4cle_gr4ts_fl46}"
    )
    headers = {
        "Content-Disposition": "inline; filename=oracle-flag.txt"
    }
    return Response(content, mimetype="text/plain", headers=headers)
