from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Resource, UserProfile, Skill, Achievement, Certificate, User, Education
from .forms import ResourceForm, CommentForm, SkillForm, AchievementForm, CertificateForm, ProfileForm, EducationForm
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Tag
from .models import ResourceFile


def home(request):
    return render(request, "resources/home.html")

def resource_list(request):
    # Start with a base queryset of approved resources
    queryset = Resource.objects.filter(is_approved=True)
    
    query = request.GET.get('q')
    if query:
        # If there's a search query, filter the base queryset
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Finally, order the result
    resources = queryset.order_by("-uploaded_at")
    
    return render(request, "resources/resources_list.html", {"resources": resources})

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
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploader = request.user
            resource.save()
            form.save_m2m()

            files = form.cleaned_data["files"]
            for f in files:
                ResourceFile.objects.create(resource=resource, file=f)

            tags_input = request.POST.get('tags', '').strip()
            if tags_input:
                tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    resource.tags.add(tag)
            instructor_name = request.POST.get('instructor_name', '').strip()
            if instructor_name:
                resource.instructor_name = instructor_name
                resource.save(update_fields=['instructor_name'])

            messages.success(request, 'فایل‌ها با موفقیت آپلود شدند و در انتظار تایید هستند.')
            return redirect('upload_resource')
        else:
            messages.error(request, 'خطا در فرم. لطفاً اطلاعات را بررسی کنید.')
    else:
        form = ResourceForm()
    return render(request, "resources/upload.html", {'form': form})




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

    return render(request, 'resources/detail.html', {
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
    return render(request, 'resources/pending.html', {'resources': resources})

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
def Profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # یا هر صفحه‌ای که می‌خواهی
    else:
        form = ProfileForm(instance=request.user.userprofile, user=request.user)

    return render(request, 'profiles/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def profile_view(request, username):
    """
    Displays a user's profile page with all their related information.
    """
    # Use get_object_or_404 to handle cases where the user doesn't exist
    profile_user = get_object_or_404(User, username=username)

    # Fetch all related data using the 'profile_user' object
    # Note: This assumes you have related_names set up or uses default Django ones.
    # It also assumes a UserProfile is created for each User.
    try:
        user_profile = profile_user.userprofile
        skills = user_profile.skills.all().order_by('-level')
        achievements = user_profile.achievements.all().order_by('-start_year') # For 'Work Experience'
        certificates = user_profile.certificates.all().order_by('-year') # For 'Publications'
        educations = user_profile.educations.all().order_by('-start_year') # For 'Education'
    except User.userprofile.RelatedObjectDoesNotExist:
        # Handle cases where a profile object hasn't been created for a user
        user_profile = None
        skills = []
        achievements = []
        certificates = []
        educations = []

    # Fetch resources uploaded by this user for the 'Recent Articles' section
    recent_resources = Resource.objects.filter(uploader=profile_user, is_approved=True).order_by('-uploaded_at')[:5]

    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'skills': skills,
        'achievements': achievements,
        'certificates': certificates,
        'educations': educations,
        'recent_resources': recent_resources,
    }

    return render(request, 'profiles/profile_view.html', context)


@login_required
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
    return render(request, 'pages/add_skill.html', {'form': form})


@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user.userprofile)
    skill.delete()
    return redirect('profile_view') 

@login_required
def add_Achievement(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = AchievementForm(request.POST)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.user = profile
            achievement.save()
            return redirect('profile_view')
    else:
        form = AchievementForm()
    return render(request, 'pages/add_achievement.html', {'form': form})

@login_required
def delete_Achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id, user=request.user.userprofile)
    achievement.delete()
    return redirect('profile_view')

@login_required
def add_Certificate(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.user = profile
            certificate.save()
            return redirect('profile_view')
    else:
        form = CertificateForm()
    return render(request, 'pages/add_certificate.html', {'form': form})

@login_required
def delete_Certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user.userprofile)
    certificate.delete()
    return redirect('profile_view')


@login_required
def add_Education(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = EducationForm(request.POST, request.FILES)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = profile
            education.save()
            return redirect('profile_view')
    else:
        form = EducationForm()
    return render(request, 'pages/add_education.html', {'form': form})

@login_required
def delete_Education(request, education_id):
    education = get_object_or_404(Education, id=education_id, user=request.user.userprofile)
    education.delete()
    return redirect('profile_view')


def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

def terms(request):
    return render(request, 'pages/terms.html')

def privacy(request):
    return render(request, 'pages/privacy.html')

def copyright(request):
    return render(request, 'pages/copyright.html')

def report(request):
    return render(request, 'pages/report.html')