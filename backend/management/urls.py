from django.urls import path
from . views import *
from . serializer import *
from . models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view()),
    path('students/', generic_api(Student, StudentSerializer)),
    path('students/<int:id>/', generic_api(Student, StudentSerializer)),
    path('hostel_owners/', generic_api(HostelOwner, HostelOwnerSerializer)),
    path('hostel_owners/<int:id>/', generic_api(HostelOwner, HostelOwnerSerializer)),
    path('hostels/<int:id>/', generic_api(Hostel, HostelSerializer)),
    path('hostels/', HostelListCreateView.as_view()),
    path('hostels/<int:id>/rooms/', generic_api(Room, RoomSerializer)),
    path('rooms/', RoomListCreateView.as_view()),
    path('rooms/<int:id>/', generic_api(Room, RoomSerializer)),
    path('bookings/', BookingListCreateView.as_view()),
    path('bookings/<int:id>/', generic_api(Booking, BookingSerializer)),
    path('payments/',PaymentListCreateView.as_view()),
    path('payments/<int:id>/', generic_api(Payment, PaymentSerializer)),
    path('notifications/', generic_api(Notification, NotificationSerializer)),
    path('notifications/<int:id>/', generic_api(Notification, NotificationSerializer)),
]