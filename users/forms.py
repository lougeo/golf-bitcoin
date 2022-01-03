from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class FriendsInlineForm(forms.ModelForm):
    class Meta:
        model = User.friends.through
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     user_pk = kwargs.pop("user_pk", None)
    #     super().__init__(*args, **kwargs)

    #     self.fields["friends"].queryset = User.objects.exclude(pk=user_pk)

    def save(self, commit=True):
        super().save(commit=commit)

        User.friends.through.objects.kindle(
            self.instance.user, self.instance.friend, status=self.instance.status
        )

        return self.instance
