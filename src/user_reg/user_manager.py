import json
import os
import re
from src.user_reg.user import User

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def is_valid_password(self, password):
        stripped_password = password.replace(" ", "")
        if len(stripped_password) < 7:
            return False
        if not re.search(r"[A-Z]", stripped_password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", stripped_password):
            return False
        return True

    def signup(self, username, password, first_name, last_name):
        if username in self.users:
            return "Username already exists. Please choose another."
        
        if not self.is_valid_password(password):
            return ("Password must be at least 7 characters long, "
                    "contain at least one uppercase letter and one special character. Please Sign Up again.")
        
        self.users[username] = User(username, password, first_name, last_name)
        self.save_users()
        return "Signup successful!"

    def login(self, username, password):
        if username not in self.users:
            return "Username not found."
        
        if self.users[username].password == password:
            return "Login successful!"
        return "Incorrect password."

    def save_users(self):
        file_path = r"C:\Users\asus\Documents\Indixpert-FSD-April-Python-Pr01\src\user_reg\user_reg.json"
        with open(file_path, 'w') as file:
            json.dump({username: vars(user) for username, user in self.users.items()}, file, indent=4)

    def load_users(self):
        file_path = r"C:\Users\asus\Documents\Indixpert-FSD-April-Python-Pr01\src\user_reg\user_reg.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.users = {username: User(**info) for username, info in data.items()}