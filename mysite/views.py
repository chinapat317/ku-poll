from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


def redirect_index(request): 
    return HttpResponseRedirect('../polls/')

def signup(request):
    #create new user
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_pw = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_pw)
            login(request, user)
            request.method = 'GET'
            return redirect_index(request)
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form':form})

