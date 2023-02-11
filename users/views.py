from django.contrib.auth import get_user_model
from django.views.generic import DetailView, View, CreateView, UpdateView, ListView
from .forms import *
from django.shortcuts import render,get_object_or_404, redirect

User = get_user_model()
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = User.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
               user_ = profile
               user_.is_active = True
               user_.save()
               profile.activated = True
               profile.activation_key = None
               profile.save()
               return redirect("/accounts/login")
    return redirect("/accounts/login")



class RegisterView(CreateView):
	form_class = RegisterForm
	template_name ='registration/register.html' 
	success_url = '/'
    
	def dispatch(self, *args, **kwargs):
		# if self.request.user.is_authenticated:
		#  	return redirect('/logout')
		return super(RegisterView, self).dispatch(*args, **kwargs)


def Index(request):
    context = {}
    return render(request, "index.html", context)

def About(request):
    context = {}
    return render(request, "about.html", context)