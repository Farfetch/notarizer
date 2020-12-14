class NotarizerException(Exception):
    def __init__(self, error_code, error_message):
        super().__init__(error_message)
        self.error_code = error_code


class NoSignatureFound(NotarizerException):
    def __init__(self, error_message):
        super().__init__(10, error_message)


class InvalidLabelSignature(NotarizerException):
    def __init__(self, error_message):
        super().__init__(11, error_message)


class VerificationFailure(NotarizerException):
    def __init__(self, error_message):
        super().__init__(12, error_message)


class ImageNotFound(NotarizerException):
    def __init__(self, error_message):
        super().__init__(14, error_message)


class SigningError(NotarizerException):
    def __init__(self, reason):
        super().__init__(16, "Error Creating Signed Docker Image")
        self.reason = reason


class PublicKeyNotFound(NotarizerException):
    def __init__(self):
        super().__init__(13, "No Public Key Provided")


class PrivateKeyNotFound(NotarizerException):
    def __init__(self):
        super().__init__(15, "No Private Key Provided")
