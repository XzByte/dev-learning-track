const showPassword = document.querySelector('.show-password');
const passwordInput = document.querySelector('#password');

showPassword.addEventListener('click', () => {
  passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
  showPassword.classList.toggle('fa-eye');
  showPassword.classList.toggle('fa-eye-slash');
});