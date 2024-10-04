import json
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
    
    def is_admin_present(self):
        for user in self.users.values():
            if user.role == "admin":
                return True
        return False

    def signup(self, username, password, first_name, last_name, role="user"):
        if len(self.users) >= 4:
            return "Maximum number of users is 4 (1 admin, 3 users)."
        
        if username in self.users:
            return "Username already exists. Please choose another."
        
        if role == "admin" and self.is_admin_present():
            return "An admin user already exists. You cannot create another admin account."
        
        if not self.is_valid_password(password):
            return ("Password must be at least 7 characters long, "
                    "contain at least one uppercase letter and one special character. Please Sign Up again.")
        self.users[username] = User(username, password, first_name, last_name, role)
        self.save_users()
        return "Signup successful!"
    
    def delete_user(self, admin_username, target_username):
        if self.users[admin_username].role != "admin":
            return "Only Admins can deactivate users."
        
        if target_username in self.users:
            del self.users[target_username]
            self.save_users()
            return f"User {target_username} deactivated successfully."
        return "User not found."

    def login(self, username, password):
        if username not in self.users:
            return "Username not found."
        if self.users[username].password == password:
            return "Login successful!"
        return "Incorrect password."

    def save_users(self):
        file_path = "src/user_reg/user_reg.json"
        with open(file_path, 'w') as file:
            json.dump({username: vars(user) for username, user in self.users.items()}, file, indent=4)

    def load_users(self):
        file_path = "src/user_reg/user_reg.json"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.users = {username: User(**info) for username, info in data.items()}
        except FileNotFoundError:
            self.users = {}