from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Role-based URLs
    path('admin/dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian/dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member/dashboard/', views.member_view, name='member_dashboard'),
    
    # Book CRUD URLs with permissions (Function-based views)
    path('books/add/', views.add_book_view, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book_view, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book_view, name='delete_book'),
    
    # Book CRUD URLs with permissions (Class-based views - alternative)
    path('books/create/', views.BookCreateView.as_view(), name='create_book'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='update_book'),
    path('books/<int:pk>/delete-cbv/', views.BookDeleteView.as_view(), name='delete_book_cbv'),
    
    # Permission check URL
    path('permissions/', views.check_permissions_view, name='check_permissions'),
    
    # Existing URLs
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('', views.LibraryListView.as_view(), name='home'),
]