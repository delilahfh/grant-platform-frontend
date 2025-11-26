
const token = localStorage.getItem("jwt");
if(!token){ window.location.href="login.html"; }

fetch("https://grant-app-backend.onrender.com/me", {
  headers: { Authorization: `Bearer ${token}` }
})
.then(r=>r.json())
.then(d=>{
 document.getElementById("user-info").innerHTML = "Welcome " + (d.name || "Applicant");
});
