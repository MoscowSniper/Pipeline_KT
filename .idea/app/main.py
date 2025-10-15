from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Hello from your CI/CD pipeline!"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
@app.route("/version")
def version():
    try:
        with open("version.txt") as f:
            version = f.read().strip()
    except FileNotFoundError:
        version = "unknown"
    return jsonify({"version": version})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)