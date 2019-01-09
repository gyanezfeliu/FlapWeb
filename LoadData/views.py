from django.http import HttpResponse
from django.shortcuts import render
import json
from django.core import serializers
from .models import Experiment, Sample, Dna, Vector, Measurement, Inducer
from . import file_reader as fr
from .forms import UploadFileForm, UserForm, UserProfileInfoForm, SearchForm

# FOR LOGIN
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def leer(request):

    form = UploadFileForm(request.POST, request.FILES)
    upload = handle_uploaded_file(request.FILES['dataFile'])

    data = json.dumps({
    'status': 'ok',
    'upload_error': upload,
    'posts': request.POST
    })

    fr.MonkeyReader.loadSynergy(request.POST['dataFull'], request.FILES['dataFile'].name)
    return HttpResponse(data, content_type='application/json')

def massUpload(request):
    fr.MonkeyReader.massUpload()
    data = json.dumps({'Status': "Your data is being loaded"})
    return HttpResponse(data, content_type='application/json')

def handle_uploaded_file(f):
    with open('../uploads/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    return render(request, 'index.html', {})

def search(request):
    form = show_search(request)
    return render(request, 'search.html', {'form': form})

def plot(request):
    to_show = fr.MonkeyReader.plot(request)
    return render(request, 'to_plot.html', {'graph': to_show})

def to_analysis(request):
    # Recibo los datos desde Search como request
    data = json.dumps({
    'posts': request.POST
    })
    return render(request, 'analysis.html', {'from_search': data})

    # Esto tengo que hacerlo desde otro método, desde el $.post que haré desde
    # analysis.html, en donde enviaré formulario con la información de la query
    # y con la información del análisis. Debo por lo tanto cambiar el nombre a
    # ESTE método (arriba) y desde el otro método llamar a MonkeyReader.analysis
    # desde analysis.html para renderizar en el mismo analysis.html el gráfico
    # resultante, igual que como hice en search.

def make_analysis(request):
    if 'INDUCTION' in request.POST['param1[]']:
        to_analyse = fr.MonkeyReader.analysis_induction(request)
        return render(request, 'analysis_induction.html', {'graph': to_analyse})
    elif 'HEATMAP' in request.POST['param1[]']:
        to_analyse = fr.MonkeyReader.analysis_heatmap(request)
        return render(request, 'analysis_heatmap.html', {'graph': to_analyse})
    elif 'KYMOGRAPH' in request.POST['param1[]']:
        to_analyse = fr.MonkeyReader.analysis_kymograph(request)
        return render(request, 'analysis_kymograph.html', {'graph': to_analyse})

def plots(request, id=0):
    return render(request, 'plots.html', {})

def home(request):
    return render(request, 'home.html', {})


## PARA LOGIN

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'registration.html',
                            {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Authenticates the user
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("ACCOUNT IS NOT ACTVE")
        else:
            print("Someone tried to login and failed")
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'login.html', {})

def show_search(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid:
            pass
    return form
