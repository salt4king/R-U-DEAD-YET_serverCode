

# 5) Fixed `Server.py` (clean, indented, safer, graceful shutdown)
#Copy this into `Server.py` 

from flask import Flask, request
import pandas as pd
import time
import os
import random
from queue import Queue, Empty
import threading
import signal
import sys

app = Flask(__name__)

# queue to store data
data_queue = Queue()
columns = ['ip', 'endpoint', 'data_size', 'headers', 'time', 'time_taken', 'is_slow', 'compromised']
data = pd.DataFrame(columns=columns)

# pick next available filename
i = 0
filename = f"rudy_data_{i}.csv"
while os.path.exists(filename):
    i += 1
    filename = f"rudy_data_{i}.csv"

# function to generate a random IP address
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# route configuration for different endpoints with ranges
route_data = {
    "/": {"packet_size": [20.0, 100.0], "time_taken": [0.25, 1.5]},
    "/endpoint-1": {"packet_size": [20.0, 100.0], "time_taken": [0.25, 1.0]},
    "/endpoint-2": {"packet_size": [110.0, 200.0], "time_taken": [0.01, 0.1]},
    "/endpoint-3": {"packet_size": [200.0, 300.0], "time_taken": [0.05, 0.2]},
    "/rudy-endpoint": {"packet_size": [10.0, 50.0], "time_taken": [0.7, 3.0]},
}

# initialize a request counter and lock
request_counter = 0
counter_lock = threading.Lock()

@app.before_request
def log_request_info():
    global request_counter
    # only log known test endpoints
    if request.path not in route_data:
        return

    # safely increment the counter
    with counter_lock:
        request_counter += 1
        local_counter = request_counter

    req_data = route_data[request.path]

    # determines if this request is slow or compromised
    data_size_str = request.args.get('data_size')
    try:
        data_size_val = float(data_size_str) if data_size_str is not None else None
    except (ValueError, TypeError):
        data_size_val = None

    is_slow = (data_size_val is not None) and (data_size_val > req_data["packet_size"][1])
    compromised = (request.path == "/rudy-endpoint")

    # generates normal packet size and time taken values
    packet_size = random.uniform(req_data["packet_size"][0], req_data["packet_size"][1])
    time_taken = random.uniform(req_data["time_taken"][0], req_data["time_taken"][1])

    # makes an outlier every 15-25 requests (random interval)
    # note: using the local_counter value ensures consistent behavior inside this call
    if local_counter % random.randint(15, 25) == 0:
        outlier_type = random.choice(['high', 'low'])
        if outlier_type == 'high':
            outlier_multiplier = random.uniform(1.01, 1.5)
        else:
            outlier_multiplier = random.uniform(0.5, 0.99)

        if random.choice(['packet_size', 'time_taken']) == 'packet_size':
            if outlier_type == 'high':
                packet_size = req_data["packet_size"][1] * outlier_multiplier
            else:
                packet_size = req_data["packet_size"][0] * outlier_multiplier
        else:
            if outlier_type == 'high':
                time_taken = req_data["time_taken"][1] * outlier_multiplier
            else:
                time_taken = req_data["time_taken"][0] * outlier_multiplier

        print(f"Outlier generated on request {local_counter}: "
              f"type={outlier_type}, packet_size={packet_size:.2f}, time_taken={time_taken:.2f}")

    # random IP address
    random_ip = generate_random_ip()

    # queue the data for logging
    data_queue.put([
        random_ip,
        request.path,
        packet_size,
        dict(request.headers),
        time.time(),
        time_taken,
        is_slow,
        compromised
    ])

@app.route('/', methods=['POST'])
def index():
    return 'Received slow request'

@app.route('/endpoint-1', methods=['POST'])
def endpoint_1():
    return 'Received normal request1'

@app.route('/endpoint-2', methods=['POST'])
def endpoint_2():
    return 'Received normal request2'

@app.route('/endpoint-3', methods=['POST'])
def endpoint_3():
    return 'Received normal request3'

@app.route('/rudy-endpoint', methods=['POST'])
def rudy_endpoint():
    print("RUDY attack received")
    return 'Received RUDY attack'

# background thread: drain the queue and append to CSV regularly
stop_event = threading.Event()

def save_logs():
    global data
    while not stop_event.is_set():
        time.sleep(1)
        res = []
        while not data_queue.empty():
            try:
                new_data = data_queue.get(timeout=0.1)
                res.append(new_data)
                data_queue.task_done()
            except Empty:
                break

        if res:
            res_df = pd.DataFrame.from_records(res, columns=columns)
            # append to main DataFrame in memory (optional) and persist to CSV
            data = pd.concat([data, res_df], ignore_index=True)
            try:
                data.to_csv(filename, index=False)
            except Exception as e:
                print("Error writing CSV:", e)

def _graceful_shutdown(signum, frame):
    print("\nShutting down: flushing queue to disk...")
    stop_event.set()
    # give the save_logs thread a moment to flush
    time.sleep(1.5)
    # final drain
    res = []
    while not data_queue.empty():
        try:
            new_data = data_queue.get_nowait()
            res.append(new_data)
            data_queue.task_done()
        except Exception:
            break
    if res:
        res_df = pd.DataFrame.from_records(res, columns=columns)
        try:
            # read any existing file and append or write new
            if os.path.exists(filename):
                existing = pd.read_csv(filename)
                combined = pd.concat([existing, res_df], ignore_index=True)
                combined.to_csv(filename, index=False)
            else:
                res_df.to_csv(filename, index=False)
        except Exception as e:
            print("Error during final CSV write:", e)
    print("Done. Exiting.")
    sys.exit(0)

if __name__ == "__main__":
    # register signal handlers for graceful exit (Ctrl+C)
    signal.signal(signal.SIGINT, _graceful_shutdown)
    signal.signal(signal.SIGTERM, _graceful_shutdown)

    saver = threading.Thread(target=save_logs, daemon=True)
    saver.start()

    # run Flask
    app.run(host='0.0.0.0', port=5000)
