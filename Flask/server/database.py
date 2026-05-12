import sqlite3
import os 

DBPath = os.path.join(os.path.dirname(__file__),"usercontent.db")

def OpenConn() -> sqlite3.Connection:
  conn = sqlite3.connect(DBPath)
  conn.row_factory = sqlite3.Row
  return conn

def DBSetup() -> None:
  with OpenConn() as conn:
    conn.execute("""
      CREATE TABLE IF NOT EXISTS finalProjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        image_filename TEXT NOT NULL            
      );
  """)
    # User table
    conn.execute("""
CREATE TABLE IF NOT EXISTS user_login (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULl
  );
                """)
    
    conn.execute("""
CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  text TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (post_id) REFERENCES finalProjects(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES user_login(id)                     
  );
                """)
    conn.commit()
