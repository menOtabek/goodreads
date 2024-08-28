from django.shortcuts import render
from django.views import View
from .models import Book

class BooksListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'books_list.html', {'books_list': books})

class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.filter(id=pk).first()
        return render(request, 'book_detail.html', {'book_detail': book})


