# R-U-DEAD-YET_Sim_Logger

📖 Overview

Rudy-sim-logger is a Python-based client-server simulation project that mimics realistic web traffic patterns, including slow users and simulated R.U.D.Y. (R-U-Dead-Yet) denial-of-service attacks. The server logs requests with metadata (IP, endpoint, headers, packet sizes, and timing) into dynamically named CSV files. The client simulates various user behaviors, such as normal browsing, slow requests, and coordinated R.U.D.Y. attacks.

This project was originally created in 2024 to analyze web traffic patterns and test server resilience under stress.

⚙️ Features
-Flask-based server that logs every request with metadata.
-Simulated user agents and endpoints to mimic realistic browser behavior.
-Automatic generation of slow or compromised traffic patterns.
-CSV logging system with automatic file versioning.
-Client simulation supporting multiple concurrent threads for traffic generation.
Differentiation between regular users, slow users, and R.U.D.Y. attackers.

🚀 Setup and Usage
1. Install Dependencies (See ServerBashExtraction.txt for more info)

Run these commands in an AWS EC2 ubuntu terminal instance:

sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
sudo apt install python3.12-venv
python3 -m venv myenv
source myenv/bin/activate
pip install pandas Flask requests
2. Run the Server
python Server.py

This will start a Flask app on port 5000 and begin logging simulated traffic data to CSV files named rudy_data_0.csv, rudy_data_1.csv, etc.

3. Run the Client

In a separate terminal window (or separate AWS EC2 instance):

source myenv/bin/activate
python Client.py

The client will start sending mixed traffic patterns to the Flask server — including normal, slow, and R.U.D.Y.-style requests.

🧠 How It Works
Server Side 

Receives requests from multiple endpoints (/endpoint-1, /endpoint-2, /endpoint-3, /rudy-endpoint).

Logs key metrics such as IP, data size, headers, and time taken.

Randomly introduces outliers and slow requests for simulation realism.

Writes logged data to CSV in real-time using a background thread.

Client Side 

Simulates users making requests with randomized user-agents.

Supports three main behaviors:

Regular Users: Make requests to standard endpoints.

Slow Users: Send small but delayed packets to simulate poor connections.

R.U.D.Y. Attackers: Simulate denial-of-service by keeping connections open.

Execution Workflow

Example terminal workflow for deployment and data retrieval on AWS:

sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
python3 -m venv myenv && source myenv/bin/activate
pip install pandas Flask requests
nano Server.py  # insert server-side code
nano Client.py  # insert client-side code
python Server.py  # start server
# in another terminal
python Client.py  # run simulation
scp -i ~/Downloads/<aws_keypair> ubuntu@<ec2_public_ip>:~/rudy_data_0.csv ~/Downloads
📊 Example Output

Each simulation produces CSV logs similar to this:

ip	endpoint	data_size	headers	time	time_taken	is_slow	compromised
192.168.1.45	/endpoint-1	54.23	{User-Agent: ...}	1697213942	0.85	False	False
103.24.56.8	/rudy-endpoint	42.56	{User-Agent: ...}	1697213950	2.33	True	True
🧰 Requirements

Python 3.10 or higher

Flask

Pandas

Requests

Install all dependencies:

pip install -r requirements.txt

Example requirements.txt:

Flask>=2.0.0
pandas>=1.3.0
requests>=2.25.0

🔒 Security Disclaimer

This project is intended strictly for educational and research purposes.
Do not deploy or run any simulated attack traffic (including R.U.D.Y.) on external or production systems. Always test in a controlled, isolated environment.

