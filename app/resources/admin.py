from django.contrib import admin
from .models import Category, Resource, Comment, UserProfile, Skill, Achievement, Certificate, Tag, ResourceFile

# Register your models here.
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Skill)
admin.site.register(Achievement)
admin.site.register(Certificate)
admin.site.register(Tag)
admin.site.register(ResourceFile)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'uploaded_at', 'is_approved')
    list_filter = ('is_approved', 'category')
    actions = ['approve_resources']

    def approve_resources(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} resource(s) approved.")
    approve_resources.short_description = "✅ Approve selected resources"


# class Resource(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     file = models.FileField(upload_to='resources/')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     uploader = models.ForeignKey(User, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     is_approved = models.BooleanField(default=False)
