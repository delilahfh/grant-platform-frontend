const token=localStorage.getItem("jwt");
if(!token)location.href="login.html";

fetch("https://grant-app-backend.onrender.com/admin/inquiries",{headers:{Authorization:`Bearer ${token}`}})
.then(r=>r.json()).then(list=>{
 const tbody=document.querySelector("#inqA tbody");
 tbody.innerHTML="";
 list.forEach(i=>{
   const tr=document.createElement("tr");
   tr.innerHTML=`<td>${i.id}</td><td>${i.user_email}</td><td>${i.application_id}</td><td>${i.message}</td><td>${i.created_at}</td>`;
   tbody.appendChild(tr);
 })
});