from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Resource, Comment
from .forms import ResourceForm, CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, "resources/home.html")


def resource_list(request):
    resources = Resource.objects.filter(is_approved=True).order_by("-uploaded_at")
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
            resource.uploader = request.user 
            resource.save()
            return redirect("home")
    else:
        form = ResourceForm()
    return render(request, "resources/upload_resource.html", {"form": form})



def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    comments = resource.comments.all()
    related_resources = Resource.objects.filter(category=resource.category).exclude(pk=pk)[:4]

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.user = request.user
            comment.save()
            return redirect('resource_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'resources/resource_detail.html', {
        'resource': resource,
        'comments': comments,
        'comment_form': form,
        'related_resources': related_resources,
    })




def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)

    if not resource.is_approved:
        if not request.user.is_authenticated or (request.user != resource.uploader and not request.user.is_staff):
            raise Http404("Resource not found.")
        
    related_resources = Resource.objects.filter(category=resource.category).exclude(pk=pk)[:4]
    comments = resource.comments.all().order_by('-created_at')
    liked = False

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.user = request.user
            comment.save()
            return redirect('resource_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'resources/resource_detail.html', {
        'resource': resource,
        'comments': comments,
        'comment_form': form,
        'related_resources': related_resources,
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


@staff_member_required
def pending_resources(request):
    resources = Resource.objects.filter(is_approved=False)
    return render(request, 'resources/pending_list.html', {'resources': resources})

@staff_member_required
def approve_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.is_approved = True
    resource.save()
    return redirect('pending_resources')


@login_required
def toggle_like(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.user in resource.likes.all():
        resource.likes.remove(request.user)
    else:
        resource.likes.add(request.user)
    return redirect('resource_detail', pk=pk)

@login_required
def profile_view(request):
    user = request.user
    context = {
        'my_resources': Resource.objects.filter(uploader=user),
        'likes_count': user.liked_resources.count() if hasattr(user, 'liked_resources') else 0,
        'comments_count': Comment.objects.filter(user=user).count(),
        'pending_count': Resource.objects.filter(uploader=user, is_approved=False).count()
    }
    return render(request, 'resources/profile.html', context)