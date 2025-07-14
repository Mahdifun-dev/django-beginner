from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Resource, UserProfile
from .forms import ResourceForm, CommentForm, SkillForm, AchievementForm, CertificateForm
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q


def home(request):
    return render(request, "resources/home.html")


def resource_list(request):
    query = request.GET.get('q')
    if query:
        resources = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        resources = Resource.objects.filter(is_approved=True)
        
    resources = Resource.objects.filter(is_approved=True).order_by("-uploaded_at")
    return render(request, "resources_list.html", {"resources": resources})

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
    if request.method == 'POST':
        title = request.POST.get('title')
        tags = request.POST.get('tags')
        instructor = request.POST.get('instructor')
        external_url = request.POST.get('external_url')
        privacy = request.POST.get('privacy', 'public')
        file_type = request.POST.get('file_type')
        category = request.POST.get('category')
        description = request.POST.get('description')

        content_educational = True if request.POST.get('content-educational') == 'on' else False
        content_copyright = True if request.POST.get('content-copyright') == 'on' else False
        content_appropriate = True if request.POST.get('content-appropriate') == 'on' else False

        uploaded_file = request.FILES.get('files')
        thumbnail = request.FILES.get('thumbnail')

        # اعتبارسنجی ساده
        if not title or not uploaded_file or not file_type:
            messages.error(request, "لطفاً فیلدهای ضروری را پر کنید")
            return render(request, 'upload_template.html')

        new_upload = Resource.objects.create(
            title=title,
            tags=tags,
            instructor=instructor,
            external_url=external_url,
            privacy=privacy,
            file_type=file_type,
            category=category,
            description=description,
            file=uploaded_file,
            thumbnail=thumbnail,
            content_educational=content_educational,
            content_copyright=content_copyright,
            content_appropriate=content_appropriate,
        )

        messages.success(request, "فایل با موفقیت آپلود شد")
        return redirect('upload')  # یا هر URL دیگری که مناسب است

    return render(request, 'upload.html')





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

    return render(request, 'detail.html', {
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
    return render(request, 'pending.html', {'resources': resources})

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

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile_view'

    def get_object(self, queryset=None):
        # نمایش پروفایل کاربر فعلی
        return UserProfile.objects.get_or_create(user=self.request.user)



def add_skill(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = profile
            skill.save()
            return redirect('profile_view')
    else:
        form = SkillForm()
    return render(request, 'add_skill.html', {'form': form})
