from django.shortcuts import render
from . models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . serializer import *
from rest_framework.viewsets import ModelViewSet
from .permission import *
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serializer import *
from rest_framework.exceptions import PermissionDenied


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]  # must awe logged in

class HostelOwnerViewSet(ModelViewSet):
    queryset = HostelOwner.objects.all()
    serializer_class = HostelOwnerSerializer
    permission_classes = [IsAuthenticated]  # must awe logged in

#Create Hostel
class HostelListCreateView(ListCreateAPIView):
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Hostel.objects.all()
        if user.role == 'hostel_owner':
            return Hostel.objects.filter(owner=user.hostel_owner_profile)
        return Hostel.objects.filter(is_approved=True,is_available=True)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'hostel_owner':
            raise PermissionDenied("You don't have permission to create hostel")
        serializer.save(owner=user.hostel_owner_profile)

#Create Room
class RoomListCreateView(ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Room.objects.all()
        if user.role == 'hostel_owner':
            return Room.objects.filter(hostel__owner=user.hostel_owner_profile)
        return Room.objects.filter(hostel__is_approved=True, status='available')

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'hostel_owner':
            raise PermissionDenied("Hostel Owner Only")
        hostel = serializer.validated_data['hostel']
        if hostel.owner != user.hostel_owner_profile:
            raise PermissionDenied("This hostel is not yours.")
        serializer.save()

#Create Booking
class BookingListCreateView(ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Booking.objects.all()
        if user.role == 'hostel_owner':
            return Booking.objects.filter(
                room__hostel__owner=user.hostel_owner_profile
            )
        return Booking.objects.filter(student=user.student_profile)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'student':
            raise PermissionDenied("Only Students can book.")
        room = serializer.validated_data['room']
        serializer.save(
            student=user.student_profile,
            total_amount=room.price_per_semester,
        )

class PaymentListCreateView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.all()
        if user.role == 'hostel_owner':
            return Payment.objects.filter(booking__room__hostel__owner=user.hostel_owner_profile)
        return Payment.objects.filter(booking__student=user.student_profile)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'student':
            raise PermissionDenied("Only Students can make payments.")
        booking = serializer.validated_data['booking']
        if booking.student != user.student_profile:
            raise PermissionDenied("This booking is not yours.")
        serializer.save(amount_paid=serializer.validated_data['amount_paid'])


































































def generic_api(model_class, serializer_class):
    @api_view(['GET','POST', 'DELETE', 'PUT'])
    # @permission_classes([IsAuthenticated])


    def api(request, id = None):
        if request.method == 'GET':
            if id:
                try:
                    instance = model_class.objects.get(id = id)
                    serializer = serializer_class(instance)
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message':'Object Not Found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                instance = model_class.objects.all()
                serializer = serializer_class(instance, many = True)
                return Response(serializer.data)

        elif request.method == 'POST':
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                    serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Success
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # If serializer is invalid


        elif request.method == 'DELETE':
            if id:
                try:
                    instance = model_class.objects.get(id = id)
                    instance.delete()
                    return Response({'message':'Delete Successfully'})
                except model_class.DoesNotExist:
                    return Response({'message':'Object Not Found'}, status=status.HTTP_404_NOT_FOUND)


        elif request.method == 'PUT':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                    return Response(serializer.data)


                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

    return api
# Create your views here.
