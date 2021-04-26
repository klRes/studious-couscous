from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=500)
    lowercase_title = models.CharField(max_length=500)
    image = models.FileField(upload_to='images/')
    pdf_file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title