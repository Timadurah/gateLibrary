# License Manager System

This project provides a Python-based system for generating and managing licenses using OTP generation, encryption, hardware ID (HUID), and a license management controller. The system includes encryption for added security and allows license validation based on hardware unique identifiers.

## Features

- **OTP Generation**: Generates a one-time password (OTP) using a secret key.
- **Encryption**: Encrypts generated OTPs using AES encryption.
- **HUID Generation**: Generates a hardware unique identifier (HUID) to tie licenses to specific machines.
- **License Management**: Provides the ability to add, update, and verify license codes with expiration dates.
- **License Validation**: Validates licenses based on the HUID and provided license code.

## Requirements

Before running this project, you will need to install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Use

1. **Generate OTP and Encrypt it:**

    The system generates a one-time password (OTP) using a secret key and encrypts the OTP to create a license identifier. The encrypted OTP will be used as the license code.

    ```python
    otp_generator = OneTimeAuthGenerator(SECRET_KEY)
    generated_otp = otp_generator.generate_otp()
    
    encryption_manager = EncryptionManager(SECRET_KEY, SECRET_IV)
    encoded = encryption_manager.encode_id(generated_otp)
    
    print(f"Encoded ID: {encoded}")
    ```

2. **Generate Hardware Unique Identifier (HUID):**

    The system generates a hardware unique identifier (HUID) to tie licenses to a specific machine. This ensures that the license is hardware-bound.

    ```python
    huid_generator = HUID()
    huid = huid_generator.get_hardware_id()
    print(f"Hardware Unique Identifier (HUID): {huid}")
    ```

3. **Insert a License Code:**

    You can add a new license code to the system, specifying the number of days for which the license is valid.

    ```python
    manager = LicenseManager()
    manager.insert_license_code('NEW_LICENSE_CODE_123', 60)
    ```

4. **Verify a License Code:**

    The system can verify if a license code is still valid based on the hardware ID and the provided license code.

    ```python
    if manager.verify_license(huid, license_code):
        print("License is valid.")
    else:
        print("License has expired.")
    ```

## Example Usage

```python
if __name__ == '__main__':
    # Generate OTP and encrypt it
    otp_generator = OneTimeAuthGenerator(SECRET_KEY)
    generated_otp = otp_generator.generate_otp()

    encryption_manager = EncryptionManager(SECRET_KEY, SECRET_IV)
    encoded = encryption_manager.encode_id(generated_otp)

    print(f"Encoded ID: {encoded}")

    # Generate hardware unique identifier (HUID)
    huid_generator = HUID()
    huid = huid_generator.get_hardware_id()
    print(f"Hardware Unique Identifier (HUID): {huid}")

    # License management operations
    manager = LicenseManager()

    # Insert a new license code valid for 60 days
    manager.insert_license_code('NEW_LICENSE_CODE_123', 60)

    # Verify the license
    if manager.verify_license(huid, 'LICENSE123'):
        print("License is valid.")
    else:
        print("License has expired.")
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
