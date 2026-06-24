from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from book.models import Book
from authentication.models import CustomUser
from order.models import Order
from author.views import librarian_required

def book_list(request):
    books = Book.get_all()
    title = request.GET.get('title')
    if title:
        books = books.filter(name__icontains=title)
    author = request.GET.get('author')
    if author:
        books = books.filter(authors__name__icontains=author)

    return render(request, 'book/book_list.html', {'books': books})

@login_required
def book_detail(request, book_id):
    book = Book.get_by_id(book_id)
    if book is None:
        context = {'error': 'Book not found'}
    else:
        context = {'book': book}
    return render(request, 'book/book_detail.html', context)

@login_required
@librarian_required
def books_by_user(request, user_id):
    user = CustomUser.get_by_id(user_id)
    if user is None:
        context = {'error': 'User not found'}
    else:
        orders = Order.objects.filter(user=user, end_at__isnull=True)
        context = {'target_user': user, 'orders': orders}
    return render(request, 'book/books_by_user.html', context)
