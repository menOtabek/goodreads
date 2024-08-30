from django.views.generic import ListView, DetailView

from .models import Book


class BooksListView(ListView):
    queryset = Book.objects.all()
    template_name = 'books_list.html'
    context_object_name = 'books_list'


class BookDetailView(DetailView):
    template_name = 'book_detail.html'
    model = Book
    context_object_name = 'book_detail'
