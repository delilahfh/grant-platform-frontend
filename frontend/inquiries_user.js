const token=localStorage.getItem("jwt");
if(!token)location.href="login.html";

document.getElementById("inqForm").onsubmit=async(e)=>{
 e.preventDefault();
 const res=await fetch("https://grant-app-backend.onrender.com/inquiries",{
  method:"POST",
  headers:{"Content-Type":"application/json",Authorization:`Bearer ${token}`},
  body:JSON.stringify({application_id:app.value,message:msg.value})
 });
 if(res.ok){alert("Sent");load();}
 else alert("Error");
}

function load(){
 fetch("https://grant-app-backend.onrender.com/inquiries",{headers:{Authorization:`Bearer ${token}`}})
 .then(r=>r.json()).then(list=>{
  const tbody=document.querySelector("#inqTable tbody");
  tbody.innerHTML="";
  list.forEach(i=>{
    const tr=document.createElement("tr");
    tr.innerHTML=`<td>${i.id}</td><td>${i.application_id}</td><td>${i.message}</td><td>${i.created_at}</td>`;
    tbody.appendChild(tr);
  })
 })
}
load();