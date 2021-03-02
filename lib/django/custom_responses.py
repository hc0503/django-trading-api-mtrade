from rest_framework.exceptions import APIException

class BadRequest(APIException):
    status_code = 400
    default_detail = 'The request cannot be fulfilled, please try again with different parameters.'
    default_code = 'bad_request'
