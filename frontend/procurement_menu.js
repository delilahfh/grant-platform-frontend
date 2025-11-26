
const token = localStorage.getItem("jwt");
if(!token){ window.location.href="login.html"; }

fetch("https://grant-app-backend.onrender.com/me", {
  headers: { Authorization:`Bearer ${token}` }
});
