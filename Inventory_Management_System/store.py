from Inventory_Management_System.inventory import Inventory
class Store:
    def __init__(self):
        self.inventory = Inventory()

    def add_product(self, product_id, name, price, quantity):
        return self.inventory.add_product(product_id, name, price, quantity)

    def update_stock(self, product_id, amount):
        return self.inventory.update_quantity(product_id, amount)

    def check_stock(self):
        return self.inventory.check_stock()