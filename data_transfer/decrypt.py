import os
from cryptography.fernet import Fernet, InvalidToken
import base64

class Decrypt:

    def __init__(self):
        with open("passwords.txt", 'rb') as file:
            # Ensure that keys are UTF-8 encoded strings
            self.keys = [line.strip().decode('utf-8') for line in file]

        self.base64_key = None  # Initialize the base64_key attribute

    def run_decryption(self, files_to_decrypt):
        for encrypted_file_path in files_to_decrypt:
            try:
                with open(encrypted_file_path, 'rb') as encrypted_file:
                    encrypted_text = encrypted_file.read()

                language, index = self._parse_file_path(encrypted_file_path)
                self._read_password_keys(index)
                decrypted_text = self._decrypt_text(encrypted_text)
                self._save_decrypted_file(decrypted_text, encrypted_file_path)
            except FileNotFoundError:
                print(f"Error: File {encrypted_file_path} not found.")
            except InvalidToken:
                print(f"Error: Invalid token for {encrypted_file_path}. Check keys or file integrity.")

    def _parse_file_path(self, file_path):
        parts = file_path.split("_")
        language = parts[0]
        index = int(parts[-2])
        return language, index

    def _read_password_keys(self, index):
        current_key = self.keys[index % len(self.keys)]  # Use keys in a cyclic manner
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
        output_file_path = encrypted_file_path.replace("_encrypted", "_decrypted")
        os.remove(encrypted_file_path)
        with open(output_file_path, 'w') as output_file:
            output_file.write(decrypted_text)

        print(f"Decrypted text saved to {output_file_path}")

if __name__ == "__main__":
    files_to_decrypt = ["nl_text_1_encrypted.txt", "nl_text_2_encrypted.txt", "nl_text_3_encrypted.txt",
                        "de_text_1_encrypted.txt", "de_text_2_encrypted.txt", "de_text_3_encrypted.txt",
                        "fr_text_1_encrypted.txt", "fr_text_2_encrypted.txt", "fr_text_3_encrypted.txt"]
    decrypt = Decrypt()
    decrypt.run_decryption(files_to_decrypt)
