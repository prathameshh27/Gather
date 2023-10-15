import uuid
from rest_framework.response import Response

def custom_id():
    """generates 8 character alphanumeric ID """
    unique_id = str(uuid.uuid4())[:8]
    return unique_id


# Returns errors encountered while serialization
def get_validation_errors(serializer) -> dict:
    """Input: instance of DRF Serializer"""

    errors = {}
    for field_name, field_errors in serializer.errors.items():
        errors[field_name] = list(field_errors)
    return errors


# Decorator to handle Response exceptions
def resp_excp_handler(func):
    """Input: Request Handler"""
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