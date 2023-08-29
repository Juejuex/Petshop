$(document).ready(function () {
    const searchInput = $('#search-input');
    const searchResults = $('#search-results');

    searchInput.on('input', function () {
      const query = searchInput.val();
      if (query.length >= 3) {
        $.ajax({
          url: '/buscar-productos/',  // Cambia esto a la URL de tu vista de búsqueda
          data: { query: query },
          success: function (data) {
            searchResults.html(data);
          }
        });
      } else {
        searchResults.empty();
      }
    });
  });