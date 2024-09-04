from django.db import models

class Name(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    name = models.ForeignKey(Name, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name.name} - {self.service}"
