import json
from Inventory_Management_System.product import Product

class Inventory:
    def __init__(self):
        self.products = {}
        self.load_inventory()

    def add_product(self, product_id, name, price, quantity):
        if product_id in self.products:
            return f"Product ID {product_id} already exists."
        self.products[product_id] = Product(product_id, name, price, quantity)
        self.save_inventory()
        return f"Product {name} added successfully."

    def update_quantity(self, product_id, amount):
        if product_id in self.products:
            product = self.products[product_id]
            if amount < 0 and abs(amount) > product.quantity:
                return f"Cannot sell {abs(amount)} units; only {product.quantity} in stock."
            product.update_quantity(amount)
            self.save_inventory()
            action = "added to" if amount > 0 else "sold from"
            return f"{abs(amount)} units {action} {product.name}. New quantity: {product.quantity}."
        else:
            return f"Product ID {product_id} not found."

    def check_stock(self):
        if not self.products:
            return "No products in inventory."
        stock_info = []
        for product in self.products.values():
            stock_info.append(product.display_info())
            if product.quantity < 5:
                stock_info.append(f"{product.name} needs restocking.")
        return "\n".join(stock_info)

    def save_inventory(self):
        file_path = r"C:\Users\lenovo\Documents\python(for class)\Project(IMS)\Indixpert-FSD-April-Python-Pr01\Inventory_Management_System\inventory.json"
        with open(file_path, 'w') as file:
            json.dump({pid: vars(product) for pid, product in self.products.items()}, file, indent=4)

    def load_inventory(self):
        file_path = r"C:\Users\lenovo\Documents\python(for class)\Project(IMS)\Indixpert-FSD-April-Python-Pr01\Inventory_Management_System\inventory.json"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.products = {pid: Product(**info) for pid, info in data.items()}
        except FileNotFoundError:
            self.products = {}