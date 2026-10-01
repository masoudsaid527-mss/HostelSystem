from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        HOSTEL_OWNER = 'hostel_owner', 'Hostel Owner'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
    @property
    def is_hostel_owner(self):
        return self.role == self.Role.HOSTEL_OWNER
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN





    def __str__(self):
        return self.username

gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
    related_name='student_profile',
    limit_choices_to={'role': User.Role.STUDENT}
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(unique=True,default='')
    age = models.IntegerField(default=0)
    date_of_birth = models.DateField()
    year_of_study = models.IntegerField(default=1)
    gender = models.CharField(max_length=10, choices=gender_choices, default='male')
    duration = models.CharField(max_length=50, default="1 Month")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class HostelOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
    related_name="hostel_owner_profile",
    limit_choices_to={'role': User.Role.HOSTEL_OWNER}
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,unique=True)
    gender = models.CharField(max_length=10,choices=gender_choices, default='male')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Hostel(models.Model):
    owner = models.ForeignKey(HostelOwner, on_delete=models.CASCADE,
    related_name='hostels')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    total_rooms = models.IntegerField(default=0)
    available_rooms = models.IntegerField(default=0)
    rules = models.TextField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15,unique=True)
    contact_email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default =False)

    def __str__(self):
        return self.name


class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        MAINTENANCE = 'maintenance', 'Maintenance'
        BOOKED = 'booked', 'Booked'
    
    room_capacity = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
    ]

    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20,unique=True)
    capacity = models.CharField(max_length=20,choices=room_capacity,default='triple')
    price_per_semester = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    status = models.CharField(max_length=20, default='available',choices = Status.choices)

    def __str__(self):
        return f"Room {self.room_number} - {self.hostel.name}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    status = models.CharField(max_length=20, default='pending',choices = Status.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    booked_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        return self.total_amount - self.amount_paid

    def __str__(self):
        return f"Booking by {self.student.first_name} {self.student.last_name}"


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
        MOBILE_PAYMENT = 'mobile_payment', 'Mobile Payment'
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, default='cash',choices = PaymentMethod.choices)
    status = models.CharField(max_length=20, default='pending',choices = Status.choices)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.student.first_name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"
