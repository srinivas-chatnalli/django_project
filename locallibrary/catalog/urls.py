
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('bbooks/', views.LoanedBooksLibrarianListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_books_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('book/create/', views.BookCreateView.as_view(), name='book_create'),
    path('bookinstance/create/', views.BookInstanceCreateView.as_view(), name='book_instance'),
]
