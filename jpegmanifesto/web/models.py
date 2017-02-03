from contextlib import closing
import uuid

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.db.utils import IntegrityError

from ..transform import Transformer


def uploaded_image_path(instance, filename):
    '''Images are keyed by the UploadedImage's UUID; mangled images live in
    the same directory.'''
    u = str(instance.public_id)
    return 'uploads/{}/{}/{}/{}'.format(u[0:2], u[2:4], u, filename)


def validate_is_jpeg(value):
    if value.file.content_type != 'image/jpeg':
        raise ValidationError(
            'Upload a JPEG image. The image you uploaded had type %(t)s.',
            params={
                't': value.file.content_type,
            }
        )


class UploadedImage(models.Model):
    public_id = models.UUIDField(unique=True,
                                 default=uuid.uuid4,
                                 editable=False)

    image = models.ImageField(upload_to=uploaded_image_path,
                              width_field='width',
                              height_field='height',
                              validators=[validate_is_jpeg])
    width = models.PositiveIntegerField(editable=False)
    height = models.PositiveIntegerField(editable=False)

    def mangle(self, n, retry=5):
        self.image.open('rb')
        with closing(self.image):
            t = Transformer(jpeg=self.image)

        for _ in range(n):
            m = MangledImage(source=self)

            for _ in range(retry):
                content, stats = t.mangle()
                content = ContentFile(content)

                try:
                    # Deduplication will kick in and generate a fresh name
                    m.image.save(name=self.image.name, content=content)
                except IntegrityError:
                    # Not a well-formed image
                    m.image.delete(save=False)
                else:
                    break


class MangledImage(models.Model):
    source = models.ForeignKey(UploadedImage, on_delete=models.CASCADE,
                               related_name='mangled_images')
    image = models.ImageField(width_field='width',
                              height_field='height')
    width = models.PositiveIntegerField(editable=False)
    height = models.PositiveIntegerField(editable=False)
