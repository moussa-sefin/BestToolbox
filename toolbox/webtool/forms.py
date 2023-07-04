from django import forms
from webtool.models import Post
from contactforms.forms import ContactForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contents', 'name','images', 'country']

class MyContactForm(ContactForm):
    subject = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)