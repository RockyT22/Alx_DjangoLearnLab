import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

def assign_roles():
    """Assign roles to existing users"""
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@library.com'}
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created admin user with password: admin123")
    
    # Update or create admin profile
    admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
    admin_profile.role = 'admin'
    admin_profile.save()
    print(f"Assigned 'admin' role to user: {admin_user.username}")
    
    # Get all users and assign default role if not set
    users = User.objects.all()
    for user in users:
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            profile.role = 'member'  # Default role
            profile.save()
            print(f"Created profile with 'member' role for user: {user.username}")
    
    print("\n=== Role Assignment Complete ===")
    print("Admin Dashboard: http://127.0.0.1:8000/admin/dashboard/")
    print("Admin Login: admin / admin123")
    print("\nOther users will have 'member' role by default.")
    print("You can change roles in the Django admin panel.")

if __name__ == "__main__":
    assign_roles()
