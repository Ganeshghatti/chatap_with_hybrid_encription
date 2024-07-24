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