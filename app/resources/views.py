from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Resource
from .forms import ResourceForm, CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden


def home(request):
    return render(request, "resources/home.html")


def resource_list(request):
    resources = Resource.objects.all().order_by("-uploaded_at")
    return render(request, "resources/resource_list.html", {"resources": resources})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# resource upload
@login_required
def upload_resource(request):
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect("home")
    else:
        form = ResourceForm()
    return render(request, "resources/upload_resource.html", {"form": form})


# resource details
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    comments = resource.comments.all().order_by('-created_at')

    # ارسال کامنت فقط اگر POST و کاربر لاگین باشد
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # یا include next param: ?next={{ request.path }}
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.user = request.user
            comment.save()
            return redirect('resources/resource_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'resources/resource_detail.html', {
        'resource': resource,
        'comments': comments,
        'form': form
    })



@login_required
def edit_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if resource.uploader != request.user:
        return HttpResponseForbidden("شما اجازهٔ ویرایش این منبع را ندارید.")
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect("resource_detail", pk=pk)
    else:
        form = ResourceForm(instance=resource)
    return render(
        request, "resources/edit_resource.html", {"form": form, "resource": resource}
    )

@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if resource.uploader != request.user:
        return HttpResponseForbidden("شما اجازهٔ حذف این منبع را ندارید.")
    if request.method == 'POST':
        resource.delete()
        return redirect('resource_list')
    return render(request, 'resources/confirm_delete.html', {'resource': resource})