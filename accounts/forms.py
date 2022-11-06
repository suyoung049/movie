from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {
            "placeholder": "ID 입력",
            "class": "input-field",
        }
        self.fields["username"].help_text = None

        self.fields["password1"].widget.attrs = {
            "placeholder": "비밀번호 입력",
            "class": "input-field",
        }
        self.fields["password1"].help_text = None


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
        )
