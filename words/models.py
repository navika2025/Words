from django.db import models

# Create your models here.
class TextReader(models.Model):
    file = models.FileField(upload_to='uploads/')
    lines = models.IntegerField()
    words = models.IntegerField()
    characters = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"file uploaded at {self.uploaded_at}"
    
        