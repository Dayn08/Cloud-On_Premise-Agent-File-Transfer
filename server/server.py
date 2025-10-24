import threading
from flask import Flask, request
from datetime import datetime, timedelta
import os, time, glob
import logging

# Redirect Flask (werkzeug) logs to a file
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)  # You can use ERROR to log only errors
file_handler = logging.FileHandler('./flask_temp.log')
log.addHandler(file_handler)

app = Flask(__name__)
AGENT_TIMEOUT = timedelta(minutes=2)
agents = {}
UPLOAD_FOLDER = "./upload/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask route to receive agent pings
@app.route('/ping', methods=['POST'])
def ping():
    agent_id = request.remote_addr
    file_exists = request.json.get("file_exists", False)
    agent_name = request.json.get("agent_name", agent_id)  # fallback to IP

    if agent_id not in agents:
        agents[agent_id] = {
            "last_seen": datetime.now(),
            "file_exists": file_exists,
            "upload_requested": False,
            "agent_name": agent_name
        }
    else:
        agents[agent_id]["last_seen"] = datetime.now()
        agents[agent_id]["file_exists"] = file_exists
        agents[agent_id]["agent_name"] = agent_name

    return {"status": "pong"}, 200

@app.route('/ping_status', methods=['GET'])
def ping_status():
    agent_id = request.remote_addr
    info = agents.get(agent_id, {})
    return {"upload_requested": info.get("upload_requested", False)}

# Flask route to receive file upload
@app.route('/upload', methods=['POST'])
def upload():
    agent_id = request.remote_addr
    agent_name = request.form.get("agent_name", agent_id)
    if 'file' in request.files:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{agent_name}_{date_str}.txt"
        full_path = os.path.join(UPLOAD_FOLDER, filename)
        request.files['file'].save(full_path)

        print(f"[+] Received file from {agent_name} ({agent_id}), saved to {full_path}")

        # Reset upload request
        if agent_id in agents:
            agents[agent_id]["upload_requested"] = False

        return {"status": "uploaded"}, 200
    return {"error": "No file"}, 400

# Background thread to run Flask server
def run_server():
    app.run(host='0.0.0.0', port=5050)

# CLI loop
def cli_loop():
    while True:
        os.system('clear')
        print("=== Agent Monitor ===")
        now = datetime.now()
        active_agents = {
            aid: info for aid, info in agents.items()
            if now - info["last_seen"] < AGENT_TIMEOUT
        }

        for i, (aid, info) in enumerate(active_agents.items(), start=1):
            print(f"{i}. {info['agent_name']}@({aid}) - file_to_download.txt exists: {info['file_exists']}")

        print("\nOptions:")
        print("  0 - Refresh")
        print("  [number] - Request file upload from agent")
        print("  q - Quit")

        choice = input("> ").strip()
        if choice.lower() == 'q':
            break
        elif choice == '0':
            continue  # Just refresh
        else:
            try:
                index = int(choice) - 1
                agent_ip = list(active_agents.keys())[index]
                agents[agent_ip]["upload_requested"] = True
                print(f"[!] Upload requested from {agent_ip}")

                agent_name = agents[agent_ip]["agent_name"]
                pattern = os.path.join(UPLOAD_FOLDER, f"{agent_name}_*.txt")

                print("[*] Waiting for agent to finish upload...")

                timeout = 90
                start_time = time.time()
                uploaded = False

                while time.time() - start_time < timeout:
                    matching_files = glob.glob(pattern)
                    if matching_files:
                        latest_file = max(matching_files, key=os.path.getctime)
                        uploaded = True
                        break
                    time.sleep(1)

                if not uploaded:
                    print("[-] Still waiting... file not uploaded yet.")

                input("Press Enter after File uploaded successfull...Taking a moment depends on the file size\n")

            except (ValueError, IndexError):
                print("Invalid choice.")
                input("Press Enter to continue...")

# Start server and CLI
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    cli_loop()
