from django.contrib import admin

from .models import Book, Author, BookAuthor, BookReview

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'isbn']
    list_display = ['id', 'title', 'description', 'isbn']
    list_display_links = ['title', 'isbn']

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(BookAuthor)
admin.site.register(BookReview)
