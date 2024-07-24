from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os

# Get the base directory of the Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_keys():
    private_key_path = os.path.join(BASE_DIR, 'private.pem')
    public_key_path = os.path.join(BASE_DIR, 'public.pem')
    
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    
    return private_key, public_key

def encrypt_file(file_data):
    private_key, public_key = load_keys()
    
    # Generate a random AES key
    aes_key = get_random_bytes(16)
    
    # Encrypt file data with AES
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    encrypted_data = cipher_aes.encrypt(pad(file_data, AES.block_size))
    iv = cipher_aes.iv
    
    # Encrypt AES key with RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    
    # Encode encrypted AES key and file data to base64 for transmission
    encrypted_aes_key_b64 = base64.b64encode(encrypted_aes_key).decode('utf-8')
    encrypted_data_b64 = base64.b64encode(iv + encrypted_data).decode('utf-8')
    
    return encrypted_aes_key_b64, encrypted_data_b64

def decrypt_file(encrypted_aes_key_b64, encrypted_data_b64):
    private_key, _ = load_keys()
    
    # Decode base64 encoded data
    encrypted_aes_key = base64.b64decode(encrypted_aes_key_b64)
    encrypted_data = base64.b64decode(encrypted_data_b64)
    
    # Decrypt AES key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    
    # Extract IV and encrypted file data
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    
    # Decrypt file data with AES
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)
    
    return decrypted_data
