import sqlite3

def init_db():
    conn = sqlite3.connect('/root/agent_system/real_estate.db')
    cursor = conn.cursor()
    
    # Δημιουργία πίνακα με όλα τα στοιχεία για Data Farming
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            sq_meters REAL,
            price_per_sqm REAL,
            floor TEXT,
            year_built INTEGER,
            location TEXT,
            property_type TEXT,
            condition TEXT,
            energy_class TEXT,
            rooms INTEGER,
            heating TEXT,
            url TEXT UNIQUE,
            platform TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Index για γρήγορη αναζήτηση στα διπλότυπα URLs
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_url ON listings(url)')
    
    conn.commit()
    conn.close()
    print("✅ Real Estate Database initialized with Data Farming fields.")

if __name__ == "__main__":
    init_db()
