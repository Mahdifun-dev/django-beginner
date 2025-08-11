# resources/context_processors.py

from .models import UserProfile

def user_profile_picture(request):
    """
    Makes the user's profile picture URL available in all templates.
    """
    if request.user.is_authenticated:
        try:
            # Get the user's profile
            profile = request.user.userprofile
            if profile.profile_picture:
                # If a picture exists, return its URL
                return {'user_profile_picture_url': profile.profile_picture.url}
        except UserProfile.DoesNotExist:
            # If the user exists but has no profile object yet
            pass
    
    # If the user is not authenticated or has no picture, return None
    return {'user_profile_picture_url': None}