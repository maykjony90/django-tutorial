# A basic form processing with a small detail: the login 
# function (renamed to auth_login to avoid clashing with 
# the built-in login view).
from django.contrib.auth import login as auth_login
# Time to create the sign up form. 
# Django has a built-in form named UserCreationForm.
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# instead of using the UserCreationForm in our views.py, 
# let’s import the new form, SignUpForm, and use it instead:
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			# A basic form processing with a small detail: the login function 
			# (renamed to auth_login to avoid clashing with the built-in login view).
			user = form.save()
			auth_login(request, user)
			# After that, the view redirects the user to the homepage, 
			# keeping the flow of the application.
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})
	


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user