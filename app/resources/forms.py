from django import forms
from .models import Resource, Comment, Skill, Achievement, Certificate, UserProfile, Education, Tag
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'birth_date', 'gender', 'bio', 'profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True, user=None):
        profile = super().save(commit=False)
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
        if commit:
            profile.save()
        return profile





class MultipleFileInput(forms.ClearableFileInput):
    """A custom widget to allow multiple file selection."""
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    """
    A custom form field that can handle multiple files.
    It uses our MultipleFileInput widget and cleans the data into a list of files.
    """
    def __init__(self, *args, **kwargs):
        # We set our custom widget as the default
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # This clean method is the core of the solution. It takes the raw data
        # from the request and processes it into a clean list of files.
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            # Handle the case of a single file being uploaded
            result = [single_file_clean(data, initial)]
        return result


class ResourceForm(forms.ModelForm):
    files = MultipleFileField(
        required=False,
        help_text="Select one or more files to upload.",
        widget=MultipleFileInput(attrs={
            'class': 'hidden', # We want to hide the default input
            'id': 'file-input'  # A nice, specific ID for our JavaScript
        })
    )
    tags_input = forms.CharField(
        label="برچسب‌ها (جدا شده با ویرگول)",
        required=False,
        help_text="کلمات کلیدی را با ویرگول (,) از هم جدا کنید.",
        widget=forms.TextInput(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'مثال: پایتون, جنگو, rest-api'
            }
        )
    )
    class Meta:
        model = Resource
        fields = ["title", "description", "category", "instructor_name", "external_url", "privacy", "file_type", "thumbnail"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'عنوان فایل را وارد کنید'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 4,
                'placeholder': 'توضیحات خود را وارد کنید'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'external_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'https://example.com'
            }),
            'instructor_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'نام مدرس یا منبع'
            }),
            'file_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded appearance-none focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent pr-10'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded appearance-none focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent pr-10'
            }),
            'privacy': forms.Select(attrs={
                'class': 'hidden'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['privacy'].initial = 'public'
        self.fields['description'].required = False
        self.fields['category'].required = False
        self.fields['thumbnail'].required = False
        self.fields['external_url'].required = False
        self.fields['instructor_name'].required = False
        if self.instance and self.instance.pk:
            # Get existing tags and join them into a single string
            existing_tags = self.instance.tags.all()
            self.fields['tags_input'].initial = ', '.join(tag.name for tag in existing_tags)

    def save(self, user=None, commit=True):
        # --- START DEBUGGING ---
        print("--- 1. INSIDE FORM SAVE METHOD ---")
        resource = super().save(commit=False)

        if user:
            resource.uploader = user
            print("--- 2. Uploader assigned ---")

        if commit:
            resource.save()
            print("--- 3. Main resource object SAVED ---")
            
            # Now let's check the tag data
            tags_input_string = self.cleaned_data.get('tags_input', '').strip()
            print(f"--- 4. Raw tags_input string from form: '{tags_input_string}' ---")

            resource.tags.clear()
            
            if tags_input_string:
                tag_names = [tag.strip() for tag in tags_input_string.split(',') if tag.strip()]
                print(f"--- 5. Parsed tag names list: {tag_names} ---")
                
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    resource.tags.add(tag)
                    print(f"--- 6. ADDED tag to resource: '{tag.name}' (Was it created new? {created}) ---")
            else:
                print("--- 5/6. No tags_input string found. SKIPPING tag logic. ---")
        else:
            print("--- 3. Commit is False. SKIPPING database save and tag logic. ---")
        # --- END DEBUGGING ---
        
        return resource



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'نظر خود را بنویسید...'})
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level', 'teachable']
        labels = {
            'name': 'نام مهارت',
            'level': 'سطح مهارت',
            'teachable': 'میتوانم این مهارت را تدریس کنم',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'مثلاً برنامه‌نویسی پایتون'}),
            'level': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 100}),
            'teachable': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'start_year', 'end_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-input'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'organization', 'year', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'organization': forms.TextInput(attrs={'class': 'form-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'file': forms.FileInput(attrs={'class': 'form-file-input'}),
        }
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_year', 'end_year', 'description']
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'form-input'}),
            'institution': forms.TextInput(attrs={'class': 'form-input'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-input'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
        }

