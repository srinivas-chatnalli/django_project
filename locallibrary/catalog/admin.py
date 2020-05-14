from django.contrib import admin
from .models import Book, Author, Language, Genre, BookInstance
# Register your models here.

class BookInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance


class BookInline(admin.TabularInline):
    extra = 0
    model = Book

#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "language", "display_genre")
    list_filter = ("author", "genre")
    inlines = [BookInstanceInline]

#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "date_of_death")
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    #exclude = ["last_name"]
    inlines = [BookInline]

#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "imprint", "borrower", "due_back", "status")
    list_filter = ("due_back", "status")
    fieldsets = (
                (None, {'fields':('book', 'imprint', 'id')}), ('Availability',{'fields':('due_back', 'status', 'borrower')})
                )

admin.site.register(Language)
admin.site.register(Genre)
