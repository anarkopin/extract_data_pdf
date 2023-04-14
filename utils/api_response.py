from rest_framework.response import Response
from datetime import datetime

class CustomResponse(Response):
    def __init__(self, data=None, status=None, message=None, error=None, *args, **kwargs):
        response_data = {
            "status": status,
            "data": data,
            "message": message,
            "timestamp": datetime.now(),
        }
        if error is not None:
            if isinstance(error, str):
                response_data["error"] = error
            else:
                response_data.update(error)

        super().__init__(response_data, status=status)