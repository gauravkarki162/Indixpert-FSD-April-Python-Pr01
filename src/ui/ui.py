from src.inventory.store import Store
from src.users.user_manager import UserManager

class UI:
    def __init__(self):
        self.store = Store()
        self.user_manager = UserManager()
        self.is_authenticated = False
        self.username = None

    def get_user_details(self, with_role=False):
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        role = None
        if with_role:
            role = input("Enter role (user/admin): ").strip().lower()
            if role not in ["user", "admin"]:
                role = "user"
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password,
            'role': role
        }

    def display_menu(self):
        print("\nInventory Management System")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")

    def display_inventory_menu(self):
        print("\nInventory Management System - Inventory Menu")
        print("1. Add Product")
        print("2. Update Stock")
        print("3. Check Stock Levels")
        print("4. Search Product")
        print("5. Delete Product")
        print("6. Logout")
        
    def display_admin_menu(self):
        print("\nAdmin Menu")
        print("1. View Products")
        print("2. Deactivate User")
        print("3. Logout")

    def pause(self):
        input("\nPress any key to continue...")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select an option: ")

            match choice:
                case '1':  # Signup
                    user_details = self.get_user_details(with_role=True)
                    message = self.user_manager.signup(
                        user_details['username'],
                        user_details['password'],
                        user_details['first_name'],
                        user_details['last_name'],
                        user_details['role']
                    )
                    print(message)

                case '2':  # Login
                    username = input("Enter username: ").strip()
                    password = input("Enter password: ").strip()
                    message = self.user_manager.login(username, password)
                    print(message)
                    if message == "Login successful!":
                        self.is_authenticated = True
                        self.username = username
                        self.handle_post_login_menu()

                case '3':
                    print("Exit.")
                    return

                case _:
                    print("Invalid option. Please try again.")
    
    def handle_post_login_menu(self):
        user_role = self.user_manager.users[self.get_user_index(self.username)]['role']
        if self.user_manager.roles[user_role].can_view_dashboard:
            self.display_admin_menu_loop()
        else:
            self.handle_inventory_menu()

    def handle_inventory_menu(self):
        in_inventory_menu = True
        while in_inventory_menu:
            self.display_inventory_menu()
            choice = input("Select an option: ")

            match choice:
                case '1':  # Add Product
                    name = input("Enter Product Name: ").strip().lower()
                    if any(product.name.strip().lower() == name.lower() for product in self.store.inventory.products.values()):
                        print(f"Product with the name '{name}' already exists. Use the update stock function.")
                        continue

                    price = self.get_valid_input("Enter Product Price: ", int, min_value=1)
                    quantity = self.get_valid_input("Enter Stock Quantity: ", int, min_value=1)

                    message = self.store.add_product(name, price, quantity, added_by=self.username)
                    print(message)
                    self.pause()

                case '2':  # Update Stock
                    product_identifier = input("Enter Product ID or Name to update: ").strip().lower()
                    amount = self.get_valid_input("Enter quantity to add/sell (- for selling): ", int)
                    message = self.store.update_stock(product_identifier, amount, username=self.username, role=self.user_manager.users[self.get_user_index(self.username)]['role'])
                    print(message)
                    self.pause()

                case '3':  # Check Stock
                    print(self.store.check_stock(self.username, self.user_manager.users[self.get_user_index(self.username)]['role']))
                    self.pause()

                case '4':  # Search Product
                    search_term = input("Enter Product ID or Name to search: ").strip().lower()
                    results = self.store.search_product(search_term, username=self.username, role=self.user_manager.users[self.get_user_index(self.username)]['role'])
                    print("\n".join(results))
                    self.pause()

                case '5':  # Delete Product
                    product_identifier = input("Enter Product ID or Name to delete: ").strip().lower()
                    message = self.store.delete_product(product_identifier, username=self.username, role=self.user_manager.users[self.get_user_index(self.username)]['role'])
                    print(message)
                    self.pause()

                case '6':
                    print(f"Logging out {self.username}...")
                    self.is_authenticated = False
                    in_inventory_menu = False

                case _:
                    print("Invalid option. Please try again.")
                    self.pause()

    def display_admin_menu_loop(self):
        continue_menu = True
        while continue_menu:
            self.display_admin_menu()
            choice = input("Select an option: ")

            match choice:
                case '1':  # View Products
                    self.display_dashboard()

                case '2':  # Deactivate User
                    target_username = input("Enter username to deactivate: ").strip()
                    message = self.user_manager.delete_user(self.username, target_username)
                    print(message)

                case '3':
                    print(f"Logging out {self.username}...")
                    self.is_authenticated = False
                    continue_menu = False

                case _:
                    print("Invalid option. Please try again.")
                    self.pause()

    def display_dashboard(self):
        dashboard = self.store.view_dashboard(self.username, self.user_manager.users[self.get_user_index(self.username)]['role'])
        print(dashboard)
        self.pause()

    def get_user_index(self, username):
        return next((i for i, user in enumerate(self.user_manager.users) if user['username'] == username), -1)

    def get_valid_input(self, prompt, cast_type, min_value=None):
        while True:
            try:
                value = cast_type(input(prompt).strip())
                if min_value is not None and value < min_value:
                    raise ValueError
                return value
            except ValueError:
                print(f"Invalid input. Please enter a valid {cast_type.__name__} greater than {min_value}.")