NEDERLANDS-- Data-Transfer app
--------------------------------------------------------------------------------------------------------------------------------
De programma's werken als volgt:

Op PC1 worden de volgende bestanden gebruikt:
    Textgen.py: Vraagt de gebruiker om drie verschillende teksten in te voeren met de namen 'text_1.txt', 'text_2.txt' en 'text_3.txt'.
    password.py: Gebruikt de Passwordgen-klasse om 50 willekeurige wachtwoorden te genereren met elk 32 tekens. Het programma selecteert vervolgens drie willekeurige wachtwoorden en maakt hieruit drie Fernet-sleutels, die vervolgens worden opgeslagen in 'passwords.txt'.
    Encrypt.py: Gebruikt de Fernet-sleutels die zijn opgeslagen in 'passwords.txt' om de teksten in 'text_1.txt', 'text_2.txt' en 'text_3.txt' te versleutelen. De versleutelde teksten worden opgeslagen in 'encrypted_text_1.txt', 'encrypted_text_2.txt' en 'encrypted_text_3.txt'.
    send_encrypted_to_pc2.py: Verstuurt de versleutelde bestanden die zijn gegenereerd met Encrypt.py en de wachtwoorden die zijn gegenereerd met password.py in 'passwords.txt' naar PC2. Vervolgens verwijdert dit programma de originele tekstbestanden. (Dit programma moet tegelijkertijd met receive_encrypted_on_pc2.py worden uitgevoerd)
    receive_pdf_on_pc1.py: Ontvangt de bestanden die zijn verzonden vanaf PC3 en slaat ze op onder dezelfde namen als ze vanaf PC3 zijn verzonden. (Dit programma moet tegelijkertijd met send_pdf_to_pc1.py worden uitgevoerd)

Op PC2 worden de volgende bestanden gebruikt:
    receive_encrypted_on_pc2.py: Ontvangt de bestanden die zijn verzonden vanaf PC1 en slaat ze op onder dezelfde namen als ze vanaf PC1 zijn verzonden. (Dit programma moet tegelijkertijd met send_encrypted_to_pc2.py worden uitgevoerd)
    send_encrypted_to_pc3.py: Verstuurt de bestanden die zijn ontvangen met receive_encrypted_on_pc2.py naar PC3. (Dit programma moet tegelijkertijd met receive_encrypted_on_pc3.py worden uitgevoerd)

Op PC3 worden de volgende bestanden gebruikt:
    receive_encrypted_on_pc3.py: Ontvangt de bestanden die zijn verzonden vanaf PC2 en slaat ze op onder dezelfde namen als ze vanaf PC2 zijn verzonden. (Dit programma moet tegelijkertijd met send_encrypted_to_pc3.py worden uitgevoerd)
    decrypt.py: Gebruikt de Fernet-sleutels die zijn opgeslagen in 'passwords.txt' om de teksten in 'encrypted_text_1.txt', 'encrypted_text_2.txt' en 'encrypted_text_3.txt' te ontsleutelen. De ontsleutelde teksten worden opgeslagen in 'decrypted_1.txt', 'decrypted_2.txt' en 'decrypted_3.txt'.
    text_to_pdf_conv.py: Zet 'decrypted_text_1.txt', 'decrypted_text_2.txt' en 'decrypted_text_3.txt' om in .PDF-bestanden en slaat ze op als 'text_1.pdf', 'text_2.pdf' en 'text_3.pdf'.
    send_pdf_to_pc1.py: Verstuurt de PDF-bestanden die zijn gemaakt met text_to_pdf_conv.py naar PC1. (Dit programma moet tegelijkertijd met receive_pdf_on_pc1.py worden uitgevoerd)
--------------------------------------------------------------------------------------------------------------------------------
Dingen om te overwegen bij het uitvoeren van de programma's:
    Elke pc moet een poort toevoegen om ervoor te zorgen dat de bestanden door de firewall kunnen komen. In onze programma's hebben we deze poort 65000 genoemd.
    De IP-adressen moeten overeenkomen met de pc's. Het is mogelijk dat een IP-adres verandert omdat de router een nieuwe toewijst.

================================================================================================================================

ENGLISH- Data-Transfer app
--------------------------------------------------------------------------------------------------------------------------------
The programs work as follows: 

On PC1, the following files are used:
    Textgen.py: Prompts the user to enter three different texts named 'text_1.txt', 'text_2.txt', and 'text_3.txt'.
    password.py: Uses the Passwordgen class to generate 50 random passwords with 32 characters each. The program then selects three random passwords and creates three Fernet keys from them, which are then stored in 'passwords.txt'.
    Encrypt.py: Uses the Fernet keys stored in 'passwords.txt' to encrypt the texts in 'text_1.txt', 'text_2.txt', and 'text_3.txt'. The encrypted texts are saved in 'encrypted_text_1.txt', 'encrypted_text_2.txt', and 'encrypted_text_3.txt'.
    send_encrypted_to_pc2.py: Sends the encrypted files generated with Encrypt.py and the passwords generated with password.py in 'passwords.txt' to PC2. Then, this program deletes the original text files. (This program needs to be run simultaneously with receive_encrypted_on_pc2.py)
    receive_pdf_on_pc1.py: Receives the files sent from PC3 and saves them under the same names as they were sent from PC3. (This program needs to be run simultaneously with send_pdf_to_pc1.py)

On PC2, the following files are used:
    receive_encrypted_on_pc2.py: Receives the files sent from PC1 and saves them under the same names as they were sent from PC1. (This program needs to be run simultaneously with send_encrypted_to_pc2.py)
    send_encrypted_to_pc3.py: Sends the files received with receive_encrypted_on_pc2.py to PC3. (This program needs to be run simultaneously with receive_encrypted_on_pc3.py)

On PC3, the following files are used:
    receive_encrypted_on_pc3.py: Receives the files sent from PC2 and saves them under the same names as they were sent from PC2. (This program needs to be run simultaneously with send_encrypted_to_pc3.py)
    decrypt.py: Uses the Fernet keys stored in 'passwords.txt' to decrypt the texts in 'encrypted_text_1.txt', 'encrypted_text_2.txt', and 'encrypted_text_3.txt'. The decrypted texts are saved in 'decrypted_1.txt', 'decrypted_2.txt', and 'decrypted_3.txt'.
    text_to_pdf_conv.py: Converts 'decrypted_text_1.txt', 'decrypted_text_2.txt', and 'decrypted_text_3.txt' into .PDF files and saves them as 'text_1.pdf', 'text_2.pdf', and 'text_3.pdf'.
    send_pdf_to_pc1.py: Sends the PDF files created with text_to_pdf_conv.py to PC1. (This program needs to be run simultaneously with receive_pdf_on_pc1.py)
--------------------------------------------------------------------------------------------------------------------------------
Things to consider when running the programs:
    Each PC needs to have a port added to ensure that the files can pass through the firewall. In our programs, we have named this port 65000.
    The IP addresses must match the PCs. It is possible that an IP address changes because the router assigns a new one.