
import os
from flask import Flask, render_template, request
from netmiko import ConnectHandler
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None

    if request.method == "POST":
        router_device = {
            "device_type": "cisco_ios_telnet",
            "ip": os.getenv("ROUTER_IP"),
            "port": int(os.getenv("ROUTER_PORT", "32770")),
            "username": os.getenv("ROUTER_USERNAME"),
            "password": os.getenv("ROUTER_PASSWORD"),
            "secret": os.getenv("ROUTER_SECRET"),
        }

        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]

        net_connect = None

        try:
            net_connect = ConnectHandler(**router_device)
            net_connect.enable()

            for cmd in commands_to_run:
                output = net_connect.send_command(cmd)
                results[cmd] = output

        except Exception as e:
            error = f"Connection failed: {e}"

        finally:
            if net_connect:
                net_connect.disconnect()

    return render_template(
        "index.html",
        results=results,
        error=error
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
