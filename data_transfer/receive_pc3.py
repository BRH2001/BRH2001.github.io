import datetime
import socket
import os
import qrcode

# This program should be run on pc3

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

def receive_files(save_paths, listen_ip, listen_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ip_address = _extracted_from_receive_files_3(s, listen_ip, listen_port, save_paths)

    # Register the current date and time
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Combine the data into a string
    log_data = f"IP address: {ip_address}\nDate and time: {formatted_datetime}"

    # Write the data to the text file 'log.txt'
    with open('log.txt', 'a') as log_file:
        log_file.write("\n\n log info: \n\n")
        log_file.write(log_data + '\n\n')

    # Generate QR code
    contents = []
    for save_path in save_paths:
        with open(save_path, 'rb') as file:
            file_content = file.read().decode('utf-8', errors='replace')
            contents.append(f"\nFile: {save_path}\n{file_content}")

    qr_code_path = 'qr_code.png'
    generate_qr_code("".join(contents), qr_code_path)

    print("Log data saved in 'log.txt'.")
    print(f"QR Code generated and saved as '{qr_code_path}'.")

def _extracted_from_receive_files_3(s, listen_ip, listen_port, save_paths):
    s.bind((listen_ip, listen_port))
    s.listen()

    print("Waiting for connection...")
    conn, _ = s.accept()
    print("Connection from:", conn.getpeername())  # Added line

    try:
        # Receive file data with a larger buffer size
        buffer_size = 4096
        for save_path in save_paths:
            # Receive file size first
            file_size_bytes = conn.recv(8)
            file_size = int.from_bytes(file_size_bytes, byteorder='big')

            with open(save_path, 'wb') as file:
                received_data = b''
                while len(received_data) < file_size:
                    data = conn.recv(buffer_size)
                    received_data += data

                file.write(received_data)

        print("Files received successfully.")
        print(f"Received file size: {file_size}")

    except Exception as e:
        print(f"Error during file reception: {e}")
    finally:
        conn.close()

    return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    files_to_save = ["passwords.txt", "encrypted_text_1.txt", "encrypted_text_2.txt", "encrypted_text_3.txt", "log.txt"]
    # This IP address should be PC3's IP address.
    listening_ip = "10.0.1.203"
    listening_port = 65000

    receive_files(files_to_save, listening_ip, listening_port)
