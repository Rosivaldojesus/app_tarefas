from pyexpat import model
from django import forms

from .models import Task, Category

class CategoryForm(forms.ModelForm):
    #name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    #Wdescription = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Category
        exclude = ('owner',)


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        exclude = ('owner',)