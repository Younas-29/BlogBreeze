from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
import os

User = get_user_model()

@require_http_methods(["GET"])
def setup_superuser(request):
    """
    Setup endpoint to create or reset superuser from environment variables.
    Deletes existing superuser and creates a new one with current env vars.
    """
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    
    if not password:
        return JsonResponse({
            'status': 'error',
            'message': 'DJANGO_SUPERUSER_PASSWORD environment variable not set'
        }, status=400)
    
    try:
        # Delete existing user with this username if exists
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            existing_user.delete()
        
        # Create new superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        # Ensure UserProfile exists and set role to admin
        if hasattr(user, 'profile'):
            user.profile.role = 'admin'
            user.profile.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Superuser "{username}" created/reset successfully',
            'username': username,
            'note': 'You can now login to /admin/ with your credentials'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error creating superuser: {str(e)}'
        }, status=500)
