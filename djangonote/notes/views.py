from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from notes.models import Note, Tag
from notes.forms import NoteForm, TagForm
from django.utils.text import slugify
from django.contrib.auth.decorators import user_passes_test
from django import forms

def superuser_only(user):
    return (user.is_authenticated and user.is_superuser)


@user_passes_test(superuser_only, login_url="/")
def index_view(request):
    notes = Note.objects.all().order_by('-timestamp')
    tags = Tag.objects.all()
    context = {
        'notes': notes,
        'tags': tags
    }
    return render(request, 'notes/index.html', context)


@user_passes_test(superuser_only, login_url="/")
def add_note(request):

    id = request.GET.get('id', None)

    if id is not None:
        note = get_object_or_404(Note, id=id)
    else:
        note = None

    if request.method == 'POST':
        if request.POST.get('control') == 'delete':
            note.delete()
            messages.add_message(request, messages.INFO, 'Note Deleted!')
            return HttpResponseRedirect('notes:index')

        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Note Added!')
            return HttpResponseRedirect('notes:index')

    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/addnote.html', {'form':form, 'note':note})


@user_passes_test(superuser_only, login_url="/")
def add_tag(request):
    id = request.GET.get('id', None)

    if id is not None:
        tag = get_object_or_404(Tag, id=id)
    else:
        tag = None

    if request.method == 'POST':
        if request.POST.get('control') == 'delete':
            tag.delete()
            messages.add_message(request, messages.INFO, 'Tag Deleted!')
            return HttpResponseRedirect('notes.index_view')

        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Tag Added!')
            return HttpResponseRedirect('notes.index')
    else:
        form = TagForm(instance=tag)

    return render(request, 'notes/addtag.html', {'form': form, 'tag': tag})


@user_passes_test(superuser_only, login_url="/")
def tag_search(request, **kwargs):
    slug = kwargs['slug']
    tags = get_object_or_404(Tag, slug=slug)
    notes = tags.notes.all()
    context = {
        'notes': notes,
        'tags': tags
    }
    return render(request, 'notes/tagsearch.html', context)
