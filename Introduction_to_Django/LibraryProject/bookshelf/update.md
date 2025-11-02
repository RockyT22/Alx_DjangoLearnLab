book.title = "Nineteen Eighty-Four"
book.save()

Book.objects.get(id=book.id).title
