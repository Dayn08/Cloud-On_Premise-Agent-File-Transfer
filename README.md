# Cloud On-Premise Agent File Transfer
This project demonstrates a cloud-hosted server and multiple on-premise clients (agents) communicating securely through HTTP. The server can trigger file downloads from any connected client on demand, even if clients are behind NAT or not publicly accessible.

## 🏗️ Architecture Overview

1. **Client (On-premise)**  
   - Connects to the cloud server.
   - Waits for file download requests.
   - Sends file data to the server when requested.

2. **Server (Cloud-hosted)**  
   - Accepts client connections.
   - Initiates file download through API or CLI.
   - Saves received files locally.
   - 
## Project Structure
```
Cloud-On_Premise-Agent-File-Transfer/
│
├── server/
│   ├── server.py
│   ├── requirements.txt
│   └── upload/                # Folder where files from clients are saved
│
└── client/
    ├── agent.py
    ├── file_to_download.txt   # The example file each client holds
    └── requirements.txt
```

## 🚀 How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Dayn08/Cloud-On_Premise-Agent-File-Transfer.git
cd Cloud-On_Premise-Agent-File-Transfer
```
### 2️⃣ Setup the Server (server/ in cloud-hosted server on Linux OS)
```
cd server/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```
When run the code, the terminal output will look similar to the example below:
<img width="855" height="171" alt="image" src="https://github.com/user-attachments/assets/2718cdab-ac48-45cd-b836-0748b96f1ac6" />

### 3️⃣ Setup the Client (client_on-premise/ in client computer Linux/Windows)
```
cd client_on-premise/
python -m pip install -r requirements.txt
```
Modify agent.py to put the url link of cloud server

<img width="426" height="157" alt="image" src="https://github.com/user-attachments/assets/bfce6afa-effc-4ede-8132-28080dda5e85" />

Change <server_url> to target cloud server (Using port 5050 on server, can modify the port in script /server/server.py)

```
python agent.py
```
The terminal output will look similar to the example below:

<img width="611" height="178" alt="image" src="https://github.com/user-attachments/assets/c0478603-1bc6-4b84-ac14-006088bb48df" />

Once connected, the client maintains a live connection to the server and waits for download requests.

### 4️⃣ Trigger File Download (from Server)


