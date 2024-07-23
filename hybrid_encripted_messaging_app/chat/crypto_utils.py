from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from Crypto.PublicKey import RSA
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

private_key, public_key = load_keys()

def encrypt_message(message, public_key):
    # Generate a random AES key
    session_key = get_random_bytes(16)

    # Encrypt the session key with the RSA public key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the message with the AES key
    cipher_aes = AES.new(session_key, AES.MODE_CBC)
    ct_bytes = cipher_aes.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher_aes.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    enc_session_key = base64.b64encode(enc_session_key).decode('utf-8')
    return iv, ct, enc_session_key

def decrypt_message(iv, ct, enc_session_key, private_key):
    # Decode the encrypted session key and IV
    enc_session_key = base64.b64decode(enc_session_key)
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)

    # Decrypt the session key with the RSA private key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the message with the AES key
    cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
    pt = unpad(cipher_aes.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')
