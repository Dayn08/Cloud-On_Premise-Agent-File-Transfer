# Cloud to On-Premise Agent File Transfer
This project demonstrates a cloud-hosted server and multiple on-premise clients (agents) communicating securely through HTTP. The server can trigger file downloads from any connected client on demand, even if clients are behind NAT or not publicly accessible.


## 🏗️ Architecture Overview

1. **Client (On-premise)**  
   - Connects to the cloud server.
   - Waits for file download requests.
   - Sends file data to the server when requested.

2. **Server (Cloud-hosted)**  
   - Accepts client connections.
   - Initiates file download through an API call.
   - Saves received files locally inside the `upload/` directory.

     
## 🗂 Project Structure
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
Run this on cloud-hosted
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
Open and modify agent.py and update the server URL to point to your cloud server.

<img width="426" height="157" alt="image" src="https://github.com/user-attachments/assets/bfce6afa-effc-4ede-8132-28080dda5e85" />

Replace <server_url> with your actual server IP or domain.
The default port is 5050, but you can modify it in server/server.py if needed.

Now, start the client:
```
python agent.py
```
The terminal will prompt to enter the Agent Name (On-premise's Name).

Expected output example:

<img width="611" height="178" alt="image" src="https://github.com/user-attachments/assets/c0478603-1bc6-4b84-ac14-006088bb48df" />

Once connected, the client maintains a live connection to the server and waits for download requests.


### 4️⃣ Trigger File Download (from Server)
The server terminal shows all connected clients.
You can choose a specific client to download the file via API.

After a request is made:

The selected client sends its file_to_download.txt to the server.

The server saves the file inside the upload/ folder.

Example of the process in action:

<img width="1411" height="268" alt="image" src="https://github.com/user-attachments/assets/490155e0-acbe-4166-9cc6-28e70d77c94e" />


## 🧑‍💻 Author
Developed by Muhammad Nizmuddin

© 2025 All rights reserved.
