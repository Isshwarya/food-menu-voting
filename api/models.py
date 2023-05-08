from django.db import models

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField()
    address = models.TextField("Address")
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
