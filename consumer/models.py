from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
class Workers(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to="workers/")
    number=models.CharField(max_length=10)
    role=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class WorkerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="worker_profile"
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    role = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class works(models.Model):
    types=models.CharField(max_length=100)
    image=models.ImageField(upload_to="workers/")
    exp=models.CharField(max_length=10)
    review=models.CharField(max_length=200)
    def __str__(self):
        return self.types





class Booking(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_bookings"
    )

    work_name = models.CharField(max_length=100)

    customer_mobile = models.CharField(max_length=15)

    work_details = models.TextField()

    booking_date = models.DateField()

    booking_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    def __str__(self):
        return self.work_name
class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="booking_notifications"
    )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message

