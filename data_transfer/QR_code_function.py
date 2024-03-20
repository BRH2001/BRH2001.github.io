import qrcode
import os

def generate_qr_code_from_files(directory_path):
    data = ""  # Initialize an empty string

    # List all files in the directory
    files = os.listdir(directory_path)

    # Iterate through files in the directory
    for file_name in files:
        # Check if the file starts with "nl", "de", or "fr" and has a ".txt" extension
        if file_name.lower().startswith(("nl", "de", "fr")) and file_name.lower().endswith(".txt"):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r') as file:
                data += file.read().strip() + "\n"
                
            print(f"Found valid file: {file_name}")

            # Extract language prefix
            language_prefix = file_name.lower()[:2]

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create QR code image based on the language prefix
            if language_prefix == "nl":
                img = qr.make_image(fill_color="green", back_color="black")
            elif language_prefix == "de":
                img = qr.make_image(fill_color="yellow", back_color="black")
            elif language_prefix == "fr":
                img = qr.make_image(fill_color="red", back_color="black")
            else:
                print("No language detected.")
                return  # Exit the function if no language is detected

            # Save the QR code image with the detected language prefix
            output_qr_code_filename = f"{language_prefix}_combined_qr_code.png"
            img.save(output_qr_code_filename)
            print(f"QR code saved to {output_qr_code_filename}")
            return  # Exit the function after processing the first valid file

if __name__ == "__main__":
    # Directory path where text files are located
    directory_path = "c:/Users/Admin/Documents/School-archive.23/GitHub/Data_Encrypter"  # Update this to the appropriate directory

    # Generate QR code from the text files in the directory
    generate_qr_code_from_files(directory_path)
