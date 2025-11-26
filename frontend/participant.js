
const token = localStorage.getItem("jwt");
if(!token){ window.location.href="login.html"; }

fetch("https://grant-app-backend.onrender.com/me", {
  headers: { Authorization:`Bearer ${token}` }
})
.then(r=>r.json())
.then(d=>{
  if(d.role !== "participant"){
    alert("Not authorized");
    window.location.href="dashboard.html";
  }
});
