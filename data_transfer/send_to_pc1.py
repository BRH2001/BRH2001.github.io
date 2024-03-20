import socket
import os
import time

def send_files(file_paths, target_ip, target_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((target_ip, target_port))
            print("Connected to:", s.getpeername())

            sender_ip = socket.gethostbyname(socket.gethostname())

            s.sendall(sender_ip.encode('utf-8'))

            num_files = len(file_paths)
            s.sendall(str(num_files).encode('utf-8'))

            for file_path in file_paths:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    s.sendall(filename.encode('utf-8'))

                    file_size = os.path.getsize(file_path)
                    s.sendall(file_size.to_bytes(8, byteorder='big'))

                    with open(file_path, 'rb') as file:
                        while True:
                            data = file.read(4096)
                            if not data:
                                break
                            s.sendall(data)
                            time.sleep(0.1)  # Add a small delay

                    print(f"Sent File: {filename}, Size: {file_size} bytes")
                else:
                    print(f"File not found: {file_path}")

        except Exception as e:
            print(f"Error while connecting to {target_ip}:{target_port}: {str(e)}")

if __name__ == "__main__":
    files_to_send = ["fr_text_1_encrypted.txt", "fr_text_2_encrypted.txt", "fr_text_3_encrypted.txt", "log.txt", "passwords.txt"]
    target_ip = "10.0.1.207"
    target_port = 65000

    send_files(files_to_send, target_ip, target_port)
