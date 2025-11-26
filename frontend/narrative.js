
let sections = [];

function addSection(){
  const title = document.getElementById("sectionTitle").value.trim();
  const content = document.getElementById("sectionContent").value.trim();
  if(!title || !content) return;

  sections.push({ title, content });
  document.getElementById("sectionsList").innerHTML = sections.map(s => 
    `<li><strong>${s.title}</strong>: ${s.content}</li>`
  ).join("");

  document.getElementById("sectionTitle").value = "";
  document.getElementById("sectionContent").value = "";
}

document.getElementById("narrativeForm").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const payload = { sections };

  const res = await fetch("https://grant-app-backend.onrender.com/narrative-proposal", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(res.ok){
    alert("Submitted!");
    window.location.href="dashboard.html";
  } else {
    alert("Error submitting");
  }
});
