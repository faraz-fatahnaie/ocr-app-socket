import binascii
import socket
import json
import os
import base64


def start_server(ip, port, output_file):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_address = (ip, port)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Listening for connections on {ip}:{port}")

    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()

        try:
            print(f"Connection from {client_address}")

            # Set a timeout for the connection to prevent blocking indefinitely
            connection.settimeout(10.0)  # Timeout after 5 seconds

            # Receive the data in small chunks and assemble it
            data = b""
            while True:
                try:
                    chunk = connection.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                    print(f"Received chunk: {chunk}")
                except socket.timeout:
                    print("Socket timeout, no data received.")
                    break

            # Check if any data was received
            if not data:
                print("No data received.")
                continue

            # Attempt to decode the data
            try:
                data_str = data.decode('utf-8')
                print(f"Received data: {data_str}")

                # Optionally, deserialize the string back into a dictionary
                try:
                    received_dict = json.loads(data_str)
                    print("Received dictionary:", received_dict)

                    # Extract and decode the base64 image data
                    image_base64 = received_dict.get('image', '')
                    print(image_base64)
                    if image_base64:
                        print(f"Base64 image data length: {len(image_base64)}")
                        #
                        # # Fix padding if necessary
                        # padding_needed = len(image_base64) % 4
                        # if padding_needed:
                        #     image_base64 += '=' * (4 - padding_needed)

                        try:
                            image = base64.b64decode(image_base64, validate=True)
                            file_to_save = ".\\retrieve_image.jpg"
                            with open(file_to_save, "wb") as f:
                                f.write(image)
                        except binascii.Error as e:
                            print(e)

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

                # Save the received data to a .json file
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(data_str)
                    print(f"Data saved to {output_file}")

            except UnicodeDecodeError as e:
                print(f"Error decoding data: {e}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__":
    # Output file where the received JSON data will be saved
    output_file = 'C:\\Users\\faraz\\Documents\\socket-handler\\received_data.json'

    # Ensure the output directory exists, if any
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    start_server('192.168.1.34', 1234, output_file)
