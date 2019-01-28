from django.db import models

# Create your models here.
class Speaker(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    photo = models.URLField()
    website = models.URLField()
    description = models.TextField()

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'