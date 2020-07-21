from django import forms
from .models import *


class ImageForm(forms.ModelForm):

    class Meta:
        model = DailySituation
        # fields = ["name", "confirm_img", "daily_img"]
        fields = [
            "name",
            # "confirm_img",
            # "daily_img"
        ]
