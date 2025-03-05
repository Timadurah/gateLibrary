import platform
import os

class OSType:
    def __init__(self):
        self.system = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        print(self.get_os_details())

    def get_os_type(self):
        """Return the name of the operating system."""
        return self.system

    def get_os_release(self):
        """Return the OS release."""
        return self.release

    def get_os_version(self):
        """Return the OS version."""
        return self.version

    def is_windows(self):
        """Check if the OS is Windows."""
        return self.system == 'Windows'

    def is_linux(self):
        """Check if the OS is Linux."""
        return self.system == 'Linux'

    def is_mac(self):
        """Check if the OS is macOS."""
        return self.system == 'Darwin'

    def get_os_details(self):
        """Return detailed OS information."""
        return {
            'os_type': self.get_os_type(),
            'release': self.get_os_release(),
            'version': self.get_os_version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'architecture': platform.architecture()[0],
        }

# Example usage
if __name__ == "__main__":
    os_info = OSType()
    
    print(f"OS Type: {os_info.get_os_type()}")
    print(f"OS Release: {os_info.get_os_release()}")
    print(f"OS Version: {os_info.get_os_version()}")
    
    # Check OS type
    if os_info.is_windows():
        print("Running on Windows")
    elif os_info.is_linux():
        print("Running on Linux")
    elif os_info.is_mac():
        print("Running on macOS")
    
    # Print detailed OS information
    details = os_info.get_os_details()
    print("\nDetailed OS Information:")
    for key, value in details.items():
        print(f"{key}: {value}")
