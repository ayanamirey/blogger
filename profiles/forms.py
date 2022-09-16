from PIL import Image
from django.contrib.auth.models import User
from django import forms
from sqlparse import format

from profiles.models import Profile, ConnectToSocialAccount


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control-sm'}),
            'username': forms.TextInput(attrs={'class': 'form-control-sm'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': '8', 'style': 'resize: vertical'}),
            'location': forms.TextInput(attrs={'class': 'form-control-sm'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control-sm', 'type': 'date', 'style': 'width: 167px;'}),
            'avatar': forms.FileInput(attrs={'class': 'file-upload', 'required': False})
        }

class AvatarForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('avatar', 'x', 'y', 'width', 'height')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'file-upload', 'required': False})
        }

    def save(self):
        profile = super(AvatarForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.avatar)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((1000, 1000), Image.ANTIALIAS)
        resized_image.save(profile.avatar.path)

        return profile


class SocialNetworkForm(forms.ModelForm):
    class Meta:
        model = ConnectToSocialAccount
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
