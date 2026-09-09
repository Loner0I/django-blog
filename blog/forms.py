from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "message"]

    def clean_message(self):
        message = self.cleaned_data["message"]
        if "buyfollowers" in message.lower():
            raise forms.ValidationError("Your comment looks like spam and cannot be submitted.")
        return message
