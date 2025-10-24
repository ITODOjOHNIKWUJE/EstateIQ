// frontend/src/auth.js
export function saveToken(token) {
  localStorage.setItem('estateiq_token', token);
}
export function getToken() {
  return localStorage.getItem('estateiq_token');
}
export function removeToken() {
  localStorage.removeItem('estateiq_token');
}
