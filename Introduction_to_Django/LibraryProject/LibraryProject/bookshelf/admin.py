from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to display in the list view
    list_filter = ('author', 'publication_year')            # Filters in the sidebar
    search_fields = ('title', 'author')                     # Search bar functionality

# Register Book with the custom admin configuration
admin.site.register(Book, BookAdmin)
