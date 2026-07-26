import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = str(BASE_DIR / "saved_passwords.db")

def initialize_database():
    """Create the database table if it doesn't exist"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                strength INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✓ Database initialized successfully\n")
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}\n")

def save_password(name, password, strength, notes=""):
    """Save a password to the database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO passwords (name, password, strength, notes)
            VALUES (?, ?, ?, ?)
        ''', (name, password, strength, notes))
        
        conn.commit()
        conn.close()
        print(f"✅ Password for '{name}' saved successfully!\n")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error saving password: {e}\n")
        return False

def get_all_passwords():
    """Retrieve all saved passwords"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, strength, created_at FROM passwords ORDER BY created_at DESC')
        passwords = cursor.fetchall()
        conn.close()
        
        return passwords
    except sqlite3.Error as e:
        print(f"❌ Error retrieving passwords: {e}\n")
        return []

def get_password_by_name(name):
    """Retrieve a specific password by name"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT password, strength, notes FROM passwords WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()
        
        return result
    except sqlite3.Error as e:
        print(f"❌ Error retrieving password: {e}\n")
        return None

def delete_password(name):
    """Delete a saved password"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM passwords WHERE name = ?', (name,))
        
        if cursor.rowcount == 0:
            print(f"⚠️  Password for '{name}' not found\n")
            return False
        
        conn.commit()
        conn.close()
        print(f"✅ Password for '{name}' deleted successfully!\n")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error deleting password: {e}\n")
        return False

def update_password(name, new_password, new_strength, new_notes=""):
    """Update an existing password"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE passwords 
            SET password = ?, strength = ?, notes = ?, created_at = CURRENT_TIMESTAMP
            WHERE name = ?
        ''', (new_password, new_strength, new_notes, name))
        
        if cursor.rowcount == 0:
            print(f"⚠️  Password for '{name}' not found\n")
            return False
        
        conn.commit()
        conn.close()
        print(f"✅ Password for '{name}' updated successfully!\n")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error updating password: {e}\n")
        return False

def display_saved_passwords():
    """Display all saved passwords in a formatted table"""
    passwords = get_all_passwords()
    
    if not passwords:
        print("📋 No saved passwords yet.\n")
        return
    
    print("\n" + "=" * 80)
    print("📋 SAVED PASSWORDS")
    print("=" * 80)
    
    strength_map = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong", 
                    5: "Very Strong", 6: "Excellent", 7: "Excellent+", 8: "Excellent+"}
    
    for pwd in passwords:
        pwd_id, name, strength, created_at = pwd
        strength_label = strength_map.get(strength, "Unknown")
        print(f"ID: {pwd_id} | Name: {name} | Strength: {strength_label} | Created: {created_at}")
    
    print("=" * 80 + "\n")

def view_password(name):
    """View a specific saved password"""
    result = get_password_by_name(name)
    
    if not result:
        print(f"⚠️  No password found for '{name}'\n")
        return
    
    password, strength, notes = result
    strength_map = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong", 
                    5: "Very Strong", 6: "Excellent", 7: "Excellent+", 8: "Excellent+"}
    strength_label = strength_map.get(strength, "Unknown")
    
    print("\n" + "=" * 60)
    print(f"🔐 PASSWORD: {name}")
    print("=" * 60)
    print(f"Password: {password}")
    print(f"Strength: {strength_label} ({strength}/8)")
    if notes:
        print(f"Notes: {notes}")
    print("=" * 60 + "\n")

def clear_all_passwords():
    """Delete all saved passwords (use with caution)"""
    try:
        confirm = input("⚠️  Are you sure you want to delete ALL passwords? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Operation cancelled\n")
            return False
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM passwords')
        conn.commit()
        conn.close()
        
        print("✅ All passwords deleted successfully!\n")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error clearing passwords: {e}\n")
        return False
