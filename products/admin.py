from django.contrib import admin

from .models import Author, Book, Category, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'date_published']
    list_filter = ['genre', 'date_published']
    search_fields = ['title', 'author__name',]

    ordering = ('-created',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)
