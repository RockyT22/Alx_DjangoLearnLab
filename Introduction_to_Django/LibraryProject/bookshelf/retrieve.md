all_books = Book.objects.all()
all_books

book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
