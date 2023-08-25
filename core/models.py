from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Animal(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class ItemCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'Item en el carrito de {self.usuario.username}: {self.producto.nombre}'

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField()
    categorias = models.ManyToManyField(Categoria)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, default=1)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Venta {self.id} - {self.fecha_venta}'

    def clean(self):
        if self.detalleventa_set.count() == 0:
            raise ValidationError("Una venta debe tener al menos un detalle.")

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle Venta {self.id} - Venta {self.venta.id}'

    def clean(self):
        if self.cantidad > self.producto.cantidad_disponible:
            raise ValidationError("La cantidad vendida es mayor que la cantidad disponible.")
        if self.precio_unitario != self.producto.precio:
            raise ValidationError("El precio unitario no coincide con el precio del producto.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.producto.cantidad_disponible -= self.cantidad
        self.producto.save()


