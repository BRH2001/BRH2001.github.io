import socket
import os
from cryptography.fernet import Fernet, InvalidToken
import base64

class Decrypt:
    def __init__(self, keys_file):
        with open(keys_file, 'rb') as file:
            # Ensure that keys are UTF-8 encoded strings
            self.keys = [line.strip().decode('utf-8') for line in file]

        self.base64_key = None  # Initialize the base64_key attribute

    def run_decryption(self, encrypted_files):
        decrypted_files = []
        for encrypted_file_path in encrypted_files:
            # Read the encrypted text from the file
            with open(encrypted_file_path, 'rb') as encrypted_file:
                encrypted_text = encrypted_file.read()

            try:
                self._read_password_keys()
                decrypted_text = self._decrypt_text(encrypted_text)
                decrypted_file_path = self._save_decrypted_file(decrypted_text, encrypted_file_path)
                decrypted_files.append(decrypted_file_path)
            except InvalidToken:
                print(f"Error: Invalid token for {encrypted_file_path}. Check keys or file integrity.")
        return decrypted_files

    def _read_password_keys(self):
        current_key = self.keys[0]  # Use the first key for simplicity

        # Convert the key to bytes
        key_bytes = current_key.encode('utf-8')

        # Convert the bytes to base64
        self.base64_key = base64.urlsafe_b64encode(key_bytes)

    def _decrypt_text(self, encrypted_text):
        cipher = Fernet(self.base64_key)
        return cipher.decrypt(encrypted_text).decode()

    @staticmethod
    def _save_decrypted_file(decrypted_text, encrypted_file_path):
        # Modify the filename to change "_encrypted" to "_decrypted"
        output_file_path = encrypted_file_path.replace("_encrypted.txt", "_decrypted.txt")
        with open(output_file_path, 'w') as output_file:
            output_file.write(decrypted_text)
        print(f"Decrypted text saved to {output_file_path}")
        return output_file_path

def receive_files(save_dir, num_files, conn):
    files_received = []

    for _ in range(num_files):
        try:
            filename = conn.recv(1024).decode('utf-8')  # Receive the original filename
            if not filename:
                raise ValueError("Empty filename received")
        except Exception as e:
            print(f"Error receiving filename: {e}")
            continue

        file_path = os.path.join(save_dir, filename)

        try:
            file_size_bytes = conn.recv(8)
            file_size = int.from_bytes(file_size_bytes, byteorder='big')
        except Exception as e:
            print(f"Error receiving file size: {e}")
            continue

        with open(file_path, 'wb') as file:
            remaining_size = file_size
            while remaining_size > 0:
                try:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    file.write(chunk)
                    remaining_size -= len(chunk)
                except Exception as e:
                    print(f"Error receiving file data: {e}")
                    break

        files_received.append(file_path)

    return files_received

def handle_connection(addr, conn, save_dir, keys_file):
    print("Connected to:", addr)

    try:
        sender_info = conn.recv(1024).decode('utf-8')
        print(sender_info)

        num_files_str = conn.recv(8).decode('utf-8')
        num_files = int(num_files_str.split('fr_text')[0])

        files_received = receive_files(save_dir, num_files, conn)

        print("Files received successfully:")
        decrypt = Decrypt(keys_file)
        for file_path in files_received:
            if "_encrypted.txt" in file_path:
                decrypted_files = decrypt.run_decryption([file_path])
                for decrypted_file in decrypted_files:
                    print(decrypted_file)
            else:
                print(file_path)

    except Exception as e:
        print(f"Error handling connection: {e}")

if __name__ == "__main__":
    save_dir = "received_files_pc1"
    os.makedirs(save_dir, exist_ok=True)

    listen_ip = "10.0.1.207"
    listen_port = 65000
    keys_file = "passwords.txt"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((listen_ip, listen_port))
        s.listen()

        print("Waiting for connection...")
        conn, addr = s.accept()
        with conn:
            handle_connection(addr, conn, save_dir, keys_file)
