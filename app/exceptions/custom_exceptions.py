class BankingException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class InsufficientFundsError(BankingException):
    def __init__(self):
        super().__init__("Insufficient funds", 400)


class AccountFrozenError(BankingException):
    def __init__(self):
        super().__init__("Account is frozen", 400)


class UnauthorizedError(BankingException):
    def __init__(self):
        super().__init__("Unauthorized", 401)