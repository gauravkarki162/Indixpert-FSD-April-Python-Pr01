from pathlib import Path
import json
import re
from src.roles.role import Role

class UserManager:
    def __init__(self):
        self.users = []
        self.roles = Role.default_roles()
        self.load_users()

    def get_user_file_path(self):
        return Path(__file__).parent / 'user_registration.json'

    def generate_user_id(self):
        return max([user["user_id"] for user in self.users], default=0) + 1

    def signup(self, username, password, first_name, last_name, role="user"):
        if len(self.users) >= 4:
            return "Maximum number of users is 4 (1 admin, 3 users)."
        
        if any(user['username'] == username for user in self.users):
            return "Username already exists. Please choose another."
        
        if role == "admin" and any(user['role'] == "admin" for user in self.users):
            return "An admin user already exists. You cannot create another admin account."
        
        if not self.is_valid_password(password):
            return ("Password must be at least 7 characters long, "
                    "contain at least one uppercase letter and one special character. Please Sign Up again.")

        new_user = {
            "user_id": self.generate_user_id(),
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "role": role
        }
        self.users.append(new_user)
        self.save_users()
        return "Signup successful!"

    def login(self, username, password):
        user = next((user for user in self.users if user['username'] == username), None)
        if not user:
            return "Username not found."
        if user['password'] == password:
            return "Login successful!"
        return "Incorrect password."

    def delete_user(self, admin_username, target_username):
        admin_user = next((user for user in self.users if user['username'] == admin_username), None)
        target_user = next((user for user in self.users if user['username'] == target_username), None)

        if not admin_user or admin_user['role'] != "admin":
            return "Only Admins can deactivate users."
        
        if target_user:
            self.users = [user for user in self.users if user['username'] != target_username]
            self.save_users()
            return f"User {target_username} deactivated successfully."
        return "User not found."

    def is_valid_password(self, password):
        stripped_password = password.replace(" ", "")
        if len(stripped_password) < 7:
            return False
        if not re.search(r"[A-Z]", stripped_password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", stripped_password):
            return False
        return True

    def save_users(self):
        file_path = self.get_user_file_path()
        with open(file_path, 'w') as file:
            json.dump({"users": self.users}, file, indent=4)

    def load_users(self):
        file_path = self.get_user_file_path()
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.users = data.get("users", [])
        except FileNotFoundError:
            self.users = []