from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_psychology_genres": num_psychology_genres,
        "num_book_with_phrase_catch": num_book_with_phrase_catch,
        "num_visits": num_visits,
    }

    # Render the HTML template with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksForLibrarians(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books loaned."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed.html"
    paginate_by = 10

    permission_required = "catalog.can_mark_returned"

    def get_queryset(self) -> QuerySet[Any]:
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")
