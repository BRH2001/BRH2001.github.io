import socket
import os
import datetime
import qrcode

def generate_qr_code(contents, qr_code_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(contents)
    qr.make(fit=True)

    img = qr.make_image(fill_color="green", back_color="black")
    img.save(qr_code_path)

def sanitize_filename(filename):
    # Replace or remove invalid characters in the filename
    return "".join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in filename)

def receive_files(save_path, listen_ip, listen_port):
    # Set up logging configuration
    log_filename = 'log.txt'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((listen_ip, listen_port))
        s.listen()

        print("Listening for incoming connections...")
        conn, addr = s.accept()
        with conn:
            print("Connected to:", addr)

            # Receive sender information
            sender_info = conn.recv(1024).decode('utf-8')
            print("Sender Information:\n", sender_info)

            # Receive files
            while True:
                # Receive original file name
                original_filename = conn.recv(1024).decode('utf-8')
                if not original_filename:
                    break

                # Sanitize the filename to remove invalid characters
                sanitized_filename = sanitize_filename(original_filename)

                # Receive file size
                file_size_bytes = conn.recv(8)
                if not file_size_bytes:
                    break

                file_size = int.from_bytes(file_size_bytes, byteorder='big')

                # Receive file data
                received_data = b''
                buffer_size = 4096
                while len(received_data) < file_size:
                    data = conn.recv(buffer_size)
                    if not data:
                        break
                    received_data += data

                # Save the received file with the sanitized original name
                received_filename = os.path.join(save_path, sanitized_filename)
                with open(received_filename, 'wb') as file:
                    file.write(received_data)

                print(f"Received File: {received_filename}, Size: {file_size} bytes")

            print("File reception completed.")

        # Log receiver information
        with open(log_filename, 'a') as log_file:
            log_file.write("\n\nReceiver Information:\n\n")
            log_file.write(f"Receiver IP: {listen_ip}\nDate and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write("\nFiles Received:\n")
            log_file.write("\n".join(os.listdir(save_path)))

            log_file.write(sender_info)
            log_file.write(f"\nDate and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(", ".join(sender_info.split("\n")[-1].split(":")[-1].strip().split(", ")))

            # Get the contents of all received files
            contents = []
            for file_name in os.listdir(save_path):
                file_path = os.path.join(save_path, file_name)
                with open(file_path, 'rb') as file:
                    file_content = file.read().decode('utf-8', errors='replace')
                    contents.append(f"\nFile: {file_name}\n{file_content}")

            # Generate QR code for the contents
            qr_code_path = os.path.join(save_path, 'qr_code.png')
            generate_qr_code("".join(contents), qr_code_path)
            log_file.write(f"\n\nQR Code Generated: {qr_code_path}")

    print("Files received successfully.")

if __name__ == "__main__":
    save_path = "received_files"
    listen_ip = "10.0.1.203"
    listen_port = 65000

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    receive_files(save_path, listen_ip, listen_port)
