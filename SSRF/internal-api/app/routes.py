from flask import Blueprint, render_template

bp = Blueprint("bp", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/admin/")
def admin_home():
    return render_template("admin.html")

@bp.route("/admin/scrolls/73/prophecy")
def flag():
    return render_template("prophecy.html", flag="o24{Or4cle_gr4ts_fl46}")

@bp.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /admin/scrolls/", 200, {"Content-Type": "text/plain"}
