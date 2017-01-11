from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.views import generic

from .forms import ProfileForm
# Create your views here.

class LoginView(generic.View):
    template_name = 'login/index.html'
    form_class = ProfileForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:index')

        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user_auth = authenticate(username = username, password=password)

        print (user_auth)

        if user_auth is not None:
            if user_auth.is_active:
                print("Hahahahahaha")
                login(request, user_auth)
                return render(request, self.template_name, {'success': 1})
            else:
                return render(request, self.template_name, {'form': form, 'message': 'Not an active user!'})

        return render(request, self.template_name, {'form': form , 'message': 'Unsuccessful login due to bad input or non-existing user'})
