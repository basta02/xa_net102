
import os
from dotenv import load_dotenv
from netmiko import ConnectHandler

# Load environment variables
load_dotenv()

# Cisco router connection
router = {
    "device_type": "cisco_ios_telnet",
    "ip": os.getenv("ROUTER_IP"),
    "port": int(os.getenv("ROUTER_PORT", "32770")),
    "username": os.getenv("ROUTER_USERNAME"),
    "password": os.getenv("ROUTER_PASSWORD"),
    "secret": os.getenv("ROUTER_SECRET")
}

# Cisco commands
commands_to_run = [
    "show version",
    "show ip interface brief",
    "show running-config",
    "show ip route"
]

net_connect = None

try:
    print("Connecting to router...")

    net_connect = ConnectHandler(**router)

    net_connect.enable()

    print("Connected successfully!")

    for cmd in commands_to_run:
        print(f"\n--- Output for: {cmd} ---")

        output = net_connect.send_command(cmd)

        print(output)

except Exception as e:
    print(f"Connection failed: {e}")

finally:
    if net_connect:
        net_connect.disconnect()
        print("\nDisconnected successfully.")
