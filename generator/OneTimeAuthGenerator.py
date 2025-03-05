import hashlib
import hmac
import time
from key.key import *

class OneTimeAuthGenerator:
    def __init__(self, secret_key, interval=30):
        """Initialize with a secret key and an interval for token expiration (in seconds)."""
        self.secret_key = secret_key
        self.interval = interval

    def _get_time_interval(self):
        """Get the current time interval based on the provided interval duration."""
        return int(time.time() // self.interval)

    def generate_otp(self):
        """Generate a unique one-time password (OTP) based on the current time interval."""
        time_interval = self._get_time_interval()

        # Create an HMAC using the secret key and the time interval as the message
        hmac_digest = hmac.new(
            self.secret_key.encode(),
            str(time_interval).encode(),
            hashlib.sha256
        ).digest()

        # Take the last 6 digits from the HMAC as the OTP
        otp = int.from_bytes(hmac_digest[-4:], 'big') % 10**10

        # Return the OTP as a zero-padded string
        return f'{otp}'

