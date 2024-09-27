class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, amount):
        self.quantity += amount

    def display_info(self):
        return f"ID: {self.product_id}, Name: {self.name},Rs. {self.price}, Quantity: {self.quantity}"

# product = Product(1, "laptop", 500000, 10)
# print(product.display_info())