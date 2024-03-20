import socket
import os
import datetime
import time
import qrcode

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
            send_string(s, log_data)
            time.sleep(1)  # Add a delay to ensure the receiver has enough time to process

            for file_path in file_paths:
                if os.path.exists(file_path):
                    try:
                        # Send original filename
                        original_filename = os.path.basename(file_path)
                        send_string(s, original_filename)
                        time.sleep(1)  # Add a delay

                        with open(file_path, 'rb') as file:
                            file_data = file.read()

                            # Send file size first
                            send_int(s, len(file_data))
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

            # Generate QR code for the contents
            contents = []
            for file_path in file_paths:
                with open(file_path, 'rb') as file:
                    file_content = file.read().decode('utf-8', errors='replace')
                    contents.append(f"\nFile: {file_path}\n{file_content}")

            qr_code_path = 'qr_code.png'
            generate_qr_code("".join(contents), qr_code_path)
            log_data += f"\n\nQR Code Generated: {qr_code_path}"

        except Exception as e:
            print(f"Error while connecting to {target_ip}:{target_port}: {str(e)}")

    # Log sender information
    with open(log_filename, 'a') as log_file:
        log_file.write("\n\n\n\n")
        log_file.write(log_data + "\n\n: " + ', '.join(os.path.basename(file_path) for file_path in file_paths) + "\n\n")

    print("Files sent successfully.")
    print(f"QR Code generated and saved as '{qr_code_path}'.")

def send_string(socket, data):
    """Send a string over the socket."""
    encoded_data = data.encode('utf-8')
    send_int(socket, len(encoded_data))
    socket.sendall(encoded_data)

def send_int(socket, value):
    """Send an integer over the socket."""
    socket.sendall(value.to_bytes(8, byteorder='big'))

def generate_qr_code(contents, qr_code_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(contents)
    qr.make(fit=True)

    img = qr.make_image(fill_color="yellow", back_color="black")
    img.save(qr_code_path)

if __name__ == "__main__":
    files_to_send = ["de_text_1_encrypted.txt", "de_text_2_encrypted.txt", "de_text_3_encrypted.txt", "log.txt", "passwords.txt"]
    target_ip = "10.0.1.203"
    target_port = 65000

    send_files(files_to_send, target_ip, target_port)
