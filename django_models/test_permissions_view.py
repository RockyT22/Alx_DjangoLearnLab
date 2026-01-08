import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')

import django
django.setup()

# Check if the view function exists
try:
    from relationship_app import views
    
    # Check if check_permissions_view exists
    if hasattr(views, 'check_permissions_view'):
        print("✓ check_permissions_view exists in views.py")
    else:
        print("✗ check_permissions_view NOT found in views.py")
        print("Adding the missing view...")
        
    # Check URL pattern
    from django.urls import reverse
    try:
        reverse('relationship_app:check_permissions')
        print("✓ URL pattern exists")
    except:
        print("✗ URL pattern not found")
        
except Exception as e:
    print(f"✗ Error: {e}")
