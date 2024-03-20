import socket
import os
import datetime
import time

def send_files(file_paths, target_ip, target_port):
    # Set up logging configuration
    log_filename = 'log.txt'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((target_ip, target_port))
            print("Connected to:", s.getpeername())

            # Get the sender's IP address
            sender_ip = socket.gethostbyname(socket.gethostname())

            # Register the current date and time
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Combine the data into a string
            log_data = f"Sender IP: {sender_ip}\nReceiver IP: {target_ip}\nDate and time: {formatted_datetime}"

            # Send sender information
            s.sendall(log_data.encode('utf-8'))
            time.sleep(1)  # Add a delay to ensure the receiver has enough time to process

            for file_path in file_paths:
                if os.path.exists(file_path):
                    try:
                        # Send original filename
                        original_filename = os.path.basename(file_path)
                        s.sendall(original_filename.encode('utf-8'))
                        time.sleep(1)  # Add a delay

                        with open(file_path, 'rb') as file:
                            file_data = file.read()

                            # Send file size first
                            s.sendall(len(file_data).to_bytes(8, byteorder='big'))
                            time.sleep(1)  # Add a delay

                            # Send file data with a larger buffer size
                            buffer_size = 4096
                            for i in range(0, len(file_data), buffer_size):
                                s.sendall(file_data[i:i + buffer_size])
                                time.sleep(0.1)  # Add a small delay

                            time.sleep(1)  # Add an additional delay

                            # Update log data to include sent file information
                            log_data += f"\nSent File: {original_filename}, Size: {len(file_data)} bytes"

                    except Exception as e:
                        print(f"Error while sending {file_path}: {str(e)}")
                else:
                    print(f"File not found: {file_path}")

        except Exception as e:
            print(f"Error while connecting to {target_ip}:{target_port}: {str(e)}")

    # Log sender information
    with open(log_filename, 'a') as log_file:
        log_file.write(log_data + "\n\nFiles Sent: " + ', '.join(os.path.basename(file_path) for file_path in file_paths) + "\n\n")

    print("Files sent successfully.")

if __name__ == "__main__":
    files_to_send = ["nl_text_1_encrypted.txt", "nl_text_2_encrypted.txt", "nl_text_3_encrypted.txt", "log.txt", "passwords.txt"]
    target_ip = "10.0.1.207"
    target_port = 65000

    send_files(files_to_send, target_ip, target_port)
