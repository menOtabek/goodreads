from django.urls import path
from .views import BooksListView, BookDetailView, BookReviewCreate
app_name='books'
urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('<int:pk>', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/create/', BookReviewCreate.as_view(), name='review_create')
]