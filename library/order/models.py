import datetime
from django.db import models
from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, blank=True)
    plated_end_at = models.DateTimeField(default=None)

    def __str__(self):
        return f"Order(id={self.id}, user={self.user.email}, book={self.book.name})"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        return {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id,
            'created_at': self.created_at,
            'end_at': self.end_at,
            'plated_end_at': self.plated_end_at,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        order = Order(user=user, book=book, plated_end_at=plated_end_at)
        order.save()
        return order

    @staticmethod
    def get_by_id(order_id):
        return Order.objects.filter(id=order_id).first()

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at:
            self.plated_end_at = plated_end_at
        if end_at:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return Order.objects.all()

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at__isnull=True)

    @staticmethod
    def delete_by_id(order_id):
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.delete()
            return True
        return False