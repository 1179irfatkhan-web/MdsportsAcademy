
from django.db import models
from django.utils import timezone
from accounts.models import User

department = (
    ('Judo', "Judo"),
    ('Wrestling', "Wrestling"),
    ('MMA', "MMA"),
    ('athletic', 'athletic'),
    ('badminton', 'badminton'),
    ('softball', 'softball'),
    ('KABADI', 'KABADI'),
    ('KHO-KHO', 'KHO-KHO'),
)


class Appointment(models.Model):
    objects = models
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=100)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    qualification_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    academy_name = models.CharField(max_length=100)
    department = models.CharField(choices=department, max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    fees = models.IntegerField()

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    # return reverse('appointment:delete-appointment', kwargs={'pk': self.pk})


class TakeAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    message = models.TextField()
    phone_number = models.CharField(max_length=120)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

# Create your models here.
