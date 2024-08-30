from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import UserToken

def token_required(view_func):
    """
    Decorator for class-based views
    """
    @wraps(view_func)
    def decorated_function(self, request, *args, **kwargs):
        try:
            token = request.headers.get('token')

            if not token:
                return Response({"message": "Token header is missing"}, status=status.HTTP_400_BAD_REQUEST)

            user_token = UserToken.objects.filter(token=token, is_active=True).first()

            if not user_token:
                return Response({"message": "Invalid or inactive token"}, status=status.HTTP_401_UNAUTHORIZED)

            return view_func(self, request, *args, **kwargs)

        except Exception as error:
            return Response({"message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return decorated_function