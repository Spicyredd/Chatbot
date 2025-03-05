from django.db import models
import os
from django.db import models
from django.conf import settings


def upload_to_overwrite(instance, filename):
    file_path = os.path.join('files/', filename)

    # Delete existing file if it exists
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_path


class APIModel(models.Model):
    message = models.TextField()
    toggle = models.BooleanField(default=False)
    sender = models.CharField(max_length=100, default='You')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chatText

class APIModelFile(models.Model):
    pdf = models.FileField(upload_to=upload_to_overwrite)
    
    def __str__(self):
        return self.pdf