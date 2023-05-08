from django.forms import ModelForm
from .models import Notes


class CreateNoteForm(ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description', 'importance']
