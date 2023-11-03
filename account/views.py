from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ActivationSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ForgotPasswordCompleteSerializer,
    UsersSerializer,
    # CategorySerializer
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from .tasks import send_password_celery
from .models import Category
from .permissions import IsAuthorPermission


# Create your views here.

User = get_user_model()


# class CategoryView(ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminUser]


class UsersView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = [IsAuthorPermission, IsAdminUser]


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Good, Registration successful', status=201)


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response(
                'User not found', status=400
            )
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response(
            'Account activate', status=200
        )


class ActivationViewCode(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer)
    def post(self, request):
        serializer = ActivationSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response(
                'Account Successfully Activate'
            )


class LoginViewEmail(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        # logger.error('Ошибка ChangePasswordV')
        return Response(
            'Пароль успешно обнавлен', status=200
        )


class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data
        email = user_data['email']

        user = User.objects.get(email=email)
        user.create_forgot_password_code()
        user.save()

        send_password_celery.delay(user.email, user.forgot_password_code)
        return Response({'Код восстановления отправлен на ваш email.'}, status=status.HTTP_200_OK)


class ForgotPasswordCompleteView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer)
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        # logger.error('Ошибка ChangePasswordV')
        return Response(
            'Пароль успешно обнавлен', status=200
        )



