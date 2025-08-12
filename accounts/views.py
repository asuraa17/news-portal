from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.views import View
from .forms import RegistrationForm

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "registration/register.html", {"form": form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() #Local variable user is assigned to but never used
            
            #Optional: Log the user in immediately after registration
            login(request, user)

            # Redirect to login page after successful registration
            
            return redirect("accounts:login")
        return render(request, "registration/register.html", {"form": form})
