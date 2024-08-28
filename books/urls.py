from django.urls import path
from .views import BooksListView, BookDetailView
app_name='books'
urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('<int:pk>', BookDetailView.as_view(), name='book_detail')
]