
// Redirect users based on role after login
const token = localStorage.getItem("jwt");
if(!token){
  window.location.href = "login.html";
}

fetch("https://grant-app-backend.onrender.com/me", {
  headers: { Authorization: `Bearer ${token}` }
})
.then(r => r.json())
.then(d => {
  if(d.role === "admin"){
    window.location.href = "admin.html";
  } else if(d.role === "participant"){
    window.location.href = "participant_dashboard.html";
  } else {
    window.location.href = "dashboard.html";
  }
})
.catch(()=>{
  window.location.href="login.html";
});
