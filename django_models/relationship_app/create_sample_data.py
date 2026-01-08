import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create comprehensive sample data for testing views"""
    
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create authors
    authors_data = [
        {"name": "J.K. Rowling"},
        {"name": "George Orwell"},
        {"name": "Agatha Christie"},
        {"name": "Stephen King"},
        {"name": "Jane Austen"},
    ]
    
    authors = {}
    for data in authors_data:
        authors[data['name']] = Author.objects.create(**data)
    
    # Create books
    books_data = [
        {"title": "Harry Potter and the Sorcerer's Stone", "author": authors["J.K. Rowling"]},
        {"title": "Harry Potter and the Chamber of Secrets", "author": authors["J.K. Rowling"]},
        {"title": "1984", "author": authors["George Orwell"]},
        {"title": "Animal Farm", "author": authors["George Orwell"]},
        {"title": "Murder on the Orient Express", "author": authors["Agatha Christie"]},
        {"title": "And Then There Were None", "author": authors["Agatha Christie"]},
        {"title": "The Shining", "author": authors["Stephen King"]},
        {"title": "Pride and Prejudice", "author": authors["Jane Austen"]},
        {"title": "Sense and Sensibility", "author": authors["Jane Austen"]},
    ]
    
    books = {}
    for data in books_data:
        book = Book.objects.create(**data)
        books[data['title']] = book
    
    # Create libraries
    libraries_data = [
        {"name": "Central Public Library"},
        {"name": "City Library"},
        {"name": "University Library"},
        {"name": "Community Library"},
    ]
    
    libraries = {}
    for data in libraries_data:
        libraries[data['name']] = Library.objects.create(name=data['name'])
    
    # Add books to libraries (ManyToMany relationship)
    libraries["Central Public Library"].books.add(
        books["Harry Potter and the Sorcerer's Stone"],
        books["1984"],
        books["The Shining"],
        books["Pride and Prejudice"]
    )
    
    libraries["City Library"].books.add(
        books["Harry Potter and the Chamber of Secrets"],
        books["Animal Farm"],
        books["Murder on the Orient Express"],
        books["And Then There Were None"]
    )
    
    libraries["University Library"].books.add(
        books["1984"],
        books["Animal Farm"],
        books["Pride and Prejudice"],
        books["Sense and Sensibility"],
        books["The Shining"]
    )
    
    libraries["Community Library"].books.add(
        books["Murder on the Orient Express"],
        books["The Shining"],
        books["Harry Potter and the Sorcerer's Stone"]
    )
    
    # Create librarians (OneToOne relationship)
    librarians_data = [
        {"name": "Alice Johnson", "library": libraries["Central Public Library"]},
        {"name": "Bob Smith", "library": libraries["City Library"]},
        {"name": "Carol Williams", "library": libraries["University Library"]},
        {"name": "David Brown", "library": libraries["Community Library"]},
    ]
    
    for data in librarians_data:
        Librarian.objects.create(**data)
    
    print("Sample data created successfully!")
    print("\nSummary:")
    print(f"- Authors: {Author.objects.count()}")
    print(f"- Books: {Book.objects.count()}")
    print(f"- Libraries: {Library.objects.count()}")
    print(f"- Librarians: {Librarian.objects.count()}")
    
    return authors, books, libraries

if __name__ == "__main__":
    create_sample_data()