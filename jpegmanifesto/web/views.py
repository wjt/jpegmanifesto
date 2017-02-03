from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import UploadedImage
from .forms import UploadedImageForm


def index(request):
    if request.method == 'POST':
        form = UploadedImageForm(request.POST, request.FILES)
        if form.is_valid():
            ui = UploadedImage(image=request.FILES['image'])
            ui.save()

            # TODO: background task(?)
            ui.mangle(10)

            return HttpResponseRedirect(reverse('image', kwargs={
                'public_id': str(ui.public_id),
            }))
    else:
        form = UploadedImageForm()
    context = {
        'form': form,
    }
    return render(request, 'web/index.html', context)


def image(request, public_id):
    ui = get_object_or_404(UploadedImage, public_id=public_id)
    context = {
        'image': ui,
    }
    return render(request, 'web/image.html', context)


def moar(request, public_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    ui = get_object_or_404(UploadedImage, public_id=public_id)
    ui.mangle(10)
    return HttpResponseRedirect(reverse('image', kwargs={
        'public_id': str(ui.public_id),
    }))
