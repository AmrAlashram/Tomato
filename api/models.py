from django.db import models

# Create your models here.

class ristorante(models.Model):
    nome = models.CharField(max_length=255, default="", unique=True)
    indirizzo = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.nome

class ingrediente(models.Model):
    nome = models.CharField(max_length=255, default="", unique=True)
    def __str__(self):
        return self.nome

class ricetta(models.Model):
    nome = models.CharField(max_length=255, default="", unique=True)
    ristorante = models.ManyToManyField(ristorante)
    ingrediente = models.ManyToManyField(ingrediente)
    def __str__(self):
        return self.nome
    



