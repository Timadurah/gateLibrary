import sqlite3

class createDb:
    def __init__(self, db_name='license_manager.db'):
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        """Creates the licenses and license_codeDB tables if they don't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Table for valid license codes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS license_codeDB (
                    license_code TEXT PRIMARY KEY,
                    expire_date TEXT NOT NULL
                )
            ''')
            
            # Table for registered licenses
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    huid TEXT NOT NULL,
                    license_code TEXT NOT NULL,
                    expiry_date TEXT NOT NULL
                )
            ''')
            conn.commit()