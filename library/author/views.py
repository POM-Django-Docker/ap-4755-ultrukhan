from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from author.models import Author
from .forms import AuthorForm


def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 1:
            return redirect('books')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@librarian_required
def author_list_view(request):
    author_list = Author.get_all()
    context = {'All_author': author_list}
    return render(request, 'author/author_list.html', context)


@login_required
@librarian_required
def author_create_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'author/author_create.html', {'form': form})


@login_required
@librarian_required
def author_delete_view(request, author_id):
    search_author = Author.get_by_id(author_id)
    if search_author is None:
        return redirect('author_list')
    if search_author.books.exists():
        return redirect('author_list')
    Author.delete_by_id(author_id)
    return redirect('author_list')