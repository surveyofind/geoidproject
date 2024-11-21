import base64
from cryptography.fernet import Fernet

def load_key():
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()
    return key

def decrypt_value(encrypted_value_base64):
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_value = base64.urlsafe_b64decode(encrypted_value_base64)
    decrypted_value = cipher_suite.decrypt(encrypted_value)
    return float(decrypted_value.decode('utf-8'))
