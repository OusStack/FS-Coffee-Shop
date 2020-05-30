"""Constants module."""

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_NO_CONTENT = 204
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404
STATUS_METHOD_NOT_ALLOWED = 405
STATUS_UNPROCESSABLE_ENTITY = 422
STATUS_INTERNAL_SERVER_ERROR = 500

STATUS_CODE_MESSAGES = {
    STATUS_OK: 'Ok',
    STATUS_CREATED: 'Created',
    STATUS_NO_CONTENT: 'No Content',
    STATUS_BAD_REQUEST: 'Bad Request',
    STATUS_UNAUTHORIZED: 'Unauthorized',
    STATUS_FORBIDDEN: 'Forbidden',
    STATUS_NOT_FOUND: 'Not Found',
    STATUS_METHOD_NOT_ALLOWED: 'Method Not Allowed',
    STATUS_UNPROCESSABLE_ENTITY: 'Unprocessable Entity',
    STATUS_INTERNAL_SERVER_ERROR: 'Internal Server Error',
}

MISSING_AUTHORIZATION = 'Authorization header in request headers is mandatory.'
MISSING_BEARER = 'Authorization header must start with "Bearer".'
MISSING_TOKEN = 'Authorization header must have token.'
MISSING_BEARER_TOKEN = 'Authorization header must be a Bearer token.'
AUTHORIZATION_MALFORMED = 'Authorization malformed.'
TOKEN_EXPIRED = 'Token Expired.'
INCORRECT_CLAIMS = 'Incorrect claims. Please, check the audience and issuer.'
UNABLE_TO_PARSE = 'Unable to parse authentication token.'
INAPPROPRIATE_KEY = 'Unable to find the appropriate key.'
