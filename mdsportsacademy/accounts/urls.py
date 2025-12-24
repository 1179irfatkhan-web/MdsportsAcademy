from django.urls import path
from accounts.views import *
from appointment.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "accounts"

urlpatterns = [
    path('student/register', RegisterStudentView.as_view(), name='student-register'),
    path('student/profile/update/', EditStudentProfileView.as_view(), name='student-profile-update'),
    path('coach/register', RegisterCoachView.as_view(), name='coach-register'),
    path('coach/profile/update/', EditCoachProfileView.as_view(), name='coach-profile-update'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]