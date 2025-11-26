
document.getElementById("evalForm").addEventListener("submit", async (e)=>{
  e.preventDefault();
  const token = localStorage.getItem("jwt");
  if(!token){ window.location.href="login.html"; return; }

  let scores;
  try { scores = JSON.parse(document.getElementById("scores").value); }
  except { alert("Invalid scores JSON"); return; }

  const payload = {
    eligibility: document.getElementById("eligibility").value,
    quality: document.getElementById("quality").value,
    preferential: document.getElementById("preferential").value,
    risks: document.getElementById("risks").value,
    selected_supplier: document.getElementById("selected").value,
    scores: scores
  };

  const res = await fetch("https://grant-app-backend.onrender.com/evaluation-report", {
    method: "POST",
    headers: {
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
    a.download = "Evaluation_Report.docx";
    a.click();
  } else {
    alert("Error generating evaluation report");
  }
});
