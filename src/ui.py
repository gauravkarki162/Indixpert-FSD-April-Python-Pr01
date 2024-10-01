from src.store import Store
from src.user_reg.user_manager import UserManager

class UI:
    def __init__(self):
        self.store = Store()
        self.user_manager = UserManager()
        self.is_authenticated = False

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
        print("5. Logout")

    def run(self):
        while True:
            if not self.is_authenticated:
                self.display_menu()
                choice = input("Select an option: ")

                if choice == '1':
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    message = self.user_manager.signup(username, password, first_name, last_name)
                    print(message)

                elif choice == '2':
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    message = self.user_manager.login(username, password)
                    print(message)
                    if message == "Login successful!":
                        self.is_authenticated = True

                elif choice == '3':
                    print("Exit.")
                    return

                else:
                    print("Invalid option. Please try again.")
            else:
                self.display_inventory_menu()
                choice = input("Select an option: ")

                if choice == '1':
                    product_id_valid = False
                    while not product_id_valid:
                        try:
                            product_id = int(input("Enter Product ID: "))
                            if product_id in self.store.inventory.products:
                                print(f"Product ID {product_id} already exists.")
                                continue
                            product_id_valid = True
                        except ValueError:
                            print("Please enter a valid Product ID.")

                    name = input("Enter Product Name: ").strip()
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

                    message = self.store.add_product(product_id, name, price, quantity)
                    print(message)

                elif choice == '2':
                    product_id = input("Enter Product ID: ")
                    try:
                        product_id = int(product_id)
                    except ValueError:
                        print("Invalid Product ID.")
                        continue
                    
                    if product_id not in self.store.inventory.products:
                        print(f"Product ID {product_id} not found.")
                        continue
                    
                    amount_valid = False
                    while not amount_valid:
                        try:
                            amount = int(input("Enter stock update (- for sale): "))
                            amount_valid = True
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    
                    message = self.store.update_stock(product_id, amount)
                    print(message)

                elif choice == '3':
                    stock_info = self.store.check_stock()
                    print(stock_info)

                elif choice == '4':
                    search_term = input("Enter Product ID or Name to search: ").strip()
                    results = self.store.search_product(search_term)
                    for result in results:
                        print(result)

                elif choice == '5':
                    self.is_authenticated = False
                    print("Log out successfull.")
                else:
                    print("Invalid option. Please try again.")