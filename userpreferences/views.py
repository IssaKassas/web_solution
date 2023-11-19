from django.shortcuts import render
from django.contrib.messages import success
from os import path
from json import load
from pdb import set_trace
from django.conf import settings
from .models import UserPreference

# set_trace is useful to hard-code a breakpoint at a given point in a program, even if the code is not otherwise being debugged (e.g. when an assertion fails). 
# If given, *header* is printed to the console just before debugging begins.
# set_trace()

# Create your views here.
def index(request):
    file_path = path.join(settings.BASE_DIR, 'currencies.json')
    currencies_data = []
    
    with open(file_path, 'r') as json_file:
        data = load(json_file)
        for key, value in data.items():
            currencies_data.append({'name': key, 'value': value})
            
    exist_user = UserPreference.objects.filter(user = request.user).exists()
    user_preferences = None
    
    if exist_user:
        user_preferences = UserPreference.objects.get(user = request.user)
                
    if request.method != "GET":
        currency = request.POST["currency"]
        if exist_user:
            user_preferences.currency = currency
            user_preferences.save()
        
        else:
            UserPreference.objects.create(user = request.user, currency = currency)
            
        success(request, "Changes saved!!")
        
    return render(request, 'preferences/index.html', {'currencies': currencies_data, 'user_preferences': user_preferences})