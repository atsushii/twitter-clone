from rest_framework import generics, response, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model, login, logout

from user.serializers import UserSerializer, LoginSerializer


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return response.Response()
