class CartNotFound(Exception):
    """Raised when a cart is not found."""
    def __init__(self, message="Cart not found."):
        self.message = message
        super().__init__(self.message)

class InvalidProductExcepton(Exception):
    """Raised when a product ID is invalid."""
    def __init__(self, message="Invalid product."):
        self.message = message
        super().__init__(self.message)

class UserNotfoundException(Exception):
    """Raised when a user is not found."""
    def __init__(self, message="User not found."):
        self.message = message
        super().__init__(self.message)

class DatabaseException(Exception):
    """Raised when there is a database error."""
    def __init__(self, message="Database error."):
        self.message = message
        super().__init__(self.message)