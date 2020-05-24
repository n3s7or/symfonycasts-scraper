class SYCSException(Exception):
    pass


class CredentialsException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__('username or password not provided.')


class InvalidCredentialsException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__('wrong username or password.')


class WrongRangeException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__("start or end must be equal or greater than 1 and start must be equal or "
                                            "lower than end")


class ForbiddenException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__("access forbidden, perhaps unpaid subscription o_0 ?")


class CourseNotFoundException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__("invalid course")


class TooManyException(SYCSException):
    def __init__(self):
        super(SYCSException, self).__init__("on auth server response: too many, slow down the process")