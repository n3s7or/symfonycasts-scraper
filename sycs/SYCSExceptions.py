class SYCSException(Exception):
    pass


class CredentialsException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__('username or password not provided.')


class WrongRangeException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__("start or end must be greater than 1")


class ForbiddenException(SYCSException):
    pass
