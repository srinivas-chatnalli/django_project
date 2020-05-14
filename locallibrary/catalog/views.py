from django.shortcuts import render, get_object_or_404
from . import views
from .models import Book, BookInstance, Author
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime

##Create
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
@login_required
def index(request):
    num_books = Book.objects.count()
    num_book_instances = BookInstance.objects.count()
    num_available_books = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    visits = request.session.get('visits', 0)
    request.session['visits'] = visits + 1

    context = {'num_books':num_books,
                'num_book_instances':num_book_instances,
                'num_available_books':num_available_books,
                'num_authors':num_authors,
                'num_visits':visits
              }
    return render(request, 'index.html',context)

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    #context_object_name='sri'
    #queryset = Book.objects.all()[:4]

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, ListView):
    model = Author

class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksLibrarianListView(PermissionRequiredMixin, ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrower_libraian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_books_librarian(request, pk):

    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse('borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back':proposed_renewal_date})
    context = {'form':form,
               'book_instance':book_instance
              }

    return render(request, 'catalog/book_renew_librarian.html', context)


####CreateView
class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'

class AuthorUpdateView(UpdateView):
    model = Author
    fields = '__all__'

class AuthorDeleteView(DeleteView):
    model = Author
    sucess_url = reverse_lazy('authors')

class BookCreateView(CreateView):
    model = Book
    fields = '__all__'

class BookInstanceCreateView(CreateView):
    model = BookInstance
    fields = '__all__'
