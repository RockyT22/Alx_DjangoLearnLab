import os
import sys
import django

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment - use the correct project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def cleanup_existing_data():
    """Clean up any existing data to avoid duplicates"""
    print("Cleaning up existing data...")
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()

def query_all_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
        return []
    except Author.MultipleObjectsReturned:
        print(f"Multiple authors found with name '{author_name}'. Using the first one.")
        author = Author.objects.filter(name=author_name).first()
        books = author.books.all()
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books

def list_all_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} library:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
        return []

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}")
        return None

# Example usage and demonstration
if __name__ == "__main__":
    print("=== Testing Django Relationship Queries ===")
    
    # Clean up any existing data first
    cleanup_existing_data()
    
    # Create fresh sample data
    print("\n1. Creating sample data...")
    
    # Create authors using get_or_create to avoid duplicates
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    author2, created = Author.objects.get_or_create(name="George Orwell")
    
    # Create books using get_or_create
    book1, created = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone", 
        author=author1
    )
    book2, created = Book.objects.get_or_create(
        title="Harry Potter and the Chamber of Secrets", 
        author=author1
    )
    book3, created = Book.objects.get_or_create(
        title="1984", 
        author=author2
    )
    book4, created = Book.objects.get_or_create(
        title="Animal Farm", 
        author=author2
    )
    
    # Create library
    library, created = Library.objects.get_or_create(name="City Central Library")
    
    # Clear any existing books and add our books to library
    library.books.clear()
    library.books.add(book1, book2, book3)
    
    # Create librarian
    librarian, created = Librarian.objects.get_or_create(
        name="Alice Johnson", 
        library=library
    )
    
    print("Sample data created successfully!")
    
    # Test the queries
    print("\n2. Testing queries:")
    
    print("\n--- Query all books by J.K. Rowling ---")
    query_all_books_by_author("J.K. Rowling")
    
    print("\n--- List all books in City Central Library ---")
    list_all_books_in_library("City Central Library")
    
    print("\n--- Retrieve librarian for City Central Library ---")
    get_librarian_for_library("City Central Library")
    
    print("\n=== Query testing completed ===")