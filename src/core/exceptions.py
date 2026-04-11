class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class BadRequestException(AppException):
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, status_code=400)


class UnprocessableException(AppException):
    def __init__(self, message: str = "Unprocessable entity"):
        super().__init__(message, status_code=422)

class InvalidPriceException(AppException):
    def __init__(self, price: float):
        self.message = f"Preço inválido: {price}. O preço deve ser maior que zero."
        super().__init__(self.message, status_code=400)

class InvalidNameException(AppException):
    def __init__(self):
        self.message = f"O Nome deve ter no minimo 3 caracteres."
        super().__init__(self.message, status_code=400)

class InvalidIngredientException(AppException):
    def __init__(self):
        self.message = f"O Ingrediente deve ter no minimo 3 caracteres."
        super().__init__(self.message, status_code=400)
