from django.db import models


class Customer(models.Model):
    nombre    = models.CharField(max_length=100)
    apellido  = models.CharField(max_length=100)
    email     = models.EmailField(unique=True)
    telefono  = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} {self.apellido} <{self.email}>"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
