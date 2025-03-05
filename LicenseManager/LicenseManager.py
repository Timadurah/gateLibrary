import sqlite3
import time
import requests
from datetime import datetime, timedelta
from db.createDB import createDb


import requests
import time
from datetime import datetime

class TimeFetcher:
    def __init__(self, retries=3, backoff=2):
        self.retries = retries
        self.backoff = backoff

    def get_online_time_worldclock(self):
        """Gets the current date and time from worldclockapi.com API with retry and fallback"""
        url = 'http://worldclockapi.com/api/json/utc/now'
        attempt = 0
        while attempt < self.retries:
            try:
                response = requests.get(url, timeout=5)  # Added timeout to prevent hanging
                if response.status_code == 200:
                    data = response.json()
                    return datetime.strptime(data['currentDateTime'], '%Y-%m-%dT%H:%M%SZ')
                else:
                    print(f"Attempt {attempt + 1} failed: Received status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")

            attempt += 1
            time.sleep(self.backoff)  # Wait for a bit before retrying

        # Fallback to local time if API is unreachable
        print("Falling back to system time")
        return datetime.utcnow()


class LicenseManager(createDb):
    def __init__(self, db_name='license_manager.db'):
        super().__init__(db_name)
    
    def get_online_time(retries=3, backoff=2):
        
        # Example usage
        time_fetcher = TimeFetcher(retries=3, backoff=2)
        online_time = time_fetcher.get_online_time_worldclock()
        return(online_time)


    def is_license_code_valid(self, license_code):
        """Checks if the license_code exists in license_codeDB and is not expired."""
        try:
            current_time = self.get_online_time()

            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT expire_date FROM license_codeDB WHERE license_code = ?
                ''', (license_code,))
                result = cursor.fetchone()

                if result:
                    expire_date = datetime.fromisoformat(result[0])
                    if current_time < expire_date:
                        return True  # License code is valid and not expired
                    else:
                        print(f"License code {license_code} has expired in license_codeDB.")
                        return False  # License code is expired in license_codeDB
                else:
                    print(f"License code {license_code} does not exist in license_codeDB.")
                    return False  # License code does not exist in license_codeDB
        except Exception as e:
            raise RuntimeError(f"Error checking license code: {e}")

    def add_license(self, huid, license_code):
        """Adds or updates the license if it exists in license_codeDB and is not expired."""
        try:
            # Check if the license_code is valid in license_codeDB
            if not self.is_license_code_valid(license_code):
                raise ValueError(f"License code {license_code} is not valid or has expired.")

            current_time = self.get_online_time()
            

            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # Check if the license is already registered in licenses table
                cursor.execute('''
                    SELECT expiry_date FROM licenses WHERE huid = ? AND license_code = ?
                ''', (huid, license_code))
                result = cursor.fetchone()

                if result:
                    expire_date = datetime.fromisoformat(result[0])
                    if current_time < expire_date:
                        print(f"License for {license_code} is still valid until {expire_date}.")
                    else:
                        # License exists but expired.
                        print(f"License for {license_code} already exists but expired contact admin for new License")
                else:
                    # License does not exist, insert a new one
                    cursor.execute('''
                        INSERT INTO licenses (huid, license_code, expiry_date)
                        VALUES (?, ?, ?)
                    ''', (huid, license_code, expire_date))
                    conn.commit()
                    print(f"License for {license_code} has been unlocked.")
        except Exception as e:
            raise RuntimeError(f"Error adding or updating license: {e}")

    def verify_license(self, huid, license_code):
        """Verifies if the license is still valid in the licenses table."""
        try:
            current_time = self.get_online_time()

            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT expiry_date FROM licenses
                    WHERE huid = ? AND license_code = ?
                ''', (huid, license_code))
                result = cursor.fetchone()

                if result:
                    expiry_date = datetime.fromisoformat(result[0])
                    if current_time < expiry_date:
                        return True
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            raise RuntimeError(f"Error verifying license: {e}")

    def insert_license_code(self, license_code, days_valid):
        """
        Inserts a new license code into the license_codeDB table.
        The license will expire after `days_valid` days from the current time.
        """
        try:
            # Get the current time and calculate expiration date
            current_time = self.get_online_time()
            expiry_date = current_time + timedelta(days=days_valid)

            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # Check if the license_code already exists in the table
                cursor.execute('''
                    SELECT license_code FROM license_codeDB WHERE license_code = ?
                ''', (license_code,))
                result = cursor.fetchone()

                if result:
                    print(f"License code '{license_code}' already exists in the database.")
                else:
                    # Insert the new license code with expiry date
                    cursor.execute('''
                        INSERT INTO license_codeDB (license_code, expire_date)
                        VALUES (?, ?)
                    ''', (license_code, expiry_date.isoformat()))
                    conn.commit()
                    print(f"License code '{license_code}' inserted successfully with expiry date {expiry_date}.")
        except Exception as e:
            raise RuntimeError(f"Error inserting license code: {e}")

    def get_all_license_codes(self):
        """Fetches all the license codes and their expiration dates from the license_codeDB table."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT license_code, expire_date FROM license_codeDB')
                result = cursor.fetchall()
                
                if result:
                    for row in result:
                        print(f"License Code: {row[0]}, Expiry Date: {row[1]}")
                else:
                    print("No license codes found in the database.")
        except Exception as e:
            raise RuntimeError(f"Error fetching license codes: {e}")
