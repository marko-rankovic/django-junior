from django.contrib.auth.models import User
from django.views import generic


# Create your views here.

class UsersView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'all_users'

    def get_queryset(self):
        return  User.objects.all()


class ProfileView(generic.DetailView):
    model = User
    template_name = 'home/profile.html'




