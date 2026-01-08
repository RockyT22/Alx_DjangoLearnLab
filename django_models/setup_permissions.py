import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

def setup_permissions():
    print("Setting up permissions...")
    
    # Get content type for Book model
    content_type = ContentType.objects.get_for_model(Book)
    
    # Get all permissions for Book model
    permissions = Permission.objects.filter(content_type=content_type)
    
    # Create or get groups
    admin_group, created = Group.objects.get_or_create(name='Admins')
    librarian_group, created = Group.objects.get_or_create(name='Librarians')
    member_group, created = Group.objects.get_or_create(name='Members')
    
    # Assign permissions to groups
    # Admins get all permissions
    admin_group.permissions.set(permissions)
    
    # Librarians can add, change, and view books
    librarian_perms = permissions.filter(codename__in=['can_add_book', 'can_change_book', 'can_view_book'])
    librarian_group.permissions.set(librarian_perms)
    
    # Members can only view books
    member_perms = permissions.filter(codename='can_view_book')
    member_group.permissions.set(member_perms)
    
    print("✓ Groups and permissions created:")
    print(f"  - Admins: {admin_group.permissions.count()} permissions")
    print(f"  - Librarians: {librarian_group.permissions.count()} permissions")
    print(f"  - Members: {member_group.permissions.count()} permissions")
    
    # Assign users to groups based on their UserProfile role
    from relationship_app.models import UserProfile
    
    for user in User.objects.all():
        try:
            profile = user.profile
            if profile.role == 'admin':
                user.groups.add(admin_group)
                user.is_staff = True
                user.is_superuser = True
                user.save()
                print(f"  - {user.username} added to Admins group")
            elif profile.role == 'librarian':
                user.groups.add(librarian_group)
                user.is_staff = True
                user.save()
                print(f"  - {user.username} added to Librarians group")
            elif profile.role == 'member':
                user.groups.add(member_group)
                print(f"  - {user.username} added to Members group")
        except UserProfile.DoesNotExist:
            pass
    
    print("\n=== Setup Complete ===")
    print("Admins: Full CRUD access")
    print("Librarians: Can add and edit books")
    print("Members: Can only view books")

if __name__ == "__main__":
    setup_permissions()
