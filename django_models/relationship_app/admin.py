from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['author']
    search_fields = ['title']

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['books']
    search_fields = ['name']

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['name', 'library']
    search_fields = ['name', 'library__name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
