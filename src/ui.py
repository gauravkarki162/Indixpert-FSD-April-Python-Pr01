from src.store import Store

class UI:
    def __init__(self):
        self.store = Store()

    def display_menu(self):
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Update Stock")
        print("3. Check Stock Levels")
        print("4. Search Product")
        print("5. Exit")

    def run(self):
        while True:
            self.display_menu()
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
                print("Exit.")
                return
            else:
                print("Invalid option. Please try again.")