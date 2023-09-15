from django import forms

class FormularioDePago(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    direccion = forms.CharField(max_length=200, label="Dirección")
    numero_tarjeta = forms.CharField(max_length=16, label="Número de Tarjeta de Crédito")
    fecha_expiracion = forms.DateField(label="Fecha de Expiración (MM/YY)")
    cvv = forms.CharField(max_length=3, label="CVV")
    
    monto_total = forms.DecimalField(max_digits=10, decimal_places=2)