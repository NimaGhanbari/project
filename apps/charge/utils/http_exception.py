from rest_framework.exceptions import APIException

class CustomValidationException(APIException):
    def __init__(self, detail, status_code):
        self.detail = detail
        self.status_code = status_code

