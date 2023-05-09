from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.utils import timezone
from .forms import CreateNoteForm
from .models import Notes


# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': ''
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('notes')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'})
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password not match'})


def notes(request):
    notes = Notes.objects.filter(
        user=request.user, dateCompleted__isnull=True)
    return render(request, 'notes.html', {'notes': notes})


def create_note(request):
    if request.method == 'GET':
        return render(request, 'create_notes.html', {'form': CreateNoteForm})
    else:
        try:
            form = CreateNoteForm(request.POST)
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            print(new_note)
            return redirect('notes')
        except ValueError:
            return render(request, 'create_notes.html', {'form': CreateNoteForm, 'error': 'please provide valid data'})


def note_detail(request, note_id):
    if request.method == 'GET':
        note = get_object_or_404(Notes, pk=note_id, user=request.user)
        form = CreateNoteForm(instance=note)
        return render(request, 'note_detail.html', {'note': note, 'form': form})
    else:
        try:
            note = get_object_or_404(Notes, pk=note_id, user=request.user)
            CreateNoteForm(request.POST, instance=note)
            form.save()
            return redirect('notes')
        except ValueError:
            return render(request, 'note_detail.html', {'note': note, 'form': form, 'error': "Error updating note"})


def complete_note(request, note_id):
    note = get_object_or_404(Notes, pk=note_id, user=request.user)
    if request.method == 'POST':
        note.dateCompleted = timezone.now()
        note.save()
        return redirect('notes')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect(notes)
