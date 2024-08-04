import socket
import json


def send_dict(ip, port, data_dict):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    try:
        # Serialize dictionary to JSON string
        message = json.dumps(data_dict)
        # Send the JSON string
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent: {message}")
    finally:
        # Close the socket
        client_socket.close()


if __name__ == "__main__":
    data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    send_dict('192.168.1.34', 1234, data)
