from cryptography.fernet import Fernet

key = Fernet.generate_key()

def get_key():
    return key