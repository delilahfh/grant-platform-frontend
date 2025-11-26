
document.getElementById("narReportForm").addEventListener("submit", async (e)=>{
  e.preventDefault();

  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  let sections;
  try { sections = JSON.parse(document.getElementById("sections").value); }
  catch { alert("Invalid JSON"); return; }

  const payload = { sections };

  const res = await fetch("https://grant-app-backend.onrender.com/narrative-report", {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(res.ok){
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Narrative_Report.docx";
    a.click();
  } else {
    alert("Error generating report");
  }
});
