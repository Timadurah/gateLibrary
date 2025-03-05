# License Management System

This project is a Python-based system for generating and managing licenses securely using OTP generation, encryption, hardware ID (HUID), and a license management controller. The system ensures that licenses are tied to specific machines and can be validated against expiration dates.

## Features

- **OTP Generation**: Generates a one-time password (OTP) using a secret key.
- **Encryption**: Encrypts the generated OTP using AES encryption to create a secure license code.
- **HUID Generation**: Generates a hardware unique identifier (HUID) to tie licenses to specific machines.
- **License Management**: Add, update, and verify license codes with expiration periods.
- **License Validation**: Ensures licenses are valid based on the HUID and the provided license code.

## Requirements

To run this system, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Add a New License

This function generates a new OTP, encrypts it, and assigns it as the new license code. The code is then stored in the license manager with the specified expiration date.

```python
def addNewLicense(expireDate: int):
    
    otp_generator = OneTimeAuthGenerator(SECRET_KEY)
    generated_otp = otp_generator.generate_otp()

    encryption_manager = EncryptionManager(SECRET_KEY, SECRET_IV)
    encoded = encryption_manager.encode_id(generated_otp)

    manager = LicenseManager()
    manager.insert_license_code(encoded, expireDate)

    return(manager.get_all_license_codes())
```

**Example:**

```python
licenses = addNewLicense(60)
# that is 60days expiring date so you will pass the expire date and the licence will be create with the date 
print("All licenses:", licenses)
```

### Login with a License

This function checks the validity of a given license code using the machine's hardware ID (HUID). If the license is valid, it is added to the system or updated if necessary.

```python
def loginWithLicense(userLicense_code: str):
    
    manager = LicenseManager()

    huid_generator = HUID()
    huid = huid_generator.get_hardware_id()

    manager.add_license(huid, userLicense_code)

    if manager.verify_license(huid, userLicense_code):
        print("License is valid.")
    else:
        print("License has expired.")
```

**Example:**

```python
loginWithLicense('LICENSE_CODE_123')
```

## Example Workflow

1. **Add a New License:**

   A new license is created with a specified expiration period (in days). The OTP is encrypted to generate a secure license code.

   ```python
   addNewLicense(60)  # Adds a new license valid for 60 days
   ```

2. **Login with an Existing License:**

   The system checks if the provided license code is valid for the current machine's hardware ID. If valid, the license is updated or inserted into the system.

   ```python
   loginWithLicense('LICENSE_CODE_123')
   ```

