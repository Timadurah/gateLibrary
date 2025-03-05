from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import hashlib
import time
from key.key import *

class EncryptionManager:
    def __init__(self, secret_key, secret_iv):
        # Store the secret key and IV
        self.secret_key = secret_key
        self.secret_iv = secret_iv
        self.key, self.iv = self._derive_key_iv()

    def _derive_key_iv(self):
        """Derive the key and initialization vector (IV) using SHA-256 hash."""
        key = hashlib.sha256(self.secret_key.encode()).digest()
        iv = hashlib.sha256(self.secret_iv.encode()).digest()[:16]
        return key, iv

    def _pad_data(self, data):
        """Apply PKCS7 padding to the data."""
        padder = padding.PKCS7(128).padder()
        return padder.update(data) + padder.finalize()

    def _unpad_data(self, padded_data):
        """Remove PKCS7 padding from the data."""
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    def encode_id(self, id_value):
        """Encrypt the given ID along with a unique identifier."""
        unique_value = str(int(time.time() * 1000))  # Timestamp in milliseconds
        data_to_encrypt = (str(id_value) + unique_value).encode()

        # Apply padding
        padded_data = self._pad_data(data_to_encrypt)

        # Encrypt the padded data
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Return base64 encoded encrypted data
        return base64.b64encode(encrypted_data).decode('utf-8')

    # def decode_id(self, encoded_id):

    #     """Decrypt the given encrypted ID and extract the original ID."""
    #     # Decode from base64 and decrypt the data
    #     encrypted_data = base64.b64decode(encoded_id)
    #     cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
    #     decryptor = cipher.decryptor()
    #     decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    #     # Remove padding
    #     unpadded_data = self._unpad_data(decrypted_data)

    #     # Extract and return the original ID by removing the unique identifier
    #     original_id = unpadded_data[:-13].decode('utf-8')  # Assuming unique identifier is 13 chars long (timestamp)
    #     return original_id
