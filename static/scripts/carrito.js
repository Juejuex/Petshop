const cartIcon = document.getElementById('cartIcon');
const cartMenu = document.getElementById('cartMenu');
const closeCart = document.getElementById('closeCart');

cartIcon.addEventListener('click', () => {
  cartMenu.classList.toggle('hidden');
});

closeCart.addEventListener('click', () => {
  cartMenu.classList.add('hidden');
});