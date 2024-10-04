from src.store import Store
from src.user_reg.user_manager import UserManager

class UI:
    def __init__(self):
        self.store = Store()
        self.user_manager = UserManager()
        self.is_authenticated = False
        self.username = None

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

            if choice == '1':
                first_name = input("Enter first name: ").strip()
                last_name = input("Enter last name: ").strip()
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                role = input("Enter role (user/admin): ").strip().lower()
                if role not in ["user", "admin"]:
                    role = "user"
                message = self.user_manager.signup(username, password, first_name, last_name, role)
                print(message)

            elif choice == '2':
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                message = self.user_manager.login(username, password)
                print(message)
                if message == "Login successful!":
                    self.is_authenticated = True
                    self.username = username
                    self.handle_post_login_menu()

            elif choice == '3':
                print("Exit.")
                return

            else:
                print("Invalid option. Please try again.")
    
    def handle_post_login_menu(self):
        user_role = self.user_manager.users[self.username].role
        if user_role == "admin":
            self.display_admin_menu_loop()
        else:
            self.handle_inventory_menu()

    def handle_inventory_menu(self):
        in_inventory_menu = True
        while in_inventory_menu:
            self.display_inventory_menu()
            choice = input("Select an option: ")

            if choice == '1':
                name = input("Enter Product Name: ").strip().lower()
                if any(product.name.strip().lower() == name.lower() for product in self.store.inventory.products.values()):
                    print(f"Product with the name '{name}' already exists. Use the update stock function.")
                    continue

                price_valid = False
                while not price_valid:
                    try:
                        price = int(input("Enter Product Price: "))
                        if price > 0:
                            price_valid = True
                        else:
                            print("Price must be greater than 0.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number for the price.")

                quantity_valid = False
                while not quantity_valid:
                    try:
                        quantity = int(input("Enter Stock Quantity: "))
                        if quantity > 0:
                            quantity_valid = True
                        else:
                            print("Quantity must be greater than 0.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                message = self.store.add_product(name, price, quantity, added_by=self.username)
                print(message)
                self.pause()

            elif choice == '2':
                product_identifier = input("Enter Product ID or Name to update: ").strip().lower()
                amount = input("Enter quantity to add/sell (- for selling): ")
                try:
                    amount = int(amount)
                    message = self.store.update_stock(product_identifier, amount, username=self.username, role=self.user_manager.users[self.username].role)
                    print(message)
                except ValueError:
                    print("Invalid input. Please enter a valid number for the quantity.")
                self.pause()

            elif choice == '3':
                print(self.store.check_stock(self.username, self.user_manager.users[self.username].role))
                self.pause()

            elif choice == '4':
                search_term = input("Enter Product ID or Name to search: ").strip().lower()
                results = self.store.search_product(search_term, username=self.username, role=self.user_manager.users[self.username].role)
                print("\n".join(results))
                self.pause()

            elif choice == '5':
                product_identifier = input("Enter Product ID or Name to delete: ").strip().lower()
                message = self.store.delete_product(product_identifier, username=self.username, role=self.user_manager.users[self.username].role)
                print(message)
                self.pause()

            elif choice == '6':
                print(f"Logging out {self.username}...")
                self.is_authenticated = False
                in_inventory_menu = False

            else:
                print("Invalid option. Please try again.")
                self.pause()

    def display_admin_menu_loop(self):
        continue_menu = True
        while continue_menu:
            self.display_admin_menu()
            choice = input("Select an option: ")

            if choice == '1':
                self.display_dashboard()

            elif choice == '2':
                target_username = input("Enter username to deactivate: ").strip()
                message = self.user_manager.delete_user(self.username, target_username)
                print(message)

            elif choice == '3':
                print(f"Logging out {self.username}...")
                self.is_authenticated = False
                continue_menu = False

            else:
                print("Invalid option. Please try again.")
                self.pause()

    def display_dashboard(self):
        dashboard = self.store.view_dashboard(self.username, self.user_manager.users[self.username].role)
        print(dashboard)
        self.pause()