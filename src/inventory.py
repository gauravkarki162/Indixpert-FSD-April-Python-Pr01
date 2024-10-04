from pathlib import Path
import json
from src.product import Product

class Inventory:
    def __init__(self):
        self.products = {}
        self.user_last_product_id = {}
        self.load_inventory()
        
    def generate_product_id(self, added_by):
        if added_by not in self.user_last_product_id:
            self.user_last_product_id[added_by] = 0
        new_id = self.user_last_product_id[added_by] + 1
        while new_id in self.products:
            new_id += 1
        self.user_last_product_id[added_by] = new_id
        return new_id
    
    def get_inventory_file_path(self):
        base_path = Path(__file__).resolve().parent
        return base_path / 'inventory' / 'inventory.json'

    def add_product(self, name, price, quantity, added_by):
        product_id = self.generate_product_id(added_by)
        if product_id in self.products:
            return f"Product ID {product_id} already exists with the name '{self.products[product_id].name}'."
        self.products[product_id] = Product(product_id, name, price, quantity, added_by)
        self.save_inventory()
        return f"Product {name} added successfully by {added_by} with ID {product_id}."
    
    def view_user_products(self, username):
        user_products = [product.display_info() for product in self.products.values() if product.added_by == username]
        if not user_products:
            return "No products found for the user."
        return "\n".join(user_products)

    def update_quantity(self, product_id, amount):
        product_id = int(product_id)
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

    def delete_product(self, product_id):
        product_id = int(product_id)
        if product_id in self.products:
            removed_product = self.products.pop(product_id)
            self.save_inventory()
            return f"Product '{removed_product.name}' (ID: {product_id}) deleted successfully."
        else:
            return f"Product ID {product_id} not found."

    def save_inventory(self):
        file_path = self.get_inventory_file_path()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump({
                'products': {pid: vars(product) for pid, product in self.products.items()},
                'user_last_product_id': self.user_last_product_id
            }, file, indent=4)

    def load_inventory(self):
        file_path = self.get_inventory_file_path()
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.products = {
                    int(pid): Product(**info) for pid, info in data.get('products', {}).items()
                }
                self.user_last_product_id = data.get('user_last_product_id', {})
        except FileNotFoundError:
            self.products = {}
            self.user_last_product_id = {}