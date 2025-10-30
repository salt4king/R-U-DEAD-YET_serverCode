# Client.py
import os
import time
import random
import threading
from time import sleep
import requests

# ============ Configuration ============
SERVER_IP_ADDRESS = os.getenv("SERVER_IP_ADDRESS", "127.0.0.1")
SERVER_PORT = 5000

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A705FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 7.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0; Nexus 6P Build/OPR6.170623.013) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-J600G Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
]

# gets the full URL for an endpoint
def get_url(endpoint):
    return f"http://{SERVER_IP_ADDRESS}:{SERVER_PORT}{endpoint}"


# regular POST request targeting the endpoints 1, 2, and 3
def make_regular_request():
    for endpoint in ['/endpoint-1', '/endpoint-2', '/endpoint-3']:
        url = get_url(endpoint)
        headers = {"User-Agent": random.choice(user_agents)}
        try:
            requests.post(url, json={"compromised": False}, headers=headers)
        except requests.RequestException as e:
            print(f"Regular request to {endpoint} failed: {e}")


# slow user requests targeting the "/" endpoint
def make_slow_request():
    url = get_url('/')
    headers = {"User-Agent": random.choice(user_agents)}
    for _ in range(5):
        try:
            requests.post(
                url,
                json={"compromised": False, "slow": True},
                params={"data_size": 600},
                headers=headers
            )
            sleep(random.uniform(0.5, 1.5))  # delay to simulate slow connection
        except requests.RequestException as e:
            print(f"Slow request to {url} failed: {e}")


# RUDY attack on the /rudy-endpoint keeping connection open with small packets
def make_rudy_attack():
    url = get_url('/rudy-endpoint')
    headers = {"User-Agent": random.choice(user_agents)}
    data = "data=" + "A" * 10000  # large data payload to keep connection open
    try:
        # send initial request with the payload and simulate delay
        with requests.post(url, data=data, headers=headers, stream=True, timeout=5) as response:
            if response.status_code == 200:
                print("RUDY attack request successful.")
            else:
                print(f"RUDY attack received unexpected status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"RUDY attack failed: {e}")


# function to simulate multiple regular users
def run_regular_users(num_users, duration):
    threads = []
    for _ in range(num_users):
        t = threading.Thread(target=simulate_regular_user, args=(duration,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


# function to simulate multiple slow users
def run_slow_users(num_users, duration):
    threads = []
    for _ in range(num_users):
        t = threading.Thread(target=simulate_slow_user, args=(duration,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


# function to simulate multiple RUDY attackers
def run_rudy_attackers(num_attackers, duration):
    threads = []
    for _ in range(num_attackers):
        t = threading.Thread(target=simulate_rudy_attack, args=(duration,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


# helper function to simulate regular user over a duration
def simulate_regular_user(duration):
    start = time.time()
    while time.time() - start < duration:
        make_regular_request()
        sleep(random.uniform(2, 5))


# helper function to simulate slow user over a duration
def simulate_slow_user(duration):
    start = time.time()
    while time.time() - start < duration:
        make_slow_request()
        sleep(random.uniform(3, 5))


# helper function to simulate RUDY attack over a duration
def simulate_rudy_attack(duration):
    start = time.time()
    while time.time() - start < duration:
        make_rudy_attack()
        sleep(1)


# runs simulations
if __name__ == "__main__":
    duration = 120  # Total duration for the simulation in seconds
    num_regular_users = 15
    num_slow_users = 8
    num_rudy_attackers = 7

    # start regular and slow users
    threading.Thread(target=run_regular_users, args=(num_regular_users, duration)).start()  # 15 regular users
    threading.Thread(target=run_slow_users, args=(num_slow_users, duration)).start()  # 8 slow users

    # wait for 30 seconds before starting RUDY attackers
    time.sleep(30)

    # simulate RUDY attackers starting
    threading.Thread(target=run_rudy_attackers, args=(num_rudy_attackers, duration - 30)).start()  # 7 RUDY attackers

    # simulate 5 regular or slow users stopping when RUDY attackers appear
    for _ in range(5):
        stop_random_user()  # function to stop a random user (either regular or slow)
        time.sleep(1)
