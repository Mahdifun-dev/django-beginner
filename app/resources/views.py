from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Resource
from .forms import ResourceForm



def home(request):
    return render(request, 'resources/home.html')


def resource_list(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'resources/resource_list.html', {'resources': resources})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect('home')
    else:
        form = ResourceForm()
    return render(request, 'resources/upload_resource.html', {'form': form})