#!/usr/bin/env python
"""
Sample queries demonstrating Django ORM relationships
Run with: python manage.py shell < relationship_app/query_samples.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing queries"""
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Agatha Christie")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    book5 = Book.objects.create(title="Murder on the Orient Express", author=author3)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Library")
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    
    # Create librarians (OneToOne relationship)
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!")
    return author1, library1, library2

def run_sample_queries():
    """Execute and demonstrate the required queries"""
    
    print("\n" + "="*60)
    print("DJANGO ORM RELATIONSHIP QUERY SAMPLES")
    print("="*60)
    
    # Create sample data first
    author1, library1, library2 = create_sample_data()
    
    print("\n" + "-"*60)
    print("1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR (ForeignKey)")
    print("-"*60)
    
    # Get author by name
    author = Author.objects.get(name="J.K. Rowling")
    
    # Query 1: All books by a specific author (ForeignKey reverse lookup)
    books_by_author = author.books.all()
    
    print(f"Author: {author.name}")
    print(f"Books by {author.name}:")
    for book in books_by_author:
        print(f"  - {book.title}")
    
    print("\n" + "-"*60)
    print("2. LIST ALL BOOKS IN A LIBRARY (ManyToManyField)")
    print("-"*60)
    
    # Query 2: All books in a library (ManyToMany relationship)
    library = Library.objects.get(name="Central Library")
    books_in_library = library.books.all()
    
    print(f"Library: {library.name}")
    print("Books in library:")
    for book in books_in_library:
        print(f"  - {book.title} (by {book.author.name})")
    
    print("\n" + "-"*60)
    print("3. RETRIEVE THE LIBRARIAN FOR A LIBRARY (OneToOneField)")
    print("-"*60)
    
    # Query 3: Librarian for a library (OneToOne relationship)
    library = Library.objects.get(name="Central Library")
    
    # Access through OneToOne relationship
    librarian = library.librarian
    
    print(f"Library: {library.name}")
    print(f"Librarian: {librarian.name}")
    
    print("\n" + "-"*60)
    print("ADDITIONAL QUERY EXAMPLES")
    print("-"*60)
    
    # Additional useful queries
    
    # Find all libraries containing a specific book
    book = Book.objects.get(title="1984")
    libraries_with_book = book.libraries.all()
    print(f"\nLibraries containing '{book.title}':")
    for lib in libraries_with_book:
        print(f"  - {lib.name}")
    
    # Find all authors with books in a library
    print(f"\nAuthors with books in '{library1.name}':")
    authors_in_library = Author.objects.filter(books__libraries=library1).distinct()
    for auth in authors_in_library:
        print(f"  - {auth.name}")
    
    # Count books by author
    print("\nNumber of books by each author:")
    for author in Author.objects.all():
        count = author.books.count()
        print(f"  - {author.name}: {count} book(s)")

def cleanup_data():
    """Clean up the sample data"""
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    print("\nSample data cleaned up.")

if __name__ == "__main__":
    try:
        run_sample_queries()
        # Uncomment the next line if you want to clean up after running
        # cleanup_data()
    except Exception as e:
        print(f"Error: {e}")