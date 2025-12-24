"""
coach_appointment_system URL Configuration

"""

from django.urls import path
from appointment.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'appointment'

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('service', ServiceView.as_view(), name='service'),
    path('sports', SportsView.as_view(), name='sports'),
    path('coach/appointment/create', AppointmentCreateView.as_view(), name='coach-appointment-create'),
    path('coach/appointment/', AppointmentListView.as_view(), name='coach-appointment'),
    path('<pk>/delete/', AppointmentDeleteView.as_view(), name='delete-appointment'),
    path('<pk>/student/delete', StudentDeleteView.as_view(), name='delete-student'),
    path('student/take-appointment/<pk>', TakeAppointmentView.as_view(), name='take-appointment'),
    path('search/', SearchView.as_view(), name='search'),
    path('student/', StudentListView.as_view(), name='student-list'),
    #path('students/<int:appointment_id>', StudentPerAppointmentView.as_view(), name='student-list'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)