
const token = localStorage.getItem("jwt");
if(!token){ window.location.href="login.html"; }

fetch("https://grant-app-backend.onrender.com/authorized-files", {
    headers: { Authorization:`Bearer ${token}` }
})
.then(r=>r.json())
.then(list=>{
    let out = "";
    list.forEach(f=>{
        out += `<div><a href="${f.url}" download>${f.name}</a></div>`;
    });
    document.getElementById("files").innerHTML = out;
})
.catch(()=>{
    document.getElementById("files").innerHTML = "Error loading files.";
});
