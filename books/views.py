from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Book


# class BooksListView(ListView):
#     queryset = Book.objects.all()
#     template_name = 'books_list.html'
#     context_object_name = 'books_list'
    # paginate_by = 2

class BooksListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_object = paginator.get_page(page_num)
        context = {
            'page_obj': page_object
        }
        return render(request, 'books_list.html', context)



class BookDetailView(DetailView):
    template_name = 'book_detail.html'
    model = Book
    context_object_name = 'book_detail'
