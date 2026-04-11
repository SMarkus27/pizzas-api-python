class AppError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class BadRequestError(AppError):
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, status_code=400)


class UnprocessableError(AppError):
    def __init__(self, message: str = "Unprocessable entity"):
        super().__init__(message, status_code=422)


class InvalidPriceError(AppError):
    def __init__(self, price: float):
        self.message = f"Preço inválido: {price}. O preço deve ser maior que zero."
        super().__init__(self.message, status_code=400)


class InvalidNameError(AppError):
    def __init__(self):
        self.message = "O Nome deve ter no minimo 3 caracteres."
        super().__init__(self.message, status_code=400)


class InvalidIngredientError(AppError):
    def __init__(self):
        self.message = "O Ingrediente deve ter no minimo 3 caracteres."
        super().__init__(self.message, status_code=400)
