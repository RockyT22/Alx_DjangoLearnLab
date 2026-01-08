from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from .models import Author, Book, Library, Librarian, UserProfile
from django.contrib.auth.models import User

# === AUTHENTICATION VIEWS ===

# User Registration View
class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('relationship_app:login')
    template_name = 'relationship_app/register.html'
    
    def form_valid(self, form):
        """Override to assign default role after registration"""
        response = super().form_valid(form)
        user = form.instance
        
        # Create UserProfile with default 'member' role
        UserProfile.objects.create(user=user, role='member')
        
        messages.success(self.request, 'Registration successful! Please login with your credentials.')
        return response

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next', 'relationship_app:home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'relationship_app/login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'relationship_app/logout.html')

# === ROLE CHECK FUNCTIONS ===

def is_admin(user):
    """Check if user has admin role"""
    if user.is_authenticated:
        try:
            return user.profile.role == 'admin'
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist
            UserProfile.objects.create(user=user, role='member')
            return False
    return False

def is_librarian(user):
    """Check if user has librarian role"""
    if user.is_authenticated:
        try:
            return user.profile.role == 'librarian'
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user, role='member')
            return False
    return False

def is_member(user):
    """Check if user has member role"""
    if user.is_authenticated:
        try:
            return user.profile.role == 'member'
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user, role='member')
            return True  # Default role is member
    return False

# === ROLE-BASED VIEWS ===

@login_required(login_url="/login/")
@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users"""
    context = {
        'user': request.user,
        'role': 'Admin',
        'total_users': User.objects.count(),
        'total_books': Book.objects.count(),
        'total_libraries': Library.objects.count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)

@login_required(login_url="/login/")
@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users"""
    # Get libraries managed by this librarian
    libraries = Library.objects.filter(librarian__name=request.user.username)
    
    context = {
        'user': request.user,
        'role': 'Librarian',
        'libraries': libraries,
        'total_books_in_charge': Book.objects.filter(libraries__in=libraries).distinct().count() if libraries else 0,
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@login_required(login_url="/login/")
@user_passes_test(is_member)
def member_view(request):
    """View accessible only to Member users"""
    context = {
        'user': request.user,
        'role': 'Member',
        'available_books': Book.objects.count(),
        'available_libraries': Library.objects.count(),
        'recent_books': Book.objects.all()[:5],  # Show 5 most recent books
    }
    return render(request, 'relationship_app/member_view.html', context)

# === PROFILE MANAGEMENT VIEW ===

@login_required(login_url="/login/")
def profile_view(request):
    """User profile view showing role information"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user, role='member')
    
    context = {
        'user': request.user,
        'profile': profile,
        'role_display': profile.get_role_display(),
        'is_admin': profile.is_admin(),
        'is_librarian': profile.is_librarian(),
        'is_member': profile.is_member(),
    }
    return render(request, 'relationship_app/profile.html', context)

# === PERMISSION CHECK VIEW (ONLY ONE VERSION!) ===

@login_required(login_url="/login/")
def check_permissions_view(request):
    """View to show current user's permissions"""
    user = request.user
    
    # Check book permissions
    permissions = {
        'can_add_book': user.has_perm('relationship_app.can_add_book'),
        'can_change_book': user.has_perm('relationship_app.can_change_book'),
        'can_delete_book': user.has_perm('relationship_app.can_delete_book'),
        'can_view_book': user.has_perm('relationship_app.can_view_book'),
    }
    
    # Also check all permissions the user has (filtered to our app)
    all_perms = []
    for perm in user.get_all_permissions():
        if 'relationship_app' in perm:
            all_perms.append(perm)
    
    context = {
        'user': user,
        'permissions': permissions,
        'all_permissions': all_perms,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    }
    
    return render(request, 'relationship_app/permissions_check.html', context)

# === EXISTING VIEWS ===

# Function-based view to list all books
def list_books(request):
    """Function-based view that lists all books in the database"""
    books = Book.objects.select_related('author').all()
    context = {
        'books': books,
        'user': request.user
    }
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """Class-based view using DetailView to display library details"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        """Add additional context data if needed"""
        context = super().get_context_data(**kwargs)
        return context

# Class-based view to list all libraries
class LibraryListView(ListView):
    """Class-based view to list all libraries"""
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

# Function-based view for book details
def book_detail(request, book_id):
    """Function-based view to show details of a specific book"""
    book = get_object_or_404(Book.objects.select_related('author'), id=book_id)
    
    # Get all libraries that have this book
    libraries = book.libraries.all()
    
    context = {
        'book': book,
        'libraries': libraries,
        'user': request.user
    }
    return render(request, 'relationship_app/book_detail.html', context)

# === BOOK CRUD VIEWS WITH PERMISSIONS ===

@permission_required('relationship_app.can_add_book', login_url='/login/')
def add_book_view(request):
    """View to add a new book (requires can_add_book permission)"""
    if request.method == 'POST':
        # Process form data
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        try:
            author = Author.objects.get(id=author_id)
            book = Book.objects.create(title=title, author=author)
            messages.success(request, f'Book "{title}" added successfully!')
            return redirect('relationship_app:list_books')
        except Author.DoesNotExist:
            messages.error(request, 'Author not found')
        except Exception as e:
            messages.error(request, f'Error adding book: {e}')
    
    # Get all authors for the dropdown
    authors = Author.objects.all()
    context = {
        'authors': authors,
        'action': 'Add'
    }
    return render(request, 'relationship_app/book_form.html', context)

@permission_required(login_url="/login/")('relationship_app.can_change_book')
def edit_book_view(request, book_id):
    """View to edit an existing book (requires can_change_book permission)"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        try:
            author = Author.objects.get(id=author_id)
            book.title = title
            book.author = author
            book.save()
            messages.success(request, f'Book updated successfully!')
            return redirect('relationship_app:book_detail', book_id=book.id)
        except Author.DoesNotExist:
            messages.error(request, 'Author not found')
        except Exception as e:
            messages.error(request, f'Error updating book: {e}')
    
    authors = Author.objects.all()
    context = {
        'book': book,
        'authors': authors,
        'action': 'Edit'
    }
    return render(request, 'relationship_app/book_form.html', context)

@permission_required(login_url="/login/")('relationship_app.can_delete_book')
def delete_book_view(request, book_id):
    """View to delete a book (requires can_delete_book permission)"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('relationship_app:list_books')
    
    context = {
        'book': book,
        'action': 'Delete'
    }
    return render(request, 'relationship_app/book_confirm_delete.html', context)

# === CLASS-BASED VIEWS WITH PERMISSIONS (Alternative) ===

class BookCreateView(LoginRequiredMixin, CreateView):
    """Class-based view for creating books with permission mixin"""
    model = Book
    fields = ['title', 'author']
    template_name = 'relationship_app/book_form_cbv.html'
    success_url = reverse_lazy('relationship_app:list_books')
    
    def dispatch(self, request, *args, **kwargs):
        # Check permission before dispatching
        if not request.user.has_perm('relationship_app.can_add_book'):
            return HttpResponseForbidden("You don't have permission to add books.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    """Class-based view for updating books with permission mixin"""
    model = Book
    fields = ['title', 'author']
    template_name = 'relationship_app/book_form_cbv.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check permission before dispatching
        if not request.user.has_perm('relationship_app.can_change_book'):
            return HttpResponseForbidden("You don't have permission to change books.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('relationship_app:book_detail', args=[str(self.object.id)])

class BookDeleteView(LoginRequiredMixin, DeleteView):
    """Class-based view for deleting books with permission mixin"""
    model = Book
    template_name = 'relationship_app/book_confirm_delete.html'
    success_url = reverse_lazy('relationship_app:list_books')
    
    def dispatch(self, request, *args, **kwargs):
        # Check permission before dispatching
        if not request.user.has_perm('relationship_app.can_delete_book'):
            return HttpResponseForbidden("You don't have permission to delete books.")
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)
