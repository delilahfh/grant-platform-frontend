
document.getElementById("docsForm").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  const formData = new FormData(document.getElementById("docsForm"));

  const res = await fetch("https://grant-app-backend.onrender.com/supporting-documents", {
    method:"POST",
    headers:{ Authorization:`Bearer ${token}` },
    body: formData
  });

  if(res.ok){
    alert("Uploaded!");
    window.location.href="dashboard.html";
  } else {
    alert("Error uploading");
  }
});
