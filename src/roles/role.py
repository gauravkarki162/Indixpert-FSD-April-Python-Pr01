class Role:
    def __init__(self, name, can_add_product=False, can_update_stock=False, can_view_dashboard=False, can_deactivate_user=False):
        self.name = name
        self.can_add_product = can_add_product
        self.can_update_stock = can_update_stock
        self.can_view_dashboard = can_view_dashboard
        self.can_deactivate_user = can_deactivate_user

    def __str__(self):
        return self.name

    @staticmethod
    def default_roles():
        return {
            "user": Role(name="user", can_add_product=True, can_update_stock=True),
            "admin": Role(name="admin", can_add_product=True, can_update_stock=True, can_view_dashboard=True, can_deactivate_user=True),
        }