from src.inventory import Inventory
class Store:
    def __init__(self):
        self.inventory = Inventory()

    def add_product(self, product_id, name, price, quantity):
        return self.inventory.add_product(product_id, name, price, quantity)

    def update_stock(self, product_id, amount):
        return self.inventory.update_quantity(product_id, amount)

    def check_stock(self):
        return self.inventory.check_stock()

    def search_product(self, search_term):
        results = []
        for product in self.inventory.products.values():
            if str(product.product_id) == search_term or product.name.lower() == search_term.lower():
                results.append(product.display_info())
        return results if results else ["No products found."]