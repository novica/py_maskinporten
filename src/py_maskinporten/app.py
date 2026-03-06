from flask import Flask, jsonify, render_template, request
from py_maskinporten.config import load_config, default_config
from py_maskinporten.request_token import request_maskinporten_token
from dotenv import load_dotenv

# Configure application
app = Flask(__name__)

# Load environment variables from .env file if it exists
load_dotenv()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    selected_env = None
    issuer_url = None
    config_error = None
    config = None

    try:
        config = load_config()
    except RuntimeError as e:
        config_error = str(e)

    if request.method == "POST":
        selected_env = request.form.get("environment")
        if selected_env == "prod":
            issuer_url = default_config["PROD_MASKINPORTEN_ISSUER"]
        elif selected_env == "test" or selected_env is None:
            issuer_url = default_config["TEST_MASKINPORTEN_ISSUER"]

    return render_template(
        "index.html",
        selected_env=selected_env,
        issuer_url=issuer_url,
        config=config,
        config_error=config_error,
    )


@app.route("/token")
def get_token():

    # reads ?env=test or ?env=prod
    env = request.args.get("env")

    if env is None:
        env = "test"

    try:
        access_token, expires_in = request_maskinporten_token(api_env=env)
        return jsonify({"access_token": access_token, "expires_in": expires_in})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
