class BaseException(Exception):
    http_code = 400


class DuplicateUser(BaseException):
    pass


class NotFound(BaseException):
    http_code = 404


class OperationAlreadyExists(BaseException):
    pass


class BadParams(BaseException):
    http_code = 500


class NotEnoughFunds(BaseException):
    pass


class MaxRetryCount(BaseException):
    http_code = 500
