from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import  UserForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


from email_hunter import EmailHunterClient
import clearbit

#Create your views here.


class RegistrationView(View):
    form_class = UserForm
    template_name = 'signup/register.html'


    def get (self, request):
        if request.user.is_authenticated :
            return redirect('home:index')

        form = self.form_class(None)
        return  render(request, self.template_name, {'form' : form})


    def post (self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form, 'message': "Invalid form data / User already exists"})


        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']

        user_auth = authenticate(username=username, password=password)

        if user_auth is None:
                user = form.save(commit=False)

                #email validation
                try:
                    validate_email(email)
                except ValidationError as e:
                    return render(request, self.template_name, {'form': form, 'message' : "Invalid or non-existent email"})

                # third party validations
                hunter = EmailHunterClient(api_key='c8877861cc333dea4e0f3423c0cfbbb5684a8b50')
                clearbit.key = 'sk_c22de2f70a4cb20521a935cac8192750'

                response = clearbit.Enrichment.find(email=email, stream=True)

                if response['person'] is None :
                    return render(request, self.template_name, {'form': form, 'message': "Invalid  data"})

                person_firstname = response['person']['name']['givenName']
                person_lastname = response['person']['name']['familyName']

                if not (person_lastname == last_name and person_firstname == first_name):
                    return render(request, self.template_name, {'form': form, 'message': "Invalid or non-existent data"})

                if not hunter.exist(email):
                    return render(request, self.template_name, {'form': form, 'message' : "Invalid or non-existent email"})

                user.set_password(password)
                user.save()

                user_auth = authenticate(username=username, password=password)

                if user_auth.is_authenticated:
                    login(request, user_auth)
                else:
                    render(request, self.template_name, {'message' : 'Login of the user failed'})
        else:
                login(request, user_auth)

        return render(request, self.template_name, {'success' : 1})
