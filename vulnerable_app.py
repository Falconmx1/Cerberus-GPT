# vulnerable_app.py
import os
import pickle
import sqlite3

def login(username, password):
    # Vulnerabilidad: SQL Injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{username}' AND pass = '{password}'"
    cursor.execute(query)
    return cursor.fetchone()

def run_system_command(command):
    # Vulnerabilidad: Command Injection
    os.system(f"ping -c 4 {command}")

def load_user_data(data_string):
    # Vulnerabilidad: Insecure Deserialization
    return pickle.loads(data_string)

def main():
    # Vulnerabilidad: Hardcoded Password
    db_password = "SuperSecretPassword123!"
    print(f"Conectando a la DB con la contraseña: {db_password}")

if __name__ == "__main__":
    main()
