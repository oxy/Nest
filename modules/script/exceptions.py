"""
Exceptions raised by the interpreter.
"""


class InterpreterError(Exception):
    """
    Raised when the interpreter fails to execute any code.
    """
    pass


class HTTPError(InterpreterError):
    """
    Raised when the HTTP request returns an invalid response code.
    """
    pass


class ProtectionError(InterpreterError):
    """
    Signals interpreter protection triggering a halt in evaluating the code.
    """

    def __init__(self, max_allowed):
        self.max = max_allowed
        super()


class WhileProtection(ProtectionError):
    """
    Raised when a while loop exceeds the maximum number of allowed repetitions.
    """
    pass


class CallProtection(ProtectionError):
    """
    Raised when a protected function is called too many times.
    """
    pass
