from generator.OneTimeAuthGenerator import OneTimeAuthGenerator
from encryption.EncryptionManager import EncryptionManager
from LicenseManager.LicenseManager import LicenseManager
from osFingerprint.HUID import HUID
from key.key import SECRET_IV, SECRET_KEY


def addNewLicense(expireDate: int):
    
    # generateOtp
    otp_generator = OneTimeAuthGenerator(SECRET_KEY)
    generated_otp = otp_generator.generate_otp()

    # Initialize the EncryptionManager
    encryption_manager = EncryptionManager(SECRET_KEY, SECRET_IV)

    # Encrypt an ID
    encoded = encryption_manager.encode_id(generated_otp)

    # Assign As ID Generated Value.
    idGenerated = encoded
    # controller operaations
    manager = LicenseManager()

    # Insert a new license code that is valid for 60 days
    manager.insert_license_code(idGenerated, expireDate)

    # Fetch and print all license codes
    return(manager.get_all_license_codes())


def loginWithLicense(userLicense_code: str):
    # this will generate the HUID and take the license check if is valid or expire then 
    # then insert if all goes well
    # controller operaations
    manager = LicenseManager()

    huid_generator = HUID()
    huid = huid_generator.get_hardware_id()
    # Add or update the license if it's valid in license_codeDB
    manager.add_license(huid, userLicense_code) 
    # License valid for 30 days

    # Verify the license
    if manager.verify_license(huid, userLicense_code):
        print("License is valid.")
    else:
        print("License has expired.")

