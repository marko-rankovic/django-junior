from django.shortcuts import render, redirect
from django.contrib.auth import  logout

from django.views import generic

# Create your views here.

class LogoutView(generic.View):
    template_name = 'logout/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home:index')

        logout(request)

        return render(request, self.template_name, {'success' : 1})
