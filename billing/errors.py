class BaseException(Exception):
    http_code = 500


class DuplicateUser(BaseException):
    http_code = 400


class NotFound(BaseException):
    http_code = 404


class OperationAlreadyExists(BaseException):
    http_code = 400


class NotEnoughFunds(BaseException):
    http_code = 400
