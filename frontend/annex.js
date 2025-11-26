
document.getElementById("annexForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  let scores;
  try { scores = JSON.parse(document.getElementById("scores").value); }
  catch { alert("Invalid JSON"); return; }

  const res = await fetch("https://grant-app-backend.onrender.com/evaluation-annex", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify({ scores })
  });

  if(res.ok){
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Evaluation_Annex.docx";
    a.click();
  } else {
    alert("Error generating annex");
  }
});
