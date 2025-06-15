from .base import *
from ..serializers import (
    RegisterSerializer,
    RegisterResponseSerializer
)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegisterLoginThrottle]

    # Register a new user
    @swagger_auto_schema(
        tags=["Authentication"],
        operation_id="auth_register",
        operation_description="Register a new user & get JWT tokens",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                'Success: Created',
                RegisterResponseSerializer
            ),
            400: 'Error: Bad request',
            429: 'Error: Too many requests',
            500: 'Error: Internal server error'
        }
    )
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = {
                'refresh': str(refresh),
                'access': access_token,
                'id': user.id,
                'username': user.username,
            }

            return Response(
                RegisterResponseSerializer(response).data,
                status=status.HTTP_201_CREATED
            )
        
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            # Log the error for debugging
            logger.error(
                f"Error in RegisterView.post(): {str(e)}",
                exc_info=True
            )

            return Response(
                {"detail": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
