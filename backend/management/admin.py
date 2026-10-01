from django.contrib import admin
from . models import *

admin.site.register(Student)
admin.site.register(Hostel)
admin.site.register(HostelOwner)
admin.site.register(Room)
admin.site.register(Notification)
admin.site.register(Payment)
admin.site.register(User)
admin.site.register(Booking)

# Register your models here.
