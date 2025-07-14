from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, verbose_name="درباره من")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class Skill(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(help_text="عدد بین 0 تا 100")

    def __str__(self):
        return f"{self.name} ({self.level}%)"

class Achievement(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} - {self.year}"

class Certificate(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    file = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"






class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    
class Resource(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('ppt', 'PowerPoint'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('link', 'External Link'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    file = models.FileField(upload_to='resources/files/', null=True, blank=True)
    external_url = models.URLField(blank=True, null=True, help_text="اگر فایل آپلود نمی‌کنید، آدرس URL وارد کنید.")
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='pdf')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)


    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor_name = models.CharField(max_length=100, blank=True, help_text="نام مدرس یا ارائه‌دهنده منبع (اختیاری)")

    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    privacy = models.CharField(max_length=20, choices=[('public','عمومی'), ('unlisted','غیرفهرست'), ('private','خصوصی')], default='public')
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_resources', blank=True)

    thumbnail = models.ImageField(upload_to='resources/thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.resource.title}'

    def __str__(self):
        return f"{self.user.username} likes {self.resource.title}"