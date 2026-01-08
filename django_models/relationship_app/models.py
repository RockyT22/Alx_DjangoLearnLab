from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_librarian(self):
        return self.role == 'librarian'
    
    def is_member(self):
        return self.role == 'member'
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

# Signal to create UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal to save UserProfile when User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('relationship_app:list_books')

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    def get_absolute_url(self):
        return reverse('relationship_app:book_detail', args=[str(self.id)])

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('relationship_app:library_detail', args=[str(self.id)])
    
    def get_book_count(self):
        return self.books.count()
    
    def get_unique_authors(self):
        return self.books.values_list('author', flat=True).distinct().count()

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    def __str__(self):
        return f"{self.name} - {self.library.name}"
class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
            ("can_view_book", "Can view book"),  # Optional: for viewing
        ]