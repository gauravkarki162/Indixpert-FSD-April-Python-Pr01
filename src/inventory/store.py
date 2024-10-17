from src.inventory.inventory import Inventory

class Store:
    def __init__(self):
        self.inventory = Inventory()

    def add_product(self, name, price, quantity, added_by):
        return self.inventory.add_product(name, price, quantity, added_by)

    def update_stock(self, product_identifier, amount, username, role):
        try:
            product_id = int(product_identifier)
            product = self.inventory.products.get(product_id)
        except ValueError:
            product = next((p for p in self.inventory.products.values() if p.name.lower() == product_identifier.lower()), None)

        if not product:
            return f"Product '{product_identifier}' not found."

        if role == "user" and product.added_by != username:
            return "You are not allowed to update this product."

        return self.inventory.update_quantity(product.product_id, amount)

    def check_stock(self, username, role):
        if role == "admin":
            return self.inventory.check_stock()
        return self.inventory.view_user_products(username)

    def delete_product(self, product_identifier, username, role):
        try:
            product_id = int(product_identifier)
            product = self.inventory.products.get(product_id)
        except ValueError:
            product = next((p for p in self.inventory.products.values() if p.name.lower() == product_identifier.lower()), None)

        if not product:
            return f"Product '{product_identifier}' not found."

        if role == "user" and product.added_by != username:
            return "You are not allowed to delete this product."

        return self.inventory.delete_product(product.product_id)

    def search_product(self, search_term, username, role):
        results = []
        for product in self.inventory.products.values():
            if (role == "admin" or product.added_by == username) and \
               (str(product.product_id) == search_term or product.name.lower() == search_term.lower()):
                results.append(product.display_info())
        return results if results else ["No products found."]
    
    def view_dashboard(self, username, role):
        if role == "admin":
            return self.inventory.check_stock()
        return self.inventory.view_user_products(username)