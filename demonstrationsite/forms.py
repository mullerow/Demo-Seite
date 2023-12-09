from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, IndexCommentModel
from django import forms

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Benutzername', label_suffix="")
    email = forms.EmailField(label='E-mail-Adresse', label_suffix="")
    password1 = forms.CharField(label="Passwort", widget=forms.PasswordInput, label_suffix="")
    password2 = forms.CharField(label="Passwort (Wdh.)", widget=forms.PasswordInput, label_suffix="")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {'required': 'Dieses Feld muss ausgefüllt werden',
                          'max_length': 'Der Nutzername darf nicht länger als 100 Zeichen sein'},
        }

class UserAccountmanagmentForm(UserChangeForm):
    salutation_list = [('not_specified', 'keine Angabe'),
                       ('woman', 'Frau'),
                       ('mister', 'Herr'),
                       ('various', 'Divers')]

    salutation = forms.CharField(widget=forms.Select(choices=salutation_list))
    class Meta:
        model = CustomUser
        fields = ['email', 'it_reference', 'salutation', 'about_me', 'first_name', 'last_name', 'profile_image']
        widgets = {
            'about_me': forms.Textarea(attrs={'id': 'form_about_me_id', 'placeholder': 'Hier ist Platz für zusätzliche Angaben...'}),
        }

class CommentForm(forms.ModelForm):
    comment_username = forms.CharField(max_length=100)
    comment_it_reference = forms.CharField(max_length=100)
    comment_text = forms.CharField(widget=forms.Textarea, max_length=1000)
    class Meta:
        model = IndexCommentModel
        exclude = ['user', 'comment_image', 'comment-date']

        widgets = {
            'comment_text': forms.Textarea(attrs={'style': 'width:245px; height:250px'}),
        }

class ContactForm(forms.Form):
    sender_first_name = forms.CharField(max_length=100)
    sender_last_name = forms.CharField(max_length=100)
    message_subject = forms.CharField(max_length=200)
    email_message = forms.CharField(widget=forms.Textarea)
    sender_email = forms.EmailField()