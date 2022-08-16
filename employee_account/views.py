from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Employee
from .forms import LoginForm


class LoginUserView(LoginView):
    template_name = 'employee_account/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('my-profile')
    
    
class MyProfile(LoginRequiredMixin, DetailView):
    
    model = Employee
    template_name = 'employee_account/my-profile.html'
    
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Employee, pk=request.user.pk)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)