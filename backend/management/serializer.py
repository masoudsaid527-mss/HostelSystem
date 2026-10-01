from . models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(
        choices=[User.Role.STUDENT, User.Role.HOSTEL_OWNER]
    )
    address = serializers.CharField(max_length=100, write_only=True)
    phone = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password', 'role', 'gender',
                  'address', 'phone']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already used")
        return value

    def create(self, validated_data):
        address = validated_data.pop('address')
        phone = validated_data.pop('phone')
        password = validated_data.pop('password')

        with transaction.atomic():
            user = User.objects.create_user(password=password, **validated_data)

            if user.role == User.Role.STUDENT:
                Student.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    gender=user.gender,
                    address=address,
                    phone=phone,
                )
            else:
                HostelOwner.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    gender=user.gender,
                    address=address,
                    phone=phone,
                )
        return user

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data





class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class HostelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelOwner
        fields = '__all__'

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = '__all__'
        read_only_fields = ['owner', 'is_approved']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['student', 'status', 'total_amount', 'amount_paid']



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'