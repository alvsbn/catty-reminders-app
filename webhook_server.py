from flask import Flask, request
from flask import jsonify
import subprocess
import os

app = Flask(__name__)

PORT = 8080
APP_DIR = "/home/sabina/catty-reminders-app"
APP_SERVICE = "catty-app"

@app.route('/', methods=['GET', 'POST'])
def handle():
    if request.method == 'GET':
        return jsonify({"message": "Webhook handler running"}), 200
    
    if request.headers.get('X-GitHub-Event') == 'push':
        print("Starting deployment...")
        
        subprocess.run(["git", "-C", APP_DIR, "pull"], check=True)
        print("Code updated")
        
        subprocess.run(["pip3", "install", "--break-system-packages", "-r", 
                       os.path.join(APP_DIR, "requirements.txt")], check=True)
        print("Dependencies installed")
        
        result = subprocess.run(["python3", "-m", "pytest", APP_DIR])
        if result.returncode != 0:
            print("Tests failed")
            return jsonify({"error": "Tests failed"}), 500
        print("Tests passed")
        
        subprocess.run(["sudo", "systemctl", "restart", APP_SERVICE], check=True)
        print("Service restarted")
        
        return jsonify({"message": "Deployment completed"}), 200
        
    return jsonify({"message": "Not a push event"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
