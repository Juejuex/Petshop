function cambiarCantidad(itemId, nuevaCantidad) {
  if (nuevaCantidad > 0) {
    $.ajax({
      url: `/cambiar_cantidad/${itemId}/${nuevaCantidad}/`,  // Cambia esto a la URL correcta en tu proyecto
      type: 'POST',
      data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
      success: function(response) {
        if (response.success) {
          location.reload();  // Actualizar la página después de cambiar la cantidad
        } else {
          alert(response.error);  // Mostrar el mensaje de error del servidor
        }
      },
      error: function() {
        alert('Error al cambiar la cantidad.');
      }
    });
  }
}
  function eliminarProducto(itemId) {
    if (confirm("¿Estás seguro de que deseas eliminar este producto del carrito?")) {
      $.ajax({
        url: `/eliminar_producto/${itemId}/`,  // Cambia esto a la URL correcta en tu proyecto
        type: 'POST',
        data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
        success: function(response) {
          location.reload();  // Actualizar la página después de eliminar el producto
        },
        error: function() {
          alert('Error al eliminar el producto.');
        }
      });
    }
  }
