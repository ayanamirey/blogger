from django.contrib.auth.models import User
from django import forms
from profiles.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    last_name = forms.CharField(required=False)
    username = forms.CharField(min_length=3)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')

    bio = forms.Textarea()
    location = forms.CharField(required=False)
    birth_date = forms.DateField(required=False,
                                 widget=forms.DateInput(format='%d-%m-%Y'),
                                 input_formats=('%d-%m-%Y',), help_text='Hint to date DD-MM-YYYY',
                                 )
