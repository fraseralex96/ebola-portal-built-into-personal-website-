from flask import Flask, render_template
from ebola_portal.app import ebola
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# url_prefix means every route inside portal_bp is reachable under /portal-name/...
# e.g. portal_bp's "/" route becomes "/portal-name/"
app.register_blueprint(ebola, url_prefix="/ebola_portal")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)