import os
import sys
import django

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
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
    """Query all books by a specific author - using objects.filter(author=author)"""
    try:
        author = Author.objects.get(name=author_name)
        # This is the required query pattern: objects.filter(author=author)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
        return []

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

# Additional query examples using different patterns
def alternative_queries():
    """Show alternative ways to query the relationships"""
    print("\n--- Alternative Query Methods ---")
    
    # Alternative 1: Using double underscore syntax
    author_name = "J.K. Rowling"
    books = Book.objects.filter(author__name=author_name)
    print(f"Books by {author_name} (using __ syntax):")
    for book in books:
        print(f"- {book.title}")
    
    # Alternative 2: Using reverse relationship
    author = Author.objects.get(name="George Orwell")
    books = author.books.all()  # This uses the related_name='books'
    print(f"Books by {author.name} (using reverse relationship):")
    for book in books:
        print(f"- {book.title}")

# Example usage and demonstration
if __name__ == "__main__":
    print("=== Testing Django Relationship Queries ===")
    
    # Clean up any existing data first
    cleanup_existing_data()
    
    # Create fresh sample data
    print("\n1. Creating sample data...")
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    
    # Create library
    library = Library.objects.create(name="City Central Library")
    
    # Add books to library
    library.books.add(book1, book2, book3)
    
    # Create librarian
    librarian = Librarian.objects.create(name="Alice Johnson", library=library)
    
    print("Sample data created successfully!")
    
    # Test the queries
    print("\n2. Testing queries:")
    
    print("\n--- Query all books by J.K. Rowling ---")
    query_all_books_by_author("J.K. Rowling")
    
    print("\n--- List all books in City Central Library ---")
    list_all_books_in_library("City Central Library")
    
    print("\n--- Retrieve librarian for City Central Library ---")
    get_librarian_for_library("City Central Library")
    
    # Show alternative queries
    alternative_queries()
    
    print("\n=== Query testing completed ===")
