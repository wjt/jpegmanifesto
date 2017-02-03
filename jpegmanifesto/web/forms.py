from django.forms import ModelForm
from .models import UploadedImage

class UploadedImageForm(ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
