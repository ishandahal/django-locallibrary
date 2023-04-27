from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Count of Genre that contains psychology
    num_psychology_genres = Genre.objects.filter(name__icontains="psychology").count()

    # Count of Book that contains the word catch
    num_book_with_phrase_catch = Book.objects.filter(title__icontains="catch").count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_psychology_genres": num_psychology_genres,
        "num_book_with_phrase_catch": num_book_with_phrase_catch,
    }

    # Render the HTML template with the data in the context variable
    return render(request, "index.html", context=context)
