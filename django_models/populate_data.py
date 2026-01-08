import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def populate_data():
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
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
    
    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    
    print("Data populated successfully!")
    print(f"Created {Author.objects.count()} authors")
    print(f"Created {Book.objects.count()} books")
    print(f"Created {Library.objects.count()} libraries")
    print(f"Created {Librarian.objects.count()} librarians")

if __name__ == "__main__":
    populate_data()