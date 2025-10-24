# Cloud On-Premise Agent File Transfer
This project demonstrates a cloud-hosted server and multiple on-premise clients (agents) communicating securely through HTTP. The server can trigger file downloads from any connected client on demand, even if clients are behind NAT or not publicly accessible.

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

## 🏗️ Architecture Overview

1. **Client (On-premise)**  
   - Connects to the cloud server.
   - Waits for file download requests.
   - Sends file data to the server when requested.

2. **Server (Cloud-hosted)**  
   - Accepts client connections.
   - Initiates file download through API or CLI.
   - Saves received files locally.

## 🚀 How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Dayn08/Cloud-On_Premise-Agent-File-Transfer.git
cd Cloud-On_Premise-Agent-File-Transfer
```
### 2️⃣ Setup the Server (server/ in cloud-hosted server)
```
cd server/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```
When run the code, the terminal output will look similar to the example below:
<img width="855" height="171" alt="image" src="https://github.com/user-attachments/assets/2718cdab-ac48-45cd-b836-0748b96f1ac6" />


