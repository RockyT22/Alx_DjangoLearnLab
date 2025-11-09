from django.urls import path
from .views import list_books
from .views import LibraryListView, LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view URL
    path('books/', list_books, name='list_books'),
    
    # Class-based view URLs
    path('libraries/', LibraryListView.as_view(), name='library_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
