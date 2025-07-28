from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import UserModel


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

class UserEditForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email')
        exclude = ('password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})