import uuid
import hashlib
import os
import subprocess
from osFingerprint.type import OSType

class HUID(OSType):
    
    def get_hardware_id(self):
        """Generates a hardware unique identifier (HUID) based on OS type."""
        if self.get_os_type() == 'Windows':
            return self._get_windows_hwid()
        elif self.get_os_type() == 'Linux':
            return self._get_linux_hwid()
        elif self.get_os_type() == 'Darwin':
            return self._get_mac_hwid()
        else:
            raise NotImplementedError(f"HUID generation not supported for {self.get_os_type()}")

    def _get_windows_hwid(self):
        """Generate hardware ID on Windows."""
        try:
            # Use wmic command to get the motherboard serial number as a hardware ID
            cmd = 'wmic baseboard get serialnumber'
            serial_number = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
            return hashlib.sha256(serial_number.encode()).hexdigest()
        except Exception as e:
            raise RuntimeError(f"Failed to get Windows HUID: {e}")

    def _get_linux_hwid(self):
        """Generate hardware ID on Linux."""
        try:
            # Fetch the machine-id (usually found in /etc/machine-id or /var/lib/dbus/machine-id)
            if os.path.exists('/etc/machine-id'):
                with open('/etc/machine-id', 'r') as f:
                    machine_id = f.read().strip()
            elif os.path.exists('/var/lib/dbus/machine-id'):
                with open('/var/lib/dbus/machine-id', 'r') as f:
                    machine_id = f.read().strip()
            else:
                # Use a fallback (e.g., UUID of the system)
                machine_id = str(uuid.getnode())
            
            return hashlib.sha256(machine_id.encode()).hexdigest()
        except Exception as e:
            raise RuntimeError(f"Failed to get Linux HUID: {e}")

    def _get_mac_hwid(self):
        """Generate hardware ID on macOS."""
        try:
            # Use ioreg command to get the hardware UUID
            cmd = "ioreg -rd1 -c IOPlatformExpertDevice | awk '/IOPlatformUUID/ { print $3; }'"
            hw_uuid = subprocess.check_output(cmd, shell=True).decode().strip().strip('"')
            return hashlib.sha256(hw_uuid.encode()).hexdigest()
        except Exception as e:
            raise RuntimeError(f"Failed to get macOS HUID: {e}")
