from cryptography.fernet import Fernet
import base64
import os

class Encrypt:

    def __init__(self, *text_files):

        with open("passwords.txt", 'rb') as file:
            self.keys = [line.strip() for line in file]

        self.text_files = []
        for text_file in text_files:
            self.text_files.append(text_file)

    def run_encryption(self):
        for i, text_file_path in enumerate(self.text_files):
            # Use absolute path to handle potential file path issues
            abs_file_path = os.path.abspath(text_file_path)

            # Check if the file exists
            if not os.path.exists(abs_file_path):
                print(f"Error: File {abs_file_path} not found.")
                continue

            # Read the text from the file
            with open(abs_file_path, 'r') as text_file:
                original_text = text_file.read()

            self._read_password_keys(i)
            encrypted_text = self._encrypt_text(original_text)
            self._save_encrypted_file(abs_file_path, encrypted_text)

    def _read_password_keys(self, i):
        current_key = self.keys[i % len(self.keys)]  # Use keys in a cyclic manner

        # Convert the key to base64
        self.base64_key = base64.urlsafe_b64encode(current_key)

    def _encrypt_text(self, original_text):
        cipher = Fernet(self.base64_key)
        return cipher.encrypt(original_text.encode())

    def _save_encrypted_file(self, text_file_path, encrypted_text):
        # Extract the filename without extension
        filename, extension = os.path.splitext(os.path.basename(text_file_path))

        # Construct the new filename
        encrypted_text_file_path = f"{filename}_encrypted{extension}"

        with open(encrypted_text_file_path, 'wb') as encrypted_text_file:
            encrypted_text_file.write(encrypted_text)

        print(f"Encrypted Text for {text_file_path} saved to {encrypted_text_file_path}")

if __name__ == "__main__":
    # Provide the paths of files to be encrypted
    files_to_encrypt = ["nl_text_1.txt", "nl_text_2.txt", "nl_text_3.txt",
                        "de_text_1.txt", "de_text_2.txt", "de_text_3.txt",
                        "fr_text_1.txt", "fr_text_2.txt", "fr_text_3.txt"]

    encrypt = Encrypt(*files_to_encrypt)
    encrypt.run_encryption()
