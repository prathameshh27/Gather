import uuid
from rest_framework.response import Response


# Typically used for replacing the default sequential IDs in the model 
def custom_id():
    """generates 8 character alphanumeric ID"""
    unique_id = str(uuid.uuid4())[:8]
    return unique_id


# Returns errors encountered while serialization
def get_validation_errors(serializer) -> dict:
    """Input: instance of DRF Serializer"""

    errors = {}
    for field_name, field_errors in serializer.errors.items():
        errors[field_name] = list(field_errors)
    return errors


# Decorator for handling Response exceptions
def resp_excp_handler(func):
    """Input: fuction based view"""
    def wrapper(*args,**kwargs):
        msg = {"message": " The request could not be fulfilled"}

        try:
            response_data = func(*args, **kwargs)
            return response_data
        except Exception as excp:
            msg["error"] = str(excp)
            response_data = Response(msg, status=500)
            return response_data
    return wrapper


# Decorator for Checking if the logged in user has superuser privileges.
def superuser_required(func):
    """Input: fuction based view"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            response_data = func(request, *args, **kwargs)
            return response_data
        else:
            response, http_status = {"message" : "You are not authorized to perform this operation"}, 403
            return Response(data=response, status=http_status)
    return wrapper