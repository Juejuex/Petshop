document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
      const content = dropdown.querySelector('.absolute');
      dropdown.addEventListener('click', function(event) {
        event.stopPropagation();
        content.classList.toggle('hidden');
      });
    });
  
    window.addEventListener('click', function() {
      dropdowns.forEach(dropdown => {
        const content = dropdown.querySelector('.absolute');
        content.classList.add('hidden');
      });
    });
  });
  