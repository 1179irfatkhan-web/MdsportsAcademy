from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView

from accounts.forms import StudentProfileUpdateForm, CoachProfileUpdateForm
from accounts.models import User
from .decorators import user_is_student, user_is_coach
from .forms import CreateAppointmentForm, TakeAppointmentForm
from .models import Appointment, TakeAppointment

"""
For Student Profile

"""


class EditStudentProfileView(UpdateView):
    model = User
    form_class = StudentProfileUpdateForm
    context_object_name = 'student'
    template_name = 'accounts/student/edit-profile.html'
    success_url = reverse_lazy('accounts:student-profile-update')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Student doesn't exists")
        return obj


class TakeAppointmentView(CreateView):
    template_name = 'appointment/take_appointment.html'
    form_class = TakeAppointmentForm
    extra_context = {
        'title': 'Take Appointment'
    }
    success_url = reverse_lazy('appointment:home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'student':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TakeAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


"""
   For coach Profile
"""


class EditCoachProfileView(UpdateView):
    model = User
    form_class = CoachProfileUpdateForm
    context_object_name = 'coach'
    template_name = 'accounts/coach/edit-profile.html'
    success_url = reverse_lazy('accounts:coach-profile-update')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_coach)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
            # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Student doesn't exists")
        return obj


class AppointmentCreateView(CreateView):
    template_name = 'appointment/appointment_create.html'
    form_class = CreateAppointmentForm
    extra_context = {
        'title': 'Post New Appointment'
    }
    success_url = reverse_lazy('appointment:coach-appointment')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'coach':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AppointmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_coach)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


class StudentListView(ListView):
    model = TakeAppointment
    context_object_name = 'students'
    template_name = "appointment/student_list.html"

    def get_queryset(self):
        return self.model.objects.filter(appointment__user_id=self.request.user.id).order_by('-id')


class StudentDeleteView(DeleteView):
    model = TakeAppointment
    success_url = reverse_lazy('appointment:student-list')


class AppointmentDeleteView(DeleteView):
    """
       For Delete any Appointment created by coach
    """
    model = Appointment
    success_url = reverse_lazy('appointment:coach-appointment')


"""
   For both Profile

"""


class HomePageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'home'
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')


class ServiceView(TemplateView):
    template_name = 'appointment/service.html'


class SportsView(TemplateView):
    template_name = 'appointment/sports.html'


class SearchView(ListView):
    paginate_by = 6
    model = Appointment
    template_name = 'appointment/search.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         department__contains=self.request.GET['department'])

# Create your views here.
