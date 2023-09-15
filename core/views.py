from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal



#Carrito

@login_required
def ver_carrito(request):
    items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)
    return render(request, 'ver_carrito.html', {'items': items, 'total': total})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    

    item, created = ItemCarrito.objects.get_or_create(
        producto=producto,
        usuario=request.user,  
        defaults={'cantidad': 1}
    )
    if not created:
        item.cantidad += 1
        item.save()
    
    return redirect('ver_carrito')  
@login_required
def eliminar_producto(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    item.delete()
    return redirect('ver_carrito')
@login_required
def cambiar_cantidad(request, item_id, nueva_cantidad):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    
    if nueva_cantidad <= 0:
        return JsonResponse({'success': False, 'error': 'La cantidad debe ser mayor que 0.'})
    
    if nueva_cantidad > item.producto.cantidad_disponible:
        return JsonResponse({'success': False, 'error': 'Cantidad supera el stock disponible.'})
    
    item.cantidad = nueva_cantidad
    item.save()
    
    return JsonResponse({'success': True})

    


#Manejo Cuentas

def inicio_sesion(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        # Intentar autenticar con nombre de usuario
        user_by_username = authenticate(request, username=username_or_email, password=password)

        # Intentar autenticar con correo electrónico
        user_by_email = None
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user_by_email = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            pass

        if user_by_username is not None:
            login(request, user_by_username)
            return redirect('index')  
        elif user_by_email is not None and user_by_email.check_password(password):
            login(request, user_by_email)
            return redirect('index')  # Cambiar 'home' por la URL de la página de inicio
        else:
            # Manejar el caso de credenciales inválidas aquí
            error_message = "Credenciales incorrectas, por favor inténtelo de nuevo."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def register(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            error_message = "Las contraseñas no coinciden."
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect('index.html')  # Cambiar 'index' por la URL de la página de inicio
            except IntegrityError:
                error_message = "El nombre de usuario o el correo electrónico ya están en uso. Por favor, elige otro nombre o correo."

    return render(request, 'register.html', {'error_message': error_message})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')  # Cambia 'index' por la URL de la página a la que deseas redirigir después del cierre de sesión

@login_required
def profile(request):
    return render(request, 'profile.html')



#Productos

def productos_por_categoria(request, categoria):
    productos = Producto.objects.filter(categorias__nombre=categoria)
    return render(request, 'categoria.html', {'productos': productos, 'categoria': categoria})

def producto_animal_categoria(request, animal_nombre, categoria_nombre):
    animal = get_object_or_404(Animal, nombre=animal_nombre)
    categoria = get_object_or_404(Categoria, nombre=categoria_nombre)
    
    productos = Producto.objects.filter(animal=animal, categorias=categoria)
    
    return render(request, 'categoria.html', {'productos': productos})

def productos_por_animal(request, animal_nombre):
    animal = get_object_or_404(Animal, nombre=animal_nombre)
    productos = Producto.objects.filter(animal=animal)
    
    return render(request, 'categoria.html', {'productos': productos})

def productos_por_categoria_marca(request, categoria_nombre, marca_nombre):
    categoria = get_object_or_404(Categoria, nombre=categoria_nombre)
    marca = get_object_or_404(Marca, nombre=marca_nombre)
    
    productos = Producto.objects.filter(categorias=categoria, marca=marca)
    
    return render(request, 'categoria.html', {'productos': productos, 'categoria': categoria, 'marca': marca})

def producto_individual(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    return render(request, 'producto_individual.html', {'producto': producto})


#Pago
@login_required
def procesar_pago(request):
    items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)

    return render(request, 'procesar_pago.html', {'items': items, 'total': total})
@login_required
def confirmacion_pago(request):
    if request.user.is_authenticated:
        # Obtén todos los elementos del carrito del usuario actual
        items = ItemCarrito.objects.filter(usuario=request.user)

        # Calcula el monto total del carrito antes de eliminarlo
        total_carrito = sum(item.producto.precio * item.cantidad for item in items)

        # Elimina los elementos del carrito del usuario
        items.delete()

        # Renderiza la página de confirmación de pago y pasa el monto total
        return render(request, 'confirmacion_pago.html', {'total_carrito': total_carrito})
    else:
        # Redirige al usuario a la página de inicio de sesión si no está autenticado
        return redirect('login')  # Asegúrate de ajustar el nombre de la URL de inicio de sesión según tu proyecto


@login_required   
def procesar_pago(request):
    return render(request,'formulario_compra.html')



#Templates
def index(request):
    categoria_alimento = Categoria.objects.get(nombre='Alimento')
    productos_alimento = Producto.objects.filter(categorias=categoria_alimento)
    oferta = "¡Oferta especial! 10% de descuento en todos los alimentos"
    return render(request, 'index.html', {'productos_alimento': productos_alimento, 'oferta': oferta})

def peo(request):
    return render(request, 'peo.html')

