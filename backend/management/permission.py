from rest_framework.permissions import BasePermission
from .models import *
from .serializer import *
from rest_framework.viewsets import ModelViewSet

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsHostelOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'hostel_owner'


class HostelPermission(BasePermission):
    def has_permission(self ,request,view):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user == 'admin':
            return True
        if view.action in ['list','retrieve']:
            return user.role in ['student','hostel_owner']
        if view.action in ['create','destroy','update','partial_update']:
            return user.role == 'hostel_owner'
        return False

class RoomPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.action in ['list', 'retrieve']:
            return request.user.role in ['student', 'hostel_owner']
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.role == 'hostel_owner'
        return False

class BookingPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.action in ['list','retrieve','create','update','partial_update','destroy']:
            return request.user.role in ['student', 'hostel_owner']
        return False

class PaymentPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.action in ['create','list','retrieve']:
            return request.user.role == 'student'
        if view.action in ['verify','update','partial_update','destroy']:
            return request.user.role == 'hostel_owner'
        return False

class NotificationPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.action in ['list']:
            return request.user.role == 'student'
        if view.action in ['retrieve','create','update','partial_update','destroy']:
            return request.user.role == 'hostel_owner'
        return False






class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [RoomPermission]

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsStudent]

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsStudent]

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsStudent]

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdmin]

