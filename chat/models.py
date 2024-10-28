
from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
