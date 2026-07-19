import sqlite3
def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    #user table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   phone TEXT,
                   password TEXT NOT NULL
        )
     """)

    # Matches Table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS matches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        team1 TEXT NOT NULL,
                        team2 TEXT NOT NULL,
                        stadium TEXT NOT NULL,
                        match_date TEXT NOT NULL,
                        match_time TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        available_seats INTEGER NOT NULL
        )
      """)

    # Bookings Table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        match_id INTEGER,
                        seat_category TEXT,
                        seat_number TEXT,
                        quantity INTEGER,
                        total_price INTEGER,
                        booking_date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(match_id) REFERENCES matches(id)
        )
     """)

    # Admin Table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS admin (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
        )
     """)

    conn.commit()
    conn.close()

    print("Database and tables created successfully!")

def insert_sample_matches():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM matches")
    count = cursor.fetchone()[0]

    if count == 0:
        matches = [
            ("CSK", "MI", "M. A. Chidambaram Stadium", "2026-06-15", "7:30 PM", 1200, 500),
            ("RCB", "KKR", "M. Chinnaswamy Stadium", "2026-06-18", "7:30 PM", 1500, 400),
            ("SRH", "DC", "Rajiv Gandhi Stadium", "2026-06-20", "7:30 PM", 1000, 450),
            ("GT", "RR", "Narendra Modi Stadium", "2026-06-22", "7:30 PM", 1300, 550),
            ("PBKS", "LSG", "IS Bindra Stadium", "2026-06-24", "7:30 PM", 1100, 350),
            ("MI", "RCB", "Wankhede Stadium", "2026-06-27", "7:30 PM", 1800, 600)
        ]

        cursor.executemany("""
            INSERT INTO matches
            (team1, team2, stadium, match_date, match_time, price, available_seats)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, matches)

        conn.commit()

    conn.close()

if __name__ == "__main__":
    create_database()
    insert_sample_matches()