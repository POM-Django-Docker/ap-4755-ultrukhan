import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from order.models import Order
from book.models import Book
from .forms import OrderForm


def is_librarian(user):
    return user.is_authenticated and user.role == 1


@login_required
def order_list(request):
    if is_librarian(request.user):
        orders = Order.objects.select_related('user', 'book').all()
    else:
        orders = Order.objects.select_related('user', 'book').filter(user=request.user)
    return render(request, 'order/order_list.html', {
        'orders': orders,
        'is_librarian': is_librarian(request.user),
    })


@login_required
def my_orders(request):
    orders = Order.objects.select_related('book').filter(user=request.user)
    return render(request, 'order/my_orders.html', {'orders': orders})


@login_required
def order_create(request):
    if is_librarian(request.user):
        return HttpResponseForbidden("Librarians cannot create orders")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']

            if book.count < 1:
                form.add_error('book', 'This book is not available')
            else:
                already_ordered = Order.objects.filter(
                    user=request.user, book=book, end_at__isnull=True
                ).exists()
                if already_ordered:
                    form.add_error('book', 'You already have an active order for this book')
                else:
                    plated_end_at = datetime.datetime.now() + datetime.timedelta(weeks=2)
                    Order.create(user=request.user, book=book, plated_end_at=plated_end_at)
                    book.count -= 1
                    book.save()
                    return redirect('my_orders')
    else:
        form = OrderForm()

    return render(request, 'order/order_create.html', {'form': form})


@login_required
def order_close(request, order_id):
    if not is_librarian(request.user):
        return HttpResponseForbidden("Access denied")
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        if order.end_at is None:
            order.end_at = datetime.datetime.now()
            order.save()
            order.book.count += 1
            order.book.save()
        return redirect('order_list')
    return render(request, 'order/order_close_confirm.html', {'order': order})