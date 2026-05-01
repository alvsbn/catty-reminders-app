from flask import Flask, request
from flask import jsonify
import subprocess
import os

app = Flask(__name__)

PORT = 8080
APP_DIR = "/home/sabina/catty-reminders-app"
APP_SERVICE = "catty-app"
ENV_FILE = "/home/sabina/catty-reminders-app/.env"

@app.route('/', methods=['GET', 'POST'])
def handle():
    if request.method == 'GET':
        return jsonify({"message": "Webhook handler running"}), 200
    
    if request.headers.get('X-GitHub-Event') == 'push':
        print("Starting deployment...")
        
        subprocess.run(["git", "-C", APP_DIR, "pull"], check=True)
        print("Code updated")
        
        sha = subprocess.check_output(["git", "-C", APP_DIR, "rev-parse", "HEAD"]).decode().strip()
        
        with open(ENV_FILE, "w") as f:
            f.write(f"DEPLOY_REF={sha}")
        print(f"DEPLOY_REF written: {sha}")
        
        subprocess.run(["sudo", "systemctl", "restart", APP_SERVICE], check=True)
        print("Service restarted")
        
        return jsonify({"message": "Deployment completed"}), 200
        
    return jsonify({"message": "Not a push event"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
