from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        title = args[0].request.data.get("title", "")
        description = args[0].request.data.get("description", "")
        if not title and not description:
            return Response(
                data={
                    "message": "Both title and description are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated