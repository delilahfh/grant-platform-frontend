
const token = localStorage.getItem("jwt");
if(!token){ window.location.href="login.html"; }

// Load existing projects
fetch("https://grant-app-backend.onrender.com/projects", {
  headers: { Authorization:`Bearer ${token}` }
})
.then(r=>r.json())
.then(list=>{
  let out = "";
  list.forEach(p=>{
    out += `<div class='p'><strong>${p.title}</strong> — ${p.donor} (${p.months} months)</div>`;
  });
  document.getElementById("projects").innerHTML = out;
});

// Create new project
document.getElementById("projectForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const formData = new FormData();
  formData.append("title", document.getElementById("title").value);
  formData.append("donor", document.getElementById("donor").value);
  formData.append("months", document.getElementById("months").value);

  const branding = document.getElementById("branding").files[0];
  if(branding) formData.append("branding", branding);

  const res = await fetch("https://grant-app-backend.onrender.com/projects", {
    method:"POST",
    headers:{ Authorization:`Bearer ${token}` },
    body: formData
  });

  if(res.ok){
    alert("Project created");
    location.reload();
  } else {
    alert("Error");
  }
});
