import requests
import time
import os
import threading

SERVER_URL = "http://<server_url>:5050"  
FILE_PATH = "file_to_download.txt"
stop_flag = False 

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print("Public IP fetch error:", e)
    return "unknown"

public_ip = get_public_ip()
agent_name = input("Enter agent name: ").strip()
agent_name = f"{agent_name} ({public_ip})"

def ping_server(file_exists):
    try:
        response = requests.post(f"{SERVER_URL}/ping", json={
            "file_exists": file_exists,
            "agent_name": agent_name
        }, timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def upload_file():
    try:
        with open(FILE_PATH, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{SERVER_URL}/upload", files=files, data={"agent_name": agent_name})
            print("[+] File uploaded, response:", response.status_code)
    except Exception as e:
        print("Upload error:", e)

def monitor_server():
    """Main loop that pings server and checks for upload requests"""
    global stop_flag
    connected = False  # Track connection status

    while not stop_flag:
        file_exists = os.path.exists(FILE_PATH)
        success = ping_server(file_exists)

        if success:
            if not connected:
                print(f"[✓] Connected to server as {agent_name}")
                connected = True
        else:
            if connected:
                print("[x] Lost connection to server.")
                connected = False

        if success:
            try:
                response = requests.get(f"{SERVER_URL}/ping_status", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("upload_requested", False):
                        print("[!] Server requested file upload.")
                        if file_exists:
                            upload_file()
                        else:
                            print("[-] file.txt not found.")
            except Exception as e:
                print("Status check error:", e)

        time.sleep(5) 

def listen_for_stop():
    """Separate thread to wait for stop command"""
    global stop_flag
    while True:
        cmd = input("\nType 'stop' to terminate agent: ").strip().lower()
        if cmd == "stop":
            stop_flag = True
            print("[!] Stopping agent...")
            break

if __name__ == "__main__":
    print(f"\n--- Agent Started ({agent_name}) ---")
    print(f"Connecting to server at {SERVER_URL}...\n")

    # Run the monitor in a separate thread
    monitor_thread = threading.Thread(target=monitor_server)
    monitor_thread.start()

    # Listen for user stop command
    time.sleep(1)
    listen_for_stop()

    # Wait for thread to finish
    monitor_thread.join()
    print("[✓] Agent stopped cleanly.")
