from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import BookReviewForms
from .models import Book, BookReview


# class BooksListView(ListView):
#     queryset = Book.objects.all()
#     template_name = 'books_list.html'
#     context_object_name = 'books_list'
# paginate_by = 2

class BooksListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)
        page_size = request.GET.get('page_size', 3)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_object = paginator.get_page(page_num)
        context = {
            'page_obj': page_object,
            'search_query': search_query
        }
        return render(request, 'books_list.html', context)


class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.filter(pk=pk).first()
        reviews = BookReview.objects.filter(book_id=book.id)
        review_form = BookReviewForms()
        context = {
            'book_detail': book,
            'reviews': reviews,
            'review_form': review_form
        }
        return render(request, 'book_detail.html', context)


class BookReviewCreate(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = Book.objects.filter(id=pk).first()
        review_form = BookReviewForms(data=request.POST)
        reviews = BookReview.objects.filter(book_id=book.id)
        context = {
            'book_detail': book,
            'reviews': reviews,
            'review_form': review_form
        }
        if not review_form.is_valid():
            return render(request, 'book_detail.html', context)
        BookReview.objects.create(book=book, user=request.user,
                                  comment=review_form.cleaned_data['comment'],
                                  stars_given=review_form.cleaned_data['stars_given'])
        return redirect(reverse('books:book_detail', kwargs={'pk':book.id}))
