from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Library, Book, Author, CustomUser
from .forms import BookForm, CustomUserCreationForm

# Utility functions for role checking
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Class-based view to list all libraries
class LibraryListView(ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

# Registration view - updated to use CustomUserCreationForm
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = CustomUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role-based views
@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    users = CustomUser.objects.all()
    return render(request, 'relationship_app/admin_view.html', {'users': users})

@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    books = Book.objects.all()
    libraries = Library.objects.all()
    return render(request, 'relationship_app/librarian_view.html', {
        'books': books,
        'libraries': libraries
    })

@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/member_view.html', {'books': books})

# Secured views with custom permissions
@permission_required('relationship_app.can_add_book', login_url='/relationship/login/')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', login_url='/relationship/login/')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', login_url='/relationship/login/')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
