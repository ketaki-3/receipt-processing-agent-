import sqlite3

def init_db():
      conn = sqlite3.connect("receipts.db")
      conn.execute("""
          CREATE TABLE IF NOT EXISTS receipts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              vendor TEXT, amount REAL, date TEXT, category TEXT
          )
      """)
      conn.execute("""
          CREATE TABLE IF NOT EXISTS budgets (
              category TEXT PRIMARY KEY, monthly_limit REAL
          )
      """)
      conn.commit()
      conn.close()

if __name__ == "__main__":
      init_db()
      conn = sqlite3.connect("receipts.db")
      conn.executemany(
          "INSERT OR REPLACE INTO budgets VALUES (?, ?)",
          [("food", 5000), ("travel", 10000), ("office", 3000), ("other", 2000)],
      )
      conn.commit()
      conn.close()