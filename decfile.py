from cryptography.fernet import Fernet

with open('encrypt_key.txt', 'rb') as file:
    key = file.read()

system_info_e = 'e_system.txt'
clipboard_info_e = 'e_clipboard.txt'
keys_info_e = 'e_key_logged.txt'

encrypt_files = [system_info_e, clipboard_info_e, keys_info_e]

for encrypted_file in encrypt_files:
    with open(encrypted_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_file, 'wb') as f:
        f.write(decrypted)
