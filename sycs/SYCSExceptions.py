class SYCSException(Exception):
    pass


class CredentialsException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__('username or password not provided.')


class WrongRangeException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__("start or end must be equal or greater than 1 and start must be equal or "
                                            "lower than end")


class ForbiddenException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__("access forbidden, wrong credentials o_0 !!?")
